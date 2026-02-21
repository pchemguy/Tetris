---
doc_id: L5_REPORTS
name: L5_REPORTS.md
title: L5 — Execution State (Reports)
status: active
authority: normative
description: Defines the execution-state artifacts that record phase, gate, and implementation progress.
references: [IMPLEMENTATION_REPORTS]
---

# L5 — Execution State (Reports)

L5 defines the artifacts that record the **actual execution history** of the repository.

Unlike L2–L4, which define structural, behavioral, and proof contracts, L5 records:

- what has been attempted,
- what has passed or failed,
- what was modified,
- what is currently blocked,
- what the next intended action is.

L5 defines **state**, not policy.

---

## Directory

**Location**: `docs/reports/`

| Title                  | Filename                    | Role                                                        |
| ---------------------- | --------------------------- | ----------------------------------------------------------- |
| Implementation Reports | `IMPLEMENTATION_REPORTS.md` | Append-only execution record of phase and gate progression. |

---

## Nature of L5 artifacts

L5 artifacts are:

- mutable over time,
- append-only,
- descriptive of repository state,
- authoritative for “where development currently stands.”

They are not behavioral specifications and do not redefine correctness.

If an L5 report contradicts L2–L4, L2–L4 prevail.

---

## Implementation reports

`IMPLEMENTATION_REPORTS.md` is the canonical execution log.

It records:

- phase and gate attempts,
- success/failure outcomes,
- test suite execution results,
- artifact modifications,
- blockers and ambiguities discovered,
- declared next steps.

It answers:

- Where did development last stop?
- Which gate was last evaluated?
- What assumptions were made?
- What remains incomplete?

---

## Agent obligations

Any agent resuming work must:

1. Read `IMPLEMENTATION_REPORTS.md` before acting.
2. Confirm the current phase and gate.
3. Append a new entry after acting.
4. Never rewrite or delete prior entries.

History is immutable. Corrections must be appended, not edited.

---

## Relationship to other layers

- L1 defines progression rules.
- L2–L4 define structural, behavioral, and proof requirements.
- L5 records whether those requirements have been satisfied in practice.

L5 provides evidence of execution; it does not create authority.
