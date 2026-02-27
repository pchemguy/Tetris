---
doc_id: ACCEPTANCE_GATES
name: ACCEPTANCE_GATES.md
title: Milestone Acceptance Gates
status: draft
authority: normative
description: Milestone-based acceptance criteria and progression rules.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# ACCEPTANCE GATES

**Milestone Acceptance Gates for Agentic Development**

## 1. Purpose and acceptance semantics

This document defines **acceptance gates** for this project. Acceptance gates are **ordered, testable milestones** that evolve the repository from one well-defined state to the next.

Acceptance gates:

- constrain development and agent scope,
- prevent premature feature creep,
- provide objective “done / not done” criteria.

A gate is considered **passed** only when:

1. All **mandatory scope** defined for that gate is implemented, and
2. All **mandatory proofs** required by that gate pass, as defined by its associated **test oracle(s)**.

Gate rules:

- **Cumulative** — Each gate subsumes all prior gates. Earlier gates must remain passing.
- **Minimal-scope** — Each gate advances the system by the smallest practical, independently testable step.
- **Testable** — A gate’s scope must be verifiable through explicit proof obligations.
- **Strict** — Failing any criterion fails the gate. “Almost correct” does not pass.
- **Non-speculative** — Behavior not explicitly required is not credited. Behavior explicitly prohibited fails the gate.

An agent or developer may not advance to a later gate unless **all criteria of the current gate are satisfied**.

---

## 2. Organization model

### 2.1 Governance hierarchy

Acceptance governance is structured as:

**Gates → Gate Families → Domains**

Each level serves a distinct purpose:

- **Gate**  
  The smallest testable incremental milestone. A gate defines a concrete scope delta and its associated proof obligations.
- **Gate Family**  
  An ordered set of related gates with a shared architectural objective. Families organize gates along architectural boundaries defined in `@DECOMPOSITION`.
- **Domain**  
  A higher-level architectural grouping derived from `@DECOMPOSITION`. Domains group architecturally related families and define structural development blocks.

Domains define architectural scope and are referenced by `@PHASES` to constrain allowed development areas.

This hierarchy ensures that:

- Implementation proceeds in alignment with architectural design,
- Structural boundaries defined in `@DECOMPOSITION` are respected,
- Development workflow remains scalable as the project grows.

---

### 2.2 Oracle policy for gates

Test oracles define the proof obligations required to accept a gate.

The following rules apply:

- A gate MAY require multiple test oracles.
- Exactly **one** oracle must be designated as the **primary oracle** for that gate. The primary oracle covers the newly introduced or expanded behavior.
- Any additional oracles listed by the gate must be **regression oracles** introduced by earlier gates and re-run because the new change may affect previously validated behavior.
- Gates must not introduce “use-once” oracles. Oracles are reusable proof artifacts and remain valid as the system evolves.

No gate may rely on undefined or implicit proof criteria. All acceptance conditions must be traceable to explicit oracle documents.

---

## G0 — Governance & Compliance

```yaml
family_id: G0
title: Governance & Compliance
prerequisite_families: []          # Unconditional root family
family_scope: Repository invariants, specification authority boundaries, and architectural compliance.  
permitted_write_paths:
  - docs/reports/
prohibited_write_paths:
  - tetris/                        # No implementation allowed in G0
```

G0 establishes **repository-wide invariants** that apply to all subsequent families and gates.

G0:

* does not
    * introduce implementation behavior,
    * introduce test oracles,
    * participate in dependency recursion,
* is always in force,
* is implicitly satisfied before any other gate may begin.

Violations of G0 invalidate the active gate immediately.

---

## G0.1 — Repository & Contract Compliance

```yaml
gate_id: G0.1
title: Repository & Contract Compliance
scope_specs: []
implementation_oracle: null
regression_gates: []
```

---

### 1. Purpose

Establish repository invariants, specification awareness, and architectural boundary enforcement that govern all subsequent families and gates.

This gate introduces no implementation behavior.
It defines global compliance constraints.

---

### 2. In-scope requirements (binding)

The following requirements apply before and during execution of any other gate.

#### Repository structure invariants

* All implementation source code MUST reside exclusively under `tetris/src/tetris/`.
* All test code MUST reside exclusively under `tetris/tests/`.
* No implementation modules may exist outside the declared package root.
* The directory layout MUST conform to component boundaries defined in `@DECOMPOSITION`.

#### Family reporting invariants

Every family `GX` is **implicitly** authorized to write report artifacts under:

`docs/reports/GX/`

- If the directory does not exist, it MUST be created before executing any numbered gate in that family.
- This implicit write permission applies to all families and does not need to be declared in family YAML `permitted_write_paths`.

For every executed gate `GX.N`:

- Execution reports MUST be written under:

`docs/reports/GX/GX.N/`

- This directory MUST be created if it does not exist.
- No report artifacts may be written outside this directory.

Report artifacts include (but are not limited to):

- test execution summaries,
- failure reports,
- structured result files,
- diagnostic logs,
- regression outcome summaries.

#### Gate awareness and scope discipline

Before creating or modifying any file:

* The active family (`GX`) and active gate (`GX.Y`) MUST be explicitly identified.
* The active gate’s `scope_specs` MUST be enumerated and treated as the upper bound of normative authority.
* The active gate’s `implementation_oracle` MUST be identified (if non-null).
* The active gate’s `regression_gates` obligations MUST be identified and understood.
* No file may be created or modified unless permitted by:
    * the active gate definition,
    * the active family’s `permitted_write_paths`, or
    * or the implicit reporting path.

#### Architectural boundary compliance

* Component responsibilities MUST conform to `@DECOMPOSITION`.
* Architectural intent defined in `@ARCHITECTURE` MUST be preserved.
* Cross-component imports MUST respect declared interface constraints.
* The Core component MUST remain deterministic and free of UI or runtime side effects.
* Shell components MUST NOT redefine, override, or reinterpret Core semantics.

---

### 3. Out-of-scope (binding)

* No gameplay mechanics are introduced in this gate.
* No new specifications are defined.
* No oracle tests are executed.

---

### 4. Mandatory postconditions

* Repository structure satisfies declared invariants.
* No unauthorized files exist.
* The active gate is explicitly declared before any modification.
* No architectural boundary violations are present.
* No code exists outside allowed write paths.

---

### 5. Prohibited behavior

* Implementing behavior not grounded in explicitly referenced L3 specifications.
* Inferring, guessing, or inventing unspecified rules.
* Writing outside
    * `permitted_write_paths` or
    * `docs/reports/{FAMILY_ID}/{GATE_ID}/`.
* Creating or modifying modules outside the active family’s scope.
* Violating component boundaries.
* Introducing optional, extension, or shell semantics without explicit gate authority.

---

### 6. Execution notes (non-normative)

G0.1 functions as a continuous compliance layer. Its constraints apply transitively to all families and gates. Violation of G0.1 invalidates the currently executing gate.

---

## G1 — Core Structural Readiness

```yaml
family_id: G1
title: Core Structural Readiness
prerequisite_families: []
family_scope: Establish an importable Core package and baseline public API surface.
permitted_write_paths:
  - tetris/src/tetris/
  - tetris/tests/
prohibited_write_paths:
  - docs/
```

---

G1 is the first implementation family.

G1:

* begins from an empty implementation tree,
* establishes the Python package structure,
* establishes the public Core API surface,
* introduces no gameplay behavior,
* introduces no shell components.

G1 defines structure only.

---

### G1.1 — Package Skeleton

```yaml
gate_id: G1.1
title: Package Skeleton
scope_specs:
  - CORE_API
implementation_oracle: ORACLE_CORE_SKELETON
regression_gates: []
```

---

#### Purpose

Create the importable package namespace from an empty source tree.

---

#### Start State

* `tetris/src/tetris/` MAY be empty or may not exist.

---

#### Mandatory Postconditions

* Directory `tetris/src/tetris/` exists.
* File `tetris/src/tetris/__init__.py` exists.
* The package is importable:
    * `import tetris` succeeds when installed in editable mode.
* No shell modules exist.
* No gameplay logic exists.

---

### G1.2 — Core API Skeleton & Types

```yaml
gate_id: G1.2
title: Core API Skeleton & Types
scope_specs: [CORE_API, GAME_STATE, ERROR_HANDLING]
implementation_oracle: ORACLE_CORE_API_TYPES
regression_gates: [G1.1]
```

---

#### Purpose

Create the Core module and define the public API surface exactly as specified, without introducing gameplay semantics.

#### Mandatory postconditions

Import surface:

* `import tetris.core` succeeds.
* All public symbols required by `@CORE_API` exist and are importable **from `tetris.core` and `tetris`** exactly as specified (names, enum members, dataclass names, and public function names).
* Package-level API surface MUST conform `@CORE_API`.

Type and structural readiness:

* The required enums and dataclasses defined by `@CORE_API` exist with the required fields.
* `new_game(config)` exists and returns a structurally valid `GameState` (field presence and basic structural invariants only).
* `step(state, inputs, config)` exists and returns a `StepResult` with `state: GameState` and `events: tuple[...]`.

Signature compliance:

* `new_game` and `step` MUST conform to the signatures defined in `@CORE_API`.

Strictness (structural only):

* Structural errors required by `@ERROR_HANDLING` for this stage MUST NOT be silently suppressed.
  (What is “in scope” for structural error handling is defined by `@ORACLE_CORE_API_TYPES`.)

#### Allowed behavior

`step(...)` MAY:

* ignore inputs,
* return a semantically unchanged state **because gameplay semantics are not implemented yet**,
* update only fields that are explicitly permitted by the stub policy in `@ORACLE_CORE_API_TYPES` (if any counters are permitted at this stage, the oracle must state that allowance explicitly).

#### Prohibited

`step(...)` MUST NOT implement any gameplay semantics, including:

* movement
* rotation
* gravity
* collision
* locking
* line clearing
* scoring
* RNG / 7-bag
* game-over transitions

Also prohibited:

* introducing any shell components
* implementing “half behavior” (e.g., move works but collision doesn’t)

---

### G1.R — Completion Boundary

G1 is complete when:

* G1.1 passes,
* G1.2 passes,
* and no prohibited behavior exists.

G1.R means: run the full G1 family test suite (all tests introduced for G1.1–G1.2).

---
