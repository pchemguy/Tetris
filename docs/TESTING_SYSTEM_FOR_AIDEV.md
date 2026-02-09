---
name: TESTING_SYSTEM_FOR_AIDEV.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# Testing System for AI-Assisted Development

## Objectives

This testing system is designed to make AI-assisted development:

* **Auditable**: correctness claims have traceable authority.
* **Refactor-safe**: tests don’t accidentally encode implementation details.
* **Non-speculative**: changing tests requires evidence; “just-to-pass” is structurally blocked.
* **Composable**: different skills can operate without stepping on each other.

The core mechanism is **layer separation**:

* Strategy defines **how** correctness may be asserted.
* Oracle specs define **what** correctness means, per behavior.
* Oracle implementations execute those specs as runnable tests.

---

# Layer 1 — Test Strategy (Governance)

## Artifact

**`TEST_STRATEGY.md`** (project-wide, high-level, non-executable)

## Scope

* **One per project** (single authoritative strategy).
* Applies to *all* tests, oracle specs, and test execution.
* Changes slowly; revisions are design decisions.

## Purpose

`TEST_STRATEGY.md` is the **governance document** that constrains:

* what kinds of tests are allowed,
* what kinds of oracles are legitimate,
* where tests live,
* how oracle specs are authored,
* how oracle specs are translated into pytest,
* how to arbitrate “test vs code vs spec” conflicts.

It is explicitly **not**:

* a list of test cases,
* a place where individual oracles live,
* a run report,
* a bug log.

## Content requirements

A complete strategy covers:

### 1) Test layers and intent

Defines permitted assertion strength by layer:

* **Unit**: precise, local, structural.
* **Integration**: contract-level, interface behavior.
* **System/E2E (if any)**: coarse outcome-based.

### 2) Oracle governance

Defines:

* when an oracle spec is required vs ad hoc tests,
* allowed oracle types (invariants, metamorphic, golden master, etc.),
* authority sources (PROJECT.md, docstrings, design notes, standards).

### 3) Oracle spec format and lifecycle

Defines:

* required header fields,
* required sections (preconditions/action/expected),
* stable IDs (oracle IDs, case IDs),
* where oracle specs live in the repo.

### 4) Translation policy (Oracle spec → pytest)

Defines:

* filename and directory mapping rules,
* traceability rules (test must reference oracle case IDs),
* what pytest is allowed to assert beyond the spec (usually: **nothing**, except harness details).

### 5) Change control

Defines:

* when code must change vs tests must change,
* evidence required to modify oracle specs,
* evidence required to modify tests due to refactor drift,
* escalation rules (what to do when intent is unclear).

### 6) Execution conventions

Defines:

* how to run the full suite,
* how to run focused subsets,
* naming/markers (if used),
* expectations for “fast check” vs “gate check”.

## Inputs / Outputs

### Inputs (to create/update `TEST_STRATEGY.md`)

* `PROJECT.md`, module docstrings, relevant design docs
* existing test tree and configs
* known pain points from recent failures (`TEST_RUN_REPORT.md`)
* architectural decomposition (if available)

### Outputs

* `TEST_STRATEGY.md` (primary)
* optionally:

  * `TESTING_CONVENTIONS.md`
  * `TEST_PLAN.md` (phase-scoped checklist)

## Skill link: S4

**S4 (Test Strategy Designer)** is responsible for producing and maintaining this layer.

### S4 inputs

* `PROJECT.md`, repo structure, test configs, existing tests

### S4 outputs

* `TEST_STRATEGY.md` (+ optional supporting docs)

### S4 behavior

* Defines the “constitution” that constrains S6, S7, bug-fixer.

---

# Layer 2 — Oracle Specs (Normative, Non-Executable)

## Artifacts

Many files of the form:

* `*_TEST_ORACLE.md` (subsystem/domain scoped)

  * e.g., `CORE_TEST_ORACLE.md`, `ROTATION_TEST_ORACLE.md`, `IO_CONTRACT_TEST_ORACLE.md`

## Scope

* **Many per project**, each scoped to:

  * a subsystem,
  * a domain concept,
  * a module contract,
  * a set of invariants.

Oracle specs must **scale by decomposition**. A single project-wide oracle file is a smell.

## Purpose

Oracle specs are **formal test definitions**:

* precise statements of correctness,
* written in structured language,
* not executable.

They define the normative “truth claims” the project intends to enforce.
They are the authority that bug-fixer and S6 use to decide whether a failing test indicates:

* code violates the spec,
* the pytest implementation is wrong/brittle,
* the spec itself is outdated.

## Required structure (recommended minimum)

Per oracle file:

* **Oracle ID**: stable identifier for the spec
* **Scope statement**: what behavior/contract it covers
* **Authority basis**: citations to:

  * docstrings
  * `PROJECT.md`
  * design notes
* **Definitions**: terms, invariants, assumptions
* **Cases**: a list of individual test cases

  * each with stable Case ID

Per case:

* Preconditions
* Inputs / setup
* Action
* Expected outcomes / invariants
* Notes on acceptable nondeterminism (if any)

## Inputs / Outputs

### Inputs (to create/update an oracle spec)

* `TEST_STRATEGY.md` (format + governance)
* `PROJECT.md` / docstrings / design notes (authority)
* code structure (for mapping to correct layer and placement)

### Outputs

* New or updated `*_TEST_ORACLE.md` files

## Skill link: S6

**S6 (Test Author)** is responsible for authoring oracle specs (Mode A) as a first-class output.

### S6 Mode A (Oracle Spec Authoring)

* Input: strategy + authority sources
* Output: oracle spec files with case IDs

---

# Layer 3 — Oracle Implementations (Executable Tests)

## Artifacts

* `tests/*.py` pytest modules, ideally translated from oracle specs.

Examples:

* `tests/test_rotation_from_oracle.py`
* `tests/test_io_contracts_from_oracle.py`

## Scope

* Module-level and suite-level.
* These are **compiled artifacts** of the oracle specs.

## Purpose

Executable test code is:

* the runnable encoding of the oracle specs,
* and the primary tool for automated verification.

But **pytest tests are not the source of truth**.
Their correctness is judged by fidelity to oracle specs and strategy constraints.

## Required traceability

Every oracle-implemented test module should:

* Reference the oracle spec file(s) it implements
* For each test (or parametrized case), reference the **Case ID**
* Avoid asserting anything not justified by the oracle spec, except minimal harness details

## Inputs / Outputs

### Inputs (to create/update tests)

* `TEST_STRATEGY.md` (placement, style constraints)
* relevant `*_TEST_ORACLE.md` spec(s)
* code under test

### Outputs

* pytest modules implementing the oracle cases
* optional small test utilities (only if policy permits)

## Skill link: S6

**S6 (Test Author)** is responsible for translating oracle specs into pytest modules (Mode B).

### S6 Mode B (Oracle Translation)

* Input: oracle specs + strategy
* Output: pytest modules with traceability back to Case IDs

---

# Observational Layer — Test Run Reports (Execution Evidence)

## Artifact

**`TEST_RUN_REPORT.md`** (run-scoped, project-level log)

## Scope

* One per run (or append-only log of runs).
* Records what happened; never defines correctness.

## Purpose

This is the output of running tests:

* commands executed
* scope
* environment snapshot
* results summary
* failure enumeration
* failure grouping/classification
* recommended next action (S6 vs bug-fixer vs strategy update)

This is the “lab notebook entry” for verification.

## Skill link: S7

**S7 (Test Runner & Failure Triage)** is responsible for producing `TEST_RUN_REPORT.md`.

---

# Skill Operations and Interfaces

## S4 — Test Strategy Designer

### Function

Produces/maintains `TEST_STRATEGY.md`.

### Inputs

* `PROJECT.md`, docstrings, design notes
* repository structure and test configs
* existing oracle specs and tests (if any)

### Outputs

* `TEST_STRATEGY.md` (primary)
* optional supporting conventions documents

### Constraints

* No code/test mutation.
* Does not define individual test cases.

---

## S6 — Test Author

S6 is a **two-output skill**:

### Mode A — Oracle Spec Authoring

Creates/updates `*_TEST_ORACLE.md`.

**Inputs**

* `TEST_STRATEGY.md`
* authoritative sources for expected behavior

**Outputs**

* `*_TEST_ORACLE.md` with stable IDs and cases

**Constraints**

* No invention of correctness.
* If behavior isn’t grounded, report ambiguity instead of writing oracles.

### Mode B — Oracle Implementation

Translates oracle specs into pytest tests.

**Inputs**

* `TEST_STRATEGY.md`
* oracle specs
* code under test

**Outputs**

* `tests/*.py` implementing oracle cases
* traceability links (oracle file + case IDs)

**Constraints**

* Don’t assert beyond spec.
* Avoid brittle coupling to implementation details unless strategy explicitly allows it.

---

## S7 — Test Runner & Failure Triage

### Function

Runs tests and produces a structured diagnostic report.

### Inputs

* repository state
* execution scope (full suite or targeted)
* triage references (e.g. Python triage doc)

### Outputs

* `TEST_RUN_REPORT.md`

### Constraints

* Strictly read-only: no code/test/config mutation.
* Group failures by root cause; classify systematically.

---

# How the layers resolve “Should we change code or tests?”

This is the key value of your system.

When a test fails, bug-fixer (or a human) must decide among:

1. **Code violates oracle spec** → fix code
2. **Pytest implementation violates oracle spec** → fix test implementation
3. **Oracle spec is outdated** → change oracle spec (highest bar; requires authority evidence)

`TEST_STRATEGY.md` defines:

* what evidence is admissible,
* when each of these choices is permitted,
* what is forbidden (aliases/stubs/just-to-pass).

Oracle specs provide the normative reference.
Pytest provides the execution surface.
Reports provide situational evidence.

---

# Practical “end-to-end” flow

## Greenfield (recommended)

1. S4: create minimal `TEST_STRATEGY.md`
2. S6(A): create initial oracle specs for core invariants
3. S6(B): translate those into pytest
4. S7: run tests → report
5. Iterate

## When tests fail

1. S7: run full suite → `TEST_RUN_REPORT.md`
2. bug-fixer:

   * uses triage doc + strategy + oracle specs
   * fixes code/tests with strict rules
   * runs focused then full suite
3. If failures reveal missing coverage:

   * S6 adds oracle cases + translations

---

# Minimal input/output summary

| Layer        | Artifact(s)          | Scope            | Produced by | Consumed by            |
| ------------ | -------------------- | ---------------- | ----------- | ---------------------- |
| Strategy     | `TEST_STRATEGY.md`   | project-wide     | S4          | S6, S7, bug-fixer      |
| Oracle specs | `*_TEST_ORACLE.md`   | subsystem/domain | S6 (Mode A) | S6 (Mode B), bug-fixer |
| Oracle impl  | `tests/*.py`         | module/suite     | S6 (Mode B) | S7, bug-fixer          |
| Run report   | `TEST_RUN_REPORT.md` | run-scoped       | S7          | bug-fixer, S6, S4      |

---

If you want, I can turn the above into a **repo-ready document** (e.g., `TESTING_SYSTEM.md`) with:

* a canonical directory layout recommendation,
* a minimal oracle spec template (with IDs),
* a “decision procedure” section for bug-fixer (code vs test vs spec).
