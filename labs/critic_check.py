"""Run the essay pipeline's critic stage (same prompt, same parser) on a developed
candidate's final argument steps, hat arm and placebo arm, through a served vLLM.
Writes only a scratch log under the run's dir (critic-check.jsonl).

    .venv/bin/python labs/critic_check.py --url http://localhost:8000 \
        runs/essay-poc/<run-id> t03
"""
import argparse
import json
import os

from essay import stages as S
from essay.backends import OpenAICompatBackend
from essay.log import RunLog


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir"); ap.add_argument("candidate")
    ap.add_argument("--url", required=True)
    ap.add_argument("--hat-model", default="fallacy-restraint")
    ap.add_argument("--base-model", default="phi-4")
    a = ap.parse_args()
    cand = json.load(open(os.path.join(a.run_dir, "candidates", f"{a.candidate}.json")))
    steps = cand["final"]["steps"]
    log = RunLog(os.path.join(a.run_dir, "critic-check.jsonl"))
    arms = {"hat": OpenAICompatBackend(a.url, a.hat_model),
            "placebo": OpenAICompatBackend(a.url, a.base_model)}
    out = {arm: S.critique(log, be, steps, a.candidate, arm, "check")
           for arm, be in arms.items()}
    for i, step in enumerate(steps):
        print(f"\n[{i + 1}] {step[:220]}")
        for arm in arms:
            v = out[arm][i]
            label = f"FLAG {v['fallacy']}" if v["flag"] else v["verdict"]
            print(f"   {arm:<8} {label:<40} {v['explanation'][:120]!r}")
    for arm in arms:
        counts = {k: sum(v["verdict"] == k for v in out[arm])
                  for k in ("fallacy", "no_fallacy", "unclear")}
        print(f"\n{arm}: {counts} of {len(steps)} steps")
    print(f"log: {log.path} ({log.verify()[1]})")


if __name__ == "__main__":
    main()
