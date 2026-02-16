---
doc_id: DOC_LAYERS
name: DOC_LAYERS.md
title: Layered Documentation Classification and Semantics
kind: meta
scope: global
status: deprecated
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines the L0–L5 documentation layer model, its meaning, and semantic coupling constraints.
references:
  - DOC_SCHEMA
  - CROSS_LAYER_DEPENDENCY
---

## Overview

Documentation in this repository is organized in a **layered structure**. Each document belongs to a defined layer serving a distinct purpose in constraining, guiding, or evaluating the development process. This layering model is a **normative interpretation and constraint model** aligned with a structured compartmentalization of development concerns and effectively implementing high-level "separation of concerns". It is **not** a “who references whom” model and it is not a statement about where work must start. 

Each layer corresponds to a distinct conceptual role in the lifecycle of system definition, validation, and evaluation. The ordering reflects increasing operational concreteness:

* structural intent,
* behavioral definition,
* proof obligations,
* recorded execution state.

Layering therefore exists to:

* separate **structure from behavior**,
* separate **behavior from proof**,
* separate **proof from recorded evidence**,
* reduce cross-cutting coupling,
* prevent circular semantic dependencies,
* limit maintenance burden by enforcing responsibility boundaries at the documentation level.

---

## Structural model

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
│      - DOC_GRAPH_SPEC.md                                                       │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ constrains + validates
                                     v
┌────────────────────────────────────────────────────────────────────────────────┐
│ L1 — Governance (Process Control)                                              │
│      - PHASES.md                                                               │
│      - ACCEPTANCE_GATES.md                                                     │
│                                                                                │
│    Relationship: Phase allows attempting a gate; gates define correctness.     │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ constrains system structure
                                     v
┌────────────────────────────────────────────────────────────────────────────────┐
│ L2 — System Structure (Global Contracts)                                       │
│      - ARCHITECTURE.md                                                         │
│      - DECOMPOSITION.md                                                        │
│      - COMPONENT_REGISTRY.md / COMPONENT_REGISTRY.json                         │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ constrains behavior
                                     v
┌────────────────────────────────────────────────────────────────────────────────┐
│ L3 — Behavioral Specifications (Component Contracts)                           │
│      - Core specs                                                              │
│      - Shell specs                                                             │
│      - Shell APIs                                                              │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ defines required proof
                                     v
┌────────────────────────────────────────────────────────────────────────────────┐
│ L4 — Test Oracles (Proof Obligations)                                          │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ records execution history (state)
                                     v
┌────────────────────────────────────────────────────────────────────────────────┐
│ L5 — Execution State (Reports)                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
```

A higher layer defines the **terms of validity** for lower layers. A lower layer provides **evidence** about whether higher-layer claims are satisfied in practice.

There are therefore two opposed flows.

---

## Constraint / validity flow (top → bottom)

This is what the vertical arrows represent.

* **L2 → L3**
    Architecture and decomposition define what components exist and where responsibilities lie; specifications must conform to those structural boundaries.
* **L3 → L4**
    Specifications define what must be true; test oracles define what must be demonstrated to support those claims.
* **L4 → L5**
    Oracles define what counts as valid evidence; reports record evidence and outcomes in that oracle vocabulary.

Constraint flows downward: higher layers constrain what lower layers are allowed to assert or record.

---

## Meaning / diagnosis flow (bottom → top)

Interpretation flows in the opposite direction.

* **L5 has meaning only through L4.**
    A report or log is uninterpreted until an oracle defines the questions it answers.
* **L4 + L5 determine whether L3 is satisfied.**
    Oracles and results establish whether specifications hold.
* **L3 satisfaction (or failure) reflects back to L2.**
    Persistent failures may indicate either implementation defects or structural flaws in architecture or decomposition.

Progression of work tends to move downward.
Interpretation of results moves upward.

---

## Layering and semantic dependency control

Because layers represent **distinct development compartments**, unrestricted cross-layer semantic dependencies would undermine the separation they are meant to provide. If architecture depends on governance, or specifications depend on their own proof artifacts, circularity and conceptual drift quickly emerge. For this reason, the repository defines a **diagnostic policy** governing YAML `references` edges between layers. This policy does not affect structural validity, but it surfaces suspicious semantic couplings that may indicate meta-leakage or circular dependency. The normative explanation of that policy is defined in `CROSS_LAYER_DEPENDENCY.md`.

Layering is therefore:

* a conceptual hierarchy,
* a maintenance boundary mechanism,
* and a coupling-control strategy,

not a rigid import system and not a development sequence mandate.

---

## Position of meta-layers

### L0 (Documentation Infrastructure)

L0 operates at a different abstraction level.

It serves two distinct roles:

1. **Enablement and validation**
   It provides the mechanism that makes the documentation system machine-checkable: stable identifiers, scope inventory, graph extraction, and validation rules. L0 is logically prior (tooling depends on it), but it is semantically external to L2–L4. Development layers do not depend on L0 for meaning.
2. **System integration surface**
   The main documentation document, `DOCUMENTATION_SYSTEM.md` (this file), integrates and explains the documentation base as a whole, including L0 itself.

Consequences:

* L0 artifacts are required for enforcement and automation.
* A human can understand L2–L4 without knowing L0 exists, though it would be more difficult.
* While not strictly required, L0 is even more important for tooling and agents.

Development layers remain **meta-agnostic** by design.

---

### L1 (Governance)

L1 does not define system meaning. It defines **workflow governance**.

* L2–L4 define the system and correctness independent of phases or gates.
* L1 defines how change is managed in a controlled way (compartmentalization, sequencing, permission to attempt work).

Therefore:

* Architecture and decomposition (L2) can exist without governance (L1).
* Governance (L1) is meaningful only insofar as it governs L2–L4.

L1 is not “above” L2 in the semantic stack. It is above in the **control stack**. L2 does not depend on L1 for meaning; L1 depends on L2–L4 for substance.

---

## Conflict resolution rule

If two documents conflict:

1. Resolve by **authority** (`normative` over `non_normative`).
2. Resolve by explicit `supersedes` / `superseded_by`.
3. Resolve by **layer precedence** (L0 → L5), meaning higher-layer validity conditions override lower-layer artifacts.

---

## Layer index

| Layer | Question                           | Directory               |
| ----- | ---------------------------------- | ----------------------- |
| L0    | How the project is documented      | `docs/meta/`            |
| L1    | When work is allowed and evaluated | `docs/control/`         |
| L2    | What exists, how it is structured  | `docs/architecture/`    |
| L3    | What behavior is defined           | `docs/specs/`           |
| L4    | How correctness is proven          | `docs/testing/oracles/` |
| L5    | What has actually happened         | `docs/reports/`         |
| –     | What may be researched or tried    | `docs/ideas/`           |

## Canonical layer mapping

Layer assignment is derived solely from the `kind` field in YAML metadata as defined in `@DOC_SCHEMA` using a fixed mapping; paths and titles are non-authoritative.

| `kind`         | Layer | Notes                                                              |
| -------------- | ----- | ------------------------------------------------------------------ |
| `meta`         | L0    | Documentation infrastructure (schemas/graph spec/etc.)             |
| `map`          | L0    | Documentation inventory / authority maps                           |
| `control`      | L1    | Governance (phases, gates, process constraints)                    |
| `architecture` | L2    | System structure (architecture, decomposition, registry)           |
| `spec`         | L3    | Behavioral contracts (core/shell specs)                            |
| `api`          | L3    | Public adapter/API contracts; still behavioral, not infrastructure |
| `oracle`       | L4    | Proof obligations / test oracle definitions                        |
| `report`       | L5    | Execution state                                                    |
| `idea`         | OUT   | Not in L0–L5; explicitly non-normative by default                  |

If a normative document cannot be mapped to L0–L5, this is a **Gate 0 failure**.

---
## L1 — Governance (Process Control)

Documents in this class control the **development process itself**, not system behavior. They define **when certain kinds of work are permitted**, and **under what conditions progress is considered acceptable**. This class consists of two distinct, complementary documents with **non-overlapping authority**:

### Phases (`PHASES.md`) — *Scope control*

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

### Acceptance gates (`ACCEPTANCE_GATES.md`) — *Correctness and progression control*

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

### Relationship between phases and gates

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

### Gate applicability rules (normative)

The applicability of documents to acceptance gates defined in `ACCEPTANCE_GATES.md` is governed by the following rules:

- **Gate 0** applies universally as a discovery and compliance gate and therefore requires awareness of all normative documents, even if they are not yet implemented.
- **System-level contracts** apply to **all gates**. They constrain the system globally and must be obeyed at all stages.
- **Core / engine contracts** apply to **core gates (0–9)**. They define the pure simulation and must not be violated during core development or extension.
- **Shell contracts** apply to **Gate 0** (discovery and scope awareness) and to their respective **shell gates (10–13)** when implementation is permitted.
- **Core test oracle** (`CORE_TEST_ORACLE.md`) applies to **Gates 1–6**, and additionally to **Gates 7–9** if those optional core extensions are enabled.
- **Shell-level test oracles** apply to **exactly one gate each**, corresponding to the shell component they validate.

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

### Notes

- **Gate 0** applies in *all phases* as a discovery and compliance gate.
- Gates **1–6** define the **mandatory core MVP**.
- Gates **7–9** are optional core extensions and may be completed in Phase 1 or Phase 3.
- Gates **10–13** define shell/system completeness and must not be attempted before Phase 2.
- “(+ext.)” indicates that additional gates may be introduced for new shell variants.

---

## L2 — System Structure (Global Contracts)

Documents in this class define the **structural reality of the system**. They constrain *what the system is*, independent of behavior, tests, or development order. This class also consists of two distinct documents with **different levels of abstraction and authority**:

### Architecture (`ARCHITECTURE.md`) — *Conceptual design intent*

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

### Decomposition (`DECOMPOSITION.md`) — *Concrete component boundaries*

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

### Relationship between architecture and decomposition

* **Architecture** defines *why the system is shaped the way it is*.
* **Decomposition** defines *how that shape is realized in components*.

Architecture without decomposition is aspirational. Decomposition without architecture is arbitrary. Together, these documents ensure that:

* structural decisions are intentional,
* responsibility boundaries are explicit,
* implementation cannot silently drift.

All implementation must conform to **both**.

---

## L3 — Behavioral Specifications (Component Contracts)

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

## L4 — Test Oracles (Proof Obligations)

Test oracle documents define **what must be proven** for an implementation to be considered correct. They answer questions such as:

* Which behaviors must be tested?
* What scenarios are mandatory?
* What level of determinism is required?
* What constitutes sufficient coverage for acceptance?

Test oracles are **normative**: passing ad-hoc or convenience tests is insufficient if oracle-mandated tests are missing. Each test oracle applies to:

* a specific component, and
* a specific acceptance gate (or small range of gates).

---

## L5 — Execution State (Reports)

These documents record the **actual execution history** of agentic development. Unlike specifications or gates (which define what is allowed or correct), these documents

- define **state**, not policy,
- are **authoritative** for “current progress”,
- are required reading for any agent resuming work.

### Implementation reports (`IMPLEMENTATION_REPORTS.md`) — *Authoritative execution state*

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

