---
doc_id: ORACLE_CORE_SCORING
name: ORACLE_CORE_SCORING.md
title: Core Scoring and Leveling Test Oracles
kind: testing
scope: core:core
status: active
authority: normative
gate_applies_to: 1-6
phase_applies_to: all
description: Mandatory test oracles for score deltas, level progression, and gravity scaling invariants derived from clearing lines.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_RULES
  - GAME_STATE
  - CORE_API
---

# ORACLE_CORE_SCORING

**Tetris Core — Scoring and Leveling Test Oracles (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* score deltas from line clears,
* prohibition of other scoring sources,
* `lines_cleared_total` accumulation effects on `level`,
* the gravity scaling function as a function of `level`.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

---

## 2. Harness assumptions

The harness must be able to:

* construct deterministic lock scenarios that produce exactly `k ∈ {0,1,2,3,4}` line clears,
* observe `score`, `level`, and `lines_cleared_total` before and after `step()`,
* call `gravity_ticks_per_cell(level)` directly.

This oracle does not constrain how lock/clear scenarios are created (that belongs to collision/line-clear oracles); it constrains the resulting scoring/progression semantics.

---

## 3. Definitions

Let:

* `score_before`, `score_after`
* `lines_before`, `lines_after`
* `level_before`, `level_after`

be the respective fields in `GameState`.

Let `k = lines_after - lines_before` be the number of lines cleared due to the lock resolved during the tick.

---

## 4. Oracle set

### ORACLE SC1: Score delta for `k` lines cleared

For a tick that results in `k` cleared lines:

* if `k = 0` → `score_after - score_before == 0`
* if `k = 1` → `score_after - score_before == 100`
* if `k = 2` → `score_after - score_before == 300`
* if `k = 3` → `score_after - score_before == 500`
* if `k = 4` → `score_after - score_before == 800`

No other score changes are permitted in that tick.

---

### ORACLE SC2: No scoring from non-clear actions

Construct ticks where:

* only horizontal movement occurs,
* only rotation occurs,
* only soft drop occurs (without causing a lock and clear),
* hard drop occurs that locks but clears `k=0` lines,

and assert:

* `score_after - score_before == 0`.

This oracle enforces “line clears only” scoring.

---

### ORACLE SC3: `lines_cleared_total` monotonicity and exact increment

For any tick:

* `lines_after >= lines_before`.

For a lock-resolution tick that clears `k` lines:

* `lines_after - lines_before == k`.

No other mechanism may change `lines_cleared_total`.

---

### ORACLE SC4: Level progression per 10 total cleared lines

Level is defined as:

* `level = 1 + floor(lines_cleared_total / 10)`.

Test at minimum these checkpoints (using deterministic accumulation across multiple locks if needed):

* from `lines_cleared_total = 0` → `level == 1`
* after reaching `lines_cleared_total = 10` → `level == 2`
* after reaching `lines_cleared_total = 20` → `level == 3`

Also assert:

* `level_after >= 1`
* `level_after >= level_before` (monotonic non-decreasing).

---

### ORACLE SC5: Gravity scaling function matches rule

For representative levels, assert:

`gravity_ticks_per_cell(level) == max(1, 20 - level)`

Minimum required sample points:

* `level = 1` → `19`
* `level = 10` → `10`
* `level = 19` → `1`
* `level = 20` → `1`

Additionally:

* for `level < 1`, `gravity_ticks_per_cell(level)` must raise `ValueError`.

(If the implementation uses a different exception type, it must still be a clear failure mode; preferred is `ValueError` per `CORE_API.md`.)

---

## 5. Minimum required set contribution (MVP)

For MVP acceptance (Gates 1–6), at minimum:

* SC1
* SC2
* SC4
* SC5

must pass.

---
