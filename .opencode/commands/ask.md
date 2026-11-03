---
description: Step 3 - ask a question (usage - /ask <topic> <question>); logged, answered briefly, restatement stub created
---
Arguments: $ARGUMENTS

The first word is the topic; the rest is the user's question. If the topic does not exist under `topics/`, ask which topic is meant and stop.

1. Answer the question in at most 6 sentences. Ground factual claims in `topics/<topic>/sources/` when relevant and name the file; if the sources don't cover it, say so and state your confidence. If the user is clearly mid-struggle, prefer a hint or a smaller question over the full answer.
2. Log it: `python3 tools/qa.py new <topic> --by me --question "<the user's question, verbatim>" --answer "<your answer>"` (add `--source`/`--quote` only if the question is about a specific passage of their writing).
3. Create the restatement stub: `python3 tools/new.py restatement <q-id printed in step 2>`.
4. End by telling the user to close this chat window's answer, write the idea in their own words in the stub file (it shows the question only, not your answer), and then run `/check <q-id>`. Do not write the restatement yourself.
