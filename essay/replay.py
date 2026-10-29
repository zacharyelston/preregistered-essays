"""Replay a finished run's frontier calls through small models: which pipeline roles
can a small model take over without changing what the pipeline decides?

For every logged writer/objector call (the frontier model's), each replay model gets
the identical system + user prompt, `k` times. Each answer is parsed the way its
stage parses it, then compared with the frontier answer at three levels:

  format          did it parse into what the stage needs (JSON shape, enum values)?
  decision        same novelty verdict / "addressed" verdict, severity within 1, and
                  for open stages size ratios (theses, steps, citations, words)
  counterfactual  substitute the small model's decisions into the run and recompute:
                  does the shortlist change (screen)? does the winner change
                  (objection-check)?

Decisions are scored on the first sample ("single") and on the k-sample majority
("vote"; median for severity), so test-time voting is measured in the same pass.

Results go to <run>/replay/<model>.jsonl (a chained RunLog, resumable: finished
(call, sample) pairs are skipped) and `summarize` writes <run>/replay/summary.json.
The run's own files are only read.
"""
from __future__ import annotations

import copy
import json
import os
import statistics
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from . import stages as S
from .log import RunLog
from .selection import rank, shortlist

ROLES = ("writer", "objector")
CATEGORICAL = {"novelty": "verdict", "objection-check": "addressed", "area": "area"}
SIZES = {"theses": "n", "steps": "n", "citations": "n", "draft": "words",
         "fit-length": "words", "respond": "words"}


def base_stage(stage: str) -> str:
    return "respond" if stage.startswith("respond-") else stage


def decide(stage: str, text: str) -> dict:
    """The decision a stage takes from one answer. Raises ValueError if the answer
    is unusable (that is the format failure)."""
    st = base_stage(stage)
    if st in ("draft", "fit-length"):
        words = S.word_count(text or "")
        if not words:
            raise ValueError("empty essay")
        return {"words": words}
    v = S.extract_json(text or "")
    if st == "area":
        cands = [c for c in v.get("candidates", []) if isinstance(c, dict) and c.get("area")]
        i = v.get("chosen", 0)
        if not cands or not isinstance(i, int) or not 0 <= i < len(cands):
            raise ValueError("no usable area choice")
        return {"area": cands[i]["area"]}
    if st in ("theses", "steps", "citations"):
        if not isinstance(v, list):
            raise ValueError(f"{st}: wanted a JSON array")
        return {"n": len(v)}
    if st == "objection":
        return {"severity": int(v["severity"])}
    if st == "novelty":
        if v.get("verdict") not in S.NOVELTY:
            raise ValueError(f"novelty verdict {v.get('verdict')!r}")
        return {"verdict": v["verdict"]}
    if st == "objection-check":
        if v.get("addressed") not in S.ADDRESSED:
            raise ValueError(f"addressed {v.get('addressed')!r}")
        return {"addressed": v["addressed"]}
    if st == "respond":
        essay = v.get("essay") or ""
        if not S.word_count(essay):
            raise ValueError("respond: no revised essay")
        return {"words": S.word_count(essay),
                "actions": [r.get("action") for r in v.get("responses", [])]}
    raise ValueError(f"no decision parser for stage {stage!r}")


def _try_decide(stage, text):
    try:
        return decide(stage, text), None
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        return None, str(e)[:200]


def frontier_calls(run_dir: str) -> list[dict]:
    log = RunLog(os.path.join(run_dir, "log.jsonl"))
    return [r for r in log.records() if r["kind"] == "call" and r.get("role") in ROLES
            and not r.get("error") and r.get("response") is not None]


def replay(run_dir: str, models: dict, k: int = 3, stages: set | None = None,
           workers: int = 4) -> dict:
    """models: name -> backend (`.complete(system, user, stage=...)`). Returns counts."""
    os.makedirs(os.path.join(run_dir, "replay"), exist_ok=True)
    calls = [c for c in frontier_calls(run_dir)
             if not stages or base_stage(c["stage"]) in stages]
    done_n = {}
    for name, be in models.items():
        log = RunLog(os.path.join(run_dir, "replay", f"{name}.jsonl"))
        have = {(r["orig_seq"], r["sample"]) for r in log.records() if r["kind"] == "replay"}
        todo = [(c, i) for c in calls for i in range(k) if (c["seq"], i) not in have]

        def one(job, be=be):
            c, i = job
            t0 = time.time()
            try:
                out = be.complete(c["system"], c["user"], stage=c["stage"])
                return job, {"response": out.text, "stop_reason": out.stop_reason,
                             "usage": out.usage, "model_served": out.model}, t0
            except Exception as e:  # noqa: BLE001 — a failure (e.g. context overflow) is data
                return job, {"error": repr(e)[:500]}, t0
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for (c, i), res, t0 in pool.map(one, todo):
                log.append("replay", orig_seq=c["seq"], role=c["role"], stage=c["stage"],
                           candidate=c.get("candidate"), sample=i, model=name,
                           latency_ms=round((time.time() - t0) * 1000), **res)
        done_n[name] = len(todo)
    return done_n


def _vote(stage, decisions):
    ok = [d for d in decisions if d]
    if not ok:
        return None
    st = base_stage(stage)
    if st == "objection":
        return {"severity": round(statistics.median(d["severity"] for d in ok))}
    key = CATEGORICAL.get(st) or SIZES.get(st)
    if st in CATEGORICAL:
        return {key: Counter(d[key] for d in ok).most_common(1)[0][0]}
    return {key: round(statistics.median(d[key] for d in ok))}


def _agree(stage, ref, got) -> dict:
    """Per-call agreement of one decision with the frontier's."""
    if got is None:
        return {"ok": False}
    st = base_stage(stage)
    if st == "objection":
        d = abs(got["severity"] - ref["severity"])
        return {"ok": True, "match": d <= 1, "abs_diff": d}
    if st in CATEGORICAL:
        key = CATEGORICAL[st]
        return {"ok": True, "match": got[key] == ref[key]}
    key = SIZES[st]
    return {"ok": True, "ratio": round(got[key] / ref[key], 3) if ref[key] else None}


def _label(stage: str) -> str | None:
    """The field compared exactly for chance-corrected agreement (None: open stages)."""
    st = base_stage(stage)
    return "severity" if st == "objection" else CATEGORICAL.get(st)


def _kappa(pairs: list) -> float | None:
    """Cohen's kappa, exact match; an unusable answer counts as its own label. None when
    the frontier gave one label throughout and the replay matched it (agreement is
    then uninformative: chance agreement is already 1)."""
    pairs = [(a, "<unusable>" if b is None else b) for a, b in pairs]
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return None if pe >= 1 else round((po - pe) / (1 - pe), 3)


def _tie_at_cut(screened: list[dict], rule: dict) -> bool:
    """True if the last kept and first dropped thesis have the same (novelty, severity):
    the shortlist was then decided by thesis id, i.e. the writer's listing order."""
    s = rule["screen"]
    keys = sorted((-S.NOVELTY[t["novelty"]["verdict"]], t["objection"]["severity"])
                  for t in screened if t["novelty"]["verdict"] not in s["exclude_novelty"])
    k = s["shortlist_k"]
    return len(keys) > k and keys[k - 1] == keys[k]


def _counterfactuals(run_dir: str, rule: dict, subs: dict) -> dict:
    """subs: (stage, candidate) -> decision. Recompute shortlist / winner with them."""
    out = {}

    def load(*p):
        path = os.path.join(run_dir, *p)
        return json.load(open(path)) if os.path.exists(path) else None
    screened, actual_sl = load("screened.json"), load("shortlist.json")
    if screened and actual_sl is not None:
        rows = copy.deepcopy(screened)
        n_sub = 0
        for t in rows:
            for st, field, key in (("objection", "objection", "severity"),
                                   ("novelty", "novelty", "verdict")):
                d = subs.get((st, t["id"]))
                if d:
                    t[field][key] = d[key]
                    n_sub += 1
        sl = shortlist(rows, rule)
        out["shortlist"] = {"actual": actual_sl, "replayed": sl, "same": sl == actual_sl,
                            "overlap": len(set(sl) & set(actual_sl)), "substituted": n_sub,
                            "actual_tie_at_cut": _tie_at_cut(screened, rule),
                            "replayed_tie_at_cut": _tie_at_cut(rows, rule)}
    sel = load("selection.json")
    cands = [c for c in (load("candidates", f"{i}.json") for i in (actual_sl or [])) if c]
    if sel and cands:
        cands = copy.deepcopy(cands)
        n_sub = 0
        for c in cands:
            d = subs.get(("objection-check", c["id"]))
            if d:
                c["final"]["objection_check"]["addressed"] = d["addressed"]
                n_sub += 1
        ranking = rank(cands, rule)
        winner = next((r["id"] for r in ranking if r["score"] > 0), None)
        out["winner"] = {"actual": sel.get("winner"), "replayed": winner,
                         "same": winner == sel.get("winner"), "substituted": n_sub}
    return out


def summarize(run_dir: str, rule: dict | None = None) -> dict:
    calls = {c["seq"]: c for c in frontier_calls(run_dir)}
    if rule is None:
        prereg = os.path.join(run_dir, "prereg.json")
        rule = json.load(open(prereg))["rule"] if os.path.exists(prereg) else None
    report = {"run": os.path.basename(run_dir.rstrip("/")), "models": {}}
    rdir = os.path.join(run_dir, "replay")
    for fn in sorted(os.listdir(rdir)) if os.path.isdir(rdir) else []:
        if not fn.endswith(".jsonl"):
            continue
        name = fn[:-6]
        samples: dict = {}
        for r in RunLog(os.path.join(rdir, fn)).records():
            if r["kind"] == "replay" and r["orig_seq"] in calls:
                samples.setdefault(r["orig_seq"], []).append(r)
        per_stage: dict = {}
        subs_single, subs_vote = {}, {}
        for seq, rs in samples.items():
            c = calls[seq]
            ref, _ = _try_decide(c["stage"], c["response"])
            if ref is None:
                continue                         # the frontier answer itself didn't parse
            rs = sorted(rs, key=lambda r: r["sample"])
            decs = [None if r.get("error") else _try_decide(c["stage"], r["response"])[0]
                    for r in rs]
            single, vote = decs[0], _vote(c["stage"], decs)
            row = per_stage.setdefault(base_stage(c["stage"]), {
                "calls": 0, "samples": 0, "format_ok": 0, "errors": 0,
                "single": [], "vote": [], "labels_single": [], "labels_vote": []})
            lab = _label(c["stage"])
            if lab:
                row["labels_single"].append((ref[lab], single and single[lab]))
                row["labels_vote"].append((ref[lab], vote and vote[lab]))
            row["calls"] += 1
            row["samples"] += len(rs)
            row["format_ok"] += sum(d is not None for d in decs)
            row["errors"] += sum(bool(r.get("error")) for r in rs)
            row["single"].append(_agree(c["stage"], ref, single))
            row["vote"].append(_agree(c["stage"], ref, vote))
            key = (base_stage(c["stage"]), c.get("candidate"))
            if single:
                subs_single[key] = single
            if vote:
                subs_vote[key] = vote
        stages_out = {}
        for st, row in per_stage.items():
            o = {"calls": row["calls"], "samples": row["samples"],
                 "format_ok_rate": round(row["format_ok"] / row["samples"], 3),
                 "errors": row["errors"]}
            for mode in ("single", "vote"):
                ag = row[mode]
                usable = [a for a in ag if a["ok"]]
                o[f"{mode}_usable"] = f"{len(usable)}/{len(ag)}"
                if usable and "match" in usable[0]:
                    o[f"{mode}_agree"] = round(sum(a["match"] for a in usable) / len(ag), 3)
                if usable and "ratio" in usable[0]:
                    rat = [a["ratio"] for a in usable if a["ratio"] is not None]
                    o[f"{mode}_size_ratio"] = round(statistics.median(rat), 3) if rat else None
                if usable and "abs_diff" in usable[0]:
                    o[f"{mode}_mean_abs_diff"] = round(
                        statistics.mean(a["abs_diff"] for a in usable), 2)
                if row[f"labels_{mode}"]:
                    o[f"{mode}_kappa"] = _kappa(row[f"labels_{mode}"])
            if row["labels_single"]:
                refs = [r for r, _ in row["labels_single"]]
                o["frontier_labels"] = dict(Counter(refs))
                # what "always answer the frontier's most common label" would score
                o["majority_baseline_agree"] = round(
                    Counter(refs).most_common(1)[0][1] / len(refs), 3)
            stages_out[st] = o
        m = {"stages": stages_out}
        if rule:
            m["counterfactual_single"] = _counterfactuals(run_dir, rule, subs_single)
            m["counterfactual_vote"] = _counterfactuals(run_dir, rule, subs_vote)
        report["models"][name] = m
    with open(os.path.join(run_dir, "replay", "summary.json"), "w") as f:
        json.dump(report, f, indent=1)
    return report
