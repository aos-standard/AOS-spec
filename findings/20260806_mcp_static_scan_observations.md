# MCP static scan observations (2026-08-06)

Measured facts only. **Not normative spec text.**

## Public MCP implementation scan

Static analysis of publicly reachable MCP server implementations (passive corpus harvest):

| Metric | Value |
|---|---:|
| Targets scanned | 29 |
| Targets with valid pattern output | 16 |
| Total divergence findings | 125 |

**Divergence class distribution:**

| Class | Count |
|---|---:|
| `undeclared_network` | 68 |
| `undeclared_write` | 39 |
| `undeclared_subprocess` | 14 |
| `undeclared_env` | 4 |

These counts describe gaps between **declared MCP tool surfaces** and observed behavior. They are not an AOS conformance audit.

## Weekly re-scan cadence

Time-series re-scans of the wild target corpus began on:

- **2026-08-02**
- **2026-08-03**

Two observation points exist so far; the series will accumulate from here.

## Standards thread discussion (external pointers)

Factual links to MCP SEP threads under discussion (no self-assessment):

- [SEP-3004](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/3004) — canonicalization two-layer separation; witness externalization
- [SEP-3140](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/3140) — signatures guarantee declaration-time authenticity only
