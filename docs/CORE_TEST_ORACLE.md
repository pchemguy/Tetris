---
name: CORE_TEST_ORACLE.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# CORE TEST ORACLE

**Tetris Core – Mandatory Test Oracles (Normative)**

## 1. Purpose

This document maps the rules in:

- [docs/GAME_RULES.md](GAME_RULES.md)
- [docs/GAME_STATE.md](GAME_STATE.md)

to **mandatory automated tests**.

It is a contract: an implementation is considered “correct” only if it satisfies these oracles.

This document applies **only to the pure core simulation** as defined by:

- `GAME_RULES.md`
- `GAME_STATE.md`
- `CORE_API.md`

It does **not** define test requirements for:

- rendering,
- runtime orchestration,
- CLI behavior,
- replay loading or execution.

Those concerns are governed by their respective specifications and acceptance gates (Gates 10–13 in `ACCEPTANCE_GATES.md`).

---

## 2. Test harness assumptions

Core tests operate on the **pure core** as defined in `DECOMPOSITION.md` (no runtime, rendering, CLI, or I/O).

The harness must be able to:

- construct a game state with a specific board + active piece,
- run `step(state, inputs)` deterministically,
- seed RNG / set RNG state,
- assert board contents and state fields.

Where necessary, tests should use **fixed board setups** rather than random play.

---

## 3. Board and coordinates

### ORACLE B1: Board bounds

- Given any state, after each step:
    - board dimensions remain 20×10.

### ORACLE B2: Collision rule (bounds)

- Any move that would place a block with:
    - x < 0 or x > 9, or y < 0 or y > 19
      must be rejected and leave state unchanged (except tick/gravity counters as defined).

### ORACLE B3: Collision rule (overlap)

- Any move that would overlap an occupied board cell must be rejected.

---

## 4. Spawn rules

### ORACLE S1: Spawn location and orientation

- After spawning, active piece origin must be `(3,0)` and rotation `R0`.

### ORACLE S2: Spawn collision -> game over

- If the spawn position collides with filled cells, `is_game_over` becomes true immediately.

### ORACLE S3: Next piece always defined

- After any spawn, `next_piece` is defined.

---

## 5. Movement

### ORACLE M1: Move left/right success

- With empty space, MOVE_LEFT decreases origin.x by 1.
- MOVE_RIGHT increases origin.x by 1.
- Active blocks update accordingly.

### ORACLE M2: Move rejection at walls

- Place piece adjacent to left wall so moving left would collide:
    - MOVE_LEFT is rejected.
- Similarly for right wall.

### ORACLE M3: Soft drop

- If space below is empty:
    - SOFT_DROP increases origin.y by 1.
- If blocked below:
    - SOFT_DROP is rejected (no lock solely due to soft drop; lock only via gravity tick failure or hard drop per GAME_STATE.md ordering).

---

## 6. Rotation

### ORACLE R1: Rotation in free space

- In empty field, ROTATE_CW and ROTATE_CCW produce the expected enumerated block sets.

### ORACLE R2: Basic wall kicks succeed at walls

- Put a piece at x such that in-place rotation would collide with wall but shifting by dx=+1 fixes it:
    - rotation must succeed with dx=+1.
- Mirror case for dx=-1.

### ORACLE R3: Rotation rejection when all attempts collide

- Create a configuration where in-place and ±1 shifts all collide:
    - rotation must be rejected and piece unchanged.

### ORACLE R4: O piece rotation invariance

- Rotating O must not change its occupied block set (rotation state may change or may be fixed; whichever is implemented must remain consistent and collision-free).

---

## 7. Gravity and ticking

### ORACLE G1: Gravity counter increments deterministically

- On each tick without lock:
    - gravity_counter increments by 1.
- When it reaches gravity_ticks_per_cell:
    - exactly one downward move is attempted and gravity_counter resets to 0.

### ORACLE G2: Gravity causes movement when possible

- With empty space below:
    - when gravity triggers, piece moves down exactly 1 cell.

### ORACLE G3: Gravity triggers lock when blocked

- With a filled cell directly below the active piece (or at bottom boundary):
    - when gravity triggers, downward move fails and piece locks immediately (same tick).

### ORACLE G4: Level affects gravity interval

- At level 1: `gravity_ticks_per_cell == 19`
- At level 20: `gravity_ticks_per_cell == 1`
- Verify the formula `max(1, 20 - level)` across at least 3 representative levels.

---

## 8. Locking

### ORACLE L1: Hard drop locks immediately

- HARD_DROP moves piece to the lowest valid y and locks it in the same tick.

### ORACLE L2: Hard drop distance correctness

- For a known empty column/landing space, HARD_DROP results in the exact expected y.

### ORACLE L3: Lock materializes blocks onto the board

- After lock, the 4 occupied active blocks become filled board cells.

### ORACLE L4: No lock delay

- If gravity triggers and downward movement is blocked:
    - lock occurs that tick with no additional grace ticks.

---

## 9. Line clearing

### ORACLE C1: Single-line clear

- Fill a row except for 4 cells where a piece will lock to complete the row.
- After lock:
    - exactly that row is cleared,
    - rows above shift down,
    - top row becomes empty.

### ORACLE C2: Multi-line clear (2, 3, 4)

- Construct deterministic setups for:
    - 2-line clear,
    - 3-line clear,
    - 4-line clear (Tetris).
- Verify:
    - cleared count matches,
    - simultaneous clearing occurs (no staged clear artifacts).

### ORACLE C3: Non-full rows remain

- If no rows are full after lock:
    - board remains unchanged except for newly locked blocks.

---

## 10. Scoring and levels

### ORACLE P1: Score increments per k lines cleared

- k=1: +100
- k=2: +300
- k=3: +500
- k=4: +800

### ORACLE P2: No extra scoring

- Verify that:
    - soft drop does not change score,
    - hard drop does not change score (unless you explicitly add such a rule; currently prohibited),
    - rotations/moves do not change score.

### ORACLE P3: Level increases per 10 total cleared lines

- Starting level is 1.
- After clearing 10 total lines across any number of locks:
    - level becomes 2.
- After 20 total lines:
    - level becomes 3.

---

## 11. Randomization (7-bag)

### ORACLE Q1: Bag completeness

- From a fresh bag draw 7 pieces:
    - set of pieces equals {I,O,T,S,Z,J,L} exactly once each.

### ORACLE Q2: Bag refill

- After drawing 7 pieces, the next draw must come from a new refilled bag.

### ORACLE Q3: Determinism with seed

- Using a fixed seed:
    - the first N pieces (recommend N=20) must be identical across runs.

---

## 12. Game over

### ORACLE O1: Spawn collision triggers game over

- Construct a board that blocks the spawn footprint:
    - spawning sets `is_game_over == true`.

### ORACLE O2: Top-row occupied after lock triggers game over

- Construct a scenario where a piece locks leaving any filled cell in y=0 (after clears):
    - game over triggers.

---

## 13. Hold (optional)

Only applicable if hold is implemented.

### ORACLE H1: First hold stores and spawns next

- If hold slot empty:
    - HOLD stores current piece in hold,
    - active becomes the previous next_piece,
    - a new next_piece is generated.

### ORACLE H2: Swap hold

- If hold slot occupied:
    - HOLD swaps active and hold.

### ORACLE H3: Once per piece

- After a successful HOLD:
    - second HOLD before locking must be rejected.

---

## 14. Meta-oracles (cross-cutting invariants)

### ORACLE X1: Post-step invariants always hold

After every step:

- board is valid,
- active piece is valid when not game over,
- counters remain in range,
- score/level non-negative and consistent.

### ORACLE X2: Rejected action does not mutate state

For each action type, construct a rejected scenario and verify:

- state (board, active piece, score, etc.) is unchanged,
- only tick/gravity counter behavior changes as specified by GAME_STATE.md ordering.

---

## 15. Minimum required test set (MVP gate)

An MVP core is accepted only if at least the following pass:

- B1, B2, B3
- S1, S2
- M1, M2, M3
- R1, R2, R3
- G1, G2, G3, G4
- L1, L3, L4
- C1, C2 (at least 2- and 4-line), C3
- P1, P3
- Q1, Q3
- O1
- X1

Shell-level gates (10–13) require their own tests, defined by their respective specifications, and are intentionally out of scope for this document.

---

## 16. Out-of-scope test oracles (non-core)

The following are intentionally excluded from this document:

- Rendering snapshot oracles (`RENDERING_SPEC.md`)
- Runtime execution oracles (`RUNTIME_SPEC.md`)
- CLI behavior oracles (`CLI_SPEC.md`)
- Replay determinism oracles (`REPLAY_SPEC.md`)

If formal test oracles are later introduced for these components, they must be defined in separate documents.
