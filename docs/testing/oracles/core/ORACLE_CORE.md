---
doc_id: ORACLE_CORE
name: ORACLE_CORE.md
title: Core Oracle (Composite)
kind: testing
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Composite normative oracle defining mandatory correctness tests for the deterministic core simulation.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_RULES
  - GAME_STATE
  - INPUT_MODEL
  - ERROR_HANDLING
  - SHAPES_AND_ROTATIONS
  - CORE_API
  - CORE_ORACLE_INDEX
  - ORACLE_CORE_COLLISION
  - ORACLE_CORE_SPAWN
  - ORACLE_CORE_GEOMETRY
  - ORACLE_CORE_GRAVITY_AND_LOCKING
  - ORACLE_CORE_LINE_CLEAR
  - ORACLE_CORE_SCORING
  - ORACLE_CORE_RNG_7BAG
  - ORACLE_CORE_GAME_OVER
  - ORACLE_CORE_INVARIANTS
  - ORACLE_CORE_HOLD
---

# ORACLE_CORE

**Tetris Core – Composite Mandatory Test Oracle (Normative)**

---

## 1. Purpose

This document defines the **complete mandatory automated test obligations** for the deterministic core simulation.

It is binding for Acceptance Gates **1–6**.

An implementation of the core is considered correct only if:

1. All applicable modular core oracle documents pass, and  
2. All cross-cutting invariants defined here hold.

This document serves as the **composite umbrella oracle**.

It does not replace modular oracles; rather, it aggregates them.

---

## 2. Scope

This oracle applies exclusively to:

- The pure deterministic core (`core:core`)
- As defined by:
  - `GAME_RULES`
  - `GAME_STATE`
  - `INPUT_MODEL`
  - `ERROR_HANDLING`
  - `SHAPES_AND_ROTATIONS`
  - `CORE_API`

It explicitly excludes:

- Rendering
- Runtime orchestration
- CLI
- Replay loading/execution
- Shell integration

Those concerns are governed by shell-level testing documents.

---

## 3. Oracle decomposition model

The core oracle is decomposed into modular documents:

| Concern | Oracle Document |
|----------|----------------|
| Collision & rejection | `ORACLE_CORE_COLLISION` |
| Spawn semantics | `ORACLE_CORE_SPAWN` |
| Geometry & rotations | `ORACLE_CORE_GEOMETRY` |
| Gravity & locking | `ORACLE_CORE_GRAVITY_AND_LOCKING` |
| Line clearing | `ORACLE_CORE_LINE_CLEAR` |
| Scoring & level progression | `ORACLE_CORE_SCORING` |
| RNG (7-bag) | `ORACLE_CORE_RNG_7BAG` |
| Game over semantics | `ORACLE_CORE_GAME_OVER` |
| Hold mechanics | `ORACLE_CORE_HOLD` |
| Global invariants | `ORACLE_CORE_INVARIANTS` |

Each modular oracle defines its own precise obligations.

This document defines the **minimum composite gate obligations**.

Traceability between oracles and spec clauses is defined in `CORE_ORACLE_INDEX`.

---

## 4. Composite acceptance rule (Gates 1–6)

The core passes its acceptance gate only if:

- All required modular oracles pass.
- No invariant violation occurs.
- Determinism holds across seeded runs.
- No undefined behavior is introduced.
- No behavior outside `GAME_RULES` is implemented.

Failure in any single modular oracle constitutes core failure.

---

## 5. Determinism requirement

Given:

- identical initial `CoreConfig`
- identical seed
- identical ordered input sequences

The following must be identical across runs:

- piece sequence
- board states at every tick
- score progression
- level progression
- line clear behavior
- emitted events (if implemented)
- game over timing

Any divergence constitutes failure.

---

## 6. Minimum MVP test obligations

At minimum, the following oracle categories must pass for MVP:

- Collision enforcement
- Spawn correctness
- Movement rejection rules
- Rotation correctness
- Gravity interval behavior
- Immediate locking (no delay)
- Single and multi-line clear
- Score increments per rule
- Level increments per rule
- 7-bag completeness
- Determinism with seed
- Spawn-based game over
- Post-step invariants

Hold-related obligations apply only if hold is enabled.

---

## 7. Meta-oracle (cross-cutting invariants)

After every successful `step()` call:

- Board dimensions are exactly 20×10.
- Board cells contain only 0/1.
- Active piece (if not game over) occupies exactly 4 in-bounds cells.
- No overlap exists between active piece and board.
- Score ≥ 0.
- Level ≥ 1.
- `tick_count` increments exactly by 1 (unless game-over short-circuit).
- RNG state contains only valid tetrominoes.
- `next_piece` is always defined.

Invariant violations are errors (not rejections).

---

## 8. Rejection vs error semantics

The following are mandatory:

- Collision-based move/rotation failure → reject (no mutation beyond allowed counters).
- Unknown input event → error.
- Multiple HARD_DROP in one tick → error.
- Invalid state → error.
- Repeated HOLD in same tick → reject after first (unless strict override).

These semantics are binding and enforced by modular oracles.

---

## 9. Prohibited implementations

The following must not be implemented:

- T-spins
- Lock delay
- Floor kicks
- Combo scoring
- Ghost pieces
- Timing-dependent logic
- Non-deterministic RNG
- Procedural rotation inference

If present, core fails validation.

---

## 10. Relationship to modular oracles

This document does not duplicate detailed test cases.

Each modular oracle defines:

- exact testable behaviors,
- rejection semantics,
- invariants specific to its concern.

`ORACLE_CORE` defines:

- acceptance aggregation,
- cross-cutting invariants,
- determinism requirements,
- MVP gate minimum.

---

## 11. Enforcement rule for agents

Agents must treat:

- `GAME_RULES` as behavioral law,
- `GAME_STATE` as transition law,
- `CORE_API` as API law,
- `ERROR_HANDLING` as strictness law,
- Modular oracles as proof obligations.

If ambiguity is detected:

- Stop.
- Escalate.
- Do not guess.

---

## 12. Summary

`ORACLE_CORE` is the composite correctness contract for the pure deterministic core.

It aggregates modular core oracles into a single gate decision mechanism.

Passing unit tests is insufficient unless those tests trace back to the modular oracles and are validated by `CORE_ORACLE_INDEX`.

Core correctness is therefore:

**spec-complete, invariant-safe, deterministic, and modularly verified.**
