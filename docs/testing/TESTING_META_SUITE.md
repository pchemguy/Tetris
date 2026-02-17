---
doc_id: TESTING_META_SUITE
name: TESTING_META_SUITE.md
title: Testing Meta Suite
kind: testing
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Describes testing meta suite
url: https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

### `TEST_STRATEGY.md` vs. `TESTING_CONVENTIONS.md`

#### Canonical distinction

##### `TEST_STRATEGY.md` answers

**“What kinds of correctness claims are allowed, where, and based on what authority?”**

It is the **governance/constitution** that defines:

* *test layers* (unit/integration/system) and *what may be asserted* at each
* authority sources* (which docs define truth)
* oracle policy* (when oracle specs are required; allowed oracle types)
* change control* (when code vs tests vs oracle specs change, evidence rules)
* execution governance* (full suite gate, required reporting artifacts)
* non-negotiable prohibitions* (no suppression, no just-to-pass, etc.)

It must be **project-wide, stable, and normative**.

##### `TESTING_CONVENTIONS.md` answers

**“How do we encode the strategy in this repository’s concrete file layout, naming, IDs, and pytest patterns?”**

It is the **mechanics/encoding manual**:

* directory layout and filenames
* naming schemes (`test_<domain>_from_oracle.py`, `ORACLE_ID`, `CASE_ID`)
* formatting rules and templates (headers, required sections)
* pytest implementation patterns (parametrization conventions, fixture conventions)
* determinism mechanics (seeding patterns, time-step hooks, banned APIs like `sleep`)
* how to write fixtures for board/pieces, helper modules, etc.
* how run reports are named and where stored (mechanically)

It should be **project-specific**, practical, and may evolve more often than strategy.

---

#### The “non-overlap” rule (hard)

**If a statement can be true in any repo that uses your testing system, it belongs in `TEST_STRATEGY.md`.**
**If a statement mentions paths, filenames, naming, IDs, pytest coding patterns, or local layout, it belongs in `TESTING_CONVENTIONS.md`.**

That single rule usually fixes 95% of overlap.

---

#### Concrete placement rules (LLM editing rubric)

When reviewing text, classify each paragraph as one of:

##### A) Governance / policy / authority  → `TEST_STRATEGY.md`

Contains any of:

* “must/shall” about what is permitted to assert
* evidence rules (“must cite docstrings/PROJECT.md”)
* layer definitions and what belongs to each layer
* rules for changing tests vs code vs spec
* definition of what counts as an oracle and allowed oracle types
* prohibited fix classes (“no xfail/skip”, “no just-to-pass”)
* required run-gating (“full suite at end of task”)

##### B) Encoding / repo mechanics → `TESTING_CONVENTIONS.md`

Contains any of:

* directory paths (`docs/testing/oracles/…`, `tetris/tests/…`)
* filenames and naming conventions
* ID format syntax (`ORACLE_ROTATION_001`)
* templates (required section headings, header blocks)
* pytest patterns (parametrize style, fixture naming, helper placement)
* determinism implementation details (seed fixture name, step harness functions)
* run report file naming and storage location

##### C) Execution cadence / scope selection → (usually) `TEST_PLAN.md`

Contains:

* suite names and exact commands
* “run when” schedule (local vs CI, pre-gate vs pre-merge)
* time budgets and recommended subsets

If this material appears in strategy/conventions, move it to `TEST_PLAN.md`.

---

#### Quick “smell tests” for overlap

##### If you see this in `TEST_STRATEGY.md`, it’s misplaced:

* “Place oracle specs in `docs/testing/oracles/`”
* “Name pytest modules `test_<domain>_from_oracle.py`”
* “Use fixture `empty_board()`”
* “Use `@pytest.mark.core`”
  These are conventions.

##### If you see this in `TESTING_CONVENTIONS.md`, it’s misplaced:

* “At integration layer, do not assert internal state”
* “Tests may be changed only with authority evidence”
* “Oracle specs are the normative source of truth”
  These are governance/strategy rules.

(Conventions may *refer* to strategy, but should not *redefine* it.)

---

#### How the LLM should rewrite drafts to enforce separation

Give the LLM this deterministic procedure:

1. **Extract all paragraphs** from both files into a single list.
2. For each paragraph, label it `STRATEGY`, `CONVENTIONS`, or `PLAN` using the rubric above.
3. **Move paragraphs** into the correct file.
4. Within each file:
    * remove duplicates
    * ensure consistent terminology
    * ensure each file is self-consistent and references the others where appropriate
5. Ensure **no paragraph appears in more than one file**.
6. Add minimal cross-references:
    * Strategy references conventions for “how encoded”
    * Conventions references strategy for “why this rule exists”
    * Plan references both (because plan executes what strategy governs and conventions encode)

---

#### Minimal table you can include at top of both docs

Put this table (or a version of it) near the top of both files to keep future edits clean:

| Document                 | Role              | Contains                                                                         | Must not contain                                                       |
| ------------------------ | ----------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `TEST_STRATEGY.md`       | Governance        | Layers, oracle policy, authority sources, change-control, prohibitions           | Paths, naming schemes, pytest patterns, templates                      |
| `TESTING_CONVENTIONS.md` | Encoding          | Layout, naming, IDs, pytest patterns, fixture conventions, determinism mechanics | Policy about what is allowed to assert, evidence rules, change-control |
| `TEST_PLAN.md`           | Execution cadence | Named suites, commands, when to run what                                         | Correctness definitions, oracle semantics                              |

---

#### A short “LLM instruction block” you can paste verbatim

Use this as a prompt snippet:

> When drafting or revising `TEST_STRATEGY.md` and `TESTING_CONVENTIONS.md`, enforce strict separation:
>
> * `TEST_STRATEGY.md` defines governance: test layers, allowed oracle strength, authority sources for correctness, change-control rules, and prohibitions. It must not mention repo-specific paths, filenames, naming schemes, pytest coding patterns, fixtures, or templates.
> * `TESTING_CONVENTIONS.md` defines encoding mechanics: directory layout, file naming, ID formats, templates, pytest patterns, fixture conventions, determinism mechanics, and report naming. It must not redefine what is allowed to assert, evidence rules, or change-control policy.
> * If content is about “what to run when,” move it to `TEST_PLAN.md`.
>   For every paragraph, classify it as STRATEGY vs CONVENTIONS vs PLAN and move it accordingly. No overlap.

---

### Templates

Below is a **clean starter outline** for all three documents:

* `TEST_STRATEGY.md`
* `TESTING_CONVENTIONS.md`
* `TEST_PLAN.md`

This structure is intentionally designed to **make overlap structurally difficult**.
Each section is placed so an LLM (or human) can classify content deterministically.

You can use this as the canonical skeleton.

---

#### 1️⃣ TEST_STRATEGY.md — Governance (Constitution)

> Purpose: Define *what correctness means and how it may be asserted*.
> Must NOT contain repo paths, filenames, naming patterns, or pytest mechanics.

---

```md
---
doc_id: TEST_STRATEGY
title: Test Strategy
kind: governance
scope: global
authority: normative
---

#### TEST_STRATEGY

##### 1. Purpose

Defines the governance rules for testing in this project.
Specifies what constitutes valid correctness claims and how tests relate to authoritative documentation.

This document governs:
- Oracle design
- Test layer boundaries
- Change control
- Failure interpretation

It does not define:
- File layout
- Naming conventions
- Execution commands

---

##### 2. Testing Objectives

- Protect core determinism.
- Enforce architectural boundaries.
- Prevent specification drift.
- Provide auditable AI-agent evaluation signals.

---

##### 3. Test Layers and Assertion Strength

###### 3.1 Unit Layer
- Scope:
- Allowed assertions:
- Prohibited assertions:

###### 3.2 Integration Layer
- Scope:
- Allowed assertions:
- Prohibited assertions:

###### 3.3 System Layer (if applicable)
- Scope:
- Allowed assertions:
- Prohibited assertions:

---

##### 4. Oracle Policy

###### 4.1 What is an Oracle

Definition of oracle in this project.

###### 4.2 When Oracle Specs Are Required

Criteria for formal oracle specification.

###### 4.3 Allowed Oracle Types

- Invariant
- Contract
- Metamorphic
- Deterministic replay
- etc.

###### 4.4 Oracle Authority Sources

Define which documents constitute correctness authority:
- PROJECT.md
- GAME_RULES.md
- etc.

---

##### 5. Change Control Policy

###### 5.1 When Code Must Change
###### 5.2 When Tests May Change
###### 5.3 When Oracle Specs May Change
###### 5.4 Evidence Requirements

---

##### 6. Determinism Requirements (Policy-Level)

High-level determinism requirements.
(No implementation details here.)

---

##### 7. Prohibited Practices

- Just-to-pass fixes
- Error suppression
- Silent weakening of assertions
- etc.

---

##### 8. Execution Governance

- Full suite must pass before declaring a gate complete.
- Required reporting artifacts.
- Relationship to bug-fixer and S7.

---

##### 9. Relationship to Other Documents

- TESTING_CONVENTIONS.md (mechanics)
- TEST_PLAN.md (execution cadence)
```

---

#### 2️⃣ TESTING_CONVENTIONS.md — Encoding (Mechanics)

> Purpose: Define *how* strategy is encoded in this repository.
> Must NOT redefine what correctness means or what evidence is required.

---

```md
---
doc_id: TESTING_CONVENTIONS
title: Testing Conventions
kind: conventions
scope: project
authority: normative
---

#### TESTING_CONVENTIONS

##### 1. Purpose

Defines repository-specific mechanical conventions for implementing the testing strategy.

This document specifies:
- Directory layout
- Naming patterns
- ID formats
- Pytest structure
- Fixture conventions
- Determinism mechanics

It does not define:
- Test layer policy
- Oracle authority
- Change-control rules

---

##### 2. Directory Structure

Describe where:
- Oracle specs live
- Pytest modules live
- Shared test utilities live
- Run reports live

---

##### 3. Naming Conventions

###### 3.1 Oracle File Naming
###### 3.2 ORACLE_ID Format
###### 3.3 CASE_ID Format
###### 3.4 Pytest Module Naming
###### 3.5 Test Function Naming

---

##### 4. Oracle-to-Pytest Mapping Rules

- Header requirements
- CASE_ID traceability rules
- Comment requirements
- Parametrization conventions

---

##### 5. Pytest Implementation Patterns

- Parametrization rules
- Fixture naming conventions
- Helper modules
- Allowed markers (if any)

---

##### 6. Determinism Mechanics

- RNG seeding conventions
- Time-stepping conventions
- Prohibited APIs (sleep, real-time calls)
- Replay injection patterns

---

##### 7. Regression Test Additions

How to add new test cases after bug fixes (mechanical process only).

---

##### 8. Run Report File Conventions

Naming/location of:
- TEST_RUN_REPORT.md
- Fix reports
- Append-only vs replace policy

---

##### 9. Relationship to Strategy

This document implements TEST_STRATEGY.md but does not modify it.
```

---

#### 3️⃣ TEST_PLAN.md — Execution Cadence

> Purpose: Define named suites and when to run them.
> Must NOT define correctness or oracle semantics.

---

```md
---
doc_id: TEST_PLAN
title: Test Plan
kind: execution
scope: project
authority: normative
---

#### TEST_PLAN

##### 1. Purpose

Defines named test suites and execution cadence.

This document specifies:
- What suites exist
- What they include
- When they must be executed

It does not define:
- Oracle semantics
- Assertion policy
- Change-control rules

---

##### 2. Named Suites

###### 2.1 suite:smoke
Purpose:
Scope:
Command:

###### 2.2 suite:core-fast
Purpose:
Scope:
Command:

###### 2.3 suite:core-full
Purpose:
Scope:
Command:

###### 2.4 suite:rendering
...

###### 2.5 suite:runtime
...

###### 2.6 suite:replay
...

###### 2.7 suite:full
...

---

##### 3. Execution Rules

- When to run fast suites
- When full suite is mandatory
- Gate-specific requirements

---

##### 4. Time Budget Expectations (Optional)

Expected runtime targets for each suite.

---

##### 5. Relationship to Other Documents

- TEST_STRATEGY.md governs correctness.
- TESTING_CONVENTIONS.md governs structure.
```

---

#### Why This Structure Works

* Strategy contains **no repo mechanics**
* Conventions contain **no policy**
* Plan contains **no correctness definitions**
* Each file explicitly states what it must not contain

An LLM can now:

1. Classify each paragraph.
2. Move it to the correct file.
3. Ensure no duplication.
4. Maintain separation over time.

---
---

# 🔎 Classification Algorithm (Deterministic)

For every paragraph in any draft of:

* `TEST_STRATEGY.md`
* `TESTING_CONVENTIONS.md`
* `TEST_PLAN.md`

Apply the following decision tree **in order**:

---

## Step 1 — Is this about execution cadence?

If the paragraph answers:

* What suite runs when?
* What command should be executed?
* Which subset is required for a gate?
* What is the time budget?
* What should run in CI vs local?

→ Classify as `PLAN`.

Move to `TEST_PLAN.md`.

---

## Step 2 — Is this about correctness policy or authority?

If the paragraph contains any of:

* What is allowed to be asserted?
* What test layers exist and what belongs in them?
* What defines correctness?
* What documents are authoritative?
* When code vs tests vs oracle specs may change?
* Prohibited fix classes?
* Determinism requirements at a policy level?
* Evidence requirements?
* Gate compliance requirements?

→ Classify as `STRATEGY`.

Move to `TEST_STRATEGY.md`.

---

## Step 3 — Is this about encoding or repository mechanics?

If the paragraph contains any of:

* Directory paths
* File names
* Naming conventions
* ID format definitions
* Template headers
* pytest patterns
* fixture names
* marker names
* RNG seeding mechanics
* step harness implementation details
* run report file naming/location

→ Classify as `CONVENTIONS`.

Move to `TESTING_CONVENTIONS.md`.

---

## Step 4 — Conflict resolution rule

If a paragraph contains both policy and mechanics:

* Extract the policy portion → `TEST_STRATEGY.md`
* Extract the mechanical portion → `TESTING_CONVENTIONS.md`
* Rewrite each so they reference one another instead of duplicating content.

---

## Step 5 — Final invariant check

After redistribution:

* No file may redefine content owned by another.
* Each file must contain a section titled:
    * “What This Document Does Not Contain”

This enforces structural clarity long-term.

---
