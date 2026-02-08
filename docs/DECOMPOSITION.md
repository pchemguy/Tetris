---
name: DECOMPOSITION.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# DECOMPOSITION

**System Decomposition and Component Responsibilities (Normative)**

---

## 1. Purpose

This document defines the **authoritative decomposition** of the Tetris application into components and assigns **explicit responsibility boundaries** to each.

It exists to:

- make responsibilities and boundaries explicit,
- prevent core/engine contamination with UI, timing, or platform concerns,
- enable role-based agent skills aligned to components,
- support incremental delivery beyond the pure core.

If a behavior or responsibility is not assigned here, it must not be implemented ad hoc.

This document is **normative** and applies to all acceptance gates.

---

## 2. Top-level decomposition

The system is decomposed into the following components:

1. **Core (Engine)**
2. **Renderer (pure)**
3. **Terminal Presenter (I/O)**
4. **Input Driver (I/O)**
5. **Input Controller (mapping / policy)**
6. **Runtime (Game Loop / Orchestrator)**
7. **App Shell (CLI / Entrypoints)**
8. **Persistence (Optional)**
9. **Test & Evaluation Harness**
10. **Telemetry / Observability (Optional)**

Notes:

- The **core** is a pure deterministic simulation; all I/O and timing live outside it.
- The **renderer** produces a representation of state; the **presenter** performs output.

Each component has a strict responsibility boundary (see §3).

---

## 3. Component responsibilities and constraints

### 3.1 Core (Engine)

**Location:** `tetris/src/tetris/core.py` (and optional submodules under `tetris/src/tetris/`)

**Responsibilities**

- Implement the full deterministic simulation defined by:
    - `GAME_RULES.md`
    - `GAME_STATE.md`
    - `SHAPES_AND_ROTATIONS.md`
    - `INPUT_MODEL.md`
    - `ERROR_HANDLING.md`
    - `CORE_API.md`
- Provide `new_game()` and `step()` as the only supported evolution interface.
- Maintain determinism and immutability guarantees.

**Explicit non-responsibilities**

- No rendering or formatting
- No real-time scheduling or sleeping
- No keyboard polling or OS integration
- No file or network I/O by default

---

### 3.2 Renderer (pure)

**Location:** `tetris/src/tetris/rendering/` (module namespace reserved)

**Responsibilities**

- Convert a `GameState` into a deterministic representation.
- Expose a renderer function with the interface (or equivalent):
    - `render(state: GameState) -> str`
- Implement the ASCII renderer behavior exactly as specified in `RENDERING_SPEC.md`.

**Explicit non-responsibilities**

- Must not perform output (stdout/stderr), screen clearing, cursor movement, or flushing.
- Must not depend on environment, terminal capabilities, locale, or timing.
- Must not mutate `GameState`.
- Must not implement game rules or time stepping.

---

### 3.3 Terminal Presenter (I/O)

**Location:** `tetris/src/tetris/presentation/` (module namespace reserved)

**Responsibilities**

- Perform terminal output for rendered frames (`str`) including (if supported):
    - clearing the screen and/or positioning the cursor,
    - writing the rendered frame to an output stream,
    - flushing output.
- Provide presentation *mechanics* only; the presenter treats the frame as opaque text.

**Explicit non-responsibilities**

- Must not compute or alter rendering semantics (formatting rules belong to `RENDERING_SPEC.md`).
- Must not interpret `GameState` (the presenter should not receive `GameState` at all).
- Must not branch behavior based on frame content (no “parsing” rendered output).
- Must not implement timing policy (tick scheduling belongs to runtime).

**Notes**

- Terminal sizing quirks or dynamic resizing are out of scope unless explicitly specified.
  If unsupported, the presenter must not attempt implicit “best effort” adaptation.

---

### 3.4 Input Driver (I/O)

**Location:** `tetris/src/tetris/input/driver/` (module namespace reserved)

**Responsibilities**

- Acquire raw input signals from the environment (e.g. keyboard).
- Support non-blocking polling when required by interactive runtime.
- Provide raw (or minimally normalized) input signals to the input controller.

**Explicit non-responsibilities**

- Must not map inputs to `InputEvent` semantics (belongs to the input controller).
- Must not implement repeats, debouncing policy, or per-tick semantics (belongs to controller/runtime policy).
- Must not mutate `GameState` or call `step()`.
- Must not implement “default keybindings” (belongs to controller configuration).

---

### 3.5 Input Controller (mapping / policy)

**Location:** `tetris/src/tetris/input/controller.py` (module namespace reserved)

**Responsibilities**

- Map raw input signals to `InputEvent` values defined by `INPUT_MODEL.md`.
- Enforce per-tick input semantics:
    - ordering,
    - no implicit key repeat unless explicitly specified,
    - any policy required for interactive mode (if supported).

**Explicit non-responsibilities**

- Must not implement core game rules (movement/rotation/collision).
- Must not mutate game state directly.
- Must not perform OS I/O (belongs to input driver).

---

### 3.6 Runtime (Game Loop / Orchestrator)

**Location:** `tetris/src/tetris/runtime/` (module namespace reserved)

**Responsibilities**

- Own tick scheduling and loop control as specified in `RUNTIME_SPEC.md`.
- Maintain the current `GameState`.
- Coordinate one tick as:
    1. collect inputs via input driver/controller,
    2. call `step(state, inputs, config)` exactly once,
    3. replace state with the returned state,
    4. call renderer,
    5. delegate output to presenter,
    6. terminate on `state.is_game_over`.
- Support scripted (virtual-time) mode as mandatory; interactive mode is optional.

**Explicit non-responsibilities**

- Must not re-implement any game rule logic (gravity, locking, scoring, etc.).
- Must not compute rendering semantics (belongs to renderer).
- Must not directly read OS input (belongs to input driver).

---

### 3.7 App Shell (CLI / Entrypoints)

**Location:** `tetris/src/tetris/__main__.py` and/or `tetris/src/tetris/cli.py`

**Responsibilities**

- Parse arguments and select execution mode per `CLI_SPEC.md`.
- Wire together components:
    - runtime,
    - renderer,
    - presenter,
    - input driver/controller (if interactive),
    - replay loader (if replay).
- Configure runtime and renderer selection explicitly when supported.

**Explicit non-responsibilities**

- Must not implement core rules.
- Must not implement rendering semantics.
- Must not contain test logic (tests live under `tetris/tests/`).

---

### 3.8 Persistence (Optional)

**Location:** `tetris/src/tetris/persistence/` (reserved)

**Responsibilities**

- Save/load auxiliary data such as:
  - high scores (if enabled),
  - configuration,
  - deterministic replay traces (inputs + seed), as specified by `REPLAY_SPEC.md`.

**Constraints**

- Persistence must not affect core determinism.
- Replay loading must be strict; no auto-correction of invalid data.

---

### 3.9 Test & Evaluation Harness

**Location:** `tetris/tests/` plus optional `eval/` (reserved)

**Responsibilities**

- Implement all mandatory oracles in:
    - `CORE_TEST_ORACLE.md`,
    - relevant shell-level `*_TEST_ORACLE.md` documents when applicable.
- Enforce:
    - determinism,
    - invariants,
    - API compatibility,
    - regression protection.

**Explicit non-responsibilities**

- Must not weaken oracles to accommodate implementation.
- Must not add speculative tests for unspecified behavior.

---

### 3.10 Telemetry / Observability (Optional)

**Location:** `tetris/src/tetris/telemetry/` (reserved)

**Responsibilities**

- Collect diagnostics such as:
    - step events,
    - counters,
    - traces,
  without mutating core logic.

**Constraints**

- Must not affect core determinism or game semantics.
- Must not become a dependency for core correctness.

---

## 4. Interfaces between components

The only allowed cross-component interfaces are:

- **Runtime → Core**
    - `new_game(config)`
    - `step(state, inputs, config)`
- **Runtime → Input Driver**
    - `poll_raw_inputs(...) -> <raw input representation>`
- **Runtime → Input Controller**
    - `poll_inputs(...) -> tuple[InputEvent, ...]`
- **Runtime → Renderer**
    - `render(state) -> str`
- **Runtime → Presenter**
    - `present(frame: str) -> None`
- **CLI → Runtime**
    - `run(...)` entrypoints

Constraints:

- Presenter must not receive `GameState`; it receives only the rendered `frame: str`.
- Renderer must not perform I/O; it returns only a `str`.
- Input driver must not return `InputEvent`; it returns only raw input signals.
- Input controller must not perform OS I/O; it maps raw inputs to `InputEvent`s.

No component may “reach across” boundaries by importing internal helpers from another
component unless explicitly designated as public API.

---

## 5. Delivery staging

The recommended staged expansion beyond the pure core:

1. **Core + tests** (Gates 0–6)
2. Optional: **core extensions** (Gates 7–9)
3. **ASCII renderer** (Gate 10)
4. **Scripted runtime** (Gate 11)
5. **CLI** (Gate 12)
6. **Replay** (Gate 13)
7. Optional: **interactive runtime + terminal I/O adapters** (input driver + presenter)

---

## 6. Skill mapping note (non-normative)

Agent skills should map to roles that primarily “own” one component:

- core logic
- test generation
- runtime/orchestration
- renderer
- terminal presenter
- input driver/controller
- CLI integration
- refactoring and bugfixing

This document provides the canonical component boundaries those roles must respect.

---
