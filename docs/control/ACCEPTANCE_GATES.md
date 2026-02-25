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
family_scope: Repository governance and specification compliance.
permitted_write_paths:
  - docs/reports/
prohibited_write_paths:
  - tetris/                        # No implementation allowed in G0
```

G0 establishes **repository-wide invariants** that apply to all subsequent families and gates.

G0:

* does not introduce implementation behavior,
* does not introduce test oracles,
* does not participate in dependency recursion,
* is always in force,
* is implicitly satisfied before any other gate may begin.

Violations of G0 invalidate the active gate immediately.

---

### G0.1 — Repository & Contract Compliance

```yaml
gate_id: G0.1
title: Repository & Contract Compliance
scope_specs: []
implementation_oracle: null
regression_oracles: []
```

#### Purpose

Establish structural correctness and specification awareness before implementation work begins.

---

#### Mandatory Criteria

##### Repository Structure

* Source code MUST reside exclusively under `tetris/src/tetris/`.
* Tests MUST reside under `tetris/tests/`.
* No implementation files may exist outside the declared package root.
* Directory layout MUST reflect component boundaries defined in `@DECOMPOSITION`.

---

##### Specification Awareness

Before any modification:

* The active family (`GX`) and gate (`GX.Y`) MUST be explicitly declared.
* All `scope_specs` defined by the active gate MUST be identified.
* The implementation oracle for the active gate MUST be identified from gate metadata.
* Regression oracle obligations (if any) MUST be identified.

No file may be created or modified unless permitted by:

* the active gate,
* the active family's `permitted_write_paths`.

---

##### Architectural Boundary Enforcement

* Component responsibilities MUST conform to `@DECOMPOSITION`.
* Architectural intent defined in `@ARCHITECTURE` MUST be preserved.
* Cross-component imports MUST obey declared interface constraints.
* Core must remain deterministic and side-effect free.
* Shell must not redefine core semantics.

---

### Prohibited Behavior

* Implementing behavior not defined in an explicitly referenced L3 specification.
* Inferring or inventing unspecified rules.
* Writing outside `permitted_write_paths`.
* Creating or modifying modules outside the active family's scope.
* Violating component boundary rules.
* Introducing optional or extension semantics without explicit gate authority.

---

### Continuous Enforcement

* G0 constraints apply to **all families and all gates**.
* G0.1 functions as a global compliance layer.

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
regression_oracles: []
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
regression_oracles: [ORACLE_CORE_SKELETON]
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
