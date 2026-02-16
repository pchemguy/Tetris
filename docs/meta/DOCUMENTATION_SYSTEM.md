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
description: Defines the structure, authority rules, and roles of the repository's documentation infrastructure.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# Documentation Infrastructure System (Normative)

Documentation is an essential first-class subsystem of any technical project, not just of the code itself. This project attempts to adapt a number of software engineering principles and apply them directly to the documentation system to facilitate documentation development and maintenance and discovery by both humans and AI agents. 

---

## 1. Layer Model

The documentation base is organized into conceptual layers, from **L0 (highest level)** to **L5 (lowest level)**. Layer assignment for individual documents is derived  from the `kind` field in YAML metadata as defined in `DOC_SCHEMA.md` or, equivalently, from the document's path according to the table below.

|Layer|Responsibility|Top Layer Directory|Main Entry|`kind`|
|---|---|---|---|---|
|L0|Documentation infrastructure|`docs/meta/`|`L0_DOCUMENTATION.md`|`meta`|
|L1|Governance (process control)|`docs/control/`|`L1_GOVERNANCE.md`|`control`|
|L2|System structure (global contracts)|`docs/architecture/`|`L2_STRUCTURE.md`|`architecture`|
|L3|Behavioral specs (component contracts)|`docs/specs/`|`L3_BEHAVIOR.md`|`spec`, `api`|
|L4|Testing (proof obligations)|`docs/testing/`|`L4_TESTING.md`|`oracle`|
|L5|Execution state (reports)|`docs/reports/`|`L5_REPORTS.md`|`report`|
|OUT|Collection of ideas|`docs/ideas/`|–|`idea`|

These layers form a semantic model that separates concerns so that:

- higher-level contracts constrain lower-level artifacts, and    
- lower-level evidence can be interpreted against higher-level intent without circularity.

The core idea is straightforward: **higher layers define validity conditions** for lower layers. Lower layers produce **evidence** that those validity conditions are either satisfied or violated.

This creates two opposing but complementary flows.

### Constraint flow

This is what the vertical arrows represent.

* **L2 → L3**
    Architecture and decomposition define what components exist and where responsibilities lie; specifications must conform to those structural boundaries.
* **L3 → L4**
    Specifications define what must be true; test oracles define what must be demonstrated to support those claims.
* **L4 → L5**
    Oracles define what counts as valid evidence; reports record evidence and outcomes in that oracle vocabulary.

Constraint flows downward: higher layers constrain what lower layers are allowed to assert or record.

### Diagnosis flow

Interpretation flows in the opposite direction.

* **L5 has meaning only through L4.**
    A report or log is uninterpreted until an oracle defines the questions it answers.
* **L4 + L5 determine whether L3 is satisfied.**
    Oracles and results establish whether specifications hold.
* **L3 satisfaction (or failure) reflects back to L2.**
    Persistent failures may indicate either implementation defects or structural flaws in architecture or decomposition.

Progression of work tends to move downward. Interpretation of results moves upward.

---

### Model Generalization

This layered structure is not unique to this project. It can be generalized to many technical systems:

0. Documentation — how the project is described and organized
1. Governance / Process Control — when and how work is allowed
2. Architecture and Decomposition — what exists and how it is structured
3. Behavioral Specifications — how defined components must behave
4. Testing Specifications — how correctness is validated
5. Reporting — what evidence must be recorded and preserved

One additional conceptual layer often exists and covers external regulatory, legal, or standards documentation. Call this layer **LR** (Regulatory Layer). LR, when present, constrains all internal layers. It may impose requirements on documentation, governance, architecture, specifications, testing practices, and reporting.

---

## 2. Design principles

### 2.1 Document metadata

Automated document discovery is facilitated via YAML front matter that conforms to `DOC_SCHEMA.json` described in `DOC_SCHEMA.md`. The YAML header is included in each participating document as the authoritative metadata record for that document. This header should declare a stable identifier (`doc_id`). Documents may reference one another in prose using `@DOC_ID` markers as a convenience mechanism (for example, `@DOC_SCHEMA`). `@DOC_ID` references should reduce the risk of agents resolving filename-only references to non-sibling documents incorrectly (such as creating new empty files locally or substituting similar names). At the same time, conventional filename-only "same directory" references are still fine. YAML metadata remains authoritative, and `@DOC_ID` markers are validated against the repository’s declared identifiers. Tooling may use YAML metadata and `@DOC_ID` markers to validate references and construct a deterministic documentation graph.

### 2.2 Layered abstraction

Development and maintenance of the documentation base is facilitated through adoption of a hierarchical, layered structure. At the top are the most abstract, system-wide documents (meta documents) that define the structure, organization, and conventions used throughout the documentation system. Lower-level documents become progressively more specific and focused, building upon the foundations established by higher-level documents.

Higher layers define terms of validity for lower layers. Lower layers provide evidence or realization of higher-layer claims. Constraint flows downward. Interpretation flows upward.

### 2.3 Single responsibility weakly coupled documents and reference discipline

This documentation system also aims to maintain modular structure, with each document serving a narrowly defined purpose and having weak, well-defined couplings to other documents. Generally, documents should not embed responsibilities of other documents beyond their scope, as mixed-up responsibilities  encourage or cause awkward interwind dependencies, complicates discovery, interpretation, and development of documents.

Because layers represent **distinct development compartments**, unrestricted cross-layer semantic dependencies would undermine the separation they are meant to provide. If architecture depends on governance, or specifications depend on their own proof artifacts, circularity and conceptual drift quickly emerge. In other words, more specific documents may reference more general/abstract documents on which they depend. Documents must not depend semantically on more specific ones. "Spurious" references and circular semantic dependencies are explicitly discouraged. For this reason, the repository defines a **diagnostic policy** governing YAML `references` edges between layers. This policy does not affect structural validity, but it surfaces suspicious semantic couplings that may indicate meta-leakage or semantic circular dependency. The normative explanation of that policy is defined in `CROSS_LAYER_DEPENDENCY.md`.

and should not embed responsibilities of other documents beyond their scope
### 2.3 Machine-checkable structure

Whenever practical:

- Concepts must be expressible as structured artifacts (JSON/YAML).
    
- Structured artifacts must be validated via JSON Schema.
    
- Markdown descriptors must explain structured artifacts without embedding enforcement logic.
    

Example separation:

- `DOC_SCHEMA.md` defines metadata semantics.
    
- `DOC_SCHEMA.json` validates metadata structure.
    
- `DOC_INVENTORY.md` defines discovery rules.
    
- `DOC_INVENTORY.json` lists actual repository documents.
    
- Neither collapses into the other.
    



---

Whenever practical:

- Refactor documents to minimize repetition (DRY) and circular semantic dependencies.
- Develop conventions that can be readily
    - Encoded as machine readable structured artifacts (such as, JSON and YAML documents).
    - Accompanied by machine readable validation artifacts (such as, JSON schema).
- Describe each important non-Markdown artifact, such as document metadata validation schema, in a Markdown document having identical name part of filename, so that purpose/meaning/organization of the artifact could be easily discovered. Then reference this artifact descriptor where relevant (this is preferable to having back references within the artifact descriptor, as it will likely create increase document couplings and created circular references).
  
  For example, the documentation prescribes that each document should include a `YAML` metadata described in `DOC_SCHEMA.md` and validated by accompanied `DOC_SCHEMA.json`. `DOC_SCHEMA.md` should
    - provide context/motivation,
    - describe the metadata,
    - indicate that `DOC_SCHEMA.json` should be used for validating metadata,
    - possibly suggest how this metadata might be used, while avoiding **prescribing** or **referencing** any such use.
  
  Then more general documents may reference `DOC_SCHEMA.md`. For example, `DOC_INVENTORY.json` and `DOC_INVENTORY.schema.json` are concerned about providing a machine readable document index as described in associated `DOC_INVENTORY.md`. While `DOC_INVENTORY.json` might include not just paths, but also `YAML` metadata from individual documents, providing essentially a metadata cache, specific metadata format in individual documents is clearly out of scope for `DOC_INVENTORY.json`. Therefore, `DOC_INVENTORY.md` must only define explicitly only metadata related to repository discovery (such as file paths/names), while referencing `DOC_SCHEMA.md` for other metadata. Similarly, file location / index is clearly out of scope for `DOC_SCHEMA.md`, which is concerned about document's metadata irrespective of document's location. Hence, the two artifacts should not be collapsed. 

---

## 2. Naming conventions, metadata, and cross-document references

This repository adopts the following document naming convention:

- capital English letters, possibly numbers, and underscores,
- at least two characters with first being a letter (`^[A-Z][A-Z0-9_]+$`),
- all document names within the repository should have unique filename regardless of location.

Every document should include a `YAML` frontmatter header defined in `DOC_SCHEMA.md`. This header should declare a stable identifier (`doc_id`). Documents may reference one another in prose using `@DOC_ID` markers (for example, `@DOC_SCHEMA`) as a convenience mechanism. Documents may still reference other documents within the same directory using filenames. The primary motivation for introducing `@DOC_ID` references is to reduce the chances of agents resolving document references to documents not within the same directory incorrectly (such as potentially creating new empty file locally or substituting a similar name). YAML metadata remains authoritative, and `@DOC_ID` markers are validated against the repository’s declared identifiers. Tooling may use YAML metadata and `@DOC_ID` markers to validate references and construct a deterministic documentation graph.

---

## 3. Layered organization

The repository documentation system is organized into conceptual layers **L0–L5**. The normative definition of the layering model (meaning, constraint/validity vs diagnosis flows, meta-layer positioning, conflict resolution, and the layer index) is specified in `DOC_LAYERS.md`. Tooling uses this layer model to classify documents deterministically (via `kind`) and to support diagnostic validation of cross-layer semantic coupling.

Documentation in this repository is organized in a **layered structure**. Each document belongs to a defined layer serving a distinct purpose in constraining, guiding, or evaluating the development process. This layering model is a **normative interpretation and constraint model** aligned with a structured compartmentalization of development concerns. 

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

Each layer corresponds to a distinct conceptual role in the lifecycle of system definition, validation, and evaluation. In fact, this layered structure may be applicable conceptually to a broad range of technical problems.

0. Documentation - how the project is documented
1. Governance / Process Control
2. Solution architecture and decomposition analysis
3. Behavioral specs - how the end product components, defined in decomposition analysis, should behave
4. Testing specification - how to validate that the product and its components meet behavioral specs.
5. What information from testing and checks needs to be included in reports.

In fact, there exist one more important layer, not relevant for the present project, which is concerned with documentation external with respect to the project. This is regulatory and legal information, standards, etc. Let's call this layer LR. This layer, in fact, may constraint all of the above defined layers.

In the diagram above, a higher layer defines the **terms of validity** for lower layers. A lower layer provides **evidence** about whether higher-layer claims are satisfied in practice. If two documents conflict:

1. Resolve by **authority** (`normative` over `non_normative`).
2. Resolve by explicit `supersedes` / `superseded_by`.
3. Resolve by **layer precedence** (L0 → L5), meaning higher-layer validity conditions override lower-layer artifacts.


There are therefore two opposed flows.

- Constraint / validity flow (top → bottom)
  This is what the vertical arrows represent. Constraint flows downward: higher layers constrain what lower layers are allowed to assert or record.
    * **L2 → L3**
        Architecture and decomposition define what components exist and where responsibilities lie; specifications must conform to those structural boundaries.
    * **L3 → L4**
        Specifications define what must be true; test oracles define what must be demonstrated to support those claims.
    * **L4 → L5**
        Oracles define what counts as valid evidence; reports record evidence and outcomes in that oracle vocabulary.
- Meaning / diagnosis flow (bottom → top)
  Interpretation flows in the opposite direction. Progression of work tends to move downward. Interpretation of results moves upward.
    * **L5 has meaning only through L4.**
        A report or log is uninterpreted until an oracle defines the questions it answers.
    * **L4 + L5 determine whether L3 is satisfied.**
        Oracles and results establish whether specifications hold.
    * **L3 satisfaction (or failure) reflects back to L2.**
        Persistent failures may indicate either implementation defects or structural flaws in architecture or decomposition.

### Layering and semantic dependency control

Because layers represent **distinct development compartments**, unrestricted cross-layer semantic dependencies would undermine the separation they are meant to provide. If architecture depends on governance, or specifications depend on their own proof artifacts, circularity and conceptual drift quickly emerge. For this reason, the repository defines a **diagnostic policy** governing YAML `references` edges between layers. This policy does not affect structural validity, but it surfaces suspicious semantic couplings that may indicate meta-leakage or circular dependency. The normative explanation of that policy is defined in `CROSS_LAYER_DEPENDENCY.md`.

Layering is therefore:

* a conceptual hierarchy,
* a maintenance boundary mechanism,
* and a coupling-control strategy,

not a rigid import system and not a development sequence mandate.

### Canonical layer mapping

Layer assignment is derived solely from the `kind` field in YAML metadata as defined in using a fixed mapping; paths and titles are non-authoritative.

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

### Layer index

Layers also map directly to high-level `docs/` organization.

| Layer | Question                           | Directory            | Main Entry            |
| ----- | ---------------------------------- | -------------------- | --------------------- |
| L0    | How the project is documented      | `docs/meta/`         | `L0_DOCUMENTATION.md` |
| L1    | When work is allowed and evaluated | `docs/control/`      | `L1_GOVERNANCE.md`    |
| L2    | What exists, how it is structured  | `docs/architecture/` | `L2_STRUCTURE.md`     |
| L3    | What behavior is defined           | `docs/specs/`        | `L3_BEHAVIOR.md`      |
| L4    | How correctness is proven          | `docs/testing/`      | `L4_TESTING.md`       |
| L5    | What has actually happened         | `docs/reports/`      | `L5_REPORTS.md`       |
| -     | What may be researched or tried    | `docs/ideas/`        | -                     |
