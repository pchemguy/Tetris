---
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69a56034-d3a0-838e-8878-343fa53eb6da
---
# Deterministic AI Coding Framework

You’re *very* close to the objective you described. The conceptual architecture is correct (layered docs → gates → oracles → tests → reports → completion flags), and you already have the two hardest prerequisites in place:

* **A machine-checkable documentation graph** (`DOC_SCHEMA`, `DOC_INVENTORY`) with stable IDs.
* **A proof-obligation system** (oracle docs + strict oracle→pytest mapping rules).

What’s missing is not “more prose specs”; it’s a small set of **normative control-plane artifacts** that make the process *scriptable, resumable, and unambiguous* under deterministic orchestration.

Below is an assessment of current state vs. required objective, followed by concrete deficiencies and how to close them.

---

## Assessment: are you amenable to deterministic, stepwise agent driving?

### You already have the key “static” primitives

1. **Document identity & closure**
    * `DOC_ID` + YAML `references` gives you a deterministic dependency graph.
    * `DOC_INVENTORY.json` gives you a canonical discovery surface.
    * This is exactly what deterministic context construction needs.
2. **Validation partitioning**
    * Oracle documents define correctness partitions.
    * `TEST_SUITE_LAYOUT` / `TESTING_CONVENTIONS` give a deterministic mapping from an oracle to a test directory (and from CASE_IDs to pytest tests).
    * This is exactly what deterministic regression selection needs.
3. **Evidence recording**
    * You have an L5 reporting layer and a proposed `completed.flag`.
    * This is exactly what deterministic progression needs.

### The gap: you don’t yet have a fully specified “control plane”

Right now, the loop is *described* in your notes, but it isn’t yet *normatively pinned down* as:

* a state machine (gate lifecycle),
* a canonical machine-readable gate inventory,
* a canonical algorithm for closure construction,
* a canonical report format and resumption protocol,
* a canonical “agent run context contract” (ENGINEER AGENT CONTEXT).

Those are the pieces that turn “this could be orchestrated deterministically” into “it **will** be orchestrated deterministically, with no discretion.”

---

## Deficiencies to address (and why they matter)

### 1) Missing: a canonical machine-readable acceptance-gate inventory artifact

You mention “probably from JSON or YAML file from a predefined location,” but the objective requires this to be explicit and normative.

**Add:**

* `docs/control/ACCEPTANCE_GATES.json` (or `GATE_INVENTORY.json`) + schema:
    * stable gate IDs (`G1.1`, `G2.0`, …)
    * total ordering rules (or partial order + deterministic tie-break)
    * dependencies (gate and family)
    * implementation oracle for the gate
    * regression gates list (the corrected `regression_gates` concept you already identified)
    * “closure roots” (optional: list of doc_ids always included for that gate family)

Why: deterministic orchestration must not scrape human prose or infer order from filenames.

### 2) Missing: a normative “Gate Lifecycle and State” model

You currently rely on filesystem presence and `completed.flag`. That’s good, but incomplete for resumability.

**Define a gate state machine**, minimally:

* `NOT_STARTED` (no directory)
* `IN_PROGRESS` (dir exists, no completion)
* `BLOCKED` (dir exists + `blocked.flag` + reason file)
* `COMPLETE` (completion flag exists)
* optionally `INVALIDATED` (complete but later found inconsistent with updated norms; this matters once specs evolve)

Also define required evidence artifacts per state, e.g.:

* `run_manifest.json` (what suite was run, command, env, commit hash)
* `results.json` (pass/fail, failing CASE_IDs)
* `summary.md` (human-readable synopsis)
* `completed.flag` / `blocked.flag`

Why: “resume without human intervention” is impossible to implement deterministically if “what happened last time” is not normalized.

### 3) Missing: a canonical “Context Construction Contract” for ENGINEER AGENT CONTEXT

You describe what context should contain, but orchestration needs a *contract*:

* what the orchestrator provides to the agent,
* what the agent may assume,
* what is forbidden (no implicit repo browsing beyond declared closure? allowed reading source tree? allowed running scripts?).

**Add a normative artifact** such as:

* `docs/control/AGENT_CONTEXT_CONTRACT.md`
* and preferably a machine-readable:
    * `docs/control/AGENT_CONTEXT.schema.json`
    * `docs/control/AGENT_CONTEXT.example.json`

Include fields like:

* target gate id
* gate dependencies (expanded)
* doc closure list (explicit paths resolved from DOC_INVENTORY)
* regression test directories to run
* required outputs (report locations + flag)
* deterministic constraints (seed policy, time policy, no network, etc.)
* escalation rules

Why: without this, different orchestrators (or different agent skills) will build different “contexts” and you lose determinism.

### 4) Missing: a normative closure algorithm (the “closure semantics” must be pinned down)

You sketched a closure derivation. Good. Now it needs to be made normative because otherwise closure is discretionary.

You need to specify, precisely:

* Closure root set per gate:
    * always-include docs (L0/L1/L2 anchors + `ACCEPTANCE_GATES` + `TEST_*` conventions)
    * gate-specific spec roots (usually via oracle `references`)
* Traversal rules:
    * follow YAML `references` recursively
    * include or exclude certain kinds (`ORACLE_*` handling)
    * whether to include informative docs
* Stopping rules:
    * layer cutoffs (e.g., include L3/L4, exclude L5 except prior reports)
    * exclude archived/non-normative zones by default
* Deterministic ordering:
    * sort by (`layer`, `path`, `doc_id`) or similar

Why: deterministic orchestration depends on the closure being reproducible byte-for-byte.

### 5) Missing: a single canonical “Orchestration Protocol” document

Right now, pieces are spread across `DOCUMENTATION_SYSTEM`, testing docs, and notes.

You want one normative control doc that states the end-to-end loop, something like:

* `docs/control/DETERMINISTIC_AGENT_ORCHESTRATION.md`

It should define:

* how “next gate” is selected (including resumption precedence)
* the mandated execution sequence:
    1. compute closure
    2. run pre-regression suites
    3. implement
    4. run implementation suite
    5. run post-regression suites (optional but you mentioned it)
    6. write reports
    7. set flag
* what counts as “pass” (no xfail? no skipped? explicit policy)
* how failures are recorded
* when to escalate and how (write `blocked.flag` + reason, never silently proceed)

Why: this is the missing “roadmap-as-algorithm.”

### 6) Missing: deterministic test execution and reporting formats (machine-readable)

You have a directory convention, but not yet a canonical **report schema**.

Add:

* `docs/meta/TEST_RUN_REPORT.schema.json`
* require each run to emit `results.json` in a fixed shape:
    * suites executed
    * counts
    * failing tests + CASE_ID extraction where applicable
    * environment fingerprint (python version, dependency lock hash)

Why: resumption and automated diagnosis require machine-readable outcomes.

### 7) Potential mismatch: current test-root paths in your notes vs repo reality

Your notes say `tetris/tests/<scope>_<topic>/` (good), but some snippets also show `tetris/tests/core/` style. You need to pick one as **normative** and make everything else derived or deprecated.

Given you already have `TEST_SUITE_LAYOUT` with `tetris/tests/<scope>_<topic>/`, that should be the canonical truth.

Why: deterministic selection of regression suites depends on path normalization having zero ambiguity.

---

## What you *do* have “enough of” already

* The layered doc system concept is strong enough to generalize into the framework you want.
* The oracle format convention is already at the right level (it’s a governance primitive, not Tetris-specific).
* The inventory concept (`DOC_INVENTORY`) is exactly what deterministic closure builders need.

So: you’re not missing conceptual pillars; you’re missing **3–6 control-plane specs + 2 machine-readable schemas**.

---

## Minimal set of additions to make this fully deterministic

If you want the smallest “make it real” increment, implement these as normative docs/artifacts:

1. **`DETERMINISTIC_AGENT_ORCHESTRATION.md`** (the loop, state machine, selection rules)
2. **`ACCEPTANCE_GATES.json` + schema** (canonical inventory, no scraping)
3. **`AGENT_CONTEXT.schema.json` + example** (ENGINEER AGENT CONTEXT contract)
4. **`CLOSURE_CONSTRUCTION.md`** (normative closure semantics)
5. **`TEST_RUN_REPORT.schema.json`** (reports are machine-readable)
6. **Gate lifecycle flags + required files spec** (formalize `completed.flag`, `blocked.flag`, plus `run_manifest.json`)

Everything else can evolve later.

---

## If the project is “in a good state,” what is the framework?

Your framework, generalized beyond Tetris, is essentially:

* A **normative documentation graph** (machine-discoverable, stable identifiers)
* A **work partitioning DAG** (gates/families + explicit dependencies)
* A **proof obligation graph** (oracles) orthogonal to the work DAG
* A **deterministic closure operator** (docs + tests needed for a gate)
* A **deterministic orchestrator** (select next gate, run loop, emit evidence)

You already have 2.5/5 of those nailed. The rest is control-plane formalization.

---

## Recommended next step (no waiting, no handwaving)

Take your current “Early Notes” algorithm and promote it into a **single normative orchestration spec** plus **two schemas**:

* `ACCEPTANCE_GATES.json` (inventory) + schema
* `AGENT_CONTEXT.json` (run context) + schema

Once those exist, everything else (scripts/skills) becomes an implementation detail.

If you want, paste your current `ACCEPTANCE_GATES.md` / gate-family definitions (even partial), and I’ll translate them into a clean `ACCEPTANCE_GATES.json` shape + schema that preserves your existing concepts (`implementation_oracle`, `regression_gates`, family deps, etc.) without introducing new semantics.
