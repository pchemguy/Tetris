---
doc_id: DOC_GRAPH_SPEC
name: DOC_GRAPH_SPEC.md
doc_title: Documentation Graph Visualization Specification
doc_kind: map
doc_scope: global
doc_status: active
doc_authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines how to extract and render a documentation dependency graph from DOC_SCHEMA YAML metadata and @DOC_ID references.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
supersedes: []
superseded_by:
references:
  - DOC_SCHEMA
  - COMPONENT_REGISTRY
---

# Documentation Graph Visualization Specification (Normative)

> [!NOTE]
> 
> `Generate a Doc Graph visualization spec of DOC_SCHEMA`

## 1. Purpose

This specification defines a deterministic procedure to:

1. **extract** a documentation graph from repository Markdown docs that conform to @DOC_SCHEMA, and
2. **render** that graph into one or more concrete outputs (e.g., Mermaid, DOT).

The resulting graph is used for:

- Gate 0 auditing (missing docs, unknown references),
- human navigation of the documentation system,
- drift detection (changed dependencies, unexpected coupling).

---

## 2. Inputs and authoritative sources

### 2.1 Repository inputs

- Markdown documents participating in the doc system (YAML front matter must validate against `DOC_SCHEMA.json`).
- `COMPONENT_REGISTRY.json` (for validating `doc_scope` and for grouping/legend).

### 2.2 Authority rules

- YAML metadata is authoritative.
- `@DOC_ID` tokens in prose are **convenience-only** and are always treated as **secondary** edges.

---

## 3. Graph model

### 3.1 Node identity

Each node corresponds to **exactly one** document.

- Node ID: `doc_id` (YAML `doc_id`)
- Node label: `doc_title` (YAML `doc_title`)
- Additional node attributes:
    - `name`
    - `doc_kind`
    - `doc_scope`
    - `doc_status`
    - `doc_authority`
    - `gate_applies_to`
    - `phase_applies_to`

A doc without valid YAML metadata MUST NOT appear as a node and MUST be reported as an error (see §7).

### 3.2 Edge types

Two edge types exist:

1. **Normative dependency edge** (authoritative)
    - Source: YAML `references: [...]`
    - Semantics: “This doc depends on the referenced doc(s) for normative meaning.”
2. **Prose mention edge** (non-authoritative)
    - Source: body text tokens matching `@DOC_ID`
    - Semantics: “This doc mentions the referenced doc in prose; may indicate informal coupling.”

### 3.3 Edge direction

Edges point from **referrer → referenced**.

- If `A.references` contains `B`, render `A → B`.
- If prose in `A` mentions `@B`, render `A → B` as prose-mention type.

### 3.4 Edge precedence and de-duplication

If both sources produce an edge `A → B`:

- Render a **single** edge `A → B` with type = **normative**.
- Prose mention is discarded as redundant.

Multiple identical edges MUST NOT be duplicated.

---

## 4. Extraction rules (deterministic)

### 4.1 YAML extraction

For each Markdown file:

1. Detect YAML front matter at top-of-file delimited by:
    - starting `---` on line 1
    - ending `---` on a later line
2. Parse YAML.
3. Validate YAML against `DOC_SCHEMA.json`.
4. Register node keyed by `doc_id`.

### 4.2 Normative edges extraction

For each node `A`:

- For each `doc_id` `B` in `A.references`:
    - Add edge `A → B` of type = normative.

### 4.3 Prose `@DOC_ID` extraction (secondary edges)

For each document body:

- Scan for `@DOC_ID` tokens under these constraints:

#### 4.3.1 Exclude fenced code blocks

- Any content within Markdown fenced code blocks MUST be ignored.
    - A fenced code block begins with a line starting with triple backticks ``` or triple tildes ~~~
    - It ends at the next matching fence of the same marker.
- `@DOC_ID` tokens inside fenced code blocks are treated as examples and ignored.

#### 4.3.2 Token pattern

A prose reference token matches:

- `@` followed by `DOC_ID` lexical format from @DOC_SCHEMA:
    - `@` + `[A-Z][0-9A-Z_]*`

Extract only the DOC_ID portion (without `@`).

#### 4.3.3 Whitespace and formatting

Tooling MUST treat `@DOC_ID` as valid even when surrounded by punctuation or Markdown emphasis, e.g.:

- `(@DOC_ID)`
- `"@DOC_ID"`
- `*@DOC_ID*`
- `` `@DOC_ID` ``

#### 4.3.4 Emission rule

For each extracted `@B` in doc `A`:

- If `B` exists as a known YAML `doc_id`, add edge `A → B` type=prose.
- If `B` is unknown, report as a warning or error based on strictness (see §7).

---

## 5. Required outputs

Tooling MUST be able to render at least these outputs:

### 5.1 Mermaid graph (required)

Output: `docs/reports/DOC_GRAPH.mmd` (path may differ; use your docs layout policy)

- Format: `flowchart LR` (or `TD`, but must be consistent)
- Nodes must display:
    - `doc_id` and `doc_title` (minimum)
- Edges:
    - normative edges: solid arrow
    - prose edges: dashed arrow

Example (illustrative):

```mermaid
flowchart LR
  DOC_SCHEMA["DOC_SCHEMA<br/>Documentation Metadata Schema"]
  COMPONENT_REGISTRY["COMPONENT_REGISTRY<br/>Component Registry"]
  DOC_GRAPH_SPEC["DOC_GRAPH_SPEC<br/>Documentation Graph Visualization Spec"]

  DOC_GRAPH_SPEC --> DOC_SCHEMA
  DOC_GRAPH_SPEC --> COMPONENT_REGISTRY
  DOC_SCHEMA -.-> COMPONENT_REGISTRY
````

### 5.2 DOT graph (optional but recommended)

Output: `docs/reports/DOC_GRAPH.dot`

* Must encode edge type via style:
    * normative: solid
    * prose: dashed

---

## 6. Visualization rules

### 6.1 Grouping (subgraphs / swimlanes)

Renderers SHOULD group nodes by `doc_scope`:

* `global`, `core`, `shell`, `testing`,
* and component-specific tokens like `shell:runtime` if present.

If grouping is not supported by the output format, grouping may be omitted, but node labels MUST still include `doc_scope` in an inspectable way (tooltip/label suffix).

### 6.2 Styling and legend (required)

Graph output MUST include a legend indicating:

* solid edges = YAML `references` (normative)
* dashed edges = prose `@DOC_ID` mentions (non-authoritative)

Optional node styling by `doc_kind`:

* `control`: distinct shape/class
* `spec`, `oracle`, `api`, `map`, `report`, `idea`: distinct classes

(Exact colors/shapes are output-format-specific; the rule is that kinds must be distinguishable.)

### 6.3 Filtering modes (required)

Tooling MUST support generating filtered graphs:

1. **Normative-only**
    * Only YAML `references` edges.
2. **Full**
    * YAML `references` edges + prose edges.

Optional filters:

* by `doc_authority` (normative only),
* by `doc_scope` (e.g., only `shell:*` docs),
* by gate/phase applicability ranges.

---

## 7. Validation and failure behavior

### 7.1 Hard failures (must BLOCK in strict mode)

Any of the following MUST be treated as a hard failure:

* Duplicate `doc_id`
* YAML metadata missing from a doc that is required to participate (policy: “all docs under docs/ except docs/ideas/”)
* YAML fails schema validation
* YAML `references` contains a DOC_ID that does not exist in YAML inventory

### 7.2 Soft failures (warnings)

* Prose `@DOC_ID` references to unknown DOC_IDs MAY be warnings (recommended),
  since prose is non-authoritative.
* Tooling SHOULD still report them in a “dangling mentions” section.

### 7.3 Output report (required)

Tooling MUST emit a report summary including:

* total nodes
* total normative edges
* total prose edges
* list of unknown YAML references (if any)
* list of dangling prose mentions (if any)
* list of docs missing YAML (if any)

---

## 8. Performance and determinism constraints

* The graph extraction MUST be deterministic given the repo state.
* File iteration order MUST NOT affect output:
    * tools must sort node IDs and edges before emitting.

---

## 9. Non-goals

This spec does not:

* define how docs are written (see @DOC_SCHEMA),
* define acceptance gates or phases (see @ACCEPTANCE_GATES and @PHASES),
* define runtime import boundaries (see @DECOMPOSITION / registry policy).

It only defines the doc graph extraction and visualization behavior.
