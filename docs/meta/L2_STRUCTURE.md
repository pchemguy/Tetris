---
doc_id: L2_STRUCTURE
name: L2_STRUCTURE.md
title: L2 - System Structure (Global Contracts)
status: active
authority: normative
description: Defines the structural contracts of the system - architecture, decomposition, and component registry.
references: [ARCHITECTURE, DECOMPOSITION, COMPONENT_REGISTRY]
---

# L2 — System Structure

This layer defines the **structural reality of the system**.

Structural documents answer:

- What components exist?
- What boundaries separate them?
- What dependencies are permitted?
- What architectural pattern governs the system?

These contracts constrain the implementation independently of behavioral details (L3), testing strategy (L4), or development order (L1).

---

## Document index

**Directory**: `docs/architecture/`

| Title                         | Filename                         | Role                                                                 |
| ----------------------------- | -------------------------------- | -------------------------------------------------------------------- |
| System Architecture           | `ARCHITECTURE.md`                | Defines architectural pattern and non-negotiable design principles.  |
| System Decomposition          | `DECOMPOSITION.md`               | Defines concrete component boundaries and allowed dependencies.      |
| Component Registry (Human)    | `COMPONENT_REGISTRY.md`          | Human-readable explanation of registered components and layers.      |
| Component Registry (Schema)   | `COMPONENT_REGISTRY.schema.json` | JSON Schema validating the registry instance.                        |
| Component Registry (Instance) | `COMPONENT_REGISTRY.json`        | Canonical machine-readable list of components and structural policy. |

---

## Authority of structural contracts

Documents in L2 are **normative structural contracts**.

They constrain:

- component existence and classification,
- dependency direction,
- responsibility boundaries,
- architectural pattern selection.

Structural violations are defects even if behavior appears correct.

---

## Architecture vs decomposition

The system distinguishes between two levels of structural authority:

### Architecture — conceptual model

`ARCHITECTURE.md` defines the governing architectural pattern and high-level principles (e.g., functional core / imperative shell).

It answers:

- Why is the system structured this way?
- What design principles are non-negotiable?
- What architectural styles are explicitly rejected?

Architecture constrains **design intent**.

---

### Decomposition — concrete boundaries

`DECOMPOSITION.md` defines the authoritative breakdown of the system into components and the dependency rules between them.

It answers:

- What components exist concretely?
- What is each responsible for?
- What must each not do?
- What dependencies are allowed?

Decomposition constrains **module boundaries and responsibility allocation**.

---

## Component registry

`COMPONENT_REGISTRY.json` is the canonical machine-readable declaration of components and their structural classification.

It exists to make structural contracts:

- machine-checkable,
- auditable,
- enforceable by tooling.

If the registry and decomposition diverge, the registry is invalid.

---

## Relationship to other layers

- L2 constrains **L3 (behavior)**: behavioral contracts must respect structural boundaries.
- L2 constrains **L4 (testing)**: tests must not violate architectural separation.
- L2 constrains **implementation**: code layout and dependencies must align with decomposition.
- L1 (governance) may stage delivery, but may not redefine structure.

---

## Change rule

Structural changes require:

1. updating `ARCHITECTURE.md` and/or `DECOMPOSITION.md`,
2. updating `COMPONENT_REGISTRY.json` if components change,
3. validating dependency rules,
4. then updating behavior and tests as necessary.

Implementation must never introduce structural change without prior structural authority.
