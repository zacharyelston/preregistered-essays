"""Summarize a finished polish: ratchet rounds, citation checks, cost, time, log.

    .venv/bin/python labs/essay_polish_summary.py runs/essay/<run> [...]
"""
import glob
import json
import os
import sys

from essay.log import RunLog


def main():
    for run in sys.argv[1:]:
        d = os.path.join(run, "polish")
        s = json.load(open(os.path.join(d, "summary.json")))
        print(f"== {os.path.basename(run.rstrip('/'))}")
        for r in s["rounds"]:
            print(f"   round {r['round']}: {'kept' if r['accepted'] else 'rejected'} "
                  f"({r['revised_wins']}/{r['of']}), {r['words']} words, "
                  f"{r['major_issues']} major issues")
        for tag, c in s["citations"].items():
            print(f"   check {tag}: {c['references']} refs, {c['unverified']} unverified, "
                  f"{c.get('unchecked', 'n/a')} unchecked")
            for ref in c["unverified_list"]:
                print(f"      unverified: {', '.join(ref['authors'][:2])} ({ref['year']}) "
                      f"{ref['title'][:80]}")
        if "citations_final_check" in s:
            f = s["citations_final_check"]
            print(f"   re-check of {f['of']}: {f['verified']}/{f['references']} verified, "
                  f"{f['unchecked']} unchecked, {len(f['unverified'])} unverified, "
                  f"{f['year_notes']} with edition-year notes")
            for ref in f["unverified"]:
                print(f"      unverified: {', '.join(ref['authors'][:2])} ({ref['year']}) "
                      f"{ref['title'][:80]}")
        cost = sum((json.load(open(m)).get("cost_usd") or 0)
                   for m in glob.glob(os.path.join(d, "queue", "*.meta.json")))
        log = RunLog(os.path.join(d, "log.jsonl"))
        recs = log.records()
        print(f"   final {s['words']} words | cost ${cost:.2f} | {recs[0]['ts']} -> "
              f"{recs[-1]['ts']} | log: {log.verify()[1]}")


if __name__ == "__main__":
    main()
