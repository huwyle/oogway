#!/usr/bin/env python3
"""Check that nothing in human/ was modified or deleted since the last commit.

Workflow: commit your own writing BEFORE running an agent command. Afterwards,
run this. New untracked stubs are expected; modified/deleted tracked files are
not, and mean something other than you touched your writing.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT  # noqa: E402


def main():
    r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("not a git repository; run `git init` and commit first")
    bad = []
    for line in r.stdout.splitlines():
        code, path = line[:2], line[3:]
        if "/human/" in path and code != "??":
            bad.append(line)
    if bad:
        print("WARNING: tracked files in human/ changed since last commit:")
        print("\n".join(bad))
        print("If you did not make these edits yourself, restore with: git checkout -- topics/*/human")
        sys.exit(1)
    print("OK: no tracked file in human/ was modified or deleted.")


if __name__ == "__main__":
    main()
