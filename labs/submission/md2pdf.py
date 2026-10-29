"""Markdown -> HTML -> PDF (headless Chrome), for the features the essays and report
use: ATX headings, paragraphs, nested bullet / numbered lists, blockquotes, pipe
tables, horizontal rules, and inline bold, italic, code and links. Standard library
plus a local Chrome; no downloads.

    .venv/bin/python labs/submission/md2pdf.py FILE.md [...]   # writes FILE.pdf beside it
"""
import html
import os
import re
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CSS = """
@page { size: A4; margin: 2.4cm 2.3cm; }
body { font-family: "Times New Roman", "STIX Two Text", Georgia, serif; font-size: 11.5pt;
       line-height: 1.45; color: #111; }
h1 { font-size: 17pt; line-height: 1.25; margin: 0 0 0.9em; }
h2 { font-size: 13.5pt; margin: 1.4em 0 0.5em; }
h3 { font-size: 12pt; margin: 1.2em 0 0.4em; }
h4, h5, h6 { font-size: 11.5pt; margin: 1em 0 0.3em; }
p { margin: 0 0 0.75em; text-align: justify; hyphens: auto; }
ul, ol { margin: 0 0 0.75em 1.4em; padding: 0; }
li { margin: 0.15em 0; }
blockquote { margin: 0.6em 1.5em; color: #333; font-style: italic; }
blockquote p { text-align: left; }
blockquote code { font-style: normal; }
table { border-collapse: collapse; margin: 0.6em 0 1em; font-size: 10pt; width: 100%; }
th, td { border: 0.5pt solid #999; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #f0f0f0; }
code { font-family: Menlo, monospace; font-size: 9.5pt; }
hr { border: 0; border-top: 0.5pt solid #999; margin: 1.2em 0; }
a { color: #111; text-decoration: none; }
"""


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return s


LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def convert(md: str) -> str:
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if m := re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line):
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
        elif re.match(r"^\s*(---|\*\*\*|___)\s*$", line):
            out.append("<hr>")
            i += 1
        elif line.lstrip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + convert("\n".join(buf)) + "</blockquote>")
        elif line.lstrip().startswith("|") and i + 1 < len(lines) and \
                re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
            head = cells(line)
            rows = []
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + \
                "</tr></thead><tbody>"
            for r in rows:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table>")
        elif LIST.match(line):
            stack, items = [], []          # (indent, tag) of open lists
            while i < len(lines) and (LIST.match(lines[i]) or
                                      (lines[i].startswith("  ") and lines[i].strip() and stack)):
                m = LIST.match(lines[i])
                if not m:                   # continuation of the previous item
                    items[-1] += " " + lines[i].strip()
                    out[-1] = out[-1][:-5] + " " + inline(lines[i].strip()) + "</li>"
                    i += 1
                    continue
                ind, tag = len(m.group(1)), ("ol" if m.group(2)[0].isdigit() else "ul")
                while stack and ind < stack[-1][0]:
                    out.append(f"</{stack.pop()[1]}>")
                if not stack or ind > stack[-1][0]:
                    stack.append((ind, tag))
                    out.append(f"<{tag}>")
                items.append(m.group(3))
                out.append(f"<li>{inline(m.group(3))}</li>")
                i += 1
            while stack:
                out.append(f"</{stack.pop()[1]}>")
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not (
                    re.match(r"^#{1,6}\s", lines[i]) or LIST.match(lines[i]) or
                    lines[i].lstrip().startswith((">", "|")) or
                    re.match(r"^\s*(---|\*\*\*|___)\s*$", lines[i])):
                buf.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


def main():
    for path in sys.argv[1:]:
        md = open(path, encoding="utf-8").read()
        title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), "")
        page = (f"<!doctype html><html><head><meta charset='utf-8'><title>"
                f"{html.escape(title)}</title><style>{CSS}</style></head><body>"
                f"{convert(md)}</body></html>")
        base = os.path.splitext(os.path.abspath(path))[0]
        with open(base + ".html", "w", encoding="utf-8") as f:
            f.write(page)
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={base}.pdf", f"file://{base}.html"],
                           capture_output=True, text=True, timeout=120)
        ok = os.path.exists(base + ".pdf") and os.path.getsize(base + ".pdf") > 1000
        print(f"{'OK ' if ok else 'FAILED'} {base}.pdf {'' if ok else r.stderr[-300:]}")


if __name__ == "__main__":
    main()
