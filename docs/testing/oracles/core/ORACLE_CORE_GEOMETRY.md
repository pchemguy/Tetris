---
doc_id: ORACLE_CORE_GEOMETRY
name: ORACLE_CORE_GEOMETRY.md
title: Core Geometry and Rotation Test Oracles
kind: testing
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Mandatory test oracles for tetromino geometry enumeration and rotation-state correctness.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - SHAPES_AND_ROTATIONS
  - GAME_STATE
  - CORE_API
---

# ORACLE_CORE_GEOMETRY

**Tetris Core — Geometry and Rotation Test Oracles (Normative)**

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* exact tetromino block geometry,
* rotation state transitions,
* invariants of enumerated shapes.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

All geometry must match `SHAPES_AND_ROTATIONS` exactly.

---

## 2. Harness assumptions

The harness must be able to:

* construct an `ActivePiece`,
* call `blocks_for(active)` (or equivalent geometry resolver),
* compare returned block sets deterministically,
* inspect rotation transitions via `step()`.

Block ordering is not semantically important but must be deterministic.

Recommended: compare **sets** of `(x, y)` coordinates.

---

## 3. Enumeration correctness

### ORACLE G1: Exactly four unique blocks per rotation

For every:

* `TetrominoType`
* `Rotation ∈ {R0, R90, R180, R270}`

assert:

* exactly 4 blocks are returned,
* all coordinates are integers,
* no duplicate block positions exist.

---

### ORACLE G2: Exact match with canonical enumeration

For every tetromino and every rotation state:

* construct an `ActivePiece` at a neutral origin (e.g., `(0,0)`),
* compute `blocks_for(active)`,
* assert that the returned block set matches **exactly** the block offsets defined in `SHAPES_AND_ROTATIONS`.

This must be an exact equality test (no normalization, no inferred rotations).

---

## 4. Rotation state transitions

### ORACLE G3: Clockwise rotation cycle

For each tetromino type:

Starting from `R0`:

* apply `ROTATE_CW` once → state must become `R90`,
* again → `R180`,
* again → `R270`,
* again → `R0`.

Assert:

* rotation enum transitions follow the defined cycle,
* the resulting block sets match the canonical enumerations for those states.

---

### ORACLE G4: Counter-clockwise rotation cycle

For each tetromino type:

Starting from `R0`:

* apply `ROTATE_CCW` once → state must become `R270`,
* again → `R180`,
* again → `R90`,
* again → `R0`.

Assert:

* enum transitions follow the defined reverse cycle,
* geometry matches canonical enumerations.

---

### ORACLE G5: CW followed by CCW is identity (in free space)

In a collision-free configuration:

* apply `ROTATE_CW`,
* then `ROTATE_CCW`,

assert:

* final rotation equals initial rotation,
* block set equals initial block set.

Mirror case:

* `ROTATE_CCW` then `ROTATE_CW` must also be identity.

---

## 5. O-piece invariance

### ORACLE G6: O-piece block invariance

For `TetrominoType.O`:

For all rotation states:

* block set must be identical.

Rotation enum may change or may remain constant, but:

* the occupied block set must remain identical,
* no collisions must arise in free space.

---

## 6. Translation consistency

### ORACLE G7: Translation is additive and stable

For any tetromino and rotation:

* compute blocks at origin `(0,0)` → call this `B0`,
* compute blocks at origin `(x,y)` → call this `B1`,

assert:

* `B1 == { (bx + x, by + y) for (bx, by) in B0 }`.

This ensures:

* no hidden normalization,
* no origin reinterpretation,
* no procedural shape distortion.

---

## 7. No procedural inference

### ORACLE G8: Enumerated geometry is not derived algorithmically

This is a structural test constraint:

* Rotations must correspond exactly to the explicit enumerations.
* The implementation must not compute rotations by matrix transform unless it reproduces the enumerated sets exactly.

Practical enforcement:

* At least one asymmetric shape (e.g., J or L) must be tested for exact coordinate equality in all four states.
* At least one 180° state must be explicitly asserted against canonical enumeration.

---

## 8. Minimum required set contribution

For MVP (Gates 1–6), at minimum:

* G1
* G2
* G3
* G5
* G6

must pass for all tetromino types.

---

## Design note (non-normative)

This document isolates **pure geometry truth**.

* Collision policy belongs in `ORACLE_CORE_COLLISION`.
* Locking/gravity effects belong in `ORACLE_CORE_GRAVITY_AND_LOCKING`.

Keeping geometry isolated prevents test coupling between shape correctness and board state logic.

---
