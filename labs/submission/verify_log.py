#!/usr/bin/env python3
"""Verify a hash-chained run log. Standard library only.

Each record carries `seq`, `prev` (the previous record's hash) and `hash` =
sha256(prev + canonical JSON of the record without `hash`), where canonical JSON
means sorted keys, no spaces, UTF-8 (not ASCII-escaped).

Some published records were redacted: identifying values were replaced by
placeholders like "[redacted-host]". A redacted record's own hash cannot be
recomputed, so this script reports it as REDACTED instead of failing. It still
checks that every record links to the previous record's published hash and that the
sequence is complete. Any other mismatch is a FAILURE.

The redacted records are listed in `<log>.redactions.json` beside each log. A record
that claims redaction but is not on that list is a FAILURE, so the placeholder
cannot be used to disguise an edit.

    python3 verify_log.py log.jsonl [more logs...]
"""
import hashlib
import json
import os
import sys

GENESIS = "0" * 64


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def verify(path):
    manifest = path + ".redactions.json"
    listed = set(json.load(open(manifest))["seqs"]) if os.path.exists(manifest) else set()
    prev, n, redacted, failures = GENESIS, 0, [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            n += 1
            rec = json.loads(line)
            body = {k: v for k, v in rec.items() if k != "hash"}
            if rec.get("seq") != n:
                failures.append(f"record {n}: seq {rec.get('seq')} out of order")
            if rec.get("prev") != prev:
                failures.append(f"record {n}: does not link to the previous record")
            digest = hashlib.sha256((prev + canonical(body)).encode()).hexdigest()
            if digest != rec.get("hash"):
                if "[redacted-" in line and n in listed:
                    redacted.append(n)
                elif "[redacted-" in line:
                    failures.append(f"record {n}: claims redaction but is not in {manifest}")
                else:
                    failures.append(f"record {n}: hash mismatch (content changed)")
            prev = rec.get("hash")
    return n, redacted, failures


def main():
    ok = True
    for path in sys.argv[1:]:
        n, redacted, failures = verify(path)
        status = "OK" if not failures else "FAILED"
        ok = ok and not failures
        print(f"{status}  {path}: {n} records; {n - len(redacted) - len(failures)} verified "
              f"in full; {len(redacted)} redacted (links checked); {len(failures)} failures")
        for msg in failures[:20]:
            print("   ", msg)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
