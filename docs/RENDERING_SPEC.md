---
name: RENDERING_SPEC.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# RENDERING SPEC

**ASCII Rendering Specification (Normative)**

## 1. Purpose

This document defines the **authoritative ASCII rendering format** for the Tetris application.

It exists to:

- provide a minimal but unambiguous presentation layer,
- ensure renderers are side-effect free,
- enable snapshot-based tests and replay inspection,
- prevent UI logic from leaking into the core.

Rendering is a **pure function of `GameState`**.

---

## 2. Renderer contract

### 2.1 Interface

The renderer must expose a function:

```
render(state: GameState) -> str
```

Properties:

- deterministic
- no mutation of state
- no I/O
- no timing assumptions

---

## 3. Board rendering

### 3.1 Dimensions

- Render exactly **20 rows × 10 columns** of cells.
- Each row corresponds to a board row `y ∈ [0, 19]`, top to bottom.

### 3.2 Cell symbols

| Cell type                 | Symbol |
| ------------------------- | ------ |
| Empty                     | `.`    |
| Locked block (board cell) | `#`    |
| Active piece block        | `@`    |

Rules:

- Active piece blocks override empty cells visually.
- Active piece must never overlap locked blocks (invariant).

---

## 4. Layout format (canonical)

The canonical ASCII output format is:

```

+----------+
|..........|
|..........|
|....@@@...|
|.....@....|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
+----------+
Score: <score>
Level: <level>
Lines: <lines_cleared_total>
Next: <TETROMINO>
Hold: <TETROMINO|None>

```

### Notes

- Top border and bottom border are required.
- Side borders are required.
- Metadata lines are required and must appear **in this order**.
- `<TETROMINO>` is one of `I O T S Z J L`.

---

## 5. Game over rendering

If `state.is_game_over` is true, append:

```
GAME OVER
```

as the final line.

---

## 6. Prohibitions

Renderers must not:

- animate,
- sleep,
- change symbols dynamically,
- omit metadata,
- infer hidden rows,
- apply color (unless explicitly extended later).

---

## 7. Testing implications

- Renderer output must be suitable for **golden snapshot tests**.
- Given the same `GameState`, output must match byte-for-byte.

---
