#!/usr/bin/env python3
"""Create empty human-owned stubs from templates. Never writes your content."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403
import index  # noqa: E402


def ensure_topic(topic):
    d = topic_dir(topic, must_exist=False)
    for sub in ("human/restatements", "llm", "qa", "sources"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("dump", "explain", "final"):
        sub.add_parser(name).add_argument("topic")
    sub.add_parser("restatement").add_argument("qid")
    a = ap.parse_args()

    if a.cmd == "dump":
        d = ensure_topic(a.topic)
        p = d / "human" / "dump.md"
        if p.exists():
            sys.exit(f"{p.relative_to(ROOT)} already exists; nothing changed")
        p.write_text(render("dump.md", topic=d.name), encoding="utf-8")
    elif a.cmd == "explain":
        d = ensure_topic(a.topic)
        n = max([num(p) for p in versions(d / "human", "explain")], default=0) + 1
        p = d / "human" / f"explain-v{n}.md"
        p.write_text(render("explain.md", topic=d.name, n=n), encoding="utf-8")
    elif a.cmd == "final":
        d = topic_dir(a.topic)
        ex = versions(d / "human", "explain")
        if not ex:
            sys.exit("error: no explanation versions to seed FINAL.md from")
        p = d / "human" / "FINAL.md"
        if p.exists():
            sys.exit(f"{p.relative_to(ROOT)} already exists; nothing changed")
        p.write_text(ex[-1].read_text(encoding="utf-8"), encoding="utf-8")
    elif a.cmd == "restatement":
        qa = find_qa(a.qid)
        meta, body = read_fm(qa)
        d = qa.parent.parent
        (d / "human" / "restatements").mkdir(parents=True, exist_ok=True)
        p = d / "human" / "restatements" / f"{meta['id']}.md"
        if p.exists():
            sys.exit(f"{p.relative_to(ROOT)} already exists; nothing changed")
        p.write_text(render("restatement.md", qid=meta["id"], question=" ".join(get_section(body, "Question").split())), encoding="utf-8")

    index.regen()
    print(f"created {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
