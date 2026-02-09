---
name: "test-runner"
description: "Use when you need to assess project health by running tests at a specified scope (single module, group, or full suite) and, on failure, produce a structured, non-mutating diagnostic report: enumerate failures, collect tracebacks, group by likely root cause, and apply platform-specific triage guidance (e.g., references/TEST_FAILURE_TRIAGE_PYTHON.md) if present."
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# Test Runner & Failure Triage

Run tests to **verify health** and, if anything fails, produce **analysis-only triage**. This skill is *read-only*: it never edits code, tests, configuration, or dependencies.

## When to use

- At the **start of work** to establish baseline health (prefer full suite).
- After changes to a component to run a **focused test scope**.
- At the **end of work** to confirm the **full suite** still passes.
- Any time you need **failure analysis** without attempting a fix.

## Non-negotiables

- **No modifications** to code/tests/config/deps while this skill runs.
- **No “make-it-pass” behavior.** Diagnose only.
- **Group failures by suspected underlying cause**, not by test name or traceback surface.
- If confidence is low, **report and stop** (do not guess).

## Decision tree

- If the request mentions “full test suite”, “all tests”, “before starting”, “final validation” → **run full suite**.
- If the request mentions a file/module/component → **run targeted scope**:
    - Prefer directory/module tests if repo conventions exist.
    - Otherwise run `pytest` with explicit paths or selectors.
- If any tests fail → run **ON_FAIL** protocol (below).

## Quick start (Python / pytest)

Typical commands (adapt to repo conventions discovered in `AGENTS.md` / `README.md` / `pyproject.toml`):

- Full suite:
    - `pytest`
- Target a test module:
    - `pytest tests/test_example.py`
- Target a single test:
    - `pytest tests/test_example.py::test_case_name`
- Filter by keyword:
    - `pytest -k "keyword"`
- More diagnostics (keep failures going; do not stop at first failure):
    - `pytest -ra --durations=20`

## Workflow

### 1) Lock the execution scope

Record (in the report):

- What scope is being run (full suite / module(s) / test(s))
- Why that scope is appropriate for the invocation context

### 2) Pre-flight discovery (minimal)

Confirm how tests are intended to run in this repo:

- Look for `AGENTS.md`, `README.md`, `pytest.ini`, `pyproject.toml`, `tox.ini`, `noxfile.py`, `Makefile`, `tasks.py`, other characteristic files. 
- Prefer repository-documented commands if present

Capture basic environment metadata (report it):

- OS and shell context (if available)
- `python --version`
- `pytest --version`
- Any repo-specific test settings discovered (markers, config, plugins)

### 3) Execute tests

Run tests with settings that help diagnosis and preserve all failures:

- Prefer *not* using `-x` or `--maxfail=1` (you must enumerate all failures).
- Prefer including:
    - `-ra` (extra summary)
    - `--durations=20` (slow tests)
- If output is too verbose, you may rerun a **narrower failing scope** after you’ve enumerated failures.

### 4) PASS path

If all tests pass:

- Report:
    - scope executed
    - pass status
    - summary counts and durations (if available)
- Stop. Do not add extra analysis.

---

## ON_FAIL protocol (mandatory)

If any test fails, do **all** of the following **without modifying the repo**.

### A) Enumerate failures (complete list)

For each failing test (and each error in collection):

- Test identifier (file::test_name)
- Failure type (assertion, exception, import, collection error, etc.)
- Full traceback (or the minimal excerpt that retains root-cause context)
- Any captured stdout/stderr that appears causal

### B) Collect diagnostics

Capture, as available:

- `pytest` summary (`-ra` output)
- Failing test list and counts
- Tracebacks and exception types
- Environment info recorded in pre-flight

If the failure looks environment/config-dependent, optionally include:

- relevant env vars (only those that appear test-related; do not dump secrets)
- active virtual env name/path if obvious
- dependency lock context if repo provides it (e.g., `uv.lock`, `poetry.lock`, `requirements*.txt`)

### C) Group failures by suspected underlying cause

Group by **cause hypothesis**, not by superficial similarity.

Typical buckets:

- **Import / resolution failures** (collection/import errors, missing symbols)
- **Environment / configuration failures** (paths, permissions, missing binaries)
- **Source code logic failures** (implementation deviates from contract)
- **Test logic / test assumption failures** (test expects wrong behavior)
- **Flake / timing / nondeterminism** (if strongly evidenced)
- **Unknown / ambiguous** (call out what blocks confident classification)

For each group:

- List included failing tests
- Provide the minimal evidence supporting the grouping (shared traceback root, same exception type, same missing symbol, same fixture error, etc.)

### D) Apply platform-specific triage guidance (hierarchical design)

If a platform-specific triage document exists, load and apply it **only after failures occur**.

For Python, check for:

- `references/test_failure_triage_python.md` (or repo-local equivalent)

Rules:

- Platform-specific triage **refines** the generic classification.
- If the document conflicts with generic classification, **report the conflict** and prefer the repository policy.
- If no platform-specific triage exists, remain in generic triage mode.

### E) Produce the structured failure report

Your output must include:

- Scope executed + rationale
- Test command(s) used
- Pass/fail status
- Failure enumeration (complete)
- Failure grouping + classification
- Most likely root causes per group (with evidence)
- Ambiguities / missing info (if any)
- Recommended next role to invoke (e.g., refactoring planner, feature implementer, test author), **without proposing fixes**

---

## Abort rules

Abort analysis (still producing the report) if:

- Failures cannot be classified with reasonable confidence from repo evidence
- The working tree state prevents safe reasoning (unexpected or confusing changes)
- Test execution is impossible due to missing tooling and repo docs don’t specify remediation

In abort mode, include:

- what you could run
- what you could not run
- what information is required for next steps

---

## Report artifact

Write a single primary report artifact:

- `TEST_RUN_REPORT.md`

Suggested structure:

1. Context and scope
2. Commands executed
3. Environment summary
4. Results summary
5. Failures (enumerated)
6. Failure groups and classifications
7. Ambiguities / risks
8. Suggested next skill (non-binding)

(If the repo uses a different artifacts convention, follow it.)

---

## Prohibitions (explicit)

This skill must not:

- edit any files
- add dependencies
- modify `pyproject.toml`, `pytest.ini`, `conftest.py`, etc.
- “patch around” failures (aliases, shim imports, broad try/except, assertion weakening)
- run unrelated cleanup/refactors

It only diagnoses and reports.

---

## References

- `references/test_failure_triage_python.md` (loaded only if tests fail; may be repo-local)

---
