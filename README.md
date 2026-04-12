# AOS — AI Operating Standard (v0.1)

**A physical governance layer for autonomous AI agents.**

> "Textual rules enforce at reading time. Physical constraints enforce at execution time."

## The Problem
In a 2026 forensic audit of a production repository, an AI agent was provided with 130KB of governance documentation. It acknowledged the rules, then proceeded to violate them in 52 out of 52 tool calls. 

**Instruction is not enough. We need architecture.**

## What is AOS?
AOS defines a minimum physical constraint layer for AI agent operations. It moves governance from "prompt-based compliance" to "system-level enforcement."

### Key Specifications:
* **§3.2 Three Zones:** Classifies every path as **Oracle** (Read-only), **Permitted** (Workspace), or **Prohibited**.
* **§4.1 Physical Enforcement:** Requires a **PreToolUse hook** that intercepts tool calls and blocks writes to the Oracle zone with `exit 2` before any side effect occurs.
* **§4.3 Structural Role Separation:** Mandates that the agent generating an artifact MUST NOT be the one evaluating it. 
* **§4.4 Physical Evidence:** Conversational assertions ("Task done") are rejected. Only physical artifacts (logs, test results) count as evidence of completion.

## Implementation
* **[AOS-v0.1.md](./AOS-v0.1.md):** The core specification for human and machine reading.
* **Reference Implementation:** [iron_cage](https://github.com/aos-standard/iron_cage) (Reference implementation for Claude Code / Cursor).

## Why this matters
As we move toward autonomous agents with filesystem access, "behaving well" cannot be a choice left to the model. AOS provides the "Physical Laws" that the model simply cannot break.

---
*Status: Draft (v0.1). Contributions via Issues and PRs are welcome.*
