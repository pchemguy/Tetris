---
name: CORE_API.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
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

This API is binding for agentic implementation and for the test suite described in `docs/TEST_ORACLE.md`.

If behavior is not defined here, it must not be invented.

---

## 2. Package and module placement

Source layout (per project layout contract):

- Python package root: `tetris/src/tetris/`
- Core module path: `tetris/src/tetris/core.py`

The core module must not import UI / rendering libraries.

---

## 3. Public types

### 3.1 Enums

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

### 3.2 Dataclasses / structs

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

## 4. Game state object

### 4.1 `GameState`

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

### 4.2 Immutability requirement

`step()` must return a **new** `GameState` object (functional style).

Implementations may optimize internally, but externally observable behavior must be consistent with immutability:

- the returned state must not share mutable board structures with the input state.

---

## 5. Public functions

### 5.1 `new_game(config: CoreConfig) -> GameState`

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

### 5.2 `step(state: GameState, inputs: tuple[InputEvent, ...], config: CoreConfig) -> StepResult`

Advances the simulation by one tick.

#### Required ordering

Must follow:

- `docs/GAME_STATE.md` §5.2
- `docs/INPUT_MODEL.md` §4

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

### 5.3 `blocks_for(active: ActivePiece) -> tuple[tuple[int, int], ...]`

Returns the **4 absolute board coordinates** occupied by the active piece.

Rules:

- Must use the enumerations in `docs/SHAPES_AND_ROTATIONS.md`.
- Returns exactly 4 unique `(x, y)` pairs.
- Ordering:
    - ordering is not semantically important, but must be deterministic.
    - recommended: sorted lexicographically by `(y, x)`.

### 5.4 `gravity_ticks_per_cell(level: int) -> int`

Returns:

```
max(1, 20 - level)
```

Errors:

- If `level < 1`, raise `ValueError`.

### 5.5 Optional helpers (allowed)

The following helper functions are allowed but not required:

- `collides(board, blocks) -> bool`
- `apply_move(...)`
- `apply_rotation(...)`
- `lock_piece(...)`
- `clear_lines(...)`
- `draw_next_piece(rng_state) -> (piece, new_rng_state)`

If exposed publicly, they must be stable and documented. Prefer keeping helpers private.

---

## 6. StepResult and events

### 6.1 `Event`

If events are implemented, define a lightweight event record:

- `type: str`
- `data: dict[str, object]` (JSON-serializable)

Event types should match suggestions in [docs/GAME_STATE.md](GAME_STATE.md) §7.

Events are recommended for tests and diagnostics, but not required for MVP.

### 6.2 `StepResult`

`step()` must return a `StepResult` object:

Fields:

- `state: GameState`
- `events: tuple[Event, ...]`

If events are not implemented, `events` must be an empty tuple.

---

## 7. Exceptions and strictness

### 7.1 Strict state validation

If `config.strict_state` is true:

- `new_game()` and `step()` must validate invariants (see [docs/ERROR_HANDLING.md](ERROR_HANDLING.md))
- violations raise `ValueError` (preferred) or a custom `CoreInvariantError`

If strict_state is false:

- behavior is undefined; this mode is not required for MVP.

### 7.2 Custom exception types (optional)

Allowed custom exceptions:

- `CoreInputError(ValueError)`
- `CoreStateError(ValueError)`

If created, they must subclass `ValueError` for test simplicity.

---

## 8. Serialization contract (recommended)

The module should provide:

- `to_dict(state: GameState) -> dict`
- `from_dict(data: dict) -> GameState`

This is recommended for golden tests, but not required for MVP.

If implemented:

- output must be JSON-serializable
- stable field names
- deterministic ordering where applicable

---

## 9. Compatibility notes

- The core must run on Python 3.11+.
- No dependency on UI/toolkit libraries.
- Use only deterministic RNG behavior under `seed`.

---
