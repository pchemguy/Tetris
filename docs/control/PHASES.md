---
doc_id: PHASES.md
name: PHASES
title: Repository Evolution Phases
kind: control
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Allowed scope of work at each stage of repository evolution.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---
# PHASES

**Repository Evolution Phases (Normative)**

---

## 1. Purpose

This document defines the **evolution phases** of the repository.

Phases:

* define **scope boundaries** for repository evolution,
* constrain what kinds of changes are appropriate at a given stage,
* provide shared vocabulary for “where the project is”,
* prevent premature refactors, extensions, or generalization.

Phases are **not** acceptance criteria and **do not replace acceptance gates**.

> **Phases define *what kind of work is allowed*.
> Acceptance gates define *whether a specific implementation is correct*.**

---

## 2. Relationship to acceptance gates

* **Acceptance gates** (`ACCEPTANCE_GATES.md`) govern:
    * implementation order,
    * correctness,
    * verification requirements.
* **Phases** govern:
    * repository scope,
    * which subsystems may be introduced,
    * what kinds of refactors or extensions are appropriate.

A phase may span multiple gates, and a gate always executes *within* a phase.

---

## 3. Phase 0 — Contract spine and evaluation framework

### Scope

Establish the **normative documentation and evaluation system**.

### Allowed work

* Authoring and revising:
    * specifications,
    * architecture and decomposition,
    * acceptance gates,
    * test oracles,
    * project structure and conventions.
* Defining agent operating constraints.
* No functional implementation required.

### Prohibited work

* Implementing game logic.
* Implementing shell/runtime/renderer code.
* Writing tests not traceable to a test oracle.

### Typical gates involved

* Gate 0 only (discovery and compliance).

### Exit condition

* A third party can evaluate an agent’s behavior *purely* by reading docs, without relying on undocumented assumptions.

---

## 4. Phase 1 — Core-only MVP benchmark

### Scope

Implement the **pure deterministic Tetris core**.

This phase treats the core as a **standalone simulation engine**, independent of any runtime, UI, or I/O.

### Allowed work

* Implementing the core API and state machine.
* Writing tests mapped to `CORE_TEST_ORACLE.md`.
* Refactoring core internals to satisfy correctness and clarity.
* Optional core extensions explicitly covered by gates.

### Prohibited work

* Implementing rendering, runtime loops, CLI, or replay.
* Introducing I/O, timing, or environment dependencies.
* Adding behavior not specified in core contracts.

### Typical gates involved

* Gates 0–6 (mandatory)
* Gates 7–9 (optional core extensions)

### Exit condition

* Core gates pass.
* Core behavior is deterministic, testable, and spec-complete.

---

## 5. Phase 2 — System / shell completeness (baseline application)

### Scope

Wrap the core in a **minimal, deterministic shell** suitable for execution, inspection, and evaluation.

### Allowed work

* Implementing:
    * ASCII renderer,
    * scripted (virtual-time) runtime,
    * CLI entrypoints,
    * replay loading and execution.
* Writing shell-level tests mapped to component test oracles.
* Extending runtime configuration *only as specified*.

### Prohibited work

* Re-implementing core logic in shell components.
* Adding alternative renderers or UIs.
* Introducing real-time, interactive, or platform-specific behavior.

### Typical gates involved

* Gates 10–13 (plus Gate 0).

### Exit condition

* The system can be run, scripted, replayed, and audited deterministically
  without modifying the core.

---

## 6. Phase 3 — Optional extensions and hardening

### Scope

Improve robustness and feature completeness **without changing the baseline model**.

### Examples

* Optional core mechanics (e.g. hold/preview).
* Strictness and invariant enforcement hardening.
* Auditability improvements (serialization, logging).
* Debugging and inspection tools.

### Constraints

* All extensions must be explicitly specified.
* Determinism must be preserved.
* Baseline behavior must remain intact.

### Typical gates involved

* Gates 7–9 (if not completed earlier).
* Additional gates, if introduced.

### Exit condition

* Extended functionality exists without destabilizing prior guarantees.

---

## 7. Phase 4 — Variant shells and alternative interfaces

### Scope

Introduce **alternative renderers, runtimes, or interfaces** as *separate components*.

This phase includes what would normally be considered a “Phase-2 refactor” in less controlled projects.

### Examples

* Curses-based renderer.
* Graphical renderer (e.g. pygame).
* Web-based UI.
* Alternative runtime modes.

### Constraints

* Each variant must have:
    * its own specification document,
    * clear boundaries to the core,
    * optional acceptance gate and test oracle if evaluative.
* The canonical baseline (Phase 2) must remain unchanged.

### Exit condition

* Multiple shells coexist, all driven by the same core contracts.

---

## 8. Phase 5 — Benchmark scaling and agent evaluation

### Scope

Turn the repository into a **repeatable benchmark suite** for agentic development.

### Examples

* Standard replay corpora.
* Automated gate scoring.
* Agent transcript capture (plans, diffs, test mappings).
* Prompt comparison and regression analysis.

### Constraints

* No weakening of correctness requirements.
* Benchmark additions must not bias results toward specific agents.

### Exit condition

* Agents and prompting systems can be compared systematically using reproducible criteria.

---

## 9. Phase policy (binding)

* Advancing phases expands **allowed scope**, not correctness standards.
* No phase may invalidate guarantees established in earlier phases.
* When in doubt, **remain in the earlier phase**.

---

## 10. Audience note

* **AI agents**: Phases constrain *what you may attempt*. Violating phase scope is failure.
* **Human developers**: Phases provide guardrails for sustainable evolution. Expand phases deliberately, not reactively.

---
