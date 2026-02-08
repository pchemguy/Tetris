
---

````md
# DECOMPOSITION

**System Decomposition and Component Responsibilities (Normative)**

---

## 1. Purpose

This document defines the **authoritative decomposition** of the Tetris application into
components and assigns **explicit responsibility boundaries** to each.

It exists to:

- make component responsibilities explicit and enforceable,
- prevent contamination of the core with UI, timing, or platform concerns,
- provide a stable basis for role-based agent skills,
- support incremental delivery from a pure core to a complete system.

If a behavior, responsibility, or interaction is not assigned here, it must **not** be
implemented ad hoc.

This document is **normative** and applies to all acceptance gates.

---

## 2. Top-level decomposition

The system is decomposed into a set of **explicitly separated components**, each with a
narrowly defined role. This separation is intentional and exists to preserve:

- determinism,
- testability,
- auditability,
- architectural clarity.

At a high level, the system consists of:

1. a **pure deterministic simulation core**,
2. **pure transformation components** (rendering),
3. **imperative I/O adapters** (input, presentation),
4. an **orchestrator** (runtime),
5. an **application shell** (CLI),
6. optional auxiliary subsystems,
7. a **test and evaluation harness**.

The components are:

---

### 1. **Core (Engine)**

The **core** is the authoritative simulation.

- Defines all game state and state transitions.
- Is deterministic, side-effect-free, and testable in isolation.
- Exposes a minimal public API (`new_game`, `step`) and nothing else.

The core **never** performs I/O, rendering, timing, or platform interaction.

---

### 2. **Renderer (pure)**

The **renderer** is a *pure presentation transformer*.

- Input: `GameState`
- Output: a representation (e.g. `str`)
- Example interface:

```python
render(state: GameState) -> str
```

The renderer:

* formats state according to presentation rules,
* produces deterministic output,
* has no side effects.

The renderer **does not**:

* write to stdout,
* clear the screen,
* animate,
* depend on timing or environment.

Rendering is **representation**, not display.

---

### 3. **Terminal Presenter (Output Adapter, I/O)**

The **presenter** emits rendered output to a concrete medium (e.g. a terminal).

Typical responsibilities include:

* clearing the screen or positioning the cursor,
* printing rendered frames,
* flushing output,
* handling terminal-specific mechanics (if supported).

The presenter:

* consumes renderer output,
* performs I/O,
* has no knowledge of game rules or state evolution.

If terminal quirks or resizing are unsupported, this must be **explicitly forbidden**.

---

### 4. **Input Driver (I/O)**

The **input driver** interfaces with the operating system or environment.

Responsibilities:

* read raw input events (keyboard, stdin, etc.),
* perform non-blocking polling if required,
* normalize platform-specific signals.

The input driver **does not** interpret game semantics.

It may return:

* raw key codes, or
* minimally normalized signals.

---

### 5. **Input Controller (mapping / policy)**

The **input controller** maps input signals to game-level intent.

Responsibilities:

* map keys or signals to `InputEvent`,
* enforce per-tick input semantics,
* apply input policy (e.g. no implicit repeats unless specified).

The input controller:

* is deterministic,
* does not mutate game state,
* does not implement game logic.

This separation prevents OS behavior from leaking into core semantics.

---

### 6. **Runtime (Game Loop / Orchestrator)**

The **runtime** coordinates execution.

Responsibilities:

* maintain the current `GameState`,
* schedule ticks (real-time or virtual-time),
* collect inputs via input driver + controller,
* call `step()` exactly once per tick,
* call the renderer,
* delegate output to the presenter,
* detect termination.

The runtime orchestrates; it does not define rules.

---

### 7. **App Shell (CLI / Entrypoints)**

The **app shell** is the user-facing entry layer.

Responsibilities:

* parse command-line arguments,
* select execution mode (run / script / replay),
* wire components together,
* configure runtime and dependencies.

The CLI contains **no game logic** and **no rendering semantics**.

---

### 8. **Persistence (Optional)**

Persistence supports durable data such as:

* high scores,
* configuration,
* deterministic replay traces.

Persistence must never affect core determinism.

---

### 9. **Test & Evaluation Harness**

The test harness enforces correctness.

Responsibilities:

* implement all test oracles,
* assert determinism and invariants,
* support regression and agent evaluation.

This subsystem is authoritative for correctness claims.

---

### 10. **Telemetry / Observability (Optional)**

Telemetry collects diagnostic data without affecting behavior.

Responsibilities:

* logging,
* counters,
* traces.

Telemetry must be strictly observational.

---

## 3. Component responsibilities and constraints

### 3.1 Core (Engine)

**Location:** `tetris/src/tetris/core.py` (and submodules under `tetris/src/tetris/`)

**Responsibilities**

* Implement the full deterministic simulation defined by:

  * `GAME_RULES.md`
  * `GAME_STATE.md`
  * `SHAPES_AND_ROTATIONS.md`
  * `INPUT_MODEL.md`
  * `ERROR_HANDLING.md`
  * `CORE_API.md`
* Provide `new_game()` and `step()` as the only supported evolution interface.
* Maintain determinism and immutability guarantees.

**Explicit non-responsibilities**

* Rendering or formatting
* Timing or sleeping
* Keyboard or OS input
* File or network I/O

---

### 3.2 Renderer (pure)

**Location:** `tetris/src/tetris/rendering/` (namespace reserved)

**Responsibilities**

* Convert `GameState` into a representation.
* Provide at least one renderer:

  * ASCII renderer (baseline).

**Explicit non-responsibilities**

* Output or display
* State mutation
* Timing or animation
* Rule implementation

---

### 3.3 Terminal Presenter (I/O)

**Location:** `tetris/src/tetris/presentation/` (namespace reserved)

**Responsibilities**

* Emit rendered output to a terminal or output stream.
* Handle terminal I/O mechanics if supported.

**Explicit non-responsibilities**

* Rendering semantics
* Game logic
* State mutation

---

### 3.4 Input Driver (I/O)

**Location:** `tetris/src/tetris/input/driver/` (namespace reserved)

**Responsibilities**

* Acquire raw input from environment.
* Perform platform-specific polling.

**Explicit non-responsibilities**

* Input semantics
* Game logic
* State mutation

---

### 3.5 Input Controller (mapping / policy)

**Location:** `tetris/src/tetris/input/controller.py`

**Responsibilities**

* Map raw input to `InputEvent`.
* Enforce per-tick input rules.

**Explicit non-responsibilities**

* Core logic
* Rendering
* I/O

---

### 3.6 Runtime (Game Loop / Orchestrator)

**Location:** `tetris/src/tetris/runtime/` (namespace reserved)

**Responsibilities**

* Tick scheduling.
* Input → core → rendering → presentation coordination.
* Termination handling.

**Explicit non-responsibilities**

* Game rule logic
* Rendering semantics
* Input acquisition logic

---

### 3.7 App Shell (CLI / Entrypoints)

**Location:** `tetris/src/tetris/__main__.py` and/or `tetris/src/tetris/cli.py`

**Responsibilities**

* Mode selection and wiring.
* Argument parsing.

**Explicit non-responsibilities**

* Core logic
* Rendering logic
* Testing

---

### 3.8 Persistence (Optional)

**Location:** `tetris/src/tetris/persistence/` (reserved)

**Responsibilities**

* Save/load auxiliary data.

**Constraint**

* Must not affect core determinism.

---

### 3.9 Test & Evaluation Harness

**Location:** `tetris/tests/` (plus optional `eval/`)

**Responsibilities**

* Enforce all test oracles.
* Validate determinism and invariants.

---

### 3.10 Telemetry / Observability (Optional)

**Location:** `tetris/src/tetris/telemetry/` (reserved)

**Responsibilities**

* Collect diagnostics without mutation.

---

## 4. Interfaces between components

The only allowed cross-component interfaces are:

* **Runtime → Core**

  * `new_game(config)`
  * `step(state, inputs, config)`
* **Runtime → Input Controller**

  * `poll_inputs(...) -> tuple[InputEvent, ...]`
* **Runtime → Renderer**

  * `render(state) -> str`
* **Runtime → Presenter**

  * `present(rendered: str) -> None`
* **CLI → Runtime**

  * `run(...)`

No component may import internal helpers from another component unless explicitly designated
as public API.

---

## 5. Delivery staging

Recommended staged expansion:

1. Core + tests (Gates 0–6)
2. ASCII renderer (pure)
3. Scripted runtime (virtual-time)
4. Interactive runtime + input driver/controller + presenter
5. Optional persistence
6. Optional alternative renderers

---

## 6. Skill mapping note (non-normative)

Agent skills should map primarily to a single component:

* core logic
* test generation
* runtime/orchestration
* renderer
* presenter
* input driver/controller
* CLI integration
* refactoring and bugfixing

This document defines the canonical boundaries those roles must respect.

---

```

If you want next, we can:
- align `ARCHITECTURE.md` wording with this decomposition,
- tighten `RUNTIME_SPEC.md` cross-references,
- or extract a **component responsibility table** for quick audits.
```
