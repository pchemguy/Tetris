## 2. Top-level decomposition

### 2.1 Architectural grounding (Core / Shell model)

This decomposition is a **concrete realization** of the architectural model defined in `ARCHITECTURE.md` and the operational enforcement of the architectural contract. The system follows a **Functional Core / Imperative Shell** architecture:

* The **Functional Core** is the authoritative deterministic simulation.
* The **Shell** surrounds the core and handles orchestration, presentation, I/O, configuration, and integration concerns.

This section translates that architectural intent into **explicit components with strict boundaries**.

---

### 2.2 System components

#### 2.2.1. Core (Engine)

The **core** is the authoritative simulation.

* It defines *all* game state and state transitions.
* It is deterministic, side-effect-free, and testable in isolation.
* It exposes a minimal public API (`new_game`, `step`) and nothing more.

The core **never** performs I/O, rendering, timing, or platform interaction.

---

#### 2.2.2. Renderer (pure)

The **renderer** is a *pure presentation transformer*.

* Convert a `GameState` into a presentable representation:
  `render(state: GameState) -> str`
* formats state,
* applies presentation rules,
* produces deterministic output.

Rendering is **representation**, not display. The renderer does not define game rules and does not evolve state.

---

#### 2.2.3. Terminal Presenter (I/O)

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

#### 2.2.4. Input Driver (I/O)

The **input driver** interfaces with the operating system or environment.

* read raw input events (keyboard, stdin, etc.)
* perform non-blocking polling if required
* translate raw keys to higher-level signals (or hand raw keys to controller)

---

#### 2.2.5. Input Controller (mapping / policy)

The **input controller** maps input signals to game-level intent.

* map keys to `InputEvent`
* enforce per-tick semantics (no implicit repeats unless specified)
* possibly handle key debouncing/repeat policy (subject to specification constraints)

The controller does not evolve state; it prepares inputs for the core.

---

#### 2.2.6. Runtime (Game Loop / Orchestrator)

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

#### 2.2.7. App Shell (CLI / Entrypoints)

The **app shell** is the user-facing entry layer.

The CLI is the *composition root*.

* parse command-line arguments
* select execution mode (run / script / replay)
* wire components together
* configure runtime and dependencies
* select renderer/presenter/input driver

The CLI contains **no game logic** and **no rendering semantics**.

---

#### 2.2.8. Persistence (Optional)

Persistence supports durable data such as:

* high scores
* configuration
* deterministic replay traces

Persistence is invoked by the **composition root (CLI)** for loading configuration and replay/script inputs. It may also be used by runtime only for explicitly specified run outputs (e.g., saving replays), preferably via injected sinks.

---

#### 2.2.9. Test & Evaluation Harness

The test harness enforces correctness. It validates component behavior against specification-defined proof obligations.

---

#### 2.2.10. Telemetry / Observability (Optional)

Telemetry collects diagnostic data without affecting behavior. It must not alter determinism or semantic correctness.

---

#### Notes

* The **core** is a pure deterministic simulation; all I/O and timing live outside it.
* The **renderer** produces a representation of state; the **presenter** performs output.
* Each component has a strict responsibility boundary defined in this document.

---

### 2.3 Development domains

The architectural model (Core / Shell) and the concrete decomposition above give rise to logical development domains, structural development partitions derived directly from component boundaries. Each domain incorporates one or more system components (or well-defined behavioral extensions within a component) forming a high-level logical development block. These blocks can then be used by governance documents (L1 layer) to define high-level development strategy.

---

#### `CORE`

Includes:

* Core (Engine)

This domain governs:

* simulation state
* state transitions
* deterministic rules
* public simulation API

It is the authoritative behavioral domain. The core includes minimalistic feature set necessary to define semantics of classic Tetris. Any semantic extensions or optional features should be included elsewhere (to be developed at later stages). At the same time, whenever possible, provisions should be made for backward compatible extensible APIs (such as explicit use of `*args` and `**kwargs` in signatures, using dictionaries where appropriate, and so on).

---

#### `SHELL_BASELINE`

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

#### `CORE_EXTENSIONS`

Includes:

* Optional mechanics implemented inside Core
* Strictness and invariant enforcement extensions
* Additional deterministic features that preserve baseline semantics
* Advanced optional features that may require extending baseline semantics

This domain modifies the Core but must not alter the baseline simulation contract, unless such a change is explicitly required according to associated specification. It is structurally part of Core, but any optional / advanced / extra features must be developed separately after baseline functionality is established. An example of a feature that will require amending baseline semantics is the use of colored tetrominoes.

---

#### `SHELL_VARIANTS`

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

#### `DOC_INFRA`

Includes:

* Documentation system
* Acceptance gates
* Test oracles
* Inventory and schema
* Governance artifacts

This domain governs specification and validation infrastructure.

It does not define runtime behavior.

---

#### `BENCHMARK`

Includes:

* Evaluation harness scaling
* Replay corpora
* Automated scoring systems
* Agent evaluation tooling

This domain operates above the baseline system to evaluate it.

---
