"""`python -m essay <verb>` — the essay pipeline's commands (see essay/__init__.py).

Runs live under $ESSAY_RUNS (default ./runs/essay); `--run` takes a run id or
path, else the newest run. Secrets never go in config: backends read API keys from
the environment (ANTHROPIC_API_KEY / `ant auth login`; the vLLM key via --*-key-env).

With `--via queue` (the default) the writer and objector need no API key: stages
queue their requests under <run>/queue/ and exit 3 while answers are pending;
`python -m essay answer` fills them with Claude Code, then re-run the stage.
"""
from __future__ import annotations

import json
import os
import sys

from . import agent
from .pipeline import PendingBatch, Run
from .selection import DEFAULT_RULE


def _runs_dir():
    return os.environ.get("ESSAY_RUNS", os.path.join("runs", "essay"))


def _open(a) -> Run:
    if a.run and os.path.isdir(a.run):
        return Run(a.run)
    root = _runs_dir()
    if a.run:
        return Run(os.path.join(root, a.run))
    runs = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))) \
        if os.path.isdir(root) else []
    if not runs:
        sys.exit(f"no runs under {root}; start one with `python -m essay init`")
    return Run(os.path.join(root, runs[-1]))


def _critic_spec(a) -> dict:
    if a.critic == "stub":
        return {"kind": "stub"}
    if not a.critic_url:
        sys.exit("--critic vllm needs --critic-url")
    return {"kind": "openai-compat", "url": a.critic_url, "hat_model": a.critic_hat_model,
            "base_model": a.critic_base_model, "key_env": a.critic_key_env}


def cmd_init(a):
    if a.writer_url:      # a served (small) model writes; the objector follows unless set
        writer = {"kind": "openai-compat", "url": a.writer_url, "model": a.writer_model,
                  "key_env": a.writer_key_env, "temperature": a.writer_temperature}
    elif a.via == "queue":
        writer = {"kind": "queue", "model": a.writer_model, "effort": a.writer_effort}
    else:
        writer = {"kind": "claude", "model": a.writer_model, "effort": a.writer_effort}
    if a.objector_url:
        objector = {"kind": "openai-compat", "url": a.objector_url,
                    "model": a.objector_model, "key_env": a.objector_key_env}
    else:
        objector = {**writer, "model": a.objector_model or a.writer_model}
    config = {"area": a.area, "writer": writer, "objector": objector,
              "critic": _critic_spec(a),
              "myvect": ({"url": a.myvect_url, "boxes": a.boxes.split(",")}
                         if a.myvect_url else None),
              "objector_same_model_as_writer": objector.get("model") == writer["model"]}
    rule = DEFAULT_RULE
    if a.rule:
        with open(a.rule) as f:
            rule = json.load(f)
    run = Run.create(_runs_dir(), config, rule=rule)
    print(f"run {run.dir}  (pre-registered rule sha256 "
          f"{run.load('prereg.json')['sha256'][:12]}…)")
    if config["objector_same_model_as_writer"]:
        print("note: objector is the same model as the writer (pass --objector-url for "
              "an independent one)")


def cmd_set_critic(a):
    run = _open(a)
    spec = _critic_spec(a)
    old = run.config["critic"]
    run.config["critic"] = spec
    run.save(run.config, "config.json")
    run.log.append("config", field="critic", old=old, new=spec)
    print(f"critic: {old['kind']} -> {spec['kind']}")


def _stage(fn):
    def cmd(a):
        try:
            out = fn(_open(a), a)
        except PendingBatch as p:
            print(f"{p}. Answer them (`python -m essay answer`), then re-run "
                  f"`python -m essay {p.stage}`.")
            sys.exit(3)
        print(json.dumps(out, indent=1, ensure_ascii=False) if not isinstance(out, str) else out)
    return cmd


def cmd_answer(a):
    run = _open(a)
    todo = agent.pending(run.path("queue"), role=a.role)[: a.limit or None]
    if not todo:
        print("queue empty: nothing to answer")
        return
    cli = agent.ClaudeCLI(a.claude_bin, ssh=a.ssh)
    print(f"answering {len(todo)} request(s) with {cli.version or 'claude (version unknown)'}"
          f"{' on ' + a.ssh if a.ssh else ''}; flags: {sorted(cli.flags) or 'basic only'}")
    failed = 0
    for i, req in enumerate(todo, 1):
        rid = os.path.basename(req).split(".")[0]
        try:
            meta = agent.answer_one(req, cli)
        except (agent.AnswerError, OSError) as e:
            failed += 1
            print(f"[{i}/{len(todo)}] {rid} FAILED: {e}")
            continue
        print(f"[{i}/{len(todo)}] {rid} answered by {meta['model_served']} "
              f"({meta['duration_ms']} ms)")
    if failed:
        sys.exit(f"{failed} request(s) failed; re-run `python -m essay answer` to retry")


def cmd_human(a):
    run = _open(a)
    rec = run.log.human(a.note, author=a.author)
    print(f"logged human note #{rec['seq']}")


def add_parser(sub):
    e = sub.add_parser("essay", help="AI-authored essay pipeline (theses -> critique -> select)")
    es = e.add_subparsers(dest="essay_cmd", required=True)

    i = es.add_parser("init", help="new run: config + pre-registered selection rule")
    i.add_argument("--area", help="philosophical area (logged as a human input); "
                                  "omit to let the writer choose it")
    i.add_argument("--via", default="queue", choices=["queue", "api"],
                   help="queue: file requests answered by `essay answer` (no API key); "
                        "api: Anthropic SDK directly")
    i.add_argument("--writer-model", default="claude-opus-5-5")
    i.add_argument("--writer-effort", default="high",
                   choices=["low", "medium", "high", "xhigh", "max"])
    i.add_argument("--writer-url", help="OpenAI-compatible endpoint (vLLM) for the writer; "
                                        "--writer-model is then its served model name")
    i.add_argument("--writer-key-env", help="env var holding the writer endpoint's key")
    i.add_argument("--writer-temperature", type=float, default=0.7,
                   help="sampling temperature for a served writer (default 0.7)")
    i.add_argument("--objector-model", help="default: the writer model")
    i.add_argument("--objector-url", help="OpenAI-compatible endpoint for an independent objector")
    i.add_argument("--objector-key-env", help="env var holding the objector endpoint's key")
    i.add_argument("--myvect-url", help="myvect base URL for citation grounding")
    i.add_argument("--boxes", default="", help="comma-separated myvect boxes")
    i.add_argument("--rule", help="JSON file replacing the default selection rule")
    _critic_args(i)
    i.set_defaults(fn=cmd_init)

    c = es.add_parser("set-critic", help="switch the critic backend (logged)")
    c.add_argument("--run")
    _critic_args(c)
    c.set_defaults(fn=cmd_set_critic)

    for name, fn, hlp in [
        ("theses", lambda r, a: r.theses(), "writer proposes the candidate pool"),
        ("screen", lambda r, a: r.screen(), "objection + novelty per thesis, then shortlist"),
        ("develop", lambda r, a: r.develop(), "draft + critic rounds for the shortlist"),
        ("select", lambda r, a: r.select(allow_stub=a.allow_stub), "score + pick the winner"),
        ("status", lambda r, a: r.status(), "calls, tokens, human notes, log integrity"),
    ]:
        p = es.add_parser(name, help=hlp)
        p.add_argument("--run")
        if name == "select":
            p.add_argument("--allow-stub", action="store_true",
                           help="dry run: allow selecting with a stubbed critic")
        p.set_defaults(fn=_stage(fn))

    q = es.add_parser("answer", help="answer queued requests with Claude Code, one fresh "
                                     "session each")
    q.add_argument("--run"); q.add_argument("--role", choices=["writer", "objector"])
    q.add_argument("--limit", type=int, help="answer at most N requests")
    q.add_argument("--claude-bin", default=os.environ.get("CLAUDE_BIN", "claude"))
    q.add_argument("--ssh", metavar="USER@HOST",
                   help="run claude on another machine (where it's signed in); only the "
                        "request and its answer cross the connection")
    q.set_defaults(fn=cmd_answer)

    h = es.add_parser("human", help="record a human intervention verbatim")
    h.add_argument("--run"); h.add_argument("--note", required=True)
    h.add_argument("--author", default="entrant")
    h.set_defaults(fn=cmd_human)


def _critic_args(p):
    p.add_argument("--critic", default="stub", choices=["stub", "vllm"])
    p.add_argument("--critic-url", help="vLLM base URL serving the base model + hat LoRA")
    p.add_argument("--critic-hat-model", default="fallacy-restraint",
                   help="served LoRA module name (the hat arm)")
    p.add_argument("--critic-base-model", default="phi-4",
                   help="served base model name (the placebo arm)")
    p.add_argument("--critic-key-env", default="VLLM_API_KEY")
