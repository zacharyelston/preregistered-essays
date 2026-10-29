"""One run = one directory: config, pre-registration, the chained log, and each
stage's output as JSON. Stages are resumable (finished work is skipped), so a
crash or a refusal mid-`develop` doesn't cost the candidates already done.

  <run>/config.json      area + backend specs (no secrets: keys come from env vars)
  <run>/prereg.json      the selection rule + its hash
  <run>/log.jsonl        every call / retrieval / human note / stage event
  <run>/theses.json      the candidate pool
  <run>/screened.json    + objection and novelty per thesis
  <run>/shortlist.json   ids chosen by the rule
  <run>/candidates/*.json full development record per shortlisted thesis
                         (*.partial.json: step checkpoints while in progress)
  <run>/queue/           queued writer/objector requests + answers (queue backend)
  <run>/selection.json   ranking + winner;  <run>/final.md  the winning essay

With the queue backend a stage stops at the first unanswered request on each path,
having queued every request it can; answer them and re-run the same stage.
"""
from __future__ import annotations

import itertools
import json
import os
import time

from . import ranking as K
from . import stages as S
from .backends import (QUEUE_README, ClaudeBackend, FileQueueBackend, MyvectRetriever,
                       OpenAICompatBackend, PendingResponse, StubBackend)
from .log import RunLog
from .selection import load_rule, preregister, rank, shortlist

STUB_CRITIC_REPLY = "No fallacy. (stub critic: the fallacy-restraint hat is not served yet)"


class PendingBatch(RuntimeError):
    def __init__(self, stage: str, n: int):
        super().__init__(f"{stage}: {n} request(s) awaiting answers")
        self.stage, self.n = stage, n


def _llm(spec: dict, run_dir: str, role: str):
    if spec["kind"] == "claude":
        return ClaudeBackend(model=spec["model"], effort=spec.get("effort", "high"))
    if spec["kind"] == "queue":
        return FileQueueBackend(os.path.join(run_dir, "queue"), role, spec["model"],
                                effort=spec.get("effort"))
    if spec["kind"] == "openai-compat":   # writer / objector: long answers, no token cap
        return OpenAICompatBackend(spec["url"], spec["model"], api_key_env=spec.get("key_env"),
                                   max_tokens=spec.get("max_tokens"),
                                   extra=spec.get("extra"),
                                   temperature=spec.get("temperature", 0.0),
                                   timeout=spec.get("timeout", 1800))
    raise ValueError(f"unknown backend kind {spec['kind']!r}")


def _critic(spec: dict, arm: str):
    if spec["kind"] == "stub":
        return StubBackend(lambda *_: STUB_CRITIC_REPLY, model=f"stub-critic-{arm}")
    model = spec["hat_model"] if arm == "hat" else spec["base_model"]
    return OpenAICompatBackend(spec["url"], model, api_key_env=spec.get("key_env"))


class Run:
    def __init__(self, run_dir: str, backends: dict | None = None):
        self.dir = run_dir
        with open(os.path.join(run_dir, "config.json")) as f:
            self.config = json.load(f)
        self.log = RunLog(os.path.join(run_dir, "log.jsonl"))
        self._b = dict(backends or {})

    @classmethod
    def create(cls, runs_dir: str, config: dict, rule: dict | None = None,
               backends: dict | None = None, run_id: str | None = None) -> "Run":
        run_id = run_id or time.strftime("%Y%m%d-%H%M%S")
        run_dir = os.path.join(runs_dir, run_id)
        os.makedirs(os.path.join(run_dir, "candidates"))
        with open(os.path.join(run_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=1, sort_keys=True)
        log = RunLog(os.path.join(run_dir, "log.jsonl"))
        log.append("init", run_id=run_id, config=config)
        if config.get("area"):
            log.human(f"Area chosen: {config['area']}")
        else:
            log.human("Area left to the writer: no human choice of topic, position or thesis.")
        preregister(run_dir, log, rule)
        if any(config[r]["kind"] == "queue" for r in ("writer", "objector")):
            os.makedirs(os.path.join(run_dir, "queue"))
            with open(os.path.join(run_dir, "queue", "README.md"), "w") as f:
                f.write(QUEUE_README)
        return cls(run_dir, backends)

    # -- backends (injectable for tests; else built from config) -------------
    def _get(self, key, build):
        if key not in self._b:
            self._b[key] = build()
        return self._b[key]

    def writer(self):
        return self._get("writer", lambda: _llm(self.config["writer"], self.dir, "writer"))

    def objector(self):
        return self._get("objector", lambda: _llm(self.config["objector"], self.dir, "objector"))

    def critic(self, arm: str):
        return self._get(f"critic_{arm}", lambda: _critic(self.config["critic"], arm))

    def retriever(self):
        mv = self.config.get("myvect")
        return self._get("retriever",
                         lambda: MyvectRetriever(mv["url"], mv["boxes"]) if mv else None)

    # -- state ----------------------------------------------------------------
    def path(self, *parts):
        return os.path.join(self.dir, *parts)

    def load(self, *parts, default=None):
        p = self.path(*parts)
        if not os.path.exists(p):
            return default
        with open(p) as f:
            return json.load(f)

    def save(self, obj, *parts):
        with open(self.path(*parts), "w") as f:
            json.dump(obj, f, indent=1, ensure_ascii=False)

    def rule(self) -> dict:
        return load_rule(self.dir, self.log)

    # -- stages ---------------------------------------------------------------
    def area(self) -> str:
        """The human's area if one was given, else the writer's choice (area.json)."""
        if self.config.get("area"):
            return self.config["area"]
        a = self.load("area.json")
        if a is None:
            a = S.choose_area(self.log, self.writer(), avoid=self.config.get("avoid_areas"))
            self.save(a, "area.json")
            self.log.append("stage", stage="area", area=a["area"], question=a["question"])
        return S.area_text(a)

    def theses(self) -> list[dict]:
        if self.load("theses.json"):
            raise RuntimeError("theses already generated for this run (the pool is fixed)")
        rule = self.rule()
        try:
            pool = S.propose_theses(self.log, self.writer(), self.area(),
                                    rule["screen"]["n_theses"])
        except PendingResponse:
            raise PendingBatch("theses", 1) from None
        self.save(pool, "theses.json")
        self.log.append("stage", stage="theses", n=len(pool))
        return pool

    def screen(self) -> list[str]:
        rule, pool = self.rule(), self.load("theses.json")
        if not pool:
            raise RuntimeError("run `theses` first")
        if rule["screen"].get("method") == "rank":
            return self._screen_ranked(rule, pool)
        done = {t["id"]: t for t in self.load("screened.json", default=[])}
        waiting = 0
        for t in pool:
            cur = done.setdefault(t["id"], dict(t))
            for key, fn in (("objection", S.objection), ("novelty", S.novelty)):
                if key in cur:
                    continue
                try:
                    cur[key] = fn(self.log, self.objector(), t)
                except PendingResponse:
                    waiting += 1
                    continue
                self.save(list(done.values()), "screened.json")
        if waiting:
            raise PendingBatch("screen", waiting)
        ids = shortlist(list(done.values()), rule)
        self.save(ids, "shortlist.json")
        self.log.append("stage", stage="screen", shortlist=ids)
        return ids

    def _screen_ranked(self, rule: dict, pool: list[dict]) -> list[str]:
        """Rule v3: the referee ranks the pool (shuffled orders, mean position), then
        objection + novelty run down that ranking until shortlist_k theses pass the
        novelty gate. A thesis still awaiting its answers counts provisionally, so a
        queued batch never runs further down the ranking than it needs to."""
        s = rule["screen"]
        ranking = self.load("ranking.json")
        if ranking is None:
            try:
                order, info = K.v_list(self.log, self.objector(), pool, s["rankings"],
                                       "screen-rank", workers=1, shuffle=True)
            except PendingResponse:
                raise PendingBatch("screen", s["rankings"]) from None
            if order is None:
                raise RuntimeError("screen: the referee gave no usable ranking")
            ranking = {"order": order, **info}
            self.save(ranking, "ranking.json")
            self.log.append("stage", stage="screen-rank", order=order,
                            incomplete=info["incomplete"], unusable=info["unusable"])
        by_id = {t["id"]: t for t in pool}
        done = {t["id"]: t for t in self.load("screened.json", default=[])}
        ids, provisional, waiting = [], 0, 0
        for tid in ranking["order"]:
            if len(ids) + provisional >= s["shortlist_k"]:
                break
            cur = done.setdefault(tid, dict(by_id[tid]))
            pending_here = False
            for key, fn in (("objection", S.objection), ("novelty", S.novelty)):
                if key in cur:
                    continue
                try:
                    cur[key] = fn(self.log, self.objector(), by_id[tid])
                except PendingResponse:
                    waiting += 1
                    pending_here = True
                    continue
                self.save(list(done.values()), "screened.json")
            if pending_here:
                provisional += 1
            elif cur["novelty"]["verdict"] not in s["exclude_novelty"]:
                ids.append(tid)
        if waiting:
            raise PendingBatch("screen", waiting)
        self.save(ids, "shortlist.json")
        self.log.append("stage", stage="screen", shortlist=ids, method="rank")
        return ids

    def _critique_all(self, steps, cid, rnd, arms):
        return {arm: S.critique(self.log, self.critic(arm), steps, cid, arm, rnd) for arm in arms}

    def develop_one(self, t: dict, rule: dict) -> dict:
        """Checkpointed: each finished step is saved to <cid>.partial.json, so a
        resume (after a pending answer, a crash, a refusal) never re-runs or
        re-logs a step — including the critic calls, which aren't queued."""
        dv, cid = rule["develop"], t["id"]
        arm, w = rule["critic_arm"], self.writer()
        max_words = rule["gates"]["max_words"]
        ck = self.load("candidates", f"{cid}.partial.json", default={})

        def step(key, fn):
            if key not in ck:
                ck[key] = fn()
                self.save(ck, "candidates", f"{cid}.partial.json")
            return ck[key]

        essay = step("draft", lambda: S.draft(self.log, w, t, t["objection"], max_words))
        rounds = []
        for rnd in range(1, dv["rounds"] + 1):
            steps = step(f"r{rnd}.steps",
                         lambda: S.extract_steps(self.log, w, essay, cid, dv["max_steps"]))
            crit = step(f"r{rnd}.critique",
                        lambda: self._critique_all(steps, cid, rnd, dv["critic_arms"]))
            flags = [f for f in crit[arm] if f["flag"]]
            entry = {"round": rnd, "essay_in": essay, "steps": steps, "critique": crit}
            if flags:
                entry["responses"], essay = step(
                    f"r{rnd}.respond",
                    lambda: list(S.respond(self.log, w, essay, flags, cid, rnd, max_words)))
            rounds.append(entry)
            if not flags:
                break
        if S.word_count(essay) > max_words:   # before the final critique, so it sees the cut
            essay = step("fit", lambda: S.fit_length(self.log, w, essay, cid, max_words))
        steps = step("final.steps",
                     lambda: S.extract_steps(self.log, w, essay, cid, dv["max_steps"]))
        cites = step("citations", lambda: S.citations(self.log, w, essay, cid))
        final = {
            "essay": essay, "steps": steps,
            "critique": step("final.critique",
                             lambda: self._critique_all(steps, cid, "final", dv["critic_arms"])),
            "citations": cites,
            "grounding": step("grounding", lambda: S.ground(
                self.log, self.retriever(), cites, cid, rule["ground_min_score"])),
            "objection_check": step("objection_check", lambda: S.check_objection(
                self.log, self.objector(), t["objection"], essay, cid)),
        }
        return {"id": cid, "thesis": t, "objection": t["objection"],
                "novelty": t["novelty"], "rounds": rounds, "final": final}

    def develop(self) -> list[str]:
        rule = self.rule()
        ids = self.load("shortlist.json")
        if ids is None:
            raise RuntimeError("run `screen` first")
        by_id = {t["id"]: t for t in self.load("screened.json")}
        waiting = 0
        for cid in ids:
            if self.load("candidates", f"{cid}.json"):
                continue
            try:
                cand = self.develop_one(by_id[cid], rule)
            except PendingResponse:
                waiting += 1          # this candidate waits; the others keep going
                continue
            self.save(cand, "candidates", f"{cid}.json")
            os.remove(self.path("candidates", f"{cid}.partial.json"))
            self.log.append("stage", stage="develop", candidate=cid,
                            words=S.word_count(cand["final"]["essay"]))
        if waiting:
            raise PendingBatch("develop", waiting)
        return ids

    def _final_pairwise(self, eligible, cands, ranking, rounds) -> dict:
        """Rule v3 final: every pair of eligible finished essays, both orders, `rounds`
        times each, judged by the referee in fresh sessions. Most wins; ties -> score,
        then id. Every comparison is queued before any is awaited."""
        essay = {c["id"]: c["final"]["essay"] for c in cands}
        score = {r["id"]: r["score"] for r in ranking}
        jobs = [(x, y, i) for a, b in itertools.combinations(eligible, 2)
                for x, y in ((a, b), (b, a)) for i in range(rounds)]
        verdicts, waiting = [], 0
        for x, y, i in jobs:
            try:
                v = S.compare_essays(self.log, self.objector(), essay[x], essay[y],
                                     f"{x}|{y}", i)
            except PendingResponse:
                waiting += 1
                continue
            except ValueError:              # unparseable after the retry: no vote
                v = {"better": None, "reason": "unparseable"}
            verdicts.append({"first": x, "second": y, "round": i, **v,
                             "winner": {"A": x, "B": y}.get(v["better"])})
        if waiting:
            raise PendingBatch("select", waiting)
        wins = {c: sum(v["winner"] == c for v in verdicts) for c in eligible}
        order = sorted(eligible, key=lambda c: (-wins[c], -score[c], c))
        slot = {"first": sum(v["winner"] == v["first"] for v in verdicts),
                "second": sum(v["winner"] == v["second"] for v in verdicts)}
        return {"winner": order[0], "wins": wins, "order": order, "comparisons": len(jobs),
                "unusable": sum(v["winner"] is None for v in verdicts),
                "slot_picks": slot, "verdicts": verdicts,
                "tie_at_top": len(order) > 1 and wins[order[0]] == wins[order[1]]}

    def critic_stubbed(self) -> bool:
        return any(r["kind"] == "call" and r["role"].startswith("critic")
                   and r["backend"] == "stub" for r in self.log.records())

    def select(self, allow_stub: bool = False) -> dict:
        rule = self.rule()
        stubbed = self.critic_stubbed()
        if stubbed and not allow_stub:
            raise RuntimeError("critic calls in this run were stubbed; its scores mean "
                               "nothing. Pass allow_stub only for a dry run.")
        ids = self.load("shortlist.json") or []
        cands = [c for c in (self.load("candidates", f"{i}.json") for i in ids) if c]
        if len(cands) != len(ids):
            raise RuntimeError("not every shortlisted candidate is developed; run `develop`")
        ranking = rank(cands, rule)
        winner = next((r["id"] for r in ranking if r["score"] > 0), None)
        final = None
        if rule.get("final", {}).get("method") == "pairwise":
            eligible = [r["id"] for r in ranking if r["score"] > 0]
            if len(eligible) > 1:
                final = self._final_pairwise(eligible, cands, ranking, rule["final"]["rounds"])
                winner = final["winner"]
        records = self.log.records()
        result = {"rule_sha256": next(r["sha256"] for r in records
                                      if r["kind"] == "preregister"),
                  "ranking": ranking, "winner": winner, "critic_stubbed": stubbed,
                  "final_pairwise": final,
                  "decided_by": ("pairwise" if final else
                                 "score" if winner else "no eligible candidate"),
                  "log_head": records[-1]["hash"],
                  "selected_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
        self.save(result, "selection.json")
        if winner:
            essay = next(c for c in cands if c["id"] == winner)["final"]["essay"]
            with open(self.path("final.md"), "w") as f:
                f.write(essay)
        self.log.append("select", winner=winner, critic_stubbed=stubbed,
                        decided_by=result["decided_by"],
                        wins=final and final["wins"],
                        ranking=[{k: r[k] for k in ("id", "score", "gate_failures")}
                                 for r in ranking])
        return result

    def status(self) -> dict:
        recs = self.log.records()
        calls = [r for r in recs if r["kind"] == "call"]
        by_role: dict = {}
        for c in calls:
            row = by_role.setdefault(c["role"], {"calls": 0, "errors": 0,
                                                 "input_tokens": 0, "output_tokens": 0})
            row["calls"] += 1
            row["errors"] += bool(c.get("error"))
            u = c.get("usage") or {}
            row["input_tokens"] += sum(u.get(k) or 0 for k in (   # cache reads/writes are input too
                "input_tokens", "prompt_tokens", "cache_creation_input_tokens",
                "cache_read_input_tokens"))
            row["output_tokens"] += u.get("output_tokens", u.get("completion_tokens", 0)) or 0
        ok, why = self.log.verify()
        return {"run": os.path.basename(self.dir), "log": why if ok else f"BROKEN: {why}",
                "stages": [r["stage"] for r in recs if r["kind"] == "stage"],
                "human_notes": sum(r["kind"] == "human" for r in recs),
                "critic_stubbed": self.critic_stubbed(), "by_role": by_role}
