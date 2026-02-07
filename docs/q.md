## `docs/RUNTIME_SPEC.md`


# RUNTIME_SPEC.md
**Runtime Loop and Execution Modes (Normative)**

## 1. Purpose

This document defines how the application **executes over time** outside the core.

It governs:
- tick scheduling,
- execution modes,
- interaction between input, core, and renderer.

---

## 2. Runtime responsibility

The runtime is responsible for:

1. Maintaining the current `GameState`
2. Acquiring inputs for each tick
3. Calling `step(state, inputs, config)`
4. Rendering the resulting state
5. Detecting termination

The runtime must not implement game logic.

---

## 3. Execution modes

### 3.1 Scripted (virtual-time) mode — REQUIRED

Characteristics:
- No sleeping
- No real-time dependency
- Tick advances only when explicitly invoked
- Inputs supplied from:
  - predefined lists, or
  - replay traces (see `REPLAY_SPEC.md`)

This mode is **mandatory** and is the default for:
- tests,
- agent evaluation,
- CI.

---

### 3.2 Interactive (real-time) mode — OPTIONAL

Characteristics:
- Fixed tick rate (recommended: 30 or 60 ticks/sec)
- Uses `sleep` or equivalent
- Polls live input per tick
- Renders continuously

This mode must be:
- optional,
- isolated,
- non-essential for correctness.

---

## 4. Tick lifecycle (normative)

For each tick:

1. Collect `inputs: tuple[InputEvent, ...]`
2. Call `step(state, inputs, config)`
3. Replace `state` with returned state
4. Render state
5. If `state.is_game_over`: terminate loop

---

## 5. Determinism guarantees

- Scripted mode must be fully deterministic.
- Interactive mode may be nondeterministic in wall-clock timing, but must not affect core logic.

---

## 6. Error handling

- If `step()` raises an exception:
  - runtime must stop execution,
  - surface the error,
  - not attempt recovery.

---

## 7. Prohibitions

Runtime must not:
- call `step()` more than once per tick,
- modify `GameState` directly,
- inspect or modify board internals beyond rendering,
- bypass input or core validation.

---
```

---

## `docs/CLI_SPEC.md`

```md
# CLI_SPEC.md
**Command-Line Interface Specification (Normative)**

## 1. Purpose

This document defines the **command-line interface** for running the application.

The CLI is a thin shell over:
- runtime,
- renderer,
- scripted inputs.

---

## 2. Entry point

The application must be invokable via:

```

python -m tetris

```

or an equivalent console script.

---

## 3. Commands

### 3.1 `run`

```

tetris run

```

Runs the game in interactive mode (if supported).

Options:
- `--seed <int>`: RNG seed
- `--tick-rate <int>`: ticks per second (interactive only)
- `--no-hold`: disable hold

---

### 3.2 `script`

```

tetris script <script_file>

```

Runs a scripted (deterministic) session.

Options:
- `--seed <int>`: overrides script seed
- `--max-ticks <int>`: stop after N ticks
- `--dump-final-state`: print final state as JSON

---

### 3.3 `replay`

```

tetris replay <replay_file>

```

Runs a deterministic replay (see `REPLAY_SPEC.md`).

---

## 4. Exit codes

| Code | Meaning |
|-----:|--------|
| 0    | Normal termination |
| 1    | Invalid CLI usage |
| 2    | Runtime error |
| 3    | Core invariant violation |

---

## 5. CLI constraints

- CLI must not implement game logic.
- CLI must not catch and suppress core errors.
- CLI must not modify rendering output.

---
```

---

## `docs/REPLAY_SPEC.md`

````md
# REPLAY_SPEC.md
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
````

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

```

---

# What you now have (important)

You now possess a **complete, end-to-end architectural spec**:

- Core: fully specified
- System decomposition: explicit
- Architecture pattern: chosen and justified
- Rendering: specified
- Runtime: specified
- CLI: specified
- Replay/evaluation: specified

This is sufficient to:

- define **role-based agent skills** cleanly,
- run **scripted agent evaluations**,
- prevent UI/runtime creep into the core,
- support human maintenance long-term.

## Next logical step (when ready)

Define `.agent/skills/` such as:

- `discover_project.py`
- `implement_core_gate_X.py`
- `write_tests_gate_X.py`
- `implement_renderer.py`
- `implement_runtime.py`
- `implement_cli.py`
- `review_against_acceptance_gates.py`

When you’re ready, say which skill you want to define first, and whether you want it **strictly gated** (fails on doc omission) or **advisory**.
```
