---
doc_id: DOC_GRAPH_SPEC
name: DOC_GRAPH_SPEC.md
title: Documentation Graph Visualization Specification
status: active
authority: normative
description: Defines how to extract and render a documentation dependency graph from DOC_SCHEMA YAML metadata and @DOC_ID references.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [DOC_SCHEMA, DOC_INVENTORY, CROSS_LAYER_DEPENDENCY, DOCUMENTATION_SYSTEM]
---

# Documentation Graph Visualization Specification (Normative)

## 1. Purpose

This spec defines the **canonical documentation graph model** used to render and validate the repository’s documentation system and a deterministic procedure to produce one or more concrete outputs (e.g., Mermaid, DOT).

It exists to ensure tooling can:

* classify documents into conceptual layers **L0–L5** deterministically,
* validate cross-document dependencies,
* enforce structural consistency of the documentation system,
* render a stable and reproducible visualization of documentation relationships.

This spec does **not** define document content. It defines how documents are **modeled, classified, and connected**.

---

## 2. Graph primitives

### 2.1 Node types

Tooling MUST represent the documentation system using the following node types.

#### A) `doc` node

Represents a single Markdown or JSON artifact that participates in the documentation system.

**Identity**

* Node key: `doc_id`

**Required attributes**

* `doc_id` (string; unique)
* `name` (filename; string)
* `kind` (enum; from `DOC_SCHEMA.md` and `DOC_SCHEMA.json`)
* `authority` (`normative` | `non_normative`)
* `status` (`draft` | `active` | `deprecated`)
* `scope` (enum token from `DOC_SCHEMA.md` and `DOC_SCHEMA.json`)
* `layer` (enum; **computed**, not authored; see §3)

**Optional attributes**

* `description`
* `url` OR `urls`

There is no separate `layer` node type. Layer is a derived classification attribute.

---

#### B) `repository` node

A single root node used to anchor layout.

**Identity**

* Node key: fixed `REPOSITORY`

Exactly one `repository` node MUST exist in rendered output.

---

### 2.2 Edge types

Tooling MUST use only the following directed edge types.

#### A) `references`

Represents an explicit document dependency.

* `doc` → `doc`
* Derived from YAML `references: [...]`
* Type = `normative`

#### B) `mentions`

Represents a non-authoritative `@DOC_ID` mention in body text.

* `doc` → `doc`
* Derived from Markdown prose (see §5)
* Type = `prose`

These edges MUST NOT override YAML dependencies.

#### C) `produces` (optional)

Represents generated artifacts or reports.

* `doc` → `doc`

Use only when explicitly modeling generated outputs (e.g., graph reports).

---

### 2.3 Edge direction

Edges always point:

```
referrer → referred
```

If `A.references` includes `B`, render:

```
A → B
```

---

### 2.4 Edge de-duplication

If both:

* YAML `references`
* and `@DOC_ID` prose mention

produce the same edge:

* Emit a **single edge**
* Type = `references`

Prose edges are suppressed when redundant.

Multiple identical edges MUST NOT be emitted.

---

### 2.5 Canonical doc kinds

Graph tooling MUST interpret `kind` using the `DOC_SCHEMA.md` `kind` enum.

---

## 3. Canonical layer mapping (normative)

Layer assignment is derived from `kind` or path using a the mapping table in `DOCUMENTATION_SYSTEM.md`. Therefore, `layer` is a **computed attribute**, not an independent node.

If a normative document cannot be mapped to L0–L5, this is a **Gate 0 failure**.

---

## 4. Structural validation rules

### 4.1 Every normative doc must be classified

For every `doc` where `authority == normative`:

* `layer` MUST be one of L0–L5.
* It MUST NOT be OUT.
* It MUST appear in the graph.

Failure is a hard error.

---

### 4.2 Layer precedence ordering

Layers have strict precedence:

```
L0 > L1 > L2 > L3 > L4 > L5
```

Interpretation:

Higher layers constrain lower layers.

---

### 4.3 Cross-layer reference validation (diagnostic only)

Cross-layer validation of YAML `references` edges is **diagnostic-only** and MUST NOT affect graph construction. The normative policy is defined in `CROSS_LAYER_DEPENDENCY.md`. The authoritative machine-readable policy instance is `YAML_REFERENCE_POLICY.json` (validated by `YAML_REFERENCE_POLICY.schema.json`).

---

## 5. Reference extraction and validation

### 5.1 YAML extraction

For each Markdown file:

1. Detect YAML front matter.
2. Parse YAML.
3. Validate against `DOC_SCHEMA.json`.
4. Register node keyed by `doc_id`.

---

### 5.2 Authoritative references

Extract only from YAML:

```
references: [DOC_ID, ...]
```

For each:

Create:

```
doc_id → referenced_doc_id
type = references
```

If referenced `DOC_ID` does not exist → hard failure.

---

### 5.3 Prose references (`@DOC_ID`)

Tooling MAY extract `@DOC_ID` tokens for linting.

#### Exclusion rule

Ignore fenced code blocks.

#### Token rule

Match:

```
@[A-Z][0-9A-Z_]*
```

Extract the DOC_ID portion.

#### Emission rule

* Create `prose` edges.
* Do NOT treat as authoritative.
* Do NOT override YAML references.

Unknown prose DOC_ID → warning.

---

### 5.4 Determinism requirements

* Node and edge lists MUST be sorted before output.
* File iteration order MUST NOT affect output.
* Graph generation MUST be deterministic.

---

## 6. Machine-readable documentation inventory

The canonical machine-readable discovery artifact for the documentation system is defined in `DOC_INVENTORY.md`.

Tooling conforming to this spec MUST:

- consume `DOC_INVENTORY.json` as the authoritative inventory of participating documents and their metadata, and
- derive all downstream graph renderings and diagnostics from that inventory.

This spec (`DOC_GRAPH_SPEC.md`) defines how inventory content is interpreted for:

- layer computation from `kind`,
- edge extraction semantics (`references` vs `mentions`),
- rendering directives for visual graph outputs.

`DOC_GRAPH_SPEC.md` does not redefine the inventory format.

---

## 7. Rendering directives (deterministic layout)

### 7.1 Vertical ordering

Renderers MUST group documents by computed `layer` in vertical order:

```
REPOSITORY
L0
L1
L2
L3
L4
L5
```

This grouping is layout-only; no explicit layer nodes are required.

---

### 7.2 Layer grouping

In Mermaid:

Use `subgraph` blocks for each layer.

Example:

```mermaid
flowchart TD

  subgraph L0["L0 — Documentation Infrastructure"]
    DOC_SCHEMA
    DOC_GRAPH_SPEC
  end

  subgraph L1["L1 — Governance"]
    PHASES
    ACCEPTANCE_GATES
  end
```

---

### 7.3 Edge styling

* YAML `references` → solid arrow
* Prose references → dashed arrow

A legend MUST be included.

---

## 8. Required outputs

### 8.1 Mermaid (required)

Must include:

* All `doc` nodes
* All normative edges
* Optional prose edges
* Layer grouping
* Legend

---

### 8.2 DOT (optional)

Edges:

* normative → solid
* prose → dashed

---

## 9. Visualization rules

### 9.1 Grouping (subgraphs / swimlanes)

Renderers SHOULD group nodes by `scope`:

* `global`, `core`, `shell`, `testing`,
* and component-specific tokens like `shell:runtime` if present.

If grouping is not supported by the output format, grouping may be omitted, but node labels MUST still include `scope` in an inspectable way (tooltip/label suffix).

### 9.2 Styling and legend (required)

Graph output MUST include a legend indicating:

* solid edges = YAML `references` (normative)
* dashed edges = prose `@DOC_ID` `mentions` (non-authoritative)

Optional node styling by `kind`:

* `control`: distinct shape/class
* `spec`, `testing`, `api`, `report`, `idea`: distinct classes

(Exact colors/shapes are output-format-specific; the rule is that kinds must be distinguishable.)

### 9.3 Filtering modes (required)

Tooling MUST support generating filtered graphs:

1. **Normative-only**
    * Only YAML `references` edges.
2. **Full**
    * YAML `references` edges + `mentions` edges.

Optional filters:

* by `authority` (normative only),
* by `scope` (e.g., only `shell:*` docs),
* by gate/phase applicability ranges.

---

## 10. Validation and failure behavior

### 10.1 Hard failures (must BLOCK in strict mode)

Must BLOCK:

* Duplicate `doc_id`
* Missing YAML in required docs
* YAML schema invalid
* YAML `references` to unknown DOC_ID
* Normative doc not classifiable to L0–L5

### 10.2 Soft failures (warnings)

* Unknown prose `@DOC_ID`
* Cross-layer policy violation (unless strict mode)

### 10.3 Output report (required)

Tooling MUST emit a report summary including:

* total nodes
* total normative edges
* total prose edges
* list of unknown YAML references (if any)
* list of dangling prose mentions (if any)
* list of docs missing YAML (if any)

---

## 11. Validation Report Format (Normative)

Tooling MUST emit a structured validation report after graph extraction. The report MUST be deterministic and stable under file ordering. Output format MAY be JSON, Markdown, or both. JSON is recommended for CI; Markdown for human review.

---

### 11.1 Required top-level sections

The report MUST contain:

1. **Inventory Summary**
2. **Layer Assignment Summary**
3. **Normative Reference Matrix**
4. **Cross-Layer Diagnostics**
5. **Structural Failures**
6. **Prose Reference Diagnostics**
7. **Determinism Check**

---

### 11.2 Inventory Summary

Must include:

* total documents discovered
* total normative documents
* total non-normative documents
* total YAML `references` edges
* total prose `@DOC_ID` mentions
* total unique `doc_id` values

Example:

```json
{
  "total_docs": 42,
  "normative_docs": 37,
  "non_normative_docs": 5,
  "normative_edges": 81,
  "prose_edges": 23,
  "unique_doc_ids": 42
}
```

---

### 11.3 Layer Assignment Summary

Tooling MUST emit:

* Count of documents per layer (L0–L5, OUT)
* List of normative docs that failed layer mapping (if any)

Example:

```json
{
  "L0": 4,
  "L1": 2,
  "L2": 2,
  "L3": 14,
  "L4": 8,
  "L5": 3,
  "OUT": 9,
  "unclassified_normative_docs": []
}
```

If any normative doc cannot be mapped → **Hard failure**.

---

### 11.4 Normative Reference Matrix

Tooling MUST compute a layer-to-layer matrix for YAML `references`. Matrix entry `[A][B]` = number of edges from layer A → layer B.

Example:

| From \ To | L0 | L1 | L2 | L3 | L4 | L5 |
| --------- | -- | -- | -- | -- | -- | -- |
| L0        | 0  | 2  | 3  | 5  | 1  | 0  |
| L1        | 4  | 0  | 2  | 3  | 1  | 0  |
| L2        | 0  | 0  | 0  | 6  | 0  | 0  |
| L3        | 0  | 0  | 3  | 0  | 0  | 0  |
| L4        | 0  | 0  | 5  | 9  | 0  | 0  |
| L5        | 2  | 1  | 3  | 4  | 2  | 0  |

This table is critical because it reveals:

* illegal upward semantic coupling
* meta leakage into dev layers
* architectural drift over time

This matrix MUST be sorted and deterministic.

---

### 11.5 Cross-Layer Diagnostics

For each YAML `references` edge:

If it violates the recommended semantic policy (§6):

Emit:

```json
{
  "type": "cross_layer_warning",
  "from_doc": "ARCHITECTURE",
  "from_layer": "L2",
  "to_doc": "PHASES",
  "to_layer": "L1",
  "reason": "Architecture should not depend on governance"
}
```

This section MUST list:

* all suspicious edges
* total suspicious edge count

These are **warnings**, not hard failures.

---

### 11.6 Structural Failures (Hard Errors)

The following MUST block in strict mode:

* Duplicate `doc_id`
* Missing YAML in required doc
* YAML schema invalid
* YAML `references` to unknown `doc_id`
* Normative doc without layer assignment

Each error MUST include:

```json
{
  "type": "hard_failure",
  "doc_id": "X",
  "message": "Duplicate doc_id"
}
```

---

### 11.7 Prose Reference Diagnostics

Tooling MUST emit:

* total prose mentions
* list of unknown prose targets
* list of prose-only references (not in YAML)

Example:

```json
{
  "unknown_prose_targets": ["UNKNOWN_DOC"],
  "prose_only_edges": [
    {"from": "ARCHITECTURE", "to": "DECOMPOSITION"}
  ]
}
```

These MUST NOT block.

---

### 11.8 Determinism Check

Tooling MUST ensure:

* Node list sorted lexicographically by `doc_id`
* Edge list sorted `(from_doc, to_doc)`
* Report output stable across runs

Emit:

```json
{
  "deterministic_ordering": true
}
```

If false → treat as tool implementation error.

---

### Why this matters

This gives you:

* a structural audit surface (hard guarantees),
* a semantic drift surface (warnings),
* a measurable architectural health signal (matrix),
* CI-friendly diffability.
* It keeps layering philosophical and normative — while making enforcement mechanical and measurable.

---
