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

Interactive mode MUST NOT be used as a source of truth for correctness or acceptance.

---

## 4. Render state (exactly once per tick)

For each tick:

1. Collect `inputs: tuple[InputEvent, ...]`
2. Call `step(state, inputs, config)`
3. Replace `state` with returned state
4. Render state
5. If `state.is_game_over`: terminate loop

---

## 5. Renderer selection

The runtime MAY support selecting a renderer at startup.

### Rules

- Renderer selection affects **only which renderer implementation is called**.
- Renderer selection MUST NOT:
    - alter rendering semantics,
    - alter output of a renderer,
    - provide fallback or auto-detection behavior.

### Selection mechanism

Renderer selection MUST be:

- explicit (e.g., configuration or CLI flag),
- resolved once at runtime initialization.

Example (non-normative):

- `--renderer ascii`
- `--renderer debug`

---

### Default renderer

- If no renderer is specified:
    - the default renderer MUST be the ASCII renderer defined in `RENDERING_SPEC.md`.

This guarantees Gate 10 remains the baseline.

---

### Renderer contract enforcement

The runtime MUST:

- call exactly one renderer per render step,
- pass the unmodified `GameState`,
- treat renderer output as opaque.

The runtime MUST NOT:

- interpret renderer output,
- branch behavior based on renderer type,
- compensate for renderer limitations.

---

### Gate interaction

- Gate 10 validates the ASCII renderer only.
- Support for additional renderers:
  - is out of scope for Gate 10,
  - MUST NOT weaken ASCII rendering requirements,
  - MUST be covered by additional gates if mandated.

---

## 6. Determinism guarantees

- Scripted mode must be fully deterministic.
- Interactive mode may be nondeterministic in wall-clock timing, but must not affect core logic.

---

## 7. Error handling

- If `step()` raises an exception:
    - runtime must stop execution,
    - surface the error,
    - not attempt recovery.

---

## 8. Prohibitions

Runtime must not:

- call `step()` more than once per tick,
- skip rendering for any tick in which `step()` was called.
- modify `GameState` directly,
- inspect or modify board internals beyond rendering,
- bypass input or core validation.

---
