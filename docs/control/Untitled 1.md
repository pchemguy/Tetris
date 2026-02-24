## Normative rules you just defined (cleanly stated)

### 1) Family prerequisites (only place cross-family ordering is allowed)

* A **family** MAY declare prerequisite families.
* A **gate** MUST NOT declare prerequisites on gates in other families.
* If a gate requires something from another family, that requirement MUST be expressed as a **family prerequisite** (not as a gate dependency).

This makes “spiral” evolution possible by adding *new families or subfamilies* later, and pinning them to prior families.

---

### 2) G0 is unconditional, never named as a prerequisite

* `G0` is a **global unconditional prerequisite**.
* `G0` MUST NOT be listed as a prerequisite anywhere (neither by families nor by gates).
* Any work attempt (implementation or regression testing) presumes `G0` compliance by default.

So: **G0 exists, but never appears in dependency metadata**.

---

### 3) Oracle policy per gate: exactly one implementation oracle; optional regression oracle; same family only

Each gate MUST define:

* `implementation_oracle`: exactly one oracle `@DOC_ID` that is the proof obligation for the new/expanded behavior in this gate.

Each gate MAY define:

* `regression_oracle`: at most one oracle `@DOC_ID`.

Constraints:

* `regression_oracle`, if present, MUST belong to the **same family** as the gate.
* Gates MUST NOT reference oracles defined in other families (neither as implementation nor regression).

Implication: if a change risks breaking other families’ behavior, you handle that at the **family acceptance layer** (e.g., G5.2) or via **family prerequisites**, not by cross-family regression lists.

---

### 4) Each gate must explicitly declare its governing L3 scope documents (by @DOC_ID)

Each gate MUST declare `scope_specs`:

* a list of `@DOC_ID` references to all **L3 behavioral specs** that define the required behavior for that gate.

Constraints:

* `scope_specs` MUST be sufficient for a developer/agent to implement without “pulling in” unrelated specs implicitly.
* Refer to specs and oracles via `@DOC_ID` only (no filenames as authority).

(You can optionally add an L2 anchor per family, but the gate-level requirement is L3 + oracle.)

---

## Recommended structure in ACCEPTANCE_GATES.md

### A) Family header block (the only place cross-family prerequisites live)

For each family `Gk`, include a machine-readable (or at least strict) metadata block:

* `family_id`: `G2`
* `title`
* `prerequisite_families`: list of family IDs (optional, empty by default)
* `family_scope`: short prose describing architectural boundary
* `primary_oracles`: list of oracle doc IDs belonging to this family (optional but useful)

Example shape (illustrative):

```yaml
family_id: G2
title: Core Behavioral Completion
prerequisite_families: [G1]
```

No mention of G0.

---

### B) Gate block template (strict fields)

Each gate `Gk.n` contains:

* `gate_id`: `G2.2`
* `title`
* `scope_specs`: [`@DOC_ID`, ...]  ✅ required
* `implementation_oracle`: `@DOC_ID` ✅ required (exactly one)
* `regression_oracle`: `@DOC_ID` ✅ optional (at most one, same family)
* `mandatory_criteria`: bullets
* `prohibited`: bullets (optional but often useful)

Example shape:

```yaml
gate_id: G2.2
title: Gravity & Line Clearing
scope_specs: [@GAME_STATE, @GAME_RULES]
implementation_oracle: @ORACLE_CORE_GRAVITY_AND_LOCKING
regression_oracle: @ORACLE_CORE_GEOMETRY
```

That satisfies your “one implementation + optional regression, same family” rule.

---

## Spiral development under these constraints

Your example:

1. baseline core + classic shell complete (G2 + G4 + G5.2)
2. add colored tetrominoes (core semantic extension)
3. add ANSI renderer/presenter variant

With your rules, you don’t create a second sequence. You **add new gates inside existing families or add new families**:

* Colored tetrominoes: new gate under **G3** (core extensions/hardening) with:

  * `scope_specs` including the new/updated L3 specs (e.g., `@GAME_STATE` plus a new `@COLOR_MODEL` if you add it)
  * `implementation_oracle` in the **G3 family** (e.g., `@ORACLE_CORE_COLOR`)
  * optional `regression_oracle` also in G3 family

* ANSI renderer: either

  * (a) new gate under **G4** if you treat it as part of shell completion, or
  * (b) create a separate family (recommended) like `G4V` / `G6` for variants, **with prerequisite families** `[G4]` and `[G3]` if it depends on color.

No cross-family oracles needed. The family prerequisite handles it.

---

## One thing to decide (you’ve implied it, but it must be explicit)

When you say “gate MUST NOT declare regression oracles implemented in other families”, you’re implicitly choosing:

* **Gate-local regression is not global regression.**
* Full regression is validated only at **milestone acceptance gates** (your G5.*) or by running whole suites outside gate semantics.

That’s fine, but write it down:

> Cross-family regression is evaluated only at milestone acceptance gates (e.g., G5.1/G5.2) and is not expressed at per-gate granularity.

If you want, I can draft that paragraph in the same style as your current doc.

---
---


