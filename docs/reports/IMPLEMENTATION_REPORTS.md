---
name: IMPLEMENTATION_REPORTS.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# IMPLEMENTATION REPORT INSTRUCTIONS

**Agentic Development Execution Reports (Authoritative State)**

---

## 1. Purpose

This document is the **authoritative execution record** of agentic development for this repository.

It records **what actually happened**, not what is allowed or correct.

It exists to:

* provide a resumable state for agents,
* give humans a precise progress and decision history,
* prevent repeated or contradictory work,
* support auditability and evaluation.

This document is **append-only**.

---

## 2. Authority and rules

* This document is **state**, not specification.
* It does **not** override:
    * `PHASES.md`,
    * `ACCEPTANCE_GATES.md`,
    * any normative spec or test oracle.
* It records **attempts, outcomes, and blockers**.

### Mandatory agent rules

Agents **must**:

1. Read this document before acting.
2. Determine the latest completed entry.
3. Append a new entry after any action.
4. Never edit or delete previous entries.

Violation of these rules is a **protocol failure**.

### Current state rule

The **latest entry with `status: completed` or `status: blocked`** defines the current authoritative state of development.

---

## 3. Report entry schema (normative)

Each report entry consists of:

1. A **YAML header** (machine-readable)
2. A **free-form Markdown body** (human-readable)

### 3.1 YAML header schema (REQUIRED)

```yaml
entry_id: <integer>              # Monotonic, strictly increasing; never reused
timestamp_utc: <ISO-8601>        # e.g. 2026-02-09T15:42:00Z
actor: <human|agent|agent:<id>>  # Who performed the action
phase: <integer>                 # Phase number per PHASES.md
target_gate: <integer|null>      # Gate being attempted, if any
status: <planned|in_progress|completed|blocked|failed|aborted>
scope:
  allowed: true|false            # Was this work in-scope for the phase?
  notes: <string|null>
artifacts:
  read:
    - <filename>
  modified:
    - <filename>
  added:
    - <filename>
  deleted:
    - <filename>
tests:
  executed: true|false
  oracle:
    - <TEST_ORACLE.md>
  result: pass|fail|not_run
outcome:
  summary: <short sentence>
  next_step: <string|null>
blockers:
  - <string>
assumptions:
  - <string>
```

All keys are required unless explicitly marked `null`.  
Agents must use a stable identifier across runs when possible.  

---

## 4. Entry format (REQUIRED)

Each entry MUST follow this exact structure:

````md
---

```yaml
<yaml header>
```

### Summary

<free-form narrative summary>

### Details

* bullet points
* reasoning
* decisions
* references to specs

### Notes for next run

* explicit guidance for resumption

---

````

Agents must not invent alternative formats.

---

## 5. Canonical example entry

````md
---

```yaml
entry_id: 1
timestamp_utc: 2026-02-09T16:10:00Z
actor: agent:gpt
phase: 0
target_gate: 0
status: completed
scope:
  allowed: true
  notes: "Documentation spine establishment"
artifacts:
  read:
    - PROJECT.md
    - PHASES.md
    - ACCEPTANCE_GATES.md
    - ARCHITECTURE.md
    - DECOMPOSITION.md
  modified:
    - PROJECT.md
  added:
    - IMPLEMENTATION_REPORTSORTS.md
  deleted: []
tests:
  executed: false
  oracle: []
  result: not_run
outcome:
  summary: "Phase 0 documentation spine established; execution report introduced"
  next_step: "Proceed to Gate 1 (core skeleton) in Phase 1"
blockers: []
assumptions:
  - "No code implementation permitted in Phase 0"
```
````

### Summary

Initialized the execution report and integrated it into the documentation authority system. No code was written. All actions were documentation-only and in-scope for Phase 0.

### Details

* Introduced `IMPLEMENTATION_REPORTS.md` as append-only execution record
* Integrated into PROJECT.md workflow and index
* Confirmed no contradictions with PHASES or ACCEPTANCE_GATES

### Notes for next run

* Agent should move to Phase 1
* Target Gate: 1 (Core skeleton & types)
* Read CORE_API.md and CORE_TEST_ORACLE.md before coding

---

## 6. Status field semantics (normative)

- `planned` — intention recorded, no action taken
- `in_progress` — partial work performed
- `completed` — gate/phase objective satisfied
- `blocked` — progress impossible without clarification
- `failed` — attempted but did not meet criteria
- `aborted` — intentionally stopped (with reason)

Agents must not create entries with `status: planned` unless explicitly instructed to record intent without execution.

---

## 7. What belongs here vs elsewhere

| Information type           | Location                     |
| -------------------------- | ---------------------------- |
| What is allowed            | PHASES.md                    |
| What is correct            | ACCEPTANCE_GATES.md          |
| What must be tested        | *_TEST_ORACLE.md             |
| What exists structurally   | ARCHITECTURE / DECOMPOSITION |
| **What actually happened** | IMPLEMENTATION_REPORTS.md    |

---

## 8. Final rule (non-negotiable)

If a future agent does not know **what to do next**, the correct answer is:

> “Read `IMPLEMENTATION_REPORTS.md`.”

---

# IMPLEMENTATION REPORTS

> [!NOTE]
> 
> **APPEND IMPLEMENTATION REPORT RECORDS BELOW THIS NOTE**

---

