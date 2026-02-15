---
doc_id: GAME_RULES
name: GAME_RULES.md
title: Game Rules
kind: spec
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
description: Behavioral specification defining gameplay rules, scoring, gravity, and progression semantics.
---

# GAME RULES

**Classic Tetris – Normative Ruleset (Agent Target Spec)**

## 1. Scope and intent

This document defines the **authoritative game rules** for the reference Tetris implementation used to evaluate the prompting system in this project.

Its purpose is to:

* eliminate ambiguity,
* constrain agent behavior,
* enable deterministic testing,
* prevent “creative” deviations.

Anything **not explicitly specified here is undefined behavior** and must not be implemented without an explicit rule update.

---

## 2. Playfield

### 2.1 Dimensions

* Width: **10 columns**
* Height: **20 visible rows**
* Coordinate system:

  * `(x, y)`
  * `x ∈ [0, 9]` left → right
  * `y ∈ [0, 19]` top → bottom

### 2.2 Hidden rows

* No hidden buffer rows are used.
* Pieces spawn partially above the visible field only if explicitly allowed by spawn rules (see §4).

---

## 3. Tetrominoes

### 3.1 Set

The standard 7 tetrominoes are used:

```
I, O, T, S, Z, J, L
```

### 3.2 Geometry

* Each tetromino is represented as **4 blocks** on a square grid.
* All rotations are defined relative to a **piece-local origin**.
* Shapes and rotation states must be **explicitly enumerated**, not inferred procedurally.

---

## 4. Rotation system

### 4.1 Rotation model

* Rotation system: **Simplified SRS-compatible**
* Rotation states:
    * `0°`, `90°`, `180°`, `270°`
* Rotation direction:
    * Clockwise
    * Counter-clockwise

### 4.2 Wall kicks

* **Basic wall kicks only**
* No floor kicks
* No T-spin recognition or bonuses

If a rotation would cause collision:

1. Attempt the rotation in-place
2. Attempt horizontal offset `±1`
3. If all attempts fail, rotation is rejected

---

## 5. Spawn rules

### 5.1 Spawn position

* All pieces spawn at:
    * `x = 3`
    * `y = 0`
* Orientation: **0° rotation state**

### 5.2 Spawn collision

* If the spawn position collides with existing blocks:
    * **Game over is triggered immediately**

---

## 6. Gravity and movement

### 6.1 Gravity

* Gravity pulls the active piece **downward by 1 cell**
* Gravity tick interval depends on level (see §9)

### 6.2 Player actions

Supported actions:

* Move left
* Move right
* Soft drop (down by 1 cell, repeatable)
* Hard drop (instant drop to lowest valid position)
* Rotate clockwise
* Rotate counter-clockwise

### 6.3 Movement constraints

* Moves that cause collision are rejected
* No partial movement is allowed

---

## 7. Locking behavior

### 7.1 Lock rule

* A piece **locks immediately** when:
    * it cannot move down during a gravity tick **or**
    * a hard drop is performed

### 7.2 Lock delay

* **No lock delay** is implemented
* This is an intentional simplification

---

## 8. Line clearing

### 8.1 Detection

* After a piece locks:
    * Any row with **all 10 cells occupied** is cleared

### 8.2 Resolution order

* All completed rows are cleared **simultaneously**
* Rows above cleared rows shift downward
* New empty rows appear at the top

---

## 9. Scoring and levels

### 9.1 Line clear scoring

| Lines cleared | Score |
| ------------- | ----- |
| 1             | 100   |
| 2             | 300   |
| 3             | 500   |
| 4             | 800   |

* No T-spin bonuses
* No combo bonuses
* No back-to-back bonuses

### 9.2 Level progression

* Initial level: **1**
* Level increases by **1 every 10 cleared lines**

### 9.3 Gravity scaling

* Gravity interval decreases with level
* Exact formula:

```
gravity_ticks_per_cell = max(1, 20 - level)
```

(Interpretation: at level 1, 19 ticks per cell; at level 19+, 1 tick per cell.)

---

## 10. Randomization

### 10.1 Piece generator

* RNG method: **7-bag randomizer**
* Each bag contains exactly one of each tetromino
* Bag is shuffled uniformly
* Pieces are drawn sequentially

### 10.2 Determinism

* RNG must be seedable
* Given the same seed and inputs, gameplay must be deterministic

---

## 11. Game over conditions

The game ends when **any** of the following occurs:

* A new piece cannot spawn due to collision
* A locked piece occupies any cell in `y = 0`

---

## 12. Hold and preview

### 12.1 Next piece preview

* Exactly **one** next piece is visible

### 12.2 Hold piece

* Hold is **optional for MVP**
* If implemented:
    * Hold can be used **once per piece**
    * Holding swaps the active piece with the hold slot
    * First hold stores the piece and spawns the next piece

---

## 13. Out of scope (explicitly prohibited)

The following features must **not** be implemented unless this document is revised:

* T-spin detection or scoring
* Ghost pieces
* Lock delay or extended placement
* Advanced SRS kicks
* Combo or back-to-back scoring
* Multiplayer
* Animations affecting logic timing
* AI/autoplay

---

## 14. Contractual note for agents

Agents must treat this document as **binding**.

If:

* a rule is ambiguous,
* a rule is missing,
* or a conflict is detected,

the agent must **stop and escalate**, not guess.

---
