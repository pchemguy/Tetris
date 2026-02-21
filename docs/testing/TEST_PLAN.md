---
doc_id: TEST_PLAN
name: TEST_PLAN.md
title: Test Execution Plan and Named Suites
status: active
authority: normative
urls:
  - https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
  - https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [ACCEPTANCE_GATES, PHASES, TEST_STRATEGY, TESTING_CONVENTIONS]
---

# TEST_PLAN

## 1. Purpose

This document defines:

- Named executable test suites
- Which suites are required for each acceptance gate
- Which suites are allowed in each repository phase
- Execution grouping rules for agents and developers

This document governs **execution scope and grouping only**.

It does not define:

- Correctness semantics (see `TEST_STRATEGY`)
- Oracle content (see `docs/testing/oracles/`)
- Test encoding mechanics (see `TESTING_CONVENTIONS`)

---

# 2. Suite Model

Suites are execution groupings derived from:

1. Architectural decomposition
2. Acceptance gates
3. Repository phases
4. Determinism requirements

Suites are cumulative:

- Higher gates require all suites from prior gates.
- Later phases may execute additional suites but may not skip required ones.

Suites never redefine oracle authority — they only group already-defined CASE_ID implementations.

---

# 3. Core-Level Suites (Phase 1+)

Core-level suites validate the pure deterministic simulation (`scope: core:core`).

These suites are the only ones permitted in Phase 1.

---

## 3.1 CORE_BASE_SUITE

**Purpose**

Validate minimal structural correctness of the core.

**Covers**

- Core API shape
- Deterministic state object construction
- Basic step contract invariants

**Authority**

- ORACLE_CORE_* documents related to structural and invariant validation

**Gate Coverage**

- Gate 0
- Gate 1

---

## 3.2 CORE_GEOMETRY_SUITE

**Purpose**

Validate canonical geometry and rotation correctness.

**Covers**

- Shapes and rotation enumeration
- Collision predicate (geometry correctness only)

**Authority**

- ORACLE_CORE_GEOMETRY
- ORACLE_CORE_COLLISION (geometry aspects only)

**Gate Coverage**

- Gate 2

No RNG involvement permitted.

---

## 3.3 CORE_EVOLUTION_SUITE

**Purpose**

Validate deterministic game evolution.

**Covers**

- Gravity
- Locking
- Line clearing
- Scoring
- Level progression
- 7-bag RNG determinism

**Authority**

- ORACLE_CORE_GRAVITY_AND_LOCKING
- ORACLE_CORE_LINE_CLEAR
- ORACLE_CORE_SCORING
- ORACLE_CORE_RNG_7BAG

**Gate Coverage**

- Gate 3
- Gate 4

---

## 3.4 CORE_INPUT_SEMANTICS_SUITE

**Purpose**

Validate input processing semantics.

**Covers**

- Rotation semantics
- Wall kicks
- Hard drop behavior
- Rejection immutability
- Per-tick input ordering

**Authority**

- ORACLE_CORE_COLLISION
- ORACLE_CORE_GEOMETRY
- ORACLE_CORE_GRAVITY_AND_LOCKING

**Gate Coverage**

- Gate 5
- Gate 7 (extended input semantics)

---

## 3.5 CORE_TERMINATION_SUITE

**Purpose**

Validate game termination behavior.

**Covers**

- Spawn collision
- Top-row occupation
- Post-game immutability

**Authority**

- ORACLE_CORE_SPAWN
- ORACLE_CORE_GAME_OVER
- ORACLE_CORE_INVARIANTS

**Gate Coverage**

- Gate 6

---

## 3.6 CORE_STRICTNESS_SUITE (Optional)

**Purpose**

Validate invariant enforcement and strict error handling.

**Covers**

- Strict mode exceptions
- Invalid input errors
- Invariant violation detection

**Authority**

- ORACLE_CORE_INVARIANTS
- ORACLE_CORE_COLLISION (error semantics)

**Gate Coverage**

- Gate 8

---

## 3.7 CORE_AUDIT_SUITE (Optional)

**Purpose**

Validate cross-run determinism and test integrity.

**Covers**

- Determinism across runs
- Optional serialization stability
- Order independence

**Gate Coverage**

- Gate 9

---

# 4. Shell-Level Suites (Phase 2+ Only)

Shell-level suites are forbidden in Phase 1.

They validate behavior outside the pure core.

---

## 4.1 RENDERING_SUITE

**Purpose**

Validate ASCII renderer correctness.

**Authority**

- ORACLE_SHELL_RENDERING

**Gate Coverage**

- Gate 10

---

## 4.2 RUNTIME_SCRIPTED_SUITE

**Purpose**

Validate deterministic virtual-time runtime orchestration.

**Authority**

- ORACLE_SHELL_RUNTIME

**Gate Coverage**

- Gate 11

---

## 4.3 CLI_SUITE

**Purpose**

Validate CLI delegation and exit semantics.

**Authority**

- ORACLE_SHELL_CLI

**Gate Coverage**

- Gate 12

---

## 4.4 REPLAY_SUITE

**Purpose**

Validate replay loading and deterministic execution.

**Authority**

- ORACLE_SHELL_REPLAY

**Gate Coverage**

- Gate 13

---

## 4.5 CONFIG_SUITE

**Purpose**

Validate configuration boundary enforcement and determinism.

**Authority**

- ORACLE_SHELL_CONFIG

**Gate Coverage**

- Gate 13 (if configuration is enabled)

---

# 5. Aggregate Suite Definitions

## 5.1 CORE_FULL_SUITE

Includes:

- CORE_BASE_SUITE
- CORE_GEOMETRY_SUITE
- CORE_EVOLUTION_SUITE
- CORE_INPUT_SEMANTICS_SUITE
- CORE_TERMINATION_SUITE

Optional if enabled:

- CORE_STRICTNESS_SUITE
- CORE_AUDIT_SUITE

Required for completion of Gates 0–6.

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
- SHELL_FULL_SUITE (Phase 2+ only)

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
| Gate 13 | REPLAY_SUITE (+ CONFIG_SUITE if enabled) |

All gates implicitly require all prior gates to pass.

---

# 7. Phase Restrictions

## Phase 0

Allowed:

- Documentation validation only.

No executable test suites permitted.

---

## Phase 1

Allowed:

- CORE_* suites only.

Forbidden:

- All shell-level suites.

---

## Phase 2

Allowed:

- CORE_* suites
- All shell suites

---

## Phase 3+

Allowed:

- All defined suites
- Any additional extension suites introduced under governance

---

# 8. Execution Modes

## 8.1 Fast Iteration Run

- CORE_BASE_SUITE
- CORE_GEOMETRY_SUITE

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

- Pass in isolated environments.
- Produce identical results across runs.
- Be order-independent.
- Not depend on ambient environment state.

Any determinism violation fails the entire suite.

---

# 10. Responsibility Boundaries

- `TEST_STRATEGY.md` defines correctness semantics.
- `TESTING_CONVENTIONS.md` defines encoding mechanics.
- `TEST_PLAN.md` defines execution grouping and sequencing.
- `@ACCEPTANCE_GATES` defines progression criteria.

This document must not duplicate oracle definitions or correctness policy.
