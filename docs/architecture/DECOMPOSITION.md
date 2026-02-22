---
doc_id: DECOMPOSITION
name: DECOMPOSITION.md
title: System Decomposition and Component Responsibilities
status: active
authority: normative
description: Explicit component decomposition and responsibility boundaries.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [ARCHITECTURE]
---

# DECOMPOSITION

**System Decomposition and Component Responsibilities (Normative)**

---

## 1. Purpose

This document builds on prior developed tentative `ARCHITECTURE.md` and defines the **authoritative decomposition** of the Tetris application into components and assigns **explicit responsibility boundaries** to each.

It exists to:

- make responsibilities and boundaries explicit,
- prevent core/engine contamination with UI, timing, or platform concerns,
- enable role-based agent skills aligned to components,
- support incremental delivery beyond the pure core.

If a behavior or responsibility is not assigned here, it must not be implemented ad hoc.

This document is **normative** and applies to all acceptance gates.

---

## 2. Top-level decomposition

This decomposition is a **concrete realization** of the architectural model defined in `ARCHITECTURE.md` and the operational enforcement of the architectural contract. The system follows a **Functional Core / Imperative Shell** architecture:

* The **Functional Core** is the authoritative deterministic simulation.
* The **Shell** surrounds the core and handles orchestration, presentation, I/O, configuration, and integration concerns.

This section translates that architectural intent into explicit system components with strict boundaries.

---

### 2.1. Core (Engine)

The **core** is the authoritative simulation.

* It defines *all* game state and state transitions.
* It is deterministic, side-effect-free, and testable in isolation.
* It exposes a minimal public API (`new_game`, `step`) and nothing more.

The core **never** performs I/O, rendering, timing, or platform interaction.

---

### 2.2. Renderer (pure)

The **renderer** is a *pure presentation transformer*.

* Convert a `GameState` into a presentable representation:
  `render(state: GameState) -> str`
* formats state,
* applies presentation rules,
* produces deterministic output.

Rendering is **representation**, not display. The renderer does not define game rules and does not evolve state.

---

### 2.3. Terminal Presenter (I/O)

The **presenter** is responsible for *emitting rendered output* to a concrete medium (e.g. a terminal).

* consumes renderer output
* performs I/O
* has no knowledge of game rules or state evolution
* clear screen / position cursor
* print frame
* flush
* optionally throttle output rate (but timing belongs in runtime)
* handle terminal sizing quirks if supported (or explicitly forbid them)

---

### 2.4. Input Driver (I/O)

The **input driver** interfaces with the operating system or environment.

* read raw input events (keyboard, stdin, etc.)
* perform non-blocking polling if required
* translate raw keys to higher-level signals (or hand raw keys to controller)

---

### 2.5. Input Controller (mapping / policy)

The **input controller** maps input signals to game-level intent.

* map keys to `InputEvent`
* enforce per-tick semantics (no implicit repeats unless specified)
* possibly handle key debouncing/repeat policy (subject to specification constraints)

The controller does not evolve state; it prepares inputs for the core.

---

### 2.6. Runtime (Game Loop / Orchestrator)

The **runtime** coordinates execution.

* maintain the current `GameState`
* schedule ticks (real-time or virtual-time)
* collect inputs via input driver + controller
* call `step()` exactly once per tick
* call the renderer
* delegate output to the presenter
* detect termination

The runtime orchestrates; it does not define rules. Runtime consumes already-resolved `core_config` / `shell_config` and already-instantiated dependencies.
It does not discover configuration or load files.

---

### 2.7. App Shell (CLI / Entrypoints)

The **app shell** is the user-facing entry layer.

The CLI is the *composition root*.

* parse command-line arguments
* select execution mode (run / script / replay)
* wire components together
* configure runtime and dependencies
* select renderer/presenter/input driver

The CLI contains **no game logic** and **no rendering semantics**.

---

### 2.8. Persistence (Optional)

Persistence supports durable data such as:

* high scores
* configuration
* deterministic replay traces

Persistence is invoked by the **composition root (CLI)** for loading configuration and replay/script inputs. It may also be used by runtime only for explicitly specified run outputs (e.g., saving replays), preferably via injected sinks.

---

### 2.9. Test & Evaluation Harness

The test harness enforces correctness. It validates component behavior against specification-defined proof obligations.

---

### 2.10. Telemetry / Observability (Optional)

Telemetry collects diagnostic data without affecting behavior. It must not alter determinism or semantic correctness.

---

### Notes

* The **core** is a pure deterministic simulation; all I/O and timing live outside it.
* The **renderer** produces a representation of state; the **presenter** performs output.
* Each component has a strict responsibility boundary defined in this document.

---

## 3. Development domains

The architectural model (Core / Shell) and the concrete decomposition above give rise to logical development domains, structural development partitions derived directly from component boundaries. Each domain incorporates one or more system components (or well-defined behavioral extensions within a component) forming a high-level logical development block. These blocks can then be used by governance documents (L1 layer) to define high-level development strategy.

---

### 3.1. `CORE`

Includes:

* Core (Engine)

This domain governs:

* simulation state,
* state transitions,
* deterministic rule evaluation,
* the public simulation API.

It is the authoritative behavioral domain of the system.

The Core defines the **baseline semantic contract** of the application: the minimal, fully specified rule set and state model required to represent canonical Tetris behavior under deterministic execution. The Core domain must remain:

* deterministic,
* side-effect free,
* isolated from I/O and orchestration concerns,
* stable once baseline behavior is accepted.

Any optional mechanics, semantic extensions, or advanced features that go beyond the baseline semantic contract must be developed under `CORE_EXTENSIONS`, with explicit specification and governance.

---

### 3.2. `SHELL_BASELINE`

Includes:

* Renderer
* Runtime
* App Shell (CLI)
* Persistence (replay/config aspects)
* Input Driver
* Input Controller
* Presenter

This domain governs:

* orchestration
* presentation
* I/O
* composition
* deterministic execution wrapping

This is the canonical minimal deterministic wrapper. It must never redefine simulation rules.

---

### 3.3. `CORE_EXTENSIONS`

Includes:

* Optional mechanics implemented inside Core (e.g., hold, advanced scoring modes)
* Strictness and invariant enforcement extensions
* Additional deterministic features that extend the Core while preserving its architectural guarantees (determinism, isolation, API discipline)

This domain represents controlled expansion of the Core component beyond the baseline semantic contract.

Two categories of extensions are recognized:

1. **Backward-compatible extensions**
   Features that extend Core behavior without altering the previously established baseline semantic contract. These extensions:
    - preserve existing rule semantics,
    - preserve previously valid state transitions,
    - do not invalidate existing deterministic guarantees,
    - remain compatible with previously accepted specifications and tests.
2. **Versioned semantic extensions**
   Features that modify or extend baseline semantics in a way that changes the authoritative rule set or state model. Such extensions:
    - amend the baseline semantic contract,
    - may require updates to state representation or API,
    - may require updated rendering, replay, or persistence handling,
    - must be explicitly specified and versioned.

CORE_EXTENSIONS must not silently alter previously established baseline behavior. Any semantic modification must be:

1. Explicitly specified,
2. Versioned or otherwise compatibility-governed,
3. Reflected in the relevant L3 specifications and L4 proof obligations.

Although structurally part of the Core component, extensions are developed only after the baseline Core functionality is fully established.

Example:

- Introducing colored tetrominoes extends the state model and therefore constitutes a versioned semantic extension. It must be explicitly specified and governed rather than implicitly introduced.

---

### 3.4. `SHELL_VARIANTS`

Includes:

* Alternative renderers
* Alternative runtimes
* Alternative presenters
* Alternative shell interfaces

Variants must:

* preserve the Core contract,
* not modify baseline semantics,
* remain replaceable at the composition root.

Variants extend the Shell and must not weaken guarantees established by SHELL_BASELINE.  
For example, baseline shell might render the board using classic ACSII characters, while a variant shell might use solid filled rectangles (in such a case, background and foreground colors are set the same and specific characters used become irrelevant).

---

### 3.5. `DOC_INFRA`

Includes:

* Documentation system
* Acceptance gates
* Test oracles
* Inventory and schema
* Governance artifacts

This domain governs specification and validation infrastructure.

It does not define runtime behavior.

---

### 3.6. `BENCHMARK`

Includes:

* Evaluation harness scaling
* Replay corpora
* Automated scoring systems
* Agent evaluation tooling

This domain operates above the baseline system to evaluate it.

---

## 4. Component responsibilities and constraints

### 4.1 Core (Engine)

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

### 4.2 Renderer (pure)

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

### 4.3 Terminal Presenter (I/O)

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

### 4.4 Input Driver (I/O)

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

### 4.5 Input Controller (mapping / policy)

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

### 4.6 Runtime (Game Loop / Orchestrator)

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

### 4.7 App Shell (CLI / Entrypoints)

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

### 4.8 Persistence (Optional)

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

### 4.9 Test & Evaluation Harness

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

### 4.10 Telemetry / Observability (Optional)

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

# 5. Component interaction model

This section defines the **allowed interaction surfaces** between components.

The interaction model follows directly from the Core / Shell architecture defined earlier:

* The Core exposes a minimal simulation API.
* The Runtime orchestrates execution.
* Presentation and I/O layers remain strictly downstream.
* The CLI is the composition root.
* No component may bypass its designated boundary.

---

## 5.1 Allowed cross-component interfaces (normative)

Only the following directional interfaces are permitted:

### 5.1.1 Runtime interactions

* **Runtime → Core**
    * `new_game(config)`
    * `step(state, inputs, config)`
* **Runtime → Input Driver**
    * `poll_raw_inputs(...) -> <raw input representation>`
* **Runtime → Input Controller**
    * `poll_inputs(...) -> tuple[InputEvent, ...]`
* **Runtime → Renderer**
    * `render(state) -> str`
* **Runtime → Presenter**
    * `present(frame: str) -> None`

---

### 5.1.2 Composition root interactions

* **CLI → Runtime**
    * `run(...)` entrypoints
* **CLI → Persistence**
    * `load_config(...)`
    * `load_replay(...)`

CLI may wire dependencies but must not implement simulation or rendering semantics.

---

## 5.2 Structural interface constraints (normative)

The following invariants enforce architectural separation:

* Presenter must not receive `GameState`; it receives only a rendered `frame: str`.
* Renderer must not perform I/O; it returns only a `str`.
* Input Driver must not return `InputEvent`; it returns only raw input signals.
* Input Controller must not perform OS I/O; it maps raw signals to `InputEvent`.
* Runtime must not implement or duplicate rule logic.
* CLI must not implement game logic or rendering semantics.

No component may bypass boundaries by importing internal helpers from another component unless explicitly designated as public API.

---

## 5.3 API evolution policy (normative)

Cross-component APIs must support controlled forward evolution.

When appropriate:

* Prefer structured configuration objects over positional parameters.
* Prefer keyword-based extensibility with validated `**kwargs`.
* Design signatures to allow additive evolution without breaking existing callers.

Extensibility must remain:

* explicit,
* documented,
* validated,
* type-safe.

APIs must not silently accept unknown parameters or weaken contract clarity.

---

# 5.4 Import discipline (normative)

Architectural boundaries are enforced via import constraints. Violations constitute **responsibility leakage** and fail Gate 0.

---

## 5.4.1 Component-to-component import constraints

> Notation: “A → B = forbidden” means “modules in A must not import modules in B”.

| Importer                                         | Forbidden imports                                                                  | Rationale                                                                          |
| ------------------------------------------------ | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Core (`tetris.core`)**                         | `runtime`, `cli`, `rendering`, `presentation`, `input`, `persistence`, `telemetry` | Core must remain pure and environment-independent.                                 |
| **Renderer (`tetris.rendering`)**                | `runtime`, `cli`, `presentation`, `input`, `persistence`, `telemetry`              | Renderer is pure; must not perform I/O or depend on execution mode.                |
| **Presenter (`tetris.presentation`)**            | `core`, `runtime`, `cli`, `input`, `persistence`, `telemetry`                      | Presenter emits bytes; it must not interpret game semantics or control flow.       |
| **Input Driver (`tetris.input.driver`)**         | `core`, `runtime`, `cli`, `rendering`, `presentation`, `persistence`, `telemetry`  | Driver is raw I/O only; must not know game rules or orchestration.                 |
| **Input Controller (`tetris.input.controller`)** | `runtime`, `cli`, `rendering`, `presentation`, `persistence`, `telemetry`          | Controller is mapping/policy; must not become the orchestrator.                    |
| **Runtime (`tetris.runtime`)**                   | `cli`                                                                              | Runtime is not composition root.                                                   |
| **CLI (`tetris.cli` / `__main__`)**              | *(none beyond public APIs of components)*                                          | CLI is the composition root; it may import public entrypoints of other components. |
| **Persistence (`tetris.persistence`)**           | `runtime`, `cli`                                                                   | Persistence must not own control flow.                                             |
| **Telemetry (`tetris.telemetry`)**               | `runtime`, `cli`                                                                   | Telemetry must remain passive.                                                     |

Any violation is a Gate 0 failure regardless of functional correctness.

---

## 5.4.2 Explicitly allowed imports (positive list)

To remove ambiguity, the following cross-component imports are allowed:

* `runtime` may import:
    * `core` (public API only)
    * `rendering`
    * `presentation`
    * `input.controller`
    * `input.driver`
* `cli` may import:
    * `runtime`
    * `core` (types / defaults only)
    * `persistence`
    * `rendering`
    * `presentation`
    * `input.*`
* `rendering` may import:
    * `core` types only (e.g., `GameState`, enums)
    * Renderer must not import rule helpers or mutation logic.

Any import not covered above is forbidden unless this document is amended first.

---

## 5.4.3 Public vs internal API boundary

When importing across components:

* Only public API modules may be imported.
* Importing internal helpers across components is forbidden.

**Enforcement guidance (non-normative):**

* Prefer importing from a component package root.
* Use `__init__.py` re-exports to define public surface.
* Avoid deep internal module imports across component boundaries.

---

## 6. Practical “baseline console app” minimal set

Minimalistic complete ASCII console game that still respects boundaries:

```
tetris/src/tetris/
├── core/                # Pure deterministic simulation
├── rendering/           # Pure renderers (no I/O)
├── presentation/        # Output adapters (I/O)
├── input/               # Input subsystem
│   ├── controller.py
│   └── driver/
├── runtime/             # Game loop / orchestrator
├── cli.py               # Composition root
├── __main__.py
├── persistence/         # Optional
└── telemetry/           # Optional
```

| Component        | Comment                                                | Source package             |
| ---------------- | :----------------------------------------------------- | -------------------------- |
| Core             | ✅                                                      | `core/`                    |
| Renderer         | ✅ (pure)                                               | `rendering/`               |
| Presenter        | ✅ (stdout)                                             | `presentation/`            |
| Runtime          | ✅ (scripted required; interactive optional)            | `runtime/`                 |
| CLI              | ✅                                                      | `cli.py`, `__main__.py`    |
| Input Controller | ✅ (maps keys to InputEvent)                            | `input/controller.py`      |
| Input Driver     | ✅ (only if interactive mode is implemented)            | `input/driver/terminal.py` |
| Persistence      | ❓ optional (replay implies it; config file implies it) | `persistence/`             |

**Source layout**

```
tetris/src/tetris/
├── core/                # Pure deterministic simulation
│   ├── __init__.py
│   ├── state.py
│   ├── rules.py
│   ├── shapes.py
│   └── api.py
│
├── rendering/           # Pure renderers (no I/O)
│   ├── __init__.py
│   └── ascii.py
│
├── presentation/        # Output adapters (I/O)
│   ├── __init__.py
│   └── terminal.py
│
├── input/               # Input subsystem (split by responsibility)
│   ├── __init__.py
│   ├── controller.py    # Mapping / policy (pure-ish)
│   └── driver/          # I/O boundary
│       ├── __init__.py
│       └── terminal.py
│
├── runtime/             # Game loop / orchestrator
│   ├── __init__.py
│   └── loop.py
│
├── cli.py               # CLI wiring & entry logic
├── __main__.py          # python -m tetris
│
├── persistence/         # Optional, explicit
│   ├── __init__.py
│   ├── replay.py
│   └── config.py
│
└── telemetry/           # Optional, explicit
    ├── __init__.py
    └── trace.py
```

For Phase 2 baseline app (shell completeness 10–13), you can still keep **interactive input/presenter** out unless you add a dedicated gate for it (you already hinted at that in staging).

---

## 7. Recommended baseline console flow (who calls whom)

### 7.0 Composition and Execution Master Controllers

There are **two different “control centers”**, operating at different times:

#### 7.0.1. Composition-time: App Shell (CLI)

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

#### 7.0.2. Execution-time: Runtime

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

Runtime is the sole execution coordinator; all other components are dependencies invoked by runtime and must not invoke each other’s internal logic.

---

### 7.1 `run` (interactive)

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

### 7.2 `script` (virtual time)

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

### 7.3 `replay`

1. **CLI**
    * parse args
    * choose mode `replay`
    * `persistence.load_replay(path)` **must happen before runtime** (strict validation belongs here or in replay loader)
    * instantiate runtime with replay adapter / scripted input provider
2. **Runtime**
    * executes replay tick-by-tick deterministically

**Why not runtime loads replay:** because replay loading is *I/O + validation policy*. Runtime should receive already-validated replay data (or a “tick input provider” object that guarantees validity).

---

    ## 8. Delivery staging
    
    The recommended staged expansion beyond the pure core:
    
    1. **Core + tests** (Gates 0–6)
    2. Optional: **core extensions** (Gates 7–9)
    3. **ASCII renderer** (Gate 10)
    4. **Scripted runtime** (Gate 11)
    5. **CLI** (Gate 12)
    6. **Replay** (Gate 13)
    7. Optional: **interactive runtime + terminal I/O adapters** (input driver + presenter)

---
