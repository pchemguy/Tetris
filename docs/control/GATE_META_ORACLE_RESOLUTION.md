---
doc_id: GATE_META_ORACLE_RESOLUTION
name: GATE_META_ORACLE_RESOLUTION.md
title: Gate Metadata, Scope Semantics, and Oracle Resolution Model
status: active
authority: normative
references:
  - TEST_ORACLE_FORMAT_CONVENTION
  - TEST_SUITE_LAYOUT
---

# GATE_META_ORACLE_RESOLUTION

**Gate Metadata, Scope Semantics, and Oracle Resolution Model (Normative)**

---

## 1. Purpose

This document defines:

* the metadata structure for gate families and individual gates,
* the relationship between gates and oracle documents,
* scope slicing semantics,
* regression and dependency resolution mechanics,
* static validity constraints for the gate system.

This document governs the **execution model of gates**.  
It does not define oracle structure or test layout (see `@TEST_ORACLE_FORMAT_CONVENTION` and `@TEST_SUITE_LAYOUT`).

---

## 2. Data Model for Families and Gates

Each **family** and **gate** MUST be represented by embedded YAML metadata immediately following the family or gate header.

---

### 2.1 Family Metadata (Required Keys)

**Example family YAML header:**

```yaml
family_id: G2
title: Core Behavioral Completion
family_scope: Deterministic gameplay mechanics of the Core component.
permitted_write_paths:
  - tetris/src/tetris/
  - tetris/tests/
prohibited_write_paths:
  - docs/
```

Rules:

1. `family_id` MUST be unique.
2. Family metadata MUST NOT declare dependency information.
3. Family prerequisites, if any, MUST be expressed only through the presence and content of `GX.0` (see §5.2).

---

### 2.2 Gate Metadata (Required Keys)

**Example gate YAML header:**

```yaml
gate_id: G2.3
title: Collision & Rejection
scope_specs: [CORE_API, GAME_STATE, ERROR_HANDLING, SHAPES_AND_ROTATIONS]
scope_notes:
  CORE_API:
    - step(...) signature only
  GAME_STATE:
    - State fields and immutability relevant to collision
  ERROR_HANDLING:
    - Rejection semantics
  SHAPES_AND_ROTATIONS:
    - Canonical block definitions
implementation_oracle: ORACLE_CORE_COLLISION
regression_gates: [G2.2]
```

Rules:

1. `gate_id` MUST be unique.
2. `implementation_oracle` is either:
    * a single oracle `doc_id`, or
    * `null`.
3. `regression_gates` is a list of **gate_id strings**, not oracle ids.
4. `regression_gates` MUST reference only gates within the same family.
5. Every gate MUST declare `scope_specs` (L3 specification `doc_id`s).
6. A gate MAY declare `scope_notes`:
    * `scope_notes` maps `doc_id` → list of slice hints.
    * `scope_notes` is **non-authoritative**.
    * The gate body defines the binding scope (see §3).

---

## 3. Scope Semantics

### 3.1 Authority Bound

`scope_specs` defines the **upper bound of normative authority** for a gate.

A gate MUST NOT:

* introduce behavior not grounded in one of the listed specs, or
* modify requirements outside those specs.

---

### 3.2 Scope Slicing (Normative)

Because gates typically apply only portions of a specification:

1. Each gate MUST contain a prose section titled:
   `In-scope requirements (binding)`
   This section defines the exact slice of requirements active for the gate.
2. Each gate SHOULD also contain:
   `Out-of-scope (binding)`
   when adjacent behavior exists in the referenced specs.
3. If `scope_notes` conflicts with gate prose, the gate prose controls.
4. If a referenced spec lacks stable section anchors, the gate MUST define its scope slice via precise, testable language.

---

## 4. Oracle-to-Test Resolution

When an oracle is executed:

1. Determine test directory associated with the oracle per `@TEST_SUITE_LAYOUT`.
2. Execute all tests under:

```
tetris/tests/<derived_name>/
```

No implicit test discovery outside mapped directories is allowed.

---

## 5. Execution Semantics

### 5.1 Running a Numbered Gate `GX.N`

To execute a numbered gate:

1. **Family prerequisite resolution**
    * If `GX.0` exists, execute it first (see §5.2).
2. **Gate-local regression resolution**
    * **Regression gates**: For each gate `gid` listed in `regression_gates`, execute that gate first.
        * Load that gate’s metadata.
        * Include its implementation_oracle test suite if non-null.
        * Then recursively process its regression_gates (depth-first).
    * **De-duplication**: If the same oracle is reached multiple times, run it once.
    * **Cycle handling**: A visited set MUST be maintained to prevent infinite loops.
3. **Execute implementation oracle**
    * If `implementation_oracle` is not null:
        * Resolve its test directory per `@TEST_SUITE_LAYOUT`.
        * Execute all tests in that directory.
4. **Gate passes only if:**
    * all prerequisite executions pass,
    * implementation oracle tests (if any) pass,
    * the gate’s `In-scope requirements (binding)` are satisfied,
    * no `Out-of-scope (binding)` violations exist.

---

### 5.2 Family Dependency Gate `GX.0`

Families express cross-family dependencies exclusively via an optional gate `GX.0`.

`GX.0`:

```yaml
gate_id: G2.0
implementation_oracle: null
regression_gates: []
prerequisite_families: [G1]
```

Rules:

1. `GX.0` MUST NOT reference oracles.
2. `prerequisite_families` is the only mechanism for expressing family dependencies.
3. Executing `GX.0` means:
    * execute each referenced `{dep}.R` in listed order.
4. If a family has no dependencies, `GX.0` MUST NOT exist.

---

### 5.3 Family Regression Checkpoint `GX.R`

Each implementation family MUST define a final checkpoint `GX.R`.

`GX.R`:

```yaml
gate_id: G2.R
implementation_oracle: null
regression_gates: []
```

Execution semantics:

1. Execute the full family test suite:
    * For every numbered gate `GX.1..GX.LAST`:
        * If that gate defines an `implementation_oracle`, execute its oracle test suite.
    * Order MUST be ascending numeric.
2. If `GX.0` exists:
    * For each family dependency listed in `GX.0.prerequisite_families`, execute that family’s `.R` checkpoint recursively.
3. Cycle detection MUST be enforced.
4. Each family dependency should only be executed once.

`GX.R` represents a formal family coherence checkpoint.

---

## 6. Static Validity Constraints

The gate system is valid only if:

1. All `family_id` values are unique.
2. All `gate_id` values are unique.
3. Every `regression_gates` entry:
    * exists,
    * belongs to the same family,
    * has a strictly smaller numeric index.
4. Every referenced `{dep}.R` exists.
5. Dependency recursion is acyclic.
6. `scope_notes` keys (if present):
    * must appear in `scope_specs`,
    * must contain only string lists.

Violation invalidates the governance model.

---

## 7. Interpretation Rule

A gate represents:

> A bounded slice of normative authority and a scoped unit of work, proven by a specific oracle test suite, sequenced by explicit regression and dependency rules.

---
