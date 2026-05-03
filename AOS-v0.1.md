# AOS — AI Operating Standard
## Version 0.1 | Status: Stable | 2026-04-06

---

## 0. Machine-Reading Instructions

This document is a specification for AI agents.
Read every MUST/MUST NOT as a hard constraint.
Read every SHOULD as a strong recommendation with documented rationale.
Section identifiers (§N.N) are stable references for citation.

---

## 1. Problem Statement

Textual rules fail at scale.

A repository may contain 130KB of governance documentation.
An AI agent reads it, acknowledges it, and violates it on the next tool call.
This is not a failure of instruction. It is a failure of architecture.

The failure mode: textual rules require the agent to choose compliance.
Physical constraints remove the choice.

AOS defines the minimum physical constraint layer for AI agent operations
in a shared codebase.

---

## 2. Definitions

**Write operation**: any action that modifies, creates, or deletes a file
on disk. Includes: file write, file edit, `sed -i`, shell redirection (`>`),
`truncate`, `perl -i`.

**Oracle**: a file or directory whose integrity must not be modified by the
agent under evaluation. Examples: test expectation files, audit logs,
governance documents.

**Physical constraint**: a mechanism that prevents a Write operation at the
OS or hook layer, before the agent's output reaches the filesystem.

**Textual rule**: a governance instruction expressed in natural language,
relied upon solely through the agent's compliance choice.

**PreToolUse hook**: a process invoked before a tool call executes,
with authority to terminate the call (exit 2) before side effects occur.

---

## 3. Core Model

### §3.1 The Fundamental Law

> Physical constraints MUST be enforced before textual rules are consulted.
> If a physical constraint and a textual rule conflict, the physical
> constraint governs.

### §3.2 Three Zones

Every path in the repository MUST be classified into one of three zones:

| Zone | Class | Write permission |
|------|-------|-----------------|
| **Oracle** | Read-only absolute | MUST NOT be written by any agent |
| **Permitted** | Agent workspace | MAY be written within role limits |
| **Prohibited** | Out of scope | MUST NOT be written without explicit sovereign authorization |

Oracle zone examples: `evals/`, governance documents, audit log directories.

### §3.3 Three Roles

AOS defines three non-overlapping roles. An agent MUST NOT act outside
its assigned role without explicit human authorization recorded in
a durable artifact (not a conversational message).

| Role | Permitted operations | Prohibited operations |
|------|---------------------|-----------------------|
| **Architect** | Design, verify, push | Bulk execution without review |
| **Executor** | Implement assigned patterns | Design decisions, push |
| **Sovereign** | Authorize phase transitions, push | — |

An agent that detects it is being asked to act outside its role
MUST stop, state the role boundary, and request clarification.

---

## 4. Specification

### §4.1 Hook Requirement (MUST)

A compliant AOS implementation MUST intercept the following tool calls
via a PreToolUse hook before filesystem access:

- File write (any mechanism)
- File edit (any mechanism)  
- Shell command execution

The hook MUST exit with code 2 (blocking) when:

1. The target path resolves to the Oracle zone.
2. The target path is outside all Permitted zones.
3. The command matches a destructive in-place edit pattern
   (e.g., `sed -i`, `perl -i`, `truncate`).

### §4.2 Oracle Integrity (MUST NOT)

An agent MUST NOT write to the Oracle zone under any instruction,
including instructions from a human in the current conversation.

The only exception: a Sovereign explicitly modifying governance documents
outside of agent-assisted sessions.

Rationale: an agent that can modify its own evaluation criteria
cannot be trusted to report accurate results.

### §4.3 Role Separation (MUST)

The agent that generates an artifact MUST NOT be the sole evaluator
of that artifact.

A compliant implementation MUST route evaluation to a separate agent
session with no access to the generation context.

This is not a recommendation. An agent evaluating its own output
shares the same failure modes as the original generation.
Structural separation is the only remedy.

### §4.4 Physical Evidence Requirement (MUST)

An agent MUST NOT assert completion of a task without a physical artifact
as evidence.

Acceptable evidence: a log file written to a non-Oracle permitted path,
a test result file, a structured output file with a timestamp.

Unacceptable evidence: a conversational assertion ("the task is done"),
a claim without a file path, a reference to prior session output.

### §4.5 Escalation on Ambiguity (MUST)

If an agent receives an instruction that requires a design decision
not already resolved in a written specification, the agent MUST stop
and escalate to the Architect role.

Executing ambiguous instructions is a role boundary violation.

---

## 5. Compliance Verification

A repository is AOS-compliant when:

- [ ] §4.1: PreToolUse hook is active and blocks Oracle writes (verifiable by attempting a blocked write and observing exit 2)
- [ ] §4.2: Oracle zone is defined in a machine-readable config loaded by the hook
- [ ] §4.3: Evaluation sessions are structurally separated from generation sessions
- [ ] §4.4: Every completed task has a physical artifact at a stable path
- [ ] §4.5: No agent has executed a task requiring unresolved design decisions

---

## 6. Reference Implementation

**iron\_cage** is the AOS reference implementation for Claude Code
(Anthropic) and Cursor environments.

Repository: [to be published]

iron\_cage implements §4.1 via Claude Code's PreToolUse hook system,
with Oracle zones defined in a Python configuration module.
The hook exits 2 on Oracle writes and prohibited-zone writes.

iron\_cage is not AOS. AOS is the standard.
iron\_cage is evidence that §4.1–§4.5 are implementable
in a production single-developer repository.

---

## 7. What AOS Does Not Specify

AOS does not specify:
- Which AI model to use
- Programming language or framework
- Repository structure beyond zone classification
- How agents communicate with each other

These are implementation decisions. AOS specifies only
the physical constraint layer that makes agent governance
structurally enforceable.

---

## Appendix: Why Textual Rules Fail

An AI agent operating on a shared codebase in 2026 reads governance
documentation at context load. It acknowledges the rules.
It then executes tool calls that violate them — not from
malicious intent, but because the cost of compliance
is not enforced at the point of execution.

The pattern is identical to why `rm -rf /` requires a confirmation flag,
not a policy document. Physical constraints enforce at execution time.
Textual rules enforce at reading time, which is the wrong moment.

AOS exists because 130KB of governance text, read and acknowledged,
produced zero verified compliance in 52 of 52 tools in a production
repository (forensic audit, 2026-04-01).

Physical constraints are not a supplement to textual rules.
They are the replacement.

---

## §8 Tool Compliance Declaration

An AOS-compliant tool declares its zone boundaries in `manifest.json`
by adding the following fields:

```json
{
  "aos_compliant": "v0.1",
  "permitted_output_paths": ["docs/reports/"],
  "oracle_paths": ["evals/", "config/"]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `aos_compliant` | **Yes** | AOS version string (e.g. `"v0.1"`). Presence signals the tool is AOS-compliant. |
| `permitted_output_paths` | **Yes** | List of relative paths (from tool root) where agents may write. |
| `oracle_paths` | Recommended | List of relative paths agents must not write. Defaults to `["evals/", "config/"]` if omitted. |

A tool that declares `aos_compliant` MUST ensure its runtime enforcement
(PreToolUse hook, CI gate, or equivalent) actually blocks writes to
`oracle_paths`. Declaration without enforcement is non-compliant.

See `examples/manifest_example.json` for a minimal compliant example.

---

## §9 Agent Discovery

AOS-compliant tools are discoverable via the MCP `list_tools` interface.
An agent querying a compliant MCP server SHOULD:

1. Call `list_tools` on the MCP endpoint.
2. Inspect each tool entry for the `aos_compliant` field.
3. Consider only entries where `aos_compliant` is present as eligible
   for autonomous, agent-to-agent invocation.
4. Retrieve `permitted_output_paths` and `oracle_paths` before issuing
   any write operations.

**Example response fragment:**

```json
[
  {
    "name": "public_catalog_publisher",
    "description": "Publishes a structured catalog of available tools for external agent discovery.",
    "aos_compliant": "v0.1",
    "permitted_output_paths": ["docs/reports/"],
    "oracle_paths": ["evals/", "config/"]
  }
]
```

Non-compliant tools (no `aos_compliant` field) SHOULD be treated as
unsafe for autonomous write operations.