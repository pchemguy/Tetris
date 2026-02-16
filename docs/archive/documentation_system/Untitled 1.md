---
doc_id: DOC_SCHEMA
doc_title: Documentation Metadata Schema
doc_kind: map
doc_scope: global
doc_status: active
doc_authority: normative
gate_applies_to: all
phase_applies_to: all
supersedes: []
superseded_by: []
comment: 📄 `docs/meta/DOC_SCHEMA.md`
references: []
---

# Documentation Metadata Schema (DOC_SCHEMA)

## 1. Purpose

This document defines the **mandatory metadata schema** for all normative
Markdown documents in this repository.

The schema exists to:

- uniquely identify documents,
- define authority and lifecycle,
- constrain scope and applicability,
- support deterministic resolution,
- enable automated validation.

This document is **normative**.

All documents under `docs/` (except `docs/ideas/`) MUST conform to this schema.

---

## 2. Required Metadata Block

Every normative document must begin with a YAML front-matter block:

```yaml
---
doc_id: <string>
doc_title: <string>
doc_kind: <enum>
doc_scope: <enum>
doc_status: <enum>
doc_authority: <enum>
gate_applies_to: <string>
phase_applies_to: <string>
supersedes: [<doc_id>, ...]
superseded_by: <doc_id|null>
references: [<doc_id>, ...]
---
```

No text may precede the front matter.

---

## 3. Field Definitions

### 3.1 `doc_id`

* Unique string identifier.
* Must be uppercase, underscore-separated.
* Must be globally unique across repository.
* Must not change after publication.

Example:

```
CORE_API
ACCEPTANCE_GATES
RENDERING_TEST_ORACLE
```

---

### 3.2 `doc_title`

Human-readable title.

---

### 3.3 `doc_kind`

One of:

* `control`
* `architecture`
* `decomposition`
* `spec`
* `oracle`
* `api`
* `map`
* `report`
* `idea`

---

### 3.4 `doc_scope`

Defines conceptual scope:

* `global`
* `core`
* `shell`
* `component:<name>`

Examples:

```
core
shell
component:renderer
component:runtime
```

---

### 3.5 `doc_status`

Lifecycle state:

* `draft`
* `active`
* `deprecated`

---

### 3.6 `doc_authority`

Defines normative force:

* `normative`
* `non_normative`

Rules:

* Only `normative` documents may define requirements.
* `idea` documents must be `non_normative`.

---

### 3.7 `gate_applies_to`

Defines acceptance gate applicability.

Allowed formats:

* `"all"`
* `"none"`
* `"0"`
* `"1-6"`
* `"10"`
* `"10-13"`

Must match a valid gate or gate range.

---

### 3.8 `phase_applies_to`

Defines repository phase applicability.

Allowed formats:

* `"all"`
* `"none"`
* `"0"`
* `"1"`
* `"2-5"`

Must match a valid phase or range.

---

### 3.9 `supersedes`

List of `doc_id`s this document replaces.

---

### 3.10 `superseded_by`

Single `doc_id` that replaces this one, or `null`.

---

### 3.11 `references`

List of `doc_id`s this document depends on.

References are semantic, not structural.

---

## 4. Validation Rules

A document is invalid if:

* required fields are missing,
* enum values are invalid,
* `doc_id` duplicates another document,
* supersession cycles exist,
* `idea` documents declare `normative` authority.

---

## 5. Authority Precedence (summary)

If conflicts arise:

1. `DOC_SCHEMA` governs metadata interpretation.
2. `ACCEPTANCE_GATES` governs correctness.
3. `PHASES` governs scope timing.
4. `spec` and `api` documents govern behavior.
5. `oracle` documents govern proof.
6. `report` documents record state.

---

## 6. Enforcement

Automated validation should use `DOC_SCHEMA.json`.

Manual review must reject:

* missing metadata,
* incorrect `doc_id`,
* misuse of authority flags.

---

## 7. Summary

This schema formalizes documentation governance.

No document exists outside this system.
