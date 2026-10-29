"""The writer's two big structured calls on a served model, via the pipeline's own
stages: choose_area, then propose_theses (n=20, one JSON array). Scratch log only
(default runs/small-structured-check.jsonl); nothing here becomes an entry.

    .venv/bin/python labs/small_structured_check.py --url <vLLM base URL>
"""
import argparse
import time

from essay import stages as S
from essay.log import RunLog
from essay.pipeline import _llm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--model", default="phi-4")
    ap.add_argument("-n", type=int, default=20)
    ap.add_argument("--log", default="runs/small-structured-check.jsonl")
    a = ap.parse_args()
    log = RunLog(a.log)
    w = _llm({"kind": "openai-compat", "url": a.url, "model": a.model, "temperature": 0.7},
             "/nonexistent", "writer")
    t0 = time.time()
    area = S.choose_area(log, w)
    print(f"area ({time.time() - t0:.0f}s): {S.area_text(area)}")
    for c in area["candidates"]:
        print(f"   - {c['area']}: {c.get('question', '')[:120]}")
    t0 = time.time()
    pool = S.propose_theses(log, w, S.area_text(area), a.n)
    print(f"theses ({time.time() - t0:.0f}s): {len(pool)} of {a.n}; "
          f"empty fields: {sum(not t[k] for t in pool for k in ('thesis', 'argument_sketch'))}")
    for t in pool[:5]:
        print(f"   {t['id']} {t['thesis'][:140]}")
    calls = [r for r in log.records() if r["kind"] == "call"]
    print(f"calls: {len(calls)} (a retry means a JSON parse failed once); "
          f"stops: {[r['stop_reason'] for r in calls]}")


if __name__ == "__main__":
    main()
