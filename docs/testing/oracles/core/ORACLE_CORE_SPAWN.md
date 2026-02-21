---
doc_id: ORACLE_CORE_SPAWN
name: ORACLE_CORE_SPAWN.md
title: Core Spawn Test Oracles
status: active
authority: normative
description: Mandatory test oracles for piece spawning semantics in the deterministic core.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [GAME_RULES, GAME_STATE, CORE_API]
---

# ORACLE_CORE_SPAWN

**Tetris Core — Spawn Test Oracles (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* spawn position and orientation,
* spawn collision semantics (game over),
* next-piece availability across spawns,
* spawn determinism under a fixed seed.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

---

## 2. Harness requirements

The test harness must be able to:

* create a fresh game via `new_game(config)`,
* drive the core via `step(state, inputs, config)`,
* (optionally) construct a state with a specific board occupancy (for spawn-collision testing),
* observe `active`, `next_piece`, `is_game_over`, `tick_count`.

---

## 3. Spawn position and orientation

### ORACLE S1: Spawn location

After `new_game(config)` (with any valid seed):

* `active.origin_x == 3`
* `active.origin_y == 0`

### ORACLE S2: Spawn rotation state

After `new_game(config)`:

* `active.rotation == Rotation.R0`

### ORACLE S3: Spawned piece type validity

After `new_game(config)`:

* `active.type` is one of `{I, O, T, S, Z, J, L}`

---

## 4. Next-piece guarantees

### ORACLE S4: Next piece is always defined

After `new_game(config)`:

* `next_piece` is defined and is one of `{I, O, T, S, Z, J, L}`

### ORACLE S5: Next piece remains defined after spawn transitions

After any tick that causes a lock + spawn transition (gravity lock or hard drop lock):

* `next_piece` is defined (same validity constraint as above)

---

## 5. Spawn collision and game over

### ORACLE S6: Spawn collision triggers game over immediately

Construct a state where, after a lock+clear resolution, the next spawn footprint overlaps at least one filled board cell at the spawn position.

When the core attempts to spawn the new active piece:

* `is_game_over == true` in the resulting state for that tick.

Notes for test construction:

* The spawn collision must be caused by board occupancy at the spawn footprint, not by an out-of-bounds condition.
* The harness may create this by:

  * building a state whose board is already occupied at the spawn cells, then forcing a spawn transition (preferred if your helpers allow it), or
  * running deterministic steps that produce such a board, then triggering a lock that causes spawn.

### ORACLE S7: No progression after game over (spawn collision path)

If `is_game_over` is set true due to spawn collision in a tick:

* a subsequent call to `step(state, inputs, config)` must return an unchanged state (as defined by `GAME_STATE`/`CORE_API` short-circuit rules), including:

  * `tick_count` unchanged.

(Exact “unchanged” criteria beyond tick_count are covered by @ORACLE_CORE_INVARIANTS; this oracle only asserts spawn-collision path leads into the game-over short-circuit regime.)

---

## 6. Spawn determinism (seeded)

### ORACLE S8: Determinism of initial active + next under fixed seed

Given the same `CoreConfig(seed=K, ...)` and the same code:

* `new_game(config)` must produce identical:

  * `active.type`
  * `next_piece`

across repeated runs.

This must hold for at least 3 representative seeds.

---

## 7. Minimum required set (MVP)

For MVP acceptance (Gates 1–6), at minimum:

* S1
* S2
* S4
* S6
* S8

must pass.

---
