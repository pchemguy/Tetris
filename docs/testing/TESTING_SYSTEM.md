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
