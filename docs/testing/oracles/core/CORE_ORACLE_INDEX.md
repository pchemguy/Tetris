---
doc_id: CORE_ORACLE_INDEX
name: CORE_ORACLE_INDEX.md
title: Core Oracle Index
status: active
authority: normative
description: Machine-checkable traceability map from core test oracles to the exact spec sections they validate.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - GAME_RULES
  - GAME_STATE
  - INPUT_MODEL
  - ERROR_HANDLING
  - SHAPES_AND_ROTATIONS
  - CORE_API
  - ORACLE_CORE_COLLISION
  - ORACLE_CORE_SPAWN
  - ORACLE_CORE_GEOMETRY
  - ORACLE_CORE_GRAVITY_AND_LOCKING
  - ORACLE_CORE_LINE_CLEAR
  - ORACLE_CORE_SCORING
  - ORACLE_CORE_RNG_7BAG
  - ORACLE_CORE_GAME_OVER
  - ORACLE_CORE_INVARIANTS
  - ORACLE_CORE_HOLD
---

# Core Oracle Index (Normative)

## 1. Purpose

This document defines the **authoritative traceability map** between:

- **core behavioral specifications** (L3), and
- **core automated test oracles** (L4).

It exists to make traceability:

- explicit (humans can audit coverage),
- machine-checkable (tooling can validate completeness),
- stable under file moves/renames (DOC_ID based).

This document **does not define new behavior** and **does not define new proof obligations**.  
It only maps existing proof obligations (oracle docs) to the spec clauses they validate.

## 2. Interpretation rules (normative)

### 2.1 Primary meaning

- Each mapping row is a claim:  
  **“This oracle validates these exact spec sections.”**
- Tooling may treat this file as a coverage matrix.

### 2.2 Non-goals

This document must not:

- introduce requirements not present in an oracle doc,
- weaken requirements specified in an oracle doc,
- redefine behavior described in a spec.

If a conflict is detected:
- the spec/oracle documents are authoritative,
- this index must be corrected.

### 2.3 Spec section identifiers (convention)

Each spec clause is referenced by:

- `@DOC_ID` plus a **section path**, using one of:

1) `§<number>` (preferred when stable)  
2) `§<number>.<number>`  
3) `§<number>.<number>.<number>`  
4) `#<heading-slug>` (allowed when numeric sections are absent)

Examples:

- `@GAME_STATE §5.2`
- `@GAME_RULES §9.3`
- `@SHAPES_AND_ROTATIONS §3.1`
- `@CORE_API §5.2`

Tooling may parse section paths as opaque strings; numeric semantics are for humans.

### 2.4 Minimum completeness rule (normative, Gate 0 style)

For Gates **1–6**, the set of core specs listed in `references:` above must be fully covered such that:

- every **normative behavioral clause** relevant to Gates 1–6
  is mapped to **at least one** oracle document,
- unless explicitly tagged **OUT OF SCOPE** in the spec itself.

If a clause is not mapped, it is treated as a documentation defect and must be resolved
by updating this index and/or introducing an oracle.

---

## 3. Machine-readable traceability artifacts

This oracle index has **two parallel representations**:

- `CORE_ORACLE_INDEX.md` (this file) — human-readable normative index.
- `CORE_ORACLE_INDEX.json` — the **machine-readable traceability matrix** containing the same oracle↔spec linkage content in structured form.
- `CORE_ORACLE_INDEX.schema.json` — the JSON Schema used to validate `CORE_ORACLE_INDEX.json`.

### 3.1 Normative relationship

- This Markdown document defines the **normative meaning** of the index (what each field represents and how to interpret it).
- The JSON instance is the **normative machine artifact** used for tooling, validation, and automated checks.
- The schema is **normative for validation**, not for semantics: it constrains structure, not intent.

If a conflict is detected:

1. Treat `CORE_ORACLE_INDEX.json` as the authoritative machine source for automation.
2. Treat this document as the authoritative human source for interpretation.
3. Resolve conflicts by updating one so that both match; do not “work around” mismatches in tooling.

### 3.2 Required invariants (tooling expectations)

Tooling that consumes the index must enforce:

- **Oracle file existence**: every oracle referenced in `CORE_ORACLE_INDEX.json` must correspond to a real `ORACLE_*.md` document with a YAML `doc_id` matching the referenced oracle id.
- **Spec target existence**: every referenced spec (`doc_id`) must exist as a YAML `doc_id` in the repository.
- **Section traceability**: each mapping must include:
    - a `spec_doc_id`, and
    - a `spec_section` (a stable section identifier, e.g. `§6 Rotation` or an explicit anchor token).
- **Gate applicability consistency**: if the JSON declares oracle applicability to gates/phases, it must not contradict the oracle document’s YAML header fields (`gate_applies_to`, `phase_applies_to`).

### 3.3 Round-trip constraint

`CORE_ORACLE_INDEX.json` must be a **faithful structured representation** of this index:

- No oracle/spec relationships may exist only in JSON or only in Markdown.
- Any update to oracle coverage must update both representations in the same change.

### 3.4 Intended use

The JSON index enables:

- generation of coverage reports (spec section → oracle coverage),
- detection of orphan specs (no oracle),
- detection of orphan oracles (not referenced by index),
- CI checks that block merges when traceability is incomplete.

### 3.5 Schema semantics boundary

`CORE_ORACLE_INDEX.schema.json` validates the **structural correctness** of the machine-readable index (field presence, types, required keys, uniqueness constraints). It does **not** define semantic meaning, coverage adequacy, or cross-document correctness.

Semantic validity — including whether mappings are conceptually correct, complete, or consistent with the referenced specification sections — is governed by this document and by the referenced spec documents themselves.

Tooling must therefore distinguish:

- **Structural validity** (schema validation),
- **Traceability completeness** (index coverage checks),
- **Normative correctness** (spec↔oracle alignment).

---

## 4. Oracle → Spec traceability map (normative)

### 4.1 ORACLE_CORE_COLLISION

Validates:

- `@GAME_RULES` §2.1, §2.2 (playfield bounds, hidden rows = none)
- `@GAME_RULES` §6.3 (movement constraints: collision rejection)
- `@GAME_RULES` §4.2 (rotation collision rejection; kicks as collision policy)
- `@GAME_STATE` §2 (coordinate system and bounds)
- `@GAME_STATE` §6.1 (collision predicate definition)
- `@GAME_STATE` §6.2 (movement actions + rejection behavior)
- `@GAME_STATE` §6.3 (rotation actions: collision gating + kick attempts)
- `@INPUT_MODEL` §3.3 (rejection semantics: continue processing)
- `@ERROR_HANDLING` §2.1 (rejected action definition)
- `@ERROR_HANDLING` §4.2 (active piece validity: within bounds, no overlap)
- `@CORE_API` §5.3 (blocks_for must return in-bounds positions given valid state)
- `@CORE_API` §7.1 (strict state validation expectations)

### 4.2 ORACLE_CORE_SPAWN

Validates:

- `@GAME_RULES` §5.1 (spawn position)
- `@GAME_RULES` §5.2 (spawn collision → game over)
- `@GAME_STATE` §6.7 (spawning semantics: active=next, generate new next)
- `@GAME_STATE` §5.2 (tick ordering: spawn after lock/clear/score)
- `@CORE_API` §5.1 (new_game initialization + spawn)
- `@CORE_API` §4.1 (GameState fields: next_piece defined)
- `@ERROR_HANDLING` §4.1 (next_piece always defined; defensive behavior)

### 4.3 ORACLE_CORE_GEOMETRY

Validates:

- `@SHAPES_AND_ROTATIONS` §2.1 (local coordinate mapping)
- `@SHAPES_AND_ROTATIONS` §2.2 (enumerated rotation states only)
- `@SHAPES_AND_ROTATIONS` §3.* (piece definitions: I/O/T/S/Z/J/L)
- `@SHAPES_AND_ROTATIONS` §4 (geometry invariants: 4 blocks, uniqueness)
- `@GAME_RULES` §3.2 (explicit enumeration required)
- `@GAME_STATE` §3.3 (blocks(active_piece) = exactly 4 blocks)
- `@CORE_API` §5.3 (blocks_for uses enumerations; deterministic ordering)

### 4.4 ORACLE_CORE_GRAVITY_AND_LOCKING

Validates:

- `@GAME_RULES` §6.1 (gravity: down by 1 cell)
- `@GAME_RULES` §7.1–§7.2 (lock rule, no lock delay)
- `@GAME_RULES` §9.3 (gravity scaling formula)
- `@GAME_STATE` §4.2 (gravity counter contract)
- `@GAME_STATE` §5.2 (tick ordering: gravity after inputs)
- `@GAME_STATE` §6.4 (locking semantics)
- `@INPUT_MODEL` §4 (ordering relative to gravity; hard drop skips gravity)
- `@CORE_API` §5.4 (gravity_ticks_per_cell formula + errors)

### 4.5 ORACLE_CORE_LINE_CLEAR

Validates:

- `@GAME_RULES` §8.1–§8.2 (row full detection; simultaneous clear)
- `@GAME_STATE` §6.5 (line clear resolution)
- `@ERROR_HANDLING` §4.1 (board invariants remain valid post-clear)

### 4.6 ORACLE_CORE_SCORING

Validates:

- `@GAME_RULES` §9.1 (score deltas for k lines)
- `@GAME_RULES` §9.2 (level progression every 10 lines)
- `@GAME_STATE` §6.6 (score/level update semantics)
- `@ERROR_HANDLING` §4.1 (score non-negative, level >= 1)

### 4.7 ORACLE_CORE_RNG_7BAG

Validates:

- `@GAME_RULES` §10.1–§10.2 (7-bag method; determinism)
- `@GAME_STATE` §3.5 (RNG must be part of state; determinism)
- `@CORE_API` §3.2 (RngState fields)
- `@CORE_API` §5.1 (new_game initializes RNG)
- `@CORE_API` §9 (compatibility notes: determinism under seed)

### 4.8 ORACLE_CORE_GAME_OVER

Validates:

- `@GAME_RULES` §11 (game over conditions)
- `@GAME_STATE` §5.2 (game-over short circuit)
- `@GAME_STATE` §6.7 (spawn collision → game over)
- `@ERROR_HANDLING` §4.2 (active validity conditional on game over)
- `@CORE_API` §5.2 (game-over short circuit semantics)

### 4.9 ORACLE_CORE_INVARIANTS

Validates:

- `@GAME_STATE` §8 (invariants after every step)
- `@ERROR_HANDLING` §4.1–§4.2 (mandatory invariants; strict enforcement)
- `@CORE_API` §4.2 (immutability requirement)
- `@CORE_API` §7.1 (strict validation behavior)

### 4.10 ORACLE_CORE_HOLD

Validates (only if hold is enabled):

- `@GAME_RULES` §12.2 (hold rules)
- `@GAME_STATE` §3.7 (hold fields)
- `@GAME_STATE` §6.8 (hold transitions + once-per-piece)
- `@INPUT_MODEL` §6 (hold input constraints)
- `@CORE_API` §3.2 (InputEvent.HOLD policy) and §4.1 (hold fields always exist)

---

## 5. Tooling contract (normative expectations)

Tooling that consumes this document may:

1. Parse YAML `references:` to locate required docs.
2. Parse `### ORACLE_*` sections as oracle identifiers.
3. Extract `Validates:` bullets as the traceability edges.

Minimum validations:

- Every oracle listed in YAML `references:` must have a corresponding section here.
- Every `@DOC_ID` referenced here must exist in YAML doc inventory.
- No unknown oracle IDs appear in this index.
- Optional: warn if any referenced spec section cannot be located (best-effort).

---
