---
doc_id: L2_STRUCTURE
name: L2_STRUCTURE.md
title: L2 — System Structure (Global Contracts)
kind: architecture
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines system architecture, decomposition, and component registry as authoritative structural contracts.
references:
  - ARCHITECTURE
  - DECOMPOSITION
  - COMPONENT_REGISTRY
---

# L2 — System Structure

## Document Index

**Directory**: `docs/architecture/`

| Title                               | Filename                         | Function / Role                                                                |
| ----------------------------------- | -------------------------------- | ------------------------------------------------------------------------------ |
| System Architecture                 | `ARCHITECTURE.md`                | High-level system architecture and design decisions (Functional Core / Shell). |
| System Decomposition                | `DECOMPOSITION.md`               | Explicit component decomposition and responsibility boundaries.                |
| Component Registry (Normative)      | `COMPONENT_REGISTRY.md`          | Human-readable explanation of registered components and layer model.           |
| Component Registry (Machine Schema) | `COMPONENT_REGISTRY.schema.json` | JSON Schema validating `COMPONENT_REGISTRY.json`.                              |
| Component Registry (Instance)       | `COMPONENT_REGISTRY.json`        | Canonical list of components, layers, and dependency policy.                   |

## Detailed description

Documents in this class define the **structural reality of the system**. They constrain *what the system is*, independent of behavior, tests, or development order. This class also consists of two distinct documents with **different levels of abstraction and authority**:

### Architecture (`ARCHITECTURE.md`) — *Conceptual design intent*

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
