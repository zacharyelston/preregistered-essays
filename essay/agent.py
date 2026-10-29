"""Answer queued requests with Claude Code (no API key needed: it uses whatever
`claude` is signed in as — on this machine, or on another over SSH).

One headless session per request, which is what keeps the roles honest: the
objector never shares a context with the writer, and no thesis sees another.
Each session runs in an empty temp cwd with
  --system-prompt   the request's own system prompt (replaces Claude Code's)
  --tools ""        no tools: no file reads, no web, no shell
  --strict-mcp-config, --setting-sources project
                    no MCP servers, no user settings
and, when the CLI has them (checked from its --help):
  --safe-mode       no CLAUDE.md, skills, plugins, hooks or custom agents
  --no-session-persistence   nothing saved to resume or leak into later sessions
  --effort <level>  the request's effort (older CLIs: their default, recorded)
so the model sees the request's system + user text and nothing else. What
Claude Code reports back (served model, stop reason, usage, cost, session id,
version, flags used) goes into <id>.meta.json and from there into the run log.

With `ssh=HOST`, only the request crosses: the prompt goes over stdin, the JSON
result comes back; the run dir and its log never leave this machine.
"""
from __future__ import annotations

import glob
import json
import os
import shlex
import subprocess
import tempfile
import time

OPTIONAL_FLAGS = ("--safe-mode", "--no-session-persistence", "--effort")


class AnswerError(RuntimeError):
    pass


def pending(queue_dir: str, role: str | None = None) -> list[str]:
    out = []
    for req in sorted(glob.glob(os.path.join(queue_dir, "*.request.json"))):
        if os.path.exists(req.replace(".request.json", ".response.md")):
            continue
        if role:
            with open(req) as f:
                if json.load(f).get("role") != role:
                    continue
        out.append(req)
    return out


class ClaudeCLI:
    def __init__(self, claude_bin: str = "claude", ssh: str | None = None,
                 timeout: int = 1800):
        self.bin, self.ssh, self.timeout = claude_bin, ssh, timeout
        self._version = self._flags = None

    def remote_command(self, args: list[str]) -> str:
        return 'cd "$(mktemp -d)" && ' + " ".join(shlex.quote(a) for a in [self.bin, *args])

    # One multiplexed connection per host for every request (a new TCP connection per
    # request tripped the host's SSH rate limit), and patience when ssh itself fails
    # (exit 255: connection refused / timed out), so a temporary block pauses a run
    # instead of ending it. Backoff 1, 2, 4, 8, 15 min: about half an hour in total.
    SSH_OPTS = ["-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
                "-o", "ControlMaster=auto", "-o", "ControlPath=~/.ssh/hb-cm-%C",
                "-o", "ControlPersist=15m", "-o", "ServerAliveInterval=30"]
    SSH_BACKOFF = (60, 120, 240, 480, 900)

    def run(self, args: list[str], stdin: str | None = None,
            timeout: int | None = None) -> subprocess.CompletedProcess:
        timeout = timeout or self.timeout
        if self.ssh:
            for wait in (*self.SSH_BACKOFF, None):
                p = subprocess.run(["ssh", *self.SSH_OPTS, self.ssh, self.remote_command(args)],
                                   input=stdin, capture_output=True, text=True,
                                   timeout=timeout)
                if p.returncode != 255 or wait is None:
                    return p
                time.sleep(wait)
        with tempfile.TemporaryDirectory(prefix="hb-answer-") as cwd:
            return subprocess.run([self.bin, *args], input=stdin, capture_output=True,
                                  text=True, cwd=cwd, timeout=timeout)

    @property
    def version(self) -> str | None:
        if self._version is None:
            try:
                self._version = self.run(["--version"], timeout=60).stdout.strip() or ""
            except (OSError, subprocess.SubprocessError):
                self._version = ""
        return self._version or None

    @property
    def flags(self) -> set[str]:
        if self._flags is None:
            try:
                help_text = self.run(["--help"], timeout=60).stdout
            except (OSError, subprocess.SubprocessError):
                help_text = ""
            self._flags = {f for f in OPTIONAL_FLAGS if f in help_text}
        return self._flags


def answer_one(req_path: str, cli: ClaudeCLI) -> dict:
    with open(req_path) as f:
        req = json.load(f)
    args = ["-p", "--output-format", "json", "--tools", "", "--strict-mcp-config",
            "--setting-sources", "project", "--model", req["model"]]
    args += [f for f in ("--safe-mode", "--no-session-persistence") if f in cli.flags]
    effort = req.get("effort") if "--effort" in cli.flags else None
    if effort:
        args += ["--effort", effort]
    if req.get("system"):
        args += ["--system-prompt", req["system"]]
    p = cli.run(args, stdin=req["user"])
    try:
        out = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise AnswerError(f"{req['id']}: claude exited {p.returncode}: "
                          f"{(p.stderr or p.stdout).strip()[:300]}") from None
    if p.returncode or out.get("is_error") or out.get("subtype") != "success":
        raise AnswerError(f"{req['id']}: {out.get('subtype')}: {str(out.get('result'))[:300]}")
    meta = {
        "answered_by": "claude-code -p" + (f" via ssh {cli.ssh}" if cli.ssh else ""),
        "claude_code_version": cli.version,
        "flags": [a for a in args if a.startswith("--") and a != "--system-prompt"],
        "effort": effort,
        "model_requested": req["model"],
        "model_served": ", ".join(sorted(out.get("modelUsage") or {})) or None,
        "stop_reason": out.get("stop_reason") or "end_turn",
        "usage": out.get("usage") or {},
        "cost_usd": out.get("total_cost_usd"),
        "session_id": out.get("session_id"),
        "duration_ms": out.get("duration_ms"),
        "num_turns": out.get("num_turns"),
    }
    base = req_path[: -len(".request.json")]
    with open(base + ".meta.json", "w") as f:
        json.dump(meta, f, indent=1)
    with open(base + ".response.md", "w") as f:   # last: its existence means "answered"
        f.write(out.get("result") or "")
    return meta
