---
name: test_failure_triage_fix_python.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# Python Test Failure Triage and Fix

## Purpose

This document defines the mandatory procedure for **analyzing, prioritizing, and correctly fixing** test failures in this repository.

Its goals are to:

- prevent speculative or "just-to-pass" fixes,
- enforce analysis-before-mutation,
- distinguish configuration issues from code or test defects,
- ensure fixes are minimal, evidence-backed, and reversible.

All tasks that involve **fixing failing tests or underlying bugs** must follow this procedure.

---

## General Rule

When tests fail, **no code, test, or configuration changes may be made** until **all failures have been classified and analyzed** according to this document. If a correct fix cannot be determined with high confidence, the task must **abort and report**. Environment or configuration failures are **never fixed** under this document and must be reported with full diagnostics.

---

## 0. Reproducibility Snapshot (mandatory)

Before classification and fixing, record:

- Exact test command(s) executed
- Execution scope (full suite vs targeted)
- Python version
- Test framework version (e.g., pytest)
- Relevant configuration sources discovered (`pytest.ini`, `pyproject.toml`, `tox.ini`, etc.)
- Sufficient output to uniquely identify each failure (test id + exception + traceback root)

This information must be preserved in the final report.

---

## 1. Failure Classification

Group failures by **underlying root cause**, not by test name or traceback surface.

Each failure must be classified as one of:

- **Import / resolution failure**
- **Test logic failure**
- **Source code logic failure**
- **Environment or configuration failure**

Do not proceed to fixes until all failures are classified.

### Classification precedence

- Failures preventing test execution (collection/import/config) take priority over assertion-level failures.
- If multiple failures share a single upstream cause, downstream failures must be treated as secondary effects unless proven independent.

---

## 2. Import and Resolution Failures (mandatory, first)

If any failure involves:

- `ImportError`
- `ModuleNotFoundError`
- `NameError` related to imports
- unresolved symbols

this section **must be applied first**.

---

### 2.1 Determine Import Type

For each failing import or unresolved symbol, determine whether it is:

1. **Missing standard-library import**
2. **External dependency import**
3. **Local project import**

Proceed according to the corresponding section below.

---

### 2.2 Missing Standard-Library Imports

#### Analysis

Verify whether the referenced module is part of the Python standard library:

- Inspect failing source and existing imports.
- Do not infer stdlib status by name similarity alone.

#### Fix Rule

- If confirmed:
    - Add the minimal missing `import` statement(s).
    - Follow existing import style and ordering.
    - Re-run the focused failing scope.
- If not confirmed:
    - Reclassify as **external dependency import**.

#### Abort Rule

If stdlib status cannot be determined unambiguously:

- abort fixing for this failure,
- report evidence and uncertainty.

---

### 2.3 External Dependency Imports

#### Analysis

Determine whether the dependency can be **unambiguously identified** using repository evidence:

- documentation,
- comments,
- `pyproject.toml`,
- lock files.

#### Fix Rule

- If dependency identity is unambiguous **and already intended by the project**:
    - Add it to `pyproject.toml` in the appropriate section.
- If ambiguity remains:
    - abort and report.

#### Prohibition

- Do not add dependencies speculatively.
- Do not pin versions opportunistically.
- Do not "try likely packages" to see what works.

---

### 2.4 Local Project Imports

For missing or failing **local project imports**, do **not** silence failures.

#### A) File-Level Analysis

- Verify whether the imported module file exists.
- If missing, determine whether evidence suggests it was:
    - renamed,
    - moved,
    - intentionally removed.

#### B) Identifier-Level Analysis

- If the module exists but the identifier does not:
    - determine whether it was:
        - renamed,
        - split or merged,
        - intentionally removed.

#### C) Documentation and Policy Alignment

Consult:

- `AGENTS.md` and `PROJECT.md`
- files referenced by `AGENTS.md` and `PROJECT.md`
- module docstrings
- documented refactor or naming policies

#### D) Fix Rule

- If refactor intent can be inferred with **high confidence**:
    - update **tests** to match the new structure.
    - cite concrete evidence (docs, commit messages, code comments).
- If intent is unclear or conflicting:
    - abort and report.

---

## 3. Non-Import Failures

For failures not related to imports:

### 3.1 Classification

Determine whether the failure is most likely due to:

- incorrect or outdated test assumptions,
- correct code behavior after refactor,
- incorrect source code logic,
- environment or configuration issues.

### 3.2 Fix Prioritization

From a fixing perspective:

- **Highest priority**:
    - tests out of sync with correct code behavior after refactor
- **High priority**:
    - localized code logic bugs
    - multiple failures sharing a single cause
- **Not fixable here**:
    - environment or configuration failures

### 3.3 Fix Rules

- Tests may be modified **only** when evidence shows code behavior matches documentation, docstrings, or explicit design intent.
- Code fixes must:
    - address the root cause,
    - avoid broad or defensive hacks,
    - not introduce aliases, stubs, or shims.

---

## 4. Fix Execution Loop

For each selected failure group:

1. Apply the minimal correct fix (code or tests).
2. Optionally add a **focused regression test** only if:
    - the bug reveals an untested edge case, or
    - the fix could plausibly introduce regressions.
3. Run focused tests for the affected scope.
4. Watch for cascading failures:
    - a later assertion may fail for a different reason.
    - reclassify before proceeding.
5. Once focused tests pass, run the **full test suite**.

Repeat until all fixable failures are resolved.

---

## 5. Global Constraints on Fixes

### 5.1 Explicitly Prohibited

You must not:

- delete tests to make the suite pass
- weaken assertions without replacement
- introduce speculative behavior
- introduce alias entry points, stubs, or compatibility shims
- suppress failures with broad exception handling
- mark tests as `xfail` or `skip` to silence failures
- change unrelated files

### 5.2 Working Tree Safety

- Touch the smallest set of files possible.
- If unexpected changes prevent safe reasoning, stop and report.

---

## 6. Abort Mode

If a correct fix cannot be determined confidently:

- stop fixing,
- produce a report containing:
    - classified failures,
    - fixability assessment,
    - evidence and uncertainties,
    - issues requiring human judgment.

---

## Output Requirement

The result of applying this document must include:

- initial failure classification,
- fix priority rationale,
- fixes applied (code/tests),
- evidence justifying test changes,
- any focused tests added,
- confirmation that the full test suite passes (or why it cannot).
