---
doc_id: GATE_STRUCTURE_ORACLE_RESOLUTION
name: GATE_STRUCTURE_ORACLE_RESOLUTION.md
title: Gate Structure, Scope Semantics, and Oracle Resolution Model
status: active
authority: normative
references:
  - TEST_SUITE_LAYOUT
---

# Gate Structure and Oracle Resolution Model

**Gate Structure, Scope Semantics, and Oracle Resolution Model (Normative)**

---

## 1. Purpose

This document defines:

* the metadata structure and prose skeleton for gate families and individual gates,
* the relationship between gates and oracle documents,
* scope slicing semantics,
* regression and dependency resolution mechanics,
* static validity constraints for the gate system.

This document governs the **execution model of gates**.  

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

### 2.3 Canonical Gate Prose Skeleton (Normative)

This skeleton MUST be used for every numbered gate `GX.N`. Gates `GX.0` and `GX.R` are explicitly excluded.

`````markdown
### GX.N — <Short Title>

```yaml
gate_id: GX.N
title: <Short Title>
scope_specs: [DOC_A, DOC_B, DOC_C]
scope_notes:
  DOC_A:
    - "<slice hint>"
  DOC_B:
    - "<slice hint>"
implementation_oracle: ORACLE_...
regression_gates: [GX.K, GX.M]
```

#### 1. Purpose
...
#### 2. In-scope requirements (binding)
...
#### 3. Out-of-scope (binding)
...
#### 4. Mandatory postconditions
...
#### 5. Prohibited behavior
...
#### 6. Execution notes (non-normative)
...
`````

---

#### Gate Sections

##### 1. Purpose

One short paragraph describing the behavioral objective of this gate.

This section MUST:

* describe intent in domain terms,
* not redefine specification text,
* not introduce new requirements outside `scope_specs`.

---

##### 2. In-scope requirements (binding)

This section defines the exact normative slice of the referenced specifications.

It MUST:

* reference specific sections when possible (e.g., `GAME_STATE §5.2`),
* list the behaviors being implemented or enforced,
* clarify any narrowing relative to the full spec.

Format:

* Bullet list of concrete requirements.
* Each bullet must be testable.

Example:

* Spawn position is `(x=3, y=0)` with `Rotation.R0`.
* `next_piece` is drawn from the current bag head.
* No gravity progression is evaluated in this gate.

---

##### 3. Out-of-scope (binding)

This section MUST list explicitly excluded behaviors that appear in the referenced specs but are not implemented in this gate.

This prevents accidental semantic leakage.

Example:

* No collision detection beyond spawn-boundary validation.
* No gravity progression.
* No line clearing.
* No scoring updates.

If no exclusions are necessary, explicitly state so.

---

##### 4. Mandatory postconditions

Structural and semantic properties that MUST hold when the gate passes.

These are higher-level than oracle assertions and may include non-testable constraints.

Example:

* `step()` must remain deterministic.
* No shell modules are introduced.
* No state mutation outside allowed fields.

---

##### 5. Prohibited behavior

Explicit MUST NOT conditions.

Examples:

* Implementing adjacent mechanics (e.g., collision while implementing geometry).
* Introducing temporary logic that contradicts referenced specs.
* Weakening strictness requirements defined in `ERROR_HANDLING`.

This section protects architectural integrity.

---

##### 6. Execution notes (non-normative)

Optional. Used for:

* clarifying implementation ordering,
* advising test construction strategy,
* explaining known tricky interactions.

Must NOT contain new requirements.

---

#### Additional Constraints

##### A. No oracle semantics inside gate prose

Gate prose MUST NOT:

- restate oracle structure,
- define test IDs,
- reference oracle internal rule IDs.

Gates declare **which oracle**, not how it works.

---

##### B. Gate independence

A gate must be readable and understandable in isolation, given:

- its YAML header,
- its referenced specs.

It must not require reading previous gate prose to understand scope.

---

## 3. Scope Semantics

### 3.1 Authority Bound

`scope_specs` defines the **upper bound of normative authority** for a gate.

A gate MUST NOT strengthen, weaken, reinterpret, or override requirements in referenced specifications outside its declared slice.

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

To execute a numbered gate `GX.N`, the system MUST perform the following steps in order.

Execution is defined relative to a **single top-level invocation** (e.g., `run_gate("G2.3")`). All de-duplication rules apply within that invocation scope.

---

#### Step 1 — Family prerequisite resolution

If a family dependency gate `GX.0` exists:

* Execute `GX.0` exactly once for this family during the current top-level invocation.
* If already executed in this invocation, it MUST NOT be re-executed.

Dependency resolution semantics are defined in §5.2.

---

#### Step 2 — Regression resolution (same-family)

For each gate listed in `regression_gates`:

* Execute that gate **as if invoked directly**, including its own:
    * family prerequisite resolution,
    * regression resolution,
    * implementation oracle (if non-null).

##### Cycle safety

* A gate-resolution stack MUST be maintained during regression traversal.
* If a gate is encountered that already exists in the active resolution stack, execution MUST fail (configuration error: regression cycle).

This stack applies only to regression traversal within the same family.

---

#### Step 3 — Implementation oracle execution

If `implementation_oracle` is not null:

* Resolve its test directory per `@TEST_SUITE_LAYOUT`.
* Execute all tests under the mapped directory.

##### Oracle de-duplication rule

Within a single top-level invocation:

* If the same `implementation_oracle` is reached multiple times through regression or family recursion, it MUST be executed only once.
* Subsequent encounters of the same oracle MUST be treated as already satisfied.

Oracle de-duplication is scoped to the entire top-level run, not per gate.

---

#### Step 4 — Gate success conditions

A numbered gate `GX.N` passes if and only if:

* All prerequisite executions succeed,
* All regression gate executions succeed,
* The implementation oracle suite (if any) passes,
* The gate’s **In-scope requirements (binding)** are satisfied,
* No **Out-of-scope (binding)** violations are present.

The last two conditions are not automatically enforceable by this algorithm and require:

* oracle coverage, and/or
* review or meta-tests as defined by project policy.

---

#### Clarification of De-duplication Domains

The execution engine maintains separate internal controls:

1. **Family dependency execution control**
    * Ensures `GX.0` is executed once per family per top-level invocation.
2. **Regression cycle detection stack**
    * Prevents infinite recursion inside same-family regression chains.
3. **Oracle execution registry**
    * Ensures each oracle suite runs at most once per top-level invocation.

These controls are logically distinct and MUST NOT be conflated.

---

### 5.2 Family Dependency Gate `GX.0`

Families express cross-family dependencies exclusively via an optional gate `GX.0`.

`GX.0`:

```yaml
gate_id: G2.0
prerequisite_families: [G1]
```

Rules:

1. `GX.0` MUST include `gate_id` and `prerequisite_families` keys only.
2. `prerequisite_families` is the only mechanism for expressing family dependencies. `prerequisite_families` refers to family IDs only. For each family `GX` listed, the system MUST resolve and execute `GX.R`.
3. Executing `GX.0` means:
    * execute each referenced `{dep}.R` in listed order.
4. If a family has no dependencies, `GX.0` MUST NOT exist.

---

### 5.3 Family Regression Checkpoint `GX.R`

Each implementation family MUST define a final checkpoint gate `GX.R`.

`GX.R` has the following required YAML structure:

```yaml
gate_id: GX.R
```

`GX.R` MUST declare `gate_id` only.


---

#### Purpose

`GX.R` represents a **family coherence checkpoint**.

It verifies that:

* all numbered gates in the family remain passing,
* all associated oracle suites for that family pass collectively,
* all transitive family dependencies remain satisfied.

---

#### Execution Semantics

Executing `GX.R` within a single top-level invocation performs the following steps.

---

#### Step 1 — De-duplication guard

If this family’s `GX.R` has already been executed during the current top-level invocation:

* It MUST NOT be executed again.
* Execution immediately succeeds.

This prevents repeated execution during recursive dependency traversal.

---

#### Step 2 — Execute family’s numbered gate oracle suites

For every numbered gate in the family:

* Enumerate gates `GX.1` through `GX.LAST`.
* Order MUST be strictly ascending numeric by gate number.

For each numbered gate:

* If that gate defines a non-null `implementation_oracle`, execute that oracle per §5.1 Step 3.
* `GX.R` executes only implementation oracles owned by numbered gates. It does not re-execute their regression chains, as regression relationships are already validated at the time those gates passed.

Oracle de-duplication rules defined in §5.1 apply globally to the entire top-level invocation.

No regression traversal occurs at this stage — only the family’s own implementation oracles are executed.

---

#### Step 3 — Resolve cross-family dependencies

If a family dependency gate `GX.0` exists:

* For each family listed in `GX.0.prerequisite_families`, execute `{dep}.R` in listed order.

Dependency resolution MUST be recursive.

---

#### Step 4 — Cycle safety

Cross-family dependency recursion MUST be cycle-safe. If during recursive `{dep}.R` execution a family is encountered that is already active in the current recursion chain, execution MUST fail (configuration error: circular family dependency). This check is distinct from same-family regression cycle detection in §5.1.

---

#### Step 5 — Success Conditions

`GX.R` passes if and only if:

* All family oracle suites pass,
* All recursively required dependency family checkpoints pass,
* No cycle or structural violations are detected.

---

#### Clarification of Execution Domains

During a single top-level invocation:

1. **Family `.R` de-duplication**
    * Each family checkpoint executes at most once.
2. **Oracle de-duplication**
    * Each oracle suite executes at most once globally.
3. **Dependency recursion stack**
    * Ensures acyclic cross-family dependency traversal.
4. **Regression traversal stack**
    * Applies only to numbered gates (§5.1) and is independent of family recursion.

These mechanisms are independent and MUST remain logically separate.

---

#### Determinism Guarantee

Given:

* a static registry,
* deterministic test suites,
* no side effects outside declared write paths,

executing `GX.R` is deterministic and idempotent within a single invocation context.

---

## 6. Static Validity Constraints

The gate system is valid only if:

1. All `family_id` values are unique.
2. All `gate_id` values are unique.
3. Numbered gates in all families form strictly increasing contiguous sequences starting at 1.
4. Every `regression_gates` entry:
    * exists,
    * belongs to the same family,
    * has a strictly smaller numeric index.
5. Every referenced `{dep}.R` exists.
6. Dependency recursion is acyclic.
7. `scope_notes` keys (if present):
    * must appear in `scope_specs`,
    * must contain only string lists.

Violation invalidates the governance model.

---

## 7. Interpretation Rule

A gate represents:

> A bounded slice of normative authority and a scoped unit of work, proven by a specific oracle test suite, sequenced by explicit regression and dependency rules.

---

## 8. Gate Execution Algorithm (Non-normative)

This section provides **reference pseudocode** that operationalizes the normative rules in §§4–6.
If any discrepancy exists between this algorithm and the normative sections, **the normative sections control**.

### 8.1 Data structures (conceptual)

```text
GateMeta:
  gate_id: str
  title: str
  scope_specs: list[str]
  scope_notes: map[str, list[str]] | null
  implementation_oracle: str | null
  regression_gates: list[str]
  prerequisite_families: list[str] | null   # ONLY valid on GX.0

FamilyMeta:
  family_id: str
  title: str
  family_scope: str
  permitted_write_paths: list[str]
  prohibited_write_paths: list[str]

Registry:
  gates: map[str, GateMeta]       # gate_id -> meta
  families: map[str, FamilyMeta]  # family_id -> meta
```

Execution state for a single top-level run:

```text
ExecutionState:
  executed_family_dep_gate: set[str]     # family_id where GX.0 has been executed
  executed_oracles: set[str]             # oracle doc_id de-duplication
  active_gate_stack: set[str]            # gate_id cycle detection for regression resolution
  executed_family_r: set[str]            # family_id de-duplication for *.R recursion
```

### 8.2 Helper functions (conceptual)

```text
family_of(gate_id):
  return gate_id.split(".")[0]  # "G2.3" -> "G2"

gate_kind(gate_id):
  suffix = gate_id.split(".")[1]
  if suffix == "0": return "dep"
  if suffix == "R": return "r"
  return "n"  # numbered gate

resolve_test_dir(oracle_doc_id):
  # governed by TEST_SUITE_LAYOUT
  assert oracle_doc_id startswith "ORACLE_"
  return lowercase(oracle_doc_id without leading "ORACLE_")
```

### 8.3 Static validation pass (conceptual)

This pass enforces §6 constraints before execution.

```text
validate(registry):
  # uniqueness is assumed by map keys; must be ensured at parse time

  for each gate in registry.gates:
    # scope_notes keys subset of scope_specs
    if gate.scope_notes exists:
      assert every key in gate.scope_notes is in gate.scope_specs
      assert each value is a list of strings

    # regression_gates constraints (§6.3)
    for each rg in gate.regression_gates:
      assert rg exists in registry.gates
      assert family_of(rg) == family_of(gate.gate_id)
      assert rg is a numbered gate
      assert numeric(rg) < numeric(gate.gate_id)

    # GX.0 constraints (§5.2)
    if gate_kind(gate.gate_id) == "dep":
      assert gate has no keys other than:  
        - gate_id  
        - prerequisite_families
      assert gate.prerequisite_families exists and is list[str]
      for each dep_family in gate.prerequisite_families:
        assert dep_family exists in registry.families
        assert (dep_family + ".R") exists in registry.gates

    # GX.R constraints (§5.3)
    if gate_kind(gate.gate_id) == "r":
      assert gate has only:  
        - gate_id

  # dependency recursion must be acyclic (§6.5)
  assert family_dependency_graph_is_acyclic(registry)
```

### 8.4 Oracle execution (conceptual)

```text
execute_oracle(oracle_doc_id, state):
  if oracle_doc_id is null:
    return PASS
  if oracle_doc_id in state.executed_oracles:
    return PASS

  dir = resolve_test_dir(oracle_doc_id)         # TEST_SUITE_LAYOUT governs this
  ok = run_all_tests_under("tetris/tests/" + dir)

  if ok:
    state.executed_oracles.add(oracle_doc_id)
  return ok
```

### 8.5 Family dependency gate execution (GX.0)

Implements §5.2.

```text
execute_family_dep_gate_if_present(family_id, registry, state):
  if family_id in state.executed_family_dep_gate:
    return PASS

  dep_gate_id = family_id + ".0"
  if dep_gate_id not in registry.gates:
    state.executed_family_dep_gate.add(family_id)
    return PASS

  dep_gate = registry.gates[dep_gate_id]
  # For each prerequisite family, execute its .R gate in listed order
  for dep_family in dep_gate.prerequisite_families:
    ok = execute_family_r(dep_family, registry, state)
    if not ok:
      return FAIL

  state.executed_family_dep_gate.add(family_id)
  return PASS
```

### 8.6 Executing a numbered gate (GX.N)

Implements §5.1.

```text
execute_numbered_gate(gate_id, registry, state):
  assert gate_kind(gate_id) == "n"
  gate = registry.gates[gate_id]
  family_id = family_of(gate_id)

  # 1) family prerequisite resolution
  ok = execute_family_dep_gate_if_present(family_id, registry, state)
  if not ok:
    return FAIL

  # 2) regression resolution (depth-first), de-duped and cycle-safe
  ok = execute_regression_gates_for(gate_id, registry, state)
  if not ok:
    return FAIL

  # 3) implementation oracle for this gate
  ok = execute_oracle(gate.implementation_oracle, state)
  if not ok:
    return FAIL

  # 4) prose-defined postconditions & scope slicing are *not* automated here
  #    (must be enforced by review or explicit tests per your policy)

  return PASS
```

Regression resolution:

```text
execute_regression_gates_for(gate_id, registry, state):
  gate = registry.gates[gate_id]

  for rg_id in gate.regression_gates:
    ok = execute_numbered_gate_with_cycle_guard(rg_id, registry, state)
    if not ok:
      return FAIL

  return PASS

execute_numbered_gate_with_cycle_guard(gate_id, registry, state):
  if gate_id in state.active_gate_stack:
    return FAIL  # regression cycle in configuration
  state.active_gate_stack.add(gate_id)

  ok = execute_numbered_gate(gate_id, registry, state)

  state.active_gate_stack.remove(gate_id)
  return ok
```

### 8.7 Executing a family regression checkpoint (GX.R)

Implements §5.3.

```text
execute_family_r(family_id, registry, state):
  if family_id in state.executed_family_r:
    return PASS
  state.executed_family_r.add(family_id)

  # 1) execute all oracle suites owned by numbered gates in this family, ascending
  for each numbered gate GX.1..GX.LAST in ascending order:
    gate = registry.gates[that_gate_id]
    if gate.implementation_oracle is not null:
      ok = execute_oracle(gate.implementation_oracle, state)
      if not ok:
        return FAIL

  # 2) recursively execute dependency families’ .R checkpoints (if GX.0 exists)
  dep_gate_id = family_id + ".0"
  if dep_gate_id in registry.gates:
    dep_gate = registry.gates[dep_gate_id]
    for dep_family in dep_gate.prerequisite_families:
      ok = execute_family_r(dep_family, registry, state)
      if not ok:
        return FAIL

  return PASS
```

### 8.8 Top-level entrypoints (conceptual)

```text
run_gate(gate_id, registry):
  validate(registry)
  state = new ExecutionState()

  if gate_kind(gate_id) == "n":
    return execute_numbered_gate_with_cycle_guard(gate_id, registry, state)

  if gate_kind(gate_id) == "dep":
    return execute_family_dep_gate_if_present(family_of(gate_id), registry, state)

  if gate_kind(gate_id) == "r":
    return execute_family_r(family_of(gate_id), registry, state)

  return FAIL
```

---

### 8.9 Normative alignment checklist (non-normative)

This algorithm intentionally matches:

* **§4**: oracle → test directory mapping is delegated to `@TEST_SUITE_LAYOUT`.
* **§5.1**: regression gate execution is resolved by executing the referenced gates as if invoked directly (with de-dup + cycle safety).
* **§5.2**: cross-family prerequisites exist only via `GX.0`, and resolve to `{dep}.R`.
* **§5.3**: `GX.R` runs the family’s numbered-gate oracle suites and then recursively runs dependency family `.R` checkpoints.
* **§6**: static validity constraints are enforced up front.

---
