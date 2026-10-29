"""The pre-registered selection rule — the answer to "picking the best of 200 drafts
is itself the philosophy". A human never chooses between candidates: the shortlist
cut, the development budget and the final ranking are all fixed here, hashed into
the run log before the first generation call, and re-verified before `select`.

Scoring follows hb/scoring.py's methodology: hard gates first (any failure -> 0),
then a weighted mean of the separable components. Components the run can't measure
(e.g. grounding with no RAG configured) are dropped and the weights renormalized —
a rule stated here in advance, not a call made after seeing the numbers.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import time

from .log import RunLog, canonical
from .stages import ADDRESSED, NOVELTY, word_count

DEFAULT_RULE = {
    "version": 2,
    "screen": {
        "n_theses": 20,                   # size of the candidate pool
        "shortlist_k": 2,                 # theses developed into full drafts
        "exclude_novelty": ["known"],     # objector's novelty verdict
        # order: novelty (desc), objection severity (asc), thesis id (asc)
    },
    "develop": {"rounds": 2, "max_steps": 25, "critic_arms": ["hat", "placebo"]},
    "gates": {
        "max_words": 6000,                # competition limit, excluding references
        "min_novelty": 0.5,
        "min_objection_addressed": 0.5,
        "max_critic_flag_rate": 0.5,      # hat arm, final pass
        "min_steps": 3,
    },
    # v2: critic_clean .35 -> .15. On the PoC essay the hat passed all 8 steps, so
    # it mostly vetoes (the flag-rate gate) rather than ranks; hat vs placebo is
    # reported as an analysis, not leaned on for selection.
    "weights": {"critic_clean": 0.15, "objection_addressed": 0.35,
                "novelty": 0.25, "grounded": 0.25},
    "ground_min_score": 0.45,             # myvect cosine for "citation found"
    "critic_arm": "hat",                  # which arm's flags count
}

# v3, from the pilot (two v2 runs): the referee's absolute ratings hedged (all 20
# theses "partly" novel, severity ~4) and the final measurements tied exactly, so
# both v2 selections fell to the thesis-id tie-break. v3 makes the referee choose:
#   screen  rank the whole pool (n listwise rankings, each in a different shuffled
#           order, mean position), then walk down the ranking running objection +
#           novelty until shortlist_k theses pass the novelty gate
#   final   among developed candidates that pass every gate, head-to-head
#           comparisons of the finished essays, each pair in both orders `rounds`
#           times (fresh sessions); most wins; ties -> v2 score, then thesis id
# The adapter critic keeps its gate and its revision loop; scores are reported but
# no longer choose.
RULE_V3 = {
    **copy.deepcopy(DEFAULT_RULE),
    "version": 3,
    "screen": {"method": "rank", "n_theses": 20, "rankings": 4, "shortlist_k": 3,
               "exclude_novelty": ["known"]},
    "final": {"method": "pairwise", "rounds": 3},
}

PREREG = "prereg.json"


class PreregError(RuntimeError):
    pass


def rule_hash(rule: dict) -> str:
    return hashlib.sha256(canonical(rule).encode()).hexdigest()


def preregister(run_dir: str, log: RunLog, rule: dict | None = None) -> dict:
    path = os.path.join(run_dir, PREREG)
    if os.path.exists(path):
        raise PreregError(f"{path} exists; a run is pre-registered exactly once")
    if any(r["kind"] == "call" for r in log.records()):
        raise PreregError("model calls already logged; pre-registration must come first")
    rule = copy.deepcopy(rule or DEFAULT_RULE)
    doc = {"rule": rule, "sha256": rule_hash(rule),
           "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    with open(path, "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    log.append("preregister", sha256=doc["sha256"], rule=rule)
    return doc


def load_rule(run_dir: str, log: RunLog) -> dict:
    """The rule, after checking file == logged hash and the log chain is intact."""
    ok, why = log.verify()
    if not ok:
        raise PreregError(f"run log failed verification: {why}")
    logged = [r for r in log.records() if r["kind"] == "preregister"]
    if len(logged) != 1:
        raise PreregError(f"expected one preregister record, found {len(logged)}")
    calls_before = [r for r in log.records() if r["kind"] == "call"
                    and r["seq"] < logged[0]["seq"]]
    if calls_before:
        raise PreregError("model calls precede the pre-registration")
    with open(os.path.join(run_dir, PREREG)) as f:
        doc = json.load(f)
    if rule_hash(doc["rule"]) != doc["sha256"] or doc["sha256"] != logged[0]["sha256"]:
        raise PreregError("prereg.json does not match the hash recorded in the log")
    return doc["rule"]


def shortlist(screened: list[dict], rule: dict) -> list[str]:
    s = rule["screen"]
    keep = [t for t in screened if t["novelty"]["verdict"] not in s["exclude_novelty"]]
    keep.sort(key=lambda t: (-NOVELTY[t["novelty"]["verdict"]],
                             t["objection"]["severity"], t["id"]))
    return [t["id"] for t in keep[: s["shortlist_k"]]]


def metrics(cand: dict, rule: dict) -> dict:
    final = cand["final"]
    flags = [f for f in final["critique"][rule["critic_arm"]] if f["flag"]]
    n_steps = len(final["steps"])
    g = final.get("grounding")
    return {
        "words": word_count(final["essay"]),
        "steps": n_steps,
        "critic_flag_rate": round(len(flags) / n_steps, 4) if n_steps else 1.0,
        "critic_clean": round(1 - len(flags) / n_steps, 4) if n_steps else 0.0,
        "novelty": NOVELTY[cand["novelty"]["verdict"]],
        "objection_addressed": ADDRESSED[final["objection_check"]["addressed"]],
        "grounded": (round(sum(c["found"] for c in g) / len(g), 4) if g else None),
    }


def score(m: dict, rule: dict) -> tuple[float, list[str]]:
    gt = rule["gates"]
    fails = [name for name, bad in [
        ("max_words", m["words"] > gt["max_words"]),
        ("min_steps", m["steps"] < gt["min_steps"]),
        ("min_novelty", m["novelty"] < gt["min_novelty"]),
        ("min_objection_addressed", m["objection_addressed"] < gt["min_objection_addressed"]),
        ("max_critic_flag_rate", m["critic_flag_rate"] > gt["max_critic_flag_rate"]),
    ] if bad]
    if fails:
        return 0.0, fails
    w = {k: v for k, v in rule["weights"].items() if m.get(k) is not None}
    total = sum(w.values())
    return round(sum(v * m[k] for k, v in w.items()) / total, 4) if total else 0.0, []


def rank(cands: list[dict], rule: dict) -> list[dict]:
    rows = []
    for c in cands:
        m = metrics(c, rule)
        s, fails = score(m, rule)
        rows.append({"id": c["id"], "score": s, "gate_failures": fails, "metrics": m})
    return sorted(rows, key=lambda r: (-r["score"], r["id"]))
