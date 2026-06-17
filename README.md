# AOS — AI Operating Standard

[![GitHub stars](https://img.shields.io/github/stars/aos-standard/AOS-spec?style=flat-square)](https://github.com/aos-standard/AOS-spec/stargazers)
![Spec Status](https://img.shields.io/badge/Spec%20Status-Stable-blue?style=flat-square)

**A minimal, machine-enforceable specification for constraining AI agent file operations.**

## Why AOS?

- **Execution-time enforcement** — Text-only policies are easy to drift from at runtime; AOS blocks unsafe writes *before* they reach the filesystem.
- **Three zones** — Every path is classified as Oracle (read-only), Permitted (workspace), or Prohibited — see [AOS-v0.2.md](./AOS-v0.2.md) §3.2.
- **Implementation-agnostic** — Any agent runtime that supports pre-invocation hooks (or equivalent guards) can comply; no single vendor stack is required.

## Quick example

This is what AOS enforcement looks like in practice — a minimal PreToolUse hook (Python):

```python
# Block writes to Oracle paths before the tool runs (exit 2 = block).
import json, re, sys
_ORACLE = [re.compile(r"(?:^|/)evals(?:/|$)")]

data = json.loads(sys.stdin.read())
path = str((data.get("tool_input") or {}).get("file_path") or "")
norm = path.replace("\\", "/")
if path and any(p.search(norm) for p in _ORACLE):
    print("[AOS] blocked Oracle write", file=sys.stderr)
    sys.exit(2)
```

Runnable copies: [`examples/minimal_hook_python/hook.py`](examples/minimal_hook_python/hook.py) · [`examples/hook_pretooluse.py`](examples/hook_pretooluse.py)

## Structure: Three Zones

| Zone | Writes |
|------|--------|
| **Oracle** | MUST NOT — canonical sources, expectations, governance inputs agents must not mutate |
| **Permitted** | MAY — workspace paths where an agent may produce artifacts within declared boundaries |
| **Prohibited** | MUST NOT — paths outside permitted scope unless explicitly authorized by a human maintainer |

Normative definitions and hook rules: **[AOS-v0.2.md](./AOS-v0.2.md)** · [AOS-v0.1.md](./AOS-v0.1.md) (previous stable).

## How to cite AOS in your project

Add zone boundaries to `manifest.json` (see §8 in the spec):

```json
{
  "aos_compliant": "v0.1",
  "oracle_paths": ["evals/", "config/"],
  "permitted_output_paths": ["docs/reports/"]
}
```

Minimal sample file: [`examples/manifest_annotation/manifest.json`](examples/manifest_annotation/manifest.json).

## Compliance validation (official)

AOS-v0.1 declarations in `manifest.json` are machine-validated by the official compliance validator published on PyPI.

**Install:**

```bash
pip install aos-compliance-validator-mcp==0.1.0
```

- **PyPI:** [aos-compliance-validator-mcp](https://pypi.org/project/aos-compliance-validator-mcp/0.1.0/)
- **MCP server (Mode A):** `aos-compliance-validator` — stdio transport for Claude / Cursor
- **CI gate (Mode B):** `aos-compliance-gate --gate-mode blocking --target-dir .` — exit 1 when non-compliant

### Guard your agent CI in 3 lines

Add this job step to your workflow (or use the reusable action below):

```yaml
- run: |
    pip install aos-compliance-validator-mcp==0.1.0
    aos-compliance-gate --gate-mode blocking --target-dir .
```

**Reusable GitHub Action** (copy into your repo, or reference from this repo after release):

```yaml
- uses: aos-standard/AOS-spec/.github/actions/aos-compliance-check@main
  with:
    target-dir: .
    package-version: "==0.1.0"
```

### MCP client snippet (Claude / Cursor)

Copy into your `mcp.json` (full example: [`examples/compliance_validator/mcp.json`](examples/compliance_validator/mcp.json)):

```json
{
  "mcpServers": {
    "aos-compliance-validator": {
      "command": "aos-compliance-validator",
      "args": [],
      "env": { "AOS_VALIDATOR_TARGET_DIR": "." }
    }
  }
}
```

## Status & roadmap

- **v0.2** — Stable. Adds §10 Implementation Examples: four production patterns showing §4.4, §4.1, §4.5, §8, §9 in practice. §6 updated to [physical-agent-patterns](https://github.com/aos-standard/physical-agent-patterns).
- **v0.1** — Stable. Three Zones, PreToolUse interception (§4.1), evaluation separation (§4.3), physical evidence (§4.4).

---

⭐ **Star this repo** if you find it useful.

💬 **Open an issue** if you have questions or use cases — [issue templates](.github/ISSUE_TEMPLATE/) available.

🔀 **Pull requests welcome** — see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 🛠 Implementation Support

Implementing AOS in production and want battle-tested templates?

The **Production AI Agent Reliability Pack** includes:
- AOS-compliant agent templates (systemd, immune loop, permission boundaries)
- Monthly agent self-audit checklist
- Async implementation Q&A via Slack

[→ Production AI Agent Reliability Pack (¥4,980/mo)](https://buy.stripe.com/cNieVf0Bs8MB4vP2G81Nu00)
