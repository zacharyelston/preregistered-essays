"""Can Phi-4 serve as the writer? One full `draft` plus `extract_steps` on it (that
prompt carries the whole essay, so it checks the 16k context), through the
pipeline's own stages and backend. The thesis is a fixed placeholder, not an entry.
Writes only a scratch log (default runs/small-writer-check.jsonl).

    .venv/bin/python labs/small_writer_check.py \
        --url http://localhost:8001/api/v1/namespaces/<namespace>/services/<hat-server>:8000/proxy
"""
import argparse
import time

from essay import stages as S
from essay.log import RunLog
from essay.pipeline import _llm

THESIS = {"id": "check", "thesis": "Omissions can be causes.",
          "argument_sketch": "A placeholder thesis to test long-form generation only."}
OBJECTION = {"objection": "If omissions are causes, there are too many causes."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--model", default="phi-4")
    ap.add_argument("--log", default="runs/small-writer-check.jsonl")
    ap.add_argument("--target", type=int, help="ask for about this many words")
    a = ap.parse_args()
    log = RunLog(a.log)
    w = _llm({"kind": "openai-compat", "url": a.url, "model": a.model,
              "temperature": 0.7}, "/nonexistent", "writer")
    t0 = time.time()
    essay = S.draft(log, w, THESIS, OBJECTION, 6000, target_words=a.target)
    rec = log.records()[-1]
    print(f"draft: {S.word_count(essay)} words, stop={rec['stop_reason']}, "
          f"usage={rec['usage']}, {time.time() - t0:.0f}s")
    print("head:", essay[:300].replace("\n", " "))
    print("refs section:", "## References" in essay)
    t0 = time.time()
    steps = S.extract_steps(log, w, essay, "check")
    print(f"steps: {len(steps)} in {time.time() - t0:.0f}s; first: {steps[:1]}")
    print(f"log: {log.verify()[1]}")


if __name__ == "__main__":
    main()
