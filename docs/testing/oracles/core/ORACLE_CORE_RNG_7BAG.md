---
doc_id: ORACLE_CORE_RNG_7BAG
name: ORACLE_CORE_RNG_7BAG.md
title: Core RNG 7-Bag Test Oracles
status: active
authority: normative
description: Mandatory test oracles for 7-bag randomization completeness, refill behavior, and seed-based determinism.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [GAME_RULES, GAME_STATE, CORE_API]
---

# ORACLE_CORE_RNG_7BAG

**Tetris Core — 7-Bag Randomization Test Oracles (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* 7-bag completeness,
* bag refill semantics,
* deterministic piece generation under fixed seed,
* internal RNG state consistency.

It applies only to the **pure deterministic core** (`core:core`) and is normative for Gates **1–6**.

---

## 2. Harness assumptions

The harness must be able to:

* construct a new game with a fixed `CoreConfig(seed=...)`,
* repeatedly trigger piece spawns deterministically (via controlled locking),
* observe:

  * `active.type`
  * `next_piece`
  * `rng` state (if exposed),
* compare piece sequences across independent runs.

Tests must avoid relying on gameplay randomness; they must drive controlled lock cycles.

---

## 3. Definitions

Let:

* `sequence(N)` be the first `N` spawned active pieces observed across deterministic play,
* a “bag cycle” be a sequence of 7 consecutive draws from a fresh bag.

---

## 4. Oracle set

### ORACLE RNG1: Bag completeness (7 unique pieces)

From a fresh `new_game(config)`:

* Advance the game deterministically to observe the first 7 spawned pieces.
* Let `S` be the set of those 7 types.

Assert:

* `S == {I, O, T, S, Z, J, L}`
* No duplicates occur within the first 7 draws.

This enforces one-of-each-per-bag.

---

### ORACLE RNG2: Bag refill after depletion

After observing 7 pieces:

* Continue deterministic play to observe the next 7 pieces.

Assert:

* The next 7 pieces again form exactly one complete set `{I,O,T,S,Z,J,L}` (order may differ).
* The second set must be independent of the first bag ordering.

This enforces proper bag refill semantics.

---

### ORACLE RNG3: Determinism under identical seed

Construct two independent games:

```
config = CoreConfig(seed=K, ...)
g1 = new_game(config)
g2 = new_game(config)
```

Advance both deterministically for `N ≥ 20` spawns.

Assert:

* The sequence of spawned piece types is identical at every index.

This ensures full deterministic reproducibility.

---

### ORACLE RNG4: Different seeds produce different sequences (probabilistic sanity)

Construct two games with distinct seeds:

```
seed = K
seed = K+1
```

Observe first `N ≥ 14` pieces.

Assert:

* The two sequences are not identical.

This is not a statistical randomness test; it is a structural sanity check to prevent seed being ignored.

---

### ORACLE RNG5: RNG state consistency after serialization (if supported)

If serialization helpers exist:

* Serialize state → deserialize → continue deterministic play.

Assert:

* The continuation piece sequence matches the unbroken run.

This enforces that RNG state is fully captured.

(If serialization is not implemented, this oracle may be deferred.)

---

### ORACLE RNG6: Bag internal invariant

At any observation point:

* The bag contains between `0` and `7` elements.
* All elements are valid `TetrominoType`.
* No duplicates exist inside the current bag.

If bag is empty:

* Next draw must refill to 7 before removal.

This may require inspecting `state.rng.bag`.

---

## 5. Minimum required set contribution (MVP)

For MVP acceptance (Gates 1–6), at minimum:

* RNG1
* RNG2
* RNG3

must pass.

---
