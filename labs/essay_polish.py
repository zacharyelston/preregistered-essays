"""Polish a finished run's winner (essay/polish.py, rule polish-1), answering
queued frontier requests with Claude Code over SSH, as the runs do.

    .venv/bin/python labs/essay_polish.py runs/essay/<run> --ssh user@gpu-host
    .venv/bin/python labs/essay_polish.py --check-lookup     # live OpenAlex/Crossref test
"""
import argparse
import json
import os

from essay import agent
from essay.pipeline import PendingBatch
from essay.polish import POLISH_RULE, Polish, lookup, match

KNOWN = [  # real works, plus one invented, to check the lookup end to end
    {"authors": ["Kripke"], "title": "Naming and Necessity", "year": 1980},
    {"authors": ["Parfit"], "title": "Reasons and Persons", "year": 1984},
    {"authors": ["Schwitzgebel"], "title": "The Unreliability of Naive Introspection",
     "year": 2008},
    {"authors": ["Nobody"], "title": "A Treatise on Imaginary Promissory Engines", "year": 2031},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", nargs="?")
    ap.add_argument("--ssh", metavar="USER@HOST")
    ap.add_argument("--check-lookup", action="store_true")
    ap.add_argument("--recheck", action="store_true",
                    help="re-verify the finished essay's references (essay unchanged)")
    ap.add_argument("--refs", help="with --recheck: which reference list (e.g. c0.refs)")
    ap.add_argument("--revert-citation-fix", action="store_true",
                    help="restore the ratchet's output as final (logged, with --note and --reason)")
    ap.add_argument("--valid-fix", action="store_true",
                    help="run the rule's one citation fix pass from the last valid --recheck")
    ap.add_argument("--note", help="the human decision, verbatim")
    ap.add_argument("--reason", help="why the fix is reverted")
    a = ap.parse_args()
    if a.revert_citation_fix:
        if not (a.run and a.note and a.reason):
            ap.error("--revert-citation-fix needs RUN, --note and --reason")
        print(json.dumps(Polish(a.run).revert_citation_fix(a.note, a.reason), indent=1))
        return
    if a.recheck:
        res = Polish(a.run).recheck(a.refs)
        print(json.dumps({k: v for k, v in res.items() if k != "unverified"}, indent=1))
        for r in res["unverified"]:
            print(f"   unverified: {', '.join(r['authors'][:2])} ({r['year']}) {r['title'][:90]}")
        return
    if a.check_lookup:
        for ref in KNOWN:
            m = match(ref, lookup(ref), POLISH_RULE)
            c = m["candidate"] or {}
            print(f"{'OK ' if m['verified'] else 'NO '} {ref['title'][:50]:<50} ratio {m['ratio']}"
                  f"  -> {c.get('source')}: {str(c.get('title'))[:50]} ({c.get('year')})")
        return
    if not (a.run and a.ssh):
        ap.error("give RUN and --ssh (or --check-lookup)")
    p = Polish(a.run) if os.path.isdir(os.path.join(a.run, "polish")) else Polish.create(a.run)
    cli = agent.ClaudeCLI(ssh=a.ssh)
    print(f"polishing {a.run} (claude {cli.version} on {a.ssh})", flush=True)
    while True:
        try:
            if a.valid_fix:
                res = p.valid_fix()
                print("[valid-fix] done")
                print(json.dumps({k: v for k, v in res.items()
                                  if k not in ("from_sha256", "to_sha256")}, indent=1))
                return
            s = p.run()
            break
        except PendingBatch as e:
            todo = agent.pending(os.path.join(p.dir, "queue"))
            print(f"[polish] {e.n} pending -> answering {len(todo)}", flush=True)
            for req in todo:
                meta = agent.answer_one(req, cli)
                print(f"   {os.path.basename(req)[:16]} {meta['model_served']} "
                      f"{meta['stop_reason']} {meta['duration_ms']}ms ${meta['cost_usd']}",
                      flush=True)
    print("[polish] done")
    print(json.dumps({k: s[k] for k in ("rounds", "words")} |
                     {"citations": {k: {kk: v[kk] for kk in ("references", "unverified")}
                                    for k, v in s["citations"].items()}}, indent=1))


if __name__ == "__main__":
    main()
