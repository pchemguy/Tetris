---
name: CLI_SPEC.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# CLI SPEC

**Command-Line Interface Specification (Normative)**

## 1. Purpose

This document defines the **command-line interface** for running the application.

The CLI is a thin shell over:

- runtime,
- renderer,
- scripted inputs.

---

## 2. Composition root responsibility (normative)

The CLI is the **composition root** of the application.

It is responsible for:

- parsing command-line arguments,
- selecting execution mode (`run`, `script`, `replay`),
- loading configuration and external data via persistence,
- instantiating and wiring together:
    - runtime,
    - renderer,
    - presenter,
    - input driver and controller (if applicable),
- passing fully constructed dependencies and configuration into the runtime.

The CLI must not:

- implement game rules,
- implement rendering semantics,
- perform tick scheduling,
- call `step()` directly.

---

## 3. Entry point

The application must be invokable via:

```
python -m tetris
```

or an equivalent console script.

---

## 4. Commands

### 4.1 `run`

```

tetris run

```

Runs the game in interactive mode (if supported).

Options:

- `--seed <int>`: RNG seed
- `--tick-rate <int>`: ticks per second (interactive only)
- `--no-hold`: disable hold

---

### 4.2 `script`

```
tetris script <script_file>
```

Runs a scripted (deterministic) session.

Options:

- `--seed <int>`: overrides script seed
- `--max-ticks <int>`: stop after N ticks
- `--dump-final-state`: print final state as JSON

---

### 4.3 `replay`

```
tetris replay <replay_file>
```

Runs a deterministic replay (see `REPLAY_SPEC.md`).

---

## 5. Exit codes

| Code | Meaning                  |
| ---: | ------------------------ |
|    0 | Normal termination       |
|    1 | Invalid CLI usage        |
|    2 | Runtime error            |
|    3 | Core invariant violation |

---

## 6. CLI constraints

- CLI must not implement game logic.
- CLI must not catch and suppress core errors.
- CLI must not modify rendering output.

---
