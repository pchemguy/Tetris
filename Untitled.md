
````md
---
doc_id: DOC_INVENTORY
name: DOC_INVENTORY.md
title: Machine-Readable Documentation Inventory Specification
kind: meta
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines the canonical machine-readable documentation inventory format (DOC_INVENTORY.json) used for discovery, validation inputs, and downstream tooling.
references:
  - DOC_SCHEMA
  - COMPONENT_REGISTRY
  - YAML_REFERENCE_POLICY
---

# Machine-Readable Documentation Inventory Specification (Normative)

## 1. Purpose

This document defines the **canonical machine-readable documentation inventory** used for:

- deterministic **project discovery** (Gate 0, agent workflows),
- stable inputs to documentation tooling,
- validation reporting (schema + reference diagnostics),
- downstream derivatives (e.g., rendered graphs, reports).

This spec defines the format of:

- `DOC_INVENTORY.json` (required output artifact)

This spec does **not** define graph rendering. Rendering is specified in `@DOC_GRAPH_SPEC`.

---

## 2. Canonical artifact

Tooling MUST be able to produce:

- **`docs/meta/DOC_INVENTORY.json`**

Filename is **normative**. Directory is conventional.

`DOC_INVENTORY.json` MUST be valid JSON and MUST conform to:

- `DOC_INVENTORY.schema.json` (schema file colocated under `docs/meta/` by convention)

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
  "version": 1,
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
* `version` MUST be an integer; current version is `1`.
* `generated_at` is informational only.
* `repo.*` is informational only and MUST NOT be used as authoritative identity.

### 4.2 Document entry shape

Each element in `docs[]` MUST include:

```json
{
  "doc_id": "DOC_SCHEMA",
  "name": "DOC_SCHEMA.md",
  "path": "docs/meta/DOC_SCHEMA.md",
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
* `layer` is **computed** from `kind` using the canonical mapping in `@DOC_GRAPH_SPEC`.
* `path` is derived from filesystem location at generation time.

### 4.3 Optional fields

A document entry MAY include:

* `description` (string)
* `url` (string, URI)
* `urls` (array of string URIs)
* `references` (array of DOC_ID strings)
* `supersedes` (array of DOC_ID strings)
* `superseded_by` (DOC_ID string)

Normative omission rules (your “present or absent” policy):

1. `references`, `supersedes` MUST be **omitted** if empty.
2. `superseded_by` MUST be **omitted** if not applicable.
3. `url` MUST be **omitted** if not present; it MUST NOT be `null` or empty.
4. `urls` MUST be **omitted** unless present and non-empty.
5. A doc MUST NOT contain both `url` and `urls`.

---

## 5. Determinism rules (normative)

To ensure stable diffs and stable agent behavior:

* `docs[]` MUST be sorted by `doc_id` ascending (lexicographic).
* Within each doc entry, arrays (if present) MUST be sorted ascending:

  * `references`, `supersedes`, `urls`
* Tools MUST NOT emit duplicates in:

  * `docs[]`
  * any array field

---

## 6. Relationship to validation

Inventory generation MUST perform:

* YAML parsing and schema validation against `DOC_SCHEMA.json`,
* dependency validation for YAML `references`,
* optional diagnostics using `@YAML_REFERENCE_POLICY`.

Validation outputs MAY be written separately (e.g., a report JSON), but the inventory MUST remain constructible even if diagnostics produce warnings.

Hard failures that MUST prevent emitting an inventory:

* duplicate `doc_id`,
* YAML schema invalid,
* required docs missing YAML (per Gate 0 policy),
* YAML `references` target missing from inventory,
* normative doc cannot be classified to L0–L5.

Warnings that MUST NOT block:

* prose mention targets missing (`@DOC_ID`),
* cross-layer reference policy violations per `@YAML_REFERENCE_POLICY`.

---

## 7. Scope

`DOC_INVENTORY.json` is a canonical representation of documentation metadata and discovery state.

It is intentionally **not** a rendered graph and intentionally does not encode layout.
Graph rendering and visualization outputs are specified in `@DOC_GRAPH_SPEC`.

````

---

## 2) Patch: `DOC_GRAPH_SPEC.md` (remove §6, reference DOC_INVENTORY)

Here’s the minimal rewrite you asked for: **delete the entire `## 6. Machine-readable documentation inventory (required)` block** and replace it with this short section.

### A) Update YAML header

Add `DOC_INVENTORY` to references:

```yaml
references:
  - DOC_SCHEMA
  - COMPONENT_REGISTRY
  - DOC_INVENTORY
````

(If you’re using `YAML_REFERENCE_POLICY` in §4.3 already, it’s fine to add it too; but you didn’t have it in the header yet. Optional.)

### B) Replace old `## 6...` section with:

```md
## 6. Machine-readable documentation inventory

The canonical machine-readable discovery artifact for the documentation system is defined in `@DOC_INVENTORY`.

Tooling conforming to this spec MUST:

- consume `DOC_INVENTORY.json` as the authoritative inventory of participating documents and their metadata, and
- derive all downstream graph renderings and diagnostics from that inventory.

This spec (`DOC_GRAPH_SPEC`) defines how inventory content is interpreted for:

- layer computation from `kind`,
- edge extraction semantics (`references` vs `mentions`),
- rendering directives for visual graph outputs.

`DOC_GRAPH_SPEC` does not redefine the inventory format.
```

That’s it. You’ve now cleanly separated:

* inventory **format + discovery role** (`DOC_INVENTORY.md`)
* graph **interpretation + visualization semantics** (`DOC_GRAPH_SPEC.md`)

---

If you want, next step (when you say so): define `DOC_INVENTORY.schema.json` (tight, “present-or-absent” compliant), and then we can revisit `DOC_GRAPH_SPEC` to specify the **derivative** artifact you hinted at (`DOC_GRAPH.json`) without conflating it with discovery.
