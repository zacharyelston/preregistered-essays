"""Polishing a selected essay (rule polish-1): a referee-report ratchet, then
citation verification. Runs after selection on the winner and never re-selects.

  ratchet    `rounds` times: the referee writes a journal-style report on the current
             essay; the writer revises; the referee compares current vs revised head to
             head, in both presentation orders, `compare_rounds` times each, in fresh
             sessions. The revision is kept only if it wins a strict majority of those
             verdicts, so the essay can only move to versions the referee prefers.
  citations  the writer lists its references; each is looked up in OpenAlex and
             Crossref (title similarity, year, first-author surname). Unmatched entries
             go back to the writer once, to correct or remove, changing nothing else.

Everything lives in <run>/polish/: its own pre-registration, chained log, request
queue and checkpoints. The parent run's files are only read. The first log record
pins the parent's final log hash and the sha256 of the essay it starts from.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from . import stages as S
from .backends import PendingResponse
from .log import RunLog
from .pipeline import PendingBatch, _llm
from .selection import load_rule, preregister

POLISH_RULE = {
    "version": "polish-1",
    "rounds": 3,
    "compare_rounds": 3,      # per presentation order: 2 x 3 = 6 verdicts per round
    "accept": "strict majority of the head-to-head verdicts, both orders",
    "max_words": 6000,
    # Classics carry several legitimate years (first paper, book, reprint, translation):
    # Kripke's Naming and Necessity is 1972 in the databases and 1980 as usually cited.
    # So a near-exact title plus a matching first-author surname verifies whatever the
    # year; the year difference is recorded, not failed.
    "citations": {"sources": ["openalex", "crossref"], "min_title_ratio": 0.85,
                  "year_tolerance": 1, "edition_title_ratio": 0.95, "fix_rounds": 1},
}


# -- citation lookup ------------------------------------------------------------
def _norm(s: str) -> str:
    """Lowercase, punctuation to spaces, single-spaced."""
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).split())


def _get_json(url: str, timeout: int = 20, tries: int = 4):
    """Paced and retried: unauthenticated OpenAlex/Crossref rate-limit bursts (two
    polish jobs at once got 40 of 51 OpenAlex lookups refused)."""
    req = urllib.request.Request(url, headers={"user-agent": "essay-citecheck/1"})
    for attempt in range(tries):
        time.sleep(0.5)                                  # pacing between requests
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == tries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == tries - 1:
                raise
        time.sleep(5 * 2 ** attempt)                     # 5, 10, 20 s


def lookup(ref: dict) -> list[dict]:
    """Candidate works for a reference from OpenAlex and Crossref (public APIs, no key;
    only the reference's own title and author are sent)."""
    out = []
    q = urllib.parse.quote(ref["title"])
    # OpenAlex meters keyless requests against a small daily budget shared per IP
    # (it ran out mid-polish); a key from $OPENALEX_API_KEY lifts that.
    key = os.environ.get("OPENALEX_API_KEY")
    auth = f"&api_key={urllib.parse.quote(key)}" if key else ""
    try:
        d = _get_json(f"https://api.openalex.org/works?search={q}&per_page=5{auth}")
        for w in d.get("results", []):
            out.append({"source": "openalex", "title": w.get("title") or "",
                        "year": w.get("publication_year"),
                        "authors": [((a.get("author") or {}).get("display_name") or "")
                                    for a in w.get("authorships", [])]})
    except Exception as e:  # noqa: BLE001 — a failed source is recorded, not fatal
        out.append({"source": "openalex", "error": repr(e)[:200]})
    biblio = urllib.parse.quote(" ".join([ref["title"], *ref["authors"][:1],
                                          str(ref["year"] or "")]))
    try:
        d = _get_json(f"https://api.crossref.org/works?query.bibliographic={biblio}&rows=5")
        for w in d.get("message", {}).get("items", []):
            year = None
            for k in ("published-print", "published-online", "issued"):
                parts = (w.get(k) or {}).get("date-parts") or [[None]]
                if parts and parts[0] and parts[0][0]:
                    year = parts[0][0]
                    break
            out.append({"source": "crossref", "title": " ".join(w.get("title") or []),
                        "year": year,
                        "authors": [a.get("family", "") for a in w.get("author", [])]})
    except Exception as e:  # noqa: BLE001
        out.append({"source": "crossref", "error": repr(e)[:200]})
    return out


def match(ref: dict, cands: list[dict], rule: dict) -> dict:
    """Verified if some candidate's title (or its main title, before a colon) is close
    enough, its year is within tolerance (when both are known), and the first author's
    surname appears among its authors (when both are known). Also verified, with
    year_note set, if the title is near-exact and the first author's surname is
    confirmed among the candidate's authors, whatever the year (editions)."""
    c = rule["citations"]
    t = _norm(ref["title"])
    best = {"verified": False, "ratio": 0.0, "candidate": None, "year_note": False}
    for cand in cands:
        if cand.get("error"):
            continue
        ct = _norm(cand["title"])
        ratio = max(difflib.SequenceMatcher(None, t, ct).ratio(),
                    difflib.SequenceMatcher(None, _norm(ref["title"].split(":")[0]),
                                            _norm(cand["title"].split(":")[0])).ratio())
        year_ok = (ref["year"] is None or cand.get("year") is None
                   or abs(int(cand["year"]) - int(ref["year"])) <= c["year_tolerance"])
        surname = _norm(ref["authors"][0]).split()[-1] if ref["authors"] else ""
        author_ok = (not surname or not cand["authors"]
                     or any(surname in _norm(a) for a in cand["authors"]))
        author_confirmed = bool(surname) and any(surname in _norm(a) for a in cand["authors"])
        strict = ratio >= c["min_title_ratio"] and year_ok and author_ok
        edition = ratio >= c["edition_title_ratio"] and author_confirmed
        ok = strict or edition
        if ok > best["verified"] or (ok == best["verified"] and ratio > best["ratio"]):
            best = {"verified": ok, "ratio": round(ratio, 3), "candidate": cand,
                    "year_note": ok and not year_ok}
    return best


# -- the polish run ---------------------------------------------------------------
class Polish:
    def __init__(self, run_dir: str, backends: dict | None = None, lookup_fn=lookup):
        self.parent = run_dir
        self.dir = os.path.join(run_dir, "polish")
        with open(os.path.join(run_dir, "config.json")) as f:
            self.config = json.load(f)
        self.log = RunLog(os.path.join(self.dir, "log.jsonl"))
        self._b = dict(backends or {})
        self.lookup = lookup_fn

    @classmethod
    def create(cls, run_dir: str, rule: dict | None = None, **kw) -> "Polish":
        d = os.path.join(run_dir, "polish")
        os.makedirs(os.path.join(d, "queue"))          # refuses if polishing already began
        sel = json.load(open(os.path.join(run_dir, "selection.json")))
        essay = open(os.path.join(run_dir, "final.md")).read()
        parent_log = RunLog(os.path.join(run_dir, "log.jsonl"))
        ok, why = parent_log.verify()
        if not ok:
            raise RuntimeError(f"parent run log failed verification: {why}")
        log = RunLog(os.path.join(d, "log.jsonl"))
        log.append("init", parent_run=os.path.basename(run_dir.rstrip("/")),
                   parent_log_head=parent_log.records()[-1]["hash"],
                   parent_winner=sel["winner"],
                   start_essay_sha256=hashlib.sha256(essay.encode()).hexdigest())
        preregister(d, log, rule or POLISH_RULE)
        with open(os.path.join(d, "queue", "README.md"), "w") as f:
            f.write("Polishing requests (see essay/polish.py).\n")
        return cls(run_dir, **kw)

    def _get(self, key, build):
        if key not in self._b:
            self._b[key] = build()
        return self._b[key]

    def writer(self):
        return self._get("writer", lambda: _llm(self.config["writer"], self.dir, "writer"))

    def objector(self):
        return self._get("objector", lambda: _llm(self.config["objector"], self.dir, "objector"))

    def _state(self) -> dict:
        p = os.path.join(self.dir, "state.json")
        return json.load(open(p)) if os.path.exists(p) else {}

    def _step(self, st: dict, key: str, fn):
        if key not in st:
            st[key] = fn()
            with open(os.path.join(self.dir, "state.json"), "w") as f:
                json.dump(st, f, indent=1, ensure_ascii=False)
        return st[key]

    def _compare(self, current: str, revised: str, rnd: int, rounds: int) -> dict:
        jobs = [(o, i) for o in ("current-first", "revised-first") for i in range(rounds)]
        verdicts, waiting = [], 0
        for order, i in jobs:
            a, b = (current, revised) if order == "current-first" else (revised, current)
            try:
                v = S.compare_essays(self.log, self.objector(), a, b, f"r{rnd}|{order}",
                                     i, stage=f"polish-compare-r{rnd}")
            except PendingResponse:
                waiting += 1
                continue
            except ValueError:
                v = {"better": None, "reason": "unparseable"}
            revised_slot = "B" if order == "current-first" else "A"
            verdicts.append({"order": order, "round": i, "better": v["better"],
                             "revised_won": v["better"] == revised_slot})
        if waiting:
            raise PendingBatch("polish", waiting)
        wins = sum(v["revised_won"] for v in verdicts)
        return {"revised_wins": wins, "of": len(verdicts),
                "accepted": wins * 2 > len(verdicts), "verdicts": verdicts}

    def run(self) -> dict:
        rule = load_rule(self.dir, self.log)
        st = self._state()
        mw = rule["max_words"]
        essay = open(os.path.join(self.parent, "final.md")).read()
        rounds = []
        for r in range(1, rule["rounds"] + 1):
            cur = essay
            try:
                report = self._step(st, f"r{r}.report",
                                    lambda: S.referee_report(self.log, self.objector(), cur, r))
                rev = self._step(st, f"r{r}.revise",
                                 lambda: S.revise(self.log, self.writer(), cur, report, r, mw))
                if S.word_count(rev) > mw:
                    rev = self._step(st, f"r{r}.fit",
                                     lambda: S.fit_length(self.log, self.writer(), rev, "polish", mw))
                verdict = self._step(st, f"r{r}.compare",
                                     lambda: self._compare(cur, rev, r, rule["compare_rounds"]))
            except PendingResponse:
                raise PendingBatch("polish", 1) from None
            if verdict["accepted"]:
                essay = rev
            rounds.append({"round": r, "accepted": verdict["accepted"],
                           "revised_wins": verdict["revised_wins"], "of": verdict["of"],
                           "words": S.word_count(essay), "major_issues": len(report["major"])})
            if f"r{r}.logged" not in st:
                self.log.append("stage", stage="polish-round", **rounds[-1])
                self._step(st, f"r{r}.logged", lambda: True)
        # citations
        cite = {}
        for tag in [f"c{i}" for i in range(rule["citations"]["fix_rounds"] + 1)]:
            cur = essay
            try:
                refs = self._step(st, f"{tag}.refs",
                                  lambda: S.list_references(self.log, self.writer(), cur, tag))
            except PendingResponse:
                raise PendingBatch("polish", 1) from None
            checked = self._step(st, f"{tag}.check", lambda: self._check(refs, rule))
            # only references a source answered for and did not match go to the writer
            bad = [c["ref"] for c in checked if not c["verified"] and not c.get("unchecked")]
            cite[tag] = {"references": len(checked), "unverified": len(bad),
                         "unchecked": sum(bool(c.get("unchecked")) for c in checked),
                         "unverified_list": bad}
            if not bad or tag == f"c{rule['citations']['fix_rounds']}":
                break
            try:
                essay = self._step(st, f"{tag}.fix",
                                   lambda: S.fix_references(self.log, self.writer(), cur, bad, mw))
            except PendingResponse:
                raise PendingBatch("polish", 1) from None
            if S.word_count(essay) > mw:
                fixed = essay
                essay = self._step(st, f"{tag}.fit", lambda: S.fit_length(
                    self.log, self.writer(), fixed, "polish", mw))
        with open(os.path.join(self.dir, "final.md"), "w") as f:
            f.write(essay)
        summary = {"rule_sha256": json.load(open(os.path.join(self.dir, "prereg.json")))["sha256"],
                   "rounds": rounds, "citations": cite, "words": S.word_count(essay),
                   "final_sha256": hashlib.sha256(essay.encode()).hexdigest(),
                   "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
        with open(os.path.join(self.dir, "summary.json"), "w") as f:
            json.dump(summary, f, indent=1)
        self.log.append("polish-done", **{k: summary[k] for k in ("rounds", "words", "final_sha256")},
                        citations={k: {kk: v[kk] for kk in ("references", "unverified")}
                                   for k, v in cite.items()})
        return summary

    def _check(self, refs: list[dict], rule: dict, stage: str = "citecheck") -> list[dict]:
        out = []
        for ref in refs:
            cands = self.lookup(ref)
            m = match(ref, cands, rule)
            errored = [c["source"] for c in cands if c.get("error")]
            # "unverified" needs every source to have answered without a match. A miss
            # with any source down is "unchecked": the sources' coverage differs
            # (Crossref alone misses many books and arXiv papers that OpenAlex has).
            unchecked = not m["verified"] and bool(errored)
            self.log.append("retrieval", stage=stage, ref=ref, verified=m["verified"],
                            unchecked=unchecked, ratio=m["ratio"], candidate=m["candidate"],
                            sources_errored=errored)
            out.append({"ref": ref, **m, "unchecked": unchecked})
        return out

    def ratchet_output(self) -> str:
        """The essay the ratchet ended on (before any citation fix), from checkpoints."""
        st = self._state()
        essay = open(os.path.join(self.parent, "final.md")).read()
        r = 1
        while f"r{r}.compare" in st:
            if st[f"r{r}.compare"]["accepted"]:
                essay = st.get(f"r{r}.fit") or st[f"r{r}.revise"]
            r += 1
        return essay

    def revert_citation_fix(self, note: str, reason: str) -> dict:
        """Restore the ratchet's output as the final essay, undoing a citation fix that
        should not have run. The human decision is logged verbatim; the superseded
        final is kept beside it, not deleted."""
        final_p = os.path.join(self.dir, "final.md")
        old = open(final_p).read()
        new = self.ratchet_output()
        if old == new:
            raise RuntimeError("final.md already equals the ratchet output; nothing to revert")
        with open(os.path.join(self.dir, "final.fixed-superseded.md"), "w") as f:
            f.write(old)
        with open(final_p, "w") as f:
            f.write(new)
        sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
        self.log.human(note)
        rec = {"from_sha256": sha(old), "to_sha256": sha(new), "reason": reason,
               "words": S.word_count(new)}
        self.log.append("revert-citation-fix", **rec)
        p = os.path.join(self.dir, "summary.json")
        summary = json.load(open(p))
        summary.update({"words": rec["words"], "final_sha256": rec["to_sha256"],
                        "citation_fix_reverted": rec})
        with open(p, "w") as f:
            json.dump(summary, f, indent=1)
        return rec

    def valid_fix(self) -> dict:
        """The rule's one citation fix pass, run from a valid check: the last
        `recheck` (every source answered) supplies the unverified references, which go
        to the writer once. Then the fixed essay's references are listed and checked.
        For entries whose original check was spoiled by lookup errors."""
        rule = load_rule(self.dir, self.log)
        st = self._state()
        mw = rule["max_words"]
        sp = os.path.join(self.dir, "summary.json")
        summary = json.load(open(sp))
        chk = summary.get("citations_final_check")
        if not chk or chk["unchecked"]:
            raise RuntimeError("needs a valid recheck first (every reference answered)")
        bad = chk["unverified"]
        essay = open(os.path.join(self.dir, "final.md")).read()
        if not bad:
            return {"fixed": 0}
        try:
            fixed = self._step(st, "v.fix", lambda: S.fix_references(
                self.log, self.writer(), essay, bad, mw))
            if S.word_count(fixed) > mw:
                pre = fixed
                fixed = self._step(st, "v.fit", lambda: S.fit_length(
                    self.log, self.writer(), pre, "polish", mw))
            refs = self._step(st, "v.refs", lambda: S.list_references(
                self.log, self.writer(), fixed, "v"))
        except PendingResponse:
            raise PendingBatch("polish", 1) from None
        checked = self._step(st, "v.check", lambda: self._check(refs, rule, stage="citecheck-valid"))
        with open(os.path.join(self.dir, "final.pre-validfix.md"), "w") as f:
            f.write(essay)
        with open(os.path.join(self.dir, "final.md"), "w") as f:
            f.write(fixed)
        sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
        res = {"sent_to_writer": bad, "references_after": len(checked),
               "verified_after": sum(c["verified"] for c in checked),
               "unchecked_after": sum(bool(c["unchecked"]) for c in checked),
               "unverified_after": [c["ref"] for c in checked
                                    if not c["verified"] and not c["unchecked"]],
               "from_sha256": sha(essay), "to_sha256": sha(fixed),
               "words": S.word_count(fixed)}
        self.log.append("citation-fix-valid", **{k: v for k, v in res.items()
                                                 if k not in ("sent_to_writer", "unverified_after")},
                        sent_n=len(bad), unverified_after_n=len(res["unverified_after"]))
        summary.update({"words": res["words"], "final_sha256": res["to_sha256"],
                        "citations_valid_fix": res})
        with open(sp, "w") as f:
            json.dump(summary, f, indent=1)
        return res

    def recheck(self, refs_key: str | None = None) -> dict:
        """Re-run the citation lookup on a reference list (default: the latest) without
        changing the essay (for a check spoiled by lookup errors). Appends to the log;
        the earlier records stay."""
        rule = load_rule(self.dir, self.log)
        st = self._state()
        last = refs_key or sorted(k for k in st if k.endswith(".refs"))[-1]
        checked = self._check(st[last], rule, stage="citecheck-recheck")
        res = {"of": last, "references": len(checked),
               "verified": sum(c["verified"] for c in checked),
               "unchecked": sum(c["unchecked"] for c in checked),
               "unverified": [c["ref"] for c in checked
                              if not c["verified"] and not c["unchecked"]],
               "year_notes": sum(bool(c.get("year_note")) for c in checked)}
        self.log.append("citecheck-recheck", **{k: v for k, v in res.items() if k != "unverified"},
                        unverified_n=len(res["unverified"]))
        p = os.path.join(self.dir, "summary.json")
        summary = json.load(open(p))
        summary["citations_final_check"] = res
        with open(p, "w") as f:
            json.dump(summary, f, indent=1)
        return res
