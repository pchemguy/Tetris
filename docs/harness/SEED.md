# A framework for deterministically driving AI coding agents

Current objective is to evaluate current state of the project potential for the following objective:

Development of an application starting from documentation only and empty source code tests bases. The documentation must include a "roadmap" that splits the development process into a sequence of treatable coding/implementation steps. At each step, an agent is driven to implement some feature functionality as defined by the step's scope, create associated test suite, execute regression test suites declared by the step and implementation test suite until all tests pass and specifications are satisfied. The agent also creates reports and a file flag indicating completion of the step.

Overall development process needs to be compatible with deterministic orchestration. Like a set of algorithmic scripts determine the next step by examining the current contents of the repo, ENGINEER AGENT CONTEXT, and start an agent. (This, of course, could be also implemented as an agent skill.) Obviously, project documentation must contain explicit normative details providing a comprehensive definition of the target project and the development process.

The project, documentation, and application must be structured in such a way, that at each step it would be possible to provide a focused subset of documents forming a closure of the implementation scope defined by the step, as well as any dependencies.

The first task is to consider

- stated objectives,
- my early notes and reminder of key documents below

and assess current project/docs design/architecture state and its amenability to the specified objective. Do I have everything in place or do I miss important pieces/solutions? How can I address any such deficiencies. If the project is in the good state already, let's start discussing and articulating the framework.

## Early Notes

- This project uses a hierarchical markdown documentation system (`docs/meta/DOCUMENTATION_SYSTEM.md`) to organize development documentation and development process. Each normative markdown document carries YAML front matter (described in `docs/meta/DOC_SCHEMA.md` and related `docs/meta/DOC_INVENTORY.md`) defining a repository unique `DOC_ID` identifier (`^[A-Z][0-9A-Z_]+$`) that is used to cross reference documents without specifying their path. This ID is used with `@` prefix in prose (non-YAML), such as `@DOC_SCHEMA`. Formal references are included as a `YAML` array `references` without `@`. Similar IDs are also used to label (and reference) specific document sections within embedded secondary YAML blocks where necessary.
- Documentation system hierarchy reflects the structure of the development process. Additionally, for non-doc artifacts that may be produced and used by coding agents, conventional file-system-based structure is defined to compartmentalize artifacts and enable deterministic automated discovery.
- With formal YAML references and cross references (per doc, per spec file, per oracle file, per oracle case), it should be possible to define a doc closure for each gate (key top-level docs plus gate specific l3-l4 docs). For example, for regression tests, agent only need the set of related tests to run and no l3/l4 docs. Tests for each oracle are placed in a conventional tests/ subdir, also enabling automated deterministic selection of specific test set.
- Need a flag indicating completed gate.

- Each agent run starts with initial context formation. Assuming no cross-run context memory, this context must provide
    - a complete big picture (top-level key docs),
    - a means for agent to understand current project state (what is done? what to do next?),
    - doc closure and/or instructions how to compute it (ideally deterministically using a script).

Assume agents are instructed to create tests in 


- Tests
  For each test oracle spec `ORACLE_ID/DOC_ID: ORACLE_<SCOPE>_<TOPIC>` a dedicated test suite should be created under
    - `tetris/tests/<scope>_<topic>/`.
  When a gate listing given test oracle spec file as "implementation" (there should exactly one such gate), this test suite is created/updated and executed to validate implementation correctness. When this gate is identified as dependency for a later gate (via gate or family dependency), this test suite will need to be executed according to protocol as a regression test suite; each gate may declare multiple dependent gates, and for each such dependency their respective implementation test suite is executed as a regression test suite for the dependent gate.
- Reports
    - `docs/reports/regression/{GATE_ID_REGRESSION_GATE}/{GATE_ID_DEPENDENT_GATE}/`
    - `docs/reports/implementation/{GATE_ID}/` 

Acceptance Gates partition development process into logical blocks, such that each gate defines implementation scope that can be implemented next, provided all defined prereqs (prior gates and gate families) are already implemented. Implementation involves 

- developing source code according to gate scope and defined associated spec files
- creating associated test suite according to test oracle spec identified as implementation test oracle by the gate
- running regression test suites and creating reports under `docs/reports/regression/{GATE_ID_REGRESSION_GATE}/{GATE_ID_DEPENDENT_GATE}/` for each regression test suite
- running implementation test suite and creating reports under `docs/reports/implementation/{GATE_ID}/` 
- once all tests are passed successfully and all specs are otherwise fulfilled, a completion flag, such as `docs/reports/implementation/{GATE_ID}/completed.flag` can be created.

So, a basic deterministic algo for comprehensive context engineering for coding agent might involve (e.g., via Python scripts executed by the agent or externally by orchestrating process):

- add top-level key docs, architecture/decomposition, acceptance gates (control), documentation system overview, probably also harness describing file. JSON files may or may not needed to be added to the context: if required doc closure, as well as any other pieces necessary for specific work scope defined by acceptance gate to be implemented can be produced via a script deterministically, only those artifacts may need to be added to the initial context, possibly instructing agent how to locate other artifacts, if necessary.
- obtain the inventory of gate families and gates (probably from a JSON or YAML file from a predefined location).
- determine next target
    1. verify that all previously started gates are completed:
        - list all subdirs in `docs/reports/implementation/` in ascending order
        - for each subdir name matching `GATE_ID` from the inventory, verify that the `docs/reports/implementation/{GATE_ID}/completed.flag` file exists.
            - If not, this is an incomplete gate and the next target. Agent would need to assess whether it can be resumed without a human intervention by analyzing report files. If possible, agent would need to go through implementation protocol steps, find which is the last implemented step and resume; otherwise, abort and escalate.
    2. find the smallest index `GATE_ID` (`GX.Y`) without corresponding existing `docs/reports/implementation/{GATE_ID}/` - this is the next target.
- extract from gate YAML implementation oracle and dependent gates list.
- if current gate family defines `GX.0`, extract family dependency list and recursively identify family dependency closure.
- construct oracle dependency closure by extracting implementation oracle from each gate dependency, as well as for all gates belonging to family dependency closure.
- transform each oracle dependency into a test suite subdir to be executed as part of regression testing before any work is performed and after implementation suite of the current gate passes.
- construct behavioral contract closure by extracting recursively all `DOC_ID`s corresponding to behavioral contracts from the oracle file YAML `references` key. Discard any DOC_IDs starting with `ORACLE_`, for remaining DOC_IDs consult doc inventory for path (probably under `docs/specs/`; verify `L3` prefix in documentation system description; probably mapping should be included in doc inventory) or layer (`L3`) designation.

## Reminder of key documents

Recall, that for my Tetris project (the current project) I have developed a layered docs system with metadata, cross references, machine readable artifacts, and associated scripts (developed or planned).

~~~
---
doc_id: DOCUMENTATION_SYSTEM
name: DOCUMENTATION_SYSTEM.md
title: Documentation Infrastructure System
status: active
authority: normative
description: Defines the structure, authority rules, and roles of the repository's documentation infrastructure.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# Documentation Infrastructure System (Normative)

Documentation is an essential first-class subsystem of any technical project, not just of the code itself. This project attempts to adapt a number of software engineering principles and apply them directly to the documentation system to facilitate documentation development and maintenance and discovery by both humans and AI agents. 

---

## 1. Layer Model

The documentation base is organized into conceptual layers, from **L0 (highest level)** to **L5 (lowest level)**. Layer assignment for individual documents is derived  according to the mapping table below from the document's path.

| Layer | Responsibility                         | Top Layer Directory  | Main Entry            |
| ----- | -------------------------------------- | -------------------- | --------------------- |
| L0    | Documentation infrastructure           | `docs/meta/`         | `L0_DOCUMENTATION.md` |
| L1    | Governance (process control)           | `docs/control/`      | `L1_GOVERNANCE.md`    |
| L2    | System structure (global contracts)    | `docs/architecture/` | `L2_STRUCTURE.md`     |
| L3    | Behavioral specs (component contracts) | `docs/specs/`        | `L3_BEHAVIOR.md`      |
| L4    | Testing (proof obligations)            | `docs/testing/`      | `L4_TESTING.md`       |
| L5    | Execution state (reports)              | `docs/reports/`      | `L5_REPORTS.md`       |
| OUT   | Collection of ideas, drafts, etc.      | `docs/archive/`      | –                     |

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

### Orthogonal Decomposition Axes

The layered model described above defines a **vertical decomposition of authority**. However, the system also contains a second, orthogonal form of decomposition that must be understood clearly.

Layers L2 and L3 decompose the system along **structural and behavioral boundaries**:

* **L2 (Architecture)** defines what exists and how it is partitioned.
* **L3 (Specifications)** defines what each structural element must do.

This is a decomposition of the system itself.

Layer L4, by contrast, does not decompose the system structurally. It decomposes the **proof of correctness**. In other words:

* L2/L3 answer: *What is the system and how must it behave?*
* L4 answers: *What must be demonstrated to prove that behavior is satisfied?*

The oracle decomposition in L4 therefore forms a second axis that cuts across L2/L3 contracts. An oracle may depend on multiple behavioral specifications, and a single specification may be validated by multiple oracles. This is intentional.

These two decompositions are not redundant; they represent different concerns:

* **Contract decomposition** (L2/L3) — system structure and semantics.
* **Validation decomposition** (L4) — correctness obligations and evidence.

Maintaining this separation prevents common failure modes such as:

* tests silently redefining behavior,
* architectural boundaries eroding under implementation pressure,
* implementation order being dictated accidentally by file layout rather than correctness obligations.

The documentation system therefore models:

1. Vertical authority flow (L0 → L5),
2. Structural decomposition (architecture → components),
3. Behavioral decomposition (specification contracts),
4. Orthogonal validation decomposition (oracle domains).

This multi-axis structure is deliberate and generalizable beyond this project. It allows both humans and agents to reason about implementation order, correctness boundaries, and diagnostic signals without collapsing architecture into tests or tests into architecture.

---

### Implementation Order Derivation Model

The documentation system defines *what is true* and *what must be proven*. It does not directly prescribe implementation order. However, implementation order must be derived in a disciplined way from the existing axes.

#### 1. Structural prerequisite rule (L2 → L3)

Implementation must respect structural authority first.

- If a component does not exist in L2 (Architecture / Decomposition), it must not be implemented.
- If a contract is not defined in L3, behavior must not be invented.

Therefore:

* Implementation begins from **defined structural components**.
* Within each component, behavior is governed exclusively by its specification documents.

This prevents speculative implementation.

---

#### 2. Oracle-driven sequencing rule (L4 → L3 realization)

While contracts define behavior, **oracles define proof obligations**. Oracles are not structural units; they are correctness partitions. Because oracles often span multiple specifications, satisfying a given oracle may require:

* implementing parts of multiple behavioral contracts,
* completing certain state transitions before others,
* deferring some spec sections until prerequisite invariants exist.

Therefore:

> Implementation sequencing should be guided primarily by oracle decomposition, not by specification file order.

Example pattern:

* `ORACLE_CORE_COLLISION` depends on geometry + board bounds + rejection semantics.
* That implies geometry must exist before collision is testable.
* Therefore geometry is implemented before or alongside collision logic, even if the specification document order differs.

This rule makes validation drive sequencing.

---

#### 3. Minimal-satisfiable slice principle

At any given gate:

* Identify the oracle(s) required for that gate.
* Determine the minimal subset of behavioral contracts necessary to satisfy that oracle.
* Implement only that subset.
* Run tests immediately.
* Stop when the oracle passes.

This produces incremental, non-speculative development.

It also aligns directly with acceptance gates.

---

#### 4. Bidirectional diagnostic feedback

If an oracle cannot be satisfied:

1. First suspect implementation.
2. Then re-check specification clarity.
3. Only then escalate to architecture reconsideration (L2).

Structural reconsideration must never be triggered by convenience — only by persistent oracle failure.

This maintains authority direction.

---

#### 5. What this model prevents

Without this model, common failure modes include:

* Implementing entire spec documents before validating any behavior.
* Writing code in spec file order rather than correctness dependency order.
* Letting test structure silently redefine architecture.
* Over-implementing features not required by current gate.

This model ensures:

* Contracts define boundaries.
* Oracles define stopping points.
* Gates define scope.
* Phases define permission.

---

### Resulting Implementation Heuristic

When asked to “implement the next piece”:

1. Determine current Phase and Gate (L1).
2. Identify required oracle(s) (L4).
3. Identify dependent behavioral contracts (L3).
4. Confirm structural legitimacy (L2).
5. Implement minimal code required to satisfy oracle.
6. Validate.
7. Record in L5.
8. Stop.

That is the complete loop.

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
~~~

~~~
---
doc_id: DOC_SCHEMA
name: DOC_SCHEMA.md
title: Documentation Metadata Schema
status: active
authority: normative
description: Normative schema for YAML metadata embedded in repository Markdown documents.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [COMPONENT_REGISTRY]
---

# Documentation Metadata Schema (Normative)

## 1. Purpose

This document defines the **normative metadata system** used in the YAML front matter of Markdown documents in this repository. It exists to make documentation **machine-checkable** and to support:

- deterministic document discovery,
- explicit authority classification (`normative` vs `non_normative`),
- automated validation of cross-document dependencies,
- detection of duplicates, drift, and misclassification.

The authoritative machine schema is **`DOC_SCHEMA.json`**.

---

## 2. Participation and authority

### 2.1 Participating documents under `docs/`

All Markdown documents intended to participate in the repository’s documentation system MUST include a YAML front matter block that validates against `DOC_SCHEMA.json`. Root-level documents are allowed to participate, but the minimum expectation is:

- all **normative** documents under `docs/` include metadata,
- any document explicitly named in `AGENTS.md` includes metadata,
- any document reachable from `AGENTS.md` by following YAML `references` includes metadata.

### 2.2 Authority constraints by location

Some directories are defined as **non-normative zones** by policy, regardless of content.

Any Markdown document located under:

- `docs/archive/`
- any directory whose name matches (case-insensitive, exact directory component match):
    - `idea`, `ideas`, `archive`, `archives`, `draft`, `drafts`, `note`, `notes`

MUST be treated as **non-normative** regardless of metadata.  
Rationale: location is a deliberate governance signal; “ideas/drafts/archives” must not acquire authority accidentally.

---

## 3. YAML front matter requirements

### 3.1 Location

The YAML front matter block:

- MUST appear at the top of the file,
- MUST begin with `---` and end with `---`,
- MUST appear before substantive content (within the first ~30 lines).

### 3.2 Required keys

Every participating document MUST include the following keys:

- `doc_id`
- `name`
- `title`
- `status`
- `authority`

Additionally, it MAY include the following optional keys:

- `description`
- `{url | urls}`
- `references`

Notes:

- Keys are case-sensitive and MUST match exactly.
- Required YAML lists MUST be populated even when empty (`[]`).
- Required keys only: YAML `null` MUST be explicit where allowed (`null`).
- Optional keys: MUST be omitted when empty.

---

## 4. DOC_ID system (normative)

### 4.1 Lexical format

`doc_id` is a stable identifier for a document.

It MUST match:

- `^[A-Z][0-9A-Z_]+$`

Rules:

- Uppercase `A–Z`, digits `0–9`, underscore `_` only.
- Must start with a letter.
- No dots, hyphens, spaces, or slashes.
- Globally unique within the repository.

Examples:

- `PHASES`
- `ACCEPTANCE_GATES`
- `ARCHITECTURE`
- `DECOMPOSITION`
- `RUNTIME_SPEC`
- `RENDERING_TEST_ORACLE`
- `PRESENTER_API`

Non-examples:

- `runtime_spec` (lowercase)
- `RUNTIME-SPEC` (hyphen)
- `TETRIS.RUNTIME.SPEC` (dots)

Any violation of these rules  is a **hard failure** (Gate 0).

### 4.2 Identity rules

- `doc_id` is the **authoritative identity**; paths and filenames are not.
- Once a document is `status: active`, its `doc_id` MUST NOT change.
- If a new identity is required:
    - create a new document with a new `doc_id`,
    - mark the old document `deprecated` if appropriate.

### 4.3 YAML references

Any `doc_id` within the `references` field MUST point to an existing participating document.

Policy:

- For `authority: normative` documents, all `references` targets MUST exist and MUST NOT be “missing from inventory”.
- Referencing `non_normative` documents is permitted, but should be considered suspicious and may be flagged diagnostically (non-blocking unless a stricter policy document requires it).

---

## 5. Prose reference marker: `@DOC_ID` (non-authoritative convenience)

### 5.1 Purpose

In Markdown body text, authors may cite other documents with:

- `@DOC_ID`

This is a convenience for humans and tooling.

### 5.2 Rules

- `@DOC_ID` references are **not authoritative**. YAML is authoritative.
- YAML metadata MUST NOT contain `@` in any field.
- Tooling MAY:
    - extract `@DOC_ID` tokens from prose,
    - ignore fenced code blocks (treat as examples),
    - validate extracted tokens against the set of YAML `doc_id` values.

### 5.3 Formatting allowances

`@DOC_ID` may appear as:

- `@DOC_ID`
- `@DOC_ID,`
- `(@DOC_ID)`
- `"@DOC_ID"`
- `*@DOC_ID*`
- `_@DOC_ID_`
- `` `@DOC_ID` ``

Tooling should interpret these as references to `DOC_ID` and validate accordingly.

---

## 6. Field semantics (normative)

- `name`
    - The expected filename.
    - Not authoritative identity; supports review and auditing.
- `title`
    - Human-readable title.
- `status`
    - `draft`, `active`, `deprecated`.
- `authority`
    - `normative` or `non_normative`.
- `description`
    - Short human-readable summary (1–3 sentences recommended).
- `url` / `urls`
    - Optional external reference(s).
    - `urls` exists only when multiple links are necessary.
    - A doc MUST NOT include both `url` and `urls` keys simultaneously.
- `references`
    - Array of DOC_IDs this document depends on (normative dependency list).
    - This is the **authoritative dependency graph** (not filenames).

---

## 7. Validation expectations (Gate 0 auditable)

An agent (or CI) MUST treat the following as a Gate 0 failure:

- a required participating document is missing YAML front matter,
- YAML fails validation against `DOC_SCHEMA.json`,
- duplicate `doc_id` exists,
- `references` points to a `doc_id` that does not exist in the YAML inventory,
- `url` and `urls` are both populated (or both provided non-empty).

---

## 8. Minimal compliant header example

```yaml
---
doc_id: RUNTIME_SPEC
name: RUNTIME_SPEC.md
title: Runtime Loop and Execution Modes
status: active
authority: normative
description: Defines execution modes and per-tick orchestration rules outside the core.
url: https://someurl.com
references: [DECOMPOSITION, CORE_API, INPUT_MODEL]
---
```

---

## 9. Relationship to machine schemas

- `DOC_SCHEMA.md` is the **human-readable normative policy**.
- `DOC_SCHEMA.json` is the **machine-checkable schema**.

If there is a conflict:

1. machine schemas MUST be updated to match this document, or
2. this document MUST be updated intentionally.

Silent divergence is forbidden.
~~~

~~~
---
doc_id: DOC_INVENTORY
name: DOC_INVENTORY.md
title: Machine-Readable Documentation Inventory Specification
status: active
authority: normative
description: Defines the canonical machine-readable documentation inventory format (DOC_INVENTORY.json) used for discovery, validation inputs, and downstream tooling.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [DOC_SCHEMA, DOCUMENTATION_SYSTEM]
---

# Machine-Readable Documentation Inventory Specification (Normative)

## 1. Purpose

This document defines the **canonical machine-readable documentation inventory** used for:

- deterministic **project discovery**,
- stable inputs to documentation tooling,
- validation reporting (schema + reference diagnostics),
- downstream derivatives (e.g., rendered graphs, reports).

This spec defines the format of:

- `DOC_INVENTORY.json` (required output artifact)

This spec does **not** define graph rendering, which is out of scope for this document.

---

## 2. Canonical artifact and script generator

Tooling MUST be able to produce the documentation inventory and validate it against its schema, as defined in the table below. A reference implementation of the generator script is included in this repository.

| Artifact         | Relative Path                                 |
| ---------------- | --------------------------------------------- |
| Inventory file   | `docs/meta/DOC_INVENTORY.json`                |
| Schema           | `docs/meta/DOC_INVENTORY.schema.json`         |
| Generator script | `docs/meta/scripts/generate_doc_inventory.py` |

* The inventory filename (`DOC_INVENTORY.json`) and schema filename (`DOC_INVENTORY.schema.json`) are **normative**.
* The generator script is a **reference implementation**; its filename and directory are conventional.
* Any alternative implementation MUST produce output conforming to `DOC_INVENTORY.schema.json` and MUST satisfy the determinism rules defined in §5.
* The inventory artifact (`DOC_INVENTORY.json`) remains the authoritative discovery surface.

---

## 3. Inventory is the discovery surface

Discovery MUST be possible without reading any human-readable index document.

Therefore:

- Gate 0 and agent discovery MUST refer to `DOC_INVENTORY.json` as the canonical “what docs exist” index.
- Human-readable indices (e.g., `DOCUMENTATION_SYSTEM.md`) MAY exist, but MUST NOT be required for discovery.

---

## 4. Inventory content model (normative)

### 4.1 Top-level shape

`DOC_INVENTORY.json` MUST have this top-level structure:

```json
{
  "format": "DOC_INVENTORY",
  "generated_at": "2026-02-13T12:34:56Z",
  "repo": {
    "doc_system_doc_id": "DOCUMENTATION_SYSTEM",
    "root": "."
  },
  "docs": []
}
````

Rules:

* `format` MUST be `"DOC_INVENTORY"`.
* `generated_at` is informational only.
* `repo.*` is informational only and MUST NOT be used as authoritative identity.
* `doc_system_doc_id` points to the root / main entry document via its `DOC_ID` (`DOC_SCHEMA.md`)

### 4.2 Document entry shape

Each element in `docs[]` MUST include:

```json
{
  "doc_id": "DOC_SCHEMA",
  "name": "DOC_SCHEMA.md",
  "path": "docs/meta/",
  "kind": "meta",
  "layer": "L0",
  "scope": "global",
  "status": "active",
  "authority": "normative",
  "gate_applies_to": "all",
  "phase_applies_to": "all"
}
```

Rules:

* The above fields are REQUIRED for every participating artifact.
* `layer` is **computed** from `kind` or path using the mapping table in `DOCUMENTATION_SYSTEM.md`.
* `path`
    * is derived from filesystem location at generation time,
    * must be relative to project directory / repository root,
    * must not include filename (the `name` field).
* Remaining fields come from YAML frontmatter of documents per `DOC_SCHEMA.md`.

### 4.3 Optional fields

A document entry MAY include optional fields per `DOC_SCHEMA.md`:

1. All optional fields MUST be **omitted** if empty.
2. A doc MUST NOT contain both `url` and `urls`.

---

## 5. Determinism rules (normative)

To ensure stable diffs and stable agent behavior:

* `docs[]` MUST be sorted by (`path`, `doc_id`) ascending (lexicographic).
* Within each doc entry, arrays (if present) MUST be sorted ascending:
    * `references`, `supersedes`, `urls`
* Tools MUST NOT emit duplicates in:
    * `docs[]`
    * any array field

---

## 6. Relationship to validation

Inventory generation MUST perform:

* YAML parsing and schema validation against `DOC_SCHEMA.json`,
* dependency validation for YAML `references` ("target missing from inventory" per `DOC_SCHEMA.md`),
* optional diagnostics using `YAML_REFERENCE_POLICY.md`.

Validation outputs MAY be written separately (e.g., a report JSON), but the inventory MUST remain constructible even if diagnostics produce warnings.

Hard failures that MUST prevent emitting an inventory:

* duplicate `doc_id`,
* YAML schema invalid,
* required docs missing YAML (per Gate 0 policy),
* YAML `references` target missing from inventory,
* normative doc cannot be classified to L0–L5.

Warnings that MUST NOT block:

* prose mention targets missing (`@DOC_ID`),
* cross-layer reference policy violations per `YAML_REFERENCE_POLICY.md`.

---

## 7. Scope

`DOC_INVENTORY.json` is a canonical representation of documentation metadata and discovery state.

It is intentionally **not** a rendered graph and intentionally does not encode layout, which is out of scope for this document.

---
~~~

~~~
---
doc_id: TESTING_CONVENTIONS
name: TESTING_CONVENTIONS.md
title: Testing Conventions
status: active
authority: normative
urls:
  - https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
  - https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [TEST_STRATEGY]
---

# TESTING_CONVENTIONS

## 1. Purpose

This document defines repository-specific **mechanical conventions** for implementing the testing strategy defined in `TEST_STRATEGY.md`.

It specifies:

- Directory layout for test artifacts
- Oracle specification organization
- Naming patterns and ID formats
- Oracle-to-pytest translation rules
- Determinism enforcement mechanics
- Run report conventions

It does **not** define:

- What correctness means
- What may be asserted
- Authority derivation rules
- Change-control policy

Those are defined in `TEST_STRATEGY.md`.

This document defines **how** testing decisions are encoded in this repository.

---

# 2. Test Artifact Structure

## 2.1 Oracle Specifications

Oracle specifications are normative testing documents:

- `kind: testing`
- `authority: normative`

They are organized by architectural scope:

Core-level:
```

docs/testing/oracles/core/

```

Shell-level:
```

docs/testing/oracles/shell/

```

Each oracle document governs exactly **one behavioral domain**.

Examples of domains:

- collision and bounds
- geometry and rotations
- spawn semantics
- gravity and locking
- line clearing
- scoring
- RNG behavior
- game-over conditions
- invariants
- rendering
- runtime orchestration
- CLI behavior
- replay execution
- configuration boundaries

No monolithic oracle documents are allowed.

If cross-domain traceability is required, it must be expressed in an index document (e.g., `ORACLE_*_INDEX.md` and corresponding machine-readable index).

---

## 2.2 Pytest Layout

All executable tests live under:

```

tetris/tests/

```

Recommended structure:

```

tetris/tests/
├── core/
├── rendering/
├── runtime/
├── cli/
├── replay/
├── config/
└── shared/

```

Each directory mirrors an oracle domain.

Cross-domain mixing inside a single module is forbidden.

---

# 3. Naming Conventions

## 3.1 Oracle File Naming

Format:

```

ORACLE_<SCOPE>_<DOMAIN>.md

```

Examples:

- `ORACLE_CORE_COLLISION.md`
- `ORACLE_CORE_GRAVITY_AND_LOCKING.md`
- `ORACLE_SHELL_RENDERING.md`

Rules:

- File name must match the declared `doc_id`.
- Exactly one domain per file.
- File renaming requires corresponding metadata update.
- Oracle files must not contain implementation guidance.

---

## 3.2 ORACLE_ID Format

Format:

```

ORACLE_<SCOPE>_<DOMAIN>

```

Examples:

- ORACLE_CORE_COLLISION
- ORACLE_CORE_RNG_7BAG
- ORACLE_SHELL_RUNTIME

Rules:

- ORACLE_ID equals the `doc_id`.
- Stable and never reused.
- Never semantically repurposed.

---

## 3.3 CASE_ID Format

Format:

```

CASE_<SCOPE>*<DOMAIN>*<NNN>

```

Examples:

- CASE_CORE_COLLISION_001
- CASE_CORE_GRAVITY_002
- CASE_SHELL_RUNTIME_004

Rules:

- Each CASE_ID belongs to exactly one ORACLE_ID.
- Stable and unique.
- Never reused.
- Never renumbered retroactively.
- Once published, must not change semantic meaning.

---

## 3.4 Pytest Module Naming

Format:

```

test_<domain>.py

```

Examples:

- `test_collision.py`
- `test_gravity.py`
- `test_runtime.py`

One translation module per oracle domain.

---

## 3.5 Test Function Naming

Format:

```

test_<case_id_lowercase>()

```

Example:

```

test_case_core_collision_001()

```

The CASE_ID must appear in:

- the test function name, or
- a comment directly above the test.

No test may exist without an associated CASE_ID.

---

# 4. Oracle-to-Pytest Translation Rules

## 4.1 Module Header (Mandatory)

Each pytest module must declare:

- The oracle document path
- The ORACLE_ID implemented

Example:

```

Implements:

* docs/testing/oracles/core/ORACLE_CORE_COLLISION.md
* ORACLE_CORE_COLLISION

```

---

## 4.2 Case Mapping

Each CASE_ID defined in an oracle document must:

- Be implemented exactly once in pytest, and
- Map to one deterministic assertion block.

No CASE_ID may:

- Exist without a test,
- Be implemented multiple times,
- Be merged across domains.

Parametrization is allowed only when:

- Structure is identical, and
- CASE_ID mapping remains explicit and visible.

Dynamic test generation that obscures CASE_ID traceability is forbidden.

---

# 5. Determinism Enforcement Mechanics

## 5.1 Randomness

- All RNG must be seeded.
- Tests must inject deterministic seed values.
- No use of unseeded random sources.
- No reliance on ambient entropy.

---

## 5.2 Time

- No use of `time.sleep()` in tests.
- Runtime tests must use virtual-time stepping.
- Tests must not depend on wall-clock timing.
- Frame advancement must be deterministic.

---

## 5.3 Replay Tests

Replay tests must:

- Load replay traces deterministically.
- Assert full-state equivalence when specified.
- Avoid heuristic comparisons.

Partial comparison is allowed only if explicitly defined in the oracle.

---

# 6. Fixtures and Utilities

## 6.1 Fixture Placement

- Domain-specific fixtures live inside their domain directory.
- Shared fixtures go in `tetris/tests/conftest.py` or `shared/`.

---

## 6.2 Fixture Constraints

Fixtures must not:

- Mutate global state.
- Depend on environment variables.
- Depend on filesystem unless explicitly required by shell tests.
- Introduce non-deterministic behavior.

---

# 7. Regression Test Additions

When a defect is discovered:

1. Update the appropriate `ORACLE_*` document first.
2. Add or refine the corresponding CASE_ID.
3. Implement the pytest translation.
4. Ensure ORACLE_ID and CASE_ID traceability.

Tests must not precede normative oracle definition.

Test-first changes are allowed only if the oracle is updated in the same change set.

---

# 8. Run Report Conventions

Test reports must be stored in:

```

docs/testing/reports/

```

Recommended naming:

```

TEST_RUN_<YYYYMMDD>_<HHMMSS>.md

```

Reports must include:

- Timestamp
- Python version
- pytest version
- Suite executed
- Pass/fail counts
- Failing CASE_ID references

Reports are append-only unless explicitly reset by governance decision.

---

# 9. Optional Pytest Markers

If markers are used, they must reflect architectural scope only:

- `@pytest.mark.core`
- `@pytest.mark.shell`
- `@pytest.mark.runtime`
- `@pytest.mark.rendering`
- `@pytest.mark.replay`
- `@pytest.mark.cli`
- `@pytest.mark.config`

Markers must not encode policy or gate status.

---

# 10. Mechanical Prohibitions

The following are mechanically forbidden:

- Tests without CASE_ID mapping.
- Multiple domains inside a single translation module.
- Cross-domain imports violating architectural boundaries.
- Snapshot tests outside renderer domain unless explicitly authorized.
- Weakening assertions without oracle update.
- Hardcoded values not traceable to normative documentation.
- Silent test skipping.
- Conditional weakening of invariants.

---

# 11. Relationship to Strategy

`TEST_STRATEGY.md` defines:

- What may be asserted.
- What constitutes correctness.
- Authority and governance rules.
- Change control policy.

This document defines only the mechanical encoding of those decisions.
~~~

~~~
---
doc_id: TEST_SUITE_LAYOUT
name: TEST_SUITE_LAYOUT.md
title: Test Suite Layout and Oracle Mapping Rules
status: active
authority: normative
description: Defines the directory structure, ownership rules, and mapping conventions between ORACLE_* documents and automated test suites.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# TEST_SUITE_LAYOUT

**Test Suite Layout and Oracle Mapping Rules (Normative)**

---

## 1. Purpose

This document defines:

* how oracle documents map to test directories,
* how test ownership is determined,
* how regression execution resolves test suites,
* structural constraints on the test tree.

This document is independent of acceptance gates.
Acceptance gates reference this document for execution semantics.

---

## 2. Test Root

All automated tests MUST reside under:

```
tetris/tests/
```

No tests may exist outside this directory.

---

## 3. Oracle Ownership Rule

Each test oracle owns exactly one test directory.

Rules:

* All tests proving an oracle MUST reside in its mapped directory.
* Tests for different oracles MUST NOT be mixed in a single directory.
* Tests MUST NOT exist without an owning oracle document.
* An oracle directory MUST NOT contain tests that assert behavior outside that oracle's scope.

This ensures:

* traceability,
* deterministic test discovery,
* clean regression recursion,
* elimination of "floating tests".

---

## 4. Oracle-to-Test Directory Mapping

### 4.1 Canonical mapping

For any oracle document with:

```
doc_id: ORACLE_<SCOPE>_<TOPIC>
```

the corresponding test directory MUST be:

```
tetris/tests/<scope>_<topic>/
```

Transformation rules:

1. Remove the `ORACLE_` prefix.
2. Convert the remainder to lowercase.
3. Preserve underscores exactly.
4. Do not introduce additional normalization.

### 4.2 Examples

| Oracle ID                | Test Directory                  |
| ------------------------ | ------------------------------- |
| `ORACLE_CORE_COLLISION`  | `tetris/tests/core_collision/`  |
| `ORACLE_CORE_API_TYPES`  | `tetris/tests/core_api_types/`  |
| `ORACLE_CORE_RNG_7BAG`   | `tetris/tests/core_rng_7bag/`   |
| `ORACLE_SHELL_RENDERING` | `tetris/tests/shell_rendering/` |

---

## 5. Directory Structure Constraints

### 5.1 Allowed structure inside an oracle directory

Within:

```
tetris/tests/<oracle_dir>/
```

the following are allowed:

* multiple `test_*.py` files,
* helper modules,
* local fixtures,
* static test data files.

### 5.2 Forbidden structure

The following are prohibited:

* importing tests across oracle directories,
* cross-oracle helper reuse unless placed in a neutral shared helper module under:

```
tetris/tests/_shared/
```

* defining tests outside an oracle directory.

---

## 6. Shared Test Utilities

Shared utilities MUST reside under:

```

tetris/tests/_shared/

```

Rules:

* `_shared/` MUST NOT contain tests.
* `_shared/` may contain:
    * fixture builders,
    * deterministic state constructors,
    * reusable assertions.

This prevents circular oracle coupling.

---

## 7. Determinism Requirement

Unless explicitly allowed by the referenced oracle document:

* Tests MUST be deterministic.
* Randomness MUST be seeded.
* No wall-clock time dependency is allowed.
* No filesystem side effects outside temporary directories are allowed.

---

## 8. Compliance Conditions

The test suite is compliant only if:

* Every oracle document has exactly one corresponding directory.
* No orphan test directories exist.
* No tests exist outside `tetris/tests/`.
* No test directory exists without a corresponding `ORACLE_*` document.

Violation invalidates regression semantics.

---
~~~

~~~
---
doc_id: TEST_ORACLE_FORMAT_CONVENTION
name: TEST_ORACLE_FORMAT_CONVENTION.md
title: Test Oracle Format Convention
status: active
authority: normative
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/699f3373-531c-8388-88fe-1fa9febfbc92
---

# Test Oracle Format Convention

## 1. Purpose

This document defines the **mandatory structural, semantic, and identifier conventions** for all `ORACLE_*` documents.

Its objectives are to ensure that:

* all oracle documents are structurally consistent,
* oracle identifiers are semantically meaningful and stable,
* acceptance gates can reference oracle IDs unambiguously,
* tests remain traceable to normative requirements,
* the taxonomy remains extensible without breaking stability.

This document is **normative** for all oracle documents.

---

## PART I — DOCUMENT STRUCTURE CONVENTION

---

### 2. Document identity and naming

#### 2.1 File naming

* Oracle files MUST be named: `ORACLE_<SCOPE>_<TOPIC>.md`
* The document H1 MUST match the `doc_id` exactly: `# ORACLE_<SCOPE>_<TOPIC>`

Examples:

* `ORACLE_CORE_COLLISION.md`
* `ORACLE_SHELL_RUNTIME.md`

#### 2.2 `doc_id` naming

* `doc_id` MUST use uppercase snake case.
* `doc_id` MUST start with `ORACLE_`.
* `doc_id` MUST match the filename (minus `.md`).

---

### 3. Required YAML front matter

Every oracle document MUST begin with YAML front matter delimited by `---` lines.

#### 3.1 Required fields

Each oracle MUST include **all** of:

* `doc_id` (see §2.2)
* `name` (the filename)
* `title` (human title)
* `status` (`draft` | `active` at minimum)
* `authority` (typically `normative` for oracles)
* `description` (1–2 sentence summary; MUST be specific)
* `references` (list of doc IDs this oracle binds to)

#### 3.2 `references` requirements

* `references` MUST be a YAML list (inline list allowed).
* `references` MUST contain the *primary spec(s)* being mapped.
* `references` MAY include other oracles if there is a strict dependency.

---

### 4. Mandatory top-of-body structure

After YAML front matter, each oracle MUST have:

1. H1: `# <doc_id>`
2. A bold "identity line" (a single bold paragraph) describing layer/topic and ending with `(Normative)`.
3. A "Purpose" section describing what the oracles cover.
4. A "Harness assumptions" section describing what tests must be able to do.
5. The oracle set itself (the numbered oracle items).
6. A "Minimum required set" section mapping to gates or MVP.
7. Optional sections:
    * "Forbidden behavior"
    * "Design note (non-normative)"
    * "Notes for implementers (non-normative)"

#### 4.1 Heading levels

* Major sections MUST be `##`.
* Oracle items MUST be `### ORACLE <ID>: <Title>`.

---

### 5. Oracle item conventions

#### 5.1 Oracle item header format

Every oracle item MUST follow:

`### ORACLE <ORACLE_ID>: <Short title>`

* `<ORACLE_ID>` MUST be unique within the document.
* `<ORACLE_ID>` SHOULD be short and stable.
* `<ORACLE_ID>` MUST be referenced verbatim in "Minimum required set".

Observed ID styles you used (all allowed by this convention):

* Simple numeric within a theme: `GO1`, `GL6`, `G3`
* Themed groups: `B1`, `M2`, `R3`
* Suffix qualifiers: `X2-C`, `R2-C`

#### 5.2 Oracle item content shape (normative)

Each oracle item SHOULD be written in this sequence (when applicable):

1. **Setup / Given**: how to construct the state or inputs.
2. **Action / When**: the call under test (`step(...)`, `render(...)`, CLI invocation, loader call, etc.).
3. **Assertions / Then**: explicit bullet list of required assertions.
4. **Notes** (optional): clarifies intent or scope boundaries.

#### 5.3 Normative strength keywords

To reduce ambiguity:

* Use **MUST** / **MUST NOT** for requirements.
* Use **SHOULD** for strong recommendations.
* Use **MAY** for optional behaviors.

If an oracle item is optional, it MUST be labeled as optional in its text (or placed into an explicit "Optional" subsection).

#### 5.4 Determinism requirement (cross-cutting)

If the layer is intended to be deterministic (core, replay, scripted runtime, rendering snapshots):

* Oracle docs MUST explicitly require determinism where relevant.
* Oracle items MUST avoid randomized setups unless the RNG is explicitly seeded and asserted.

---

### 6. Harness assumptions section requirements

The "Harness assumptions" section MUST list capabilities the test suite must have, in bullets.

It MUST be specific to the layer, e.g.:

* core: construct `GameState`, call `step(...)`, compare state fields,
* rendering: call `render(state) -> str` and compare byte-for-byte,
* CLI: run `python -m ...` and assert exit code/stdout/stderr,
* replay/runtime: load fixtures, run in-process, count ticks, ensure no wall-clock dependency.

Harness assumptions MUST NOT silently introduce new product requirements (they can require *test capabilities*, not new features beyond referenced specs).

---

### 7. Gate and "minimum required set" convention

Every oracle document MUST include a section:

* `## <N>. Minimum required test set`

This section MUST:

* explicitly list the oracle IDs considered minimal

Examples:

```
## 5. Minimum required test set

- F1, F2, F3, F4, F5, F6
- M1, M2

Additionally, snapshot (golden) tests must exist for at least:

- empty initial state,
- representative mid-game state,
- game-over state.
```

```
## 6. Minimum required test set

- C1, C2, C3
- X1, X2
- P1

Additionally, at least one test must assert exit codes for error cases:

- either X3 or X4 (or both).
```

---

### 8. Prohibitions / forbidden behavior section

If the topic has common failure modes, the oracle doc SHOULD include a "Forbidden behavior" section that lists explicit MUST NOT behaviors.

When present:

* Each forbidden behavior bullet SHOULD be testable (directly or indirectly).
* Forbidden behavior MUST align with referenced specs; do not invent new rules here.

---

### 9. Cross-document boundary rule

Oracle docs MUST be narrow and avoid coupling:

* Pure geometry truth belongs in geometry oracles.
* Collision policy belongs in collision oracles.
* Gravity/locking sequencing belongs in gravity/locking oracles.
* Shell concerns (CLI/runtime/replay/rendering/config) MUST NOT leak into core oracles.

If an oracle depends on another oracle’s correctness, it MUST reference it in `references` and the dependency should be described briefly (one sentence) near the relevant oracle item(s).

---

### 10. Non-normative blocks

Non-normative guidance is allowed but MUST be clearly labeled as **non-normative**, e.g.:

* `### Notes for implementers and test authors (non-normative)`
* `## Design note (non-normative)`

Non-normative sections MUST NOT contain new MUST/MUST NOT requirements.

---

### 11. Canonical template

Use this template for new oracle docs (fill in fields; keep structure intact):

```markdown
---
doc_id: ORACLE_<SCOPE>_<TOPIC>
name: ORACLE_<SCOPE>_<TOPIC>.md
title: <Human Title>
status: active
authority: normative
description: <1–2 sentence specific description of what this oracle enforces.>
references:
  - <SPEC_DOC_ID_1>
  - <SPEC_DOC_ID_2>
  - <API_DOC_ID_IF_ANY>
  - <RELATED_ORACLE_DOC_ID_IF_DEPENDENT>
---

# ORACLE_<SCOPE>_<TOPIC>

**<Layer> — <Topic> Test Oracles (Normative)**

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* <bullet>
* <bullet>
* <bullet>

It applies to: <layer / module scope>.
It is normative for: <gate number(s) or range>.

## 2. Harness assumptions

The test harness must be able to:

* <capability>
* <capability>
* <capability>

Tests should use deterministic setups (seeded where applicable).

## 3. Oracle set

### ORACLE <ID1>: <Title>

Construct/Given:
* ...

Action/When:
* ...

Assert/Then:
* ...
* ...
* ...

### ORACLE <ID2>: <Title>

...

## 4. Forbidden behavior

The following are prohibited:

* <must-not behavior>
* <must-not behavior>

## 5. Minimum required test set

* <IDX1>, <IDX2>, <IDX3>
* <IDY1>, <IDY2>

### Notes for implementers and test authors (non-normative)

* <guidance>
* <guidance>
```

---

## PART II — ORACLE IDENTIFIER TAXONOMY

---

### 12. Purpose of Oracle Identifiers

Oracle identifiers are:

* stable normative handles,
* referenced by acceptance gates,
* mapped to automated tests,
* semantic indicators of the behavior under test.

Oracle IDs are part of the project’s normative contract.

---

### 13. Canonical Oracle ID Structure

Oracle IDs MUST follow:

```
<PREFIX><NUMBER>[ -<SUFFIX> ]
```

Where:

* `<PREFIX>` — behavioral category code (uppercase)
* `<NUMBER>` — stable ordinal (1–99 recommended)
* `<SUFFIX>` — optional uppercase qualifier

Examples:

* `GO1`
* `GL10`
* `R2-C`
* `CFG3-S`

---

### 14. Prefix Definition Rules (Generalized)

#### 14.1 Prefix meaning

A prefix represents a **behavioral category**, not:

* an implementation detail,
* a data structure,
* a programming language,
* a gate number.

Prefixes MUST describe *what property is being verified*.

---

#### 14.2 Prefix scope

Prefixes may represent:

* domain behaviors (gravity, spawn, replay),
* cross-cutting properties (determinism, invariants),
* layer concerns (CLI, runtime, config).

Prefixes MUST remain valid even if implementation changes.

---

#### 14.3 Introducing new prefixes

New prefixes MAY be introduced when:

* a new behavior category emerges,
* semantic ambiguity would otherwise arise.

When introducing a new prefix:

1. It MUST be added to the registry (Section 13).
2. Its semantic scope MUST be defined in one sentence.
3. It MUST NOT overlap meaning with an existing prefix without justification.

The taxonomy is intentionally extensible.

---

### 15. Suffix Definition Rules

#### 15.1 Suffix meaning

Suffixes refine meaning. They represent:

* specialization within a category,
* cross-cutting qualifiers (collision, strictness, determinism),
* structural variants of the same rule type.

Example:

* `R2-C` → rotation rule, collision-focused
* `CFG1-S` → configuration rule, strictness variant

---

#### 15.2 When to use a suffix

A suffix SHOULD be used when:

* the prefix alone is too broad,
* multiple variants of the same behavioral rule exist,
* collision/strictness/determinism semantics are isolated.

Suffixes MUST NOT be used for numbering convenience.

---

#### 15.3 Introducing new suffixes

When introducing a new suffix:

1. It MUST be documented in Section 14.
2. Its meaning MUST be defined once.
3. It SHOULD be reusable across documents.

Suffix proliferation SHOULD be avoided.

---

### 16. Identifier Stability Rules

* Oracle IDs MUST remain stable once referenced by acceptance gates.
* Renaming an ID requires updating all references.
* New IDs MAY be inserted but MUST NOT renumber existing IDs.
* Numbers are local to the document; prefixes provide semantic context.

---

## PART III — CURRENT PREFIX REGISTRY (PROJECT SNAPSHOT)

This registry reflects prefixes currently in use.
It is descriptive, not restrictive.

---

### 17. Core Layer Prefixes

| Prefix | Meaning                                  |
| ------ | ---------------------------------------- |
| G      | Geometry and canonical block enumeration |
| R      | Rotation policy and kick ordering        |
| M      | Movement semantics                       |
| B      | Board invariants and bounds              |
| C      | Collision semantics                      |
| GL     | Gravity and locking                      |
| LC     | Line clear and scoring                   |
| SP     | Spawn and piece queue behavior           |
| HO     | Hold mechanics                           |
| GO     | Game-over behavior                       |

---

### 18. Shell Layer Prefixes

| Prefix | Meaning                             |
| ------ | ----------------------------------- |
| C      | Command availability                |
| X      | Exit codes / negative semantics     |
| P      | Error propagation                   |
| F      | Output format constraints           |
| S      | Snapshot / golden determinism       |
| L      | Loading and schema validation       |
| E      | Execution semantics                 |
| V      | Virtual-time runtime guarantees     |
| B      | Boundary and separation constraints |
| CFG    | Configuration model and resolution  |

---

### 19. Cross-Cutting Prefixes

| Prefix | Meaning                |
| ------ | ---------------------- |
| I      | Structural invariants  |
| D      | Determinism guarantees |
| API    | Public API contract    |

---

### 20. Current Suffix Registry

| Suffix | Meaning                         |
| ------ | ------------------------------- |
| -C     | Collision-focused semantics     |
| -S     | Strictness (no auto-correction) |
| -D     | Determinism refinement          |
| -B     | Boundary/separation qualifier   |

New suffixes MAY be added under §10.3.

---

## PART IV — INTERPRETATION RULE

An Oracle ID MUST be readable as:

> Rule `<NUMBER>` in behavioral category `<PREFIX>`, optionally refined by `<SUFFIX>`.

Examples:

* `GL4` → Gravity/Locking rule 4.
* `GO3` → Game-over rule 3.
* `R2-C` → Rotation rule 2, collision-focused.
* `CFG3-S` → Configuration rule 3, strictness refinement.

---

## PART V — COMPLIANCE

An oracle document is compliant with this convention only if:

* its structure matches Part I,
* its identifiers conform to Part II,
* its minimum required set references oracle IDs verbatim,
* no identifier is reused ambiguously within the document.

Failure to comply invalidates the oracle as a normative artifact.

---
~~~

~~~

# Software Development Harness

## Synopsis

The project documentation base MUST be alias-invariant and semantically self-contained. Domain-loaded terms are treated as arbitrary labels and may be mechanically replaced without loss of meaning. All behavior must be derived exclusively from explicit normative specification and validated by corresponding test oracles. No implementation agent may rely on cultural knowledge of the domain.

## 1. Purpose

This document defines requirements for constructing a **domain-neutral software development harness**.

The harness formalizes a documentation-first development paradigm in which human developers operate as specification engineers. The primary artifact of development is a rigorously structured, normative documentation corpus written in technical natural language.

This documentation corpus MUST be sufficient to:

- drive context construction for implementation agents,
- enable stepwise generation of source code and test suites,
- support iterative refinement under formal acceptance gates,
- allow full system implementation from an empty repository.

Implementation agents (human or automated) MUST be able to construct the system using **only explicit specifications**, without reliance on:

- prior domain knowledge,
- cultural familiarity,
- historical conventions,
- latent model semantics,
- undocumented assumptions.

The documentation corpus MUST therefore be:

- self-contained,
- behaviorally complete,
- formally structured,
- alias-invariant,
- verifiable via explicit test oracles.

---

## 2. Core Objective: Alias-Invariance

The project documentation set MUST fully specify behavior such that all domain-loaded identifiers (e.g., `tetris`, `tetromino`, `line`, `bag`, `rotation`) can be mechanically replaced with semantically neutral aliases (e.g., `system`/`app`/`application`/`program`/`package`, `unit`/`piece`/`element`/`figure`/`shape`, `full_row`, `permutation_pool`, `orientation`) without changing:

- implementability,
- correctness,
- testability.

An implementation agent MUST be able to rely exclusively on explicit contracts and MUST NOT require prior knowledge of the cultural concept and prior art traditionally associated with the domain terms.

Importantly, any domain knowledge available to AI systems can and absolutely should be used when developing project documentation interactively. The important part is to formalize any such implicit knowledge explicitly in specifications in the course of documentation development. At early stages, it might be often wise to exploit the models domain knowledge to full extent and only later worry about evolving documentation base, ensuring explicit encoding of implicit knowledge.

---

## 3. Semantically Neutral Aliases - Definition

A term qualifies as a **semantically neutral alias** if it:

- carries no embedded game or cultural meaning beyond being an arbitrary label,
- introduces no behavioral implications through metaphor,
- is defined exclusively through formal specification.
* is consistently applied across:
    * prose
    * code identifiers (public API + internal names where referenced)
    * diagrams/tables
    * test names and oracle phrasing

Examples of acceptable neutral terms:

- `unit`
- `entity_a`
- `orientation_index`
- `state_delta`
- `permutation_pool`

Examples of prohibited metaphor-bearing terms in normative layers:

- `fall`
- `gravity`
- `stack`
- `clear`
- `well`
- `bag`
- `hold`
- `block`
- `row-clear`

---

## 4. Acceptance Criteria

### A. Mechanical Rename Invariance

A deterministic mechanical rename pass over a defined vocabulary set MUST produce a documentation corpus that remains:

- internally consistent,
- cross-reference complete,
* fully implementable (no missing semantics),
* fully testable (oracles still executable/meaningful).

The rename operation MUST require no semantic interpretation — simple search-and-replace must suffice.

---

### B. Zero Implicit-Domain Dependency

No requirement may depend on “common knowledge” of the domain. Any behavior that might be inferred from domain terminology MUST be explicitly specified.

This includes, but is not limited to:

- shape definitions
- orientation rules
- spawning rules
- movement rules
- collision detection
- row completion detection
- scoring rules (if applicable)
- termination conditions

If a behavior cannot be derived directly from explicit specification, the documentation is non-compliant.

---

### C. Explicit Concept Grounding

All behaviorally relevant nouns MUST:

1. Have a formal definition in the normative glossary.
2. Reference an authoritative specification section defining its operational meaning.
3. Be linked to at least one corresponding oracle or gate if correctness-critical.

No concept may exist implicitly.

---

### D. Vocabulary Quarantine

Domain-loaded terms MUST be treated as *presentation-layer labels* only:

- MAY appear in informative or presentation contexts.
- MUST NOT define or imply normative behavior.
- MUST be replaceable without loss of meaning.

Normative specifications MUST use canonical neutral terminology.

---

## 5. Documentation Architecture Requirements

### 5.1 Two-Layer Terminology Pattern

The documentation MUST adopt a two-layer structure:

#### Normative Layer

Uses canonical, semantically-neutral terms exclusively:
- `unit`
- `orientation`
- `grid`
- `occupancy_state`
- `spawn_rule`

#### Informative Alias Layer

Provides a mapping between domain-loaded and canonical terms, e.g.:

* `tetromino` ↔ `unit`
* `tetris` ↔ `system` / `game`
* `line` ↔ `full_row`
* etc.

The mapping MUST be defined in `ALIAS_MAP.yaml`. Normative rules MUST remain valid if domain terms are removed entirely.

---

### 5.2 No-Metaphor Rule

Normative prose MUST describe:

- state transitions,
- invariants,
- preconditions,
- postconditions,
- rejection semantics.

It MUST NOT describe behavior through metaphorical language.

Correct:  
> On each step, apply translation vector (0, +1) unless blocked by occupancy or boundary constraint.

Incorrect:  
> The piece falls due to gravity until it lands.

---

### 5.3 Oracle Alias-Proofing

Test oracles MUST:

- reference canonical terms only,
- define expected state transitions precisely,
- avoid metaphor,
- remain valid under mechanical renaming.

If renaming breaks oracle clarity, the oracle is non-compliant.

---

## 6. Alias-Invariance Gate

### GX.Y — Alias-Invariance Check

#### Objective

Prove that the documentation base is semantically independent of domain terminology.

#### Mandatory Criteria

1. `ALIAS_MAP.yaml` exists and is normative.
2. All canonical terms exist in `GLOSSARY_NORMATIVE.md`.
3. Normative specifications use canonical terminology.
4. Domain-loaded terms do not define behavior.
5. Mechanical rename produces a consistent documentation corpus.
6. All referenced oracles remain interpretable after renaming.

#### Evidence Artifacts

- `ALIAS_MAP.yaml`
- `ALIAS_MAP.md`
- Renamed documentation under `docs/_derived/alias_invariant/`
- Rename validation report
- Confirmation that all referenced oracles remain valid

#### Failure Conditions

The gate fails if:

- Any behavior relies on implicit domain knowledge.
- Any canonical term lacks formal definition.
- Mechanical renaming breaks references.
- Any oracle becomes ambiguous after renaming.

---

## 7. Harness-Level Guarantees

If this document is satisfied:

- The documentation corpus functions as a **generic behavioral specification engine**.
- The project can serve as a reusable AI-agent training harness.
- The system can be implemented under arbitrary naming schemes.
- No semantic leakage from historical domain context is required.

---
~~~