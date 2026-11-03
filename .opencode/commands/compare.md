---
description: Step 4 - compare your latest explanation with the previous one and the gap report (critique only, no rewrite)
subtask: true
---
Topic: $ARGUMENTS

1. Read the two highest-numbered `human/explain-v*.md` files (vN and v(N-1)), the latest `llm/gaps-v*.md` and any earlier `llm/compare-v*.md`, and `sources/`. If there is only one explanation, stop and say there is nothing to compare yet.
2. For each earlier finding (g-ids), decide: `closed` (now correct and well explained), `open` (still wrong or missing), or `regressed` (was fine, now broken). Cite the user's exact new wording as evidence. Also list any NEW errors or gaps with new g-ids continuing the numbering, and create a ledger question for each via `python3 tools/qa.py new $ARGUMENTS --by llm --source human/explain-vN.md --quote "<exact sentence>" --question "..." --answer "..."`.
3. Write `topics/$ARGUMENTS/llm/compare-vN.md` containing a table (id, tag, status, evidence quote, one-line note) and, on their own lines at the end, exactly these two machine-readable lines:

```
OPEN_ERRORS: <number of findings tagged ERROR that are open or regressed>
OPEN_GAPS: <number of GAP/HANDWAVE/JARGON findings that are open or regressed>
```

4. Run `python3 tools/index.py`. Report in three sentences: how many closed, how many remain, and the single most important remaining item by title. Do not rewrite or suggest replacement text for their explanation.
