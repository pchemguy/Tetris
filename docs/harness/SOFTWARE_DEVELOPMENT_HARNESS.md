---
doc_id: SOFTWARE_DEVELOPMENT_HARNESS
name: SOFTWARE_DEVELOPMENT_HARNESS.md
title: Software Development Harness Specification
status: active
authority: normative
description: Defines the requirements for a domain-neutral, alias-invariant documentation harness enabling implementation without reliance on implicit or cultural knowledge.
keywords:
  - Domain-Neutral Documentation (DND)
  - Semantic Independence of Specification (SIS)
  - Terminology De-Semanticization (TDS)
  - Alias-Invariance of Requirements (AIR)
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69a27bc9-5f60-838f-b2dc-e7a32de243ca
---

# Software Development Harness

## Synopsis

The project documentation base MUST be alias-invariant and semantically self-contained. Domain-loaded terms are treated as arbitrary labels and may be mechanically replaced without loss of meaning. All behavior must be derived exclusively from explicit normative specification and validated by corresponding test oracles. No implementation agent may rely on cultural knowledge of the domain.

## 1. Purpose

This document defines requirements for constructing a **domain-neutral software development harness**.

The harness formalizes a documentation-first development paradigm in which human developers operate as specification engineers. The primary artifact of development is a rigorously structured, normative documentation corpus written in technical natural language.

This documentation corpus MUST be sufficient to:

- drive context construction for implementation agents,
- enable stepwise generation of source code and test suites,
- support iterative refinement under formal acceptance gates,
- allow full system implementation from an empty repository.

Implementation agents (human or automated) MUST be able to construct the system using **only explicit specifications**, without reliance on:

- prior domain knowledge,
- cultural familiarity,
- historical conventions,
- latent model semantics,
- undocumented assumptions.

The documentation corpus MUST therefore be:

- self-contained,
- behaviorally complete,
- formally structured,
- alias-invariant,
- verifiable via explicit test oracles.

---

## 2. Core Objective: Alias-Invariance

The project documentation set MUST fully specify behavior such that all domain-loaded identifiers (e.g., `tetris`, `tetromino`, `line`, `bag`, `rotation`) can be mechanically replaced with semantically neutral aliases (e.g., `system`/`app`/`application`/`program`/`package`, `unit`/`piece`/`element`/`figure`/`shape`, `full_row`, `permutation_pool`, `orientation`) without changing:

- implementability,
- correctness,
- testability.

An implementation agent MUST be able to rely exclusively on explicit contracts and MUST NOT require prior knowledge of the cultural concept traditionally associated with the domain terms.

---

## 3. Semantically Neutral Aliases - Definition

A term qualifies as a **semantically neutral alias** if it:

- carries no embedded game or cultural meaning beyond being an arbitrary label,
- introduces no behavioral implications through metaphor,
- is defined exclusively through formal specification.
* is consistently applied across:
    * prose
    * code identifiers (public API + internal names where referenced)
    * diagrams/tables
    * test names and oracle phrasing

Examples of acceptable neutral terms:

- `unit`
- `entity_a`
- `orientation_index`
- `state_delta`
- `permutation_pool`

Examples of prohibited metaphor-bearing terms in normative layers:

- `fall`
- `gravity`
- `stack`
- `clear`
- `well`
- `bag`
- `hold`
- `block`
- `row-clear`

---

## 4. Acceptance Criteria

### A. Mechanical Rename Invariance

A deterministic mechanical rename pass over a defined vocabulary set MUST produce a documentation corpus that remains:

- internally consistent,
- cross-reference complete,
* fully implementable (no missing semantics),
* fully testable (oracles still executable/meaningful).

The rename operation MUST require no semantic interpretation — simple search-and-replace must suffice.

---

### B. Zero Implicit-Domain Dependency

No requirement may depend on “common knowledge” of the domain. Any behavior that might be inferred from domain terminology MUST be explicitly specified.

This includes, but is not limited to:

- shape definitions
- orientation rules
- spawning rules
- movement rules
- collision detection
- row completion detection
- scoring rules (if applicable)
- termination conditions

If a behavior cannot be derived directly from explicit specification, the documentation is non-compliant.

---

### C. Explicit Concept Grounding

All behaviorally relevant nouns MUST:

1. Have a formal definition in the normative glossary.
2. Reference an authoritative specification section defining its operational meaning.
3. Be linked to at least one corresponding oracle or gate if correctness-critical.

No concept may exist implicitly.

---

### D. Vocabulary Quarantine

Domain-loaded terms MUST be treated as *presentation-layer labels* only:

- MAY appear in informative or presentation contexts.
- MUST NOT define or imply normative behavior.
- MUST be replaceable without loss of meaning.

Normative specifications MUST use canonical neutral terminology.

---

## 5. Documentation Architecture Requirements

### 5.1 Two-Layer Terminology Pattern

The documentation MUST adopt a two-layer structure:

#### Normative Layer

Uses canonical, semantically-neutral terms exclusively:
- `unit`
- `orientation`
- `grid`
- `occupancy_state`
- `spawn_rule`

#### Informative Alias Layer

Provides a mapping between domain-loaded and canonical terms, e.g.:

* `tetromino` ↔ `unit`
* `tetris` ↔ `system` / `game`
* `line` ↔ `full_row`
* etc.

The mapping MUST be defined in `ALIAS_MAP.yaml`. Normative rules MUST remain valid if domain terms are removed entirely.

---

### 5.2 No-Metaphor Rule

Normative prose MUST describe:

- state transitions,
- invariants,
- preconditions,
- postconditions,
- rejection semantics.

It MUST NOT describe behavior through metaphorical language.

Correct:  
> On each step, apply translation vector (0, +1) unless blocked by occupancy or boundary constraint.

Incorrect:  
> The piece falls due to gravity until it lands.

---

### 5.3 Oracle Alias-Proofing

Test oracles MUST:

- reference canonical terms only,
- define expected state transitions precisely,
- avoid metaphor,
- remain valid under mechanical renaming.

If renaming breaks oracle clarity, the oracle is non-compliant.

---

## 6. Alias-Invariance Gate

### GX.Y — Alias-Invariance Check

#### Objective

Prove that the documentation base is semantically independent of domain terminology.

#### Mandatory Criteria

1. `ALIAS_MAP.yaml` exists and is normative.
2. All canonical terms exist in `GLOSSARY_NORMATIVE.md`.
3. Normative specifications use canonical terminology.
4. Domain-loaded terms do not define behavior.
5. Mechanical rename produces a consistent documentation corpus.
6. All referenced oracles remain interpretable after renaming.

#### Evidence Artifacts

- `ALIAS_MAP.yaml`
- `ALIAS_MAP.md`
- Renamed documentation under `docs/_derived/alias_invariant/`
- Rename validation report
- Confirmation that all referenced oracles remain valid

#### Failure Conditions

The gate fails if:

- Any behavior relies on implicit domain knowledge.
- Any canonical term lacks formal definition.
- Mechanical renaming breaks references.
- Any oracle becomes ambiguous after renaming.

---

## 7. Harness-Level Guarantees

If this document is satisfied:

- The documentation corpus functions as a **generic behavioral specification engine**.
- The project can serve as a reusable AI-agent training harness.
- The system can be implemented under arbitrary naming schemes.
- No semantic leakage from historical domain context is required.

---
