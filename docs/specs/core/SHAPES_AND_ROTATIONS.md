---
doc_id: SHAPES_AND_ROTATIONS
name: SHAPES_AND_ROTATIONS.md
title: Shapes and Rotations
status: active
authority: normative
description: Canonical geometry definition of tetromino shapes and rotations.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# SHAPES AND ROTATIONS

**Tetromino Geometry and Rotation Enumeration (Normative)**

## 1. Purpose

This document defines the **exact block geometry** and **rotation states** for all tetrominoes used by this project.

It exists to:

- eliminate geometric ambiguity,
- forbid procedural inference of shapes,
- enable strict, geometry-based test oracles.

All tetromino shapes and rotations must be implemented **exactly as enumerated here**.

If a rotation or shape is not listed, it does not exist.

---

## 2. General conventions

### 2.1 Local coordinate system

Each tetromino is defined in **piece-local coordinates** relative to an origin `(0, 0)`.

- Local coordinates are integer `(dx, dy)` offsets.
- The **piece origin** is mapped to board coordinates `(origin.x, origin.y)` (see GAME_STATE.md).
- A block at local `(dx, dy)` occupies board cell:
  `(origin.x + dx, origin.y + dy)`

### 2.2 Rotation states

Each tetromino has exactly four rotation states:

- `R0`
- `R90`
- `R180`
- `R270`

Rotation states are **explicit enumerations**, not computed via matrix rotation.

Rotation direction semantics:

- `ROTATE_CW`: R0 → R90 → R180 → R270 → R0
- `ROTATE_CCW`: R0 → R270 → R180 → R90 → R0

---

## 3. Tetromino definitions

### 3.1 I tetromino

#### R0

```
(0,1) (1,1) (2,1) (3,1)
```

#### R90

```
(2,0)
(2,1)
(2,2)
(2,3)
```

#### R180

```
(0,2) (1,2) (2,2) (3,2)
```

#### R270

```
(1,0)
(1,1)
(1,2)
(1,3)
```

---

### 3.2 O tetromino

**Note:** All rotation states are identical.

#### R0 / R90 / R180 / R270

```
(1,0) (2,0)
(1,1) (2,1)
```

Rotation may be treated as a no-op or as cycling identical states; behavior must be consistent.

---

### 3.3 T tetromino

#### R0

```
(1,0)
(0,1) (1,1) (2,1)
```

#### R90

```
(1,0)
(1,1) (2,1)
(1,2)
```

#### R180

```
(0,1) (1,1) (2,1)
(1,2)
```

#### R270

```
      (1,0)
(0,1) (1,1)
      (1,2)
```

---

### 3.4 S tetromino

#### R0

```
      (1,0) (2,0)
(0,1) (1,1)
```

#### R90

```
(1,0)
(1,1) (2,1)
(2,2)
```

#### R180

```
(1,1) (2,1)
(0,2) (1,2)
```

#### R270

```
(0,0)
(0,1) (1,1)
(1,2)
```

---

### 3.5 Z tetromino

#### R0

```
(0,0) (1,0)
(1,1) (2,1)
```

#### R90

```
      (2,0)
(1,1) (2,1)
(1,2)
```

#### R180

```
(0,1) (1,1)
(1,2) (2,2)
```

#### R270

```
      (1,0)
(0,1) (1,1)
(0,2)

```

---

### 3.6 J tetromino

#### R0

```
(0,0)
(0,1) (1,1) (2,1)
```

#### R90

```
(1,0) (2,0)
(1,1)
(1,2)
```

#### R180

```
(0,1) (1,1) (2,1)
(2,2)
```

#### R270

```
      (1,0)
      (1,1)
(0,2) (1,2)
```

---

### 3.7 L tetromino

#### R0

```
            (2,0)
(0,1) (1,1) (2,1)
```

#### R90

```
(1,0)
(1,1)
(1,2) (2,2)
```

#### R180

```
(0,1) (1,1) (2,1)
(0,2)
```

#### R270

```
(0,0) (1,0)
(1,1)
(1,2)
```

---

## 4. Geometry invariants (mandatory)

For all tetrominoes and all rotations:

- Exactly **4 blocks** exist.
- All `(dx, dy)` are integers.
- No duplicate block positions exist within a rotation state.
- Rotations do **not** change block count.
- Rotation transitions must use the enumerated sets only.

---

## 5. Agent constraints (binding)

Agents must:

- use these enumerations verbatim,
- not infer geometry procedurally,
- not normalize shapes dynamically,
- not introduce additional rotation states,
- not reinterpret the origin.

If a test fails due to geometry mismatch, the implementation is incorrect.

---

## 6. Recommended tests (non-exhaustive)

At minimum, the test suite should assert:

- each rotation has exactly 4 unique blocks,
- all rotations for all pieces match this document exactly,
- rotating CW then CCW returns to the original block set,
- O-piece rotations are invariant.

These tests should be independent of board state.

---
