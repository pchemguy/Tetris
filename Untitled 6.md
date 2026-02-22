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

#### Notes

* The **core** is a pure deterministic simulation; all I/O and timing live outside it.
* The **renderer** produces a representation of state; the **presenter** performs output.
* Each component has a strict responsibility boundary defined in this document.

---

## 3. Development domains

The architectural model (Core / Shell) and the concrete decomposition above give rise to logical development domains, structural development partitions derived directly from component boundaries. Each domain incorporates one or more system components (or well-defined behavioral extensions within a component) forming a high-level logical development block. These blocks can then be used by governance documents (L1 layer) to define high-level development strategy.

---

### `CORE`

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

### `SHELL_BASELINE`

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

### `CORE_EXTENSIONS`

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

### `SHELL_VARIANTS`

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

### `DOC_INFRA`

Includes:

* Documentation system
* Acceptance gates
* Test oracles
* Inventory and schema
* Governance artifacts

This domain governs specification and validation infrastructure.

It does not define runtime behavior.

---

### `BENCHMARK`

Includes:

* Evaluation harness scaling
* Replay corpora
* Automated scoring systems
* Agent evaluation tooling

This domain operates above the baseline system to evaluate it.

---
