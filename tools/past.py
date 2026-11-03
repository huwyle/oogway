#!/usr/bin/env python3
"""Pick a random passage from one of your OLDER writings for self-review."""
import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403


def paragraphs(path):
    text = strip_comments(path.read_text(encoding="utf-8"))
    paras = [p.strip() for p in text.split("\n\n")]
    return [(i, p) for i, p in enumerate(paras, 1) if len(p) >= 80 and not p.startswith("#") and not p.startswith("Audience:")]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("topic")
    a = ap.parse_args()
    d = topic_dir(a.topic)
    h = d / "human"
    pool = []
    ex = versions(h, "explain")
    older = ex[:-1] if len(ex) > 1 else ex
    for p in ([h / "dump.md"] if (h / "dump.md").exists() else []) + older:
        pool += [(p, i, t) for i, t in paragraphs(p)]
    if not pool:
        sys.exit("No older passages yet. Write a dump or an explanation first.")
    p, i, t = random.choice(pool)
    print(f"FILE: {p.relative_to(ROOT)}  PARAGRAPH: {i}")
    print("---")
    print(t)


if __name__ == "__main__":
    main()
