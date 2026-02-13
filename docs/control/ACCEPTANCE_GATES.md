---
doc_id: ACCEPTANCE_GATES
name: ACCEPTANCE_GATES.md
title: Milestone Acceptance Gates
kind: control
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Milestone-based acceptance criteria and progression rules.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - 
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

Each acceptance gate may reference one or more **test oracle documents**. A gate is considered satisfied only if all mandatory criteria for that gate **and** all corresponding test oracles pass.

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
- Agent must identify which test oracle(s) apply to the current target gate.
- Agent must identify the current repository phase and confirm that the target gate is permitted in that phase.
- All normative docs are discovered and referenced (at minimum by name in the plan/review notes).

**Core / engine contracts**

- `GAME_RULES.md`
- `GAME_STATE.md`
- `INPUT_MODEL.md`
- `ERROR_HANDLING.md`
- `SHAPES_AND_ROTATIONS.md`
- `CORE_API.md`
- `CORE_TEST_ORACLE.md`
- `ACCEPTANCE_GATES.md`

**System-level contracts**

- `DECOMPOSITION.md`
- `ARCHITECTURE.md`

**Shell contracts**

- `RUNTIME_SPEC.md`
- `RENDERING_SPEC.md`
- `CLI_SPEC.md`
- `REPLAY_SPEC.md`

- No contradictions between implementation and docs.
- Component boundaries are respected per `DECOMPOSITION.md` (e.g., no game logic in renderer/CLI).
- **Agent must explicitly state the current target gate** and confirm scope limitations (core vs shell) before editing code.

### Automatic failure conditions

- Implementing behavior not specified in docs.
- Guessing missing rules instead of stopping and escalating.
- Violating component boundaries (logic leakage across core/runtime/input/render/CLI).
- Implementing shell features (runtime/renderer/CLI/replay) **without** the corresponding spec being present and acknowledged.
- Creating/modifying shell modules (`tetris.rendering`, `tetris.runtime`, `tetris.cli`, replay/persistence) while working on core-only gates (1–6) fails unless explicitly required by the current gate.

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

### Core test oracle

Correctness for Gates 1–6 is governed by:

- `CORE_TEST_ORACLE.md`

Only the oracles explicitly listed for MVP are required unless a later gate explicitly expands the required set.

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

## 13. Gate 10 — ASCII renderer

### Objective

Implement a minimal, deterministic presentation layer that renders `GameState` for inspection, debugging, and evaluation, without contaminating core logic.

### Mandatory criteria

- An ASCII renderer is implemented with the interface:
  `render(state: GameState) -> str`
- Rendering behavior matches `RENDERING_SPEC.md` **exactly**, including:
- board dimensions and borders,
- cell symbols,
- metadata lines (score, level, lines, next, hold),
- game-over rendering.
- Renderer is a pure function:
- no mutation of `GameState`,
- no I/O,
- no timing logic.

### Required tests

- Snapshot (golden) tests for at least the following states:
- empty initial state,
- representative mid-game state with an active piece,
- game-over state.
- Snapshot comparisons must be byte-for-byte deterministic.

### Prohibited behavior

- Animations or timing-dependent output.
- Conditional rendering based on environment.
- Implementing game logic inside the renderer.

### Test oracle

Gate 10 correctness is governed by:

- `RENDERING_TEST_ORACLE.md`

All mandatory oracles in that document must pass.

---

## 14. Gate 11 — Scripted runtime (virtual-time)

### Objective

Provide a deterministic runtime capable of executing the game in **virtual time**, suitable for tests, evaluation, and replay.

### Mandatory criteria

- A scripted runtime exists that:
- advances the game by discrete ticks,
- does not call `sleep` or depend on wall-clock time.
- Inputs are supplied as explicit per-tick input lists.
- For each tick:
- inputs are collected,
- `step(state, inputs, config)` is called exactly once,
- the resulting state is rendered.
- Runtime terminates immediately when `state.is_game_over` becomes true.

### Required tests

- A test that runs a fixed number of ticks with scripted inputs and asserts:
- deterministic final state,
- correct tick count progression.
- A test that confirms early termination on game over.

### Prohibited behavior

- Re-implementing game rules or gravity logic in the runtime.
- Calling `step()` multiple times per tick.
- Modifying `GameState` outside the core.

### Test oracle

Gate 11 correctness is governed by:

- `RUNTIME_TEST_ORACLE.md`

All mandatory oracles in that document must pass.

---

## 15. Gate 12 — Command-line interface (CLI)

### Objective

Expose a minimal command-line interface that allows humans and evaluation harnesses to run the application without embedding logic in the CLI layer.

### Mandatory criteria

- CLI supports the following commands exactly as specified in `CLI_SPEC.md`:
- `run`
- `script`
- `replay`
- CLI flags and options match the specification.
- Exit codes match the specification.
- CLI delegates execution to runtime and core without altering behavior.

### Required tests

- CLI invocation tests for each command that assert:
- correct exit code on normal termination,
- correct exit code on invalid usage,
- propagation of core/runtime errors.

### Prohibited behavior

- Suppressing or catching core invariant violations.
- Implementing game logic in argument parsing.
- Silent fallback behavior on invalid input.

### Test oracle

Gate 12 correctness is governed by:

- `CLI_TEST_ORACLE.md`

All mandatory oracles in that document must pass.

---

## 16. Gate 13 — Replay and deterministic evaluation

### Objective

Enable exact reproduction of game runs for auditing, regression testing, and agent evaluation.

### Mandatory criteria

- Replay files are loaded and validated per `REPLAY_SPEC.md`.
- Replay execution:
- initializes the core with the replay seed,
- applies exactly one input list per tick,
- uses the scripted runtime (virtual-time).
- Replay validation is strict:
- unknown input events are errors,
- malformed structure is rejected.
- Given identical replay files and implementation:
- final `GameState` is deterministic and identical.

### Required tests

- A test that replays a valid replay file and asserts final state.
- A test that rejects malformed replay files.
- A determinism test:
- same replay run twice yields identical final state.

### Prohibited behavior

- Ignoring invalid replay inputs.
- Auto-correcting malformed replay data.
- Introducing nondeterminism during replay execution.

### Test oracle

Gate 13 correctness is governed by:

- `REPLAY_TEST_ORACLE.md`

All mandatory oracles in that document must pass.

---

## 17. Final acceptance (MVP complete)

The project is considered **MVP-complete (core-only)** when:

- Gates **0–6** are fully satisfied, and
- No prohibited behaviors exist for those gates, and
- All required tests for Gates 0–6 pass.
- For MVP acceptance, only `CORE_TEST_ORACLE.md` applies; shell-level test oracles (`*_TEST_ORACLE.md`) are explicitly out of scope.

### Notes

- Gates **7–9** (hold mechanics, strictness hardening, auditability) are **core extensions**:
    - strongly recommended,
    - not required for MVP unless explicitly requested.
- Gates **10–13** (renderer, runtime, CLI, replay) define **system/shell completeness**:
    - explicitly **out of scope for MVP**,
    - required only when progressing beyond a core-only benchmark.
- Passing MVP does **not** imply the presence of:
    - rendering,
    - runtime loop,
    - CLI,
    - replay capability.

MVP acceptance certifies the correctness, determinism, and testability of the **pure core simulation**, independent of presentation or execution environment.

---

## 18. Agent evaluation rubric (meta)

Agent performance is evaluated on:

- **Spec obedience** (primary)
- **Determinism**
- **Correct escalation when blocked**
- **Test completeness**
- **Absence of speculative behavior**

Passing all gates with minimal supervision is considered a successful demonstration of agentic software development prompting.

---


