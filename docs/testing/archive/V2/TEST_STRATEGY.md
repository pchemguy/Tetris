---
doc_id: TEST_STRATEGY
name: TEST_STRATEGY.md
title: Test Strategy
kind: meta
scope: global
status: active
authority: normative
phase_applies_to: all
gate_applies_to: all
url: https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# TEST_STRATEGY

## 1. Purpose

This document defines the governance rules for testing in the this repository.

The purpose of testing in this project is not merely to detect defects, but to:

- enforce architectural boundaries,
- validate deterministic simulation behavior,
- ensure documentation authority is respected,
- provide auditable evaluation signals for AI agents,
- prevent specification drift and guesswork.

This document defines **what correctness claims are allowed and how they are governed**.

It does not define repository layout, naming patterns, or pytest mechanics.  
Those are defined in `TESTING_CONVENTIONS.md`.

---

## 2. Testing Objectives

Testing must ensure:

1. The Core remains deterministic and pure.
2. Architectural boundaries defined in `ARCHITECTURE.md` and `DECOMPOSITION.md` are respected.
3. All correctness claims are grounded in authoritative documentation.
4. No behavior is silently invented or altered.
5. AI agent contributions remain auditable and non-speculative.

---

## 3. Test Layers and Assertion Policy

### 3.1 Unit Layer (Core)

Scope:

- Pure simulation logic.

Allowed assertions:

- Exact structural state equality.
- Deterministic invariants.
- Rule compliance defined in normative documents.

Prohibited:

- Rendering output.
- I/O behavior.
- Time-based assumptions.

---

### 3.2 Integration Layer (Runtime Coordination)

Scope:

- Interaction between core and orchestrator logic.

Allowed:

- Contract-level assertions.
- State transition correctness after input sequences.

Prohibited:

- Inspection of private internal state unless documented invariant.

---

### 3.3 System Layer (Optional)

Scope:

- Scripted or replay-driven full execution.

Allowed:

- Deterministic outcome validation.
- Replay equivalence assertions.

Prohibited:

- Real-time timing assertions.
- Terminal behavior assumptions.

---

## 4. Oracle Governance

### 4.1 Definition

An oracle is a normative correctness claim derived from authoritative documentation.

### 4.2 Authority Sources

Correctness authority derives from:

- PROJECT.md
- GAME_RULES.md
- GAME_STATE.md
- SHAPES_AND_ROTATIONS.md
- CORE_API.md
- ARCHITECTURE.md
- DECOMPOSITION.md

Tests must not invent behavior beyond these documents.

---

### 4.3 When Oracle Specs Are Required

Formal oracle specifications are required for:

- Core rule invariants
- State machine transitions
- Geometry and collision logic
- Replay determinism guarantees

---

### 4.4 Allowed Oracle Types

- Invariant-based
- Contract-based
- Deterministic replay equivalence
- State transition mapping

Golden-master snapshot tests are discouraged unless explicitly authorized.

---

## 5. Determinism Policy

The core simulation must be fully deterministic.

Tests must:

- not rely on wall-clock time,
- not rely on unseeded randomness,
- not depend on environment state.

Determinism violations are structural defects.

---

## 6. Change Control Policy

### 6.1 Code Changes

Code must change when:

- It violates documented rules.
- It violates architectural boundaries.
- It produces non-deterministic behavior.

---

### 6.2 Test Changes

Tests may change only when:

- They encode outdated documentation.
- They violate layer rules.
- They over-specify implementation details.

Test weakening without authority evidence is forbidden.

---

### 6.3 Oracle Spec Changes

Oracle specs may change only when:

- Normative documentation changes first.

Oracle changes require documentation updates before implementation.

---

## 7. Prohibited Practices

- Just-to-pass fixes.
- Suppressing failing tests.
- Weakening assertions without evidence.
- Encoding undocumented behavior.
- Silent cross-component coupling.

---

## 8. Execution Governance

- Full suite must pass before declaring any gate complete.
- Targeted suites may be used during development but are not substitutes for full validation.
- All failures must be classified before mutation.

---

## 9. Relationship to Other Documents

- `TESTING_CONVENTIONS.md` defines encoding mechanics.
- `TEST_PLAN.md` defines execution cadence.
- Oracle specifications define concrete correctness claims.
