"""Pre-submission checks on the essays: word count (bibliography excluded, the
contest's rule), instruction-like text aimed at an AI screener (prompt injection
means disqualification), hidden markup or invisible characters, and self-disclosure
of AI authorship (judging is blind to method). Prints each hit with context.

    .venv/bin/python labs/submission/check_essays.py submission/<dir>/entry-*/essay.md
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("/labs/", 1)[0])
from essay.stages import word_count  # noqa: E402

INJECTION = [r"(?i)ignore (all |any |the )?(previous|prior|above) (instructions|prompts)",
             r"(?i)\b(system|developer) prompt\b", r"(?i)\byou are (an? )?(ai|assistant|grader|judge|reviewer)\b",
             r"(?i)\b(grader|screener|evaluator|reviewer)s?\b.{0,40}\b(should|must|rate|score)\b",
             r"(?i)\brate this (essay|paper)\b", r"(?i)\bscore (this|it) (highly|as)\b",
             r"(?i)\bas an? (ai|language model)\b", r"(?i)\bI am (an? )?(ai|language model|claude|qwen)\b",
             r"(?i)\b(this|the present) (essay|paper) (was|is) (written|generated|produced) by\b"]
HIDDEN = [(r"<!--", "HTML comment"), (r"<[a-zA-Z/][^>]*>", "HTML tag"),
          (r"[​-‏⁠-⁤﻿]", "invisible character"),
          (r"\\color|\\textcolor|font-size:\s*0", "styling that could hide text")]


def ctx(text, m, width=90):
    s, e = max(0, m.start() - width), min(len(text), m.end() + width)
    return text[s:e].replace("\n", " ")


def main():
    bad = False
    for path in sys.argv[1:]:
        text = open(path, encoding="utf-8").read()
        wc = word_count(text)
        print(f"== {path}: {wc} words before the references "
              f"({'OK' if wc <= 6000 else 'OVER THE 6,000 LIMIT'})")
        bad |= wc > 6000
        for pat in INJECTION:
            for m in re.finditer(pat, text):
                print(f"   instruction-like? {m.group(0)!r}: ...{ctx(text, m)}...")
        for pat, label in HIDDEN:
            for m in re.finditer(pat, text):
                bad = True
                print(f"   HIDDEN ({label}) at {m.start()}: {m.group(0)!r}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
