---
description: Step 3 - diagnose your latest explanation (fresh context): errors, gaps, handwaves, jargon, application checks
subtask: true
---
Topic: $ARGUMENTS

Follow the "Diagnosing an explanation" section of AGENTS.md exactly.

1. List `topics/$ARGUMENTS/human/` and find the highest-numbered `explain-vN.md`. Read it, plus `human/dump.md` and everything in `sources/`. Read nothing else from `llm/` or `qa/`, except the output of `python3 tools/qa.py list $ARGUMENTS`, which you use only to avoid duplicate questions.
2. For every finding and application check, create a ledger question with `python3 tools/qa.py new $ARGUMENTS --by llm --source human/explain-vN.md --quote "<exact sentence>" --question "<question>" --answer "<short, source-backed model answer>"`. Use the printed q-ids in the report.
3. Write `topics/$ARGUMENTS/llm/gaps-vN.md` in the exact format from AGENTS.md. List what is correct under "Solid". Do not put answers in the report, only questions.
4. Run `python3 tools/index.py`.

Finish with a short summary: counts per tag, the three highest-priority findings by title only, and the path of the report. Do not write in `human/`.
