---
description: Spaced retrieval - answer questions that are due (usage - /review [topic])
---
Topic filter (may be empty): $ARGUMENTS

1. Run `python3 tools/due.py $ARGUMENTS`. If nothing is due, say so and stop.
2. Take the questions one at a time. For each: run `python3 tools/qa.py show <id>` and present ONLY the question (and the quoted sentence from the user's writing if present). Do not read or reveal the stored answer yet. Then stop and wait for the user to answer from memory.
3. When the user answers, read the stored answer and `sources/`, and judge substance, not wording. Then run `python3 tools/qa.py grade <id> pass|fail --attempt "<the user's answer, verbatim>"`.
4. Give feedback: what was right, what was missing. If it was a fail, now show the key point of the stored answer and say the question will return tomorrow. If it was a pass, say when it will return (from the tool output).
5. Ask whether to continue with the next due question.
