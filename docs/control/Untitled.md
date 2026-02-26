

~~~
## G0 — Governance & Compliance

```yaml
family_id: G0
title: Governance & Compliance
prerequisite_families: []
family_scope: Repository layout and documentation discovery.
permitted_write_paths: [docs/reports/]
prohibited_write_paths: [tetris/]
```

### G0.1 Repository & Contract Compliance

```yaml
gate_id: G0.1
title: Repository & Contract Compliance
scope_specs: [DOCUMENTATION_SYSTEM]
implementation_oracle: null
regression_oracles: []
mandatory_criteria:
  - Source code placed under `tetris/src/tetris/`
  - Tests placed under `tetris/tests/`
  - No source files outside the package path.
  - Agent must identify which test oracle(s) apply to the current target gate from gate metadata.
  - All normative docs are discovered and referenced.
prohibited:
  - Implementing behavior not specified in docs.
  - Guessing missing rules instead of stopping and escalating.
  - Violating component boundaries (logic leakage across core/runtime/input/render/CLI).
  - Implementing features without the corresponding spec (L3 artifact) being present and acknowledged.
  - Creating/modifying source modules out of scope for the current family/gate.
scope: `mandatory_criteria` and `prohibited` applies to all families/gates
```
~~~

* `family_id`: `G2`
* `title`
* `prerequisite_families`: list of family IDs (optional, empty by default)
* `family_scope`: short prose describing architectural boundary

### Cleaned-up `G2` proposal (minimal changes, but slightly more gates)

**G1 — Core Structural Readiness**

* `G1.1 Core Skeleton & Types`

  * implementation oracle: *(none, or a dedicated structural oracle if you want)*
  * L3 scope: `@CORE_API`, plus any state/type docs needed.

**G2 — Core Behavioral Completion**

1. `G2.1 Spawn Semantics`

   * implementation oracle: `@ORACLE_CORE_SPAWN`
   * regression: none
   * L3 scope: `@GAME_STATE`, `@GAME_RULES` (spawn rules), `@CORE_API`

2. `G2.2 Geometry & Rotations`

   * implementation oracle: `@ORACLE_CORE_GEOMETRY`
   * regression: `@ORACLE_CORE_SPAWN` (optional, but sane if spawn depends on piece definitions)
   * L3 scope: `@SHAPES_AND_ROTATIONS`, `@GAME_STATE`

3. `G2.3 Collision & Rejection`

   * implementation oracle: `@ORACLE_CORE_COLLISION`
   * regression: `@ORACLE_CORE_GEOMETRY`
   * L3 scope: `@GAME_STATE`, `@ERROR_HANDLING` (rejection policy)

4. `G2.4 Gravity & Locking`

   * implementation oracle: `@ORACLE_CORE_GRAVITY_AND_LOCKING`
   * regression: `@ORACLE_CORE_COLLISION` (and/or geometry if you prefer minimal)
   * L3 scope: `@GAME_RULES`, `@GAME_STATE`

5. `G2.5 Line Clearing`

   * implementation oracle: `@ORACLE_CORE_LINE_CLEAR`
   * regression: `@ORACLE_CORE_GRAVITY_AND_LOCKING` (and collision if necessary)
   * L3 scope: `@GAME_RULES`, `@GAME_STATE`

6. `G2.6 Scoring & Level Progression`

   * implementation oracle: `@ORACLE_CORE_SCORING`
   * regression: `@ORACLE_CORE_LINE_CLEAR`
   * L3 scope: `@GAME_RULES`, `@GAME_STATE`

7. `G2.7 RNG (7-bag)`

   * implementation oracle: `@ORACLE_CORE_RNG_7BAG`
   * regression: `@ORACLE_CORE_SPAWN` (and/or scoring only if RNG affects scoring in your model)
   * L3 scope: `@GAME_RULES`, `@CORE_API`, `@GAME_STATE`

8. `G2.8 Input Semantics`

   * **requires a new oracle**: `@ORACLE_CORE_INPUT_SEMANTICS` (recommended)
   * regression: collision + gravity (because inputs can affect both)
   * L3 scope: `@INPUT_MODEL`, plus `@GAME_STATE`, `@GAME_RULES` where needed

9. `G2.9 Game Over`

   * implementation oracle: `@ORACLE_CORE_GAME_OVER`
   * regression: `@ORACLE_CORE_SPAWN` + whichever mechanics can trigger top-row occupation
   * L3 scope: `@GAME_RULES`, `@GAME_STATE`, `@ERROR_HANDLING`

This is the **cleanest** mapping under your gate/oracle rules.

---

## How old gates map under the split model

* **Old Gate 1 (Core skeleton & types)** → `G1.1`
* **Old Gate 2 (Geometry & collision)** → `G2.2` + `G2.3`
* **Old Gate 3 (Gravity, locking, line clearing)** → `G2.4` + `G2.5`
* **Old Gate 4 (Scoring, levels, RNG)** → `G2.6` + `G2.7`
* **Old Gate 5 (Inputs, rotation, hard drop)** → `G2.8` *(and part of rotation semantics is exercised in collision/geometry gates, but the *input* contract must be owned by its gate)*
* **Old Gate 6 (Game over)** → `G2.9`
* **Old Gate 7 (Hold)** → `G3.1` with `@ORACLE_CORE_HOLD`
* **Old Gate 8 (Strictness)** → `G3.2` with `@ORACLE_CORE_INVARIANTS`
* **Old Gate 9 (Auditability)** → `G3.3` *(you likely need a dedicated oracle or an “audit gate” definition that references the whole family suite, depending on how you formalize it)*

---

