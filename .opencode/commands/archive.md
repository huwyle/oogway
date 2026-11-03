---
description: Step 4 - gate and archive a finished topic (blocks while ERROR findings remain open)
---
Topic: $ARGUMENTS

Run `python3 tools/archive.py $ARGUMENTS` with the bash tool and report its output faithfully. If it refuses, list each reason and what command or action fixes it (`/compare`, edit FINAL.md, etc.). Never pass `--force`; tell the user they may run it themselves in a terminal if they truly want to override. If it succeeds, mention the git tag (if any) and any unresolved questions that remain in their review queue.
