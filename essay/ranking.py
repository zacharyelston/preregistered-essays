"""Ranking a thesis pool: a frontier reference, and small-model harness variants scored
against it. Research only: nothing here feeds a contest run's shortlist.

Why: absolute screening ratings (novel/partly/known, severity 1-5) let the frontier
referee hedge (every thesis "partly", nearly every severity 4), so they are no
reference to measure a small model against. A ranking forces distinctions.

Variants (each argument-neutral; only the procedure differs):
  list       one listwise ranking (the frontier's own prompt)
  list5      five listwise rankings, aggregated by mean position (Borda)
  pairwise   every pair compared once (presentation order randomized, seeded),
             ranked by wins, then mean position across tied groups by id
  pointwise  each thesis rated alone (originality + defensibility, 1-10), sorted
Metrics: Kendall tau-b against the reference consensus; top-k overlap (k = the
rule's shortlist size).
"""
from __future__ import annotations

import itertools
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from . import stages as S
from .backends import PendingResponse, call

RANK_SYSTEM = S.OBJECTOR_SYSTEM
CRITERION = ("judged on one question: to what extent do its ideas and arguments make a "
             "valuable contribution to philosophical knowledge. Weigh how original the "
             "contribution would be and how well it could withstand the strongest objection")


def block(t: dict) -> str:
    return (f"[{t['id']}] {t.get('title', '')}\nThesis: {t['thesis']}\n"
            f"Argument sketch: {t['argument_sketch']}\nWhat it adds: {t.get('why_new', '')}")


LIST_FORMAT = "Reply with a JSON object: {\"ranking\": [every id exactly once, best first]}."


def list_prompt(pool: list[dict], restate: bool = False) -> str:
    """`restate`: repeat the output format after the pool. On a 6k-token pool Phi-4
    dropped the up-front JSON instruction and wrote a prose discussion instead."""
    return (f"Below are {len(pool)} candidate theses for a 6,000-word philosophy essay that "
            f"will be {CRITERION}. Rank all {len(pool)}, best first. {LIST_FORMAT}\n\n"
            + "\n\n".join(block(t) for t in pool)
            + (f"\n\nNow rank all {len(pool)}. {LIST_FORMAT} JSON only." if restate else ""))


def lenient_ranking(text: str, ids: list[str]) -> list[str] | None:
    """For a reply that ignored the format: ids in order of first mention. Scored as a
    separate number from the strict parse, never mixed into it."""
    import re
    seen = []
    for m in re.finditer(r"\bt\d{2}\b", text or ""):
        if m.group(0) in ids and m.group(0) not in seen:
            seen.append(m.group(0))
    return seen + [i for i in sorted(ids) if i not in seen] if len(seen) >= len(ids) // 2 \
        else None


def pair_prompt(a: dict, b: dict) -> str:
    return (f"Two candidate theses for a 6,000-word philosophy essay that will be {CRITERION}. "
            "Which is the better candidate? Reply with a JSON object: "
            "{\"better\": \"A\" | \"B\"}.\n\nA:\n" + block(a) + "\n\nB:\n" + block(b))


def point_prompt(t: dict) -> str:
    return (f"A candidate thesis for a 6,000-word philosophy essay that will be {CRITERION}. "
            "Rate it. Reply with a JSON object: {\"originality\": int 1-10, "
            "\"defensibility\": int 1-10}.\n\n" + block(t))


def parse_ranking(text: str, ids: list[str]) -> tuple[list[str], bool]:
    """A full ranking of `ids`, and whether the reply was complete. Unknown ids are
    dropped, repeats keep their first position, missing ids go last in id order."""
    v = S.extract_json(text)
    raw = v.get("ranking", []) if isinstance(v, dict) else v
    seen, out = set(), []
    for x in raw if isinstance(raw, list) else []:
        x = str(x).strip().strip("[]")
        if x in ids and x not in seen:
            seen.add(x)
            out.append(x)
    complete = len(out) == len(ids)
    return out + [i for i in sorted(ids) if i not in seen], complete


def borda(rankings: list[list[str]]) -> list[str]:
    pos = defaultdict(list)
    for r in rankings:
        for i, x in enumerate(r):
            pos[x].append(i)
    return sorted(pos, key=lambda x: (sum(pos[x]) / len(pos[x]), x))


def kendall_tau(r1: list[str], r2: list[str]) -> float:
    """Kendall tau between two full rankings of the same items (no ties)."""
    p1 = {x: i for i, x in enumerate(r1)}
    p2 = {x: i for i, x in enumerate(r2)}
    items = list(p1)
    conc = disc = 0
    for a, b in itertools.combinations(items, 2):
        s = (p1[a] - p1[b]) * (p2[a] - p2[b])
        conc += s > 0
        disc += s < 0
    n = conc + disc
    return round((conc - disc) / n, 3) if n else 0.0


def top_overlap(r1: list[str], r2: list[str], k: int) -> int:
    return len(set(r1[:k]) & set(r2[:k]))


# -- variants: each returns (ranking, info) and logs every call ----------------
def v_list(log, be, pool, n=1, tag="list", workers=4, shuffle=False, restate=False):
    """With a queue backend (the frontier reference) every sample is queued first, then
    PendingResponse is raised once; answer the queue and call again. `shuffle`: each
    sample sees the pool in a different seeded order (ids unchanged), the control for
    position bias."""
    ids = [t["id"] for t in pool]

    def order(i):
        if not shuffle:
            return pool
        p = list(pool)
        random.Random(1000 + i).shuffle(p)
        return p

    def one(i):
        try:
            text = call(log, be, role="ranker", stage=f"{tag}-{i}", system=RANK_SYSTEM,
                        user=list_prompt(order(i), restate), allow_truncated=True)
            return parse_ranking(text, ids)
        except PendingResponse as p:
            return p
        except (ValueError, RuntimeError, OSError):
            return None
    outs = [one(i) for i in range(n)] if workers == 1 else _pmap(one, range(n), workers)
    pending = [o for o in outs if isinstance(o, PendingResponse)]
    if pending:
        raise pending[0]
    rankings = [r for r, _ in (o for o in outs if o)]
    incomplete = sum(not ok for ok in (o[1] for o in outs if o))
    unusable = sum(o is None for o in outs)
    if not rankings:
        return None, {"unusable": unusable}
    return borda(rankings), {"samples": n, "incomplete": incomplete, "unusable": unusable,
                             "rankings": rankings}


def _pmap(fn, items, workers):
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(fn, items))


def v_pairwise(log, be, pool, seed=0, workers=4):
    rng = random.Random(seed)
    pairs = [((a, b) if rng.random() < 0.5 else (b, a))
             for a, b in itertools.combinations(pool, 2)]

    def judge(pair):
        first, second = pair
        try:
            text = call(log, be, role="ranker", stage="pair", system=RANK_SYSTEM,
                        user=pair_prompt(first, second),
                        candidate=f"{first['id']}|{second['id']}", allow_truncated=True)
            return str(S.extract_json(text).get("better", "")).strip().upper()
        except (ValueError, RuntimeError, AttributeError, OSError):
            return ""
    wins, unusable = defaultdict(float), 0
    for (first, second), pick in zip(pairs, _pmap(judge, pairs, workers)):
        a, b = first, second
        if pick in ("A", "B"):
            wins[(first if pick == "A" else second)["id"]] += 1
        else:
            unusable += 1
            wins[a["id"]] += 0.5
            wins[b["id"]] += 0.5
    ranking = sorted((t["id"] for t in pool), key=lambda x: (-wins[x], x))
    return ranking, {"comparisons": len(pool) * (len(pool) - 1) // 2, "unusable": unusable,
                     "wins": dict(wins)}


def v_pairwise_both(log, be, pool, workers=4):
    """Every pair judged in both orders. A thesis wins the pair only if it wins in both
    orders; otherwise (a verdict that flips with order, or an unusable reply) the pair
    is a draw. Cancels a model's preference for the first or second slot, which made
    one-order pairwise no better than chance for Qwen (it picked B 69% of the time)."""
    jobs = [(a, b) for a, b in itertools.combinations(pool, 2)]
    jobs = jobs + [(b, a) for a, b in jobs]

    def judge(pair):
        first, second = pair
        try:
            text = call(log, be, role="ranker", stage="pair2", system=RANK_SYSTEM,
                        user=pair_prompt(first, second),
                        candidate=f"{first['id']}|{second['id']}", allow_truncated=True)
            pick = str(S.extract_json(text).get("better", "")).strip().upper()
        except (ValueError, RuntimeError, AttributeError, OSError):
            return None
        return {"A": first["id"], "B": second["id"]}.get(pick)
    winner = {(f["id"], s["id"]): w for (f, s), w in zip(jobs, _pmap(judge, jobs, workers))}
    wins, draws, slot = defaultdict(float), 0, defaultdict(int)
    for (a, b) in itertools.combinations(pool, 2):
        w1, w2 = winner[(a["id"], b["id"])], winner[(b["id"], a["id"])]
        slot["first"] += (w1 == a["id"]) + (w2 == b["id"])
        slot["second"] += (w1 == b["id"]) + (w2 == a["id"])
        if w1 and w1 == w2:
            wins[w1] += 1
        else:
            draws += 1
            wins[a["id"]] += 0.5
            wins[b["id"]] += 0.5
    ranking = sorted((t["id"] for t in pool), key=lambda x: (-wins[x], x))
    return ranking, {"comparisons": len(jobs), "draws": draws, "slot_picks": dict(slot),
                     "unusable": sum(v is None for v in winner.values()), "wins": dict(wins)}


def v_pointwise(log, be, pool, n=3, workers=4):
    jobs = [(t, i) for t in pool for i in range(n)]

    def rate(job):
        t, i = job
        try:
            text = call(log, be, role="ranker", stage=f"point-{i}", system=RANK_SYSTEM,
                        user=point_prompt(t), candidate=t["id"], allow_truncated=True)
            v = S.extract_json(text)
            return int(v["originality"]) + int(v["defensibility"])
        except (ValueError, RuntimeError, KeyError, TypeError, AttributeError, OSError):
            return None
    score, unusable = defaultdict(list), 0
    for (t, _), s in zip(jobs, _pmap(rate, jobs, workers)):
        if s is None:
            unusable += 1
        else:
            score[t["id"]].append(s)
    mean = {t["id"]: (sum(score[t["id"]]) / len(score[t["id"]]) if score[t["id"]] else 0)
            for t in pool}
    ranking = sorted(mean, key=lambda x: (-mean[x], x))
    return ranking, {"samples": n, "unusable": unusable, "mean_score": mean}


VARIANTS = {
    "list": lambda log, be, pool: v_list(log, be, pool, 1, "list"),
    "list5": lambda log, be, pool: v_list(log, be, pool, 5, "list5"),
    "listshuf5": lambda log, be, pool: v_list(log, be, pool, 5, "listshuf5", shuffle=True),
    "listshuf5r": lambda log, be, pool: v_list(log, be, pool, 5, "listshuf5r", shuffle=True,
                                               restate=True),
    "pairwise": v_pairwise,
    "pairwise2": v_pairwise_both,
    "pointwise": v_pointwise,
}
