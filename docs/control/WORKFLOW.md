---
doc_id: WORKFLOW
name: WORKFLOW.md
title: Repository Development Workflow
kind: control
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
references:
  - PROJECT
  - DOCUMENTATION_SYSTEM
  - DOC_INVENTORY
  - PHASES
  - ACCEPTANCE_GATES
  - TEST_STRATEGY
  - TEST_PLAN
  - TESTING_CONVENTIONS
---

# WORKFLOW

## 1. Purpose

This document defines the **normative operational procedure** for evolving this repository.

It integrates:

* documentation discovery rules,
* architectural contracts,
* oracle authority,
* acceptance gates,
* test execution grouping,
* reporting obligations.

This document defines **how work proceeds** from one valid repository state to the next. It defines execution sequencing and decision control.

---

# 2. Pre-Execution Discovery Phase (Mandatory)

Before any modification:

### 2.1 Build Documentation Context

One of:

* Traverse `docs/` and parse YAML metadata; or
* Load `DOC_INVENTORY.json`.

The inventory is authoritative for:

* DOC_ID resolution,
* doc_scope validation,
* layer inference,
* normative vs non-normative filtering.

Filesystem guessing is prohibited.

---

### 2.2 Determine Current State

Read:

* `PHASES.md`
* `ACCEPTANCE_GATES.md`
* `IMPLEMENTATION_REPORTS.md`

Determine:

* Current repository phase
* Highest passed gate
* Next eligible gate

If unclear → stop and escalate.

---

# 3. Target Gate Selection

Work must target **exactly one gate** at a time.

Rules:

* No multi-gate jumps.
* No speculative future behavior.
* No partial cross-gate blending.

The selected gate determines:

* Applicable specs
* Applicable oracles
* Required test suites (via `TEST_PLAN.md`)
* Allowed feature surface

---

# 4. Specification Closure

Before writing code:

1. Identify all normative specs relevant to the selected gate.
2. Identify all oracles that validate those specs.
3. Compute reference closure using DOC_ID references.

If ambiguity or conflict is detected:

* Stop.
* Escalate.
* Do not guess.

---

# 5. Implementation Loop (Single Gate)

For the selected gate:

### 5.1 Minimal Implementation

* Implement only what is required by the specs.
* Respect architectural boundaries.
* No undocumented features.
* No anticipatory extensions.

### 5.2 Oracle Translation

* Ensure each relevant oracle has pytest translation.
* Follow `TESTING_CONVENTIONS.md`.
* Maintain CASE_ID traceability.

### 5.3 Suite Execution

Run only suites required for this gate (`TEST_PLAN.md`).

If failure:

* Classify:
    * spec violation
    * architectural violation
    * test encoding defect
    * determinism defect
* Fix root cause.
* Do not weaken tests without authority update.

Repeat until suite passes.

---

# 6. Gate Validation

A gate is considered satisfied only if:

* All required suites pass.
* No lower gate suite regresses.
* No invariant violations occur.
* Determinism holds.

Then:

* Append to `IMPLEMENTATION_REPORTS.md`.
* Record:
    * Gate number
    * Suites executed
    * Python version
    * Determinism status
    * Any deviations

---

# 7. Escalation Rules

Escalation is mandatory if:

* Spec ambiguity is detected.
* Spec conflict is detected.
* Oracle contradicts spec.
* Implementation requires undocumented behavior.
* Cross-layer coupling emerges.
* Determinism cannot be satisfied.

Escalation must precede implementation change.

---

# 8. Phase Restrictions

All workflow steps are constrained by `PHASES.md`.

If a gate requires behavior forbidden in the current phase:

* Phase must be advanced explicitly.
* Reports must reflect phase transition.

Implicit phase changes are prohibited.

---

# 9. Change Authority Rules

Changes must follow strict ordering:

1. Documentation update (if behavior changes).
2. Oracle update (if required).
3. Test update.
4. Implementation update.

Reverse order is forbidden.

---

# 10. Determinism Enforcement

All development and validation:

* Must be reproducible.
* Must not depend on environment.
* Must not rely on wall-clock timing.
* Must be seed-controlled.

Determinism failure invalidates gate completion.

---

# 11. Human vs Agent Responsibilities

### Agent

* Must read normative docs.
* Must compute reference closure.
* Must obey gate boundaries.
* Must not invent behavior.
* Must stop on ambiguity.

### Human

* Defines or revises specifications.
* Advances phases.
* Approves gate progression.
* Resolves escalations.

---
