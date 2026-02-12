---
doc_id: DOCS_AUTHORITY_MAP
name: DOCS_AUTHORITY_MAP.md
title: Documentation Metadata Schema
kind: meta
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Hierarchy and conflict-resolution rules among normative documents.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# Documentation Authority Map (Normative)

This repository is governed by a **layered documentation system**.
Each document class has a **defined authority domain**.
When documents conflict, **authority flows downward only** as specified here.

---

## Authority hierarchy (top → bottom)

```
┌──────────────────────────────────────────────┐
│ PROCESS & SCOPE CONTROL                      │
│                                              │
│  PHASES.md                                   │
│  ACCEPTANCE_GATES.md                         │
│                                              │
│  • What work is allowed                      │
│  • When progression is permitted             │
│  • What constitutes “done”                   │
└──────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│ SYSTEM STRUCTURE                             │
│                                              │
│  ARCHITECTURE.md                             │
│  DECOMPOSITION.md                            │
│                                              │
│  • What the system is                        │
│  • What components exist                     │
│  • Responsibility boundaries                 │
│  • Non-negotiable separations                │
└──────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│ BEHAVIORAL SPECIFICATIONS                    │
│                                              │
│  Core specs:                                 │
│    GAME_RULES.md                             │
│    GAME_STATE.md                             │
│    INPUT_MODEL.md                            │
│    ERROR_HANDLING.md                         │
│    SHAPES_AND_ROTATIONS.md                   │
│    CORE_API.md                               │
│                                              │
│  Shell specs:                                │
│    RUNTIME_SPEC.md                           │
│    RENDERING_SPEC.md                         │
│    CLI_SPEC.md                               │
│    REPLAY_SPEC.md                            │
│                                              │
│  • What the system does                      │
│  • What behavior is permitted                │
│  • What is explicitly out of scope           │
└──────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│ CORRECTNESS PROOF                            │
│                                              │
│  CORE_TEST_ORACLE.md                         │
│  *_TEST_ORACLE.md                            │
│                                              │
│  • What must be tested                       │
│  • What evidence is required                 │
│  • What “correct” means                      │
└──────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────┐
│ IMPLEMENTATION                               │
│                                              │
│  tetris/src/tetris/                          │
│  tests/                                      │
│                                              │
│  • Must satisfy all above layers             │
│  • Has no authority of its own               │
└──────────────────────────────────────────────┘
```

---

## Conflict resolution rules (normative)

If two artifacts disagree, authority is resolved as follows:

1. **Process beats structure**
    If work is correct but not allowed in the current phase or gate → **FAIL**.
2. **Structure beats behavior**
    If behavior is specified but violates architecture or decomposition → **FAIL**.
3. **Behavior beats implementation**
    If code behaves differently from specs → **FAIL**.
4. **Oracles beat ad-hoc tests**
    Passing tests not required by a test oracle is **insufficient**.
5. **Docs always beat code**
    Code is never authoritative.

---

## What each layer may and may not do

### PHASES / ACCEPTANCE_GATES

* ✔ decide *whether* work is allowed
* ✘ define system behavior

### ARCHITECTURE / DECOMPOSITION

* ✔ define structure and boundaries
* ✘ define exact behavior or algorithms

### SPECIFICATIONS

* ✔ define exact behavior
* ✘ define test sufficiency

### TEST ORACLES

* ✔ define proof requirements
* ✘ define new behavior

### CODE

* ✔ implement
* ✘ decide scope, structure, or correctness

---

## One-sentence rule for agents (normative)

> Determine **phase → gate → structure → behavior → oracle** before writing or modifying code.

---

## One-sentence rule for humans

> If something feels ambiguous, the ambiguity must be resolved by **editing the highest-authority document**, not by changing code.

---

