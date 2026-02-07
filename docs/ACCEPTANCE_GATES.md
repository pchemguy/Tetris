---
name: ACCEPTANCE_GATES.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# ACCEPTANCE GATES

**Milestone Acceptance Gates for Agentic Development**

## 1. Purpose

This document defines **explicit acceptance gates** for the Tetris reference project.

Acceptance gates:

- constrain agent scope,
- prevent premature feature creep,
- provide objective “done / not done” criteria,
- enable automated or human-in-the-loop evaluation of agent behavior.

An agent may not advance to a later gate unless **all criteria** of the current gate are satisfied.

---

## 2. Gate philosophy

- Gates are **cumulative**: each gate subsumes all prior gates.
- Failing any criterion fails the gate.
- “Almost correct” does not pass.
- Behavior not explicitly required is not credited.
- Behavior explicitly prohibited fails the gate.

---

## 3. Gate 0 — Repository & contract compliance

### Objective

Ensure the agent correctly discovers and obeys:

- repository layout constraints,
- the full normative specification set,
- component boundaries and staging rules.

### Mandatory criteria

- Source code placed under:
  `tetris/src/tetris/`
- No source files outside the package path.
- All normative docs are discovered and referenced (at minimum by name in the plan/review notes).

**Core / engine contracts**

- `GAME_RULES.md`
- `GAME_STATE.md`
- `INPUT_MODEL.md`
- `ERROR_HANDLING.md`
- `SHAPES_AND_ROTATIONS.md`
- `CORE_API.md`
- `TEST_ORACLE.md`
- `ACCEPTANCE_GATES.md`

**System-level contracts**

- `DECOMPOSITION.md`
- `ARCHITECTURE.md`

**Shell contracts (only applicable when implementing shell components)**

- `RUNTIME_SPEC.md`
- `RENDERING_SPEC.md`
- `CLI_SPEC.md`
- `REPLAY_SPEC.md`

- No contradictions between implementation and docs.
- Component boundaries are respected per `DECOMPOSITION.md` (e.g., no game logic in renderer/CLI).

### Automatic failure conditions

- Implementing behavior not specified in docs.
- Guessing missing rules instead of stopping and escalating.
- Violating component boundaries (logic leakage across core/runtime/input/render/CLI).
- Implementing shell features (runtime/renderer/CLI/replay) **without** the corresponding spec being present and acknowledged.

### Notes

- Gate 0 does **not** forbid UI/runtime work in general; it forbids doing so **prematurely** or without the relevant shell specs.
- When working on core-only gates (1–6), runtime/renderer/CLI must not be introduced unless a gate explicitly calls for it.

---

## 4. Gate 1 — Core skeleton & types

### Objective

Establish the Python-level core API without full logic.

### Mandatory criteria

- `core.py` exists at `tetris/src/tetris/core.py`.
- All public types defined in `CORE_API.md` exist:
- enums,
- dataclasses,
- configuration object.
- `new_game()` returns a structurally valid `GameState`.
- `step()` exists and returns a `StepResult`.

### Allowed behavior

- `step()` may be a stub that:
- increments `tick_count`,
- returns unchanged state,
- emits no events.

### Prohibited behavior

- Partial implementations of movement/rotation.
- Silent failures instead of exceptions.

---

## 5. Gate 2 — Deterministic geometry & collision

### Objective

Prove that geometry and collision logic is correct and spec-compliant.

### Mandatory criteria

- `blocks_for(active)` returns exact shapes from `SHAPES_AND_ROTATIONS.md`.
- All rotations enumerated correctly.
- Collision detection respects board bounds and filled cells.
- Movement rejection on collision is correct.

### Required tests

- Geometry tests for all pieces and rotations.
- Collision-at-wall tests.
- Collision-with-filled-cell tests.

### Prohibited behavior

- Procedural rotation or inferred geometry.
- Dynamic normalization of shapes.

---

## 6. Gate 3 — Gravity, locking, and line clearing

### Objective

Implement core time evolution and structural board changes.

### Mandatory criteria

- Gravity obeys `gravity_ticks_per_cell(level)`.
- Locking occurs immediately on gravity failure or hard drop.
- Line clearing:
- detects full rows,
- clears simultaneously,
- shifts rows correctly.

### Required tests

- Gravity counter progression tests.
- Lock-on-blocked-gravity tests.
- Single- and multi-line clear tests.

---

## 7. Gate 4 — Scoring, levels, and RNG

### Objective

Ensure scoring and progression are correct and deterministic.

### Mandatory criteria

- Scoring matches table in `GAME_RULES.md`.
- Level increases every 10 total cleared lines.
- Gravity speed scales with level.
- RNG uses strict 7-bag randomization.
- RNG is seedable and deterministic.

### Required tests

- Score-per-clear-count tests.
- Level progression tests.
- Bag completeness and refill tests.
- Deterministic piece sequence tests with fixed seed.

---

## 8. Gate 5 — Inputs, rotation, and hard drop

### Objective

Implement full player interaction semantics.

### Mandatory criteria

- All input events handled per `INPUT_MODEL.md`.
- Rotation obeys wall-kick rules.
- Rejected actions do not mutate state.
- Hard drop:
- drops to correct height,
- locks immediately,
- skips gravity for that tick.

### Required tests

- Rotation success/rejection tests.
- Hard drop distance and lock tests.
- Rejection immutability tests.

---

## 9. Gate 6 — Game over semantics

### Objective

Ensure correct termination behavior.

### Mandatory criteria

- Game over on spawn collision.
- Game over when locked piece occupies row `y=0`.
- `is_game_over` short-circuits future steps.

### Required tests

- Spawn-blocked game over tests.
- Top-row occupation game over tests.
- No-state-change-after-game-over tests.

---

## 10. Gate 7 — Hold & preview (optional)

### Objective

Validate optional mechanics without affecting core correctness.

### Mandatory criteria (if enabled)

- One-piece preview always available.
- Hold behavior matches `GAME_RULES.md`.
- Hold usable once per active piece.

### Required tests

- First hold store test.
- Hold swap test.
- Hold reuse rejection test.

---

## 11. Gate 8 — Invariants & strictness

### Objective

Ensure robustness and correctness under strict evaluation.

### Mandatory criteria

- All invariants in `ERROR_HANDLING.md` are enforced.
- Invalid inputs raise errors in strict mode.
- Invalid states raise errors.
- Multiple `HARD_DROP` in a tick raises an error.

### Required tests

- Invalid input tests.
- Invariant violation tests.
- Strict-mode exception tests.

---

## 12. Gate 9 — Regression & auditability

### Objective

Ensure the system is testable, auditable, and reproducible.

### Mandatory criteria

- Test suite passes in clean environment.
- No test order dependence.
- Deterministic results across runs.
- Optional:
- state serialization produces stable output,
- event logs match state transitions.

---

## 13. Final acceptance (MVP complete)

The project is considered **MVP-complete** when:

- Gates 0–6 are fully satisfied, and
- No prohibited behaviors exist, and
- All required tests pass.

Gates 7–9 are strongly recommended but not required for MVP unless explicitly requested.

---

## 14. Agent evaluation rubric (meta)

Agent performance is evaluated on:

- **Spec obedience** (primary)
- **Determinism**
- **Correct escalation when blocked**
- **Test completeness**
- **Absence of speculative behavior**

Passing all gates with minimal supervision is considered a successful demonstration of agentic
software development prompting.

---


