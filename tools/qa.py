#!/usr/bin/env python3
"""Question ledger: IDs, status and spaced-review dates, deterministically."""
import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F403
import index  # noqa: E402


def _save(path, meta, body):
    write_fm(path, meta, body)
    index.regen()


def _attempt(body, line):
    return set_section(body, "Attempts", line, append=True)


def cmd_new(a):
    d = topic_dir(a.topic)
    (d / "qa").mkdir(exist_ok=True)
    nums = [num(p) for p in all_qa()]
    qid = f"q-{max(nums, default=0) + 1:04d}"
    meta = {
        "id": qid,
        "topic": d.name,
        "asked_by": a.by,
        "source": a.source or "",
        "quote": a.quote or "",
        "status": "answered" if (a.by == "me" and a.answer) else "open",
        "due": str(today()),
        "interval_days": 1,
    }
    body = f"## Question\n\n{a.question.strip()}\n\n## Answer (agent)\n\n{(a.answer or '_(none yet)_').strip()}\n\n## Attempts\n\n"
    p = d / "qa" / f"{qid}.md"
    _save(p, meta, body)
    print(f"{qid} {p.relative_to(ROOT)}")


def cmd_answer(a):
    p = find_qa(a.qid)
    meta, body = read_fm(p)
    body = set_section(body, "Answer (agent)", a.text)
    if meta.get("status") == "open" and meta.get("asked_by") == "me":
        meta["status"] = "answered"
    _save(p, meta, body)
    print(f"{meta['id']} answer updated")


def cmd_restated(a):
    p = find_qa(a.qid)
    meta, body = read_fm(p)
    r = p.parent.parent / "human" / "restatements" / f"{meta['id']}.md"
    if not r.exists() or words(r.read_text(encoding="utf-8")) < 15:
        sys.exit(f"error: no real restatement at {r.relative_to(ROOT)} yet (need at least ~15 words of your own text)")
    if a.verdict == "ok":
        meta.update(status="restated", interval_days=1, due=str(today() + datetime.timedelta(days=1)))
    else:
        meta.update(status="needs-work", interval_days=1, due=str(today()))
    body = _attempt(body, f"- {today()} CHECK {a.verdict}: {a.note or ''}".rstrip())
    _save(p, meta, body)
    print(f"{meta['id']} -> {meta['status']} (due {meta['due']})")


def cmd_grade(a):
    p = find_qa(a.qid)
    meta, body = read_fm(p)
    quoted = "\n".join("  > " + l for l in a.attempt.strip().splitlines())
    if a.result == "pass":
        new = max(2, int(meta.get("interval_days", 1)) * 2)
        meta.update(interval_days=new, due=str(today() + datetime.timedelta(days=new)), status="solid" if new >= 8 else "restated")
    else:
        meta.update(interval_days=1, due=str(today() + datetime.timedelta(days=1)), status="needs-work")
    body = _attempt(body, f"- {today()} {a.result.upper()} (from memory)\n{quoted}")
    _save(p, meta, body)
    print(f"{meta['id']} -> {meta['status']} (next review {meta['due']}, interval {meta['interval_days']}d)")


def cmd_list(a):
    paths = sorted((topic_dir(a.topic) / "qa").glob("q-*.md")) if a.topic else all_qa()
    for p in paths:
        meta, body = read_fm(p)
        print(f"{meta['id']} | {meta['topic']} | {meta['asked_by']} | {meta['status']} | due {meta['due']} | {first_line(get_section(body, 'Question'))}")


def cmd_show(a):
    p = find_qa(a.qid)
    meta, body = read_fm(p)
    print(f"{meta['id']} [{meta['topic']}] status={meta['status']}")
    if meta.get("quote"):
        print(f'From your writing: "{meta["quote"]}"')
    print()
    print(get_section(body, "Question"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("topic")
    n.add_argument("--by", choices=["llm", "me"], required=True)
    n.add_argument("--question", required=True)
    n.add_argument("--source", default="")
    n.add_argument("--quote", default="")
    n.add_argument("--answer", default="")
    n.set_defaults(f=cmd_new)
    s = sub.add_parser("answer")
    s.add_argument("qid")
    s.add_argument("--text", required=True)
    s.set_defaults(f=cmd_answer)
    s = sub.add_parser("restated")
    s.add_argument("qid")
    s.add_argument("--verdict", choices=["ok", "needs-work"], required=True)
    s.add_argument("--note", default="")
    s.set_defaults(f=cmd_restated)
    s = sub.add_parser("grade")
    s.add_argument("qid")
    s.add_argument("result", choices=["pass", "fail"])
    s.add_argument("--attempt", required=True)
    s.set_defaults(f=cmd_grade)
    s = sub.add_parser("list")
    s.add_argument("topic", nargs="?")
    s.set_defaults(f=cmd_list)
    s = sub.add_parser("show")
    s.add_argument("qid")
    s.set_defaults(f=cmd_show)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
