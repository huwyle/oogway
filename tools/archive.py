#!/usr/bin/env python3
"""Gate and record finalizing a topic. Blocks while errors remain open."""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403
import index  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("topic")
    ap.add_argument("--force", action="store_true", help="user-only: archive despite open errors")
    a = ap.parse_args()
    d = topic_dir(a.topic)
    problems = []
    final = d / "human" / "FINAL.md"
    if not final.exists() or words(final.read_text(encoding="utf-8")) < 50:
        problems.append("human/FINAL.md is missing or too short (create a seed with: python3 tools/new.py final <topic>, then rewrite it yourself)")
    cmp_ = versions(d / "llm", "compare")
    if not cmp_:
        problems.append("no comparison yet; run /compare so open errors are known")
    else:
        m = re.search(r"^OPEN_ERRORS:\s*(\d+)", cmp_[-1].read_text(encoding="utf-8"), re.M)
        n = int(m.group(1)) if m else None
        if n is None:
            problems.append(f"{cmp_[-1].name} has no OPEN_ERRORS line")
        elif n > 0:
            problems.append(f"{n} open ERROR finding(s) in {cmp_[-1].name}")
    if problems and not a.force:
        print("NOT archived:")
        for p in problems:
            print(f"- {p}")
        sys.exit(1)
    unres = []
    for p in sorted((d / "qa").glob("q-*.md")):
        meta, _ = read_fm(p)
        if meta.get("status") in ("open", "answered", "needs-work"):
            unres.append(meta["id"])
    with open(d / "log.md", "a", encoding="utf-8") as f:
        f.write(f"ARCHIVED {today()}{' (forced)' if problems else ''}\n")
    tag = f"final-{d.name}-{today()}"
    r = subprocess.run(["git", "tag", tag], cwd=ROOT, capture_output=True, text=True)
    index.regen()
    print(f"archived {d.name}" + (" (forced)" if problems else ""))
    print(f"git tag: {tag}" if r.returncode == 0 else "git tag skipped (not a git repo, no commits, or tag exists)")
    if unres:
        print(f"note: {len(unres)} question(s) still unresolved: {', '.join(unres)} (they stay in your review queue)")


if __name__ == "__main__":
    main()
