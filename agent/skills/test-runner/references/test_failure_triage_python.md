---
name: test_failure_triage_python.md
URLs:
  - https://chatgpt.com/g/g-p-697ef0e4c8ec8191bbf0acac1fa069a8-rpncalc/c/697fb4b4-6564-8386-bc9d-284b1824eb07
---

# Python Test Failure Triage

## Purpose

This document defines the mandatory procedure for **analyzing and classifying** test failures in this repository.

Its goals are to:

- prevent speculative or "make-it-pass" behavior,
- enforce analysis-before-mutation (mutation is out of scope here),
- distinguish dependency, configuration, and logic failures,
- and produce a clear, structured diagnostic report suitable for downstream action.

All tasks that involve **running or diagnosing tests** must follow this procedure.

---

## General Rule

When tests fail, **no code, test, or configuration changes may be made** while following this document. This document is **diagnostic-only**. If a failure cannot be classified with high confidence using repository evidence, the task must **abort and report**. Even in abort mode, you must still:

- analyze all observed failures,
- classify them to the extent possible,
- identify likely root causes,
- and document uncertainties or missing information.

---

## 0. Reproducibility Snapshot (mandatory)

Before classification, record the following:

- Exact test command(s) executed
- Execution scope (full suite vs targeted)
- Python version
- Test framework version (e.g., pytest)
- Relevant configuration sources discovered (`pytest.ini`, `pyproject.toml`, `tox.ini`, etc.)
- Enough output to uniquely identify each failure (test id + exception + traceback root)

This information must be preserved in the diagnostic report.

---

## 1. Failure Classification

Group failures by **underlying root cause**, not by test name or traceback surface.

Each failure must be classified as one of:

- **Import / resolution failure**
- **Test logic failure**
- **Source code logic failure**
- **Environment or configuration failure**

Do not proceed to recommendations until all failures have been classified.

### Classification precedence

- Failures that prevent test execution (collection/import/config) take priority over assertion-level failures.
- If multiple failures share a single upstream cause, downstream failures should be treated as secondary effects unless proven independent.

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

### 2.2 Missing Standard-Library Imports (diagnostic)

This applies **only** when a Python standard-library module is referenced but not imported.

#### Diagnostic Procedure

1. Verify whether the referenced module is part of the Python standard library:
    - Inspect failing source and existing imports.
    - Do not infer stdlib status by name similarity.
2. If confirmed:
    - Record the missing import and its location.
    - Note that this failure is **likely trivially fixable**.
3. If not confirmed:
    - Reclassify as an **external dependency import**.

#### Abort Rule

If stdlib status cannot be determined unambiguously using repository contents:

- abort classification for this failure,
- report:
    - unresolved symbol or module name,
    - file(s) and line(s) where it is referenced,
    - reason stdlib status could not be confirmed.

---

### 2.3 External Dependency Imports (diagnostic)

For failures caused by missing external dependencies:

#### Diagnostic Procedure

1. Determine whether the dependency can be **unambiguously identified** using
   repository evidence:
    - explicit references in documentation,
    - comments,
    - `pyproject.toml`,
    - lock files.
2. If unambiguous:
    - Record the dependency name and evidence.
    - Classify as **environment / dependency failure**.
3. If ambiguous:
    - Produce a detailed ambiguity report:
        - failing import statement,
        - candidate packages (if any),
        - reason ambiguity cannot be resolved locally.

#### Internet Access Note

- Internet access may be used **only to confirm identity**, never to speculate.
- If identity remains ambiguous after best effort, abort and report.

---

### 2.4 Local Project Imports (diagnostic)

For missing or failing **local project imports**, do **not** attempt to silence the failure.

#### A) File-Level Analysis

- Verify whether the imported module file exists.
- If it does not:
    - Determine whether evidence suggests it was:
        - renamed,
        - moved,
        - intentionally removed.

#### B) Identifier-Level Analysis

- If the module exists but the imported identifier does not:
    - Determine whether evidence suggests it was:
        - renamed,
        - split or merged,
        - intentionally removed.

#### C) Documentation and Policy Alignment

Consult:

- `AGENTS.md`
- files referenced by `AGENTS.md`
- module docstrings
- documented refactor or naming policies

#### D) Diagnostic Conclusion

- If intent can be inferred with **high confidence**, record:
    - the inferred change,
    - supporting evidence.
- If intent is unclear or conflicting:
    - abort and produce a detailed ambiguity report.

---

## 3. Non-Import Failures (diagnostic)

For failures not related to imports:

1. Determine whether the failure is most likely due to:
    - incorrect test assumptions,
    - outdated tests after refactor,
    - incorrect source code behavior,
    - misconfiguration.
2. For each failure:
    - record evidence supporting the classification,
    - note whether the failure appears **systemic** or **localized**,
    - assess confidence level.

No corrective action is taken here.

---

## 4. Global Constraints (diagnostic-only)

### 4.1 Explicitly Prohibited Actions

While operating under this document, you must not:

- modify code, tests, or configuration
- delete or weaken tests
- add dependencies or change versions
- introduce alias entry points or compatibility shims
- suppress failures via broad exception handling or warning filters
- mark tests as `xfail` or `skip` to silence failures
- change unrelated files

---

### 4.2 Working Tree Safety

Assume the working tree may be dirty:

- Do not discard or rewrite unrelated changes.
- If unexpected changes prevent safe reasoning, stop and report.

---

## 5. Abort Mode

If confident classification cannot be achieved:

- stop analysis,
- produce a diagnostic report containing:
    - classified failures (partial if needed),
    - likely root causes,
    - fixability assessment,
    - issues requiring human judgment.

No mutation is performed.

---

## Output Requirement

The result of applying this document must be a **diagnostic artifact** containing:

- execution context,
- failure enumeration,
- classification and grouping,
- supporting evidence,
- confidence and uncertainty notes.

This artifact is intended for **downstream roles** authorized to perform fixes.
