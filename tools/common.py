"""Shared helpers for the mastery tools. Standard library only."""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOPICS = ROOT / "topics"
TEMPLATES = ROOT / "templates"


def today():
    return datetime.date.today()


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.strip().lower()).strip("-")
    if not s:
        sys.exit("error: empty topic name")
    return s


def topic_dir(topic, must_exist=True):
    d = TOPICS / slug(topic)
    if must_exist and not d.is_dir():
        sys.exit(f"error: no such topic '{topic}'. Create it with: python3 tools/new.py dump {topic}")
    return d


def render(template_name, **kw):
    text = (TEMPLATES / template_name).read_text(encoding="utf-8")
    for k, v in kw.items():
        text = text.replace("{" + k + "}", str(v))
    return text


# ---- minimal frontmatter (flat key: value, JSON-quoted when needed) ----

_FM = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


def _parse_val(v):
    v = v.strip()
    if v.startswith('"'):
        try:
            return json.loads(v)
        except ValueError:
            return v
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def _fmt_val(v):
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str) and re.fullmatch(r"[A-Za-z0-9_./-]+", v):
        return v
    return json.dumps(v, ensure_ascii=False)


def split_fm(text):
    m = _FM.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = _parse_val(v)
    return meta, m.group(2)


def join_fm(meta, body):
    lines = [f"{k}: {_fmt_val(v)}" for k, v in meta.items()]
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def read_fm(path):
    return split_fm(pathlib.Path(path).read_text(encoding="utf-8"))


def write_fm(path, meta, body):
    pathlib.Path(path).write_text(join_fm(meta, body), encoding="utf-8")


# ---- markdown sections ----

def get_section(body, title):
    m = re.search(rf"^## {re.escape(title)}[^\n]*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def set_section(body, title, text, append=False):
    pat = re.compile(rf"(^## {re.escape(title)}[^\n]*\n)(.*?)(?=^## |\Z)", re.S | re.M)
    m = pat.search(body)
    if not m:
        return body.rstrip() + f"\n\n## {title}\n\n{text.strip()}\n"
    old = m.group(2).strip()
    new = (old + "\n" + text.strip()) if (append and old) else text.strip()
    return body[: m.start()] + m.group(1) + "\n" + new + "\n\n" + body[m.end():]


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def words(text):
    text = strip_comments(text)
    text = "\n".join(l for l in text.splitlines() if not l.startswith("#") and not l.startswith("Audience:") and not l.startswith("Question:"))
    return len(text.split())


# ---- topic files ----

def num(path):
    m = re.search(r"(\d+)", pathlib.Path(path).stem)
    return int(m.group(1)) if m else 0


def versions(d, prefix):
    return sorted(d.glob(f"{prefix}-v*.md"), key=num)


def all_qa():
    return sorted(TOPICS.glob("*/qa/q-*.md"))


def find_qa(qid):
    qid = str(qid).strip()
    if not qid.startswith("q-"):
        qid = f"q-{int(qid):04d}"
    hits = list(TOPICS.glob(f"*/qa/{qid}.md"))
    if not hits:
        sys.exit(f"error: no question {qid}")
    return hits[0]


def first_line(text, n=110):
    line = " ".join(text.split())
    return line if len(line) <= n else line[: n - 1] + "…"
