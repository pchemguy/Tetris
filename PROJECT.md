---
doc_id: PROJECT
name: PROJECT.md
title: Project Entry Point
kind: map
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
references:
  - DOCUMENTATION_SYSTEM
  - DOC_INVENTORY
description: |
  Primary repository entry point. Defines high-level goals, repository layout, and mandatory documentation discovery workflow. Delegates normative documentation system rules to DOCUMENTATION_SYSTEM and inventory-based traversal.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# PROJECT.md

This document acts as the primary entry point for project's technical documentation, and explains its documentation system and high-level workflows.

## 1. Project overview

This project develops and evaluates a **prompting system for agentic software development**. Repository evolution is organized into explicit **phases** (defined in `docs/PHASES.md`), which constrain *what kind of work is allowed* at each stage. 

The reference implementation target is **classic Tetris**, chosen not as a game project per se, but as a compact, well-understood system that stresses:

* deterministic state machines,
* strict rule adherence,
* geometry and collision logic,
* time-stepped simulation,
* incremental feature integration,
* comprehensive test oracles.

The primary deliverable of this repository is **not** “a Tetris game”, but a **set of development contracts, specifications, and acceptance gates** that allow rigorous evaluation of whether an AI agent can:

* discover and obey documentation,
* implement incrementally without guessing,
* stop and escalate when blocked,
* produce auditable, deterministic software artifacts.

Human developers remain ultimately responsible for correctness and maintenance, but the project is explicitly designed to be **AI-readable, AI-actionable, and AI-auditable**.

---

## 2. Repository layout (high level)

```
Tetris/
├── docs/                  # Normative development specifications (authoritative)
├── docs/ideas/            # Non-normative preliminary features/component ideas for possible future consideration
├── tetris/
│     ├── src/tetris/      # Python core + shell implementation package
│     └── tests/           # Tests
├── .agent/skills/         # Agent skills (plan / implement / review units)
├── AGENTS.md              # General agent instructions
├── PROJECT.md             # This document (primary entry point)
└── README.md              # Optional human-facing wrapper
```

The **docs/** directory is authoritative.
Code exists to satisfy the docs — not the other way around.

---

## 3. Intended development workflow (summary)

The workflow below assumes full understanding of the documentation authority model described in the next section.

1. Build or load a documentation inventory (docs traversal or `DOC_INVENTORY.json`).
2. Read all normative documents required for the target gate (per inventory and authority rules).
3. **Read `IMPLEMENTATION_REPORTS.md`** to determine current state.
4. Determine the current repository **phase** (`PHASES.md`).
5. Confirm the current **acceptance gate** (`ACCEPTANCE_GATES.md`).
6. Implement incrementally, gate by gate.
7. Write tests mapped to the applicable `*_TEST_ORACLE.md` document(s).
8. Append results to `IMPLEMENTATION_REPORTS.md`.
9. Stop and escalate on ambiguity.
10. Extend behavior **only by updating documentation first**.

---

## 4. Documentation system and discovery (normative)

This repository uses a **hybrid documentation reference model**:

- **Filename references** (e.g., `AGENTS.md`) are primarily used conventionally for **local directory references**.
- Special **DOC_ID references** (e.g., `@PHASES`, `@RUNTIME_SPEC`) are the **canonical repository-wide reference mechanism** for documents under `docs/`.

The normative rules, metadata conventions, authority rules, and reference-resolution algorithm are defined in:

- `docs/meta/DOCUMENTATION_SYSTEM.md`

This includes:

- DOC_ID YAML metadata requirements,
- the authority model and conflict resolution,
- reference-resolution rules (filename vs `@DOC_ID`),
- Gate 0 documentation compliance checks.

To resolve document references deterministically, agents and tooling must operate from a documentation inventory produced by either:

1. **Standard docs traversal**:
   recursively traverse `docs/`, parse YAML metadata headers, and build an in-memory DOC_ID index; or
2. **Inventory file (preferred)**:
   load the precomputed inventory (described in `DOC_INVENTORY.md`):
    - `docs/meta/DOC_INVENTORY.json`

Because this repository intentionally mixes filename-local references and repository-wide DOC_ID references, agents must **not** attempt to “follow references” by filesystem guessing alone.

## 5. Audience note

* **AI agents**: This document defines your operating environment. Partial reading is failure.
* **Human developers**: This document is intended to remain readable, editable, and authoritative even as AI assistance evolves.

---

