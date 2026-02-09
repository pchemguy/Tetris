---
name: TEST_FAILURE_TRIAGE_PYTHION.md
URLs:
  - https://chatgpt.com/g/g-p-697ef0e4c8ec8191bbf0acac1fa069a8-rpncalc/c/697fb4b4-6564-8386-bc9d-284b1824eb07
---

# Python Test Failure Triage

## Purpose

This document defines the mandatory procedure for analyzing and resolving test failures in this repository.

Its goals are to:

- prevent speculative or "make-it-pass" fixes,
- enforce analysis-before-mutation,
- distinguish dependency issues from local refactors,
- and ensure minimal, reversible changes.

All tasks that involve running or fixing tests must follow this procedure.

---

## General Rule

When tests fail, **no code or configuration changes may be made** until all failures have been classified and analyzed according to this document.

If a correct fix cannot be determined with high confidence, the task must **abort and report**. If the task must be aborted, you must still:

- analyze all failures,
- identify which failures are likely fixable automatically,
- and produce a detailed report.

---

## 1. Failure Classification

Group failures by **underlying root cause**, not by test name or traceback surface.

Each failure must be classified as one of:

- **Import / resolution failure**
- **Test logic failure**
- **Source code logic failure**
- **Environment or configuration failure**

Do not proceed to fixes until all failures are classified.

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

This applies **only** when a Python standard-library module is referenced but not imported.

#### Procedure

1. Confirm that the referenced module is part of the Python standard library:
    - Verify by inspecting the failing source code and existing imports.
    - Do not assume stdlib status based on name similarity alone.
2. If confirmed:
    - Add the minimal missing `import` statement(s) to the appropriate source file(s).
    - Follow existing import style in the file (module-level imports, ordering, etc.).
3. Re-run the failing scope to confirm the issue is resolved.

#### Reclassification Rule

If the referenced module is **not** part of the standard library, reclassify the failure as an **external dependency import** and proceed to section 2.3.

#### Abort Rule

If stdlib status cannot be determined unambiguously using repository contents:

- abort the task,
- produce a detailed analysis, including
    - unresolved symbol or module name,
    - file(s) and line(s) where it is referenced,
    - reason stdlib status could not be confirmed.

---

### 2.3 External Dependency Imports

For failures caused by missing external dependencies:

#### Procedure

1. Determine whether the dependency can be **unambiguously identified** using repository contents:
    - clear mapping from import name to package name, or
    - explicit references in documentation, comments, or `pyproject.toml`.
2. If unambiguous:
    - Add the dependency to `pyproject.toml` in the appropriate section:
        - `[project].dependencies` for runtime dependencies, or
        - `[project.optional-dependencies].dev` for test-only dependencies.
    - Prefer the most flexible constraint:
        1) unconstrained,
        2) minimum version consistent with existing dependencies,
        3) other appropriate specification.
    - Add missing `import` statements if applicable.
    - Continue the task.
3. If ambiguous:
    - Produce a detailed dependency analysis:
        - failing import statement
        - candidate packages (if any)
        - reason ambiguity cannot be resolved locally
    - Abort the task without making speculative changes.

#### Internet Access Rules

- If Internet access is unavailable and dependency identity cannot be confirmed:
    - abort and report.
- If Internet access is available and dependency can be unambiguously identified:
    - add it to `pyproject.toml` and continue.
- If ambiguity remains after best effort:
    - abort and report.

---

### 2.4 Local Project Imports

For missing or failing **local project imports**, do **not** immediately modify source code to silence the failure.

#### A) File-Level Resolution

- Verify whether the imported module file exists.
- If it does not exist:
    - Examine a limited, recent commit window to determine whether the file was:
        - renamed,
        - moved,
        - intentionally removed.

#### B) Identifier-Level Resolution

- If the module exists but the imported identifier does not:
    - Examine recent commits, including full diff's, to determine whether it was:
        - renamed,
        - split or merged,
        - intentionally removed.

#### C) Documentation and Policy Alignment

Consult:

- `AGENTS.md`
- files referenced by `AGENTS.md`
- module docstrings
- documented naming or refactoring guidelines

#### D) Fix Selection Rule

- Infer intended refactoring or naming schemes only from these sources (2.4.A-C).
- If a likely refactor or rename can be determined with **high confidence**:
    - update **test code** to match the new structure.
    - do **not** add compatibility aliases, dummy exports, or shim imports.
    - output specific evidences (doc sections, commit messages, relevant patches) supporting refactoring-related culprit.
- If intent is unclear, conflicting, or cannot be determined within a bounded analysis effort:
    - abort and produce a detailed ambiguity report.

---

## 3. Non-Import Failures

For failures not related to imports:

1. Determine whether the failure is due to:
    - incorrect test assumptions,
    - outdated tests after refactor,
    - incorrect source code behavior,
    - misconfiguration.
2. Apply the **minimum change** that resolves the root cause and is consistent with:
    - current implementation,
    - documented contracts,
    - `DEV_STRATEGY.md`.

---

## 4. Global Constraints on Fixes (all failure types)

### 4.1 Allowed modifications

You may modify:

* failing test files, when failures are caused by refactors or contract changes or clear test logic failure
* the source module(s) under test, when tests correctly encode documented behavior
* shared test utilities (`conftest.py`, helpers) only if it reduces duplication or fixes a systematic issue
* configuration only if the failure is clearly caused by misconfiguration and the intended config is evident from repo docs

### 4.2 Prohibited modifications

You must not:

* delete tests to make the suite pass
* weaken assertions without replacing them with equally meaningful assertions
* introduce speculative behavior not evidenced by code/docs
* introducing new alias entry points (e.g., adding `foo = bar` or `def foo(): return bar()`) intended primarily to satisfy failing imports/calls
* apply compatibility hacks (dummy imports, alias re-exports, blanket `try/except`) to silence failures
* silence failures by catching broad exceptions or suppressing warnings unless repo docs require it
* change unrelated files

### 4.3 Working tree safety

Assume the working tree may be dirty:

* Do not discard unrelated changes.
* Touch the smallest set of files needed.
* If you detect unexpected changes that affect your ability to reason safely, stop and report.

---

## 5. Abort Mode

If a correct fix cannot be determined confidently:

- do not modify code or configuration,
- produce analysis only,
- report:
    - classified failures,
    - likely fixable issues,
    - issues requiring human intervention.

---
