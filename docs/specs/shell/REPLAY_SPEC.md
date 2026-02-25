---
doc_id: REPLAY_SPEC
name: REPLAY_SPEC.md
title: Replay Specification
status: active
authority: normative
description: Defines deterministic replay file format and validation rules.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [GAME_STATE, INPUT_MODEL]
---

# REPLAY SPEC

**Deterministic Replay Format (Optional but Strongly Recommended)**

## 1. Purpose

This document defines a **deterministic replay format** for evaluation and debugging.

Replays allow:

- exact reproduction of runs,
- agent output auditing,
- regression testing.

---

## 2. Replay file format

Replay files are JSON.

### 2.1 Top-level structure

```json
{
  "version": 1,
  "seed": 12345,
  "config": {
    "enable_hold": false
  },
  "ticks": [
    [],
    ["MOVE_LEFT"],
    ["ROTATE_CW"],
    ["HARD_DROP"]
  ]
}
```

---

## 3. Semantics

* `seed` initializes the RNG.
* `ticks[i]` is the input list for tick `i`.
* Empty list means no input that tick.
* Input strings must match `InputEvent` enum names exactly.

---

## 4. Determinism contract

Given:

* identical replay file,
* identical core implementation,

the final state **must be identical** byte-for-byte.

---

## 5. Validation rules

Replay loader must:

* validate input names,
* reject unknown events,
* reject malformed structure,
* reject missing ticks array.

Malformed replay files are errors, not warnings.

---

## 6. Scope limits

Replay files do not:

* encode rendering,
* encode timing,
* encode intermediate states.

They describe **inputs only**.

---
