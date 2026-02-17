---
doc_id: TEST_PLAN
name: TEST_PLAN.md
title: Test Execution Plan and Named Suites
kind: control
scope: global
status: active
authority: normative
references:
  - ACCEPTANCE_GATES
  - PHASES
  - TEST_STRATEGY
  - TESTING_CONVENTIONS
url: https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# TEST_PLAN

## 1. Purpose

This document defines:

- Named test suites
- Which suites are executed for each acceptance gate
- Which suites are allowed in each repository phase
- Execution grouping for S7 (Test Runner) and bug-fixer

This document does **not**:

- Define correctness (see TEST_STRATEGY.md)
- Define oracle mechanics (see TESTING_CONVENTIONS.md)
- Define gate criteria (see ACCEPTANCE_GATES.md)

It defines **execution scope and grouping only**.

---

# 2. Suite Taxonomy

Suites are defined according to:

1. Architectural decomposition
2. Acceptance gates
3. Repository phases
4. Determinism and reproducibility requirements

Each suite is cumulative within its domain.

---

# 3. Named Suites

## 3.1 CORE_BASE_SUITE

**Scope**

- Core skeleton and API shape
- Structural correctness
- Deterministic state transitions

**Covers gates**

- Gate 1

**Oracle authority**

- CORE_TEST_ORACLE.md (subset)

**Used in phase**

- Phase 1+

**Purpose**
Fast structural validation during early core development.

---

## 3.2 CORE_GEOMETRY_SUITE

**Scope**

- Piece geometry
- Rotations
- Collision detection

**Covers gates**

- Gate 2

**Oracle authority**

- CORE_TEST_ORACLE.md

**Used in phase**

- Phase 1+

**Notes**
Must be fully deterministic.
No RNG involved.

---

## 3.3 CORE_EVOLUTION_SUITE

**Scope**

- Gravity
- Locking
- Line clearing
- Scoring
- Level progression
- RNG (7-bag determinism)

**Covers gates**

- Gate 3
- Gate 4

**Oracle authority**

- CORE_TEST_ORACLE.md

**Used in phase**

- Phase 1+

---

## 3.4 CORE_INPUT_SEMANTICS_SUITE

**Scope**

- Rotation semantics
- Wall kicks
- Hard drop
- Input rejection immutability

**Covers gates**

- Gate 5

**Oracle authority**

- CORE_TEST_ORACLE.md

**Used in phase**

- Phase 1+

---

## 3.5 CORE_TERMINATION_SUITE

**Scope**

- Game over rules
- Spawn collision
- Top-row occupation
- Post-game immutability

**Covers gates**

- Gate 6

**Oracle authority**

- CORE_TEST_ORACLE.md

**Used in phase**

- Phase 1+

---

## 3.6 CORE_STRICTNESS_SUITE (optional)

**Scope**

- Invariant enforcement
- Strict mode errors
- Invalid input rejection

**Covers gates**

- Gate 8

**Oracle authority**

- CORE_TEST_ORACLE.md

**Used in phase**

- Phase 1 or 3

---

## 3.7 CORE_AUDIT_SUITE (optional)

**Scope**

- Determinism across runs
- Serialization stability (if enabled)
- Test independence

**Covers gates**

- Gate 9

**Used in phase**

- Phase 1 or 3

---

# 4. Shell-Level Suites (Phase 2+ Only)

These suites are forbidden in Phase 1.

---

## 4.1 RENDERING_SUITE

**Scope**

- ASCII rendering snapshots
- Byte-for-byte frame comparison

**Covers gates**

- Gate 10

**Oracle authority**

- RENDERING_TEST_ORACLE.md

**Used in phase**

- Phase 2+

---

## 4.2 RUNTIME_SCRIPTED_SUITE

**Scope**

- Deterministic virtual-time execution
- One-step-per-tick enforcement
- Early termination on game over

**Covers gates**

- Gate 11

**Oracle authority**

- RUNTIME_TEST_ORACLE.md

**Used in phase**

- Phase 2+

---

## 4.3 CLI_SUITE

**Scope**

- CLI argument parsing
- Exit codes
- Delegation correctness

**Covers gates**

- Gate 12

**Oracle authority**

- CLI_TEST_ORACLE.md

**Used in phase**

- Phase 2+

---

## 4.4 REPLAY_SUITE

**Scope**

- Replay file validation
- Deterministic replay execution
- Strict rejection of malformed input

**Covers gates**

- Gate 13

**Oracle authority**

- REPLAY_TEST_ORACLE.md

**Used in phase**

- Phase 2+

---

## 4.5 CONFIG_SUITE

**Scope**

- Config loading
- Strict validation
- No silent fallback

**Covers gates**

- Gate 13 (if config enabled)

**Oracle authority**

- CONFIG_TEST_ORACLE.md

**Used in phase**

- Phase 2+

---

# 5. Full Suite Definitions

## 5.1 CORE_FULL_SUITE

Includes:

- CORE_BASE_SUITE
- CORE_GEOMETRY_SUITE
- CORE_EVOLUTION_SUITE
- CORE_INPUT_SEMANTICS_SUITE
- CORE_TERMINATION_SUITE

Optional (if enabled):

- CORE_STRICTNESS_SUITE
- CORE_AUDIT_SUITE

**Required for MVP completion (Gates 0–6)**

---

## 5.2 SHELL_FULL_SUITE

Includes:

- RENDERING_SUITE
- RUNTIME_SCRIPTED_SUITE
- CLI_SUITE
- REPLAY_SUITE
- CONFIG_SUITE (if applicable)

---

## 5.3 PROJECT_FULL_SUITE

Includes:

- CORE_FULL_SUITE
- SHELL_FULL_SUITE (if Phase 2+)

---

# 6. Gate-to-Suite Mapping

| Gate | Required Suites |
|------|-----------------|
| Gate 0 | CORE_BASE_SUITE |
| Gate 1 | CORE_BASE_SUITE |
| Gate 2 | CORE_GEOMETRY_SUITE |
| Gate 3 | CORE_EVOLUTION_SUITE |
| Gate 4 | CORE_EVOLUTION_SUITE |
| Gate 5 | CORE_INPUT_SEMANTICS_SUITE |
| Gate 6 | CORE_TERMINATION_SUITE |
| Gate 7 | CORE_INPUT_SEMANTICS_SUITE (extended) |
| Gate 8 | CORE_STRICTNESS_SUITE |
| Gate 9 | CORE_AUDIT_SUITE |
| Gate 10 | RENDERING_SUITE |
| Gate 11 | RUNTIME_SCRIPTED_SUITE |
| Gate 12 | CLI_SUITE |
| Gate 13 | REPLAY_SUITE (+ CONFIG_SUITE if applicable) |

All gates implicitly require all previous gates to pass.

---

# 7. Phase-to-Suite Restrictions

## Phase 0

- No execution suites allowed.
- Documentation validation only.

## Phase 1

Allowed:

- CORE_* suites only.

Forbidden:

- All shell-level suites.

## Phase 2

Allowed:

- CORE_* suites
- All shell suites

## Phase 3+

Allowed:

- All suites
- Additional extension suites if defined

---

# 8. Execution Modes

## 8.1 Fast Local Run

- CORE_BASE_SUITE
- CORE_GEOMETRY_SUITE

Used for rapid iteration.

---

## 8.2 Gate Verification Run

Run only suites required for the current gate.

---

## 8.3 Pre-Commit Run

CORE_FULL_SUITE

---

## 8.4 Release Verification

PROJECT_FULL_SUITE

---

# 9. Determinism Requirement

All suites must:

- Pass in isolated environment.
- Produce identical results across runs.
- Be order-independent.

Failure of determinism fails the entire suite.

---

# 10. Non-Overlapping Responsibility Reminder

- TEST_STRATEGY.md defines correctness semantics.
- TESTING_CONVENTIONS.md defines file/layout mechanics.
- TEST_PLAN.md defines execution grouping and sequencing.
- ACCEPTANCE_GATES.md defines progression criteria.

This document must not duplicate policy or oracle content.

