---
name: DECOMPOSITION.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# DECOMPOSITION

**System Decomposition and Component Responsibilities (Normative)**

## 1. Purpose

This document defines the authoritative decomposition of the Tetris application into components.

It exists to:

- make responsibilities and boundaries explicit,
- prevent core/engine contamination with UI or platform concerns,
- enable role-based agent skills aligned to components,
- support incremental delivery beyond the pure core.

If a behavior or responsibility is not assigned here, it must not be implemented ad hoc.

---

## 2. Top-level decomposition

The system is decomposed into the following components:

1. **Core (Engine)**
2. **Presentation (Renderer)**
3. **Input (Controller)**
4. **Runtime (Game Loop / Orchestrator)**
5. **App Shell (CLI / Entrypoints)**
6. **Persistence (Optional)**
7. **Test & Evaluation Harness**
8. **Telemetry / Observability (Optional)**

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

- No rendering
- No real-time scheduling
- No keyboard polling
- No OS/window integration
- No file IO by default

---

### 3.2 Presentation (Renderer)

**Location:** `tetris/src/tetris/rendering/` (module namespace reserved)

**Responsibilities**

- Convert a `GameState` into a presentable representation.
- Support at least one "view":
    - **ASCII renderer** for terminal display (MVP-friendly, dependency-light)

Optional later:

- a graphical renderer (separate module / optional dependency)

**Explicit non-responsibilities**

- Must not modify game state.
- Must not implement game rules.
- Must not perform time stepping.

---

### 3.3 Input (Controller)

**Location:** `tetris/src/tetris/input/` (module namespace reserved)

**Responsibilities**

- Map platform/user interactions into `InputEvent` sequences per tick.
- Implement key repeat (if desired) *outside* the core.

MVP target:

- terminal input mapping sufficient for manual play OR scripted input.

**Explicit non-responsibilities**

- Must not implement collision/movement/rotation logic.
- Must not mutate game state directly.

---

### 3.4 Runtime (Game Loop / Orchestrator)

**Location:** `tetris/src/tetris/runtime/` (module namespace reserved)

**Responsibilities**

- Own the "tick clock":
    - choose tick rate (e.g., 60 ticks/sec) for interactive play
    - call `step(state, inputs, config)` once per tick
- Coordinate:
    - input acquisition
    - rendering
    - state progression
    - termination conditions

MVP target:

- deterministic loop where tick rate can be:
    - real-time (sleep-based), or
    - virtual time (step-by-step), or
    - scripted (no sleeps).

**Explicit non-responsibilities**

- Must not re-implement gravity rules (core already does).
- Must not contain game logic beyond orchestration.

---

### 3.5 App Shell (CLI / Entrypoints)

**Location:** `tetris/src/tetris/__main__.py` and/or `tetris/src/tetris/cli.py`

**Responsibilities**

- Parse args and choose mode:
    - run interactive terminal game
    - run scripted simulation
    - dump state snapshots
    - run quick sanity checks

**Explicit non-responsibilities**

- No implementation of core rules.
- No tests (tests live in `tetris/tests/`).

---

### 3.6 Persistence (Optional)

**Location:** `tetris/src/tetris/persistence/` (reserved)

**Responsibilities**

- Save/load:
    - high scores (if enabled),
    - configuration,
    - optionally deterministic replay traces (inputs + seed).

**Constraint**

- Persistence must not affect determinism of the core.

---

### 3.7 Test & Evaluation Harness

**Location:** `tetris/tests/` plus optional `eval/` (reserved)

**Responsibilities**

- Implement all oracles in `CORE_TEST_ORACLE.md`.
- Provide regression tests that enforce:
    - determinism,
    - invariants,
    - API compatibility.

Optional:

- scenario-based "agent evaluation" tasks and reports.

---

### 3.8 Telemetry / Observability (Optional)

**Location:** `tetris/src/tetris/telemetry/` (reserved)

**Responsibilities**

- Collect:
    - step events,
    - performance counters,
    - debug traces,
      without mutating logic.

---

## 4. Interfaces between components

The only allowed cross-component interfaces:

- Runtime -> Core:
    - `new_game(config)`
    - `step(state, inputs, config)`
- Runtime -> Input:
    - `poll_inputs(...) -> tuple[InputEvent, ...]`
- Runtime -> Renderer:
    - `render(state) -> str` (ASCII MVP)
- CLI -> Runtime:
    - `run(...)` entrypoints

No component may "reach across" boundaries by importing internal helpers from another component unless explicitly designated as public API.

---

## 5. Delivery staging

The recommended staged expansion beyond core:

1. **Core + tests** (Gates 0-6)
2. **ASCII renderer** (view only)
3. **Scripted runtime** (no real-time) to support reproducible replays
4. **Interactive runtime + input mapping**
5. Optional: persistence (high scores / replay traces)
6. Optional: graphical renderer

---

## 6. Skill mapping note (non-normative)

Agent skills should map to roles that primarily "own" one component:

- core logic
- test generation
- runtime/orchestration
- renderer
- input/controller
- CLI integration
- refactoring and bugfixing

This document provides the canonical component boundaries those roles must respect.

---
