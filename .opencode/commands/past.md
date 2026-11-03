---
description: Growth-spotting - critique a passage from your own older writing (usage - /past <topic>)
---
Topic: $ARGUMENTS

1. Run `python3 tools/past.py $ARGUMENTS`. Show the user the passage and its file, with no commentary, no hints, and no mention of what is right or wrong in it.
2. Ask: "Knowing what you know now, what is wrong, missing, or hand-waved here?" Then stop and wait.
3. After they answer, read the matching `llm/gaps-v*.md` and `qa/` files for findings that quote this passage, and show what the original diagnosis said. Say what they caught, what they missed, and whether they now see something that the diagnosis missed too.
4. If they found a new problem worth tracking, offer to log it with `python3 tools/qa.py new <topic> --by me --source <file> --quote "<sentence>" --question "<their question>"`.
