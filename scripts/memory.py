#!/usr/bin/env python3
"""Workspace-scoped experience memory for fullstack-test-engineer skill.

Commands:
  path                 Print memory file path
  snapshot             JSON: common_patterns + recent_runs + exists
  update               Read JSON spec from stdin; merge patterns; print stats

Memory lives under:
  $HOME/.fullstack-test-engineer/memory/<workspace-id>.md

No project secrets should be written. Callers must generalize patterns.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import fcntl
except ImportError:  # Windows fallback: no flock
    fcntl = None  # type: ignore

DEFAULT_HEADER = [
    "# Full-Stack QA Experience Memory",
    "",
    "> Maintained by the fullstack-test-engineer skill.",
    "> Store only generalized, privacy-safe patterns (no hosts, tokens, PII, internal paths).",
    "> Shared across worktrees that resolve to the same workspace id.",
    "",
]

MAX_PATTERNS_PER_CATEGORY = 25
MAX_RECENT_RUNS = 20
CATEGORIES_ORDER = [
    "Requirements",
    "API",
    "Frontend",
    "Content",
    "Compatibility",
    "Security",
    "Performance",
    "Defects",
    "Process",
    "Other",
]


def _home() -> Path:
    h = os.environ.get("HOME") or os.environ.get("USERPROFILE")
    if not h:
        h = str(Path.home())
    return Path(h)


def _memory_root() -> Path:
    return _home() / ".fullstack-test-engineer" / "memory"


def _run(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str]:
    import subprocess

    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return p.returncode, (p.stdout or "").strip()
    except Exception as e:
        return 1, str(e)


def workspace_id(cwd: Optional[Path] = None) -> str:
    cwd = cwd or Path.cwd()
    code, remote = _run(["git", "config", "--get", "remote.origin.url"], cwd)
    if code == 0 and remote:
        key = _canonicalize_remote(remote)
    else:
        code, gitdir = _run(["git", "rev-parse", "--git-common-dir"], cwd)
        if code == 0 and gitdir:
            key = str(Path(gitdir).resolve())
        else:
            key = str(cwd.resolve())
    return "ws-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def _canonicalize_remote(url: str) -> str:
    u = url.strip().rstrip("/")
    if u.endswith(".git"):
        u = u[:-4]
    # git@host:org/repo -> host/org/repo
    m = re.match(r"git@([^:]+):(.+)$", u)
    if m:
        return f"{m.group(1).lower()}/{m.group(2).lower()}"
    u = re.sub(r"^https?://", "", u, flags=re.I)
    u = re.sub(r"^ssh://git@", "", u, flags=re.I)
    return u.lower()


def memory_path(cwd: Optional[Path] = None) -> Path:
    return _memory_root() / f"{workspace_id(cwd)}.md"


def _lock_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".lock")


class FileLock:
    def __init__(self, path: Path, timeout: float = 30.0):
        self.path = path
        self.timeout = timeout
        self._fh = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.path, "a+", encoding="utf-8")
        if fcntl is None:
            return self
        import time

        start = time.time()
        while True:
            try:
                fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except BlockingIOError:
                if time.time() - start > self.timeout:
                    raise TimeoutError(f"lock timeout: {self.path}")
                time.sleep(0.05)

    def __exit__(self, *args):
        if self._fh:
            if fcntl is not None:
                try:
                    fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
                except Exception:
                    pass
            self._fh.close()


_SEEN_RE = re.compile(
    r"^- (?P<desc>.+?) \(seen (?P<count>\d+) times?\)$", re.I
)
_RUN_RE = re.compile(
    r"^###\s+(?P<date>\d{4}-\d{2}-\d{2})\s+[—–-]\s+\"?(?P<title>.*?)\"?\s*$"
)


def parse_memory(text: str) -> Dict[str, Any]:
    patterns: Dict[str, Dict[str, int]] = {}
    runs: List[Dict[str, Any]] = []
    section = None
    category = "Other"
    current_run: Optional[Dict[str, Any]] = None

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## Common Issues") or line.startswith("## Common Patterns"):
            section = "patterns"
            if current_run:
                runs.append(current_run)
                current_run = None
            continue
        if line.startswith("## Recent Runs"):
            section = "runs"
            if current_run:
                runs.append(current_run)
                current_run = None
            continue
        if section == "patterns":
            if line.startswith("### "):
                category = line[4:].strip() or "Other"
                patterns.setdefault(category, {})
            else:
                m = _SEEN_RE.match(line.strip())
                if m:
                    desc = m.group("desc").strip()
                    count = int(m.group("count"))
                    patterns.setdefault(category, {})
                    patterns[category][desc] = patterns[category].get(desc, 0) + count
        elif section == "runs":
            m = _RUN_RE.match(line.strip())
            if m:
                if current_run:
                    runs.append(current_run)
                current_run = {
                    "date": m.group("date"),
                    "description": m.group("title").strip().strip('"'),
                    "body_lines": [],
                }
            elif current_run is not None and line.strip().startswith("-"):
                current_run["body_lines"].append(line.strip())
    if current_run:
        runs.append(current_run)
    return {"patterns": patterns, "runs": runs}


def render_memory(patterns: Dict[str, Dict[str, int]], runs: List[Dict[str, Any]], header: Optional[List[str]] = None) -> str:
    lines = list(header or DEFAULT_HEADER)
    lines.append("## Common Patterns")
    lines.append("")

    # stable category order then alpha
    cats = list(patterns.keys())
    cats.sort(
        key=lambda c: (
            CATEGORIES_ORDER.index(c) if c in CATEGORIES_ORDER else 999,
            c.lower(),
        )
    )
    for cat in cats:
        items = patterns.get(cat) or {}
        if not items:
            continue
        lines.append(f"### {cat}")
        ordered = sorted(items.items(), key=lambda kv: (-kv[1], kv[0].lower()))
        ordered = ordered[:MAX_PATTERNS_PER_CATEGORY]
        for desc, count in ordered:
            unit = "time" if count == 1 else "times"
            lines.append(f"- {desc} (seen {count} {unit})")
        lines.append("")

    lines.append("## Recent Runs")
    lines.append("")
    for run in runs[:MAX_RECENT_RUNS]:
        title = (run.get("description") or "(no description)").replace('"', "")
        date = run.get("date") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        lines.append(f'### {date} — "{title}"')
        for bl in run.get("body_lines") or []:
            if not bl.startswith("-"):
                bl = f"- {bl}"
            lines.append(bl)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _norm_desc(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip().lower())
    s = re.sub(r"[\"'`]", "", s)
    return s


def merge_update(existing: Dict[str, Any], spec: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    patterns: Dict[str, Dict[str, int]] = {
        k: dict(v) for k, v in (existing.get("patterns") or {}).items()
    }
    runs: List[Dict[str, Any]] = list(existing.get("runs") or [])
    stats = {
        "new_patterns": 0,
        "merged_patterns": 0,
        "categories_touched": [],
        "recent_runs_dropped": 0,
    }
    touched = set()

    for p in spec.get("patterns") or []:
        if not isinstance(p, dict):
            continue
        cat = (p.get("category") or "Other").strip() or "Other"
        desc = p.get("description")
        if desc is None:
            continue
        desc = re.sub(r"[\r\n\t]+", " ", str(desc)).strip()
        if not desc:
            continue
        # privacy hard reject
        if _looks_sensitive(desc):
            continue
        bucket = patterns.setdefault(cat, {})
        # exact or normalized match
        match_key = None
        nd = _norm_desc(desc)
        for k in bucket:
            if _norm_desc(k) == nd:
                match_key = k
                break
        if match_key is not None:
            bucket[match_key] = bucket.get(match_key, 0) + 1
            stats["merged_patterns"] += 1
        else:
            bucket[desc] = 1
            stats["new_patterns"] += 1
        touched.add(cat)

    run = spec.get("run")
    if isinstance(run, dict):
        date = (run.get("date") or "").strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date or ""):
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        description = str(run.get("description") or "(no description)").replace('"', "")
        if _looks_sensitive(description):
            description = "(redacted run description)"
        body = []
        deliverables = run.get("deliverables")
        if isinstance(deliverables, list) and deliverables:
            body.append("- **Deliverables**: " + ", ".join(str(x) for x in deliverables[:12]))
        key_patterns = run.get("key_patterns")
        if isinstance(key_patterns, list) and key_patterns:
            cleaned = [str(x) for x in key_patterns[:5] if not _looks_sensitive(str(x))]
            if cleaned:
                body.append("- **Key patterns**: " + "; ".join(cleaned))
        runs.insert(0, {"date": date, "description": description, "body_lines": body})
        if len(runs) > MAX_RECENT_RUNS:
            stats["recent_runs_dropped"] = len(runs) - MAX_RECENT_RUNS
            runs = runs[:MAX_RECENT_RUNS]

    stats["categories_touched"] = sorted(touched)
    return {"patterns": patterns, "runs": runs}, stats


_SENSITIVE = re.compile(
    r"(api[_-]?key|secret|password|passwd|\btoken\b|bearer\s+[a-z0-9\-\._]+|"
    r"authorization:\s*\S+|"
    r"\b\d{1,3}(?:\.\d{1,3}){3}\b|"
    r"[a-z0-9.-]+\.(?:corp|internal|local)\b|"
    r"/Users/[^\s]+|"
    r"/home/[^\s]+|"
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    re.I,
)


def _looks_sensitive(text: str) -> bool:
    return bool(_SENSITIVE.search(text or ""))


def cmd_path() -> int:
    print(memory_path())
    return 0


def cmd_snapshot() -> int:
    path = memory_path()
    exists = path.is_file()
    patterns_flat = []
    runs = []
    if exists:
        data = parse_memory(path.read_text(encoding="utf-8"))
        for cat, items in data["patterns"].items():
            for desc, count in items.items():
                patterns_flat.append(
                    {"category": cat, "description": desc, "count": count}
                )
        patterns_flat.sort(key=lambda x: (-x["count"], x["category"], x["description"]))
        runs = data["runs"]
    out = {
        "file": str(path),
        "exists": exists,
        "common_patterns": patterns_flat,
        "recent_runs": runs,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_update() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        print("memory.py: empty stdin JSON", file=sys.stderr)
        return 4
    try:
        spec = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"memory.py: invalid JSON: {e}", file=sys.stderr)
        return 4
    if not isinstance(spec, dict):
        print("memory.py: spec must be object", file=sys.stderr)
        return 4

    path = memory_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with FileLock(_lock_path(path)):
            existed = path.is_file()
            if existed:
                existing = parse_memory(path.read_text(encoding="utf-8"))
            else:
                existing = {"patterns": {}, "runs": []}
            merged, stats = merge_update(existing, spec)
            text = render_memory(merged["patterns"], merged["runs"])
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".mem-", suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as fh:
                    fh.write(text)
                os.replace(tmp, path)
                try:
                    os.chmod(path, 0o600)
                except OSError:
                    pass
            finally:
                if os.path.exists(tmp):
                    try:
                        os.remove(tmp)
                    except OSError:
                        pass
        result = {
            "file": str(path),
            "existed_before": existed,
            "stats": stats,
            "total_patterns": sum(len(v) for v in merged["patterns"].values()),
            "total_categories": len([k for k, v in merged["patterns"].items() if v]),
            "total_recent_runs": len(merged["runs"]),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except TimeoutError as e:
        print(f"memory.py: {e}", file=sys.stderr)
        return 3
    except OSError as e:
        print(f"memory.py: I/O error: {e}", file=sys.stderr)
        return 1


def main(argv: List[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "path":
        return cmd_path()
    if cmd == "snapshot":
        return cmd_snapshot()
    if cmd == "update":
        return cmd_update()
    print(f"memory.py: unknown command {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
