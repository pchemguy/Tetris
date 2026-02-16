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
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - DOC_SCHEMA
  - DOC_LAYERS
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

## 2. Canonical artifact

Tooling MUST be able to produce:

- **`docs/meta/DOC_INVENTORY.json`**

Filename is **normative**. Directory is conventional.

`DOC_INVENTORY.json` MUST be valid JSON and MUST conform to:

- `DOC_INVENTORY.schema.json` (schema file collocated under `docs/meta/` by convention)

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
* `layer` is **computed** from `kind` using the canonical mapping in `DOC_LAYERS.md`.
- `path`
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
