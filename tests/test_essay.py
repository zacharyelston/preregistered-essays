"""Essay pipeline: the chained log, the pre-registration guard, the stage parsers,
and a full theses -> screen -> develop -> select run on scripted backends (no
network, no keys). The guards are the point: a stubbed critic can't silently
produce a "winner", and an edited rule or log can't pass `select`."""
import glob
import json
import os
import stat
import sys

import pytest

from essay.__main__ import main
from essay import agent
from essay import stages as S
from essay.backends import Completion, FileQueueBackend, PendingResponse, StubBackend, call
from essay.log import RunLog
from essay.pipeline import PendingBatch, Run
from essay.selection import DEFAULT_RULE, PreregError, load_rule, score

THESES = [{"title": f"T{i}", "thesis": f"Thesis T{i}", "argument_sketch": f"Sketch T{i}",
           "why_new": "new"} for i in range(1, 5)]
ESSAY = "# Essay\n\nAn argument in several steps.\n\n## References\n\n- Pearl, Causality, 2009\n"


def writer_fn(stage, system, user):
    if stage == "area":
        return json.dumps({"candidates": [{"area": "ethics", "question": "q0", "why": "w"},
                                          {"area": "metaphysics of causation",
                                           "question": "Are omissions causes?", "why": "w"}],
                           "chosen": 1, "reason": "most room"})
    if stage == "theses":
        return "Here you go:\n```json\n" + json.dumps(THESES) + "\n```"
    if stage == "draft":
        return ESSAY
    if stage == "steps":
        revised = "REVISED" in user
        steps = ["P1. Therefore, C1.", "P2. Therefore, C2.", "P3. Therefore, C3."]
        return json.dumps(steps + ([] if revised else ["BAD step. Therefore, C4."]))
    if stage.startswith("respond"):
        return json.dumps({"responses": [{"step": 4, "action": "fix", "reason": "r"}],
                           "essay": ESSAY.replace("several steps", "several steps REVISED")})
    if stage == "citations":
        return json.dumps([{"work": "Pearl, Causality, 2009", "claim": "do-calculus"}])
    raise AssertionError(f"unexpected writer stage {stage}")


def objector_fn(stage, system, user):
    if stage == "objection":
        return json.dumps({"objection": "obj", "severity": 2 if "T2" in user else 4,
                           "rationale": "x"})
    if stage == "novelty":
        verdict = "known" if "T3" in user else "partly" if "T4" in user else "novel"
        return json.dumps({"verdict": verdict, "closest_work": [], "note": ""})
    if stage == "objection-check":
        return json.dumps({"addressed": "yes", "reason": "answered in §3"})
    raise AssertionError(f"unexpected objector stage {stage}")


def critic_fn(stage, system, user):
    return "Fallacy: composition. The whole is not its parts." if "BAD" in user \
        else "No fallacy. Valid."


class FakeServedCritic:
    """Stands in for the vLLM hat server (kind != 'stub')."""
    kind = "openai-compat"

    def __init__(self, model):
        self.model = model

    def complete(self, system, user, *, stage, max_tokens=None):
        return Completion(text=critic_fn(stage, system, user), model=self.model,
                          stop_reason="stop")


class FakeRetriever:
    boxes = ["pearl-causality"]

    def search(self, query, k=3):
        return [{"box": "pearl-causality", "text": "do-calculus", "score": 0.81}]


CONFIG = {"area": "philosophy of causation", "writer": {"kind": "claude", "model": "w"},
          "objector": {"kind": "claude", "model": "o"}, "critic": {"kind": "stub"},
          "myvect": None}


def _run(tmp_path, served_critic=True):
    critic = (lambda arm: FakeServedCritic(f"{arm}-model")) if served_critic else \
        (lambda arm: StubBackend(critic_fn, model=f"stub-{arm}"))
    backends = {"writer": StubBackend(writer_fn), "objector": StubBackend(objector_fn),
                "critic_hat": critic("hat"), "critic_placebo": critic("placebo"),
                "retriever": FakeRetriever()}
    return Run.create(str(tmp_path), CONFIG, backends=backends, run_id="r1")


def test_log_chain_detects_edits(tmp_path):
    p = tmp_path / "log.jsonl"
    log = RunLog(str(p))
    for i in range(3):
        log.append("call", n=i)
    assert log.verify()[0]
    assert RunLog(str(p)).append("call", n=3)["seq"] == 4      # resumes the chain
    lines = p.read_text().splitlines()
    lines[1] = lines[1].replace('"n":1', '"n":99').replace('"n": 1', '"n": 99')
    p.write_text("\n".join(lines) + "\n")
    ok, why = log.verify()
    assert not ok and "record 2" in why


def test_prereg_guards(tmp_path):
    run = _run(tmp_path)
    assert load_rule(run.dir, run.log) == DEFAULT_RULE
    doc = json.loads(open(run.path("prereg.json")).read())
    doc["rule"]["weights"]["novelty"] = 0.9                      # post-hoc tuning
    open(run.path("prereg.json"), "w").write(json.dumps(doc))
    with pytest.raises(PreregError):
        run.theses()


def test_end_to_end_selects_by_rule(tmp_path):
    run = _run(tmp_path)
    assert len(run.theses()) == 4
    with pytest.raises(RuntimeError):
        run.theses()                                             # the pool is fixed
    # known (t03) excluded; novel before partly; lower severity first
    assert run.screen() == ["t02", "t01"]
    run.develop()
    cand = run.load("candidates", "t02.json")
    assert len(cand["rounds"]) == 2                              # flag -> fix -> clean
    assert cand["rounds"][0]["critique"]["hat"][3]["flag"] is True
    assert "REVISED" in cand["final"]["essay"]
    assert cand["final"]["grounding"][0]["found"] is True
    sel = run.select()
    # same scripted essay for both -> equal scores -> the rule's id tie-break decides
    assert [r["score"] for r in sel["ranking"]] == [sel["ranking"][0]["score"]] * 2
    assert sel["winner"] == "t01" and not sel["critic_stubbed"]
    assert all(r["score"] > 0 and not r["gate_failures"] for r in sel["ranking"])
    assert open(run.path("final.md")).read().startswith("# Essay")
    st = run.status()
    assert st["log"].endswith("chain intact") and st["human_notes"] == 1
    assert st["by_role"]["critic:hat"]["calls"] > 0


def test_stubbed_critic_cannot_pick_a_winner(tmp_path):
    run = _run(tmp_path, served_critic=False)
    run.theses(); run.screen(); run.develop()
    with pytest.raises(RuntimeError, match="stubbed"):
        run.select()
    assert run.select(allow_stub=True)["critic_stubbed"] is True


def test_gates_zero_the_score():
    m = {"words": 7000, "steps": 5, "critic_flag_rate": 0.0, "critic_clean": 1.0,
         "novelty": 1.0, "objection_addressed": 1.0, "grounded": None}
    s, fails = score(m, DEFAULT_RULE)
    assert s == 0.0 and fails == ["max_words"]
    s, fails = score({**m, "words": 5000}, DEFAULT_RULE)
    assert s == 1.0 and not fails                                # grounding dropped, renormalized


def test_parsers():
    assert S.parse_verdict("No fallacy. Sound.")["flag"] is False
    v = S.parse_verdict("Fallacy: composition. Parts vs whole.")
    assert v["flag"] and v["fallacy"] == "composition"
    assert S.extract_json('ok ```json\n{"a": [1, 2]}\n``` done') == {"a": [1, 2]}
    assert S.word_count("one two three\n\n## References\n\nfour five") == 3


def test_cli_init_and_status(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("ESSAY_RUNS", str(tmp_path))
    main(["essay", "init", "--area", "formal epistemology"])
    assert "pre-registered" in capsys.readouterr().out
    main(["essay", "human", "--note", "corrected a typo in the area name"])
    main(["essay", "status"])
    st = json.loads(capsys.readouterr().out.split("\n", 1)[1])
    assert st["human_notes"] == 2 and st["log"].endswith("chain intact")
    run_dir = os.path.join(tmp_path, os.listdir(tmp_path)[0])
    cfg = json.load(open(os.path.join(run_dir, "config.json")))
    assert cfg["writer"]["model"] == "claude-opus-5-5" and cfg["critic"] == {"kind": "stub"}


# -- queue backend: no API key, an agent answers files ------------------------

def _answer_queue(queue_dir):
    """Stand-in agent: answers every pending request from its own fields only."""
    fns = {"writer": writer_fn, "objector": objector_fn}
    n = 0
    for req in agent.pending(queue_dir):
        r = json.load(open(req))
        with open(req.replace(".request.json", ".response.md"), "w") as f:
            f.write(fns[r["role"]](r["stage"], r["system"], r["user"]))
        n += 1
    return n


def test_queue_backend_pends_then_answers_once(tmp_path):
    log = RunLog(str(tmp_path / "log.jsonl"))
    q = FileQueueBackend(str(tmp_path / "queue"), "writer", "claude-opus-5-5")
    for _ in range(2):                                  # re-asking doesn't re-queue
        with pytest.raises(PendingResponse):
            call(log, q, role="writer", stage="draft", system="S", user="U")
    assert [r["kind"] for r in log.records()] == ["request"]
    (rid,) = [os.path.basename(p).split(".")[0] for p in glob.glob(str(tmp_path / "queue/*.request.json"))]
    (tmp_path / "queue" / f"{rid}.response.md").write_text("the answer")
    for _ in range(2):                                  # a resume re-reads; logged once
        assert call(log, q, role="writer", stage="draft", system="S", user="U") == "the answer"
    calls = [r for r in log.records() if r["kind"] == "call"]
    assert len(calls) == 1 and calls[0]["meta"]["request_id"] == rid
    assert calls[0]["model_served"] == "unrecorded (agent-written)"


def test_end_to_end_via_queue(tmp_path):
    cfg = {**CONFIG, "writer": {"kind": "queue", "model": "m"},
           "objector": {"kind": "queue", "model": "m"}}
    backends = {"critic_hat": FakeServedCritic("hat-model"),
                "critic_placebo": FakeServedCritic("placebo-model"), "retriever": FakeRetriever()}
    run = Run.create(str(tmp_path), cfg, backends=backends, run_id="q1")
    queue = run.path("queue")
    assert os.path.exists(os.path.join(queue, "README.md"))
    cycles = 0
    for stage in (run.theses, run.screen, run.develop):
        while True:
            try:
                stage()
                break
            except PendingBatch:
                assert _answer_queue(queue) > 0
                cycles += 1
    sel = run.select()
    assert sel["winner"] == "t01" and cycles >= 3
    calls = [r for r in run.log.records() if r["kind"] == "call" and r["backend"] == "queue"]
    ids = [c["meta"]["request_id"] for c in calls]
    assert len(ids) == len(set(ids))                    # no answer logged twice
    hat_calls = [r for r in run.log.records() if r["kind"] == "call" and r["role"] == "critic:hat"]
    # 2 candidates x (round1: 4 steps, round2: 3, final: 3) — checkpoints stop re-critiquing
    assert len(hat_calls) == 2 * (4 + 3 + 3)
    assert not glob.glob(run.path("candidates", "*.partial.json"))
    assert run.log.verify()[0]


def _fake_claude(tmp_path, help_text):
    fake = tmp_path / "claude"
    fake.write_text(f"#!{sys.executable}\n" + f"HELP = {help_text!r}\n" + """import json, os, sys
if sys.argv[1:] == ["--version"]:
    print("9.9.9 (Claude Code)"); sys.exit(0)
if sys.argv[1:] == ["--help"]:
    print(HELP); sys.exit(0)
print(json.dumps({"type": "result", "subtype": "success", "is_error": False,
                  "result": json.dumps({"argv": sys.argv[1:], "stdin": sys.stdin.read(),
                                        "cwd_files": os.listdir(".")}),
                  "stop_reason": "end_turn",
                  "modelUsage": {"claude-opus-5-5": {}}, "session_id": "s-1",
                  "duration_ms": 7, "num_turns": 1, "total_cost_usd": 0.01,
                  "usage": {"input_tokens": 3, "output_tokens": 4}}))
""")
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    return str(fake)


@pytest.mark.parametrize("help_text,isolated", [
    ("--tools --safe-mode --no-session-persistence --effort <level>", True),   # new CLI
    ("--tools --model", False),                                               # 2.0.x
])
def test_agent_driver_runs_claude_headless_and_isolated(tmp_path, help_text, isolated):
    cli = agent.ClaudeCLI(_fake_claude(tmp_path, help_text))
    q = FileQueueBackend(str(tmp_path / "queue"), "objector", "claude-opus-5-5", effort="high")
    with pytest.raises(PendingResponse) as e:
        q.complete("SYS", "the user prompt", stage="novelty")
    meta = agent.answer_one(e.value.path, cli)
    assert meta["model_served"] == "claude-opus-5-5" and meta["claude_code_version"].startswith("9.9.9")
    assert meta["effort"] == ("high" if isolated else None)        # recorded, never assumed
    got = json.loads(q.complete("SYS", "the user prompt", stage="novelty").text)
    argv = got["argv"]
    assert argv[argv.index("--tools") + 1] == ""                    # no tools at all
    assert argv[argv.index("--system-prompt") + 1] == "SYS"         # our system prompt only
    assert "--strict-mcp-config" in argv and argv[argv.index("--model") + 1] == "claude-opus-5-5"
    assert ("--safe-mode" in argv) is isolated and ("--no-session-persistence" in argv) is isolated
    assert got["stdin"] == "the user prompt" and got["cwd_files"] == []   # empty sandbox cwd
    assert agent.pending(str(tmp_path / "queue")) == []


def test_ssh_command_quotes_prompts():
    cli = agent.ClaudeCLI("claude", ssh="user@gpu-host")
    cmd = cli.remote_command(["-p", "--tools", "", "--system-prompt", "It's \"quoted\"; $(rm -x)"])
    assert cmd.startswith('cd "$(mktemp -d)" && claude -p --tools \'\' --system-prompt ')
    assert "'It'\"'\"'s \"quoted\"; $(rm -x)'" in cmd             # inert inside single quotes


def test_overlong_revision_is_fit_before_final_critique(tmp_path):
    long_essay = "# Essay\n\nREVISED " + "word " * 7000 + "\n\n## References\n\n- Pearl\n"

    def wordy_writer(stage, system, user):
        if stage.startswith("respond"):
            assert "within 6000 words" in user                 # the limit reaches the writer
            return json.dumps({"responses": [{"step": 4, "action": "fix", "reason": "r"}],
                               "essay": long_essay})
        if stage == "fit-length":
            assert "hard limit is 6000" in user
            return ESSAY.replace("several steps", "several steps REVISED")
        return writer_fn(stage, system, user)

    backends = {"writer": StubBackend(wordy_writer), "objector": StubBackend(objector_fn),
                "critic_hat": FakeServedCritic("hat"), "critic_placebo": FakeServedCritic("p"),
                "retriever": FakeRetriever()}
    run = Run.create(str(tmp_path), CONFIG, backends=backends, run_id="fit")
    run.theses(); run.screen(); run.develop()
    cand = run.load("candidates", "t02.json")
    assert S.word_count(cand["final"]["essay"]) <= 6000
    stages = [r["stage"] for r in run.log.records() if r["kind"] == "call" and r["role"] == "writer"]
    assert stages.index("fit-length") < len(stages) - 1 - stages[::-1].index("steps")


def test_critic_accepts_truncation_but_writer_does_not(tmp_path):
    class Wordy:
        kind, model = "openai-compat", "phi-4"

        def complete(self, system, user, *, stage, max_tokens=None):
            return Completion(text="No fallacy. And then at great length", model="phi-4",
                              stop_reason="length")

    log = RunLog(str(tmp_path / "log.jsonl"))
    v = S.critique(log, Wordy(), ["P. Therefore, C."], "c1", "placebo", 1)
    assert v[0]["flag"] is False
    assert log.records()[-1]["stop_reason"] == "length"        # still on the record
    from essay.backends import TruncatedError
    with pytest.raises(TruncatedError):
        call(log, Wordy(), role="writer", stage="draft", user="U")


@pytest.mark.parametrize("text,verdict,name", [
    # trained format (the hat)
    ("No fallacy. The argument logically derives the conditions.", "no_fallacy", None),
    ("Fallacy: composition. Parts vs whole.", "fallacy", "composition"),
    # prose from the base model behind the placebo arm (real PoC answers)
    ("The argument presented does not contain any obvious logical fallacies. It is a "
     "structured reasoning about interventionist surgery.", "no_fallacy", None),
    ("The argument presented does not appear to contain a logical fallacy. It is "
     "structured as a reasoned response.", "no_fallacy", None),
    ("This passage contains a few potential logical fallacies or areas of unclear "
     "reasoning. Let's break it down:\n\n1. **Begging the Question (Petitio Principii)**",
     "fallacy", "Begging the Question (Petitio Principii)"),
    ("The passage you provided is a philosophical argument discussing the nature of "
     "grounding, particularly essence-backed grounding.", "unclear", None),
    ("The passage is a philosophical argument about grounding.\n\n**No Fallacy**: the "
     "inference is valid given the premises.", "no_fallacy", None),
    ("The argument involves several concepts relating mental variables to realizers.\n\n"
     "1. **Essence-Fixed Link and Counteressential Interventions**: the argument holds "
     "that an essence-fixed link rules out separate intervention.", "unclear", None),
])
def test_parse_verdict_reads_prose(text, verdict, name):
    v = S.parse_verdict(text)
    assert v["verdict"] == verdict and v["flag"] is (verdict == "fallacy") and v["fallacy"] == name


def test_writer_chooses_area_when_none_is_given(tmp_path):
    seen = []

    def w(stage, system, user):
        seen.append((stage, user))
        return writer_fn(stage, system, user)
    backends = {"writer": StubBackend(w), "objector": StubBackend(objector_fn)}
    run = Run.create(str(tmp_path), {**CONFIG, "area": None}, backends=backends, run_id="r1")
    assert len(run.theses()) == 4
    assert [s for s, _ in seen] == ["area", "theses"]
    assert "metaphysics of causation (open question: Are omissions causes?)" in seen[1][1]
    assert run.load("area.json")["chosen"] == 1
    assert run.area() == "metaphysics of causation (open question: Are omissions causes?)"
    assert len(seen) == 2                                        # chosen once, then read back
    notes = [r["note"] for r in run.log.records() if r["kind"] == "human"]
    assert notes == ["Area left to the writer: no human choice of topic, position or thesis."]


def test_served_writer_leaves_max_tokens_to_vllm(monkeypatch):
    from essay import backends as B
    bodies = []

    class Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"model": "phi-4", "choices": [
                {"message": {"content": "ok"}, "finish_reason": "stop"}]}).encode()

    def fake_urlopen(req, timeout):
        bodies.append((json.loads(req.data), timeout))
        return Resp()
    monkeypatch.setattr(B.urllib.request, "urlopen", fake_urlopen)
    from essay.pipeline import _llm
    w = _llm({"kind": "openai-compat", "url": "http://x", "model": "phi-4",
              "temperature": 0.7}, "/nonexistent", "writer")
    assert w.complete(None, "u", stage="draft").text == "ok"
    body, timeout = bodies[0]
    assert "max_tokens" not in body and body["temperature"] == 0.7 and timeout == 1800
    B.OpenAICompatBackend("http://x", "fallacy-restraint").complete(None, "u", stage="c")
    assert bodies[1][0]["max_tokens"] == 400                     # the critic keeps its cap


def test_replay_scores_format_agreement_and_counterfactuals(tmp_path):
    from essay import replay as R
    run = _run(tmp_path)
    run.theses(); run.screen(); run.develop(); run.select()

    def small(stage, system, user):
        if stage == "novelty":
            return json.dumps({"verdict": "known"})              # disagrees on every thesis
        if stage == "objection-check":
            return "Sure! The essay addresses it."               # unusable: no JSON
        if stage == "steps":
            return json.dumps(["only one step. Therefore, C."])
        return writer_fn(stage, system, user) if stage in ("theses", "draft", "citations") \
            or stage.startswith("respond") else objector_fn(stage, system, user)
    assert R.replay(run.dir, {"small": StubBackend(small, model="small")}, k=2) == \
        {"small": 2 * len(R.frontier_calls(run.dir))}
    assert R.replay(run.dir, {"small": StubBackend(small, model="small")}, k=2) == \
        {"small": 0}                                             # resumable: nothing redone
    st = R.summarize(run.dir)["models"]["small"]
    nov, chk = st["stages"]["novelty"], st["stages"]["objection-check"]
    assert nov["format_ok_rate"] == 1.0 and nov["single_agree"] < 1.0
    assert chk["format_ok_rate"] == 0.0 and chk["vote_usable"] == "0/2"
    assert st["stages"]["objection"]["single_agree"] == 1.0
    assert st["stages"]["steps"]["single_size_ratio"] < 1.0
    cf = st["counterfactual_vote"]
    assert cf["shortlist"]["actual"] == ["t02", "t01"] and cf["shortlist"]["replayed"] == []
    assert cf["winner"]["actual"] == "t01" and cf["winner"]["substituted"] == 0
    assert RunLog(run.path("replay", "small.jsonl")).verify()[0]
    assert run.log.verify()[0]                                   # the run itself untouched


def test_served_backend_retries_transient_errors_only(monkeypatch):
    import urllib.error
    from essay import backends as B
    monkeypatch.setattr(B.time, "sleep", lambda s: None)
    fails = [urllib.error.URLError("reset"),
             urllib.error.HTTPError("u", 502, "bad gateway", {}, None)]

    class Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"choices": [{"message": {"content": "ok"},
                                            "finish_reason": "stop"}]}).encode()

    def flaky(req, timeout):
        if fails:
            raise fails.pop(0)
        return Resp()
    monkeypatch.setattr(B.urllib.request, "urlopen", flaky)
    assert B.OpenAICompatBackend("http://x", "m").complete(None, "u", stage="s").text == "ok"

    def bad_request(req, timeout):
        raise urllib.error.HTTPError("u", 400, "context too long", {}, None)
    monkeypatch.setattr(B.urllib.request, "urlopen", bad_request)
    with pytest.raises(urllib.error.HTTPError):
        B.OpenAICompatBackend("http://x", "m").complete(None, "u", stage="s")


def test_kappa_and_tie_at_cut():
    from essay import replay as R
    assert R._kappa([("a", "a"), ("a", "a")]) is None             # one label: uninformative
    assert R._kappa([("a", "a"), ("b", "b")]) == 1.0
    assert R._kappa([("a", "b"), ("b", "a")]) < 0
    assert R._kappa([("a", None), ("b", "b")]) == 0.333           # unusable is its own label
    row = lambda i, v, s: {"id": i, "novelty": {"verdict": v}, "objection": {"severity": s}}
    tied = [row("t01", "partly", 4), row("t02", "partly", 4), row("t03", "partly", 4)]
    assert R._tie_at_cut(tied, DEFAULT_RULE) is True
    assert R._tie_at_cut([row("t01", "novel", 4), row("t02", "partly", 2),
                          row("t03", "partly", 4)], DEFAULT_RULE) is False


def test_ranking_variants_and_metrics(tmp_path):
    from essay import ranking as K
    pool = [{"id": f"t{i:02d}", "title": "", "thesis": f"T{i}", "argument_sketch": "s",
             "why_new": "w"} for i in range(1, 7)]
    ids = [t["id"] for t in pool]

    def prefers_low_ids(stage, system, user):
        found = [x for x in ids if f"[{x}]" in user]
        if stage.startswith("pair"):
            a, b = user.index("\nA:\n"), user.index("\nB:\n")
            ia = next(x for x in ids if f"[{x}]" in user[a:b])
            ib = next(x for x in ids if f"[{x}]" in user[b:])
            return json.dumps({"better": "A" if ia < ib else "B"})
        if stage.startswith("point"):
            n = int(found[0][1:])
            return json.dumps({"originality": 10 - n, "defensibility": 5})
        return json.dumps({"ranking": ids[:4] + ["t99", "t01"]})    # junk, repeat, missing
    be = StubBackend(prefers_low_ids)
    log = RunLog(str(tmp_path / "rank.jsonl"))
    for name, fn in K.VARIANTS.items():
        r, info = fn(log, be, pool)
        assert r == ids, name
    r, ok = K.parse_ranking(json.dumps({"ranking": ["t03", "[t01]", "t03"]}), ids)
    assert not ok and r == ["t03", "t01", "t02", "t04", "t05", "t06"]
    assert K.kendall_tau(ids, ids) == 1.0 and K.kendall_tau(ids, ids[::-1]) == -1.0
    assert K.borda([["a", "b", "c"], ["b", "a", "c"]]) == ["a", "b", "c"]   # tie -> id
    assert K.top_overlap(ids, ids[::-1], 2) == 0
    assert log.verify()[0]                                       # threaded appends chain
    always_b = StubBackend(lambda stage, system, user: json.dumps({"better": "B"}))
    r, info = K.v_pairwise_both(RunLog(str(tmp_path / "b.jsonl")), always_b, pool)
    assert info["draws"] == 15 and info["slot_picks"] == {"first": 0, "second": 30}


def test_queued_reference_queues_every_sample_before_pending(tmp_path):
    from essay import ranking as K
    pool = [{"id": "t01", "thesis": "a", "argument_sketch": "s"},
            {"id": "t02", "thesis": "b", "argument_sketch": "s"}]
    be = FileQueueBackend(str(tmp_path / "q"), "ranker", "claude")
    log = RunLog(str(tmp_path / "log.jsonl"))
    with pytest.raises(PendingResponse):
        K.v_list(log, be, pool, 2, "ref", workers=1)
    reqs = sorted(glob.glob(str(tmp_path / "q" / "*.request.json")))
    assert len(reqs) == 2
    for req in reqs:
        open(req.replace(".request.json", ".response.md"), "w").write(
            json.dumps({"ranking": ["t02", "t01"]}))
    r, info = K.v_list(log, be, pool, 2, "ref", workers=1)
    assert r == ["t02", "t01"] and info["samples"] == 2


def test_ssh_failures_back_off_then_succeed(monkeypatch):
    import subprocess as sp
    calls, slept = [], []
    codes = [255, 255, 0]

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return sp.CompletedProcess(cmd, codes.pop(0), stdout="ok", stderr="")
    monkeypatch.setattr(agent.subprocess, "run", fake_run)
    monkeypatch.setattr(agent.time, "sleep", slept.append)
    p = agent.ClaudeCLI(ssh="u@h").run(["--version"])
    assert p.returncode == 0 and len(calls) == 3 and slept == [60, 120]
    assert "ControlMaster=auto" in calls[0]                       # one shared connection


def _v3_backends(prefer="Thesis T4"):
    def writer(stage, system, user):
        if stage == "draft":                     # each essay carries its thesis
            return ESSAY.replace("several steps", user.split("\n")[0])
        return writer_fn(stage, system, user)

    def referee(stage, system, user):
        if stage.startswith("screen-rank"):
            return json.dumps({"ranking": ["t03", "t04", "t02", "t01"]})
        if stage.startswith("final-compare"):
            a, b = user.split("=== Essay B ===")[0], user.split("=== Essay B ===")[1]
            return json.dumps({"better": "A" if prefer in a else "B" if prefer in b
                               else "A", "reason": "r"})
        return objector_fn(stage, system, user)
    critics = {}
    for arm in ("hat", "placebo"):
        critics[f"critic_{arm}"] = StubBackend(lambda *a: "No fallacy. Valid.",
                                               model=f"{arm}-model")
        critics[f"critic_{arm}"].kind = "openai-compat"   # a served critic, not a stub
    return {"writer": StubBackend(writer), "objector": StubBackend(referee), **critics,
            "retriever": FakeRetriever()}


def test_rule_v3_ranks_screen_and_decides_by_head_to_head(tmp_path):
    from essay.selection import RULE_V3
    rule = {**RULE_V3, "final": {"method": "pairwise", "rounds": 1}}
    run = Run.create(str(tmp_path), CONFIG, rule=rule, backends=_v3_backends(), run_id="r1")
    run.theses()
    # ranked t03 first, but t03 is "known": the novelty gate skips it
    assert run.screen() == ["t04", "t02", "t01"]
    assert run.load("ranking.json")["order"] == ["t03", "t04", "t02", "t01"]
    calls = [r for r in run.log.records() if r["kind"] == "call"]
    assert sum(r["stage"] == "novelty" for r in calls) == 4      # stopped once 3 passed
    run.develop()
    sel = run.select()
    score = {r["id"]: r["score"] for r in sel["ranking"]}
    assert score["t04"] < score["t01"] == score["t02"]          # t04 is only "partly" novel
    assert sel["decided_by"] == "pairwise" and sel["winner"] == "t04"   # not score, not id
    fp = sel["final_pairwise"]
    assert fp["comparisons"] == 6 and fp["wins"]["t04"] == 4 and not fp["tie_at_top"]
    assert run.log.verify()[0]


def test_rule_v3_final_queues_every_comparison_first(tmp_path):
    from essay.selection import RULE_V3
    run = Run.create(str(tmp_path), CONFIG, rule=RULE_V3, backends=_v3_backends(),
                     run_id="r1")
    run.theses(); run.screen(); run.develop()
    q = FileQueueBackend(str(tmp_path / "q"), "objector", "claude")
    run._b["objector"] = q
    with pytest.raises(PendingBatch) as e:
        run.select()
    assert e.value.stage == "select" and e.value.n == 3 * 2 * 3   # 3 pairs, 2 orders, 3 rounds
    assert len(glob.glob(str(tmp_path / "q" / "*.request.json"))) == 18


def test_rank_probe_cache_reuses_logged_answers_in_order(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("rank_exp", "labs/rank_exp.py")
    rx = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rx)
    old = RunLog(str(tmp_path / "old.jsonl"))
    for text in ("first", "second"):                             # two samples, same prompt
        old.append("call", role="ranker", stage="s", system="S", user="U", response=text)
    old.append("call", role="ranker", stage="s", system="S", user="U", error="boom")
    asked = []
    inner = StubBackend(lambda stage, system, user: asked.append(user) or "fresh")
    c = rx.Cached(inner, old.records())
    got = [c.complete("S", "U", stage="s").text for _ in range(3)]
    assert got == ["first", "second", "fresh"] and asked == ["U"] and c.reused == 2
    assert c.complete("S", "other", stage="s").text == "fresh"


def _polish_backends(prefer_revised=True):
    def body(user):
        return user.split("Essay:\n\n", 1)[1].split("\n\n=== End of essay ===")[0]

    def writer(stage, system, user):
        if stage.startswith("polish-revise"):
            return body(user) + "\nPOLISHED"
        if stage.startswith("polish-refs"):
            refs = [{"authors": ["Pearl"], "title": "Causality", "year": 2009}]
            if "FIXED" not in user:
                refs.append({"authors": ["Nobody"], "title": "A Book That Does Not Exist",
                             "year": 2031})
            return json.dumps(refs)
        if stage == "polish-fixrefs":
            return body(user) + "\nFIXED"
        return writer_fn(stage, system, user)

    def referee(stage, system, user):
        if stage.startswith("polish-report"):
            return json.dumps({"contribution": "c", "major": ["m1"], "minor": ["n1"]})
        if stage.startswith("polish-compare"):
            a, b = user.split("=== Essay B ===")
            more_a = a.count("POLISHED") > b.count("POLISHED")
            return json.dumps({"better": ("A" if more_a else "B") if prefer_revised
                               else ("B" if more_a else "A")})
        return objector_fn(stage, system, user)
    return {"writer": StubBackend(writer), "objector": StubBackend(referee)}


def _fake_lookup(ref):
    if ref["title"] == "Causality":
        return [{"source": "openalex", "title": "Causality", "year": 2009,
                 "authors": ["Judea Pearl"]}]
    return [{"source": "crossref", "title": "Something Else Entirely", "year": 1990,
             "authors": ["Smith"]}]


def _finished_run(tmp_path):
    run = _run(tmp_path)
    run.theses(); run.screen(); run.develop(); run.select()
    return run


def test_polish_ratchet_keeps_only_winning_revisions_then_checks_citations(tmp_path):
    from essay.polish import Polish
    run = _finished_run(tmp_path)
    original = open(run.path("final.md")).read()
    p = Polish.create(run.dir, backends=_polish_backends(True), lookup_fn=_fake_lookup)
    s = p.run()
    assert [r["accepted"] for r in s["rounds"]] == [True, True, True]
    assert all(r["revised_wins"] == 6 and r["of"] == 6 for r in s["rounds"])
    final = open(os.path.join(p.dir, "final.md")).read()
    assert final.count("POLISHED") == 3 and "FIXED" in final
    assert s["citations"]["c0"]["unverified"] == 1 and s["citations"]["c1"]["unverified"] == 0
    assert open(run.path("final.md")).read() == original           # parent untouched
    assert p.log.verify()[0] and run.log.verify()[0]
    first = p.log.records()[0]
    assert first["kind"] == "init" and first["parent_log_head"] == run.log.records()[-1]["hash"]
    with pytest.raises(FileExistsError):
        Polish.create(run.dir, backends=_polish_backends(True), lookup_fn=_fake_lookup)


def test_polish_rejects_revisions_the_referee_prefers_less(tmp_path):
    from essay.polish import Polish
    run = _finished_run(tmp_path)
    original = open(run.path("final.md")).read()
    p = Polish.create(run.dir, backends=_polish_backends(False), lookup_fn=_fake_lookup)
    s = p.run()
    assert [r["accepted"] for r in s["rounds"]] == [False, False, False]
    final = open(os.path.join(p.dir, "final.md")).read()
    assert "POLISHED" not in final and final.startswith(original.rstrip())   # + the ref fix


def test_citation_match_rules():
    from essay.polish import POLISH_RULE, match
    ref = {"authors": ["Kripke"], "title": "Naming and Necessity", "year": 1980}
    good = {"source": "openalex", "title": "Naming and necessity", "year": 1981,
            "authors": ["Saul A. Kripke"]}
    m = match(ref, [good], POLISH_RULE)
    assert m["verified"] and not m["year_note"]
    # 1972 paper vs 1980 book: exact title + confirmed author verifies, year noted
    m = match(ref, [{**good, "year": 1972}], POLISH_RULE)
    assert m["verified"] and m["year_note"]
    # a year that far off with no author to confirm it does not verify
    assert not match(ref, [{**good, "year": 1972, "authors": []}], POLISH_RULE)["verified"]
    assert not match(ref, [{**good, "authors": ["Lewis"]}], POLISH_RULE)["verified"]
    sub = {"authors": ["Parfit"], "title": "Reasons and Persons", "year": 1984}
    assert match(sub, [{"source": "crossref", "title": "Reasons and Persons: A Study",
                        "year": 1984, "authors": ["Parfit"]}], POLISH_RULE)["verified"]
    assert not match(ref, [{"source": "openalex", "error": "timeout"}], POLISH_RULE)["verified"]


def test_polish_revert_citation_fix_restores_ratchet_output(tmp_path):
    from essay.polish import Polish
    run = _finished_run(tmp_path)
    p = Polish.create(run.dir, backends=_polish_backends(True), lookup_fn=_fake_lookup)
    p.run()
    fixed = open(os.path.join(p.dir, "final.md")).read()
    assert "FIXED" in fixed
    rec = p.revert_citation_fix("entrant: revert it", "fix was triggered by a lookup error")
    final = open(os.path.join(p.dir, "final.md")).read()
    assert final == p.ratchet_output() and "FIXED" not in final and final.count("POLISHED") == 3
    assert open(os.path.join(p.dir, "final.fixed-superseded.md")).read() == fixed
    kinds = [r["kind"] for r in p.log.records()[-2:]]
    assert kinds == ["human", "revert-citation-fix"] and p.log.verify()[0]
    assert json.load(open(os.path.join(p.dir, "summary.json")))["final_sha256"] == rec["to_sha256"]
    with pytest.raises(RuntimeError):
        p.revert_citation_fix("again", "no-op")


def test_polish_valid_fix_sends_only_checked_failures_once(tmp_path):
    from essay.polish import Polish
    run = _finished_run(tmp_path)
    p = Polish.create(run.dir, backends=_polish_backends(True), lookup_fn=_fake_lookup)
    p.run()
    p.revert_citation_fix("entrant: revert", "spoiled check")           # back to the ratchet output
    with pytest.raises(RuntimeError):
        p.valid_fix()                                                   # no recheck yet
    chk = p.recheck("c0.refs")
    assert len(chk["unverified"]) == 1 and chk["unchecked"] == 0
    res = p.valid_fix()
    final = open(os.path.join(p.dir, "final.md")).read()
    assert "FIXED" in final and res["unverified_after"] == [] and res["verified_after"] == 1
    assert open(os.path.join(p.dir, "final.pre-validfix.md")).read() == p.ratchet_output()
    assert p.log.records()[-1]["kind"] == "citation-fix-valid" and p.log.verify()[0]
    fixes = [r for r in p.log.records() if r["kind"] == "call" and r["stage"] == "polish-fixrefs"]
    assert len(fixes) == 2                                              # run()'s, then this one
