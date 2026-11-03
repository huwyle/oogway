# Feynman mastery workspace (OpenCode)

A folder of markdown where **you write the understanding and the agent only
critiques it**. Everything is plain files + git, so you can read it in any
editor (Obsidian, VS Code) while OpenCode runs in a terminal on the same folder.

Requires: OpenCode, Python 3.8+ (standard library only), git.

## Setup

```bash
cd mastery
git init && git add -A && git commit -m "scaffold"
opencode            # AGENTS.md, opencode.json and .opencode/commands/ load automatically
```

Put authoritative material (textbook chapters, papers, your lecture notes) in
`topics/<topic>/sources/`. The agent grounds its criticism there; without it, it
falls back on its own memory, which is the weakest link.

## The loop

| Step | You | Command |
|---|---|---|
| 1. Dump | write everything you know in `human/dump.md` | `/dump laplacian` creates the empty file |
| 2. Explain | write `human/explain-v1.md` from memory | `/explain laplacian` creates the next version |
| 3. Gaps | read the report, work the questions | `/gaps laplacian` (fresh context) |
| 3. Ask | ask what you need | `/ask laplacian why does the sign flip?` then write your own-words restatement and `/check q-0007` |
| 4. Re-explain | write `explain-v2.md`, repeat 3 as needed | `/compare laplacian` |
| 4. Archive | rewrite `human/FINAL.md` yourself | `/final laplacian` seeds it, `/archive laplacian` gates it |
| Anytime | answer due questions | `/review [topic]` |
| Anytime | critique your own old writing | `/past laplacian` |

Commit before each agent command (`git add -A && git commit -m ...`); then
`python3 tools/audit.py` afterward confirms nothing in `human/` was modified.

## What you get

`topics/<topic>/index.md` is regenerated after every command: your artifacts, the
agent reports, and the question ledger (asked by you or by the agent) with each
question linked to the sentence of yours that prompted it, its status
(`open` → `answered` → `restated` → `solid`, or `needs-work`) and due date.
Cross-topic links you write as `[[other-topic/human/FINAL]]` are collected under
"Links out". `topics/index.md` lists all topics.

## How ownership is enforced

1. `opencode.json` denies the agent's edit tool on `topics/*/human/*`, the scripts,
   templates, commands and its own rules, and denies bash commands that mention
   `human/`.
2. Question state (IDs, status, due dates) is only changed through `tools/qa.py`,
   so the agent can't corrupt the schedule.
3. `tools/audit.py` + git catches anything that slips through.

Permission rules are pattern-matched on tool input and are not an OS sandbox. A
determined shell command could get around them, which is why step 3 exists.

## First-run test (do this once)

Start `opencode` and say: *"Append the word TEST to topics/<any>/human/dump.md."*
It should be refused. Also confirm `/dump demo` works, then delete
`topics/demo`. I verified the scripts here, but I could not run OpenCode itself,
so this is the check that the permission block loaded. If your OpenCode version
uses a different permission schema (newer docs use a `permissions` array of
`{action, resource, effect}` rules), translate the same rules and re-test.

## Caveats

- The agent can miss subtle errors and tends to agree with fluent text. Treat
  `sources/` and the application-check questions as your real test.
- Answers are stored in `qa/*.md`, so you *can* peek. The tool only prevents the
  agent from leaking them; the discipline of attempting first is yours.
- `/gaps` and `/compare` run as sub-sessions (`subtask: true`) for fresh context.
  If your OpenCode version uses `subagent: true` instead, swap the frontmatter key.
