---
doc_id: SOFTWARE_DEVELOPMENT_HARNESS
name: SOFTWARE_DEVELOPMENT_HARNESS.md
title: Generic Software Development Harness
status: active
authority: normative
description: This document discusses the key objective of the project focused on developing a harness for agentic software development.
keywords:
  - Domain-Neutral Documentation (DND)
  - Semantic Independence of Specification (SIS)
  - Terminology De-Semanticization (TDS)
  - Alias-Invariance of Requirements (AIR)
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69a27bc9-5f60-838f-b2dc-e7a32de243ca
---
## Alias-Invariance Objective

The project documentation set MUST fully specify behavior such that all domain-loaded identifiers (e.g., `tetris`, `tetromino`, `line`, `bag`, `rotation`, etc.) can be mechanically replaced with **semantically neutral aliases** (e.g., `system`, `piece`, `row`, `pool`, `orientation`) without changing the implementability, correctness, or testability of the system.

This ensures that an implementation agent can rely exclusively on explicit contracts and not on prior cultural/LLM knowledge of “Tetris”.

## Semantically neutral aliases

A term is a **neutral alias** if it:

* carries **no game/domain meaning** in ordinary English beyond being a label (e.g., `entity_a`, `token_7`, `actor`, `unit`, `state_delta`),
* does not embed hints via metaphor (avoid `block`, `fall`, `stack`, `row-clear`, etc.),
* is consistently applied across:
    * prose
    * code identifiers (public API + internal names where referenced)
    * diagrams/tables
    * test names and oracle phrasing

## Acceptance criteria (make it measurable)

### A. Mechanical rename invariance

A deterministic, mechanical rename pass (search/replace) over a defined vocabulary set MUST produce a doc set that is still:

* internally consistent (no broken cross-refs),
* fully implementable (no missing semantics),
* fully testable (oracles still executable/meaningful).

### B. Zero implicit-domain dependency

No requirement may depend on “common knowledge of Tetris”. Concretely: any behavior that a reader might otherwise infer from the word “tetromino” MUST be explicitly defined elsewhere (shapes, spawn rules, rotation rules, collision rules, scoring if present, termination, etc.).

### C. Explicit concept grounding

All behaviorally relevant nouns MUST have:

   * a formal definition (in a glossary / terminology section),
   * a reference to the authoritative spec section defining its operational meaning,
   * at least one corresponding oracle or gate criterion if it affects correctness.

### D. Vocabulary quarantine (optional but strong)

Domain-loaded terms MUST be treated as *presentation-layer labels* only:

   * they may appear in “friendly alias” sections,
   * but normative rules MUST be written so that domain words are replaceable without loss.

## How to structure the docs to satisfy it (practical design)

### 1. Two-layer terminology pattern

* **Normative layer:** uses neutral *canonical* terms (e.g., `unit`, `shape_kind`, `orientation`, `grid`, `occupied_cells`, `spawn_rule`).
* **Informative alias map:** a non-normative table mapping:
    * `tetromino` ↔ `unit`
    * `tetris` ↔ `system` / `game`
    * `line` ↔ `full_row`
    * etc.

This lets humans keep readability without letting semantics leak into the normative layer.

### 2) “No-metaphor” rule for normative prose

In normative sections, prohibit metaphor words that smuggle meaning:

* “falls”, “drops”, “gravity”, “stack”, “clear”, “well”, “bag”, “hold”, etc.

Instead, describe only state transitions:

* “on each step, apply translation vector (0, +1) unless blocked…”

### 3) Make oracles alias-proof

Oracle phrasing should reference only:

* state inputs
* deterministic transitions
* invariants
* rejection semantics
  …not domain language.

## A concrete “gate” you can add (fits your workflow)

**G?.X — Alias-Invariance Check**

Mandatory criteria:

* Provide a rename map for at least: `tetris`, `tetromino` (and ideally the whole domain vocabulary list).
* Apply rename to the normative docs (mechanically).
* Verify:
    * all normative cross-references still resolve,
    * all required concepts remain defined,
    * all test oracle statements remain interpretable and implementable.

Evidence artifacts:

* `ALIAS_MAP.md` (or YAML/JSON)
* renamed build output under `docs/_derived/alias_invariant/`
* a short “diff rationale” stating that only identifiers changed, not semantics.

## Synopsis

The documentation base MUST be **alias-invariant**: domain-loaded terms (e.g., “tetris”, “tetromino”) are treated as arbitrary labels and may be replaced via mechanical renaming with semantically neutral identifiers without loss of implementability or testability. Any behavior that might be inferred from those terms MUST be defined explicitly by normative specifications and validated by corresponding test oracles; no implicit reliance on cultural knowledge of the game is permitted.
