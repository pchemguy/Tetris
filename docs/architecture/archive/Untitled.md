Below is a **complete, drop-in DOC_ID metadata system** you can adopt across `docs/` (and optionally root docs). It’s designed to be:

* deterministic to parse (even by dumb scripts/agents),
* resilient to file moves/renames,
* strict about duplicates/conflicts,
* compatible with your “authority map / phases / gates / oracles” model.

You’ll add a small YAML block near the top of each normative doc.

---

## DOC_ID Metadata System (Normative)

### 1) Purpose

`DOC_ID` metadata provides a **stable identity** for each document that does not depend on file paths. It enables:

* unambiguous citation (`DOC_ID` beats filename),
* conflict detection (duplicate or mismatched docs),
* automated doc indexing and Gate 0 auditing,
* safe refactors (move/rename files without breaking identity).

---

## 2) Required header format

Every **normative** Markdown document under `docs/` MUST start with a metadata block in the first ~30 lines, before substantive content:

```yaml
---
doc_id: <string>
doc_title: <string>
doc_kind: <one of: control|architecture|decomposition|spec|oracle|api|map|report>
doc_scope: <one of: global|core|shell|component:<name>>
doc_status: <one of: draft|active|deprecated>
doc_authority: <one of: normative|non_normative>
gate_applies_to: <string>        # e.g. "0", "1-6", "10", "10-13", "all", "none"
phase_applies_to: <string>       # e.g. "0", "1", "2-5", "all", "none"
supersedes: [<doc_id>, ...]      # optional, may be empty list
superseded_by: <doc_id|null>     # optional
references: [<doc_id>, ...]      # list of DOC_IDs this doc depends on (not filenames)
---
```

Notes:

* YAML keys must be **exactly** as shown (case-sensitive).
* `doc_id` is immutable once published (see §4).
* `references` should be DOC_IDs, not filenames. Filenames may still appear in prose.

---

## 3) DOC_ID format (strict)

`doc_id` MUST match:

```
TETRIS.<CLASS>.<NAME>[.<VARIANT>]
```

Where:

* `TETRIS` is the fixed project namespace.

* `<CLASS>` is one of:

  * `CONTROL` (phases, gates)
  * `ARCH` (architecture)
  * `DECOMP` (decomposition)
  * `SPEC` (component specifications)
  * `ORACLE` (test oracles)
  * `API` (public shell APIs like presenter/input driver)
  * `MAP` (authority maps / doc graphs)
  * `REPORT` (execution logs / reports)

* `<NAME>` is uppercase snake case.

* Optional `<VARIANT>` is uppercase snake case, used for renderer variants etc.

Examples:

* `TETRIS.CONTROL.PHASES`
* `TETRIS.CONTROL.ACCEPTANCE_GATES`
* `TETRIS.ARCH.SYSTEM`
* `TETRIS.DECOMP.SYSTEM`
* `TETRIS.SPEC.CORE_API`
* `TETRIS.SPEC.RENDERING_ASCII`
* `TETRIS.ORACLE.CORE`
* `TETRIS.ORACLE.RENDERING_ASCII`
* `TETRIS.API.PRESENTER`
* `TETRIS.API.INPUT_DRIVER`
* `TETRIS.MAP.DOCS_AUTHORITY`
* `TETRIS.REPORT.IMPLEMENTATION`

---

## 4) Identity and immutability rules

### 4.1 Uniqueness

Within the repository:

* Each `doc_id` MUST be globally unique.
* If two files contain the same `doc_id`, it is a **hard failure** (Gate 0).

### 4.2 Immutability

Once a document is `doc_status: active`, its `doc_id` MUST NOT change.

Permitted refactors without changing `doc_id`:

* file rename,
* file move within `docs/`,
* content edits consistent with authority rules.

If you need a “new doc identity”:

* create a new `doc_id`
* mark the old one deprecated and link via `supersedes` / `superseded_by`.

---

## 5) Reference rules

### 5.1 Prefer DOC_ID in normative references

Normative docs MUST reference other normative docs by `doc_id` in one of:

* the `references:` header list (preferred for machine parsing),
* or explicitly in text (e.g., “See `TETRIS.CONTROL.PHASES`”).

Filenames may be included for convenience but are not authoritative.

### 5.2 Resolution precedence

If a filename and DOC_ID disagree, **DOC_ID wins**.

Example: If a file is named `PHASES.md` but its header says `doc_id: TETRIS.SPEC.RENDERING_ASCII`, the filename is wrong; treat as mismatch and BLOCK (see §7).

---

## 6) Non-normative docs

Non-normative docs MAY include metadata, but if they do:

* `doc_authority` MUST be `non_normative`
* `doc_kind` SHOULD be `report` or `map` or `spec` depending on intent
* `gate_applies_to` and `phase_applies_to` MUST be `none` unless explicitly intended

For `docs/ideas/`, enforce:

* either **no metadata at all**, or
* `doc_authority: non_normative` and `doc_status: draft`

---

## 7) Gate 0 enforcement checks (machine-auditable)

An agent must treat any of the following as a Gate 0 failure and halt `BLOCKED`:

* missing metadata header in a normative doc,
* invalid `doc_id` format,
* duplicate `doc_id` across files,
* `doc_authority` not `normative` for a doc listed in PROJECT index as normative,
* `references:` contains unknown `doc_id` (unless explicitly allowed),
* filename implies a different role than `doc_id` (optional but recommended).

---

## 8) Minimal headers for your key docs

Here are compliant minimal examples you can paste.

### `docs/PHASES.md`

```yaml
---
doc_id: TETRIS.CONTROL.PHASES
doc_title: Repository Evolution Phases
doc_kind: control
doc_scope: global
doc_status: active
doc_authority: normative
gate_applies_to: all
phase_applies_to: all
supersedes: []
superseded_by: null
references: [TETRIS.CONTROL.ACCEPTANCE_GATES]
---
```

### `docs/ACCEPTANCE_GATES.md`

```yaml
---
doc_id: TETRIS.CONTROL.ACCEPTANCE_GATES
doc_title: Milestone Acceptance Gates
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
```

### `docs/ARCHITECTURE.md`

```yaml
---
doc_id: TETRIS.ARCH.SYSTEM
doc_title: System Architecture
doc_kind: architecture
doc_scope: global
doc_status: active
doc_authority: normative
gate_applies_to: all
phase_applies_to: all
supersedes: []
superseded_by: null
references: [TETRIS.DECOMP.SYSTEM]
---
```

### `docs/DECOMPOSITION.md`

```yaml
---
doc_id: TETRIS.DECOMP.SYSTEM
doc_title: System Decomposition and Component Responsibilities
doc_kind: decomposition
doc_scope: global
doc_status: active
doc_authority: normative
gate_applies_to: all
phase_applies_to: all
supersedes: []
superseded_by: null
references: [TETRIS.ARCH.SYSTEM]
---
```

### `docs/CORE_TEST_ORACLE.md`

```yaml
---
doc_id: TETRIS.ORACLE.CORE
doc_title: Core Test Oracle
doc_kind: oracle
doc_scope: core
doc_status: active
doc_authority: normative
gate_applies_to: 1-6
phase_applies_to: 1
supersedes: []
superseded_by: null
references: [TETRIS.SPEC.CORE_API, TETRIS.SPEC.GAME_RULES, TETRIS.SPEC.GAME_STATE]
---
```

(Adjust references to match your actual spec DOC_IDs.)

---

## 9) One clause to add to AGENTS.md

If you want to formalize agent behavior, drop this in:

> **DOC_ID rule:** For any normative document, the agent must resolve and cite documents by `doc_id` when available. If a normative document lacks a valid DOC_ID header, the agent must halt `BLOCKED`.

---

If you want, I can also give you a **DOC_ID registry table** (PROJECT.md section) listing every doc with its DOC_ID, file path, scope, and gate applicability—so Gate 0 can be checked mechanically without opening every file.
