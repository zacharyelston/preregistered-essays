"""`python -m essay <verb>`: the pipeline's command line (see essay/cli.py)."""
import argparse
import sys

from .cli import add_parser


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] != "essay":
        argv = ["essay"] + argv
    p = argparse.ArgumentParser(prog="python -m")
    add_parser(p.add_subparsers(dest="cmd", required=True))
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
