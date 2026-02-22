---
doc_id: ACCEPTANCE_GATES
name: ACCEPTANCE_GATES.md
title: Acceptance Gates
status: active
authority: normative
description: Ordered, testable implementation milestones and proof obligations.
---

# ACCEPTANCE GATES

Normative definition of ordered implementation milestones and proof obligations.

---

# 1. What Acceptance Gates Are

Acceptance gates define:

- the **ordered sequence of implementation milestones**,
- the **smallest testable deltas** that advance the system,
- the **mandatory proof obligations** required for progression.

A gate is satisfied only if:

1. Its defined implementation scope is complete, and
2. All required test oracles for that gate pass.

Gates are:

- cumulative,
- strictly ordered,
- minimal in scope,
- test-driven.

Gates do not define architecture (L2), behavior (L3), or proof semantics (L4).  
They reference those layers.

---

# 2. Organizational Model

## 2.1 Domains

Domains classify architectural scope.  
They are used by `PHASES.md`.

Domains:

- `DOC_INFRA`
- `CORE`
- `SHELL_BASELINE`
- `CORE_EXTENSIONS`
- `VARIANTS`
- `BENCHMARK`

Domains do not define order.  
Gate numbering defines order.

---

## 2.2 Gate Families

Families group gates by shared objective.

| Family | Name                                      | Primary Domain(s)        |
|--------|-------------------------------------------|--------------------------|
| G0     | Governance & Compliance                    | DOC_INFRA                |
| G1     | Core Structural Readiness                  | CORE                     |
| G2     | Core Behavioral Completion                 | CORE                     |
| G3     | Core Robustness & Extensions               | CORE, CORE_EXTENSIONS    |
| G4     | Shell Completion                           | SHELL_BASELINE           |
| G5     | Integration & System-Level Guarantees      | DOC_INFRA + CORE + SHELL_BASELINE |

Families are navigational.  
Only gate numbering defines order.

---

## 2.3 Oracle Usage Policy (Normative)

For every gate:

- Exactly **one primary oracle** must be declared.
- Additional oracles MAY be listed as **regression oracles**.
- Regression oracles must have been introduced in earlier gates.
- Gates must not introduce one-time-use oracles.

L4 defines oracle semantics.  
Gates reference oracle documents but do not interpret their internal structure.

---

# 3. Alignment with L2, L3, L4

- L2 defines structure and boundaries.
- L3 defines behavior.
- L4 defines proof obligations.
- Gates reference L3 for required behavior.
- Gates reference L4 for required proofs.

No behavior may be inferred from tests.  
No behavior may be inferred from implementation.

---

# G0 — Governance & Compliance

## Purpose

Establish deterministic repository discovery and governance compliance.

## Gate Table

| Gate | Name                             | Domain     | Primary Oracle |
|------|----------------------------------|------------|----------------|
| G0.1 | Repository & Contract Compliance | DOC_INFRA  | ORACLE_DOC_INFRA |

---

## G0.1 Repository & Contract Compliance

### Objective

The repository is machine-discoverable and contract-consistent.

### Mandatory Scope

- Documentation inventory generation succeeds.
- YAML metadata validates against schema.
- No duplicate DOC_ID.
- YAML `references` resolve.
- Repository layout matches structural constraints.
- Component boundaries per `DECOMPOSITION.md` are respected.

### Failure Conditions

- Missing required YAML.
- Duplicate DOC_ID.
- Broken reference graph.
- Structural boundary violation.

---

# G1 — Core Structural Readiness

## Purpose

Stabilize public core API and state model before behavioral implementation.

## Gate Table

| Gate | Name                  | Domain | Primary Oracle                |
|------|-----------------------|--------|-------------------------------|
| G1.1 | Core Skeleton & Types | CORE   | ORACLE_CORE_STRUCTURE |

---

## G1.1 Core Skeleton & Types

### Objective

Public API and state objects exist and conform to L3.

### Mandatory Scope

- Public types from `CORE_API.md` exist.
- `new_game()` returns valid `GameState`.
- `step()` exists with allowed stub semantics.
- No partial behavioral logic.

---

# G2 — Core Behavioral Completion

## Purpose

Implement full deterministic Tetris core (MVP semantics).

---

## G2 Gate Table

| Gate | Name                    | Primary Oracle                      | Regression Oracles |
|------|-------------------------|-------------------------------------|--------------------|
| G2.1 | Geometry & Collision    | ORACLE_CORE_GEOMETRY                | —                  |
| G2.2 | Gravity & Line Clearing | ORACLE_CORE_GRAVITY_AND_LOCKING     | ORACLE_CORE_GEOMETRY |
| G2.3 | Scoring & RNG           | ORACLE_CORE_SCORING                 | ORACLE_CORE_LINE_CLEAR |
| G2.4 | Input Semantics         | ORACLE_CORE_COLLISION               | ORACLE_CORE_GEOMETRY |
| G2.5 | Game Over               | ORACLE_CORE_GAME_OVER               | ORACLE_CORE_COLLISION |

---

## G2.1 Geometry & Collision

- Shapes exactly match `SHAPES_AND_ROTATIONS.md`.
- Collision rejects out-of-bounds and occupied cells.
- No procedural rotation.

---

## G2.2 Gravity & Line Clearing

- Gravity tick model correct.
- Locking on failure.
- Simultaneous line clearing.

---

## G2.3 Scoring & RNG

- Score table correct.
- Level increments every 10 lines.
- 7-bag RNG deterministic and seedable.

---

## G2.4 Input Semantics

- Inputs applied per `INPUT_MODEL.md`.
- Hard drop locks immediately.
- Rejections do not mutate state.

---

## G2.5 Game Over

- Spawn collision triggers game over.
- Locked piece at top triggers game over.
- `is_game_over` short-circuits further steps.

---

# G3 — Core Robustness & Extensions

## Purpose

Optional mechanics and strict invariant enforcement.

---

## G3 Gate Table

| Gate | Name                    | Domain            | Primary Oracle                | Regression |
|------|-------------------------|-------------------|-------------------------------|-----------|
| G3.1 | Hold Mechanics          | CORE_EXTENSIONS   | ORACLE_CORE_HOLD              | ORACLE_CORE_COLLISION |
| G3.2 | Invariants & Strictness | CORE              | ORACLE_CORE_INVARIANTS        | ORACLE_CORE_* |
| G3.3 | Determinism Audit       | CORE              | ORACLE_CORE_RNG_7BAG          | ORACLE_CORE_* |

---

# G4 — Shell Completion

## Purpose

Implement deterministic shell components without contaminating core.

---

## G4 Gate Table

| Gate | Name              | Primary Oracle              | Regression |
|------|-------------------|-----------------------------|-----------|
| G4.1 | ASCII Renderer    | ORACLE_SHELL_RENDERING      | ORACLE_CORE_* |
| G4.2 | Scripted Runtime  | ORACLE_SHELL_RUNTIME        | ORACLE_CORE_* |
| G4.3 | CLI               | ORACLE_SHELL_CLI            | ORACLE_SHELL_RUNTIME |
| G4.4 | Replay            | ORACLE_SHELL_REPLAY         | ORACLE_SHELL_RUNTIME |

---

## G4.1 ASCII Renderer

- Pure function.
- Exact rendering per `RENDERING_SPEC.md`.
- Snapshot deterministic.

---

## G4.2 Scripted Runtime

- One `step()` per tick.
- No wall-clock timing.
- Stops on game over.

---

## G4.3 CLI

- Commands match `CLI_SPEC.md`.
- Exit codes correct.
- No logic in CLI layer.

---

## G4.4 Replay

- Strict validation.
- Deterministic replay.
- No auto-correction of malformed input.

---

# G5 — Integration & System-Level Guarantees

## Purpose

Define cross-cutting acceptance compositions.

---

## G5 Gate Table

| Gate | Name                        | Domain     | Primary Oracle |
|------|-----------------------------|------------|----------------|
| G5.1 | Core MVP Acceptance         | DOC_INFRA  | ORACLE_CORE.md |
| G5.2 | Full System Acceptance      | DOC_INFRA  | ORACLE_SHELL_* + ORACLE_CORE_* |

---

## G5.1 Core MVP Acceptance

- G0–G2 gates satisfied.
- All required core oracles pass.

---

## G5.2 Full System Acceptance

- G0–G4 satisfied.
- All core and shell oracles pass.

---

# 6. Evaluation Principles

- Spec obedience is primary.
- Determinism is mandatory.
- Speculative behavior is failure.
- Missing rules must cause escalation, not guessing.