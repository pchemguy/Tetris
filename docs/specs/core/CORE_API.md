---
doc_id: CORE_API
name: CORE_API.md
title: Core API
status: active
authority: normative
description: Public Python API contract for interacting with the deterministic core.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [GAME_STATE, INPUT_MODEL, ERROR_HANDLING, SHAPES_AND_ROTATIONS]
---

# CORE API

**Tetris Core Python API Contract (Normative)**

## 1. Purpose

This document defines the **exact Python-level public API** for the Tetris **core** implementation.

The core must be:

- deterministic,
- UI-agnostic,
- test-friendly,
- strict about invariant violations.

If behavior is not defined here, it must not be invented.

---

## 2. Package and module placement

Source layout (per project layout contract):

- Python package root: `tetris/src/tetris/`
- Core module path: `tetris/src/tetris/core.py`

The core module must not import UI / rendering libraries.

---

## 3. Package-level API surface

### 3.1 Root-level import contract

The following **Core API symbols MUST be importable from the package root**:

```python
import tetris
```

The following symbols MUST be available as:

```python
from tetris import (
    CoreConfig,
    GameState,
    StepResult,
    InputEvent,
    TetrominoType,
    Rotation,
    new_game,
    step,
)
```

### 3.2 Export discipline

The package-root exports MUST obey the following rules:

* They MUST be **direct re-exports** of the corresponding `tetris.core` symbols.
* No wrappers.
* No renamed aliases.
* No alternate implementations.
* No conditional exports.

`tetris/__init__.py` MUST:

* Explicitly import the symbols from `tetris.core`
* Define `__all__`
* `__all__` MUST equal:

```python
[
    # Types
    "CoreConfig",
    "GameState",
    "StepResult",
    "InputEvent",
    "TetrominoType",
    "Rotation",

    # Functions
    "new_game",
    "step",
]
```

The order in `__all__` must match the order listed above.

### 3.3 Isolation requirement

Importing the root package:

```python
import tetris
```

MUST NOT:

* Import shell modules
* Initialize UI components
* Trigger rendering or side effects
* Initialize optional subsystems

The root package must expose only the deterministic core API.

This requirement ensures:

* shell/core decoupling,
* test isolation,
* forward compatibility for extended shells.

---

## 4. Public types

### 4.1 Enums

The module must define the following enums (names are binding):

- `TetrominoType(Enum)`
    - Members: `I, O, T, S, Z, J, L`
- `Rotation(Enum)`
    - Members: `R0, R90, R180, R270`
- `InputEvent(Enum)`
    - Members:
        - `MOVE_LEFT`
        - `MOVE_RIGHT`
        - `SOFT_DROP`
        - `HARD_DROP`
        - `ROTATE_CW`
        - `ROTATE_CCW`
        - `HOLD` (only if hold is enabled; if hold is not enabled, this member must not exist)

**Note**: If hold is optional at runtime, prefer keeping `HOLD` defined in the enum and gating its acceptance by configuration. If you do this, `HOLD` exists always, but `step()` must reject/raise according to configuration. If you choose to omit `HOLD`, you must also omit hold functionality entirely for MVP. The preferred approach is: include `HOLD` but allow disabling hold by config.

### 4.2 Dataclasses / structs

The module must define:

#### `CoreConfig`

A frozen configuration object for core behavior.

Required fields:

- `seed: int`
- `enable_hold: bool` (default false)
- `strict_input: bool` (default true)
- `strict_state: bool` (default true)

Semantics:

- `seed` initializes the RNG / 7-bag generator deterministically.
- `enable_hold` gates hold behavior.
- `strict_input` governs whether invalid input lists raise exceptions or are tolerated.
- `strict_state` governs whether invariant violations raise exceptions (must be true in tests).

#### `ActivePiece`

Defines the active tetromino.

Required fields:

- `type: TetrominoType`
- `rotation: Rotation`
- `origin_x: int`
- `origin_y: int`

#### `RngState`

A serializable representation of RNG/bag status.

Required fields:

- `seed: int`
- `bag: tuple[TetrominoType, ...]`  (remaining pieces in current bag, draw from front)
- `draw_count: int`  (monotonic count of draws; used for debugging/golden tests)

You may include additional fields if they are JSON-serializable and deterministic.

---

## 5. Game state object

### 5.1 `GameState`

The module must define a dataclass (or equivalent immutable struct) named `GameState`.

Required fields:

- `board: tuple[tuple[int, ...], ...]`
    - 20 rows, each 10 ints (0/1)
    - must be treated as immutable by consumers
- `active: ActivePiece`
- `next_piece: TetrominoType`
- `hold_piece: TetrominoType | None`
    - must exist even if hold disabled (always `None` if disabled)
- `hold_used_for_current_piece: bool`
- `score: int`
- `level: int`
- `lines_cleared_total: int`
- `tick_count: int`
- `gravity_counter: int`
- `rng: RngState`
- `is_game_over: bool`

### 5.2 Immutability requirement

`step()` must return a **new** `GameState` object (functional style).

Implementations may optimize internally, but externally observable behavior must be consistent with immutability:

- the returned state must not share mutable board structures with the input state.

---

## 6. Public functions

### 6.1 `new_game(config: CoreConfig) -> GameState`

Creates a new deterministic initial state.

Required behavior:

- Initializes:
    - empty 20×10 board
    - score = 0
    - level = 1
    - lines_cleared_total = 0
    - tick_count = 0
    - gravity_counter = 0
    - hold_piece = None
    - hold_used_for_current_piece = false
    - is_game_over = false
- Initializes RNG per `config.seed` and produces:
    - an initial `active` piece spawned at `(x=3, y=0)` with rotation `R0`
    - an initial `next_piece`

Spawn collision at game start:

- If spawn collides (should only happen if board not empty, which it is):
    - is_game_over must be set to true (defensive).

### 6.2 `step(state: GameState, inputs: tuple[InputEvent, ...], config: CoreConfig) -> StepResult`

Advances the simulation by one tick.

#### Required ordering

Must follow:

- `GAME_STATE.md` §5.2
- `INPUT_MODEL.md` §4

#### Input validation

- If `config.strict_input` is true:
    - unknown input values are errors (raise)
    - multiple HARD_DROP in one tick is an error (raise)
- If `enable_hold` is false and `HOLD` appears:
    - if strict_input: raise
    - else: reject with no effect

#### Game-over short circuit

If `state.is_game_over` is true:

- return state unchanged
- emit no events
- tick_count must not change

### 6.3 `blocks_for(active: ActivePiece) -> tuple[tuple[int, int], ...]`

Returns the **4 absolute board coordinates** occupied by the active piece.

Rules:

- Must use the enumerations in `SHAPES_AND_ROTATIONS.md`.
- Returns exactly 4 unique `(x, y)` pairs.
- Ordering:
    - ordering is not semantically important, but must be deterministic.
    - recommended: sorted lexicographically by `(y, x)`.

### 6.4 `gravity_ticks_per_cell(level: int) -> int`

Returns:

```
max(1, 20 - level)
```

Errors:

- If `level < 1`, raise `ValueError`.

### 6.5 Optional helpers (allowed)

The following helper functions are allowed but not required:

- `collides(board, blocks) -> bool`
- `apply_move(...)`
- `apply_rotation(...)`
- `lock_piece(...)`
- `clear_lines(...)`
- `draw_next_piece(rng_state) -> (piece, new_rng_state)`

If exposed publicly, they must be stable and documented. Prefer keeping helpers private.

---

## 7. StepResult and events

### 7.1 `Event`

If events are implemented, define a lightweight event record:

- `type: str`
- `data: dict[str, object]` (JSON-serializable)

Event types should match suggestions in [GAME_STATE.md](GAME_STATE.md) §7.

Events are recommended for tests and diagnostics, but not required for MVP.

### 7.2 `StepResult`

`step()` must return a `StepResult` object:

Fields:

- `state: GameState`
- `events: tuple[Event, ...]`

If events are not implemented, `events` must be an empty tuple.

---

## 8. Exceptions and strictness

### 8.1 Strict state validation

If `config.strict_state` is true:

- `new_game()` and `step()` must validate invariants (see [ERROR_HANDLING.md](ERROR_HANDLING.md))
- violations raise `ValueError` (preferred) or a custom `CoreInvariantError`

If strict_state is false:

- behavior is undefined; this mode is not required for MVP.

### 8.2 Custom exception types (optional)

Allowed custom exceptions:

- `CoreInputError(ValueError)`
- `CoreStateError(ValueError)`

If created, they must subclass `ValueError` for test simplicity.

---

## 9. Serialization contract (recommended)

The module should provide:

- `to_dict(state: GameState) -> dict`
- `from_dict(data: dict) -> GameState`

This is recommended for golden tests, but not required for MVP.

If implemented:

- output must be JSON-serializable
- stable field names
- deterministic ordering where applicable

---

## 10. Compatibility notes

- The core must run on Python 3.11+.
- No dependency on UI/toolkit libraries.
- Use only deterministic RNG behavior under `seed`.

---
