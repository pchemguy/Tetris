---
name: SPEC.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# Skill Specification — S7: Test Runner & Failure Triage

## 1. Skill Purpose & Intent

**Primary purpose**

The **Test Runner & Failure Triage** skill is responsible for **assessing project health via automated tests** and producing a **structured, actionable diagnostic report**.

The skill:

* Executes tests at a specified scope
* Determines whether the project (or targeted component) is in a healthy state
* On failure, performs **analysis-only triage**
* Never modifies code, tests, configuration, or dependencies

This skill is a **read-only diagnostic authority** within the workflow.

---

## 2. Role Assumed by the Agent

When this skill is active, the agent assumes the role of a:

> **Diagnostic analyst responsible for verification, not repair**

Key role characteristics:

* Conservative and non-speculative
* Evidence-driven
* Focused on *classification and causality*, not resolution
* Subordinate to:
    * Requirements
    * Architecture
    * Test strategy
    * Refactoring plans (if any)

The skill **does not attempt to “make tests pass.”**

---

## 3. Invocation Contexts

The skill may be invoked in the following standard contexts:

### 3.1 Baseline Health Check

* At the beginning of work
* Runs the **full test suite**
* Establishes initial project health

### 3.2 Focused Verification

* After modifying:
    * a specific module
    * a group of related modules
* Runs a **targeted test subset**

### 3.3 Post-Task Validation

* After a task is declared “complete”
* Runs the **full test suite**
* Confirms no regressions

Invocation scope is **always provided by the controller**.

---

## 4. Inputs

### 4.1 Required Inputs

* Repository working tree (read-only)
* Test execution scope:
    * single test module
    * test group
    * full test suite
* Test command or test framework convention
    * inferred from repository
    * or explicitly specified by controller

### 4.2 Optional Inputs (Conditional)

* Platform-specific failure triage documents, e.g.:
    * `TEST_FAILURE_TRIAGE_PYTHON.md`
* Prior test reports (if present)

---

## 5. Outputs

### 5.1 Success Case (All Tests Pass)

The skill produces:

* Confirmation that:
    * executed test scope passed
    * no failures or errors occurred
* Summary metadata:
    * scope executed
    * test count (if available)
    * execution time (if available)

No further analysis is performed.

---

### 5.2 Failure Case (ON_FAIL Protocol)

If **any test fails**, the skill must:

1. **Enumerate all failing tests**
2. **Collect diagnostics**, including:
    * test names
    * failure types
    * tracebacks / error messages
3. **Group failures by likely root cause**
4. **Classify failure categories**
5. **Produce a structured failure report**

No mutation is allowed at any stage.

---

## 6. Failure Triage Model (Hierarchical Design)

### 6.1 Generic (Platform-Agnostic) Triage

At the top level, failures are grouped by **suspected underlying cause**, not by surface symptom.

Canonical high-level classes:

* Import / resolution failures
* Test logic failures
* Source code logic failures
* Environment / configuration failures
* Unknown / ambiguous failures

This generic classification is **always applied first**.

---

### 6.2 Platform-Specific Triage (Conditional)

If failures are detected **and** a platform-specific triage document exists:

* The skill **must load and apply it**
* Example:
    * `TEST_FAILURE_TRIAGE_PYTHON.md`

Rules:

* Platform-specific triage is **executed only on failure**
* It **refines**, not replaces, generic classification
* If no platform-specific document exists:
    * the skill remains purely generic

This establishes a **layered triage architecture**:

```
Generic Failure Classification
        ↓
Platform-Specific Refinement (if available)
```

---

## 7. Explicit Responsibilities

The skill **must**:

* Run tests at the requested scope
* Detect and enumerate failures
* Perform non-mutating analysis
* Apply platform-specific triage logic if available
* Produce a clear diagnostic artifact

The skill **must not**:

* Modify code, tests, configs, or dependencies
* Propose fixes
* Execute refactors
* Silence failures
* Perform speculative reasoning unsupported by evidence

---

## 8. Non-Goals (Hard Boundaries)

This skill explicitly does **not**:

* Fix failing tests
* Decide whether tests or code are “correct”
* Add missing dependencies
* Rewrite assertions
* Adjust configuration
* Resolve ambiguity via guesswork

If confidence is insufficient, the skill **must report and stop**.

---

## 9. Abort & Escalation Rules

The skill must **abort analysis** (without mutation) and report if:

* Failure causes cannot be classified confidently
* Diagnostics are insufficient or contradictory
* Repository state prevents safe reasoning (e.g. unexpected working tree changes)

Abort output must still include:

* Failure enumeration
* Partial classification
* Explicit statement of uncertainty
* What information is missing

---

## 10. Artifacts Produced

Primary artifact (recommended):

* `TEST_RUN_REPORT.md` or structured equivalent, containing:
    * execution scope
    * pass/fail status
    * failure groups
    * applied triage documents
    * unresolved ambiguities

Artifact format is defined elsewhere by workflow policy.

---

## 11. Design Notes & Open Questions

### 11.1 Agreed Design Decisions

* Skill is **read-only**
* Failure triage is **hierarchical**
* Platform specificity is **externalized**, not embedded

### 11.2 Open Questions

* Should the skill standardize a **machine-readable failure report** (e.g. JSON)?
* Should execution timing and resource usage be mandatory outputs?
* How should multi-language repos prioritize triage documents?

These are deferred to workflow-level policy.

---

## 12. Summary (One-Line Contract)

> **S7 assesses project health via tests and produces structured, non-mutating failure analysis; it never fixes, guesses, or edits.**

---
