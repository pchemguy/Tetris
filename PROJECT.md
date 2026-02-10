---
name: PROJECT.md
description: This document acts as the primary entry point for project's technical documentation, and explains its documentation system and high-level workflows.
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# PROJECT.md

This document acts as the primary entry point for project's technical documentation, and explains its documentation system and high-level workflows.

## 1. Project overview

This project develops and evaluates a **prompting system for agentic software development**. Repository evolution is organized into explicit **phases** (defined in `docs/PHASES.md`), which constrain *what kind of work is allowed* at each stage. 

The reference implementation target is **classic Tetris**, chosen not as a game project per se, but as a compact, well-understood system that stresses:

* deterministic state machines,
* strict rule adherence,
* geometry and collision logic,
* time-stepped simulation,
* incremental feature integration,
* comprehensive test oracles.

The primary deliverable of this repository is **not** “a Tetris game”, but a **set of development contracts, specifications, and acceptance gates** that allow rigorous evaluation of whether an AI agent can:

* discover and obey documentation,
* implement incrementally without guessing,
* stop and escalate when blocked,
* produce auditable, deterministic software artifacts.

Human developers remain ultimately responsible for correctness and maintenance, but the project is explicitly designed to be **AI-readable, AI-actionable, and AI-auditable**.

---

## 2. Repository layout (high level)

```
.
├── docs/                  # Normative development specifications (authoritative)
├── tetris/
│     ├── src/tetris/      # Python core + shell implementation package
│     └── tests/           # Tests
├── .agent/skills/         # Agent skills (plan / implement / review units)
├── AGENTS.md              # General agent instructions
├── PROJECT.md             # This document (primary entry point)
└── README.md              # Optional human-facing wrapper
```

The **docs/** directory is authoritative.
Code exists to satisfy the docs — not the other way around.

---

## 3. Intended development workflow (summary)

The workflow below assumes full understanding of the documentation authority model described in the next section.

1. **Read all normative documents** (mandatory).
2. **Read `IMPLEMENTATION_REPORTS.md`** to determine current state.
3. Determine the current repository **phase** (`docs/PHASES.md`).
4. Confirm the current **acceptance gate** (`docs/ACCEPTANCE_GATES.md`).
5. Implement incrementally, gate by gate.
6. Write tests mapped to the applicable `docs/*_TEST_ORACLE.md` document(s).
7. Append results to `IMPLEMENTATION_REPORTS.md`.
8. Stop and escalate on ambiguity.
9. Extend behavior **only by updating documentation first**.

---

## 4. Normative documentation system

This repository is governed by a **layered documentation system**. Each document belongs to a **defined class** serving a distinct purpose in constraining, guiding, or evaluating the development process. The intent of this system is to:

* make **expectations explicit**,
* surface and document all assumptions,
* allow both humans and AI agents to reason correctly about:
    * *what exists*,
    * *what is allowed*,
    * *what is correct*.

---

### Development control documents (when work is allowed and evaluated)

Documents in this class control the **development process itself**, not system behavior. They define **when certain kinds of work are permitted**, and **under what conditions progress is considered acceptable**. This class consists of two distinct, complementary documents with **non-overlapping authority**:

#### Phases (`PHASES.md`) — *Scope control*

Phases define the **allowed scope of change** at a given point in the repository’s evolution. They answer questions such as:

* *What kinds of changes are permitted right now?*
* *Which subsystems may exist at all at this stage?*
* *Is this work premature, even if it could be implemented correctly?*

Phases constrain:

* **what may be attempted**,
* **which components may be introduced**,
* **what kinds of refactors or extensions are in-bounds**.

A phase violation is a **scope failure**, even if all acceptance criteria would otherwise pass.

---

#### Acceptance gates (`ACCEPTANCE_GATES.md`) — *Correctness and progression control*

Acceptance gates define **what must be implemented and proven** to advance development. They answer questions such as:

* *What concrete functionality is required at this stage?*
* *What correctness properties must hold?*
* *Which tests and oracles must pass?*

Acceptance gates constrain:

* **what constitutes “done”**,
* **what evidence of correctness is required**,
* **when progression is allowed**.

A gate failure is a **correctness failure**, even if the work is in-scope for the current phase.

---

#### Relationship between phases and gates

* **Phases** decide *whether work is allowed to be attempted*.
* **Acceptance gates** decide *whether attempted work is correct and complete*.

Both must be satisfied:

* correct work in the wrong phase **fails**,
* in-phase work that fails gate criteria **fails**.

Together, these documents prevent:

* premature generalization,
* scope creep disguised as “cleanup”,
* skipping validation steps,
* implementing features “because they’re easy”.

---

### System architecture and decomposition (what exists, how it is structured)

Documents in this class define the **structural reality of the system**. They constrain *what the system is*, independent of behavior, tests, or development order. This class also consists of two distinct documents with **different levels of abstraction and authority**:

#### Architecture (`ARCHITECTURE.md`) — *Conceptual design intent*

The architecture document defines the **high-level design model** of the system. It answers questions such as:

* *What architectural pattern is used?*
* *Why is the system structured this way?*
* *What design principles are non-negotiable?*
* *What alternatives were considered and rejected?*

Architecture constrains:

* **design intent**,
* **allowed architectural styles**,
* **non-goals and explicit exclusions**.

It provides *rationale* and *direction*, not a module map.

---

#### Decomposition (`DECOMPOSITION.md`) — *Concrete component boundaries*

The decomposition document defines the **authoritative breakdown of the system into components**. It answers questions such as:

* *What components exist concretely?*
* *What is each component responsible for?*
* *What must a component not do?*
* *What interfaces are allowed between components?*

Decomposition constrains:

* **component responsibilities**,
* **module boundaries**,
* **allowed dependencies**.

It is the **operational boundary document** used to evaluate responsibility leakage.

---

#### Relationship between architecture and decomposition

* **Architecture** defines *why the system is shaped the way it is*.
* **Decomposition** defines *how that shape is realized in components*.

Architecture without decomposition is aspirational. Decomposition without architecture is arbitrary. Together, these documents ensure that:

* structural decisions are intentional,
* responsibility boundaries are explicit,
* implementation cannot silently drift.

All implementation must conform to **both**.

---

### Component specifications (what behavior is defined)

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

### Test oracles (how correctness is proven)

Test oracle documents define **what must be proven** for an implementation to be considered correct. They answer questions such as:

* Which behaviors must be tested?
* What scenarios are mandatory?
* What level of determinism is required?
* What constitutes sufficient coverage for acceptance?

Test oracles are **normative**: passing ad-hoc or convenience tests is insufficient if oracle-mandated tests are missing. Each test oracle applies to:

* a specific component, and
* a specific acceptance gate (or small range of gates).

---

### Core vs shell distinction (what is inside vs outside the simulation)

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

## 5. Normative Documentation System

### Execution record (what has actually happened)

This document records the **actual execution history** of agentic development.

#### Implementation reports (`reports/IMPLEMENTATION_REPORTS.md`) — *Authoritative execution state*

The implementation log is an **append-only record** of:

- which phases and gates have been attempted,
- what actions were taken,
- what artifacts were modified,
- what passed, failed, or was blocked,
- what the next intended step is.

It answers questions such as:

- *Where did development stop last time?*
- *Which gate was last attempted, and with what outcome?*
- *What assumptions or blockers were discovered?*

This document is:

- **state**, not policy,
- **authoritative** for “current progress”,
- required reading for any agent resuming work.

Unlike specifications or gates, the implementation log does **not** define what is allowed or correct; it records **what actually occurred**.

All agents must:

- read it before acting,
- append to it after acting,
- never rewrite or delete history.

---

## 6. Development documentation index (synopsis) and integration

This section provides a **synoptic index** of all normative documents grouped by **conceptual responsibility**; applicability and permitted use are determined solely by the Gate applicability rules and `ACCEPTANCE_GATES.md`, not by table order. Agents are expected to **discover and reason over all of them**, not just one. Partial discovery or selective reading constitutes non-compliance.

This section is not a/an

* development checklist,
* implementation sequence,
* tutorial.

To determine:

* *what applies now* → consult **phases** and **acceptance gates**,
* *what behavior is allowed* → consult **component specifications**,
* *what must be tested* → consult **test oracles**.

**IMPORTANT**: For each group, relative path (with respect to project directory / repo root) of the containing directory is provided. In other documents, these files will be conventionally referred to by name only. You must use appropriate relative prefix from this section to locate individual files.

### System architecture

**Directory**: `docs/architecture/`

| Title                       | Filename                | Function / Role                                                  |
| --------------------------- | ----------------------- | ---------------------------------------------------------------- |
| System Architecture         | `ARCHITECTURE.md`       | High-level system architecture and design choices                |
| System Decomposition        | `DECOMPOSITION.md`      | Explicit component decomposition and boundaries                  |
| Documentation Authority Map | `DOCS_AUTHORITY_MAP.md` | Authoritative hierarchy and conflict-resolution rules among docs |

---

### Development control

**Directory**: `docs/control/`

| Title                       | Filename              | Function / Role                                             |
| --------------------------- | --------------------- | ----------------------------------------------------------- |
| Repository Evolution Phases | `PHASES.md`           | Allowed scope of work at each stage of repository evolution |
| Acceptance Gates            | `ACCEPTANCE_GATES.md` | Milestone-based acceptance criteria and progression rules   |

---

### Core contracts

**Directory**: `docs/specs/core/`

| Title              | Filename                  | Function / Role                                  |
| ------------------ | ------------------------- | ------------------------------------------------ |
| Game Rules         | `GAME_RULES.md`           | Behavioral specification (what the game does)    |
| Game State Model   | `GAME_STATE.md`           | Deterministic state machine and step semantics   |
| Input Model        | `INPUT_MODEL.md`          | Input representation and tick ordering           |
| Error Handling     | `ERROR_HANDLING.md`       | Rejection vs error policy; invariant enforcement |
| Shapes & Rotations | `SHAPES_AND_ROTATIONS.md` | Exact tetromino geometry and rotations           |
| Core API           | `CORE_API.md`             | Python-level public API contract                 |

---

### Shell contracts

**Directory**: `docs/specs/shell/`

| Title                   | Filename            | Function / Role                                     |
| ----------------------- | ------------------- | --------------------------------------------------- |
| Runtime Specification   | `RUNTIME_SPEC.md`   | Tick loop, execution modes, and orchestration rules |
| Rendering Specification | `RENDERING_SPEC.md` | ASCII renderer contract and output format           |
| CLI Specification       | `CLI_SPEC.md`       | Command-line interface and entrypoint behavior      |
| Replay Specification    | `REPLAY_SPEC.md`    | Deterministic replay and evaluation format          |

---

### I/O API specifications

**Directory**: `docs/specs/io/`

| Title                                | Filename              | Function / Role                                           |
| ------------------------------------ | --------------------- | --------------------------------------------------------- |
| Input driver interface specification | `INPUT_DRIVER_API.md` | Input Driver API and its strict responsibility boundaries |
| Presenter interface specification    | `PRESENTER_API.md`    | Presenter API and its strict responsibility boundaries    |

### Progress reporting

**Directory**: `docs/reports/`

| Title                  | Filename                    | Function / Role                                                       |
| ---------------------- | --------------------------- | --------------------------------------------------------------------- |
| Implementation Reports | `IMPLEMENTATION_REPORTS.md` | Append-only execution record of phase/gate progress and agent actions |

---

### Core test oracle

**Directory**: `docs/oracles/core/`

| Title            | Filename              | Function / Role                               |
| ---------------- | --------------------- | --------------------------------------------- |
| Core Test Oracle | `CORE_TEST_ORACLE.md` | Mandatory correctness tests for the pure core |

---

### Shell-level test oracles

**Directory**: `docs/oracles/shell/`

| Title                 | Filename                   | Function / Role                                     |
| --------------------- | -------------------------- | --------------------------------------------------- |
| Rendering Test Oracle | `RENDERING_TEST_ORACLE.md` | Mandatory snapshot tests for ASCII rendering        |
| Runtime Test Oracle   | `RUNTIME_TEST_ORACLE.md`   | Deterministic execution tests for scripted runtime  |
| CLI Test Oracle       | `CLI_TEST_ORACLE.md`       | Mandatory behavioral tests for CLI commands         |
| Replay Test Oracle    | `REPLAY_TEST_ORACLE.md`    | Deterministic replay validation and execution tests |

---

### Gate applicability rules (normative)

The applicability of documents to acceptance gates defined in `ACCEPTANCE_GATES.md` is governed by the following rules:

- **System-level contracts** apply to **all gates**. They constrain the system globally and must be obeyed at all stages.
- **Core / engine contracts** apply to **core gates (0–9)**. They define the pure simulation and must not be violated during core development or extension.
- **Core test oracle** (`CORE_TEST_ORACLE.md`) applies to **Gates 1–6**, and additionally to **Gates 7–9** if those optional core extensions are enabled.
- **Shell contracts** apply to **Gate 0** (discovery and scope awareness) and to their respective **shell gates (10–13)** when implementation is permitted.
- **Shell-level test oracles** apply to **exactly one gate each**, corresponding to the shell component they validate.
- **Gate 0** applies universally as a discovery and compliance gate and therefore requires awareness of all normative documents, even if they are not yet implemented.

These rules are authoritative and supersede any informal interpretation of document scope.

---

### Phase ↔ Gate matrix

The following table defines which acceptance gates are expected to be exercised within each repository evolution phase. This matrix is **normative** and constrains scope. It does not replace the detailed gate definitions in `docs/ACCEPTANCE_GATES.md`.

| Phase | Phase name                                 | Applicable gates |
| ----- | ------------------------------------------ | ---------------- |
| 0     | Contract spine & evaluation framework      | 0                |
| 1     | Core-only MVP benchmark                    | 0–6              |
| 2     | System / shell completeness (baseline app) | 0, 10–13         |
| 3     | Optional extensions & hardening            | 0, 7–9           |
| 4     | Variant shells & alternative interfaces    | 0, 10–13 (+ext.) |
| 5     | Benchmark scaling & agent evaluation       | 0–13             |

#### Notes

- **Gate 0** applies in *all phases* as a discovery and compliance gate.
- Gates **1–6** define the **mandatory core MVP**.
- Gates **7–9** are optional core extensions and may be completed in Phase 1 or Phase 3.
- Gates **10–13** define shell/system completeness and must not be attempted before Phase 2.
- “(+ext.)” indicates that additional gates may be introduced for new shell variants.

---

### Further development

Adding a new component requires adding:

* A specification document
* An index row in the appropriate subsection above
* An extended description in `Extended development documentation overview` below
* A test oracle document (optional)
* An acceptance gate (optional in `ACCEPTANCE_GATES.md`)

### Notes

* This section is a **synopsis**, not a substitute for reading the documents themselves.
* All documents listed above are **normative** unless explicitly stated otherwise. Non-normative documents (guides, notes, examples) may be added later.
* All test oracle documents follow the naming convention `<COMPONENT>_TEST_ORACLE.md` and apply only to the corresponding acceptance gate(s).
* If a conflict arises between code and docs, the implementation is considered incorrect.

---

## 7. Extended development documentation overview

This section explains **how each document is intended to be used**, both by AI agents and by human developers supervising or reviewing agent output.

### Project-wide

#### `ACCEPTANCE_GATES.md` — Milestone control

**Role**  
Defines **when the agent is allowed to advance**.

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

#### `PHASES.md` — Repository evolution phases

**Role**   
Defines the **allowed scope of work** at each stage of the repository’s evolution.

**Contents**

- Named repository evolution phases
- Scope boundaries per phase
- Relationship between phases and acceptance gates
- Phase ↔ Gate matrix

**Usage**

- Prevents premature refactors, extensions, or generalization.
- Constrains *what kinds of changes are allowed*, independent of correctness.
- Works in tandem with `ACCEPTANCE_GATES.md`, which governs *whether an implementation is correct*.
- Agents must determine the current phase before selecting a target gate.
- Humans should advance phases deliberately and explicitly, not implicitly.

---

### System-level contracts

#### `ARCHITECTURE.md` — System-level architecture

**Role**  
Defines the **big-picture architecture** of the application.

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

#### `DECOMPOSITION.md` — Explicit system decomposition (what exists)

**Role**  
Defines the **authoritative component breakdown** of the system.

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

### Core Test Oracle

#### `CORE_TEST_ORACLE.md` — Mandatory tests

**Role**  
Defines **what must be proven** for correctness.

**Contents**

- Explicit test oracles mapped to rules
- Required vs optional tests
- Minimum acceptable test set for MVP

**Usage**

- This document is the arbiter of correctness.
- Passing ad-hoc tests is insufficient if oracles are missing.
- Agents should generate tests directly traceable to this document.
- Applies exclusively to Acceptance Gates 1–6.

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

### Shell Test Oracles

#### `RENDERING_TEST_ORACLE.md` — Renderer correctness

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

#### `RUNTIME_TEST_ORACLE.md` — Scripted runtime correctness

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

#### `CLI_TEST_ORACLE.md` — CLI behavior and robustness

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

#### `REPLAY_TEST_ORACLE.md` — Deterministic replay correctness

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

## 8. Audience note

* **AI agents**: This document defines your operating environment. Partial reading is failure.
* **Human developers**: This document is intended to remain readable, editable, and authoritative even as AI assistance evolves.

---

