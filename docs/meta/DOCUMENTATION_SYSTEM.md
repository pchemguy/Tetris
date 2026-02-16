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

The documentation base is organized into conceptual layers, from **L0 (highest level)** to **L5 (lowest level)**. Layer assignment for individual documents is derived  according to the mapping table below from the `kind` field (`DOC_SCHEMA.md`) or, equivalently, from the document's path.

| Layer | Responsibility                         | Top Layer Directory  | Main Entry            | `kind`         |
| ----- | -------------------------------------- | -------------------- | --------------------- | -------------- |
| L0    | Documentation infrastructure           | `docs/meta/`         | `L0_DOCUMENTATION.md` | `meta`         |
| L1    | Governance (process control)           | `docs/control/`      | `L1_GOVERNANCE.md`    | `control`      |
| L2    | System structure (global contracts)    | `docs/architecture/` | `L2_STRUCTURE.md`     | `architecture` |
| L3    | Behavioral specs (component contracts) | `docs/specs/`        | `L3_BEHAVIOR.md`      | `spec`, `api`  |
| L4    | Testing (proof obligations)            | `docs/testing/`      | `L4_TESTING.md`       | `oracle`       |
| L5    | Execution state (reports)              | `docs/reports/`      | `L5_REPORTS.md`       | `report`       |
| OUT   | Collection of ideas                    | `docs/ideas/`        | –                     | `idea`         |

These layers form a semantic model that separates concerns so that:

- higher-level contracts constrain lower-level artifacts, and    
- lower-level evidence can be interpreted against higher-level intent without circularity.

The core idea is straightforward: **higher layers define validity conditions** for lower layers. Lower layers produce **evidence** that those validity conditions are either satisfied or violated.

This creates two opposing but complementary flows.

---

### Constraint flow

This is what the vertical arrows represent.

* **L2 → L3**
    Architecture and decomposition define what components exist and where responsibilities lie; specifications must conform to those structural boundaries.
* **L3 → L4**
    Specifications define what must be true; test oracles define what must be demonstrated to support those claims.
* **L4 → L5**
    Oracles define what counts as valid evidence; reports record evidence and outcomes in that oracle vocabulary.

Constraint flows downward: higher layers constrain what lower layers are allowed to assert or record.

---

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

---

### 2.2 Layered abstraction

Development and maintenance of the documentation base is facilitated through adoption of a hierarchical, layered structure. At the top are the most abstract, system-wide documents (meta documents) that define the structure, organization, and conventions used throughout the documentation system. Lower-level documents become progressively more specific and focused, building upon the foundations established by higher-level documents. Higher layers define terms of validity for lower layers. Lower layers provide evidence or realization of higher-layer claims. Constraint flows downward. Interpretation flows upward.

---

### 2.3 Single responsibility documents

This documentation system also aims to maintain modular structure, with each document serving a narrowly defined purpose and having weak, well-defined couplings to other documents. Generally, documents should not embed responsibilities of other documents beyond their scope. Mixed-up responsibilities  encourage or cause complex interwoven dependencies, complicating discovery, interpretation, and development of documents.

---

### 2.4 Weak coupling and dependency control

Because layers represent **distinct development compartments**, unrestricted cross-layer semantic dependencies would undermine the separation they are meant to provide. If architecture depends on governance, or specifications depend on their own proof artifacts, circularity and conceptual drift quickly emerge. In other words, more specific documents may reference more general/abstract documents on which they depend. Documents must not depend semantically on more specific ones. "Spurious" references and circular semantic dependencies are explicitly discouraged. For this reason, the repository defines a **diagnostic policy** governing YAML `references` edges between layers. This policy does not affect structural validity, but it surfaces suspicious semantic couplings that may indicate meta-leakage or semantic circular dependency. The normative explanation of that policy is defined in `CROSS_LAYER_DEPENDENCY.md`.

---

### 2.5 Machine-checkable structure

Whenever practical, the documentation system should adopt conventions that are:

- expressible as machine-readable structured artifacts (for example, JSON or YAML documents), and    
- accompanied by corresponding machine-readable validation artifacts (for example, JSON Schema definitions).

Every important non-Markdown artifact should have a companion Markdown document with the same base filename (e.g., `X.md` describing `X.json` or `X.schema.json`). This Markdown document should explain artifact's

- purpose,
- conceptual structure,
- intended usage boundaries.

`X.md` may include suggested uses for the associated artifact, it should not prescribe or define any such uses - usage is generally out of scope of `X.md`, unless the use case is closely related and can be completely defined within `X.md`. This scope limitation generally improves clarity, minimizes coupling, and reduces the risk of circular semantic dependencies.

For example:

The documentation system prescribes that each document include a YAML metadata header defined in `DOC_SCHEMA.md` and validated by `DOC_SCHEMA.json`.

`DOC_SCHEMA.md` should:

- provide context and motivation for the metadata system,
- describe each metadata field and its semantics,
- specify that `DOC_SCHEMA.json` is the validation authority,
- optionally suggest how metadata may be used by tooling,

while deliberately avoiding prescribing specific tooling implementations.

More general documents may then reference `DOC_SCHEMA.md` when they depend on metadata semantics. Consider `DOC_INVENTORY.json` and `DOC_INVENTORY.schema.json`. These artifacts define a machine-readable document index, as described in `DOC_INVENTORY.md`. Although `DOC_INVENTORY.json` may include cached YAML metadata extracted from individual documents, the format and semantics of that metadata are not defined by the inventory artifact itself. Those semantics belong exclusively to `DOC_SCHEMA.md`.

Accordingly:

- `DOC_INVENTORY.md` defines repository discovery structure (e.g., paths, file identities, indexing rules),
- `DOC_SCHEMA.md` defines document metadata structure,
- neither artifact should subsume the other’s responsibilities.

File location and indexing are out of scope for `DOC_SCHEMA.md`, just as metadata structure is out of scope for `DOC_INVENTORY.md`. These concerns must remain separated to preserve modularity and avoid unnecessary coupling.

---

### 2.5 Document file names

- Uppercase A–Z, digits, underscore.
- Unique across repository.
- Regex: `^[A-Z][A-Z0-9_]+$`

