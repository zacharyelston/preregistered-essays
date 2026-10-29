"""Drive one contest run end to end: area -> theses -> screen -> develop -> select.

Arms (same rule, same scaffold; only the models differ):
  frontier  writer + objector = Claude via the file queue, answered by Claude Code
            over SSH (one fresh, tool-less session per request)
  small     writer + objector = Phi-4 on the hat server (vLLM) (no queue)
  qwen      writer + objector = Qwen3.8-27B (FP8, 64k context) at xhigh reasoning effort,
            through its ingress; the key is read from $VLLM_API_KEY. Sampling is the
            model's own recommendation (temperature 1.0; top-p/top-k from its
            generation config)
Critic (all arms): the fallacy-restraint hat + its Phi-4 base as placebo, same server.

The writer chooses the area (no --area): the only human inputs are starting the
run and the arm. Start `kubectl proxy --port 8001` first; the vLLM URL goes through
the API server's service proxy, which survives pod restarts.

    .venv/bin/python labs/essay_run.py --arm frontier --ssh user@gpu-host
    .venv/bin/python labs/essay_run.py --arm small
    .venv/bin/python labs/essay_run.py --resume runs/essay/<run-id> [--ssh ...]
"""
import argparse
import json
import os

from essay import agent
from essay.pipeline import PendingBatch, Run
from essay.selection import DEFAULT_RULE, RULE_V3

RULES = {2: DEFAULT_RULE, 3: RULE_V3}

VLLM = ("http://localhost:8001/api/v1/namespaces/<namespace>/services/"
        "<hat-server>:8000/proxy")
CRITIC = {"kind": "openai-compat", "url": VLLM, "hat_model": "fallacy-restraint",
          "base_model": "phi-4", "key_env": None}
ARMS = {
    "frontier": {"kind": "queue", "model": "claude-opus-5-5", "effort": "high"},
    "small": {"kind": "openai-compat", "url": VLLM, "model": "phi-4", "key_env": None,
              "temperature": 0.7},
    "qwen": {"kind": "openai-compat", "url": "https://<qwen-endpoint>",
             "model": "qwen3.8-27b", "key_env": "VLLM_API_KEY", "temperature": 1.0,
             "timeout": 3600, "extra": {"chat_template_kwargs": {"reasoning_effort": "xhigh"}}},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=sorted(ARMS))
    ap.add_argument("--resume", metavar="RUN_DIR")
    ap.add_argument("--ssh", metavar="USER@HOST", help="where Claude Code answers the queue")
    ap.add_argument("--runs-dir", default=os.path.join("runs", "essay"))
    ap.add_argument("--avoid-area-of", action="append", metavar="RUN_DIR",
                    help="another entry's run: its chosen area is off-limits here")
    ap.add_argument("--rule", type=int, choices=sorted(RULES), default=3,
                    help="selection rule version for a new run (default 3)")
    ap.add_argument("--human-note", action="append", default=[],
                    help="a human decision about this run, logged verbatim after init")
    a = ap.parse_args()
    if bool(a.arm) == bool(a.resume):
        ap.error("give exactly one of --arm (new run) or --resume")

    if a.resume:
        run = Run(a.resume)
    else:
        llm = ARMS[a.arm]
        avoid = []
        for d in a.avoid_area_of or []:
            with open(os.path.join(d, "area.json")) as f:
                taken = json.load(f)
            avoid.append(f"{taken['area']} ({taken['question']})")
        config = {"area": None, "arm": a.arm, "writer": llm, "objector": dict(llm),
                  "critic": CRITIC, "myvect": None, "objector_same_model_as_writer": True,
                  "avoid_areas": avoid}
        run = Run.create(a.runs_dir, config, rule=RULES[a.rule], run_id=None)
        for note in a.human_note:
            run.log.human(note)
    queued = run.config["writer"]["kind"] == "queue"
    if queued and not a.ssh:
        ap.error("this arm answers through the queue: pass --ssh USER@HOST")
    print(f"run: {run.dir}  arm: {run.config.get('arm')}", flush=True)

    cli = agent.ClaudeCLI(ssh=a.ssh) if queued else None
    if cli:
        print(f"claude {cli.version} on {a.ssh}; flags {sorted(cli.flags)}", flush=True)
    sel = None
    # select is a stage too: rule v3's final queues its head-to-head comparisons
    for stage in ("theses", "screen", "develop", "select"):
        if stage == "theses" and run.load("theses.json"):
            continue                       # the pool is fixed once generated
        while True:
            try:
                out = getattr(run, stage)()
                if stage == "select":
                    sel = out
                print(f"[{stage}] done", flush=True)
                break
            except PendingBatch as p:
                todo = agent.pending(run.path("queue"))
                print(f"[{stage}] {p.n} pending -> answering {len(todo)}", flush=True)
                for req in todo:
                    meta = agent.answer_one(req, cli)
                    print(f"   {os.path.basename(req)[:16]} {meta['model_served']} "
                          f"{meta['stop_reason']} {meta['duration_ms']}ms "
                          f"${meta['cost_usd']}", flush=True)
    print(json.dumps({"winner": sel["winner"], "decided_by": sel["decided_by"],
                      "wins": (sel.get("final_pairwise") or {}).get("wins"),
                      "ranking": sel["ranking"]}, indent=1))
    print(json.dumps(run.status(), indent=1))


if __name__ == "__main__":
    main()
