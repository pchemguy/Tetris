---
name: GAME_STATE.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# GAME STATE

**Tetris Core State Model (Normative, Agent Target Spec)**

## 1. Purpose

This document defines the **authoritative core state model** and **step contract** for the Tetris implementation governed by [docs/GAME_RULES.md](GAME_RULES.md).

The goal is to make the game core:

- deterministic,
- testable without UI,
- suitable for agentic implementation with clear invariants.

Anything not defined here is undefined behavior and must not be invented.

---

## 2. Coordinate system and conventions

- Board coordinates: `(x, y)`
- `x` increases left→right, `y` increases top→bottom.
- Valid board cells: `x ∈ [0, 9]`, `y ∈ [0, 19]`.
- Cell occupancy is boolean: empty/filled.

A **block position** is always an absolute `(x, y)` on the board grid.

---

## 3. Core data types (logical)

### 3.1 Tetromino identifiers

`TetrominoType ∈ { I, O, T, S, Z, J, L }`

### 3.2 Rotation state

`Rotation ∈ { R0, R90, R180, R270 }`

### 3.3 Active piece

An active piece is defined by:

- `type: TetrominoType`
- `rotation: Rotation`
- `origin: (x: int, y: int)`  (piece-local origin in board coords)

The active piece occupies exactly 4 blocks:

- `blocks(active_piece) -> set[(x,y)]`
- Shapes must be explicitly enumerated (see GAME_RULES.md §3.2), and wall-kick attempts must follow [GAME_RULES.md](GAME_RULES.md) §4.2.

### 3.4 Board

`board[y][x] ∈ {0, 1}`

### 3.5 RNG

RNG state must be fully captured as part of game state so simulation is deterministic.

The piece generator must be a 7-bag randomizer:

- `bag: list[TetrominoType]` (remaining items in the current bag)
- `rng_state: ...` (implementation-defined but serializable for tests)
- `seed: int` (or equivalent seed material)

**Contract**: given identical initial RNG state + identical inputs, the produced piece sequence must match.

### 3.6 Scoring / progression

- `score: int >= 0`
- `level: int >= 1`
- `lines_cleared_total: int >= 0`

### 3.7 Hold / preview (optional)

Preview is required:

- `next_piece: TetrominoType` (exactly one)

Hold is optional; if implemented it must include:

- `hold_piece: TetrominoType | None`
- `hold_used_for_current_piece: bool`

See [GAME_RULES.md](GAME_RULES.md) §12.

### 3.8 Game status

- `is_game_over: bool`

---

## 4. Inputs and time

### 4.1 Input events

Core must accept a sequence (or set) of **discrete input events** per step:

- `MOVE_LEFT`
- `MOVE_RIGHT`
- `SOFT_DROP`
- `HARD_DROP`
- `ROTATE_CW`
- `ROTATE_CCW`
- `HOLD` (only if hold is enabled)

### 4.2 Time / ticking model

The core advances by **ticks**, not by wall-clock time.

A **tick** is one call to the step function.
Gravity is applied based on the rule:

```
gravity_ticks_per_cell = max(1, 20 - level)
```

The state must include:

- `tick_count: int >= 0` (monotonic)
- `gravity_counter: int in [0, gravity_ticks_per_cell - 1]`

**Gravity application rule**:
- On each tick, increment `gravity_counter` by 1.
- If `gravity_counter == gravity_ticks_per_cell`, attempt to move active piece down by 1:
    - if succeeds: reset `gravity_counter = 0`.
    - if fails: lock piece immediately (see §6), then reset `gravity_counter = 0`.

**Note**: This is a deterministic discretization of gravity suitable for tests.

---

## 5. Step function contract

### 5.1 Signature (logical)

`step(state, inputs) -> (new_state, events)`

Where:

- `inputs` is a list of input events for the current tick (ordered).
- `events` is a list of emitted events for UI/telemetry (defined in §7).

### 5.2 Ordering rules within a tick

Within one tick, processing order is:

1. If `state.is_game_over` is true: return state unchanged and emit no events.
2. Apply **inputs in given order**, each as an attempted action:
    - rejected actions have no effect.
3. Apply gravity according to §4.2.
4. If locking occurred due to gravity or hard drop:
    - perform line clear resolution (§6.3),
    - update score/level (§6.4),
    - spawn next piece (§6.5),
    - evaluate game over (§6.6).
5. Increment `tick_count` by 1.

**Hard drop rule**:

- A hard drop immediately moves the active piece to the lowest valid position and locks it in the same tick (before gravity application).
- After a hard drop lock, gravity step for that tick is skipped (since no active piece remains until respawn is complete).

---

## 6. State transitions (normative)

### 6.1 Collision predicate

`collides(board, blocks_set) -> bool`

A blocks set collides if any block:

- has x < 0 or x > 9
- has y < 0 or y > 19
- overlaps an occupied board cell

### 6.2 Movement actions

Movement actions attempt to adjust active piece origin:

- left: `origin.x -= 1`
- right: `origin.x += 1`
- soft drop: `origin.y += 1`

If resulting blocks collide, the move is rejected.

### 6.3 Rotation actions

Rotation changes active `rotation` and may apply basic wall-kicks:

Attempt order:

1. rotate in place
2. rotate + (dx=+1)
3. rotate + (dx=-1)

If all collide, rotation is rejected.

### 6.4 Locking

Lock occurs when:

- gravity attempts a downward move and it collides, OR
- hard drop executed.

Lock means:

- convert active piece blocks into occupied board cells
- emit a `PIECE_LOCKED` event
- then line clear and spawn processing occurs in the same tick

No lock delay.

### 6.5 Line clearing

After lock:

- detect all full rows (`10/10 occupied`)
- clear them simultaneously
- shift rows above down
- insert empty rows at top

### 6.6 Scoring and progression

Let `k` = number of cleared lines in that lock resolution.

Score increment:

- 1 -> +100
- 2 -> +300
- 3 -> +500
- 4 -> +800
- 0 -> +0

Update:

- `lines_cleared_total += k`
- `level = 1 + floor(lines_cleared_total / 10)`

### 6.7 Spawning

Spawning uses:

- `active_piece = next_piece` at `(x=3, y=0, rotation=R0)`
- generate a new `next_piece` by drawing from the 7-bag generator

If spawn collides: set `is_game_over = true` and emit `GAME_OVER`.

Additionally, if after lock the board has any filled cell at `y=0`, that also triggers game over (see [GAME_RULES.md](GAME_RULES.md) §11). (If you implement this, it should be checked after line clear resolution.)

### 6.8 Hold (optional)

If enabled:
- HOLD swaps active piece with `hold_piece`.
- First HOLD when `hold_piece is None` stores current piece and spawns `next_piece`.
- HOLD is allowed at most once per active piece:
    - guarded by `hold_used_for_current_piece`.
- After a successful hold:
    - set `hold_used_for_current_piece = true`.

---

## 7. Emitted events (for UI/tests)

Events are optional but strongly recommended for test clarity.

Suggested event types:

- `MOVE_REJECTED(action)`
- `ROTATION_REJECTED(direction)`
- `PIECE_MOVED(action)`
- `PIECE_ROTATED(direction, kick_dx)`
- `PIECE_HARD_DROPPED(drop_distance)`
- `PIECE_LOCKED`
- `LINES_CLEARED(k)`
- `SCORE_CHANGED(delta, new_score)`
- `LEVEL_CHANGED(old_level, new_level)`
- `PIECE_SPAWNED(type)`
- `GAME_OVER(reason)`

If events are implemented, they must be deterministic and reflect the actual transitions.

---

## 8. Invariants (must hold after every step)

- Board is 20×10 and contains only 0/1.
- If `is_game_over` is false:
    - active piece exists and occupies 4 blocks, all within bounds and not overlapping board cells.
- Score, level, lines are non-negative; level >= 1.
- Bag contains 0..7 items; when empty, it refills to 7 and shuffles.
- `next_piece` is always defined.
- `tick_count` increments exactly by 1 per step call.

---
