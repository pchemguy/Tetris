---
doc_id: DOC_SCHEMA
doc_title: Documentation Metadata Schema
doc_kind: control
doc_scope: global
doc_status: active
doc_authority: normative
gate_applies_to: all
phase_applies_to: all
supersedes: []
superseded_by: null
references: []
---

# Documentation Metadata Schema (Normative)

## 1. Purpose

This document defines the **normative metadata schema** used in the YAML front matter
of Markdown documents in this repository.

It exists to enable:

- deterministic documentation discovery,
- automated validation of references,
- explicit authority and applicability rules.

The authoritative machine schema is `DOC_SCHEMA.json`.

---

## 2. Where this schema applies

All Markdown documents intended to participate in the repository’s normative
documentation system **must** include YAML front matter that validates against
`DOC_SCHEMA.json`.

Exceptions:

- `docs/ideas/` documents may omit metadata, or may use `doc_kind: idea` and
  `doc_authority: non_normative` if metadata is present.

---

## 3. DOC_ID conventions (normative)

### 3.1 DOC_ID lexical format

A document identifier (DOC_ID) is a string matching:

- `^[0-9A-Z_]+$`

Rules:

- Uppercase letters `A–Z`, digits `0–9`, underscore `_` only.
- No dots, hyphens, spaces, or slashes.
- Non-empty.

Examples:

- `PROJECT`
- `PHASES`
- `ACCEPTANCE_GATES`
- `RUNTIME_SPEC`
- `RENDERING_TEST_ORACLE`

Non-examples:

- `runtime_spec` (lowercase)
- `RUNTIME-SPEC` (hyphen)
- `TETRIS.RUNTIME.SPEC` (dots)

### 3.2 Prose reference marker (non-authoritative convenience)

In document bodies, authors may reference other documents using:

- `@DOC_ID`

Examples:

- `See @RUNTIME_SPEC for tick semantics.`
- `Gate rules are in @ACCEPTANCE_GATES.`

Rules:

- `@DOC_ID` is **not authoritative**; YAML metadata is authoritative.
- Tooling may extract `@DOC_ID` tokens (typically excluding fenced code blocks)
  and validate them against the set of YAML `doc_id` values present in the repo.
- YAML front matter must not include `@` in any field.

---

## 4. Field semantics (normative)

- `doc_id`: The unique identifier of this document (see §3).
- `doc_title`: Human-readable title.
- `doc_kind`: Classification of the document’s role (control/spec/oracle/etc.).
- `doc_scope`: Applicability scope: `global`, `core`, `shell`, or `component:<name>`.
- `doc_status`: Lifecycle status: `draft`, `active`, `deprecated`.
- `doc_authority`: `normative` or `non_normative`.
- `gate_applies_to`: Gate range applicability (`all`, `none`, `N`, `N-M`).
- `phase_applies_to`: Phase range applicability (`all`, `none`, `N`, `N-M`).
- `supersedes`: List of DOC_IDs this document supersedes (may be empty).
- `superseded_by`: DOC_ID that supersedes this one, or `null`.
- `references`: DOC_IDs this document depends on (normative dependencies).

---

## 5. Validation expectations (normative)

1. **All YAML metadata must validate** against `DOC_SCHEMA.json`.
2. `doc_id` values must be **globally unique** across all docs participating in
   the system.
3. `references`, `supersedes`, and `superseded_by` must refer only to **existing**
   DOC_IDs (as defined by YAML front matter), unless the referenced doc is being
   introduced in the same change.
4. `doc_authority: non_normative` documents must not be treated as requirements
   unless a normative document explicitly promotes them.

---
