"""Model + retrieval backends for the essay pipeline, behind one logged `call()`.

  ClaudeBackend        writer / objector — Anthropic SDK, streamed (long drafts),
                       explicit effort, server-side refusal fallback ("default")
  OpenAICompatBackend  the hat critic on the vLLM wardrobe server; the arm is the
                       served model name (base vs the LoRA module), so hat and
                       placebo share one GPU and one prompt
  FileQueueBackend     writer / objector with no API key: each request becomes a
                       file an agent answers (`python -m essay answer` runs
                       Claude Code headless, one fresh session per request)
  StubBackend          scripted answers — tests, and the critic until it's served

`call()` writes the full request and response to the run log *before* judging the
result, so refusals, truncations and transport errors are on the record too.
SDKs are imported lazily: `import essay` stays light and the tests need no keys.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, Protocol

from .log import RunLog, canonical

FALLBACK_BETA = "server-side-fallback-2026-07-01"   # pairs with fallbacks="default"


class RefusalError(RuntimeError):
    pass


class PendingResponse(Exception):
    """A queued request has no answer yet. Stages catch it, finish what they can,
    and resume on the next run once the answer file exists."""

    def __init__(self, request_id: str, path: str, new: bool):
        super().__init__(f"awaiting answer for {request_id}")
        self.request_id, self.path, self.new = request_id, path, new


class TruncatedError(RuntimeError):
    pass


@dataclass
class Completion:
    text: str
    model: str                      # the model that actually served the request
    stop_reason: str | None
    usage: dict = field(default_factory=dict)
    request_id: str | None = None
    meta: dict = field(default_factory=dict)


class Backend(Protocol):
    kind: str
    model: str

    def complete(self, system: str | None, user: str, *, stage: str,
                 max_tokens: int | None = None) -> Completion: ...


class ClaudeBackend:
    kind = "claude"

    def __init__(self, model: str = "claude-opus-5-5", effort: str = "high",
                 max_tokens: int = 64000, client=None):
        self.model, self.effort, self.max_tokens = model, effort, max_tokens
        self._client = client

    def _get_client(self):
        if self._client is None:
            import anthropic           # credentials from the environment / `ant auth login`
            self._client = anthropic.Anthropic()
        return self._client

    def complete(self, system, user, *, stage, max_tokens=None):
        kwargs = dict(model=self.model, max_tokens=max_tokens or self.max_tokens,
                      messages=[{"role": "user", "content": user}],
                      output_config={"effort": self.effort},
                      betas=[FALLBACK_BETA], fallbacks="default")
        if system:
            kwargs["system"] = system
        with self._get_client().beta.messages.stream(**kwargs) as stream:
            msg = stream.get_final_message()
        text = "".join(b.text for b in msg.content if b.type == "text")
        switches = [{"from": getattr(getattr(b, "from_", None), "model", None),
                     "to": getattr(getattr(b, "to", None), "model", None)}
                    for b in msg.content if b.type == "fallback"]
        stop_details = msg.stop_details.to_dict() if getattr(msg, "stop_details", None) else None
        return Completion(text=text, model=msg.model, stop_reason=msg.stop_reason,
                          usage=msg.usage.to_dict(), request_id=msg._request_id,
                          meta={"effort": self.effort, "fallbacks": switches,
                                "stop_details": stop_details})


class OpenAICompatBackend:
    """`/v1/chat/completions` on vLLM. `model` picks the arm: the base model name for
    the placebo arm, the `--lora-modules` name for the hat arm. `max_tokens=None`
    leaves it to vLLM, which allows the rest of the context window (a small model
    as writer: drafts are long and the prompt length varies). `extra` is merged into
    the request body, e.g. {"chat_template_kwargs": {"reasoning_effort": "low"}}
    for a reasoning model (Qwen3.8's template defaults to xhigh). The answer is
    `content` only: vLLM's reasoning parser keeps the thinking out of it."""
    kind = "openai-compat"

    def __init__(self, base_url: str, model: str, api_key_env: str | None = None,
                 max_tokens: int | None = 400, temperature: float = 0.0, timeout: int = 120,
                 extra: dict | None = None, retries: int = 3):
        self.base_url, self.model = base_url.rstrip("/"), model
        self.retries = retries     # transient (5xx / connection) failures, 30 s backoff
        self.api_key_env, self.max_tokens = api_key_env, max_tokens
        self.temperature, self.timeout = temperature, timeout
        self.extra = extra or {}

    def complete(self, system, user, *, stage, max_tokens=None):
        msgs = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": user}]
        req_body = {"model": self.model, "messages": msgs, "temperature": self.temperature,
                    **self.extra}
        if max_tokens or self.max_tokens:
            req_body["max_tokens"] = max_tokens or self.max_tokens
        body = json.dumps(req_body).encode()
        headers = {"content-type": "application/json"}
        key = os.environ.get(self.api_key_env) if self.api_key_env else None
        if key:
            headers["authorization"] = f"Bearer {key}"
        req = urllib.request.Request(self.base_url + "/v1/chat/completions",
                                     data=body, headers=headers)
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    out = json.load(r)
                break
            except urllib.error.HTTPError as e:   # 4xx is the request's fault: no retry
                if e.code < 500 or attempt == self.retries:
                    raise
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                if attempt == self.retries:
                    raise
            time.sleep(30 * (attempt + 1))
        choice = out["choices"][0]
        return Completion(text=choice["message"]["content"] or "",
                          model=out.get("model", self.model),
                          stop_reason=choice.get("finish_reason"),
                          usage=out.get("usage") or {})


class FileQueueBackend:
    """Requests out, answers in, as files in `queue_dir`:

      <id>.request.json   {id, role, stage, model, effort, system, user, created_at}
      <id>.response.md    the answer text, exactly as the model wrote it
      <id>.meta.json      optional: who answered (model served, session, cost, ...)

    `id` hashes (role, stage, system, user), so re-running a stage maps the same
    prompt to the same file — answering is idempotent and order-free."""
    kind = "queue"

    def __init__(self, queue_dir: str, role: str, model: str, effort: str | None = None):
        self.dir, self.role, self.model, self.effort = queue_dir, role, model, effort
        os.makedirs(queue_dir, exist_ok=True)

    def request_id(self, stage: str, system: str | None, user: str) -> str:
        return hashlib.sha256(canonical([self.role, stage, system, user]).encode()).hexdigest()[:16]

    def complete(self, system, user, *, stage, max_tokens=None):
        rid = self.request_id(stage, system, user)
        base = os.path.join(self.dir, rid)
        if os.path.exists(base + ".response.md"):
            with open(base + ".response.md") as f:
                text = f.read()
            meta = {}
            if os.path.exists(base + ".meta.json"):
                with open(base + ".meta.json") as f:
                    meta = json.load(f)
            return Completion(text=text,
                              model=meta.get("model_served") or "unrecorded (agent-written)",
                              stop_reason=meta.get("stop_reason", "end_turn"),
                              usage=meta.get("usage") or {},
                              meta={"request_id": rid, "via": "queue",
                                    **{k: v for k, v in meta.items()
                                       if k not in ("model_served", "stop_reason", "usage")}})
        new = not os.path.exists(base + ".request.json")
        if new:
            with open(base + ".request.json", "w") as f:
                json.dump({"id": rid, "role": self.role, "stage": stage, "model": self.model,
                           "effort": self.effort, "system": system, "user": user,
                           "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
                          f, indent=1, ensure_ascii=False)
        raise PendingResponse(rid, base + ".request.json", new)


QUEUE_README = """# Request queue

Each `<id>.request.json` is one model call the essay pipeline is waiting on.
To answer one, write `<id>.response.md` containing only the reply.

- Answer every request in a fresh context: use only its `system` and `user`
  fields. Never read other requests, responses, or files in this repo — the
  writer and objector must not see each other's work.
- Write nothing else into the response file (no preamble, no notes).
- Optionally write `<id>.meta.json` with `model_served`, `session_id`, etc.

`python -m essay answer` does all of this by running Claude Code headless,
one session per request, with no tools.
"""


class StubBackend:
    kind = "stub"

    def __init__(self, fn: Callable[[str, str | None, str], str], model: str = "stub"):
        self.fn, self.model = fn, model

    def complete(self, system, user, *, stage, max_tokens=None):
        return Completion(text=self.fn(stage, system, user), model=self.model,
                          stop_reason="end_turn")


def call(log: RunLog, backend: Backend, *, role: str, stage: str, user: str,
         system: str | None = None, candidate: str | None = None,
         max_tokens: int | None = None, allow_truncated: bool = False) -> str:
    """`allow_truncated`: for answers read from their opening (the critic's
    verdict); the truncation is still logged via stop_reason."""
    rec = dict(role=role, stage=stage, candidate=candidate, backend=backend.kind,
               model_requested=backend.model, system=system, user=user)
    t0 = time.time()
    try:
        c = backend.complete(system, user, stage=stage, max_tokens=max_tokens)
    except PendingResponse as p:
        if p.new:
            log.append("request", **rec, request_id=p.request_id)
        raise
    except Exception as e:  # noqa: BLE001 — log every failure, then re-raise
        log.append("call", **rec, error=repr(e), latency_ms=round((time.time() - t0) * 1000))
        raise
    qid = c.meta.get("request_id")
    already = qid and any(r["kind"] == "call" and (r.get("meta") or {}).get("request_id") == qid
                          for r in log.records())
    if not already:   # a queued answer re-read on resume is logged once
        log.append("call", **rec, model_served=c.model, response=c.text,
                   stop_reason=c.stop_reason, usage=c.usage, request_id=c.request_id,
                   latency_ms=round((time.time() - t0) * 1000), meta=c.meta)
    if c.stop_reason == "refusal":
        raise RefusalError(f"{role}/{stage}: refused ({c.meta.get('stop_details')})")
    if c.stop_reason in ("max_tokens", "length") and not allow_truncated:
        raise TruncatedError(f"{role}/{stage}: hit max_tokens")
    return c.text


class MyvectRetriever:
    """myvect `/api/search` over the given boxes. Hits: {box, text, score, metadata}.
    The first query after a cold start loads the embedding model (>15 s seen)."""

    def __init__(self, base_url: str, boxes: list[str], timeout: int = 60):
        self.base_url, self.boxes, self.timeout = base_url.rstrip("/"), boxes, timeout

    def search(self, query: str, k: int = 3) -> list[dict]:
        body = json.dumps({"query": query, "boxes": self.boxes, "k": k}).encode()
        req = urllib.request.Request(self.base_url + "/api/search", data=body,
                                     headers={"content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.load(r).get("hits", [])
