"""Ranking-referee experiment (research only; never feeds a contest run).

  reference  the frontier ranks a run's thesis pool twice (queue, answered by Claude
             Code over SSH: fresh tool-less sessions, as in the runs)
  probe      small-model harness variants rank the same pool (essay/ranking.py)
  report     Kendall tau / top-k overlap of every variant vs the frontier consensus,
             with the frontier's own self-agreement as the ceiling

All under runs/rank-exp/<run-id>/: reference.json, results/<model>__<variant>.json,
one chained log per backend (log-<name>.jsonl), and queue/ for frontier requests.

    .venv/bin/python labs/rank_exp.py reference runs/essay/<run> --ssh user@gpu-host
    .venv/bin/python labs/rank_exp.py probe runs/essay/<run> --model phi-4=<url>,phi-4 \
        [--model qwen-off=<url>,qwen3.8-27b,off --key-env VLLM_API_KEY] \
        [--variants list,list5,pairwise,pointwise]
    .venv/bin/python labs/rank_exp.py report runs/essay/<run> [runs/essay/<run2> ...]
"""
import argparse
import json
import os
import threading
from collections import defaultdict, deque

from essay import agent
from essay import ranking as K
from essay.backends import (Completion, FileQueueBackend, OpenAICompatBackend,
                               PendingResponse)
from essay.log import RunLog, canonical


class Cached:
    """Answers a prompt from an earlier (stopped) probe's log before asking the model,
    so resuming never pays for the same call twice. Identical prompts (list5's
    samples) take their logged answers in order. Reused answers are marked in meta."""
    kind = "openai-compat"

    def __init__(self, inner, records):
        self.inner, self.model = inner, inner.model
        self._lock = threading.Lock()
        self._have = defaultdict(deque)
        for r in records:
            if r["kind"] == "call" and not r.get("error") and r.get("response") is not None \
                    and not (r.get("meta") or {}).get("cached"):
                self._have[canonical([r.get("system"), r["user"]])].append(r)
        self.reused = 0

    def complete(self, system, user, *, stage, max_tokens=None):
        with self._lock:
            q = self._have.get(canonical([system, user]))
            r = q.popleft() if q else None
        if r is None:
            return self.inner.complete(system, user, stage=stage, max_tokens=max_tokens)
        self.reused += 1
        return Completion(text=r["response"], model=r.get("model_served") or self.model,
                          stop_reason=r.get("stop_reason"), usage=r.get("usage") or {},
                          meta={"cached": True, "from_seq": r["seq"]})


def exp_dir(run_dir):
    d = os.path.join("runs", "rank-exp", os.path.basename(run_dir.rstrip("/")))
    os.makedirs(os.path.join(d, "results"), exist_ok=True)
    return d


def pool_of(run_dir):
    with open(os.path.join(run_dir, "theses.json")) as f:
        return json.load(f)


def cmd_reference(a):
    d, pool = exp_dir(a.run), pool_of(a.run)
    suffix = "-shuf" if a.shuffle else ""
    out = os.path.join(d, f"reference{suffix}.json")
    if os.path.exists(out):
        print(f"exists: {out}")
        return
    log = RunLog(os.path.join(d, f"log-frontier{suffix}.jsonl"))
    be = FileQueueBackend(os.path.join(d, "queue"), "ranker", "claude-opus-5-5",
                          effort="high")
    cli = agent.ClaudeCLI(ssh=a.ssh)
    while True:
        try:
            consensus, info = K.v_list(log, be, pool, a.k, "ref" + suffix, workers=1,
                                       shuffle=a.shuffle)
            break
        except PendingResponse:
            for req in agent.pending(os.path.join(d, "queue")):
                meta = agent.answer_one(req, cli)
                print(f"  {os.path.basename(req)[:16]} {meta['model_served']} "
                      f"{meta['duration_ms']}ms ${meta['cost_usd']}", flush=True)
    r = info["rankings"]
    doc = {"consensus": consensus, "rankings": r, "info": info,
           "self_tau": [K.kendall_tau(r[i], r[j]) for i in range(len(r))
                        for j in range(i + 1, len(r))]}
    with open(out, "w") as f:
        json.dump(doc, f, indent=1)
    print(f"reference{suffix}: self-tau {doc['self_tau']}; top-2 {consensus[:2]}")


def cmd_probe(a):
    d, pool = exp_dir(a.run), pool_of(a.run)
    variants = a.variants.split(",")
    for spec in a.model:
        name, rest = spec.split("=", 1)
        url, served, *effort = rest.split(",")
        extra = ({"chat_template_kwargs": {"enable_thinking": False} if effort[0] == "off"
                  else {"reasoning_effort": effort[0]}} if effort else {})
        be = OpenAICompatBackend(url, served, api_key_env=a.key_env, max_tokens=None,
                                 temperature=a.temperature, timeout=3600, extra=extra)
        for v in variants:
            out = os.path.join(d, "results", f"{name}__{v}.json")
            if os.path.exists(out):
                continue
            # one log per (model, variant): concurrent probe processes never share a file
            log = RunLog(os.path.join(d, f"log-{name}-{v}.jsonl"))
            cbe = Cached(be, log.records())
            ranking, info = K.VARIANTS[v](log, cbe, pool)
            info["reused_from_log"] = cbe.reused
            if ranking is None:   # nothing usable (e.g. every call 401'd): retry next run
                errs = [r.get("error") for r in log.records() if r.get("error")]
                print(f"[{name} {v}] NO USABLE RANKING, not saved; last error: "
                      f"{(errs[-1] if errs else 'unparseable replies')[:200]}", flush=True)
                continue
            with open(out, "w") as f:
                json.dump({"model": name, "variant": v, "ranking": ranking, "info": info},
                          f, indent=1)
            print(f"[{name} {v}] done: top-2 {ranking[:2] if ranking else None}", flush=True)


def cmd_lenient(a):
    """Re-score logged listwise answers without new calls: strict JSON where it parses,
    else ids in order of first mention. Saved as <model>__<variant>-lenient.json so the
    report shows the format failure and the underlying judgment as separate rows."""
    d, pool = exp_dir(a.run), pool_of(a.run)
    ids = [t["id"] for t in pool]
    for fn in sorted(os.listdir(d)):
        if not (fn.startswith("log-") and fn.endswith(".jsonl")) or "frontier" in fn:
            continue
        rankings, how = [], {"strict": 0, "lenient": 0, "unusable": 0}
        for r in RunLog(os.path.join(d, fn)).records():
            if r["kind"] != "call" or not r["stage"].startswith("list"):
                continue
            try:
                rankings.append(K.parse_ranking(r.get("response") or "", ids)[0])
                how["strict"] += 1
            except ValueError:
                lr = K.lenient_ranking(r.get("response") or "", ids)
                if lr:
                    rankings.append(lr)
                    how["lenient"] += 1
                else:
                    how["unusable"] += 1
        if not how["lenient"]:
            continue          # nothing rescued: the strict result already says it all
        name = fn[len("log-"):-len(".jsonl")]
        model, _, variant = name.rpartition("-")
        if variant not in K.VARIANTS or not os.path.exists(
                os.path.join(d, "results", f"{model}__{variant}.json")):
            continue          # an older all-variants log, or a probe still running
        out = os.path.join(d, "results", f"{model}__{variant}-lenient.json")
        with open(out, "w") as f:
            json.dump({"model": model, "variant": f"{variant}-lenient",
                       "ranking": K.borda(rankings) if rankings else None,
                       "info": {**how, "unusable": how["unusable"]}}, f, indent=1)
        print(f"{model} {variant}: {how}")


def report(run_dir, k=2):
    d = exp_dir(run_dir)
    ref = json.load(open(os.path.join(d, "reference.json")))
    shuf_path = os.path.join(d, "reference-shuf.json")
    shuf = json.load(open(shuf_path)) if os.path.exists(shuf_path) else None
    # primary reference: every frontier ranking pooled (fixed order + shuffled), so the
    # frontier's own order effects average out; the fixed-only consensus is kept too
    pooled = K.borda(ref["rankings"] + (shuf["rankings"] if shuf else []))
    rows = []
    for fn in sorted(os.listdir(os.path.join(d, "results"))):
        r = json.load(open(os.path.join(d, "results", fn)))
        if not r["ranking"]:
            rows.append({**{x: r[x] for x in ("model", "variant")}, "tau": None})
            continue
        rows.append({"model": r["model"], "variant": r["variant"],
                     "tau": K.kendall_tau(r["ranking"], pooled),
                     f"top{k}_overlap": K.top_overlap(r["ranking"], pooled, k),
                     "tau_vs_fixed_ref": K.kendall_tau(r["ranking"], ref["consensus"]),
                     "tau_each_ref": [K.kendall_tau(r["ranking"], x) for x in
                                      ref["rankings"] + (shuf["rankings"] if shuf else [])],
                     "unusable": r["info"].get("unusable")})
    every = ref["rankings"] + (shuf["rankings"] if shuf else [])
    out = {"run": os.path.basename(run_dir.rstrip("/")), "frontier_self_tau": ref["self_tau"],
           "frontier_top": pooled[:k], "frontier_pooled": pooled,
           # the ceiling: one frontier ranking vs the pool of the *other* frontier rankings
           # (leave-one-out; against a pool that includes it, it would be flattered)
           "frontier_each_vs_pooled": [
               K.kendall_tau(x, K.borda(every[:i] + every[i + 1:]))
               for i, x in enumerate(every)] if len(every) > 1 else [],
           "rows": rows}
    if shuf:
        out["frontier_shuffled"] = {
            "self_tau": shuf["self_tau"], "top": shuf["consensus"][:k],
            "tau_fixed_vs_shuffled": K.kendall_tau(ref["consensus"], shuf["consensus"])}
    return out


def cmd_report(a):
    for run in a.runs:
        rep = report(run)
        print(f"\n== {rep['run']}  frontier pooled top-2 {rep['frontier_top']}  "
              f"each frontier ranking vs pooled {rep['frontier_each_vs_pooled']}")
        if rep.get("frontier_shuffled"):
            print(f"   frontier shuffled: {rep['frontier_shuffled']}")
        for r in sorted(rep["rows"], key=lambda r: -(r["tau"] if r["tau"] is not None else -9)):
            print(f"  {r['model']:<14} {r['variant']:<10} tau {r['tau']}  "
                  f"top2 {r.get('top2_overlap')}  per-ref {r.get('tau_each_ref')}  "
                  f"unusable {r.get('unusable')}")
        with open(os.path.join(exp_dir(run), "report.json"), "w") as f:
            json.dump(rep, f, indent=1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("reference"); r.add_argument("run"); r.add_argument("--ssh", required=True)
    r.add_argument("-k", type=int, default=2)
    r.add_argument("--shuffle", action="store_true",
                   help="present the pool in a different order per sample (position control)")
    p = sub.add_parser("probe"); p.add_argument("run")
    p.add_argument("--model", action="append", required=True,
                   metavar="NAME=URL,SERVED[,EFFORT]")
    p.add_argument("--variants", default="list,list5,pairwise,pointwise")
    p.add_argument("--key-env"); p.add_argument("--temperature", type=float, default=0.7)
    rp = sub.add_parser("report"); rp.add_argument("runs", nargs="+")
    le = sub.add_parser("lenient"); le.add_argument("run")
    a = ap.parse_args()
    {"reference": cmd_reference, "probe": cmd_probe, "report": cmd_report,
     "lenient": cmd_lenient}[a.cmd](a)


if __name__ == "__main__":
    main()
