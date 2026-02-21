---
name: TESTING_SYSTEM_01.md
description: Canonical, AI-oriented testing system specification for this repository. Defines governance (TEST_STRATEGY.md), normative oracle specs (*_TEST_ORACLE.md), executable implementations (pytest), and observational run reports (TEST_RUN_REPORT.md), plus how skills S4/S6/S7 and bug-fixer interact with these layers.
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# Testing System

This document specifies the testing system used for AI-assisted development in this repository. It defines **layers**, **artifacts**, **scope boundaries**, **inputs/outputs**, and **skill interactions** so that test creation, execution, and fixing remain **auditable**, **non-speculative**, and **refactor-safe**.

## Design goals

- **Separation of concerns**: governance vs truth-spec vs execution vs observation.
- **Non-speculative changes**: tests and code are changed only with evidence.
- **Traceability**: failing executable tests can be mapped to normative oracle cases.
- **Refactor resilience**: oracle specs represent stable behavior; implementations may change without redefining truth.
- **Skill composability**: S4/S6/S7 and bug-fixer can operate with minimal coupling and predictable handoffs.

---

## Layer model

The testing system is intentionally layered:

1. **Strategy (Governance)**: defines *how* correctness may be asserted.
2. **Oracle Specs (Normative, non-executable)**: define *what* correctness means.
3. **Oracle Implementations (Executable, pytest)**: execute oracle specs.
4. **Run Reports (Observational)**: record what ran and what happened.

Each layer has exactly one responsibility. Mixing responsibilities is a structural error.

---

## Canonical repository layout

This system assumes a decomposition-friendly layout (adjust paths if your repo differs, but keep the same semantics):

```
docs/testing/
  TEST_STRATEGY.md
  oracles/
    CORE_TEST_ORACLE.md
    ROTATION_TEST_ORACLE.md
    IO_CONTRACT_TEST_ORACLE.md
...
tests/
  test_core_from_oracle.py
  test_rotation_from_oracle.py
  test_io_contract_from_oracle.py
...
artifacts/test_runs/
  TEST_RUN_REPORT_YYYYMMDD_HHMMSS.md
...
```

Notes:
- `TEST_STRATEGY.md` is **one per project**.
- `docs/testing/oracles/` contains **many** oracle spec files, each scoped by subsystem/domain.
- `tests/` contains executable translations; these are **derivative artifacts**.
- `artifacts/test_runs/` contains run-scoped reports. Do not store run reports in oracle/spec directories.

If your repo already has an artifacts convention, follow it. The key is that **run reports are not strategy and not specs**.

---

## Layer 1 — Strategy (Governance)

### Artifact

- `docs/testing/TEST_STRATEGY.md` (project-wide, high-level, non-executable)

### Scope and authority

- **One per project** (single authoritative strategy).
- Governs all oracle specs, pytest tests, and interpretation/fixing rules.
- Evolves slowly; changes are design decisions.

### Purpose

`TEST_STRATEGY.md` is the **test constitution**. It does not define individual test cases. It defines the rules under which test cases (oracles) are allowed to exist and how they must be implemented.

### Required content (minimum)

1. **Test layers and intent**
    - Define layers (unit / integration / system) and permitted assertion strength.
2. **Oracle governance**
    - When oracle specs are required vs ad hoc tests.
    - Allowed oracle types (invariant, property, metamorphic, golden master, etc.).
    - Accepted sources of truth (PROJECT.md, docstrings, design notes, standards).
3. **Oracle spec format and lifecycle**
    - Required headers and required sections.
    - Stable ID rules (oracle IDs, case IDs).
    - Location rules (where specs live).
4. **Translation policy (oracle spec → pytest)**
    - Mapping rules for filenames and directories.
    - Traceability requirements (pytest tests must reference Case IDs).
    - Prohibition on asserting beyond spec except minimal harness details.
5. **Change control**
    - When code must change vs tests must change vs spec must change.
    - Evidence requirements for modifying:
        - pytest translation,
        - oracle specs,
        - test expectations after refactor drift.
6. **Execution conventions**
       - Full suite vs fast subset conventions.
       - Standard commands and any markers (if used).

### Inputs / Outputs

**Inputs**

- `PROJECT.md`, docstrings, relevant design docs
- repo structure and current test configuration
- prior `TEST_RUN_REPORT`s (optional but useful)

**Outputs**

- `TEST_STRATEGY.md` (primary)
- optional supporting docs: `TESTING_CONVENTIONS.md`, `TEST_PLAN.md`

### Skill mapping: S4

- **S4 (Test Strategy Designer)** owns this layer.
- S4 produces/updates `TEST_STRATEGY.md`.
- S4 does not create individual tests and does not modify code.

---

## Layer 2 — Oracle Specs (Normative, non-executable)

### Artifacts

- `docs/testing/oracles/*_TEST_ORACLE.md`

Examples:

- `CORE_TEST_ORACLE.md`
- `ROTATION_TEST_ORACLE.md`
- `IO_CONTRACT_TEST_ORACLE.md`

### Scope and authority

- **Many files per project**, each scoped to a subsystem/domain.
- Oracle specs define **individual test cases logically**, but are **not executable**.
- Oracle specs are normative: they define correctness claims that implementations must satisfy.

### Purpose

Oracle specs are **formal language definitions of tests**. They exist to:

- prevent pytest tests from becoming accidental specs,
- separate truth claims from test harness details,
- provide an authority basis for bug fixing and refactoring.

### Required structure (recommended canonical template)

Each oracle spec file must include:

1. **Header**
    - Oracle title
    - `ORACLE_ID` (stable)
    - Scope statement (what behavior/contract this covers)
    - Authority basis (what documents define correctness)
2. **Definitions**
    - Terms, assumptions, invariants, constraints
3. **Cases**
   Each case must include:
    - `CASE_ID` (stable)
    - Preconditions / setup
    - Inputs
    - Action
    - Expected outcomes / invariants
    - Notes: acceptable nondeterminism (if any), edge cases, boundaries

### ID conventions (mandatory)

- Oracle ID: `ORACLE_<DOMAIN>_<NNN>`
- Case ID: `CASE_<DOMAIN>_<NNN>`
- IDs must be stable across refactors and test reorganization.

### Inputs / Outputs

**Inputs**

- `TEST_STRATEGY.md` (format + governance)
- authority sources (`PROJECT.md`, docstrings, design notes)
- code structure (for mapping to appropriate scope)

**Outputs**

- new/updated `*_TEST_ORACLE.md` files

### Skill mapping: S6 (Mode A)

- **S6 (Test Author)** creates/updates oracle specs.
- S6 must not invent correctness; if authority is missing, S6 must report ambiguity.

---

## Layer 3 — Oracle Implementations (Executable, pytest)

### Artifacts

- `tests/*.py`

Typical pattern:

- `tests/test_<domain>_from_oracle.py`

### Scope and authority

- Executable tests are **derivative artifacts** that implement oracle specs.
- They are not the ultimate source of truth; the oracle specs are.

### Purpose

Convert oracle specs into runnable pytest tests that:

- execute deterministically where possible,
- validate invariants and expected outcomes,
- provide stable failure signals for bug-fixer.

### Traceability requirements (mandatory)

Every oracle-implementation test module must:

1. Reference the oracle spec file(s) it implements (path + `ORACLE_ID`).
2. Ensure each test case (or parametrized case) references a `CASE_ID`.
3. Avoid asserting any behavior not grounded in oracle spec, except minimal harness details.

Recommended pattern at top of pytest file:

- A short comment block listing:
  - oracle spec path(s)
  - ORACLE_ID(s)
  - mapping notes

### Inputs / Outputs

**Inputs**

- `TEST_STRATEGY.md`
- oracle specs for the domain
- code under test

**Outputs**

- pytest modules implementing oracle cases
- optional shared test utilities only if allowed by strategy/policy

### Skill mapping: S6 (Mode B)

- **S6 (Test Author)** translates oracle specs into pytest.
- S6 should not encode “extra” correctness beyond the oracle spec.

---

## Layer 4 — Run Reports (Observational)

### Artifacts

- `artifacts/test_runs/TEST_RUN_REPORT_<timestamp>.md` (or your repo’s equivalent)

### Scope and authority

- Run-scoped, project-level observational record.
- Records what ran and what happened; never defines correctness.

### Purpose

To provide a durable diagnostic artifact answering:

- What scope was run?
- Under what environment/config?
- What failed (enumeration)?
- How do failures group by root cause?
- What is the recommended next action (S6 vs bug-fixer vs S4 update)?

### Required content (minimum)

1. **Run metadata**
    - timestamp, scope, commands executed
    - invoking role (S7 vs bug-fixer)
2. **Environment snapshot**
    - Python version, pytest version
    - key configs detected (`pytest.ini`, `pyproject.toml`, etc.)
3. **Result summary**
    - counts: pass/fail/error/skip
4. **Failure enumeration**
    - all failing tests/errors with tracebacks
5. **Failure grouping and classification**
    - groups by suspected root cause
6. **Next action recommendation**
    - bug-fixer, S6, or S4 (non-binding)

### Skill mapping: S7

- **S7 (Test Runner & Failure Triage)** produces run reports.
- S7 is strictly diagnostic: **no code/test/config mutation**.

---

## Skill interactions

### S4 — Test Strategy Designer

**Role**: governance author  
**Consumes**: project intent + existing test landscape  
**Produces**: `TEST_STRATEGY.md`  
**Does not**: write tests, write oracle specs, run/fix failures (unless workflow explicitly permits running)

### S6 — Test Author (two-mode)

**Role**: oracle spec author + translation implementer  
**Consumes**: `TEST_STRATEGY.md` + authority sources + code under test  
**Produces**:
- Mode A: `*_TEST_ORACLE.md`
- Mode B: `tests/*.py` implementing cases
**Does not**: implement features; does not “invent correctness”; should avoid broad refactors

### S7 — Test Runner & Failure Triage

**Role**: verifier + diagnostician  
**Consumes**: repo + execution scope + triage references  
**Produces**: `TEST_RUN_REPORT_*`  
**Does not**: modify anything

### bug-fixer (mutation-authorized, strict)

**Role**: diagnose + prioritize + fix within strict constraints  
**Consumes**:
- `TEST_STRATEGY.md` (governance)
- `*_TEST_ORACLE.md` (normative truth claims)
- failing pytest output (from full suite)
- triage doc: `references/test_failure_triage_fix_python.md`

**Produces**:

- code/test fixes (strictly minimal, evidence-backed)
- optional focused tests (only for regression gaps/edge cases)
- updated run reports / fix report notes (repo policy dependent)

**Prohibitions (hard)**

- No aliases, stubs, shims, compatibility exports
- No “just-to-pass” changes in code or tests
- No suppressing failures (xfail/skip, broad try/except, warning filters)
- No fixing environment/config failures (diagnose and report only)

---

## Decision procedure when tests fail (code vs translation vs spec)

When a pytest test fails, the system requires classification into one of three normative outcomes:

### Outcome A — Code violates oracle spec

- Oracle spec defines expected behavior and authority basis is valid.
- Pytest translation faithfully implements the spec.
- Therefore: **fix code**.

### Outcome B — Pytest translation violates oracle spec (or is brittle)

- Oracle spec is correct and stable.
- Pytest test asserts extra behavior, encodes harness mistakes, or has brittle assumptions.
- Therefore: **fix pytest implementation** (keep oracle spec unchanged).

### Outcome C — Oracle spec is wrong/outdated

- Requires high bar:
    - authoritative sources changed or contradict prior spec,
    - clear evidence that intended behavior differs.
- Therefore: **change oracle spec** (and then update translation).
- This should be rare and treated as a design decision.

`TEST_STRATEGY.md` defines:

- which evidence sources are admissible,
- which layer is allowed to change under what conditions.

---

## Standard flows

### Greenfield baseline (recommended)

1. S4: create minimal `TEST_STRATEGY.md`
2. S6(A): create oracle specs for core invariants
3. S6(B): translate oracle specs into pytest
4. S7: run full suite → run report
5. Iterate

### Repair loop (suite failing)

1. S7: run full suite → run report with classifications
2. bug-fixer: apply triage/fix loop using strategy + oracle specs
3. If missing coverage is discovered:
    - S6(A): extend oracle specs
    - S6(B): add translations
4. S7: run full suite gate

---

## Minimal templates

### Oracle spec file template (recommended)

Use this structure for each `*_TEST_ORACLE.md`:

- Title
- ORACLE_ID
- Scope
- Authority basis
- Definitions
- Cases:
    - CASE_ID
    - Preconditions
    - Inputs
    - Action
    - Expected outcomes / invariants
    - Notes / edge cases

### Pytest translation header (recommended)

At the top of each `tests/test_<domain>_from_oracle.py`:

- Oracle spec path(s)
- ORACLE_ID(s)
- Notes about mapping/parametrization
- Link each test (or param case) to CASE_ID(s)

---

## Operational invariants (pin these)

- `TEST_STRATEGY.md` governs, but never enumerates tests.
- `*_TEST_ORACLE.md` defines correctness cases, but is not executable.
- `tests/*.py` executes oracle cases, but is not the source of truth.
- `TEST_RUN_REPORT_*` records what happened, but never defines correctness.
- If a change can’t be justified with admissible evidence, stop and report.

---
