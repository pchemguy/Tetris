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
    The **core** is the authoritative simulation.
    - It defines _all_ game state and state transitions.
    - It is deterministic, side-effect-free, and testable in isolation.
    - It exposes a minimal public API (`new_game`, `step`) and nothing more.
    The core **never** performs I/O, rendering, timing, or platform interaction.
2. **Renderer (pure)**
    The **renderer** is a _pure presentation transformer_.
    - Convert a `GameState` into a presentable representation: 
      `render(state: GameState) -> str`
    - formats state,
    - applies presentation rules,
    - produces deterministic output.
    Rendering is **representation**, not display.
3. **Terminal Presenter (I/O)**
    The **presenter** is responsible for _emitting rendered output_ to a concrete medium (e.g. a terminal).
    - consumes renderer output
    - performs I/O
    - has no knowledge of game rules or state evolution
    - clear screen / position cursor
    - print frame
    - flush
    - optionally throttle output rate (but timing belongs in runtime)
    - handle terminal sizing quirks if you decide to support them (or explicitly forbid)
4. **Input Driver (I/O)**
    The **input driver** interfaces with the operating system or environment.
    - read raw input events (keyboard, stdin, etc.)  
    - perform non-blocking polling if required
    - translate raw keys to higher-level signals (or hand raw keys to controller)
5. **Input Controller (mapping / policy)**
    The **input controller** maps input signals to game-level intent.
    - map keys to `InputEvent`
    - enforce per-tick semantics (no implicit repeats unless specified)
    - possibly handle key debouncing/repeat policy (but your core model says “no implicit repeat”)
6. **Runtime (Game Loop / Orchestrator)**
    The **runtime** coordinates execution.
    - maintain the current `GameState`
    - schedule ticks (real-time or virtual-time)
    - collect inputs via input driver + controller
    - call `step()` exactly once per tick
    - call the renderer
    - delegate output to the presenter
    - detect termination
    The runtime orchestrates; it does not define rules. Runtime consumes already-resolved `core_config`/`shell_config` and already-instantiated dependencies; it does not discover configuration or load files.
7. **App Shell (CLI / Entrypoints)**
    The **app shell** is the user-facing entry layer.
    CLI is the _composition root_.
    - parse command-line arguments
    - select execution mode (run / script / replay)
    - wire components together
    - configure runtime and dependencies
    - select renderer/presenter/input driver
    The CLI contains **no game logic** and **no rendering semantics**.
8. **Persistence (Optional)**
    Persistence supports durable data such as:
    - high scores
    - configuration
    - deterministic replay traces
    Persistence is invoked by the **composition root (CLI)** for loading configuration and replay/script inputs; it may also be used by runtime _only_ for explicitly specified run outputs (e.g., saving replays), preferably via injected sinks.
9. **Test & Evaluation Harness**
    The test harness enforces correctness.
10. **Telemetry / Observability (Optional)**
    Telemetry collects diagnostic data without affecting behavior.

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

**Configuration boundary**

- The runtime consumes an already-resolved configuration.
- The runtime must not:
    - locate configuration files,
    - parse command-line arguments,
    - load configuration or replay data from disk.
- All configuration discovery and loading is performed by the App Shell (CLI), which passes the resulting configuration objects into the runtime explicitly.

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

Persistence provides durable I/O services for the application, such as:

- loading configuration files,
- loading deterministic replay traces,
- saving replay traces or run artifacts (if enabled),
- saving auxiliary data such as high scores.

Persistence is a service, not a controller.

**Constraints**

- Persistence must not affect core determinism.
- Replay loading must be strict; no auto-correction of invalid data.

**Invocation rules**

- Persistence is invoked by the App Shell (CLI) when:
    - loading configuration,
    - loading scripts or replay files,
    - performing upfront validation of external data.
- Persistence may be invoked by the runtime only for:
    - explicitly specified run outputs (e.g. saving a replay trace),
    - and preferably via injected sink interfaces rather than direct imports.

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
- **CLI → Persistence**
    - `load_config(...)`
    - `load_replay(...)`

**Constraints**:

- Presenter must not receive `GameState`; it receives only the rendered `frame: str`.
- Renderer must not perform I/O; it returns only a `str`.
- Input driver must not return `InputEvent`; it returns only raw input signals.
- Input controller must not perform OS I/O; it maps raw inputs to `InputEvent`s.

No component may “reach across” boundaries by importing internal helpers from another
component unless explicitly designated as public API.

---

## 5. Practical “baseline console app” minimal set

If you want the smallest complete ASCII console game that still respects boundaries:

* Core ✅
* Renderer ✅ (pure)
* Presenter ✅ (stdout)
* Runtime ✅ (scripted required; interactive optional)
* CLI ✅
* Input Controller ✅ (maps keys to InputEvent)
* Input Driver ✅ (only if interactive mode is implemented)
* Persistence ❓ optional (replay implies it; config file implies it)

For Phase 2 baseline app (shell completeness 10–13), you can still keep **interactive input/presenter** out unless you add a dedicated gate for it (you already hinted at that in staging).

---

## 6. Recommended baseline console flow (who calls whom)

### 6.0 Composition and Execution Master Controllers

There are **two different “control centers”**, operating at different times:

#### 1. Composition-time: App Shell (CLI)

*(runs once, before execution starts)*

The CLI is the **composition root**.

It answers:

* *What mode are we running in?*
* *Which renderer / presenter / input stack do we use?*
* *Where does configuration come from?*
* *Are we running scripted, replay, or interactive?*

It does:

* parse arguments,
* load config / replay via Persistence,
* construct:
    * runtime,
    * renderer,
    * presenter,
    * input driver + controller,
* inject all dependencies into runtime,
* then **hands off control**.

After this point, the CLI is done.

---

#### 2. Execution-time: Runtime

*(runs the entire program lifetime)*

Once started, **runtime is the hub-and-spokes controller**.

It owns:

* the tick loop,
* the current `GameState`,
* input collection timing,
* calling `step()` exactly once per tick,
* calling renderer,
* delegating output to presenter,
* termination conditions.

During execution:

**Data Flow**

```
Input Driver  →  
                \
Input Controller → Runtime → Core → Renderer → Presenter
```

**Control Flow**

```
                +------------------+
                |   Input Driver   |
                +------------------+
                         |
                         v
                +------------------+
                | Input Controller |
                +------------------+
                         |
                         v
+--------+      +------------------+      +----------+
|  Core  | <--- |     Runtime      | ---> | Renderer |
+--------+      +------------------+      +----------+
                         |
                         v
                +------------------+
                |    Presenter     |
                +------------------+
```

Runtime is the sole execution coordinator; all other components are dependencies invoked by runtime and must not invoke each other’s internal logic.

---

### 6.1 `run` (interactive)

1. **CLI**
    * parse args
    * choose mode `run`
    * call `persistence.load_config(path)` (optional)
    * select renderer + presenter + input driver/controller
    * instantiate runtime with explicit dependencies
    * call `runtime.run_interactive(...)`
2. **Runtime**
    * tick loop
    * poll input driver → controller → `InputEvent`s
    * call `core.step()` once/tick
    * call `renderer.render(state) -> str`
    * call `presenter.present(frame)`
    * terminate on game over / user exit condition
3. **Persistence (optional)**
    * maybe save high score / config (but only if spec says)

```
CLI (composition root)
 ├─ loads config / replay (Persistence)
 ├─ wires components
 └─ hands control to Runtime

Runtime (orchestrator)
 ├─ owns tick loop
 ├─ calls Core.step()
 ├─ calls Renderer.render()
 └─ delegates I/O to Presenter / Input stack

Core (pure)
 └─ authoritative simulation
```

**Why CLI loads config here:** because config affects *composition* (renderer choice, interactive tick rate, input mapping), which are shell decisions.

---

### 6.2 `script` (virtual time)

1. **CLI**
    * parse args
    * choose mode `script`
    * load config (optional)
    * load script inputs (could be from file) via persistence or simple file read helper
    * instantiate runtime in scripted mode
2. **Runtime**
    * apply per-tick input lists
    * step/render/present per spec cadence (maybe presenter optional; could print each frame)
3. **Persistence**
    * optional: save transcript/log/output

---

### 6.3 `replay`

1. **CLI**
    * parse args
    * choose mode `replay`
    * `persistence.load_replay(path)` **must happen before runtime** (strict validation belongs here or in replay loader)
    * instantiate runtime with replay adapter / scripted input provider
2. **Runtime**
    * executes replay tick-by-tick deterministically

**Why not runtime loads replay:** because replay loading is *I/O + validation policy*. Runtime should receive already-validated replay data (or a “tick input provider” object that guarantees validity).

---

## 7. Delivery staging

The recommended staged expansion beyond the pure core:

1. **Core + tests** (Gates 0–6)
2. Optional: **core extensions** (Gates 7–9)
3. **ASCII renderer** (Gate 10)
4. **Scripted runtime** (Gate 11)
5. **CLI** (Gate 12)
6. **Replay** (Gate 13)
7. Optional: **interactive runtime + terminal I/O adapters** (input driver + presenter)

---

## 8. Skill mapping note (non-normative)

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
