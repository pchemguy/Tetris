---
doc_id: L3_BEHAVIOR
name: L3_BEHAVIOR.md
title: L3 — Behavioral Specifications (Component Contracts)
status: active
authority: normative
description: Defines and indexes all normative behavioral specifications for core and shell components.
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

This layer contains the repository’s **behavioral contracts**: documents that define what the system is allowed to do, component by component. These are **normative specifications**, not implementation guides.

They answer questions such as:

- What is the exact behavior?
- What inputs are valid?
- What state transitions are permitted?
- What is explicitly out of scope?

If a behavior is not defined in a specification, it **must not be implemented**. Behavior must not be inferred from tests, examples, or implementation patterns.

---

## Document index

This index is the canonical navigation entry point for L3. It is intentionally descriptive and avoids duplicating the specifications themselves.

### Core contracts

**Directory**: `docs/specs/core/`

| Title              | Filename                  | Role                                                        |
| ------------------ | ------------------------- | ----------------------------------------------------------- |
| Game Rules         | `GAME_RULES.md`           | Normative gameplay semantics (“what the game does”).        |
| Game State Model   | `GAME_STATE.md`           | Deterministic state machine and tick/step semantics.        |
| Input Model        | `INPUT_MODEL.md`          | Per-tick input representation and ordering rules.           |
| Error Handling     | `ERROR_HANDLING.md`       | Error vs rejection semantics; invariant enforcement policy. |
| Shapes & Rotations | `SHAPES_AND_ROTATIONS.md` | Canonical tetromino geometry and rotation enumeration.      |

### Shell contracts

**Directory**: `docs/specs/shell/`

| Title                   | Filename            | Role                                                                  |
| ----------------------- | ------------------- | --------------------------------------------------------------------- |
| Runtime Specification   | `RUNTIME_SPEC.md`   | Tick loop, execution modes, and orchestration rules outside the core. |
| Rendering Specification | `RENDERING_SPEC.md` | ASCII rendering contract and output format.                           |
| CLI Specification       | `CLI_SPEC.md`       | Command-line surface and entrypoint behavior.                         |
| Replay Specification    | `REPLAY_SPEC.md`    | Deterministic replay format and validation rules.                     |

### API specifications

**Directory**: `docs/specs/api/`

| Title             | Filename          | Role                                                   |
| ----------------- | ----------------- | ------------------------------------------------------ |
| Core API          | `CORE_API.md`     | Public Python API contract for the deterministic core. |
| Renderer API      | `RENDERER_API.md` | Renderer interface and purity guarantees.              |
| Runtime API       | `RUNTIME_API.md`  | Runtime interface and orchestration boundaries.        |
| Configuration API | `CONFIG_API.md`   | Typed configuration model for composition and wiring.  |

### IO API specifications

**Directory**: `docs/specs/io/`

| Title            | Filename              | Role                                                            |
| ---------------- | --------------------- | --------------------------------------------------------------- |
| Input Driver API | `INPUT_DRIVER_API.md` | Input capture/translation boundary contract (outside the core). |
| Presenter API    | `PRESENTER_API.md`    | Presentation boundary contract (how outputs are surfaced).      |

---

## Core vs shell boundary

The system is intentionally split into:

- a **pure deterministic core** (the simulation), and
- **shell components** around it (runtime, rendering, CLI, replay, IO adapters).

This separation is not a stylistic preference; it is a **correctness constraint**.

The **core** defines game state evolution and must remain deterministic, side-effect-free, and testable in isolation. The **shell** exists to execute, observe, and interact with the core without re-implementing its logic.

This boundary is enforced by architecture/decomposition, acceptance gates, and component-specific test oracles. When in doubt, the rule is:

- gameplay semantics belong in the core specifications,
- execution, presentation, persistence, and I/O belong in the shell specifications.

---

## Relationship to testing

L3 defines **what must be true**. L4 defines **what counts as proof**.

A test suite is valid only to the extent that its assertions are grounded in L3 contracts and mapped through L4 oracles. Tests must not become a secondary source of behavior.

---

## Change rule

To change behavior:

1. update the relevant L3 specification(s) first,
2. then update the corresponding L4 oracle(s),
3. then update implementation and tests.

Changing implementation or tests without specification authority is treated as drift, not progress.
