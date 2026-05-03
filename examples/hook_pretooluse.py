"""
AOS v0.1 — Oracle Zone Enforcement Hook (Reference Implementation)

Purpose:
    Intercept agent write calls before they reach the filesystem.
    Block writes to Oracle Zone paths. Allow writes to Permitted Zone paths.

Usage:
    Invoke this script as a PreToolUse hook in your agent runtime.
    The hook reads a JSON payload from stdin describing the pending tool call
    and exits with code 2 to block, or 0 to allow.

Stdin payload (JSON):
    {
        "tool_name": "Write",          # or "Edit", "Bash", etc.
        "tool_input": {
            "file_path": "evals/test_output.json"
        },
        "cwd": "/path/to/tool/root"
    }

Exit codes:
    0 — Allow the operation.
    2 — Block the operation (agent runtime must abort the tool call).
"""

from __future__ import annotations

import json
import re
import sys


# ---------------------------------------------------------------------------
# Oracle Zone patterns (relative path fragments that must never be written)
# ---------------------------------------------------------------------------
_ORACLE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?:^|/)evals(?:/|$)"),
    re.compile(r"(?:^|/)config(?:/|$)"),
    re.compile(r"(?:^|/)governance(?:/|$)"),
]


def is_oracle_path(file_path: str) -> bool:
    """Return True if file_path matches any Oracle Zone pattern."""
    norm = file_path.replace("\\", "/")
    return any(p.search(norm) for p in _ORACLE_PATTERNS)


def main() -> int:
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return 0  # Cannot parse — allow (fail open for unknown inputs)

    tool_name: str = (data.get("tool_name") or "").strip()
    tool_input: dict = data.get("tool_input") or {}

    if tool_name in ("Write", "Edit"):
        file_path: str = str(tool_input.get("file_path") or tool_input.get("filePath") or "")
        if file_path and is_oracle_path(file_path):
            print(
                f"[AOS Hook] BLOCKED {tool_name}: '{file_path}' is in the Oracle Zone. "
                "Agents must not write to Oracle Zone paths.",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
