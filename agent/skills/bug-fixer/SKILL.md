---
name: "bug-fixer"
description: "Use when tests are failing and the task is to diagnose, prioritize, and fix bugs in code or tests under strict anti-speculation rules: run the full test suite, perform detailed failure triage (using platform-specific guidance when available), assess fixability and severity, apply minimal correct fixes, run focused tests after each fix, and iterate until the full suite passes."
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# Bug Fixer

Diagnose and **correctly fix** failing tests and underlying bugs without speculation, shortcuts, or behavior drift. This skill is **mutation-authorized**, but only within tight constraints.

## When to use

- Tests are failing and **fixing is explicitly required**
- After refactors where tests may be out of sync with correct code behavior
- When failures indicate localized, well-defined bugs
- When repeated failures suggest a common underlying cause

Do **not** use this skill for:

- Pure diagnostics (use *Test Runner & Failure Triage*)
- Feature development
- Refactoring for structure or style
- Configuration or environment repair

---

## Non-negotiables

- **No “just-to-pass” fixes** — in code *or* tests
- **No aliasing, stubs, shims, or compatibility hacks**
- **No error suppression** (broad `try/except`, warnings filters, skips)
- **No speculative behavior** not supported by documentation or code evidence
- **Configuration / environment failures are not fixed** here
- All changes must be:
    - minimal
    - localized
    - evidence-backed
    - reversible

---

## Decision tree

- If the request is to *assess health only* → stop and use *Test Runner & Failure Triage*
- If failures are **environment / configuration** → diagnose and report only
- If failures are **test–code mismatch after refactor** → high-priority test fixes
- If failures indicate **localized code bugs** → prioritize and fix
- If failures suggest **shared root cause** → treat as a batch, not individually

---

## Workflow

### 1) Run the full test suite (mandatory)

- Always begin with the **entire test suite**
- Capture:
    - exact command
    - scope
    - Python / test framework versions
    - relevant config sources
- Preserve full failure output

This establishes the **baseline failure set**.

---

### 2) Enumerate and classify failures

Apply full triage:

- Enumerate all failing tests
- Group by **likely root cause**
- Classify each group as:
    - Import / resolution
    - Test logic
    - Source code logic
    - Environment / configuration

If a platform-specific triage document exists, load and apply it **only after failures occur**.

For Python, check for:

- `references/test_failure_triage_fix_python.md` (or repo-local equivalent)

Rules:

- Platform-specific triage **refines** the generic classification.
- If the document conflicts with generic classification, **report the conflict** and prefer the repository policy.
- If no platform-specific triage exists, remain in generic triage mode.

---

### 3) Assess fixability & severity (fixing perspective)

For each failure group, assess:

#### A) Environment / configuration failures

- **Not fixable by this skill**
- Produce detailed diagnostics only
- Exclude from fix loop

#### B) Test–code desynchronization (HIGH PRIORITY)

- Tests fail because code behavior changed intentionally
- Fixing tests is allowed **only if** evidence shows:
    - code behavior matches documentation, docstrings, or explicit design notes
- Required evidence must be cited before modifying tests

These are typically **easy, high-value fixes**.

#### C) Source code logic failures

Prioritize based on:

1. **Localization**
    - Single function / method
    - Narrow diff surface
2. **Multiplicity**
    - Multiple tests failing for the same reason
3. **Clarity**
    - Failure message points clearly to incorrect logic

---

### 4) Fix loop (one issue at a time)

For each selected failure group:

1. **Confirm scope**
    - Identify the minimal code/test surface involved
2. **Apply the fix**
    - Code fix *or* test fix — never both speculatively
3. **Optional: add a focused test**
   Allowed **only if**:
    - the bug exposes an untested edge case, or
    - the fix could plausibly introduce a regression
   The test must be:
    - narrowly scoped
    - directly tied to the diagnosed bug
    - clearly documented as part of the fix
4. **Run focused tests**
    - Only the tests relevant to this fix
5. **Watch for cascading failures**
    - A later assertion may now fail for a *different* reason
    - Re-classify if necessary before continuing

Repeat until all tests in this failure group pass.

---

### 5) Full suite verification

After a group is resolved:

- Run the **full test suite**
- If new failures appear:
    - classify them
    - determine whether they are regressions or pre-existing masked failures
- Continue with the next highest-priority group

Repeat until:

- the full test suite passes, or
- remaining failures are exclusively configuration/environmental

---

## Test modification rules (strict)

Tests may be modified **only** when:

- They encode outdated assumptions
- They contradict documented behavior
- They no longer reflect refactored but correct code logic
- There is an evidence-backed test logic error

Modified tests must:

- Assert **meaningful behavior**
- Reflect actual invariants
- Never be weakened to silence failures

---

## Explicit prohibitions

The bug fixer must not:

- create aliases or forwarding functions
- add dummy exports or placeholder identifiers
- weaken assertions without replacement
- mark tests as `xfail` or `skip` to pass
- catch exceptions broadly to hide errors
- change configuration to mask failures
- introduce speculative behavior

Violations invalidate the fix.

---

## Reporting requirements

At completion, report:

- Initial failure groups and classifications
- Fixes applied (code/tests)
- Evidence used to justify test updates
- Any focused tests added (with rationale)
- Remaining unfixed failures (if any) and why
- Confirmation that the **full test suite passes**

---

## Summary contract

> **Bug Fixer diagnoses, prioritizes, and correctly fixes failing tests and bugs using evidence-driven minimal changes, iterating through focused fixes and full-suite validation until the project is stable — without hacks, shortcuts, or speculation.**

## References

- `references/test_failure_triage_fix_python.md`  
  Platform-specific failure classification and evidence rules. Must be consulted before any fix decisions.

---
