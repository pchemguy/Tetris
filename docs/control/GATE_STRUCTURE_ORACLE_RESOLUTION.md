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

This skeleton MUST be used for every numbered gate `GX.N`.

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

To execute a numbered gate:

1. **Family prerequisite resolution**
    * If `GX.0` exists, execute it first (see §5.2).
2. **Gate-local regression resolution**
    * **Regression gates**: For each gate `gid` listed in `regression_gates`, execute that gate first.
        * Execute the referenced gate exactly as if it were invoked directly (including its own prerequisite resolution and regression resolution), maintaining a visited set to prevent cycles.
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
2. `prerequisite_families` is the only mechanism for expressing family dependencies. `prerequisite_families` refers to family IDs only. For each family `GX` listed, the system MUST resolve and execute `GX.R`.
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

## 8. Gate Execution Algorithm

> [!WARNING]
> 
> This algorithm has been generated by LLM and is not yet verified.

```
TITLE: Gate execution algorithm

DATA STRUCTURES
---------------
GateMeta:
  gate_id: str                  # e.g. "G2.3", "G2.0", "G2.R"
  title: str
  scope_specs: list[str]        # doc_id list (L3 upper bound)
  scope_notes: map[str, list[str]] | null
  implementation_oracle: str | null
  regression_gates: list[str]   # gate_id list, same-family only
  prerequisite_families: list[str] | null   # ONLY allowed on GX.0

FamilyMeta:
  family_id: str
  title: str
  family_scope: str
  permitted_write_paths: list[str]
  prohibited_write_paths: list[str]

Registry:
  gates: map[str, GateMeta]     # gate_id -> meta
  families: map[str, FamilyMeta]
  family_gate_numbers: map[str, list[int]]   # GX -> [1,2,3,...] (numbered only)
  family_has_dep_gate: map[str, bool]         # GX.0 exists?
  family_last_number: map[str, int]           # if needed (optional policy)

ExecutionState:
  executed_dep_gate: set[str]   # family_id where GX.0 already executed in this run context
  visited_gate_stack: set[str]  # for cycle detection within a single gate-resolution walk
  executed_oracles: set[str]    # de-dup oracle execution within one top-level run
  executed_family_r: set[str]   # de-dup family regression checkpoints within recursion

HELPERS
-------
parse_family_id(gate_id):
  # "G2.3" -> "G2", "G2.0" -> "G2", "G2.R" -> "G2"
  return gate_id.split(".")[0]

parse_gate_kind(gate_id):
  # returns ("dep", 0) for GX.0; ("r", None) for GX.R; ("n", N) for GX.N numbered
  suffix = gate_id.split(".")[1]
  if suffix == "0": return ("dep", 0)
  if suffix == "R": return ("r", null)
  else: return ("n", int(suffix))

resolve_test_dir_from_oracle(oracle_doc_id):
  # Per TEST_SUITE_LAYOUT: strip "ORACLE_", lower-case remainder, keep underscores.
  # "ORACLE_CORE_COLLISION" -> "core_collision"
  assert oracle_doc_id.startswith("ORACLE_")
  return lower(oracle_doc_id[len("ORACLE_"):])

run_tests_in_dir(dir_name):
  # Implementation-defined; must execute *only* tests under tetris/tests/<dir_name>/**.
  # Returns pass/fail.
  execute_pytest("tetris/tests/" + dir_name)
  return result

STATIC VALIDATION (must run before any execution)
-------------------------------------------------
validate_registry(reg):
  # Enforce §6 constraints minimally required for safe execution.

  # 1) Unique ids assumed by map keys; verify no duplicates at parse time.

  # 2) Regression gate constraints
  for each gate in reg.gates.values():
    fam = parse_family_id(gate.gate_id)

    # regression_gates exist, same family, smaller number
    (kind, n) = parse_gate_kind(gate.gate_id)
    for rg in gate.regression_gates:
      assert rg in reg.gates
      assert parse_family_id(rg) == fam

      (rg_kind, rg_n) = parse_gate_kind(rg)
      assert rg_kind == "n"    # regression_gates must point to numbered gates
      assert kind == "n"       # only numbered gates have regression_gates meaningfully
      assert rg_n < n

    # scope_notes keys subset of scope_specs
    if gate.scope_notes != null:
      for k in gate.scope_notes.keys():
        assert k in gate.scope_specs
        assert is_list_of_strings(gate.scope_notes[k])

    # GX.0 rules
    if kind == "dep":
      assert gate.implementation_oracle == null
      assert gate.regression_gates is empty
      # prerequisite_families present and list[str]
      assert gate.prerequisite_families is not null
      for dep_fam in gate.prerequisite_families:
        assert dep_fam in reg.families
        assert (dep_fam + ".R") in reg.gates   # required by §6.4

    # GX.R rules
    if kind == "r":
      assert gate.implementation_oracle == null
      assert gate.regression_gates is empty
      assert gate.prerequisite_families is null  # only GX.0 owns deps

  # 3) Acyclic family dependency graph (via GX.0 -> prerequisite_families)
  assert family_dependency_graph_is_acyclic(reg)

EXECUTION CORE
--------------
execute_oracle_if_needed(oracle_doc_id, state):
  if oracle_doc_id is null:
    return PASS
  if oracle_doc_id in state.executed_oracles:
    return PASS
  dir_name = resolve_test_dir_from_oracle(oracle_doc_id)
  ok = run_tests_in_dir(dir_name)
  if ok:
    state.executed_oracles.add(oracle_doc_id)
  return ok

execute_family_dep_gate_if_present(family_id, state, reg):
  # §5.2: execute GX.0 exactly once at start of working in family GX
  if family_id in state.executed_dep_gate:
    return PASS
  dep_gate_id = family_id + ".0"
  if dep_gate_id not in reg.gates:
    state.executed_dep_gate.add(family_id)  # mark as done: no deps
    return PASS

  dep_gate = reg.gates[dep_gate_id]

  # Derivation rule: for each dep family Gk, execute Gk.R
  for dep_fam in dep_gate.prerequisite_families:
    ok = execute_family_r(dep_fam, state, reg)
    if not ok:
      return FAIL

  state.executed_dep_gate.add(family_id)
  return PASS

execute_gate_numbered(gate_id, state, reg):
  # §5.1: numbered gate execution with prerequisite resolution + regression recursion + oracle
  assert gate_id in reg.gates
  gate = reg.gates[gate_id]
  (kind, n) = parse_gate_kind(gate_id)
  assert kind == "n"

  fam = parse_family_id(gate_id)

  # 1) family prerequisites
  ok = execute_family_dep_gate_if_present(fam, state, reg)
  if not ok:
    return FAIL

  # 2) gate-local regression resolution (depth-first over regression_gates)
  #    "execute referenced gate exactly as if invoked directly"
  ok = execute_regression_chain(gate_id, state, reg)
  if not ok:
    return FAIL

  # 3) execute implementation oracle
  ok = execute_oracle_if_needed(gate.implementation_oracle, state)
  if not ok:
    return FAIL

  # 4) non-test mandatory criteria / scope slice compliance
  #    NOTE: This algorithm cannot auto-validate prose requirements.
  #    Enforce via review checklist or dedicated meta-tests if you implement them.
  return PASS

execute_regression_chain(root_gate_id, state, reg):
  # Depth-first evaluation of regression_gates of the *root* gate,
  # where each referenced gate is itself executed like a numbered gate,
  # but WITHOUT re-running family prereqs repeatedly (already de-duped by state.executed_dep_gate).
  root = reg.gates[root_gate_id]

  for rg_id in root.regression_gates:
    ok = execute_gate_numbered_with_cycle_guard(rg_id, state, reg)
    if not ok:
      return FAIL
  return PASS

execute_gate_numbered_with_cycle_guard(gate_id, state, reg):
  if gate_id in state.visited_gate_stack:
    return FAIL  # configuration error: regression cycle within family
  state.visited_gate_stack.add(gate_id)

  ok = execute_gate_numbered(gate_id, state, reg)

  state.visited_gate_stack.remove(gate_id)
  return ok

execute_family_r(family_id, state, reg):
  # §5.3: family coherence checkpoint
  r_gate_id = family_id + ".R"
  assert r_gate_id in reg.gates

  if family_id in state.executed_family_r:
    return PASS
  state.executed_family_r.add(family_id)

  # 1) run family’s full oracle suite in ascending gate order
  numbered_ids = all_gate_ids_for_family_numbered_sorted(family_id, reg)
  for gid in numbered_ids:
    gate = reg.gates[gid]
    if gate.implementation_oracle is not null:
      ok = execute_oracle_if_needed(gate.implementation_oracle, state)
      if not ok:
        return FAIL

  # 2) if GX.0 exists, execute dependency families’ .R recursively
  dep_gate_id = family_id + ".0"
  if dep_gate_id in reg.gates:
    dep_gate = reg.gates[dep_gate_id]
    for dep_fam in dep_gate.prerequisite_families:
      ok = execute_family_r(dep_fam, state, reg)
      if not ok:
        return FAIL

  return PASS

TOP-LEVEL ENTRYPOINTS
---------------------
run_gate(gate_id, reg):
  validate_registry(reg)
  state = ExecutionState(
    executed_dep_gate = empty_set(),
    visited_gate_stack = empty_set(),
    executed_oracles = empty_set(),
    executed_family_r = empty_set()
  )

  (kind, n) = parse_gate_kind(gate_id)
  if kind == "n":
    return execute_gate_numbered_with_cycle_guard(gate_id, state, reg)
  if kind == "dep":
    # Explicitly runnable, but normally called implicitly.
    fam = parse_family_id(gate_id)
    return execute_family_dep_gate_if_present(fam, state, reg)
  if kind == "r":
    fam = parse_family_id(gate_id)
    return execute_family_r(fam, state, reg)

  return FAIL

NOTES / REQUIRED BEHAVIORAL GUARANTEES (non-code)
-------------------------------------------------
1) "De-duplication" in §5.1 is implemented by state.executed_oracles.
2) Family dep gate GX.0 is executed once per family per run_gate(...) invocation.
3) Regression cycles within a family fail via visited_gate_stack.
4) Cross-family dependency cycles fail in validate_registry(reg).
5) Scope slicing enforcement is explicitly NOT automated here; it requires:
   - human review checklists, or
   - meta-tests that validate required invariants implied by gate prose.
```

---