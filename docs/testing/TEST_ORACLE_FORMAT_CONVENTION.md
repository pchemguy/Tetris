# TEST_ORACLE_FORMAT_CONVENTION

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
