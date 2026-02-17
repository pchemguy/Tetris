---
doc_id: TESTING_SYSTEM
name: TESTING_SYSTEM.md
title: Testing System
kind: testing
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Conceptual description of the testing system.
url: https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
references:
---

### `TEST_STRATEGY.md` vs. `TESTING_CONVENTIONS.md`

## Canonical distinction

### `TEST_STRATEGY.md` answers

**“What kinds of correctness claims are allowed, where, and based on what authority?”**

It is the **governance/constitution** that defines:

* *test layers* (unit/integration/system) and *what may be asserted* at each
* authority sources* (which docs define truth)
* oracle policy* (when oracle specs are required; allowed oracle types)
* change control* (when code vs tests vs oracle specs change, evidence rules)
* execution governance* (full suite gate, required reporting artifacts)
* non-negotiable prohibitions* (no suppression, no just-to-pass, etc.)

It must be **project-wide, stable, and normative**.

### `TESTING_CONVENTIONS.md` answers

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

## The “non-overlap” rule (hard)

**If a statement can be true in any repo that uses your testing system, it belongs in `TEST_STRATEGY.md`.**
**If a statement mentions paths, filenames, naming, IDs, pytest coding patterns, or local layout, it belongs in `TESTING_CONVENTIONS.md`.**

That single rule usually fixes 95% of overlap.

---

## Concrete placement rules (LLM editing rubric)

When reviewing text, classify each paragraph as one of:

### A) Governance / policy / authority  → `TEST_STRATEGY.md`

Contains any of:

* “must/shall” about what is permitted to assert
* evidence rules (“must cite docstrings/PROJECT.md”)
* layer definitions and what belongs to each layer
* rules for changing tests vs code vs spec
* definition of what counts as an oracle and allowed oracle types
* prohibited fix classes (“no xfail/skip”, “no just-to-pass”)
* required run-gating (“full suite at end of task”)

### B) Encoding / repo mechanics → `TESTING_CONVENTIONS.md`

Contains any of:

* directory paths (`docs/testing/oracles/…`, `tetris/tests/…`)
* filenames and naming conventions
* ID format syntax (`ORACLE_ROTATION_001`)
* templates (required section headings, header blocks)
* pytest patterns (parametrize style, fixture naming, helper placement)
* determinism implementation details (seed fixture name, step harness functions)
* run report file naming and storage location

### C) Execution cadence / scope selection → (usually) `TEST_PLAN.md`

Contains:

* suite names and exact commands
* “run when” schedule (local vs CI, pre-gate vs pre-merge)
* time budgets and recommended subsets

If this material appears in strategy/conventions, move it to `TEST_PLAN.md`.

---

## Quick “smell tests” for overlap

### If you see this in `TEST_STRATEGY.md`, it’s misplaced:

* “Place oracle specs in `docs/testing/oracles/`”
* “Name pytest modules `test_<domain>_from_oracle.py`”
* “Use fixture `empty_board()`”
* “Use `@pytest.mark.core`”
  These are conventions.

### If you see this in `TESTING_CONVENTIONS.md`, it’s misplaced:

* “At integration layer, do not assert internal state”
* “Tests may be changed only with authority evidence”
* “Oracle specs are the normative source of truth”
  These are governance/strategy rules.

(Conventions may *refer* to strategy, but should not *redefine* it.)

---

## How the LLM should rewrite drafts to enforce separation

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

## Minimal table you can include at top of both docs

Put this table (or a version of it) near the top of both files to keep future edits clean:

| Document                 | Role              | Contains                                                                         | Must not contain                                                       |
| ------------------------ | ----------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `TEST_STRATEGY.md`       | Governance        | Layers, oracle policy, authority sources, change-control, prohibitions           | Paths, naming schemes, pytest patterns, templates                      |
| `TESTING_CONVENTIONS.md` | Encoding          | Layout, naming, IDs, pytest patterns, fixture conventions, determinism mechanics | Policy about what is allowed to assert, evidence rules, change-control |
| `TEST_PLAN.md`           | Execution cadence | Named suites, commands, when to run what                                         | Correctness definitions, oracle semantics                              |

---

## A short “LLM instruction block” you can paste verbatim

Use this as a prompt snippet:

> When drafting or revising `TEST_STRATEGY.md` and `TESTING_CONVENTIONS.md`, enforce strict separation:
>
> * `TEST_STRATEGY.md` defines governance: test layers, allowed oracle strength, authority sources for correctness, change-control rules, and prohibitions. It must not mention repo-specific paths, filenames, naming schemes, pytest coding patterns, fixtures, or templates.
> * `TESTING_CONVENTIONS.md` defines encoding mechanics: directory layout, file naming, ID formats, templates, pytest patterns, fixture conventions, determinism mechanics, and report naming. It must not redefine what is allowed to assert, evidence rules, or change-control policy.
> * If content is about “what to run when,” move it to `TEST_PLAN.md`.
>   For every paragraph, classify it as STRATEGY vs CONVENTIONS vs PLAN and move it accordingly. No overlap.

---

### Meta-suite

#### 1) Are `TEST_STRATEGY.md` and `TESTING_CONVENTIONS.md` inputs to the oracle/test writer?

**Yes.** For S6 (oracle + pytest author), they are **mandatory upstream governance**:

* **`TEST_STRATEGY.md`** = *policy / constitution*
    * defines layers, allowed oracle strength, authority sources, traceability rules, change-control rules.
* **`TESTING_CONVENTIONS.md`** = *project-specific mechanics*
    * naming, directory layout, ID formats, pytest module naming, determinism rules, fixture conventions, etc.

So S6 consumes them to ensure:

* oracle specs are structured and grounded correctly
* pytest translations are placed/named correctly
* traceability is enforced (`ORACLE_ID`, `CASE_ID`)

If these are missing, S6 can still write tests, but it becomes “ad hoc testing,” which your framework explicitly tries to avoid.

#### 2) Is `TEST_PLAN.md` “which tests should be executed when”?

**Usually, yes—but only in a specific sense.**

`TEST_PLAN.md` is best treated as a **scope selection + execution cadence document**, not a redefinition of tests.

It answers questions like:

* What’s the **fast gate** for local iteration?
* What is required before merging / before a gate is considered satisfied?
* Which subsets correspond to which **phases/gates/components**?

##### What `TEST_PLAN.md` *should* contain

* Named suites (e.g., “core-fast”, “core-full”, “runtime-smoke”, “rendering”)
* The exact commands to run them
* When each suite is required (per gate / per phase / per workflow step)
* Time budgets (optional but useful)
* Mapping to **components/domains**, not to individual cases

Example shape:

```md
### TEST_PLAN

#### Local iteration (fast)
- Core unit fast: `pytest -q tetris/tests/test_core_from_oracle.py`
- Rotation fast: `pytest -q tetris/tests/test_rotation_from_oracle.py`

#### Pre-gate check (core)
- Core full: `pytest -q tetris/tests -m core`

#### Pre-release / full confidence
- Full suite: `pytest -q`
```

##### What `TEST_PLAN.md` should *not* contain

* Individual test case definitions (those are in oracle specs)
* “Expected behaviors” (those are in oracle specs)
* Failure triage procedures (those are triage docs / skills)

#### How these three relate (clean mental model)

* **Strategy** (`TEST_STRATEGY.md`) = *what is allowed / how to reason about correctness*
* **Conventions** (`TESTING_CONVENTIONS.md`) = *how we name/organize/encode it in this repo*
* **Plan** (`TEST_PLAN.md`) = *what to run when, and with what scope*

#### In skill terms

* **S4** produces/maintains: `TEST_STRATEGY.md` (+ usually `TEST_PLAN.md` and `TESTING_CONVENTIONS.md`)
* **S6** consumes those, and produces: `*_TEST_ORACLE.md` + `tests/*.py`
* **S7 / bug-fixer** consult `TEST_PLAN.md` to pick scopes, and produce run reports

### What suites should exist (recommended baseline set)

These assume your decomposition (core / rendering / runtime / CLI) and your “scripted virtual-time first” architecture.

**A. Always-have suites (even early project)**
1. **`suite:smoke`**
    * Purpose: “does the test harness run at all?”
    * Scope: minimal test(s) + import sanity
    * Command: smallest stable subset (often a single module)
2. **`suite:core-fast`**
    * Purpose: tight inner loop while touching core
    * Scope: core unit tests only (no runtime/render/CLI)
    * Expectation: fast (< a few seconds)
3. **`suite:core-full`**
    * Purpose: gate for “core is correct”
    * Scope: all core-domain oracles and translations
    * Run when: before declaring any core gate done
4. **`suite:full`**
    * Purpose: global health gate
    * Scope: everything in `tetris/tests`
    * Run when: end of any task that claims “repo healthy”
**B. Add as components land (post-core)**
5. **`suite:rotation`** (often also part of core, but useful as a named slice)
    * Purpose: highly targeted debugging of geometry logic
    * Scope: rotation-only oracle translations (and any helpers)
6. **`suite:rendering-fast`**
    * Purpose: quick check for ASCII renderer determinism
    * Scope: pure renderer unit tests only
7. **`suite:runtime-scripted-fast`**
    * Purpose: validate orchestration invariants in virtual time
    * Scope: runtime scripted-mode tests (no OS input)
8. **`suite:cli-smoke`**
    * Purpose: composition root wiring doesn’t break
    * Scope: CLI invocation tests for scripted mode only
**C. When replay exists (evaluation critical)**
9. **`suite:replay`**
    * Purpose: determinism + replay trace correctness
    * Scope: replay loader + replay runner invariants, equivalence tests
**D. Optional / later (only if you explicitly gate them)**
10. **`suite:interactive`**
    * Purpose: OS input + terminal presenter integration
    * Only if: you add a gate that makes interactive mode correctness mandatory
    * Otherwise: keep this out of required gating

---

## How do you decide which suites to include?

You decide suites from three inputs, in this priority order:

### 1) Phases / gates (primary driver)

Suites exist to answer: **“Is Gate X satisfied?”**
So at minimum you want:

* one suite per **gate cluster** (core gates, renderer gate, runtime gate, CLI gate, replay gate)
* plus a project-wide `full` suite

If your gates are fine-grained, you still group them into a small number of executable suites.

### 2) Architecture / decomposition (secondary driver)

Your decomposition defines **fault boundaries**, which should map to suites:

* core
* rendering
* runtime
* CLI
* persistence/replay

Suites let you validate a boundary without dragging in unrelated components (especially critical given your “functional core / imperative shell” rule).

### 3) Practical dev loop (time budgets / failure locality)

You need suites that support:

* fast inner loop (“I’m editing core; run core-fast”)
* isolation for high-churn subsystems (rotation, collision)
* “confidence” suites (core-full, full)

This is not theoretical: it’s about turnaround time and triage speed.

---

## What else can influence suite design?

* **Determinism requirements**: separate anything involving real-time/OS I/O into its own suite so it can’t pollute core gating.
* **Oracle organization**: if oracles are split by domain (rotation/collision/scoring), it’s useful to have matching domain suites.
* **CI vs local**: if you later add CI, you may add “CI-fast” vs “CI-full”, but that’s just aliases over the same suite definitions.

---

## A concrete suite catalog (what I’d put in `TEST_PLAN.md`)

**Required (always):**

* `smoke`
* `core-fast`
* `core-full`
* `full`

**Required once implemented:**

* `rendering-fast`
* `runtime-scripted-fast`
* `cli-smoke`
* `replay`

**Useful targeted slices (optional but recommended):**

* `rotation`
* `collision`
* `scoring`
* `line-clear`
* `state-machine`

**Optional future:**

* `interactive`

---

## Implementation note: markers vs paths

You can implement named suites either by:

* **path-based** selection (most robust early), or
* **pytest markers** (more flexible later)

Given your repo’s “auditability” goals, I’d start path-based, and add markers only when the suite matrix grows.

Example (path-based) mapping:

* `core-fast`: `pytest -q tetris/tests/test_core_from_oracle.py tetris/tests/test_rotation_from_oracle.py`
* `core-full`: `pytest -q tetris/tests/test_*core*.py tetris/tests/test_*rotation*.py ...` (or just a directory `tetris/tests/core/`)
* `full`: `pytest -q tetris/tests`

If you want, I can draft the actual `TEST_PLAN.md` with:

* suite names
* exact commands
* “run when” rules for S7 and bug-fixer
* time-budget expectations

…but I’ll make a safe default now: **assume path-based suites**, and a directory layout like:

* `tetris/tests/core/`
* `tetris/tests/rendering/`
* `tetris/tests/runtime/`
* `tetris/tests/cli/`
* `tetris/tests/replay/`

If that directory layout is not what you want, tell me your intended `tetris/tests` structure and I’ll adapt the suite definitions.

---
