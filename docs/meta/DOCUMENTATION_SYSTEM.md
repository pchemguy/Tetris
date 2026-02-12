---
doc_id: DOCUMENTATION_SYSTEM
name: DOCUMENTATION_SYSTEM.md
title: Documentation Infrastructure System
kind: meta
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
supersedes: []
superseded_by:
references:
  - DOC_SCHEMA
  - COMPONENT_REGISTRY
  - DOCS_AUTHORITY_MAP
  - DOC_GRAPH_SPEC
description: Defines the structure, authority rules, and roles of the repository's documentation infrastructure.
---

# Documentation Infrastructure System (Normative)

## 1. Purpose

This document defines the **documentation infrastructure** of the repository.

It formalizes:

* how documents are identified,
* how components are classified,
* how authority and scope are determined,
* how cross-document references are validated,
* how documentation integrity is enforced at Gate 0.

The documentation system itself is treated as a **first-class, auditable subsystem** of the project.

It is designed to ensure that:

* documentation is machine-checkable,
* authority is explicit and deterministic,
* scope boundaries are enforceable,
* references are structurally valid,
* evolution is controlled and traceable.

This document governs the **meta-layer** of the repository: not game behavior, not architecture, not tests — but the structure that makes those documents coherent, verifiable, and automatable.

**Audience note**

* **AI agents**: This document defines your operating environment. Partial reading is failure.
* **Human developers**: This document is intended to remain readable, editable, and authoritative even as AI assistance evolves.

---

## 2. Metadata and cross-document references

Every normative document declares a stable `DOC_ID` in its YAML header as defined in `DOC_SCHEMA.md`. This identifier is the authoritative identity of the document and remains valid regardless of filename or directory location. Documents may reference one another in prose using `@DOC_ID` (for example, `@DOC_SCHEMA` for `DOC_SCHEMA.md`) as a convenience marker. Authoritative relationships between documents are declared in metadata, not inferred from filenames or directory structure. This enables tooling to validate identifiers, resolve references, and construct a deterministic documentation graph as defined in `DOC_GRAPH_SPEC.md`.

In this document, other documents will be generally referred do by their name. Actual location of individual files is indicated in the `Technical documentation index` section of this document. In other documents, location independent `@DOC_ID` references will be generally used instead, while filenames may still refer to documents within the same group/directory.

---

## 3. Layered organization

### Overview

Documentation in this repository is organized in a **layered structure**. Each document belongs to a **defined class** (or layer) serving a distinct purpose in constraining, guiding, or evaluating the development process. The intent of this organization is to:

* make **expectations explicit**,
* surface and document all assumptions,
* allow both humans and AI agents to reason correctly about:
    * *what exists*,
    * *what is allowed*,
    * *what is correct*.

```
                    ┌───────────────────────────────────────────┐
                    │               REPOSITORY                  │
                    │ (code + docs + tests + agent workflows)   │
                    └───────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────┐
│ L0 — Documentation Infrastructure (Meta-layer)                                 │
│    Defines how docs are identified, scoped, linked, and validated.             │
│                                                                                │
│      - DOC_SCHEMA.md / DOC_SCHEMA.json                                         │
│          * YAML front matter schema                                            │
│          * identifier + applicability + authority fields                       │
│                                                                                │
│      - COMPONENT_REGISTRY.md / COMPONENT_REGISTRY.json (+ schema)              │
│          * canonical component ids + layers                                    │
│          * doc_scope enum inventory                                            │
│                                                                                │
│      - DOC_GRAPH_SPEC.md                                                       │
│          * allowed node/edge types + validations                               │
│                                                                                │
│    Outputs / enforcement:                                                      │
│      - machine-validated doc inventory                                         │
│      - validated @DOC_ID references (convenience)                              │
│      - generated doc graph / reports                                           │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │                                         
                                     │ constrains + validates                  
                                     v                                         
┌────────────────────────────────────────────────────────────────────────────────┐
│ L1 — Governance (Process Control)                                              │
│    Defines when work is allowed and what “done” means.                         │
│                                                                                │
│      - PHASES.md             (scope permission)                                │
│      - ACCEPTANCE_GATES.md   (progression + pass/fail criteria)                │
│                                                                                │
│    Relationship: Phase allows attempting a gate; gates define correctness.     │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │                                         
                                     │ constrains system structure             
                                     v                                         
┌────────────────────────────────────────────────────────────────────────────────┐
│ L2 — System Structure (Global Contracts)                                       │
│    Defines architecture intent and component responsibility boundaries.        │
│                                                                                │
│      - ARCHITECTURE.md                                                         │
│      - DECOMPOSITION.md                                                        │
│                                                                                │
│    These apply to all gates.                                                   │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │                                         
                                     │ constrains behavior                     
                                     v                                         
┌────────────────────────────────────────────────────────────────────────────────┐
│ L3 — Behavioral Specifications (Component Contracts)                           │
│    Defines what the system does; if not specified, it must not be implemented. │
│                                                                                │
│      - Core specs: GAME_RULES, GAME_STATE, INPUT_MODEL, ERROR_HANDLING,        │
│                   SHAPES_AND_ROTATIONS, CORE_API, ...                          │
│      - Shell specs: RUNTIME_SPEC, RENDERING_SPEC, CLI_SPEC, REPLAY_SPEC, ...   │
│      - Shell APIs: PRESENTER_API, INPUT_DRIVER_API, ...                        │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │                                         
                                     │ defines required proof                  
                                     v                                         
┌────────────────────────────────────────────────────────────────────────────────┐
│ L4 — Test Oracles (Proof Obligations)                                          │
│    Defines what must be tested to claim correctness at each gate.              │
│                                                                                │
│      - CORE_TEST_ORACLE.md                                                     │
│      - RENDERING_TEST_ORACLE.md                                                │
│      - RUNTIME_TEST_ORACLE.md                                                  │
│      - CLI_TEST_ORACLE.md                                                      │
│      - REPLAY_TEST_ORACLE.md                                                   │
│      - CONFIG_TEST_ORACLE.md (if enabled)                                      │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │                                         
                                     │ records execution history (state)       
                                     v                                         
┌────────────────────────────────────────────────────────────────────────────────┐
│ L5 — Execution State (Reports)                                                 │
│    Records what actually happened, append-only.                                │
│                                                                                │
│      - IMPLEMENTATION_REPORTS.md                                               │
│      - generated reports/ (optional)                                           │
└────────────────────────────────────────────────────────────────────────────────┘
```

- Higher layers **constrain** lower layers.
- Lower layers must not “reach upward” to change the meaning of higher layers.
- If two documents conflict:
    1. resolve by **authority** (`normative` over `non_normative`), then
    2. by **layer precedence** (L0 → L5), then
    3. by explicit `supersedes` / `superseded_by` relationships, if present.

| Layer                                                | Question                           | Directory            |
| ---------------------------------------------------- | ---------------------------------- | -------------------- |
| L0 — Documentation Infrastructure (Meta-layer)       | How the project is documented      | `docs/meta/`         |
| L1 — Governance (Process Control)                    | When work is allowed and evaluated | `docs/control/`      |
| L2 — System Structure (Global Contracts)             | What exists, how it is structured  | `docs/architecture/` |
| L3 — Behavioral Specifications (Component Contracts) | What behavior is defined           | `docs/specs/`        |
| L4 — Test Oracles (Proof Obligations)                | How correctness is proven          | `docs/oracles/`      |
| L5 — Execution State (Reports)                       | What has actually happened         | `docs/reports/`      |
| -                                                    | What may be researched or tried    | `docs/ideas/`        |

---

### L1 — Governance (Process Control)

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

#### Gate applicability rules (normative)

The applicability of documents to acceptance gates defined in `ACCEPTANCE_GATES.md` is governed by the following rules:

- **Gate 0** applies universally as a discovery and compliance gate and therefore requires awareness of all normative documents, even if they are not yet implemented.
- **System-level contracts** apply to **all gates**. They constrain the system globally and must be obeyed at all stages.
- **Core / engine contracts** apply to **core gates (0–9)**. They define the pure simulation and must not be violated during core development or extension.
- **Shell contracts** apply to **Gate 0** (discovery and scope awareness) and to their respective **shell gates (10–13)** when implementation is permitted.
- **Core test oracle** (`CORE_TEST_ORACLE.md`) applies to **Gates 1–6**, and additionally to **Gates 7–9** if those optional core extensions are enabled.
- **Shell-level test oracles** apply to **exactly one gate each**, corresponding to the shell component they validate.

These rules are authoritative and supersede any informal interpretation of document scope.

---

#### Phase ↔ Gate matrix

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

### L2 — System Structure (Global Contracts)

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

### L3 — Behavioral Specifications (Component Contracts)

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

#### Core vs shell distinction (what is inside vs outside)

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

### L4 — Test Oracles (Proof Obligations)

Test oracle documents define **what must be proven** for an implementation to be considered correct. They answer questions such as:

* Which behaviors must be tested?
* What scenarios are mandatory?
* What level of determinism is required?
* What constitutes sufficient coverage for acceptance?

Test oracles are **normative**: passing ad-hoc or convenience tests is insufficient if oracle-mandated tests are missing. Each test oracle applies to:

* a specific component, and
* a specific acceptance gate (or small range of gates).

---

### L5 — Execution State (Reports)

These documents record the **actual execution history** of agentic development. Unlike specifications or gates (which define what is allowed or correct), these documents

- define **state**, not policy,
- are **authoritative** for “current progress”,
- are required reading for any agent resuming work.

#### Implementation reports (`IMPLEMENTATION_REPORTS.md`) — *Authoritative execution state*

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

All agents must:

- read it before acting,
- append to it after acting,
- never rewrite or delete history.

---

## 4. Technical documentation index

This section provides a **synoptic index** of all normative documents grouped by **conceptual responsibility**; applicability and permitted use are determined solely by the Gate applicability rules and `ACCEPTANCE_GATES.md`, not by table order. Agents are expected to **discover and reason over all of them**, not just one. Partial discovery or selective reading constitutes non-compliance.

**IMPORTANT**: For each group, relative path (with respect to project directory / repo root) of the containing directory is provided. In other documents, these files will be conventionally referred to by name only. You must use appropriate relative prefix from this section to locate individual files.

---

### L0 — Documentation Infrastructure (Meta-layer) 

**Directory**: `docs/meta/`


| Title                                           | Filename                  | Function / Role                                                     |
| ----------------------------------------------- | ------------------------- | ------------------------------------------------------------------- |
| Documentation Infrastructure System (this file) | `DOCUMENTATION_SYSTEM.md` | Defines the documentation infrastructure                            |
| Documentation Metadata Schema (Spec)            | `DOC_SCHEMA.md`           | Normative specification of documentation metadata semantics.        |
| Documentation Metadata Schema (JSON)            | `DOC_SCHEMA.json`         | Machine-validated schema for YAML front matter in Markdown docs.    |
| Documentation Graph Specification               | `DOC_GRAPH_SPEC.md`       | Rules for extracting and rendering documentation dependency graphs. |
| Documentation Authority Map                     | `DOCS_AUTHORITY_MAP.md`   | Hierarchy and conflict-resolution rules among normative documents.  |


---

### L1 — Governance (Process Control)

**Directory**: `docs/control/`

| Title                       | Filename              | Function / Role                                             |
| --------------------------- | --------------------- | ----------------------------------------------------------- |
| Repository Evolution Phases | `PHASES.md`           | Allowed scope of work at each stage of repository evolution |
| Acceptance Gates            | `ACCEPTANCE_GATES.md` | Milestone-based acceptance criteria and progression rules   |

---

### L2 — System Structure (Global Contracts)

**Directory**: `docs/architecture/`

| Title                                | Filename                         | Function / Role                                                                |
| ------------------------------------ | -------------------------------- | ------------------------------------------------------------------------------ |
| System Architecture                  | `ARCHITECTURE.md`                | High-level system architecture and design decisions (Functional Core / Shell). |
| System Decomposition                 | `DECOMPOSITION.md`               | Explicit component decomposition and responsibility boundaries.                |
| Component Registry (Normative)       | `COMPONENT_REGISTRY.md`          | Human-readable explanation of registered components and layer model.           |
| Component Registry (Machine Schema)  | `COMPONENT_REGISTRY.schema.json` | JSON Schema validating `COMPONENT_REGISTRY.json`.                              |
| Component Registry (Instance)        | `COMPONENT_REGISTRY.json`        | Canonical list of components, layers, and dependency policy.                   |

---

### L3 — Behavioral Specifications (Component Contracts)

#### Core contracts

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

#### Shell contracts

**Directory**: `docs/specs/shell/`

| Title                            | Filename            | Function / Role                                                 |
| -------------------------------- | ------------------- | --------------------------------------------------------------- |
| Runtime Specification            | `RUNTIME_SPEC.md`   | Tick loop, execution modes, and orchestration rules             |
| Rendering Specification          | `RENDERING_SPEC.md` | ASCII renderer contract and output format                       |
| CLI Specification                | `CLI_SPEC.md`       | Command-line interface and entrypoint behavior                  |
| Replay Specification             | `REPLAY_SPEC.md`    | Deterministic replay and evaluation format                      |
| Renderer interface specification | `RENDERER_API.md`   | Renderer API and its strict purity guarantees                   |
| Runtime interface specification  | `RUNTIME_API.md`    | Runtime API and its role as the execution-time orchestrator     |
| Configuration API                | `CONFIG_API.md`     | Typed configuration model used to parameterize the application. |

---

#### Shell API specifications

**Directory**: `docs/specs/io/`

| Title                                | Filename              | Function / Role                                           |
| ------------------------------------ | --------------------- | --------------------------------------------------------- |
| Input driver interface specification | `INPUT_DRIVER_API.md` | Input Driver API and its strict responsibility boundaries |
| Presenter interface specification    | `PRESENTER_API.md`    | Presenter API and its strict responsibility boundaries    |

---

### L4 — Test Oracles (Proof Obligations)

#### Core test oracle

**Directory**: `docs/oracles/core/`

| Title            | Filename              | Function / Role                               |
| ---------------- | --------------------- | --------------------------------------------- |
| Core Test Oracle | `CORE_TEST_ORACLE.md` | Mandatory correctness tests for the pure core |

---

#### Shell-level test oracles

**Directory**: `docs/oracles/shell/`

| Title                 | Filename                   | Function / Role                                     |
| --------------------- | -------------------------- | --------------------------------------------------- |
| Rendering Test Oracle | `RENDERING_TEST_ORACLE.md` | Mandatory snapshot tests for ASCII rendering        |
| Runtime Test Oracle   | `RUNTIME_TEST_ORACLE.md`   | Deterministic execution tests for scripted runtime  |
| CLI Test Oracle       | `CLI_TEST_ORACLE.md`       | Mandatory behavioral tests for CLI commands         |
| Replay Test Oracle    | `REPLAY_TEST_ORACLE.md`    | Deterministic replay validation and execution tests |
| Config Test Oracle    | `CONFIG_TEST_ORACLE.md`    | *(TODO)*                                            |

---

### L5 — Execution State (Reports)

**Directory**: `docs/reports/`

| Title                  | Filename                    | Function / Role                                                       |
| ---------------------- | --------------------------- | --------------------------------------------------------------------- |
| Implementation Reports | `IMPLEMENTATION_REPORTS.md` | Append-only execution record of phase/gate progress and agent actions |

---

### Further development

Adding a new component requires adding:

* A specification document
* An index row in the appropriate subsection above
* An extended description in `Extended development documentation overview` below
* A test oracle document (optional)
* An acceptance gate (optional in `ACCEPTANCE_GATES.md`)

Raw / early ideas should be noted under `docs/ideas/`. Agents **MUST** ignore this path by default unless specifically instructed otherwise.

### Notes

* This section is a **synopsis**, not a development checklist, an implementation sequence, a tutorial, or a substitute for reading the documents themselves.
* All documents listed above are **normative** unless explicitly stated otherwise. Non-normative documents (guides, notes, examples) may be added later.
* All test oracle documents follow the naming convention `<COMPONENT>_TEST_ORACLE.md` and apply only to the corresponding acceptance gate(s).
* If a conflict arises between code and docs, the implementation is considered incorrect.

To determine:

* *what applies now* → consult **phases** and **acceptance gates**,
* *what behavior is allowed* → consult **component specifications**,
* *what must be tested* → consult **test oracles**.

## 5. Extended development documentation overview

This section explains **how each document is intended to be used**, both by AI agents and by human developers supervising or reviewing agent output.

---

### L1 — Governance (Process Control)

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

### L2 — System Structure (Global Contracts)

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

### L3 — Behavioral Specifications (Component Contracts)

#### Core / engine contracts

##### `GAME_RULES.md` — Behavioral specification

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

##### `GAME_STATE.md` — State machine and step semantics

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

##### `INPUT_MODEL.md` — Input semantics

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

##### `ERROR_HANDLING.md` — Errors vs rejections

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

##### `SHAPES_AND_ROTATIONS.md` — Geometry truth table

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

##### `CORE_API.md` — Python API contract

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

#### Shell contracts

##### `RUNTIME_SPEC.md` — Execution model and orchestration

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

##### `RENDERING_SPEC.md` — Presentation contract

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

##### `CLI_SPEC.md` — Command-line interface

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

##### `REPLAY_SPEC.md` — Deterministic replay and evaluation

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

### L4 — Test Oracles (Proof Obligations)

#### Core Test Oracle

##### `CORE_TEST_ORACLE.md` — Mandatory tests

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

#### Shell Test Oracles

##### `RENDERING_TEST_ORACLE.md` — Renderer correctness

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

##### `RUNTIME_TEST_ORACLE.md` — Scripted runtime correctness

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

##### `CLI_TEST_ORACLE.md` — CLI behavior and robustness

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

##### `REPLAY_TEST_ORACLE.md` — Deterministic replay correctness

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

