#!/usr/bin/env python3
"""Scan paths for privacy-sensitive content before publishing a skill or cases.

Usage:
  python3 scrub_privacy.py --path <file-or-dir> [--report] [--json]
  python3 scrub_privacy.py --path <file-or-dir> --fix-dry-run

Does not auto-rewrite files unless --write-redacted is set (writes *.redacted beside originals).
Exit code: 0 = clean or only LOW; 2 = HIGH findings; 1 = usage/IO error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional

SKIP_DIR_NAMES = {
    ".git",
    ".svn",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".py",
    ".ts",
    ".js",
    ".tsx",
    ".jsx",
    ".csv",
    ".xml",
    ".html",
    ".css",
    ".sh",
    ".env",
    ".toml",
    ".ini",
    ".cfg",
    ".example",
}


@dataclass
class Finding:
    severity: str  # HIGH | MEDIUM | LOW
    rule: str
    path: str
    line: int
    excerpt: str


RULES = [
    (
        "HIGH",
        "secret_assignment",
        re.compile(
            r"(?i)(api[_-]?key|secret|password|passwd|access[_-]?token|private[_-]?key)\s*[:=]\s*['\"][^'\"]{6,}['\"]"
        ),
    ),
    (
        "HIGH",
        "bearer_token",
        re.compile(r"(?i)bearer\s+[a-z0-9\-_\.=]{20,}"),
    ),
    (
        "HIGH",
        "private_key_block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "HIGH",
        "home_path_unix",
        re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"),
    ),
    (
        "HIGH",
        "windows_user_path",
        re.compile(r"(?i)C:\\Users\\[^\\]+\\"),
    ),
    (
        "MEDIUM",
        "email",
        re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ),
    (
        "MEDIUM",
        "ipv4",
        re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    ),
    (
        "MEDIUM",
        "internal_host",
        re.compile(
            r"(?i)\b[a-z0-9.-]+\.(?:corp|internal|intranet|local|lan)\b"
        ),
    ),
    (
        "MEDIUM",
        "mesh_or_internal_gateway",
        re.compile(r"(?i)\b[\w.-]*mesh[\w.-]*\.[a-z0-9.-]+\b"),
    ),
    (
        "LOW",
        "phone_cn",
        re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    ),
    (
        "LOW",
        "jwt_like",
        re.compile(r"\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b"),
    ),
]

# Allow common docs examples / placeholders (not real secrets)
ALLOW_HOME_USERS = {
    "you",
    "alice",
    "bob",
    "username",
    "your-name",
    "yourname",
    "user",
    "name",
    "example",
}
ALLOW_SUBSTRINGS = [
    "user@example.com",
    "127.0.0.1",
    "0.0.0.0",
    "localhost",
    "example.com",
    "example.org",
    "your-name",
    "/Users/you/",
    "/Users/alice/",
    "/home/you/",
    "Bearer <token>",
    "sk-xxx",
]


def iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if p.suffix.lower() in TEXT_SUFFIXES or p.name in {
            "SKILL.md",
            "README.md",
            "AGENTS.md",
            "LICENSE",
            ".gitignore",
        }:
            yield p


def _allowed(line: str) -> bool:
    low = line.lower()
    for a in ALLOW_SUBSTRINGS:
        if a.lower() in low:
            # still flag if real secret patterns besides allowlist phrase
            if "bearer <token>" in low or "sk-xxx" in low:
                return True
            # if line only contains example email etc., skip medium email hits later via match context
            pass
    return False


_HOME_PATH_RE = re.compile(r"/(?:Users|home)/([A-Za-z0-9._-]+)/")


def _is_placeholder_home_path(line: str) -> bool:
    for m in _HOME_PATH_RE.finditer(line):
        if m.group(1).lower() not in ALLOW_HOME_USERS:
            return False
    # true only if every home path on the line is a placeholder
    return bool(_HOME_PATH_RE.search(line))


def scan_text(path: Path, text: str) -> List[Finding]:
    findings: List[Finding] = []
    for i, line in enumerate(text.splitlines(), 1):
        for sev, name, rx in RULES:
            m = rx.search(line)
            if not m:
                continue
            if name in ("home_path_unix", "windows_user_path"):
                # documentation / code that only shows placeholder homes is OK
                if _is_placeholder_home_path(line) or "Users/you" in line or "Users/alice" in line:
                    continue
                # regex patterns inside source that match the rule string itself
                if "Users|home" in line or r"Users\\you" in line or "ALLOW_HOME" in line:
                    continue
            if name == "email" and "example.com" in line:
                continue
            if name == "ipv4" and any(
                x in line for x in ("127.0.0.1", "0.0.0.0", "255.255.255.")
            ):
                continue
            if name == "bearer_token" and "<token>" in line:
                continue
            findings.append(Finding(sev, name, str(path), i, line.strip()[:200]))
    return findings


REDACTIONS = [
    (re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"), "/Users/you/"),
    (re.compile(r"(?i)C:\\Users\\[^\\]+\\"), r"C:\\Users\\you\\"),
    (re.compile(r"(?i)bearer\s+[a-z0-9\-_\.=]{20,}"), "Bearer <token>"),
    (
        re.compile(
            r"(?i)((?:api[_-]?key|secret|password|passwd|access[_-]?token)\s*[:=]\s*)['\"][^'\"]{6,}['\"]"
        ),
        r"\1\"<redacted>\"",
    ),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "user@example.com"),
]


def redact_text(text: str) -> str:
    out = text
    for rx, repl in REDACTIONS:
        out = rx.sub(repl, out)
    return out


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Privacy scrub for skill publish")
    ap.add_argument("--path", required=True, help="File or directory to scan")
    ap.add_argument("--report", action="store_true", help="Print human report")
    ap.add_argument("--json", action="store_true", help="Print JSON findings")
    ap.add_argument(
        "--write-redacted",
        action="store_true",
        help="Write sibling *.redacted copies with simple substitutions",
    )
    args = ap.parse_args(argv)

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"path not found: {root}", file=sys.stderr)
        return 1

    all_findings: List[Finding] = []
    for f in iter_files(root):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"skip {f}: {e}", file=sys.stderr)
            continue
        findings = scan_text(f, text)
        all_findings.extend(findings)
        if args.write_redacted and findings:
            red = redact_text(text)
            out = f.with_name(f.name + ".redacted")
            out.write_text(red, encoding="utf-8")

    high = sum(1 for x in all_findings if x.severity == "HIGH")
    medium = sum(1 for x in all_findings if x.severity == "MEDIUM")
    low = sum(1 for x in all_findings if x.severity == "LOW")

    if args.json:
        print(
            json.dumps(
                {
                    "path": str(root),
                    "counts": {"HIGH": high, "MEDIUM": medium, "LOW": low},
                    "findings": [asdict(x) for x in all_findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.report or not args.json:
        print(f"Privacy scan: {root}")
        print(f"  HIGH={high} MEDIUM={medium} LOW={low} total={len(all_findings)}")
        for x in all_findings[:100]:
            print(f"  [{x.severity}] {x.rule} {x.path}:{x.line}")
            print(f"           {x.excerpt}")
        if len(all_findings) > 100:
            print(f"  ... {len(all_findings) - 100} more")
        if high == 0 and medium == 0:
            print("  Result: CLEAN (or only LOW). OK to publish after manual review.")
        elif high == 0:
            print("  Result: REVIEW MEDIUM findings (hosts/emails) before publish.")
        else:
            print("  Result: BLOCKED — fix HIGH findings before GitHub.")

    return 2 if high else 0


if __name__ == "__main__":
    sys.exit(main())
