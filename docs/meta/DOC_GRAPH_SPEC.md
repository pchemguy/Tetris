---
doc_id: DOC_GRAPH_SPEC
name: DOC_GRAPH_SPEC.md
title: Documentation Graph Visualization Specification
kind: meta
scope: global
status: active
authority: normative
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

## 1. Purpose

This spec defines the **canonical doc graph model** used to render and validate the repository’s documentation system and a deterministic procedure to render that graph into one or more concrete outputs (e.g., Mermaid, DOT).

It exists to ensure tooling can:

* classify docs into **layers L0–L5** deterministically,
* render the repository-wide **authority/constraint flow** as a stable diagram,
* validate that all docs participate consistently (no “floating” normative docs).

This spec does **not** define doc content; it defines how docs are **represented and connected** as a graph.

---

## 2. Graph primitives

### 2.1 Node types

Tooling MUST represent the documentation system using these node types:

#### A) `doc` node

Represents a single Markdown or JSON artifact that participates in the doc system.

**Identity**

* Node key: `doc_id` (from YAML front matter for `.md`, or from file metadata for `.json` registry artifacts).

**Required attributes**

* `doc_id` (string; unique)
* `name` (filename; string)
* `kind` (enum; see §2.3)
* `authority` (enum: `normative` | `non_normative`)
* `status` (enum: `draft` | `active` | `deprecated`)
* `scope` (enum token from registry / schema)
* `layer` (enum; computed by tooling; see §3)

**Optional attributes**

* `description` (string)
* `url` (string) OR `urls` (array of strings)

##### `doc` node subtypes

1. **Normative dependency edge** (authoritative)
    - Source: YAML `references: [...]`
    - Semantics: “This doc depends on the referenced doc(s) for normative meaning.”
2. **Prose mention edge** (convenience, non-authoritative)
    - Source: body text tokens matching `@DOC_ID`
    - Semantics: “This doc mentions the referenced doc in prose; may indicate informal coupling.”

#### B) `layer` node

Represents one of the conceptual layers **L0–L5**.

**Identity**

* Node key: `layer_id`

**Required attributes**

* `layer_id` (enum: `L0`|`L1`|`L2`|`L3`|`L4`|`L5`)
* `title` (string)
* `description` (string)

#### C) `repository` node

A single root node used to anchor diagram layout.

**Identity**

* Node key: fixed `REPOSITORY`

**Required attributes**

* `title` (string)

> Rendering requirement: exactly one `repository` node MUST exist.

### 2.2 Edge types

Tooling MUST use only these directed edge types:

#### A) `belongs_to_layer`

Connects a `doc` node to its `layer` node.

* `doc` → `layer`
* Exactly one per `doc` that is part of the documentation system.

#### B) `constrains`

Represents **layer-to-layer constraint flow** (your vertical arrows).

* `layer` → `layer`

Allowed pairs are exactly:

* `L0` → `L1`
* `L1` → `L2`
* `L2` → `L3`
* `L3` → `L4`
* `L4` → `L5`

No other `constrains` edges are allowed.

#### C) `references`

Represents **explicit doc-to-doc dependency**.

* `doc` → `doc`
* Derived from YAML front matter `references: [...]` (authoritative)
* Optionally enriched by `@DOC_ID` tokens in prose (non-authoritative convenience; see §5)

#### D) `produces`

Represents generation outputs (reports, graphs, inventories).

* `doc` → `doc` OR `layer` → `doc`

Use cases:

* `DOC_GRAPH_SPEC` produces a generated graph artifact report.
* L0 tooling produces generated inventories.

This edge is optional and should be used only when you have explicit generated artifacts.

### 2.3 Edge direction

Edges point from **referrer → referred**.

- If `A.references` contains `B`, render `A → B`.
- If prose in `A` mentions `@B`, render `A → B` as prose-mention type.

### 2.4 Edge precedence and de-duplication

If both `doc` node subtypes produce an edge `A → B`:

- Render a **single** edge `A → B` with subtype = **normative**.
- Prose mention is discarded as redundant.

Multiple identical edges MUST NOT be duplicated.

### 2.5 Canonical doc kinds (for graph classification)

Graph tooling MUST interpret doc `kind` using the `DOC_SCHEMA` enum.

At minimum, the following kinds must be understood for layer mapping:

* `meta`
* `control`
* `architecture`
* `decomposition`
* `spec`
* `api`
* `oracle`
* `report`
* `idea` (non-normative)

---

## 3. Layer mapping rules (deterministic)

Tooling MUST assign each `doc` node to exactly one layer using the following mapping:

### 3.1 L0 — Documentation Infrastructure (Meta-layer)

A doc belongs to `L0` if **any** of the following holds:

* `kind == meta`, OR
* `doc_id` is one of:
    * `DOC_SCHEMA`
    * `COMPONENT_REGISTRY`
    * `DOC_GRAPH_SPEC`
    * `DOCS_AUTHORITY_MAP`
    * `DOCUMENTATION_SYSTEM` (if used as the narrative umbrella doc)

Also included in L0:

* `*.schema.json` files for these meta artifacts.

### 3.2 L1 — Governance (Process Control)

A doc belongs to `L1` if:

* `kind == control`, AND
* it is not classified as `L0`.

Examples:

* `PHASES`
* `ACCEPTANCE_GATES`

### 3.3 L2 — System Structure (Global Contracts)

A doc belongs to `L2` if:

* `kind in {architecture, decomposition}`

### 3.4 L3 — Behavioral Specifications (Component Contracts)

A doc belongs to `L3` if:

* `kind in {spec, api}`

### 3.5 L4 — Test Oracles (Proof Obligations)

A doc belongs to `L4` if:

* `kind == oracle`

### 3.6 L5 — Execution State (Reports)

A doc belongs to `L5` if:

* `kind == report`, AND
* it is not classified as `L0`.

Examples:

* `IMPLEMENTATION_REPORTS`

---

## 4. Required structure constraints

### 4.1 Layer nodes must exist

The graph MUST contain exactly:

* 1 `repository` node
* 6 `layer` nodes: `L0`…`L5`

### 4.2 Layer constraint chain must exist

The graph MUST contain exactly 5 `constrains` edges forming the chain:

`L0 → L1 → L2 → L3 → L4 → L5`

No additional `constrains` edges are allowed.

### 4.3 Every normative doc must be placed

For every `doc` node where `authority == normative`:

* a `belongs_to_layer` edge MUST exist (exactly one),
* its layer MUST be one of `L0`…`L5`,
* it MUST NOT be unclassified.

If any normative doc cannot be mapped to a layer, this is a **Gate 0 failure**.

---

## 5. Reference extraction and validation

### 5.1 YAML extraction

For each Markdown file:

1. Detect YAML front matter at top-of-file delimited by:
    - starting `---` on line 1
    - ending `---` on a later line
2. Parse YAML.
3. Validate YAML against `DOC_SCHEMA.json`.
4. Register node keyed by `doc_id`.

### 5.1 Authoritative references

Tooling MUST extract authoritative `references` edges only from YAML front matter:

* `references: [DOC_ID, ...]`

For each entry:

* Create a `references` edge from `doc_id` → referenced `DOC_ID` of type = `normative`.

If a referenced `DOC_ID` does not exist in the YAML inventory, tooling MUST flag it.

### 5.2 Convenience references (`@DOC_ID`) — optional enrichment

Tooling MAY additionally extract `@DOC_ID` tokens from Markdown bodies to provide lint hints.

#### 5.2.1 Exclude fenced code blocks

- Any content within Markdown fenced code blocks MUST be ignored.
    - A fenced code block begins with a line starting with three or more backticks or tildes
    - It ends at the next matching fence of the same marker.
- `@DOC_ID` tokens inside fenced code blocks are treated as examples and ignored.

#### 5.2.2 Token pattern

A prose reference token matches:

- `@` followed by `DOC_ID` lexical format from @DOC_SCHEMA:
    - `@` + `[A-Z][0-9A-Z_]*`

Extract only the DOC_ID portion (without `@`).

#### 5.2.3 Whitespace and formatting

Tooling MUST treat `@DOC_ID` as valid even when surrounded by punctuation, single backticks, or Markdown emphasis, e.g.:

- `(@DOC_ID)`
- `"@DOC_ID",`
- `_@DOC_ID_`
- `*@DOC_ID*`
- `` `@DOC_ID` ``

#### 5.2.4 Emission rule

* Treat these as **non-authoritative**:
    * They MUST NOT create `references` edges automatically.
    * They MAY create `produces` edges to a lint report, or be emitted as warnings (use type = `prose`).

If a `@DOC_ID` token is not present in YAML inventory, tooling SHOULD flag it.

### 5.3 Determinism constraints

* The graph extraction MUST be deterministic given the repo state.
* File iteration order MUST NOT affect output:
    * tools must sort node IDs and edges before emitting.

---

## 6. Allowed cross-layer reference policy (recommended, deterministic)

This is a **graph validation rule**, not a prohibition on prose.

Tooling SHOULD enforce:

* `L4` (oracles) may reference `L3` (spec/api), `L2`, `L1`, `L0`.
* `L3` (spec/api) may reference `L2`, `L1`, `L0`.
* `L2` may reference `L1`, `L0`.
* `L1` may reference `L0`.
* `L5` may reference anything (it’s a log/reporting surface).
* `L0` may reference anything.

If violated, tooling SHOULD emit a warning (or error if you choose strict mode).

---

## 7. Rendering directives (deterministic layout)

To reproduce the diagram structure, renderers MUST:

1. Draw the `repository` node at top.
2. Draw layer nodes vertically in order `L0..L5`.
3. Draw `constrains` edges as vertical arrows between consecutive layers.
4. Place `doc` nodes inside (or grouped under) their `layer` node.
5. Optionally draw `references` edges as dotted lines, but they must not affect layer ordering.

---

## 8. Minimal layer node definitions (normative)

Tooling MUST materialize the following layer nodes:

* `L0` — Documentation Infrastructure (Meta-layer)
* `L1` — Governance (Process Control)
* `L2` — System Structure (Global Contracts)
* `L3` — Behavioral Specifications (Component Contracts)
* `L4` — Test Oracles (Proof Obligations)
* `L5` — Execution State (Reports)

---

## 9. Required outputs

Tooling MUST be able to render at least these outputs:

### 9.1 Mermaid graph (required)

Output: `docs/reports/DOC_GRAPH.mmd` (path may differ; use your docs layout policy)

- Format: `flowchart LR` (or `TD`, but must be consistent)
- Nodes must display:
    - `doc_id` and `title` (minimum)
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

### 9.2 DOT graph (optional but recommended)

Output: `docs/reports/DOC_GRAPH.dot`

* Must encode edge type via style:
    * normative: solid
    * prose: dashed

---

## 10. Visualization rules

### 10.1 Grouping (subgraphs / swimlanes)

Renderers SHOULD group nodes by `scope`:

* `global`, `core`, `shell`, `testing`,
* and component-specific tokens like `shell:runtime` if present.

If grouping is not supported by the output format, grouping may be omitted, but node labels MUST still include `scope` in an inspectable way (tooltip/label suffix).

### 10.2 Styling and legend (required)

Graph output MUST include a legend indicating:

* solid edges = YAML `references` (normative)
* dashed edges = prose `@DOC_ID` mentions (non-authoritative)

Optional node styling by `kind`:

* `control`: distinct shape/class
* `spec`, `oracle`, `api`, `map`, `report`, `idea`: distinct classes

(Exact colors/shapes are output-format-specific; the rule is that kinds must be distinguishable.)

### 10.3 Filtering modes (required)

Tooling MUST support generating filtered graphs:

1. **Normative-only**
    * Only YAML `references` edges.
2. **Full**
    * YAML `references` edges + prose edges.

Optional filters:

* by `authority` (normative only),
* by `scope` (e.g., only `shell:*` docs),
* by gate/phase applicability ranges.

---

## 11. Validation and failure behavior

### 11.1 Hard failures (must BLOCK in strict mode)

Any of the following MUST be treated as a hard failure:

* Duplicate `doc_id`
* YAML metadata missing from a doc that is required to participate (policy: “all docs under docs/ except docs/ideas/”)
* YAML fails schema validation
* YAML `references` contains a DOC_ID that does not exist in YAML inventory

### 11.2 Soft failures (warnings)

* Prose `@DOC_ID` references to unknown DOC_IDs MAY be warnings (recommended),
  since prose is non-authoritative.
* Tooling SHOULD still report them in a “dangling mentions” section.

### 11.3 Output report (required)

Tooling MUST emit a report summary including:

* total nodes
* total normative edges
* total prose edges
* list of unknown YAML references (if any)
* list of dangling prose mentions (if any)
* list of docs missing YAML (if any)

---
