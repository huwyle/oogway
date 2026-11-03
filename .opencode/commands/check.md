---
description: Step 3 - check your own-words restatement of a question (usage - /check q-0007)
---
Question id: $ARGUMENTS

1. Read `qa/` file for this id (find it with `python3 tools/qa.py list`), the stored "Answer (agent)", the relevant `sources/`, and the user's restatement at `topics/<topic>/human/restatements/<id>.md`. If the restatement is only the template, stop and tell the user to write it first.
2. Judge the restatement against the stored answer and sources for substance, not wording. Identify: what is correct, what is wrong, what is missing.
3. Record the verdict with `python3 tools/qa.py restated <id> --verdict ok|needs-work --note "<one-line reason>"`. Use `ok` only if the core idea is correct and the restatement is genuinely in their own words and not a paraphrase of your answer's wording.
4. Report to the user: a short list of what is right, and for anything wrong or missing, ask a pointed hint question rather than giving the corrected text. If `needs-work`, tell them to edit the restatement and run `/check` again. Never edit the restatement.
