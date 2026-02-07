---
name: RUNTIME_SPEC.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# RUNTIME SPEC

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
