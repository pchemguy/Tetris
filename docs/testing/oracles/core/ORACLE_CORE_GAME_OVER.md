---
doc_id: ORACLE_CORE_GAME_OVER
name: ORACLE_CORE_GAME_OVER.md
title: Core Game Over Test Oracles
status: active
authority: normative
description: Mandatory test oracles for game-over triggering conditions and terminal-state behavior.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_RULES
  - GAME_STATE
  - CORE_API
  - ORACLE_CORE_SPAWN
  - ORACLE_CORE_GRAVITY_AND_LOCKING
---

# ORACLE_CORE_GAME_OVER

**Tetris Core — Game Over Test Oracles (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* spawn-collision game over,
* post-lock top-row game over,
* terminal-state immutability,
* short-circuit step semantics when `is_game_over == true`.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

---

## 2. Definitions

Game over is a terminal state defined by:

```
state.is_game_over == true
```

Once set:

* no further gameplay progression may occur,
* `step()` must short-circuit deterministically.

Game over may be triggered only by rules defined in `GAME_RULES` and `GAME_STATE`.

---

## 3. Harness assumptions

The harness must be able to:

* construct specific board states,
* force deterministic spawn events,
* trigger locking and spawning sequences,
* inspect:

  * `is_game_over`
  * board contents
  * active piece
  * tick counters.

Tests must use controlled setups rather than random gameplay.

---

## 4. Oracle set

### ORACLE GO1: Spawn collision triggers immediate game over

Construct a board such that the spawn footprint at:

```
(origin_x=3, origin_y=0, rotation=R0)
```

overlaps at least one occupied cell.

Trigger spawn.

Assert:

* `is_game_over == true`
* No further active piece progression occurs.

This enforces §5.2 of `GAME_RULES`.

---

### ORACLE GO2: Top-row occupancy after lock triggers game over

Construct a scenario where:

* A piece locks,
* After line clear resolution,
* At least one filled cell exists at `y == 0`.

Assert:

* `is_game_over == true`

This enforces §11 of `GAME_RULES`.

---

### ORACLE GO3: Game over short-circuits step

Given a state where:

```
state.is_game_over == true
```

Call:

```
step(state, inputs)
```

Assert:

* Returned state equals input state (structurally identical except possibly event tuple),
* `tick_count` does not increment,
* No gravity changes occur,
* No new active piece is spawned,
* No score or level changes occur.

This enforces terminal immutability.

---

### ORACLE GO4: No double-trigger side effects

Trigger game over once.

On subsequent calls to `step()`:

* No additional state mutation occurs.
* No duplicate `GAME_OVER` event is emitted (if events implemented).

Game over must be idempotent.

---

### ORACLE GO5: Game over does not corrupt state invariants

After game over:

* Board remains valid (20×10, 0/1 only).
* RNG state remains valid.
* `next_piece` remains defined.
* Score and level remain unchanged.
* Active piece may remain for inspection but must not mutate further.

---

## 5. Forbidden behavior

The following are prohibited:

* Continuing gravity after game over.
* Incrementing `tick_count` after game over.
* Clearing additional lines after game over.
* Generating new pieces after terminal state.

If any occur, implementation is incorrect.

---

## 6. Minimum required set contribution (MVP)

For MVP acceptance (Gates 1–6), at minimum:

* GO1
* GO3

must pass.

GO2 is strongly recommended for full correctness.

---
