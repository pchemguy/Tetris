---
doc_id: DOC_SCHEMA
name: DOC_SCHEMA.md
title: Documentation Metadata Schema
status: active
authority: normative
description: Normative schema for YAML metadata embedded in repository Markdown documents.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - COMPONENT_REGISTRY
---

# Documentation Metadata Schema (Normative)

## 1. Purpose

This document defines the **normative metadata system** used in the YAML front matter of Markdown documents in this repository. It exists to make the documentation system **machine-checkable** and to support:

- deterministic document discovery,
- explicit authority classification (normative vs non-normative),
- explicit applicability (phase/gate),
- automated validation of cross-document dependencies,
- detection of duplicates, drift, and misclassification.

The authoritative machine schema is **`DOC_SCHEMA.json`**.

---

## 2. Applicability and authority

### 2.1 Normative documents under `docs/` must include metadata

All Markdown documents intended to participate in the repository’s documentation system **must** include a YAML front matter block that validates against
`DOC_SCHEMA.json`. Root documents are allowed to participate, but the minimum expectation is:

- all normative documents under `docs/` include metadata,
- any doc listed in the `AGENTS.md` index includes metadata,
- any doc, which can be backtracked to `AGENTS.md` via `references`, includes metadata.

### 2.2 Non-normative documents under `docs/`

- `docs/archive/`
- any path that includes a directory component matching case-insensitively one of (full directory name must match)
    - "idea"
    - "ideas"
    - "archive"
    - "archives"
    - "draft"
    - "drafts"
    - "note"
    - "notes"

Docs within these directories have **zero authority**.

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

- `references`
- `description`
- {`url` | `urls`}

Notes:

- Keys are case-sensitive and MUST match exactly.
- Required YAML lists MUST be populated even when empty (`[]`).
- YAML `null` MUST be explicit where allowed (`null`).
- Optional empty YAML keys should omitted.

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

### 4.2 Identity rules

- `doc_id` is the **authoritative identity**; paths and filenames are not.
- Once a document is `status: active`, its `doc_id` MUST NOT change.
- If a new identity is required:
    - create a new document with a new `doc_id`,
    - mark the old document `deprecated` if appropriate.

### 4.3 YAML references

Any `doc_id` within the `references` field must point to an existing normative document.

### 4.3 Uniqueness

If two files declare the same `doc_id`, it is a **hard failure** (Gate 0).

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
    - This is not authoritative identity; it supports review and auditing.
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
    - Most docs should use `url` (single link).
    - `urls` exists only when multiple links are necessary.
    - A doc MUST NOT include both `url` and `urls` keys simultaneously.
- `references`
    - Array of DOC_IDs this document depends on (normative dependency list).
    - This is the **authoritative dependency graph** (not filenames).

---

## 7. Validation expectations (Gate 0 auditable)

An agent (or CI) must treat the following as a Gate 0 failure:

- A required document is missing YAML front matter.
- YAML fails validation against `DOC_SCHEMA.json`.
- Duplicate `doc_id` exists.
- `references` points to a `doc_id` that does not exist in YAML inventory.
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
````

---

## 9. Relationship to machine schemas

* `DOC_SCHEMA.md` is the **human-readable normative policy**.
* `DOC_SCHEMA.json` is the **machine-checkable schema**.

If there is a conflict:

1. machine schemas must be updated to match this document, or
2. this document must be updated intentionally.

Silent divergence is forbidden.
