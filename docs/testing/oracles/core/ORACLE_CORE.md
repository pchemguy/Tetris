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
description: Composite normative oracle aggregating mandatory correctness obligations for the deterministic core simulation.
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

**Tetris Core — Composite Mandatory Test Oracle (Normative)**

## 1. Purpose

`ORACLE_CORE` defines the **composite proof obligation** for the pure deterministic core.

It is binding for Acceptance Gates **1–6**.

An implementation is considered correct for Gates 1–6 only if:

1. Every **required modular core oracle** passes, and
2. All **cross-cutting invariants** required by the core are continuously enforced, and
3. The core is **deterministic** under the determinism definition in this document.

This document does **not** replace modular oracles. It aggregates them into a single gate-level acceptance rule.

## 2. Scope boundary

This oracle applies exclusively to the pure core (`scope: core:core`) as defined by:

- `GAME_RULES`
- `GAME_STATE`
- `INPUT_MODEL`
- `ERROR_HANDLING`
- `SHAPES_AND_ROTATIONS`
- `CORE_API`

This oracle is intentionally **not applicable** to any shell concerns (rendering, runtime orchestration, CLI, replay, persistence). Those are governed by shell-level testing documents.

## 3. Modular decomposition

The core’s proof obligations are decomposed into focused oracle documents:

| Concern                     | Oracle Document                      |
| --------------------------- | ------------------------------------ |
| Collision & rejection       | `ORACLE_CORE_COLLISION.md`           |
| Spawn semantics             | `ORACLE_CORE_SPAWN.md`               |
| Geometry & rotations        | `ORACLE_CORE_GEOMETRY.md`            |
| Gravity & locking           | `ORACLE_CORE_GRAVITY_AND_LOCKING.md` |
| Line clearing               | `ORACLE_CORE_LINE_CLEAR.md`          |
| Scoring & level progression | `ORACLE_CORE_SCORING.md`             |
| RNG (7-bag)                 | `ORACLE_CORE_RNG_7BAG.md`            |
| Game over semantics         | `ORACLE_CORE_GAME_OVER.md`           |
| Hold mechanics              | `ORACLE_CORE_HOLD.md`                |
| Global invariants           | `ORACLE_CORE_INVARIANTS.md`          |

Each modular oracle defines its own concrete test obligations.

Traceability (oracle → spec clauses) and any conditional applicability are defined in:

- `CORE_ORACLE_INDEX.md`
- `CORE_ORACLE_INDEX.json` (machine-readable)
- `CORE_ORACLE_INDEX.schema.json` (validation)

## 4. Composite acceptance rule (Gates 1–6)

For Gates 1–6, the core is accepted only if:

- Every oracle listed as **required** by `CORE_ORACLE_INDEX` passes, and
- Determinism holds as defined in §5, and
- Global invariants hold as defined in §6.

If any single required modular oracle fails, the composite core oracle fails.

**Conditional obligations** (e.g. hold) apply only under the conditions declared in `CORE_ORACLE_INDEX`.

## 5. Dependencies and recommended verification order

This section defines **engineering dependencies** between oracle concerns. It does not change the normative rules of gameplay; it defines what must exist in the implementation to make specific oracle suites executable and meaningful. The dependency graph defined here is **normative for workflow semantics** and is **mirrored in machine-readable form** in:

- `CORE_ORACLE_INDEX.json`

The JSON artifact is the authoritative machine-checkable representation of this dependency graph. This Markdown section is the human-readable counterpart. If any dependency rule defined here changes, the corresponding JSON structure in `CORE_ORACLE_INDEX.json` MUST be updated in the same revision. Divergence between the two artifacts constitutes a documentation defect.

### Dependency model

Each modular oracle falls into one of two categories:

- **Foundational**: establishes primitives used by multiple other oracles.
- **Derived**: assumes foundational behavior exists and composes it.

A derived oracle may be executed before its prerequisites only if the missing prerequisites are stubbed in a way that still preserves determinism and does not introduce undefined behavior. In practice, prerequisites should be implemented first.

### Minimal dependency graph (normative for workflow)

The following dependency constraints apply:

- `ORACLE_CORE_GEOMETRY` is foundational for:
    - `ORACLE_CORE_COLLISION` (collision checks require block sets),
    - `ORACLE_CORE_SPAWN` (spawn validity requires geometry),
    - all movement/rotation behavior validated through collision.
- `ORACLE_CORE_COLLISION` is foundational for:
    - `ORACLE_CORE_GRAVITY_AND_LOCKING` (gravity step attempts and lock trigger),
    - `ORACLE_CORE_LINE_CLEAR` (lock must materialize blocks correctly),
    - `ORACLE_CORE_GAME_OVER` (spawn collision and blocked movement semantics).
- `ORACLE_CORE_SPAWN` is foundational for:
    - `ORACLE_CORE_RNG_7BAG` (spawn consumes piece generation),
    - `ORACLE_CORE_GAME_OVER` (spawn collision is a game-over condition),
    - most end-to-end tick evolution tests.
- `ORACLE_CORE_GRAVITY_AND_LOCKING` is foundational for:
    - `ORACLE_CORE_LINE_CLEAR` (line clear occurs after lock),
    - `ORACLE_CORE_SCORING` (scoring depends on cleared line count),
    - `ORACLE_CORE_GAME_OVER` (top-row occupancy checks occur after lock/clear).
- `ORACLE_CORE_LINE_CLEAR` is foundational for:
    - `ORACLE_CORE_SCORING` (score delta depends on k cleared lines),
    - `ORACLE_CORE_GAME_OVER` (post-clear top-row rule where applicable).
- `ORACLE_CORE_RNG_7BAG` is foundational for:
    - any oracle that asserts determinism of piece sequences across multiple spawns.
- `ORACLE_CORE_INVARIANTS` is cross-cutting:
    - it may be executed at any time,
    - but it becomes maximally informative only once the above behaviors exist.
- `ORACLE_CORE_HOLD` is conditional:
    - it applies only when hold is enabled (per `CORE_ORACLE_INDEX` conditions),
    - it depends on `ORACLE_CORE_SPAWN` and `ORACLE_CORE_RNG_7BAG` (because hold interacts with next/active piece sequencing).

### Recommended shortest-feedback implementation order (non-normative)

This is a recommended sequence that minimizes false failures and maximizes early signal. It is guidance only; compliance is determined solely by oracle pass/fail.

1. `ORACLE_CORE_GEOMETRY`
2. `ORACLE_CORE_COLLISION`
3. `ORACLE_CORE_SPAWN`
4. `ORACLE_CORE_GRAVITY_AND_LOCKING`
5. `ORACLE_CORE_LINE_CLEAR`
6. `ORACLE_CORE_SCORING`
7. `ORACLE_CORE_RNG_7BAG`
8. `ORACLE_CORE_GAME_OVER`
9. `ORACLE_CORE_INVARIANTS`
10. `ORACLE_CORE_HOLD` (only if enabled)

If work is scoped to a specific gate, follow the gate’s required oracle subset from `CORE_ORACLE_INDEX` and preserve prerequisite order within that subset.

## 6. Determinism requirement

Given:

- identical initial `CoreConfig`,
- identical seed material,
- identical ordered per-tick input sequences,

the core must produce identical results across runs.

At minimum, the following must be identical across runs:

- piece sequence,
- board and state evolution at each tick,
- score / level / lines cleared progression,
- game-over timing.

If the core emits events (`StepResult.events`), event sequences must also be deterministic.

Any divergence is a correctness failure.

## 7. Composite meta-oracle: invariants (cross-cutting)

After every successful `step()` call, the core must satisfy the invariants enforced by:

- `ORACLE_CORE_INVARIANTS.md`

At minimum, this includes (non-exhaustive summary):

- board shape and cell domain constraints,
- active-piece validity when not game over,
- non-negative score / line counters and level >= 1,
- tick-count progression semantics,
- RNG/bag validity,
- `next_piece` definedness.

**Important**: the normative, complete invariant list is defined in `ORACLE_CORE_INVARIANTS.md`. This section exists only to assert that invariants are part of the composite acceptance rule.

## 8. Rejection vs error policy (composite binding)

Rejection vs error semantics are defined by:

- `ERROR_HANDLING`
- and validated through the relevant modular oracles.

This document asserts the composite requirement:

- A core implementation that “passes tests” but violates `ERROR_HANDLING` is non-compliant, and fails this composite oracle.

## 9. Minimum obligations for Gate completion

Gates 1–6 require, at minimum, coverage of these categories:

- collision and rejection behavior,
- spawn correctness,
- geometry and rotation correctness,
- gravity interval behavior and locking,
- single- and multi-line clearing,
- scoring and level progression,
- 7-bag correctness and seed determinism,
- game-over conditions,
- cross-cutting invariants.

Hold obligations apply only if enabled, per `CORE_ORACLE_INDEX`.

## 10. Relationship to specifications and modular oracles

- Specifications (`GAME_RULES`, `GAME_STATE`, etc.) define *what the core must do*.
- Modular oracles define *what must be proven by tests* for each concern.
- `CORE_ORACLE_INDEX` defines *traceability* and (optionally) an explicit implementation / verification sequence.
- `ORACLE_CORE` defines *how the modular oracles combine* into a single acceptance decision for Gates 1–6.

## 11. Agent enforcement rule

If an ambiguity, omission, or conflict is detected in authoritative documents:

- Stop.
- Escalate.
- Do not guess.

`ORACLE_CORE` is an acceptance aggregator. It does not authorize inventing behavior.
