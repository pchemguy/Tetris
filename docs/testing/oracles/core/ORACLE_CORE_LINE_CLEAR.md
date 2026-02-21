---
doc_id: ORACLE_CORE_LINE_CLEAR
name: ORACLE_CORE_LINE_CLEAR.md
title: Core Line Clear Test Oracles
status: active
authority: normative
description: Mandatory test oracles for full-row detection, simultaneous clearing, and row-shift semantics in the deterministic core.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [GAME_STATE, GAME_RULES, CORE_API]
---

# ORACLE_CORE_LINE_CLEAR

**Tetris Core — Line Clear Test Oracles (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* detecting full rows after a lock,
* clearing all full rows **simultaneously**,
* shifting remaining rows downward correctly,
* inserting empty rows at the top.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

---

## 2. Harness assumptions

The harness must be able to:

* construct deterministic pre-lock board states,
* force a lock deterministically (via gravity-triggered lock or hard drop),
* observe the post-step board state and `lines_cleared_total`.

Tests must avoid randomness beyond controlled piece selection and seed.

---

## 3. Definitions

* Board is `20×10`, indexed `(x, y)` with `y=0` top.
* A row `y` is **full** iff all 10 cells are occupied (`1`).
* “Simultaneous clearing” means the set of full rows is computed from the board **as of immediately after lock**, and the clear is applied in one resolution step (no staged partial effects).

---

## 4. Oracle set

### ORACLE LC1: No-clear stability

Given a lock where **no row becomes full**:

* the board after the tick must equal the locked-board state (i.e., exactly the active piece’s blocks are added),
* no other rows may change.

(Scoring changes are out of scope here.)

---

### ORACLE LC2: Single-line clear correctness

Construct a scenario where locking completes exactly **one** row (some `y = r`):

After `step()` resolves the lock:

* that row `r` must be cleared,
* all rows `0..r-1` shift down by 1,
* row `0` becomes all-zero,
* all rows below `r` remain unchanged (except for the absence of row `r`).

Additionally:

* `lines_cleared_total` increases by exactly 1.

---

### ORACLE LC3: Multi-line clear correctness (2, 3, 4)

Construct deterministic scenarios where locking completes exactly:

* 2 rows,
* 3 rows,
* 4 rows,

in a single lock resolution.

After `step()`:

* exactly those rows must be removed,
* the remaining non-cleared rows must shift down by exactly `k` where `k` is number of cleared rows *below them*,
* the top `k` rows must be all-zero,
* row order of non-cleared rows must be preserved.

Additionally:

* `lines_cleared_total` increases by exactly `k`.

---

### ORACLE LC4: Simultaneity (no staged clearing artifacts)

Construct a case where:

* two rows become full at the same lock,
* and a third row would become full **only if** clearing were staged (e.g., by shifting a partially-filled row into place between clears).

After `step()`:

* only the rows full immediately after lock may be cleared,
* no additional “secondary clears” may occur within the same tick.

This oracle forbids multi-pass clearing.

---

### ORACLE LC5: Preservation of non-cleared cells

In any clear scenario:

* any cell not part of the locked piece and not in a cleared row must appear in the post-step board exactly once, at its shifted location, with no duplication or loss.

This is a strong conservation oracle: the clear is a row deletion + compaction, not a rewrite.

---

### ORACLE LC6: Empty-row insertion at top

Whenever `k` rows are cleared:

* exactly `k` new empty rows must be inserted at the top,
* each inserted row must be `10` zeros.

No other “padding” behavior is permitted.

---

## 5. Minimum required set contribution (MVP)

For MVP acceptance (Gates 1–6), at minimum:

* LC1
* LC2
* LC3 (at least 2-line and 4-line cases)
* LC4
* LC6

must pass.

---
