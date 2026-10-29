"""Replay a run's frontier calls through small models, then summarize (essay/replay.py).

    .venv/bin/python labs/essay_replay.py runs/essay/<run-id> [-k 3] \
        [--model phi-4=<url>,phi-4] [--model hat=<url>,fallacy-restraint] \
        [--stages novelty,objection,objection-check]
    .venv/bin/python labs/essay_replay.py runs/essay/<run-id> --summary-only

Default models: Phi-4 and the fallacy-restraint hat on the hat server, through
`kubectl proxy --port 8001`. Sampling: temperature 0.7, no max_tokens cap.
"""
import argparse
import json

from essay import replay as R
from essay.backends import OpenAICompatBackend

VLLM = ("http://localhost:8001/api/v1/namespaces/<namespace>/services/"
        "<hat-server>:8000/proxy")
DEFAULT_MODELS = [f"phi-4={VLLM},phi-4", f"hat-fallacy={VLLM},fallacy-restraint"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("-k", type=int, default=3, help="samples per call (vote over k)")
    ap.add_argument("--model", action="append", metavar="NAME=URL,SERVED_NAME[,EFFORT]",
                    help="EFFORT for reasoning models: xhigh | medium | low | off")
    ap.add_argument("--key-env", help="env var holding the endpoints' API key")
    ap.add_argument("--stages", help="comma-separated base stages to replay (default all)")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--summary-only", action="store_true")
    a = ap.parse_args()
    if not a.summary_only:
        models = {}
        for spec in a.model or DEFAULT_MODELS:
            name, rest = spec.split("=", 1)
            url, served, *effort = rest.split(",")
            extra = {}
            if effort:
                extra = {"chat_template_kwargs": {"enable_thinking": False}
                         if effort[0] == "off" else {"reasoning_effort": effort[0]}}
            models[name] = OpenAICompatBackend(url, served, api_key_env=a.key_env,
                                               max_tokens=None, temperature=a.temperature,
                                               timeout=3600, extra=extra)
        stages = set(a.stages.split(",")) if a.stages else None
        print("replayed:", R.replay(a.run_dir, models, k=a.k, stages=stages,
                                    workers=a.workers), flush=True)
    rep = R.summarize(a.run_dir)
    for name, m in rep["models"].items():
        print(f"\n== {name}")
        for st, o in sorted(m["stages"].items()):
            extras = {k: v for k, v in o.items()
                      if k not in ("calls", "samples", "format_ok_rate", "errors")}
            print(f"  {st:<16} calls {o['calls']:>3}  format {o['format_ok_rate']:.2f}  "
                  f"errors {o['errors']:>2}  {extras}")
        for mode in ("single", "vote"):
            print(f"  counterfactual ({mode}): "
                  f"{json.dumps(m.get('counterfactual_' + mode, {}))}")


if __name__ == "__main__":
    main()
