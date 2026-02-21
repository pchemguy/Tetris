---
doc_id: L3_BEHAVIOR
name: L3_BEHAVIOR.md
title: L3 — Behavioral Specifications (Component Contracts)
status: active
authority: normative
description: Defines all normative behavioral specifications for core and shell components.
references:
  - GAME_STATE
  - INPUT_MODEL
  - ERROR_HANDLING
  - SHAPES_AND_ROTATIONS
  - CORE_API
  - RUNTIME_SPEC
  - RENDERING_SPEC
  - CLI_SPEC
  - REPLAY_SPEC
  - RENDERER_API
  - RUNTIME_API
  - CONFIG_API
  - INPUT_DRIVER_API
  - PRESENTER_API
---

# L3 — Behavioral Specifications

## Document Index

### Core contracts

**Directory**: `docs/specs/core/`

| Title              | Filename                  | Function / Role                                  |
| ------------------ | ------------------------- | ------------------------------------------------ |
| Game Rules         | `GAME_RULES.md`           | Behavioral specification (what the game does)    |
| Game State Model   | `GAME_STATE.md`           | Deterministic state machine and step semantics   |
| Input Model        | `INPUT_MODEL.md`          | Input representation and tick ordering           |
| Error Handling     | `ERROR_HANDLING.md`       | Rejection vs error policy; invariant enforcement |
| Shapes & Rotations | `SHAPES_AND_ROTATIONS.md` | Exact tetromino geometry and rotations           |


---

### Shell contracts

**Directory**: `docs/specs/shell/`

| Title                            | Filename            | Function / Role                                                |
| -------------------------------- | ------------------- | -------------------------------------------------------------- |
| Runtime Specification            | `RUNTIME_SPEC.md`   | Tick loop, execution modes, and orchestration rules            |
| Rendering Specification          | `RENDERING_SPEC.md` | ASCII renderer contract and output format                      |
| CLI Specification                | `CLI_SPEC.md`       | Command-line interface and entrypoint behavior                 |
| Replay Specification             | `REPLAY_SPEC.md`    | Deterministic replay and evaluation format                     |


---

### API specifications

**Directory**: `docs/specs/api/`

| Title                            | Filename          | Function / Role                                                |
| -------------------------------- | ----------------- | -------------------------------------------------------------- |
| Core API                         | `CORE_API.md`     | Python-level public API contract                               |
| Renderer interface specification | `RENDERER_API.md` | Renderer API and its strict purity guarantees                  |
| Runtime interface specification  | `RUNTIME_API.md`  | Runtime API and its role as the execution-time orchestrator    |
| Configuration API                | `CONFIG_API.md`   | Typed configuration model used to parameterize the application |

---

### IO API specifications

**Directory**: `docs/specs/io/`

| Title                                | Filename              | Function / Role                                           |
| ------------------------------------ | --------------------- | --------------------------------------------------------- |
| Input driver interface specification | `INPUT_DRIVER_API.md` | Input Driver API and its strict responsibility boundaries |
| Presenter interface specification    | `PRESENTER_API.md`    | Presenter API and its strict responsibility boundaries    |

---

## Detailed description

These documents define **what the system does**, component by component. They are **normative behavioral contracts**, not implementation guides. They answer questions such as:

* What is the exact behavior?
* What inputs are valid?
* What outputs or state transitions are permitted?
* What is explicitly out of scope?

This class includes:

* core / engine behavior specifications,
* shell-level behavior specifications (runtime, rendering, CLI, replay).

Behavior must not be inferred from tests, examples, or implementation patterns; only explicit specification text is authoritative. If a behavior is not defined in a specification, it **must not be implemented**.

---

### Core vs shell distinction (what is inside vs outside)

The system is intentionally split into:

* a **pure deterministic core** (the simulation), and
* **shell components** around it (runtime, rendering, CLI, replay).

This separation is fundamental:

* The **core** defines game state evolution and must remain deterministic, side-effect-free, and testable in isolation.
* The **shell** exists to execute, observe, and interact with the core without re-implementing its logic.

This distinction is enforced by:

* architecture and decomposition documents,
* acceptance gates,
* component-specific test oracles.

---

### Core / engine contracts

#### `GAME_RULES.md` — Behavioral specification

**Role**  
Defines **what** the game does.

**Contents**

- Playfield dimensions
- Tetromino set
- Rotation rules and wall kicks
- Gravity, locking, and line clearing
- Scoring and level progression
- RNG model (7-bag)
- Game over conditions
- Explicit out-of-scope features

**Usage**

- Agents must treat this as binding behavioral law.
- If a behavior is not specified here, it must not be implemented.
- Humans should modify this document first when changing gameplay semantics.

---

#### `GAME_STATE.md` — State machine and step semantics

**Role**  
Defines **how** the game evolves deterministically.

**Contents**

- Exact state fields
- Tick model and gravity counters
- Step function ordering
- Locking, clearing, spawning transitions
- Invariants that must always hold

**Usage**

- This is the primary reference for implementing `step()`.
- Tests should assert transitions defined here, not inferred behavior.
- Agents must not invent alternative time models or implicit clocks.

---

#### `INPUT_MODEL.md` — Input semantics

**Role**  
Defines **how inputs are applied** per tick.

**Contents**

- Discrete input events
- Per-tick ordered input lists
- No implicit key repeat
- Hard-drop special handling
- Hold constraints

**Usage**

- Prevents UI assumptions leaking into the core.
- Ensures input ordering is explicit and testable.
- Agents must not batch or normalize inputs unless explicitly stated.

---

#### `ERROR_HANDLING.md` — Errors vs rejections

**Role**  
Defines **failure vs rejection semantics**.

**Contents**

- Definition of rejected actions
- Definition of errors
- Strict vs permissive modes
- Invariant enforcement rules

**Usage**

- Essential for evaluating agent discipline.
- Prevents silent corruption and “best-effort” guessing.
- Humans may relax strictness deliberately, but only via config.

---

#### `SHAPES_AND_ROTATIONS.md` — Geometry truth table

**Role**  
Defines **exact tetromino geometry** and rotation states.

**Contents**

- Explicit block coordinates for every piece and rotation
- No procedural rotation allowed
- Mandatory invariants

**Usage**

- Eliminates all geometric interpretation freedom.
- Agents must implement shapes verbatim.
- Geometry tests should reference this document directly.

---

#### `CORE_API.md` — Python API contract

**Role**  
Defines the **only supported public core API** for the core.

**Contents**

- Module path and layout
- Enums and dataclasses
- `new_game()` and `step()` contracts
- Immutability requirements
- RNG and serialization expectations

**Usage**

- Agents must not invent alternative APIs.
- Humans reviewing code should compare signatures against this doc first.
- Tests should assume this API and no other.

---

### Shell contracts

#### `RUNTIME_SPEC.md` — Execution model and orchestration

**Role**  
Defines **how the system runs over time** outside the core.

**Contents**

* Tick lifecycle
* Scripted (virtual-time) execution mode
* Optional interactive (real-time) execution mode
* Determinism guarantees
* Error propagation rules

**Usage**

* Governs all orchestration logic.
* Ensures that determinism is preserved for testing and evaluation.
* Agents implementing runtimes must follow this document strictly.
* Humans should extend this document before adding new runtime modes.

---

#### `RENDERING_SPEC.md` — Presentation contract

**Role**  
Defines the **ASCII rendering contract** for the application.

**Contents**

* Renderer interface
* Board layout and symbols
* Metadata display (score, level, lines, next, hold)
* Game-over rendering
* Explicit prohibitions (no animation, no timing, no mutation)

**Usage**

* Enables snapshot-based rendering tests.
* Ensures rendering remains a pure function of state.
* Prevents UI logic from contaminating core or runtime.
* Humans may extend this specification for additional renderers (e.g., graphical, web) only by adding separate specification documents.

---

#### `CLI_SPEC.md` — Command-line interface

**Role**  
Defines the **command-line surface** of the application.

**Contents**

* Entry points (`python -m tetris`)
* Supported commands (`run`, `script`, `replay`)
* Flags and options
* Exit codes and error handling expectations

**Usage**

* Keeps CLI logic thin and declarative.
* Prevents game logic from being implemented in argument parsing.
* Agents implementing CLI features must follow this document exactly.
* Humans should update this document before adding or changing commands.

---

#### `REPLAY_SPEC.md` — Deterministic replay and evaluation

**Role**  
Defines a **deterministic replay format** for evaluation, debugging, and regression testing.

**Contents**

* Replay file schema
* Input-per-tick semantics
* Validation rules
* Determinism guarantees

**Usage**

* Enables exact reproduction of runs.
* Forms the backbone of agent evaluation and auditing.
* Allows separation of *what happened* from *how it was rendered*.
* Humans may evolve the replay format, but versioning must be explicit.

---
