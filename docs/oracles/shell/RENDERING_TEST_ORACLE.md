---
name: RENDERING_TEST_ORACLE.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---
# RENDERING TEST ORACLE

**ASCII Rendering – Mandatory Test Oracles (Normative)**

## 1. Purpose

This document maps `RENDERING_SPEC.md` to mandatory automated tests for the ASCII renderer.

It is a contract: an ASCII renderer is considered “correct” only if it satisfies these oracles.

This document corresponds to **Acceptance Gate 10**.

---

## 2. Test harness assumptions

Tests operate on the rendering layer only and must be able to:

- create `GameState` instances (or load from fixtures),
- call `render(state) -> str`,
- compare output byte-for-byte.

The harness must not depend on terminal capabilities (no color, no cursor control).

---

## 3. Output format oracles

### ORACLE F1: Output is deterministic

- For the same `GameState`, repeated calls to `render(state)` must produce identical output byte-for-byte.

### ORACLE F2: Output contains canonical borders

- Output begins with the exact first line:

```
+----------+
```

- Output contains the exact bottom border line:

```
+----------+
```

### ORACLE F3: Board area dimensions

- Between the top and bottom borders, there are exactly **20** board lines.
- Each board line matches:
- begins with `|`
- ends with `|`
- contains exactly **10** cell symbols between the borders.

### ORACLE F4: Cell symbol alphabet is restricted

- The board area contains only:
- `.` (empty),
- `#` (locked),
- `@` (active),
- plus `|` border characters.
- No other characters appear within the board area.

### ORACLE F5: Metadata lines exist and order is fixed

After the board and bottom border, output contains exactly the following metadata lines in this order:

1. `Score: <int>`
2. `Level: <int>`
3. `Lines: <int>`
4. `Next: <TetrominoType>`
5. `Hold: <TetrominoType|None>`

### ORACLE F6: Game over line

- If `state.is_game_over == true`, output ends with an additional final line:

```
GAME OVER
```

- If `state.is_game_over == false`, output must not contain `GAME OVER`.

---

## 4. State-to-render mapping oracles

### ORACLE M1: Locked cells render as `#`

- Given a `GameState` with known locked cells in the board, those cells appear as `#` in the corresponding board positions.

### ORACLE M2: Active piece cells render as `@`

- Given a non-game-over `GameState` with an active piece, all 4 active blocks appear as `@` in the correct positions.

### ORACLE M3: Active piece does not overwrite locked cells

- If a constructed invalid state would cause overlap, this is a core invariant violation and the renderer is not required to “resolve” it.
- In strict test suites, such invalid states must not be used as renderer fixtures unless the goal is to assert invariant enforcement outside the renderer.

---

## 5. Minimum required test set (Gate 10)

Gate 10 is accepted only if at least the following pass:

- F1, F2, F3, F4, F5, F6
- M1, M2

Additionally, snapshot (golden) tests must exist for at least:

- empty initial state,
- representative mid-game state,
- game-over state.

---
