---
doc_id: PHASES
name: PHASES.md
title: Repository Evolution Phases
status: active
authority: normative
description: Allowed architectural scope at each stage of repository evolution.
---

# PHASES

**Repository Evolution Phases (Normative)**

---

## 1. Purpose

This document defines the **allowed architectural scope** of the repository at each stage of evolution.

Phases:

- constrain which **domains** may be modified or introduced,
- prevent premature expansion into later subsystems,
- define repository maturity boundaries.

> Phases define *what may be worked on*.
> Acceptance gates define *what must be proven correct*.

---

## 2. Phase Definitions

| Phase | Name                           | Primary Domain    | Scope                                                                                             |
| ----- | ------------------------------ | ----------------- | ------------------------------------------------------------------------------------------------- |
| 0     | Documentation & Governance     | `DOC_INFRA`       | Establish the documentation system, architecture definitions, acceptance gates, and test oracles. |
| 1     | Core Deterministic Simulation  | `CORE`            | Implement the pure deterministic simulation core as a standalone engine.                          |
| 2     | Baseline Shell                 | `SHELL_BASELINE`  | Wrap the deterministic core with a minimal deterministic execution shell.                         |
| 3     | Extensions & Hardening         | `CORE_EXTENSIONS` | Introduce optional mechanics and robustness improvements that preserve baseline semantics.        |
| 4     | Variant Interfaces             | `VARIANTS`        | Introduce alternative interfaces or runtime variants while preserving baseline contracts.         |
| 5     | Benchmark & Evaluation Scaling | `BENCHMARK`       | Transform the repository into a structured evaluation benchmark.                                  |

Architectural domains are defined in `ACCEPTANCE_GATES.md`. Each phase has a primary domain as indicated in the table. All primary domains of earlier phases are also allowed. For example, `Phase 2` focuses on `SHELL_BASELINE` with `DOC_INFRA` and `CORE` also being allowed.

**Rules:**

1. Domain permissions are cumulative.
2. A later phase may introduce new domains.
3. No phase may remove domains permitted in earlier phases.
4. Work in a domain not allowed in the current phase is a violation.
5. A phase permits modification of allowed domains but does not require it.

---

## 3. Phase Policy

- Phases constrain architectural scope only.
- Acceptance gates remain the sole authority for correctness.
- When uncertain, remain in the earlier phase.
- Expanding into a new domain requires explicit phase advancement.

---

## 4. Audience

AI agents must determine the current phase and restrict changes to allowed domains.
Human developers must advance phases deliberately.

