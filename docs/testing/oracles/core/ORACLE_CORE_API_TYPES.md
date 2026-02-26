---
doc_id: ORACLE_CORE_API_TYPES
name: ORACLE_CORE_API_TYPES.md
title: Core API Surface and Type Contract Test Oracles
status: active
authority: normative
description: Mandatory test oracles ensuring `tetris.core` and package-root re-exports match the `@CORE_API` contract (symbols, types, signatures, and import-time isolation) without implementing gameplay semantics.
references:
  - TEST_ORACLE_FORMAT_CONVENTION
  - CORE_API
  - GAME_STATE
  - ERROR_HANDLING
---

# ORACLE_CORE_API_TYPES

**Core — API Surface and Type Contract Test Oracles (Normative)**

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* the existence and importability of `tetris.core`,
* the exact presence of all required public symbols (names, enum members, dataclass names, function names),
* package-root re-export discipline (`from tetris import ...`),
* signature compliance for `new_game()` and `step()`,
* structural (not behavioral) correctness of `new_game()` and `step()` return shapes,
* explicit absence of gameplay semantics at this stage.

## 2. Harness assumptions

The test harness must be able to:

* import `tetris` and `tetris.core`,
* introspect exported attributes and `__all__`,
* detect enum membership and dataclass fields,
* call `new_game(config)` and `step(state, inputs, config)` with deterministic dummy inputs,
* validate "structural validity" of returned objects (types and required fields),
* assert that forbidden semantic effects do not occur (e.g., board changes, movement, RNG draws) under this stage’s stub policy.

## 3. Oracle set

### ORACLE API10: Core module is importable

Action/When:

* `import tetris.core`

Assert/Then:

* import MUST succeed.

### ORACLE API11: Required public symbols exist in `tetris.core`

Action/When:

* `import tetris.core as core`

Assert/Then:

* `core` MUST define all symbols required by `@CORE_API`, including at minimum:

  * Enums: `TetrominoType`, `Rotation`, `InputEvent`
  * Dataclasses/structs: `CoreConfig`, `ActivePiece`, `RngState`, `GameState`, `StepResult`
  * Functions: `new_game`, `step`, `blocks_for`, `gravity_ticks_per_cell`

And:

* each enum MUST contain the required members specified by `@CORE_API`.
* each dataclass/struct MUST contain the required fields specified by `@CORE_API`.

### ORACLE API12: Package-root re-export contract

Action/When:

* `import tetris`

Assert/Then:

* all symbols listed in `@CORE_API` §3.1 MUST be importable from the package root via:

  * `from tetris import CoreConfig, GameState, StepResult, InputEvent, TetrominoType, Rotation, new_game, step`

Export discipline:

* `tetris.__all__` MUST exist.
* `tetris.__all__` MUST items specified in `@CORE_API` §3.2.
* The package-root exports MUST be direct re-exports of the corresponding `tetris.core` symbols:
    * `tetris.CoreConfig is tetris.core.CoreConfig` (and similarly for each required symbol),
    * no wrappers, aliases-under-different-names, or conditional exports.

### ORACLE API13: Import-time isolation (no implicit shell import)

Action/When:

* In a fresh Python process (or after clearing `sys.modules` of any `tetris*` entries), execute:
    - `import tetris`
    - `import tetris.core`

Assert/Then:

* Neither import MUST implicitly import shell component packages.

Operationally, after `import tetris` and again after `import tetris.core`:

* `sys.modules` MUST NOT contain any of:
    - `"tetris.runtime"`
    - `"tetris.rendering"`
    - `"tetris.cli"`
    - `"tetris.persistence"`
    - `"tetris.input"`
    - `"tetris.presentation"`
    - `"tetris.telemetry"`

Optional (allowed as an additional check, not a substitute):

* Importing those modules MAY be asserted to fail with `ModuleNotFoundError` at this stage.

### ORACLE API14: Signature compliance for core entrypoints

Assert/Then:

* `new_game` MUST have signature: `new_game(config: CoreConfig) -> GameState`
* `step` MUST have signature:
  `step(state: GameState, inputs: tuple[InputEvent, ...], config: CoreConfig) -> StepResult`

Tests MAY accept equivalent typing spellings, but MUST reject incompatible arity or parameter order.

### ORACLE API15: Structural validity of `new_game()`

Construct/Given:

* `config = CoreConfig(...)` with a valid seed and defaults per `@CORE_API`.

Action/When:

* `state = new_game(config)`

Assert/Then:

* `state` MUST be a `GameState`.
* `state` MUST have all required fields from `@CORE_API` §5.1.
* `state.board` MUST be a `tuple` of length 20, each row a `tuple` of length 10.
* All board cell values MUST be integers (representation constraints beyond structural typing may be asserted later).
* `state.is_game_over` MUST be a boolean.
* `state.rng` MUST be an `RngState`.

This oracle is structural: it asserts field existence and basic shape, not gameplay semantics.

### ORACLE API16: Structural validity of `step()` return shape

Construct/Given:

* `state0 = new_game(config)`
* `inputs = tuple()` (empty)

Action/When:

* `result = step(state0, inputs, config)`

Assert/Then:

* `result` MUST be a `StepResult`.
* `result.state` MUST be a `GameState`.
* `result.events` MUST be a `tuple` (may be empty).

### ORACLE API17: Stub policy (no gameplay semantics)

This oracle enforces the "structure-only" constraint.

Construct/Given:

* `state0 = new_game(config)`
* `inputs = (InputEvent.MOVE_LEFT,)` and similarly for at least:
  `MOVE_RIGHT`, `SOFT_DROP`, `HARD_DROP`, `ROTATE_CW`, `ROTATE_CCW`
  (and `HOLD` if the enum member exists per your chosen `@CORE_API` strategy).

Action/When:

* `result = step(state0, inputs, config)`
* `state1 = result.state`

Assert/Then:

* No gameplay mechanics MUST be implemented. At minimum:
    * `state1.board` MUST equal `state0.board`
    * `state1.active` MUST equal `state0.active` (no movement/rotation)
    * `state1.score`, `state1.level`, `state1.lines_cleared_total` MUST equal the originals
    * `state1.is_game_over` MUST remain unchanged
    * `state1.next_piece` and `state1.rng` MUST remain unchanged

Counters:

* If `@CORE_API` requires `tick_count` and/or `gravity_counter` fields to exist, then **either** of the following is acceptable at this stage:
    * counters remain unchanged (preferred), **or**
    * counters change only in a deterministic, explicitly documented way.

If counters are permitted to change, the exact allowance MUST be encoded in text and reflected in this oracle by tightening this clause to a single permitted rule.

> This oracle intentionally prevents "partial implementation" (e.g., movement without collision).

## 4. Forbidden behavior

The following are prohibited for the scope governed by this oracle:

* implementing any gameplay semantics (movement, rotation, gravity, collision, locking, line clear, scoring, RNG draw, game-over transitions),
* introducing shell modules/packages,
* weakening the `@CORE_API` export discipline (wrappers, aliases, conditional exports),
* silent suppression of structural errors that are in-scope for this stage under `@ERROR_HANDLING`.

## 5. Minimum required test set

For compliance, the minimum required set is:

* API10, API11, API12, API13, API14, API15, API16, API17

### Notes for implementers and test authors (non-normative)

* API17 should be table-driven: iterate over representative input events and assert invariance.
