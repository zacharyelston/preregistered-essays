"""Can the served model do the simple things the pipeline needs, reliably? Each probe
runs N times at each temperature through the pipeline's own backend and JSON
parser; prints pass rates and the first failure verbatim. No log, no state.

    .venv/bin/python labs/phi_simple_tasks.py --url <vLLM base URL> [--model phi-4] [-n 3]
"""
import argparse
import json
import re
import time

from essay import stages as S
from essay.backends import OpenAICompatBackend

LEAKS = re.compile(r"<\|(?:im_end|im_start|im_sep|end|endoftext|assistant|user)\|>")


def is_json(kind, keys=()):
    def check(text):
        v = S.extract_json(text)
        if not isinstance(v, kind):
            return f"wanted {kind.__name__}, got {type(v).__name__}"
        if kind is dict and set(keys) - set(v):
            return f"missing keys {sorted(set(keys) - set(v))}"
        return None
    return check


PROBES = [
    ("one word", None, "Reply with exactly the word YES and nothing else.",
     lambda t: None if t.strip().strip(".").upper() == "YES" else "not exactly YES"),
    ("arithmetic", None, "What is 17 times 3? Reply with the number only.",
     lambda t: None if re.fullmatch(r"\s*51\.?\s*", t) else "not 51"),
    ("system prompt", "Always answer in French.", "What colour is the sky on a clear day? One sentence.",
     lambda t: None if re.search(r"\bbleu", t, re.I) else "not French"),
    ("json list", None, "List three prime numbers as a JSON array of integers. JSON only.",
     is_json(list)),
    ("json object", S.OBJECTOR_SYSTEM,
     "Thesis: Lying is always wrong.\n\nGive the single strongest objection to this thesis. "
     "Then rate how damaging it is if unanswered, 1 (minor) to 5 (fatal). Reply with a JSON "
     "object: {\"objection\": str, \"severity\": int, \"rationale\": str}.",
     is_json(dict, ("objection", "severity", "rationale"))),
    ("json list of steps", S.WRITER_SYSTEM,
     "Essay:\n\nAll humans are mortal. Socrates is human. So Socrates is mortal. Mortal beings "
     "fear death, so Socrates fears death.\n\nList the essay's main inferential steps, at most "
     "5. Restate each as a short self-contained argument: its premises, then 'Therefore, ...'. "
     "Reply with a JSON array of strings.", is_json(list)),
]


def run(be, system, user, check):
    t0 = time.time()
    c = be.complete(system, user, stage="probe")
    text = c.text
    why = None
    if LEAKS.search(text):
        why = f"template token leaked: {LEAKS.search(text).group(0)}"
    elif c.stop_reason not in ("stop", "end_turn"):
        why = f"stop_reason={c.stop_reason}"
    else:
        try:
            why = check(text)
        except ValueError as e:
            why = f"unparseable: {e}"
    return why, text, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--model", default="phi-4")
    ap.add_argument("-n", type=int, default=3)
    ap.add_argument("--key-env", help="env var holding the endpoint's API key")
    a = ap.parse_args()
    total = fails = 0
    for temp in (0.7, 0.0):
        be = OpenAICompatBackend(a.url, a.model, api_key_env=a.key_env, max_tokens=600,
                                 temperature=temp, timeout=300)
        print(f"\n== {a.model} @ temperature {temp}")
        for name, system, user, check in PROBES:
            results = [run(be, system, user, check) for _ in range(a.n)]
            bad = [(w, t) for w, t, _ in results if w]
            total += len(results); fails += len(bad)
            secs = sum(s for *_, s in results) / len(results)
            print(f"  {name:<20} {len(results) - len(bad)}/{len(results)} ok  ({secs:.1f}s avg)")
            if bad:
                print(f"     first failure: {bad[0][0]}\n     reply: {bad[0][1][:400]!r}")
    print(f"\n{total - fails}/{total} probes passed")


if __name__ == "__main__":
    main()
