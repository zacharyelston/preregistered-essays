"""The stage prompts and their parsers. Each stage is one (or a few) logged calls
and returns plain data; `pipeline.py` decides what to persist and when.

Role split (so no model grades its own work):
  writer    proposes theses, drafts, extracts argument steps, answers critic flags,
            lists its citations
  objector  strongest objection, novelty verdict, and the final "was the objection
            actually answered?" check
  critic    the fallacy-restraint hat (and its base as the placebo arm), one short
            self-contained argument per call — the shape it was trained on
"""
from __future__ import annotations

import json
import re

from .backends import Backend, MyvectRetriever, call
from .log import RunLog

# Verbatim instruction prefix from the fallacy-restraint training data
# (train/recovered/fv2-cfg/fallacy_v2_train.jsonl). Change it and the hat is off-distribution.
FALLACY_PREFIX = ("You identify logical fallacies in arguments. Name the fallacy (or say "
                  "\"no fallacy\") and explain briefly why, citing the flaw in the reasoning. "
                  "Base your judgments on Kelley, The Art of Reasoning.")

WRITER_SYSTEM = (
    "You are the sole author of an original essay in analytic philosophy. It will be "
    "judged blind by professional philosophers on one question: to what extent do its "
    "ideas and arguments make a valuable contribution to philosophical knowledge. "
    "Style is not graded. Develop the positions and arguments yourself.")

OBJECTOR_SYSTEM = (
    "You are a demanding referee for a top philosophy journal. You are not the author "
    "and owe the author nothing. Be specific, cite the literature where you can, and "
    "say plainly when an argument fails.")


def extract_json(text: str):
    """First JSON value in `text` (tolerates ```json fences and prose around it)."""
    text = re.sub(r"```(?:json)?", "", text)
    starts = [i for i in (text.find("["), text.find("{")) if i >= 0]
    if not starts:
        raise ValueError("no JSON in response")
    return json.JSONDecoder().raw_decode(text[min(starts):])[0]


def call_json(log: RunLog, backend: Backend, *, retries: int = 1, **kw):
    """`call()` + JSON parse; on a parse failure re-ask once (that call is logged too)."""
    user = kw.pop("user")
    for attempt in range(retries + 1):
        text = call(log, backend, user=user, **kw)
        try:
            return extract_json(text)
        except ValueError as e:
            if attempt == retries:
                raise ValueError(f"{kw.get('stage')}: unparseable JSON after retry") from e
            user = (user + "\n\nYour previous reply could not be parsed. Reply with the "
                    "JSON value only.")


def choose_area(log, writer, k: int = 5, avoid: list[str] | None = None) -> dict:
    """The writer picks the area itself, so the topic is AI-originated too. `avoid`:
    areas another entry already took (a topic constraint, no philosophical content)."""
    taken = ("" if not avoid else " Another entry already covers the following, so choose "
             "a clearly different area and question: " + "; ".join(avoid) + ".")
    user = (f"Survey philosophy as a whole and name {k} areas, each with one open question "
            "in it, where you believe you could make a genuinely original contribution in a "
            "6,000-word essay. Then choose the one where your contribution would be most "
            f"valuable.{taken} Reply with a JSON object: {{\"candidates\": [{{\"area\": str, "
            "\"question\": str, \"why\": str}], \"chosen\": int (0-based index), "
            "\"reason\": str}.")
    r = call_json(log, writer, role="writer", stage="area", system=WRITER_SYSTEM, user=user)
    cands = [c for c in r.get("candidates", []) if isinstance(c, dict) and c.get("area")]
    if not cands:
        raise ValueError("area: no candidate areas in reply")
    i = r.get("chosen", 0)
    i = i if isinstance(i, int) and 0 <= i < len(cands) else 0
    pick = cands[i]
    return {"area": pick["area"], "question": pick.get("question", ""),
            "reason": r.get("reason", ""), "candidates": cands, "chosen": i}


def area_text(a: dict) -> str:
    return f"{a['area']} (open question: {a['question']})" if a.get("question") else a["area"]


def propose_theses(log, writer, area: str, n: int) -> list[dict]:
    user = (f"Area: {area}\n\nPropose {n} distinct candidate theses for a 6,000-word essay "
            "in this area. Each should be a definite, contestable claim you could defend "
            "with a novel argument, not a survey. Reply with a JSON array of objects with "
            "keys: title, thesis, argument_sketch (3-6 sentences), why_new (what this adds "
            "beyond the existing literature).")
    rows = call_json(log, writer, role="writer", stage="theses", system=WRITER_SYSTEM, user=user)
    return [{"id": f"t{i:02d}", **{k: r.get(k, "") for k in
             ("title", "thesis", "argument_sketch", "why_new")}}
            for i, r in enumerate(rows[:n], 1)]


def _thesis_block(t: dict) -> str:
    return f"Thesis: {t['thesis']}\n\nArgument sketch: {t['argument_sketch']}"


def objection(log, objector, t: dict) -> dict:
    user = (_thesis_block(t) + "\n\nGive the single strongest objection to this thesis "
            "and argument. Then rate how damaging it is if unanswered, 1 (minor) to 5 "
            "(fatal). Reply with a JSON object: {\"objection\": str, \"severity\": int, "
            "\"rationale\": str}.")
    r = call_json(log, objector, role="objector", stage="objection", system=OBJECTOR_SYSTEM,
                  user=user, candidate=t["id"])
    return {"objection": r.get("objection", ""), "severity": int(r.get("severity", 5)),
            "rationale": r.get("rationale", "")}


NOVELTY = {"novel": 1.0, "partly": 0.5, "known": 0.0}


def novelty(log, objector, t: dict) -> dict:
    user = (_thesis_block(t) + "\n\nHas this thesis, or substantially this argument for "
            "it, already been published? Name the closest existing work. Reply with a "
            "JSON object: {\"verdict\": \"novel\" | \"partly\" | \"known\", "
            "\"closest_work\": [{\"work\": str, \"relation\": str}], \"note\": str}.")
    r = call_json(log, objector, role="objector", stage="novelty", system=OBJECTOR_SYSTEM,
                  user=user, candidate=t["id"])
    v = r.get("verdict", "known")
    return {"verdict": v if v in NOVELTY else "known",
            "closest_work": r.get("closest_work", []), "note": r.get("note", "")}


def draft(log, writer, t: dict, obj: dict, max_words: int,
          target_words: int | None = None) -> str:
    length = (f"aim for about {target_words} words before the references (hard limit "
              f"{max_words})" if target_words else
              f"at most {max_words} words before the references")
    user = (_thesis_block(t) + f"\n\nThe strongest objection a referee raised:\n{obj['objection']}"
            f"\n\nWrite the essay in Markdown, {length}. "
            "It must answer that objection in the text. End with a "
            "'## References' section listing every work you cite.")
    return call(log, writer, role="writer", stage="draft", system=WRITER_SYSTEM,
                user=user, candidate=t["id"])


def extract_steps(log, writer, essay: str, cid: str, max_steps: int = 25) -> list[str]:
    user = (f"Essay:\n\n{essay}\n\nList the essay's main inferential steps, at most "
            f"{max_steps}. Restate each as a short self-contained argument a reader could "
            "evaluate without the essay: its premises, then 'Therefore, ...'. Reply with a "
            "JSON array of strings.")
    steps = call_json(log, writer, role="writer", stage="steps", system=WRITER_SYSTEM,
                      user=user, candidate=cid)
    return [s for s in steps if isinstance(s, str) and s.strip()][:max_steps]


# Prose verdicts, for arms that don't answer in the trained format (the base model
# behind the placebo arm writes "The argument ... does not contain any obvious
# logical fallacies" or a bolded list of named fallacies). Reading every
# non-"No fallacy" opening as a flag made the placebo look like it flagged 8/8
# steps of the PoC essay when it named fallacies in 3.
_NONE = re.compile(r"\bno (?:obvious |clear |apparent )?(?:logical )?fallac|"
                   r"\b(?:does not|doesn't|do not) (?:appear to |seem to )?(?:contain|commit|"
                   r"involve|exhibit) (?:any |a )?(?:obvious |clear )?(?:logical )?fallac|"
                   r"\bis not (?:a |an )?(?:fallacy|fallacious)", re.I)
_BOLD = re.compile(r"\*\*([^*\n]{3,60})\*\*")
# A bolded heading counts as a flag only if it names a fallacy (Kelley's families
# plus common aliases) — base-model answers also bold section titles.
_FALLACY_NAMES = re.compile(
    r"hominem|tu quoque|appeal to|begging|circular|petitio|composition|division|"
    r"dilemma|dichotomy|straw|equivocation|amphiboly|ambiguity|vagueness|hasty|"
    r"generali[sz]ation|slippery|post hoc|false cause|non sequitur|red herring|"
    r"affirming|denying|consequent|antecedent|two wrongs|complex question|"
    r"loaded question|gambler|accident|special pleading|no true|genetic|"
    r"(?<!no )fallacy", re.I)


def parse_verdict(text: str) -> dict:
    """Three-way verdict: 'fallacy' | 'no_fallacy' | 'unclear' (only 'fallacy' flags).

    The hat answers 'No fallacy. ...' or 'Fallacy: <name>. ...'; other arms are read
    from their opening: a no-fallacy statement in the first sentence, or a named
    (bolded) fallacy in the first 400 characters."""
    t = (text or "").strip()
    out = lambda v, name=None: {"flag": v == "fallacy", "verdict": v, "fallacy": name,
                                "explanation": t}
    if re.match(r"no fallacy", t, re.I):
        return out("no_fallacy")
    m = re.match(r"fallacy\s*:\s*([^.\n]+)", t, re.I)
    if m:
        return out("fallacy", m.group(1).strip())
    first = re.split(r"(?<=[.!?:])\s", t, maxsplit=1)[0]
    if _NONE.search(first):
        return out("no_fallacy")
    head = t[:400]
    named = [b.strip() for b in _BOLD.findall(head) if _FALLACY_NAMES.search(b)]
    if named:
        return out("fallacy", named[0])
    if _NONE.search(head) or any(re.fullmatch(r"\s*no fallacy\W*", b, re.I)
                                 for b in _BOLD.findall(head)):
        return out("no_fallacy")
    return out("unclear")


def critique(log, critic, steps: list[str], cid: str, arm: str, rnd: int) -> list[dict]:
    out = []
    for i, step in enumerate(steps, 1):
        # the verdict is the opening sentence; a long-winded arm running out of
        # tokens (the base model writes prose) doesn't invalidate it
        text = call(log, critic, role=f"critic:{arm}", stage=f"critique-r{rnd}",
                    user=FALLACY_PREFIX + "\n\n" + step, candidate=cid,
                    allow_truncated=True)
        out.append({"step": i, "text": step, **parse_verdict(text)})
    return out


def respond(log, writer, essay: str, flags: list[dict], cid: str, rnd: int,
            max_words: int) -> tuple[list, str]:
    listing = "\n\n".join(f"[{f['step']}] {f['text']}\n  Critic: {f['explanation']}"
                          for f in flags)
    user = (f"Essay:\n\n{essay}\n\nAn automated fallacy critic flagged these argument steps. "
            "It is known to over-flag sound arguments about 15% of the time, so treat each "
            "flag as a claim to check, not a verdict. For each, either fix the essay or "
            "defend the step as sound. The revised essay must stay within "
            f"{max_words} words before the references: if a fix adds text, cut elsewhere. "
            "Reply with a JSON object: {\"responses\": "
            "[{\"step\": int, \"action\": \"fix\" | \"defend\", \"reason\": str}], "
            "\"essay\": str (the full revised essay in Markdown)}.\n\nFlags:\n\n" + listing)
    r = call_json(log, writer, role="writer", stage=f"respond-r{rnd}", system=WRITER_SYSTEM,
                  user=user, candidate=cid)
    return r.get("responses", []), r.get("essay") or essay


def fit_length(log, writer, essay: str, cid: str, max_words: int) -> str:
    """Cut an over-length essay to the limit without changing its arguments."""
    user = (f"Essay:\n\n{essay}\n\nThis essay is {word_count(essay)} words before the "
            f"references; the hard limit is {max_words}. Cut it to at most {max_words} words "
            "without dropping or weakening any argument, objection or reply: tighten prose, "
            "merge repetition, trim examples. Keep the '## References' section, removing only "
            "works no longer cited. Reply with the full revised essay in Markdown only.")
    return call(log, writer, role="writer", stage="fit-length", system=WRITER_SYSTEM,
                user=user, candidate=cid)


def citations(log, writer, essay: str, cid: str) -> list[dict]:
    user = (f"Essay:\n\n{essay}\n\nList every claim the essay attributes to a specific "
            "published work. Reply with a JSON array of objects: {\"work\": str "
            "(author, title, year), \"claim\": str (what the essay says the work says)}.")
    rows = call_json(log, writer, role="writer", stage="citations", system=WRITER_SYSTEM,
                     user=user, candidate=cid)
    return [{"work": r.get("work", ""), "claim": r.get("claim", "")} for r in rows]


def ground(log, retriever: MyvectRetriever | None, cites: list[dict], cid: str,
           min_score: float) -> list[dict] | None:
    """Look each attributed claim up in the RAG boxes. None = grounding not configured."""
    if retriever is None:
        return None
    out = []
    for c in cites:
        q = f"{c['work']} {c['claim']}"
        try:
            hits = retriever.search(q, k=3)
        except Exception as e:  # noqa: BLE001 — on the record, then re-raise
            log.append("retrieval", stage="ground", candidate=cid, query=q,
                       boxes=retriever.boxes, error=repr(e))
            raise
        log.append("retrieval", stage="ground", candidate=cid, query=q,
                   boxes=retriever.boxes, hits=hits)
        top = max((h.get("score", 0.0) for h in hits), default=0.0)
        out.append({**c, "top_score": top, "found": top >= min_score})
    return out


ADDRESSED = {"yes": 1.0, "partly": 0.5, "no": 0.0}


def check_objection(log, objector, obj: dict, essay: str, cid: str) -> dict:
    user = (f"You raised this objection:\n{obj['objection']}\n\nHere is the final essay:\n\n"
            f"{essay}\n\nDoes the essay answer the objection adequately? Reply with a JSON "
            "object: {\"addressed\": \"yes\" | \"partly\" | \"no\", \"reason\": str}.")
    r = call_json(log, objector, role="objector", stage="objection-check",
                  system=OBJECTOR_SYSTEM, user=user, candidate=cid)
    a = r.get("addressed", "no")
    return {"addressed": a if a in ADDRESSED else "no", "reason": r.get("reason", "")}


COMPARE_FORMAT = ("Reply with a JSON object: {\"better\": \"A\" | \"B\", \"reason\": str}.")


def compare_essays(log, referee, essay_a: str, essay_b: str, pair: str, rnd: int,
                   stage: str = "final-compare") -> dict:
    """Rule v3's final: which of two finished essays makes the more valuable
    contribution. The format is restated after the essays: small models dropped an
    up-front format instruction on long prompts."""
    user = ("Two complete philosophy essays follow. Each will be judged blind by "
            "professional philosophers on one question: to what extent do its ideas and "
            "arguments make a valuable contribution to philosophical knowledge. Style is "
            "not graded. Which essay makes the more valuable contribution? "
            f"{COMPARE_FORMAT}\n\n=== Essay A ===\n\n{essay_a}\n\n=== Essay B ===\n\n"
            f"{essay_b}\n\n=== End ===\n\nWhich essay makes the more valuable contribution? "
            f"{COMPARE_FORMAT}")
    r = call_json(log, referee, role="objector", stage=f"{stage}-{rnd}",
                  system=OBJECTOR_SYSTEM, user=user, candidate=pair)
    better = str(r.get("better", "")).strip().upper() if isinstance(r, dict) else ""
    return {"better": better if better in ("A", "B") else None,
            "reason": r.get("reason", "") if isinstance(r, dict) else ""}


# -- polishing (rule polish-1): referee report -> revision -> head-to-head ratchet,
# then citation verification. All prompts are generic: no position or argument.
CRITERIA = ("clarity; quality of argumentation; significance; originality; engagement "
            "with the literature; accuracy and scholarship")
REPORT_FORMAT = ("Reply with a JSON object: {\"contribution\": str, \"major\": [str], "
                 "\"minor\": [str]}.")


def referee_report(log, referee, essay: str, rnd: int) -> dict:
    user = (f"Essay:\n\n{essay}\n\n=== End of essay ===\n\nWrite a referee report on this "
            "essay as for a top philosophy journal. It will be judged on: " + CRITERIA +
            ". State its central contribution, then its most important problems, most "
            f"serious first. {REPORT_FORMAT}")
    r = call_json(log, referee, role="objector", stage=f"polish-report-{rnd}",
                  system=OBJECTOR_SYSTEM, user=user, candidate="polish")
    r = r if isinstance(r, dict) else {}
    return {"contribution": str(r.get("contribution", "")),
            "major": [str(x) for x in r.get("major", []) if x],
            "minor": [str(x) for x in r.get("minor", []) if x]}


def revise(log, writer, essay: str, report: dict, rnd: int, max_words: int) -> str:
    listing = ("Contribution (as the referee sees it): " + report["contribution"] +
               "\n\nMajor issues:\n" + "\n".join(f"- {x}" for x in report["major"]) +
               "\n\nMinor issues:\n" + "\n".join(f"- {x}" for x in report["minor"]))
    user = (f"Essay:\n\n{essay}\n\n=== End of essay ===\n\nA referee's report:\n\n{listing}"
            "\n\nRevise the essay in response. Address the points you judge correct; where "
            "you judge a point mistaken, you may leave the essay as it is. Stay within "
            f"{max_words} words before the references. Reply with the full revised essay in "
            "Markdown only, ending with a '## References' section.")
    return call(log, writer, role="writer", stage=f"polish-revise-{rnd}", system=WRITER_SYSTEM,
                user=user, candidate="polish")


def list_references(log, writer, essay: str, tag: str) -> list[dict]:
    user = (f"Essay:\n\n{essay}\n\n=== End of essay ===\n\nList every entry in the essay's "
            "References section. Reply with a JSON array of objects: {\"authors\": [surnames], "
            "\"title\": str, \"year\": int or null}. JSON only.")
    rows = call_json(log, writer, role="writer", stage=f"polish-refs-{tag}", system=WRITER_SYSTEM,
                     user=user, candidate="polish")
    out = []
    for r in rows if isinstance(rows, list) else []:
        if isinstance(r, dict) and r.get("title"):
            y = r.get("year")
            out.append({"authors": [str(a) for a in r.get("authors", []) if a],
                        "title": str(r["title"]), "year": y if isinstance(y, int) else None})
    return out


def fix_references(log, writer, essay: str, unverified: list[dict], max_words: int) -> str:
    listing = "\n".join(f"- {', '.join(r['authors'])} ({r['year']}), {r['title']}"
                        for r in unverified)
    user = (f"Essay:\n\n{essay}\n\n=== End of essay ===\n\nThese references could not be "
            f"matched in the OpenAlex or Crossref bibliographic databases:\n\n{listing}\n\n"
            "For each: if you are not certain the work exists exactly as cited (authors, "
            "title, year), correct it to the work you are certain of, or remove it together "
            "with any claim that depends on it. For a classic work, give its standard "
            "citation. Change nothing else. Stay within "
            f"{max_words} words before the references. Reply with the full essay in Markdown "
            "only.")
    return call(log, writer, role="writer", stage="polish-fixrefs", system=WRITER_SYSTEM,
                user=user, candidate="polish")


def word_count(essay: str) -> int:
    """Words before the references section (the rules exclude the bibliography)."""
    body = re.split(r"(?im)^#+\s*(references|bibliography)\s*$", essay)[0]
    return len(re.findall(r"\b\w[\w'-]*\b", body))
