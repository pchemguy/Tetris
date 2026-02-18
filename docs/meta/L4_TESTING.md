---
doc_id: L4_TESTING
name: L4_TESTING.md
title: L4 — Test Oracles (Proof Obligations)
kind: testing
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines mandatory correctness proofs and component-specific test oracles mapped to acceptance gates.
references:
  - ORACLE_CORE
  - ORACLE_SHELL_RENDERING
  - ORACLE_SHELL_RUNTIME
  - ORACLE_SHELL_CLI
  - ORACLE_SHELL_REPLAY
  - ORACLE_SHELL_CONFIG
---

# L4 — Testing

## Document Index

#### Core test oracle

**Directory**: `docs/testing/oracles/core/`

| Title                                | Filename         | Function / Role                                                       |
| ------------------------------------ | ---------------- | --------------------------------------------------------------------- |
| Composite Mandatory Core Test Oracle | `ORACLE_CORE.md` | Describes ORACLE_CORE decomposition and lists associated oracle files |

---

#### Shell-level test oracles

**Directory**: `docs/testing/oracles/shell/`

| Title                 | Filename                    | Function / Role                                     |
| --------------------- | --------------------------- | --------------------------------------------------- |
| Rendering Test Oracle | `ORACLE_SHELL_RENDERING.md` | Mandatory snapshot tests for ASCII rendering        |
| Runtime Test Oracle   | `ORACLE_SHELL_RUNTIME.md`   | Deterministic execution tests for scripted runtime  |
| CLI Test Oracle       | `ORACLE_SHELL_CLI.md`       | Mandatory behavioral tests for CLI commands         |
| Replay Test Oracle    | `ORACLE_SHELL_REPLAY.md`    | Deterministic replay validation and execution tests |
| Config Test Oracle    | `ORACLE_SHELL_CONFIG.md`    | Mandatory automated configuration handling tests    |

---

## Detailed description

Test oracle documents define **what must be proven** for an implementation to be considered correct. They answer questions such as:

* Which behaviors must be tested?
* What scenarios are mandatory?
* What level of determinism is required?
* What constitutes sufficient coverage for acceptance?

Test oracles are **normative**: passing ad-hoc or convenience tests is insufficient if oracle-mandated tests are missing. Each test oracle applies to:

* a specific component, and
* a specific acceptance gate (or small range of gates).

---

###  Core Test Oracle

####  `CORE_TEST_ORACLE.md` — Mandatory tests

**Role**  
Defines **what must be proven** for correctness.

**Contents**

- Explicit test oracles mapped to rules
- Required vs optional tests
- Minimum acceptable test set for MVP

**Usage**

- This document is the arbiter of correctness.
- Passing ad-hoc tests is insufficient if oracles are missing.
- Agents should generate tests directly traceable to this document.
- Applies exclusively to Acceptance Gates 1–6.

---

###  Shell Test Oracles

####  `RENDERING_TEST_ORACLE.md` — Renderer correctness

**Role**  
Defines the **mandatory automated tests** that the ASCII renderer must satisfy.

**Contents**

* Deterministic output requirements
* Exact board layout and border rules
* Cell symbol constraints
* Metadata line presence and ordering
* Game-over rendering behavior
* Snapshot (golden) test requirements

**Usage**

* Enforces strict compliance with `RENDERING_SPEC.md`.
* Enables byte-for-byte snapshot testing.
* Prevents rendering logic from drifting or becoming environment-dependent.
* Applies exclusively to **Acceptance Gate 10**.

---

####  `RUNTIME_TEST_ORACLE.md` — Scripted runtime correctness

**Role**  
Defines the **mandatory tests** for the scripted (virtual-time) runtime.

**Contents**

* One-tick-per-step execution guarantees
* Deterministic input application
* Rendering cadence requirements
* Early termination on game over
* Error propagation rules

**Usage**

* Ensures the runtime is suitable for deterministic evaluation and CI.
* Prevents re-implementation of core logic in the runtime layer.
* Applies exclusively to **Acceptance Gate 11**.

---

####  `CLI_TEST_ORACLE.md` — CLI behavior and robustness

**Role**  
Defines **mandatory behavioral tests** for the command-line interface.

**Contents**

* Command availability (`run`, `script`, `replay`)
* Exit code semantics
* Error propagation requirements
* Prohibitions on silent failure or logic leakage

**Usage**

* Keeps the CLI thin, declarative, and auditable.
* Ensures consistent behavior for humans and automation.
* Applies exclusively to **Acceptance Gate 12**.

---

####  `REPLAY_TEST_ORACLE.md` — Deterministic replay correctness

**Role**  
Defines **mandatory tests** for replay loading, validation, and execution.

**Contents**

* Replay file schema validation
* Strict input validation
* Deterministic tick-by-tick execution
* Final state determinism guarantees

**Usage**

* Enables exact reproduction of runs for debugging and agent evaluation.
* Prevents permissive or auto-correcting replay behavior.
* Applies exclusively to **Acceptance Gate 13**.

---
