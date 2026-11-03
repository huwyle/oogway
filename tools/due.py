#!/usr/bin/env python3
"""List questions due for review today (question text only, never answers)."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("topic", nargs="?")
    ap.add_argument("-n", type=int, default=5, help="max questions to list (default 5)")
    a = ap.parse_args()
    paths = sorted((topic_dir(a.topic) / "qa").glob("q-*.md")) if a.topic else all_qa()
    due = []
    for p in paths:
        meta, body = read_fm(p)
        if str(meta.get("due", "9999")) <= str(today()):
            due.append((str(meta["due"]), meta["id"], meta["topic"], meta["status"], get_section(body, "Question")))
    due.sort()
    if not due:
        print("Nothing due today.")
        return
    print(f"{len(due)} due; showing {min(a.n, len(due))}:")
    for d, qid, topic, status, q in due[: a.n]:
        print(f"- {qid} [{topic}] ({status}, due {d}): {first_line(q, 200)}")


if __name__ == "__main__":
    main()
