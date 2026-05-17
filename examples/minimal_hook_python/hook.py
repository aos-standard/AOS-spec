# AOS v0.1 compliant — Oracle zone protection example
"""Minimal stdin JSON hook: exit 2 blocks Write/Edit targeting Oracle paths."""

from __future__ import annotations

import json
import re
import sys

_ORACLE_PATTERNS = (
    re.compile(r"(?:^|/)evals(?:/|$)"),
    re.compile(r"(?:^|/)config(?:/|$)"),
)


def _is_oracle_path(file_path: str) -> bool:
    norm = file_path.replace("\\", "/")
    return any(p.search(norm) for p in _ORACLE_PATTERNS)


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0

    tool_name = (data.get("tool_name") or "").strip()
    tool_input = data.get("tool_input") or {}

    if tool_name in ("Write", "Edit"):
        fp = str(tool_input.get("file_path") or tool_input.get("filePath") or "")
        if fp and _is_oracle_path(fp):
            print("[AOS hook] blocked Oracle-zone write", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
