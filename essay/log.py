"""Append-only, hash-chained run log.

Each record carries `prev` (the previous record's hash) and `hash` =
sha256(prev + canonical JSON of the record body). `verify()` recomputes the chain,
so an edited, dropped or reordered record is detectable — the methodology report
can claim the log is complete and unedited and a reader can check it.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from typing import Any

GENESIS = "0" * 64


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _digest(prev: str, body: dict) -> str:
    return hashlib.sha256((prev + canonical(body)).encode()).hexdigest()


class RunLog:
    def __init__(self, path: str):
        self.path = path
        self._seq, self._last = 0, GENESIS
        self._lock = threading.Lock()
        if os.path.exists(path):
            for rec in self.records():
                self._seq, self._last = rec["seq"], rec["hash"]

    def records(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            return [json.loads(line) for line in f if line.strip()]

    def append(self, kind: str, **fields) -> dict:
        with self._lock:          # threads share one log: seq/prev must not interleave
            body = {"seq": self._seq + 1, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "kind": kind, **fields, "prev": self._last}
            rec = {**body, "hash": _digest(self._last, body)}
            with open(self.path, "a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self._seq, self._last = rec["seq"], rec["hash"]
            return rec

    def human(self, note: str, author: str = "entrant") -> dict:
        """A human intervention, verbatim. Topic choice, corrections, aborts — all of it."""
        return self.append("human", author=author, note=note)

    def verify(self) -> tuple[bool, str]:
        prev, recs = GENESIS, self.records()
        for i, rec in enumerate(recs, 1):
            body = {k: v for k, v in rec.items() if k != "hash"}
            if rec.get("seq") != i:
                return False, f"record {i}: seq {rec.get('seq')} out of order"
            if rec.get("prev") != prev:
                return False, f"record {i}: chain broken (prev mismatch)"
            if _digest(prev, body) != rec.get("hash"):
                return False, f"record {i}: hash mismatch (edited)"
            prev = rec["hash"]
        return True, f"{len(recs)} records, chain intact"
