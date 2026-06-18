# AOS — AI Operating Standard
## Version 0.2 | Status: Stable | 2026-06-02

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

## 6. Reference Implementations

**physical-agent-patterns** — three patterns for AOS-compliant agent infrastructure
in production environments:

| Pattern | Path | AOS section |
|---------|------|-------------|
| systemd Runtime | `patterns/01_systemd-runtime/` | §4.4 (persistent evidence across restarts) |
| Physical-First | `patterns/02_physical-first/` | §4.4 (evidence before completion claim) |
| Immune Loop | `patterns/03_immune-loop/` | §4.1, §4.5 (violation detection + escalation) |

Repository: https://github.com/aos-standard/physical-agent-patterns

These patterns are not AOS. AOS is the standard.
They are evidence that §4.1–§4.5 are implementable
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
  "aos_compliant": "v0.2",
  "permitted_output_paths": ["docs/reports/"],
  "oracle_paths": ["evals/", "config/"]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `aos_compliant` | **Yes** | AOS version string (e.g. `"v0.2"`). Presence signals the tool is AOS-compliant. |
| `permitted_output_paths` | **Yes** | List of relative paths (from tool root) where agents may write. |
| `oracle_paths` | Recommended | List of relative paths agents must not write. Defaults to `["evals/", "config/"]` if omitted. |

A tool that declares `aos_compliant` MUST ensure its runtime enforcement
(PreToolUse hook, CI gate, or equivalent) actually blocks writes to
`oracle_paths`. Declaration without enforcement is non-compliant.

**Machine validation:** Declarations and blast-radius divergences are checked by
[`mcp-blast-radius`](https://pypi.org/project/mcp-blast-radius/)
(`pip install mcp-blast-radius`; pin a version in CI — see
[README § Compliance validation](./README.md#compliance-validation-official)).
Use `mcp-blast-radius-gate --gate-mode blocking --target-dir .` in CI, or the
MCP server `mcp-blast-radius` for interactive checks.

See `examples/manifest_annotation/manifest.json` for a minimal compliant example.

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
    "aos_compliant": "v0.2",
    "permitted_output_paths": ["docs/reports/"],
    "oracle_paths": ["evals/", "config/"]
  }
]
```

Non-compliant tools (no `aos_compliant` field) SHOULD be treated as
unsafe for autonomous write operations.

---

## §10 Implementation Examples

This section shows how AOS-compliant tools satisfy the specification in practice.
All examples are from production repositories and are publicly available.

### §10.1 Manifest Declaration in Practice

**Corresponds to:** §8, §9

A production AOS-compliant tool declares its zones in `manifest.json`.
The following illustrative fragment shows the declaration style used by
AOS-compliant tools such as `0012_Public_Catalog_Publisher`:

```json
{
  "aos_compliant": "v0.2",
  "permitted_output_paths": ["docs/reports/"],
  "oracle_paths": ["evals/", "config/"]
}
```

`oracle_paths` maps directly to the Oracle zone in §3.2 — the hook blocks any
agent write to these paths at execution time.
`permitted_output_paths` is the Permitted zone: the only paths where the tool
may produce output.

A PreToolUse hook loads this manifest at startup and enforces the boundaries
before any write tool call executes. Declaration without a running hook is
non-compliant (§8, final paragraph).

Annotated sample: [`examples/manifest_annotation/manifest.json`](examples/manifest_annotation/manifest.json)

---

### §10.2 Physical Evidence Pattern

**Corresponds to:** §4.4 Physical Evidence Requirement

The key failure mode AOS prevents: an agent "ran" but left no trace.
The physical-first pattern makes evidence a precondition of completion,
not an afterthought.

```python
# Write evidence BEFORE declaring done (from agent_with_evidence.py)
evidence = {
    "task": task,
    "result": result_text,
    "timestamp": datetime.date.today().isoformat(),
    "model": model,
}
evidence_path.write_text(json.dumps(evidence, indent=2))
# Only after the file exists: print completion
print(f"[done] Evidence written: {evidence_path}")
```

The completion claim is only valid when `evidence_path` exists on disk.
A caller can verify completion by checking the file — no conversational
assertion required.

Source: [`physical-agent-patterns/patterns/02_physical-first/agent_with_evidence.py`](https://github.com/aos-standard/physical-agent-patterns/blob/main/patterns/02_physical-first/agent_with_evidence.py)

---

### §10.3 Immune Loop Pattern

**Corresponds to:** §4.1 Hook Requirement, §4.5 Escalation on Ambiguity

A running agent detects AOS violations in the workspace and triggers a
repair sequence. The violation detector writes a structured JSON report
(satisfying §4.4 itself). The repair planner reads that report and either
applies known fixes or escalates to the Sovereign when a design decision
is required (§4.5).

```python
# violation_detector.py — writes report before any repair attempt
violations = _scan(root)
report = {
    "timestamp": datetime.datetime.utcnow().isoformat(),
    "violations": violations,
}
report_path.write_text(json.dumps(report, indent=2))
```

The loop separates detection (read-only scan) from repair (write), which
satisfies §4.3 role separation: the detector does not repair its own findings.

Source: [`physical-agent-patterns/patterns/03_immune-loop/`](https://github.com/aos-standard/physical-agent-patterns/tree/main/patterns/03_immune-loop)

---

### §10.4 systemd Runtime Pattern

**Corresponds to:** §4.4 Physical Evidence Requirement (persistence across restarts)

An agent that only runs interactively cannot satisfy §4.4 across reboots.
The systemd pattern binds the agent to the OS process supervisor: the service
defines the execution boundary; the timer enforces the schedule; output files
survive restarts.

```python
# agent.py — output file is evidence of the run
output_path = OUTPUT_DIR / f"agent_run_{today}.md"
if output_path.exists():
    print(f"[skip] Output already exists for {today}: {output_path}")
    return output_path
# ... run and write ...
output_path.write_text(content)
```

The idempotency guard (`if output_path.exists(): return`) prevents duplicate
runs while keeping the evidence file as the canonical completion record.

```ini
# physical-agent.service (excerpt)
[Service]
ExecStart=/usr/bin/python3 /opt/agent/agent.py
```

```ini
# physical-agent.timer (excerpt)
[Timer]
OnCalendar=daily
Persistent=true
```

`Persistent=true` ensures the timer fires on next boot if the scheduled run
was missed — the evidence requirement is met regardless of uptime.

Source: [`physical-agent-patterns/patterns/01_systemd-runtime/`](https://github.com/aos-standard/physical-agent-patterns/tree/main/patterns/01_systemd-runtime)
