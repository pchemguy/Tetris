---
doc_id: ORACLE_CORE_COLLISION
name: ORACLE_CORE_COLLISION.md
title: Core Collision and Rejection Test Oracles
kind: testing
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Mandatory test oracles for core collision rules, bounds/overlap checks, and rejection non-mutation semantics for movement and rotation attempts.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_RULES
  - GAME_STATE
  - INPUT_MODEL
  - ERROR_HANDLING
  - SHAPES_AND_ROTATIONS
  - CORE_API
---

# ORACLE_CORE_COLLISION

**Tetris Core — Collision and Rejection Test Oracles (Normative)**

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* board bounds enforcement,
* overlap collision enforcement,
* rejection semantics (no mutation beyond tick/gravity counters as allowed by `GAME_STATE`),
* movement and rotation *attempts* as they relate to collision and rejection.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

## 2. Harness assumptions

The test harness must be able to:

* construct a `GameState` with a known board + active piece,
* call `step(state, inputs, config)` deterministically,
* assert board contents and state fields,
* compare two states for “no mutation” (with defined allowances).

Where possible, tests should use **fixed setups**, not random play.

## 3. Collision oracles

### ORACLE B1: Board bounds invariant (post-step)

After every `step()` call:

* board dimensions remain exactly **20×10**,
* all board cell values remain within the allowed representation (per `GAME_STATE` / `CORE_API`).

This oracle is **cross-cutting** and should be asserted in many tests, not only once.

### ORACLE B2: Bounds collision rejection (candidate blocks out of bounds)

For any attempted action that would produce candidate blocks containing any coordinate with:

* `x < 0` or `x > 9`, or
* `y < 0` or `y > 19`

the action must be **rejected**, with the state unchanged except as permitted by tick/gravity ordering in `GAME_STATE`.

Minimum required scenarios:

* `MOVE_LEFT` rejected at left wall.
* `MOVE_RIGHT` rejected at right wall.
* A rotation rejected if all wall-kick attempts still collide with bounds.

### ORACLE B3: Overlap collision rejection (candidate blocks overlap filled cells)

For any attempted action that would produce candidate blocks overlapping any occupied board cell:

* the action must be **rejected**.

Minimum required scenarios:

* `MOVE_LEFT` rejected due to overlap.
* `MOVE_RIGHT` rejected due to overlap.
* `SOFT_DROP` rejected due to overlap (and does not lock solely due to soft drop).
* Rotation rejected due to overlap if all attempts collide.

## 4. Rejection and non-mutation semantics

### ORACLE X2-C: Rejected action does not mutate state (except counters per tick ordering)

For each of these action types:

* `MOVE_LEFT`
* `MOVE_RIGHT`
* `SOFT_DROP`
* `ROTATE_CW`
* `ROTATE_CCW`
* `HOLD` (only if enabled; otherwise covered under input strictness elsewhere)

construct a scenario where the action is rejected due to collision and assert:

* board contents unchanged,
* active piece unchanged (type/rotation/origin),
* `next_piece`, `hold_piece`, RNG state unchanged,
* `score`, `level`, `lines_cleared_total` unchanged,
* `is_game_over` unchanged,

and additionally:

* only tick/gravity counters may change **exactly as specified** by the `GAME_STATE` tick ordering.

**Important:** This oracle is about rejecting *the action*, not skipping the tick.

## 5. Movement oracles (collision-focused subset)

### ORACLE M1: Move left/right success in free space

In a configuration with sufficient free space:

* `MOVE_LEFT` decreases `origin_x` by 1.
* `MOVE_RIGHT` increases `origin_x` by 1.

Also assert:

* the resulting occupied block set equals the expected translated block set.

### ORACLE M2: Move rejection at walls

Place an active piece such that:

* `MOVE_LEFT` would cause bounds collision → rejected.
* `MOVE_RIGHT` would cause bounds collision → rejected.

This oracle is a concrete instantiation of ORACLE B2.

### ORACLE M3: Soft drop collision rejection does not lock

Construct a state where the cell(s) immediately below the active piece would collide (board or bounds).

When applying:

* `SOFT_DROP`

assert:

* the soft drop is rejected (active piece unchanged),
* the tick continues normally (gravity may still trigger later in the tick depending on counters),
* **no lock occurs solely due to the soft drop input**.

(Actual lock-on-gravity is covered by `ORACLE_CORE_GRAVITY_AND_LOCKING`.)

## 6. Rotation oracles (collision-focused subset)

### ORACLE R2-C: Wall kicks are attempted in the prescribed order

Construct a state where rotation in-place would collide with a wall, but shifting by `dx=+1` would succeed.

For `ROTATE_CW` and/or `ROTATE_CCW` (as applicable):

* rotation must succeed using the `dx=+1` kick.

Mirror case:

* if in-place collides but `dx=-1` succeeds, rotation must succeed with `dx=-1`.

This oracle asserts the **collision policy** of kicks (the geometry correctness lives in `ORACLE_CORE_GEOMETRY`).

### ORACLE R3: Rotation rejection when all attempts collide

Construct a state where:

* in-place rotation collides, and
* both `dx=+1` and `dx=-1` attempts also collide,

then:

* the rotation must be rejected and the active piece unchanged.

### ORACLE R4-C: O-piece rotation is collision-neutral

For the O piece in a collision-free area:

* rotating must not produce an out-of-bounds or overlap collision,
* and must preserve a valid 4-block occupied set.

(Exact invariance of block set is asserted in `ORACLE_CORE_GEOMETRY`.)

## 7. Minimum required set contribution

For MVP gate compliance (Gates 1–6), this document contributes at minimum:

* B1, B2, B3,
* M1, M2, M3,
* R2-C, R3,
* X2-C.

---

### Notes for implementers and test authors (non-normative)

* Prefer **table-driven test construction**: define a helper that builds a state + applies one input and returns both states for comparison.
* Ensure rejection tests assert *absence* of mutation beyond counters, not merely that the action “did nothing”.

---
