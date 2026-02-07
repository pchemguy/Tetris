---
name: PROJECT.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---
# PROJECT.md

## 1. Project overview

This project develops and evaluates a **prompting system for agentic software development**.

The reference implementation target is **classic Tetris**, chosen not as a game project per se, but as a compact, well-understood system that stresses:

- deterministic state machines,
- strict rule adherence,
- geometry and collision logic,
- time-stepped simulation,
- incremental feature integration,
- comprehensive test oracles.

The primary deliverable of this repository is **not** “a Tetris game”, but a **set of development contracts, specifications, and acceptance gates** that allow rigorous evaluation of whether an AI agent can:

- discover and obey documentation,
- implement incrementally without guessing,
- stop and escalate when blocked,
- produce auditable, deterministic software artifacts.

Human developers remain ultimately responsible for correctness and maintenance, but the project is explicitly designed to be **AI-readable, AI-actionable, and AI-auditable**.

---

## 2. Repository layout (high level)

```
.
├── docs/                  # Normative development specifications (this project’s core)
├── tetris/src/tetris/     # Pure Python implementation package
├── .agent/skills/         # Agent skills (plan / implement / review units)
├── PROJECT.md             # This document (primary entry point)
└── README.md              # Optional human-facing wrapper (may delegate to PROJECT.md)

```

The **docs/** directory is authoritative.  
Code exists to satisfy the docs — not the other way around.

---

## 3. Development documentation index (synopsis)

The following table provides a **synoptic index** of all normative development documents.
These documents reside under `/docs/`, with the exception of `PROJECT.md` (this file) placed in the root.  
Agents are expected to **discover and reason over all of them**, not just one.  

|        | Title                        | Filename                   | Function / Role                                     |
| ------ | ---------------------------- | -------------------------- | --------------------------------------------------- |
| **1**  | Game Rules                   | `GAME_RULES.md`            | Behavioral specification (what the game does)       |
| **2**  | Game State Model             | `GAME_STATE.md`            | Deterministic state machine and step semantics      |
| **3**  | Input Model                  | `INPUT_MODEL.md`           | Input representation and tick ordering              |
| **4**  | Error Handling               | `ERROR_HANDLING.md`        | Rejection vs error policy; invariant enforcement    |
| **5**  | Shapes & Rotations           | `SHAPES_AND_ROTATIONS.md`  | Exact tetromino geometry and rotations              |
| **6**  | Core API                     | `CORE_API.md`              | Python-level public API contract                    |
| **7**  | Core Test Oracle             | `TEST_ORACLE.md`           | Mandatory correctness tests for the pure core       |
| **8**  | Rendering Test Oracle        | `RENDERING_TEST_ORACLE.md` | Mandatory snapshot tests for ASCII rendering        |
| **9**  | Runtime Test Oracle          | `RUNTIME_TEST_ORACLE.md`   | Deterministic execution tests for scripted runtime  |
| **10** | CLI Test Oracle              | `CLI_TEST_ORACLE.md`       | Mandatory behavioral tests for CLI commands         |
| **11** | Replay Test Oracle           | `REPLAY_TEST_ORACLE.md`    | Deterministic replay validation and execution tests |
| **12** | Acceptance Gates             | `ACCEPTANCE_GATES.md`      | Milestone-based acceptance criteria                 |
| **13** | System Architecture          | `ARCHITECTURE.md`          | High-level system architecture and design choices   |
| **14** | System Decomposition         | `DECOMPOSITION.md`         | Explicit component decomposition and boundaries     |
| **15** | Runtime Specification        | `RUNTIME_SPEC.md`          | Tick loop, execution modes, and orchestration rules |
| **16** | Rendering Specification      | `RENDERING_SPEC.md`        | ASCII renderer contract and output format           |
| **17** | CLI Specification            | `CLI_SPEC.md`              | Command-line interface and entrypoint behavior      |
| **18** | Replay Specification         | `REPLAY_SPEC.md`           | Deterministic replay and evaluation format          |
| **19** | Project Overview (this file) | `PROJECT.md`               | Entry point and documentation map                   |

**Important**:  
This table is a **synopsis**, not a substitute for reading the documents themselves.

---

## 4. Extended development documentation overview

This section explains **how each document is intended to be used**, both by AI agents and by human developers supervising or reviewing agent output.

### 4.1 `GAME_RULES.md` — Behavioral specification

**Role**  
Defines *what* the game does, independent of implementation.

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

### 4.2 `GAME_STATE.md` — State machine and step semantics

**Role**  
Defines *how* the game evolves over time in a deterministic, testable way.

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

### 4.3 `INPUT_MODEL.md` — Input semantics

**Role**  
Removes ambiguity around how inputs are applied.

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

### 4.4 `ERROR_HANDLING.md` — Errors vs rejections

**Role**  
Defines when the system should **reject** an action versus **fail fast**.

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

### 4.5 `SHAPES_AND_ROTATIONS.md` — Geometry truth table

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

### 4.6 `CORE_API.md` — Python API contract

**Role**  
Defines the **only supported public API** for the core.

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

### 4.7 `TEST_ORACLE.md` — Mandatory tests

**Role**  
Defines *what must be proven* for correctness.

**Contents**
- Explicit test oracles mapped to rules
- Required vs optional tests
- Minimum acceptable test set for MVP

**Usage**
- This document is the arbiter of correctness.
- Passing ad-hoc tests is insufficient if oracles are missing.
- Agents should generate tests directly traceable to this document.

---

### 4.8 `RENDERING_TEST_ORACLE.md` — Renderer correctness

**Role**
Defines the **mandatory automated tests** that the ASCII renderer must satisfy.

**Contents**

* Deterministic output requirements
* Exact board layout and border rules
* Cell symbol constraints
* Metadata line presence and ordering
* Game-over rendering behavior
* Snapshot (golden) test requirements

**Usage**

* Enforces strict compliance with `RENDERING_SPEC.md`.
* Enables byte-for-byte snapshot testing.
* Prevents rendering logic from drifting or becoming environment-dependent.
* Applies exclusively to **Acceptance Gate 10**.

---

### 4.9 `RUNTIME_TEST_ORACLE.md` — Scripted runtime correctness

**Role**
Defines the **mandatory tests** for the scripted (virtual-time) runtime.

**Contents**

* One-tick-per-step execution guarantees
* Deterministic input application
* Rendering cadence requirements
* Early termination on game over
* Error propagation rules

**Usage**

* Ensures the runtime is suitable for deterministic evaluation and CI.
* Prevents re-implementation of core logic in the runtime layer.
* Applies exclusively to **Acceptance Gate 11**.

---

### 4.10 `CLI_TEST_ORACLE.md` — CLI behavior and robustness

**Role**
Defines **mandatory behavioral tests** for the command-line interface.

**Contents**

* Command availability (`run`, `script`, `replay`)
* Exit code semantics
* Error propagation requirements
* Prohibitions on silent failure or logic leakage

**Usage**

* Keeps the CLI thin, declarative, and auditable.
* Ensures consistent behavior for humans and automation.
* Applies exclusively to **Acceptance Gate 12**.

---

### 4.11 `REPLAY_TEST_ORACLE.md` — Deterministic replay correctness

**Role**
Defines **mandatory tests** for replay loading, validation, and execution.

**Contents**

* Replay file schema validation
* Strict input validation
* Deterministic tick-by-tick execution
* Final state determinism guarantees

**Usage**

* Enables exact reproduction of runs for debugging and agent evaluation.
* Prevents permissive or auto-correcting replay behavior.
* Applies exclusively to **Acceptance Gate 13**.

---

### 4.12 `ACCEPTANCE_GATES.md` — Milestone control

**Role**  
Controls **when the agent is allowed to advance**.

**Contents**
- Ordered development gates
- Mandatory criteria per gate
- Prohibited behaviors
- MVP definition

**Usage**
- Prevents “all-at-once” implementations.
- Enables human-in-the-loop approval per stage.
- Ideal for automated evaluation harnesses.

---

### 4.13 `ARCHITECTURE.md` — System-level architecture

**Role**
Defines the **big-picture architecture** of the application and records key architectural
decisions.

**Contents**

* Chosen architectural pattern (functional core / imperative shell)
* High-level component interaction diagram
* Technology and design options considered
* Explicit architectural decisions and non-goals

**Usage**

* Provides context for all non-core development.
* Prevents ad hoc architectural drift.
* Agents must align all new components with this document before implementation.
* Humans should treat this as the place to record architectural intent and rationale.

---

### 4.14 `DECOMPOSITION.md` — Explicit system decomposition (what exists)

**Role**
Defines the **authoritative functional decomposition** of the system into components.

**Contents**

* List of system components (core, runtime, renderer, input, CLI, etc.)
* Responsibility boundaries for each component
* Explicit non-responsibilities
* Allowed interfaces between components
* Delivery staging guidance

**Usage**

* Serves as the *bridge* between architecture and task execution.
* Forms the basis for role-based agent skills.
* Prevents responsibility leakage (e.g. logic in renderer, IO in core).
* Humans should consult this before adding any new module or package.

---

### 4.15 `RUNTIME_SPEC.md` — Execution model and orchestration

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

### 4.16 `RENDERING_SPEC.md` — Presentation contract

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
* Humans may extend this spec for additional renderers (graphical, web), but only additively.

---

### 4.17 `CLI_SPEC.md` — Command-line interface

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

### 4.18 `REPLAY_SPEC.md` — Deterministic replay and evaluation

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

## 5. Intended development workflow (summary)

1. **Read all docs** (mandatory for agents).
2. Start at **Acceptance Gate 0**.
3. Implement incrementally, gate by gate.
4. Write tests mapped to `TEST_ORACLE.md`.
5. Stop and escalate on ambiguity.
6. Only extend behavior by modifying docs first.

---

## 6. Audience note

- **AI agents**: This document defines your operating environment. Partial reading is failure.
- **Human developers**: This document is meant to remain readable, editable, and authoritative even as AI assistance evolves.

If a conflict arises between code and docs, **the docs win**.

---

