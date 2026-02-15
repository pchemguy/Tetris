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
references:
description: Defines the structure, authority rules, and roles of the repository's documentation infrastructure.
---

# Documentation Infrastructure System (Normative)

## 1. Purpose

This document defines the **documentation infrastructure** of the repository. It governs the **meta-layer**: not game behavior, not architecture, not tests — but the structure that makes those documents coherent, verifiable, and automatable.

The documentation system itself is treated as a **first-class, auditable subsystem** of the project: documentation is machine-checkable, authority is explicit, scope boundaries are enforceable, references are structurally valid, and evolution is controlled and traceable.

---

## 2. Metadata and cross-document references

Every normative document declares a stable identifier (`doc_id`) in its YAML header, as defined in `DOC_SCHEMA.md`. Documents may reference one another in prose using `@DOC_ID` markers (for example, `@DOC_SCHEMA`) as a convenience mechanism; YAML metadata remains authoritative, and `@DOC_ID` markers are validated against the repository’s declared identifiers. Tooling may use YAML metadata and `@DOC_ID` markers to validate references and construct a deterministic documentation graph as defined in `DOC_GRAPH_SPEC.md`.

---

## 3. Layered organization

The repository documentation system is organized into conceptual layers **L0–L5**. The normative definition of the layering model (meaning, constraint/validity vs diagnosis flows, meta-layer positioning, conflict resolution, and the layer index) is specified in `@DOC_LAYERS`. Tooling uses this layer model to classify documents deterministically (via `kind`) and to support diagnostic validation of cross-layer semantic coupling.

## 4. Technical documentation index

This section provides a **synoptic index** of all normative documents grouped by **conceptual responsibility**; applicability and permitted use are determined solely by the Gate applicability rules and `ACCEPTANCE_GATES.md`, not by table order. Agents are expected to **discover and reason over all of them**, not just one. Partial discovery or selective reading constitutes non-compliance.

**IMPORTANT**: For each group, relative path (with respect to project directory / repo root) of the containing directory is provided. In other documents, these files will be conventionally referred to by name only. You must use appropriate relative prefix from this section to locate individual files.

---

### L0 — Documentation Infrastructure (Meta-layer) 

**Directory**: `docs/meta/`

| Title                                               | Filename                            | Function / Role                                                                 |
| --------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------- |
| Documentation Infrastructure System (this file)     | `DOCUMENTATION_SYSTEM.md`           | Defines the documentation infrastructure                                        |
| Documentation Layers and Classification             | `DOC_LAYERS.md`                     | Defines the L0–L5 layering meaning, motivation, and classification model        |
| Documentation Metadata Schema (Spec)                | `DOC_SCHEMA.md`                     | Normative specification of documentation metadata semantics                     |
| Documentation Metadata Schema (JSON)                | `DOC_SCHEMA.json`                   | Machine-validated schema for YAML front matter in Markdown docs                 |
| Documentation Graph Specification                   | `DOC_GRAPH_SPEC.md`                 | Rules for extracting and rendering documentation dependency graphs              |
| Documentation Inventory (Spec)                      | `DOC_INVENTORY.md`                  | Defines the machine-readable inventory artifact and required invariants         |
| Documentation Inventory                             | `DOC_INVENTORY.json`                | Generated machine inventory (tool output / discovery input)                     |
| Documentation Inventory (Schema)                    | `DOC_INVENTORY.schema.json`         | JSON Schema validating `DOC_INVENTORY.json`                                     |
| Cross-Layer YAML Reference Dependency Policy (Spec) | `CROSS_LAYER_DEPENDENCY.md`         | Normative rationale/interpretation for diagnostic cross-layer YAML dependencies |
| YAML Reference Policy                               | `YAML_REFERENCE_POLICY.json`        | Machine-readable cross-layer validation policy (diagnostic by default)          |
| YAML Reference Policy (Schema)                      | `YAML_REFERENCE_POLICY.schema.json` | JSON Schema validating `YAML_REFERENCE_POLICY.json`                             |
| Documentation Authority Map                         | `DOCS_AUTHORITY_MAP.md`             | Hierarchy and conflict-resolution rules among normative documents               |

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

| Title                               | Filename                         | Function / Role                                                                |
| ----------------------------------- | -------------------------------- | ------------------------------------------------------------------------------ |
| System Architecture                 | `ARCHITECTURE.md`                | High-level system architecture and design decisions (Functional Core / Shell). |
| System Decomposition                | `DECOMPOSITION.md`               | Explicit component decomposition and responsibility boundaries.                |
| Component Registry (Normative)      | `COMPONENT_REGISTRY.md`          | Human-readable explanation of registered components and layer model.           |
| Component Registry (Machine Schema) | `COMPONENT_REGISTRY.schema.json` | JSON Schema validating `COMPONENT_REGISTRY.json`.                              |
| Component Registry (Instance)       | `COMPONENT_REGISTRY.json`        | Canonical list of components, layers, and dependency policy.                   |

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

