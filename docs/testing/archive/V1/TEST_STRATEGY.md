---
doc_id: TEST_STRATEGY
name: TEST_STRATEGY.md
title: Test Strategy
kind: testing
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: |-
  Project-wide testing governance. Defines test layers, oracle spec workflow, translation rules, determinism requirements,
  and change-control rules for AI-assisted development.
url: https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
references:
  - PROJECT
  - ARCHITECTURE
  - DECOMPOSITION
---

# TEST_STRATEGY

## 1. Purpose

This document defines the **project-wide testing governance** for AI-assisted development.

It exists to ensure that:

- correctness claims are **auditable** and grounded in authoritative docs,
- tests are **refactor-safe** (avoid implementation-detail coupling),
- deterministic execution is enforced (virtual-time and seeded behavior),
- test failures can be triaged and fixed without speculation.

This file is **not** a catalog of test cases. Individual test cases are specified only in `docs/testing/oracles/*_TEST_ORACLE.md`.

---

## 2. Layer model (normative)

This project uses four-layer testing system:

1. **Strategy (this file)**: governance and constraints.
2. **Oracle specs**: normative, non-executable test definitions (`*_TEST_ORACLE.md`).
3. **Oracle implementations**: executable pytest modules (`tests/*.py`) translating oracle cases.
4. **Run reports**: observational artifacts capturing a specific test run (`TEST_RUN_REPORT_*`).

**Non-negotiable separation rule**:

- Strategy defines *how* correctness may be asserted.
- Oracle specs define *what* correctness means.
- Pytest executes oracle specs; pytest is never the primary authority.
- Run reports record what happened; they define nothing.

---

## 3. Authority model (what defines correctness)

Correctness must be grounded in **normative documentation** under `docs/` per the documentation system.

### 3.1 Allowed authority sources for oracle specs

Oracle specs may cite:

- Core rules/specs under `docs/specs/core/`
- Shell specs under `docs/specs/shell/`
- Other specs under `docs/specs/`
- Component boundaries (`@ARCHITECTURE`, `@DECOMPOSITION`)
- Explicit gate requirements (`@ACCEPTANCE_GATES`)
- Docstrings that are explicitly declared normative by the relevant spec

### 3.2 Prohibited authority sources

- Current implementation behavior (“it does X today”) unless explicitly documented as intended.
- Accidental properties of an implementation (private fields, incidental ordering, formatting quirks).
- “Common knowledge Tetris rules” unless codified in the repo’s normative docs.

If authority is missing or ambiguous, the correct action is:

- **stop and escalate** (do not invent test expectations).

---

## 4. Test layers (aligned to architecture)

The architecture mandates a **pure deterministic core** and an **impure shell**. Test layers follow that split.

### 4.1 Core unit tests (mandatory)

**Scope**

- `tetris.core` only (pure simulation).
- No I/O, no timing, no rendering, no OS input.

**Allowed assertions**

- Exact state transition equality (or structured comparisons).
- Invariants over board/piece/score/state machine.
- Deterministic error handling.

**Prohibited**

- Real-time assumptions.
- Terminal/ASCII rendering semantics (belongs to renderer layer).
- OS input behavior (belongs to input driver/controller layer).

### 4.2 Pure renderer unit tests (mandatory once renderer exists)

**Scope**

- `tetris.rendering` (pure function `render(state) -> str`).

**Allowed assertions**

- Deterministic output for known states.
- Formatting rules exactly as specified by `@RENDERING_SPEC`.

**Prohibited**

- Terminal presenter behavior (cursor control, clearing).
- Timing assumptions.

### 4.3 Runtime integration tests (mandatory once runtime exists)

**Scope**

- `tetris.runtime` orchestrating: input → step → render → present.

**Allowed assertions**

- Deterministic behavior in **scripted/virtual time** mode.
- Event sequencing invariants (one `step()` per tick).
- Replay/script equivalence (when replay exists).

**Prohibited**

- Real-time sleep-based behavior as an oracle (interactive mode is optional and not a correctness gate).
- OS-specific input behavior unless an explicit gate introduces it.

### 4.4 CLI smoke tests (optional / minimal)

**Scope**

- CLI wiring only.

**Allowed assertions**

- Exit code, basic invocation, deterministic scripted mode runs.

**Prohibited**

- End-to-end interactive UI correctness unless explicitly gated later.

---

## 5. Determinism requirements (global)

Determinism is a system-level invariant (see architecture).

### 5.1 Virtual time is the baseline oracle surface

- All correctness gates must be satisfiable under virtual-time scripted runs.

### 5.2 Randomness policy

- If randomness exists (e.g. piece generation), it must be:
    - seeded, and
    - part of explicit state, or injected as a deterministic generator.

Unseeded RNG in core or tests is forbidden.

### 5.3 Time policy

- `time.sleep` is forbidden in correctness oracles.
- Timing-dependent tests are forbidden unless explicitly gated and made deterministic.

---

## 6. Oracle specs (normative, non-executable)

### 6.1 Location

Oracle specs live only under:

`docs/testing/oracles/`

### 6.2 Required IDs (traceability)

Each oracle spec file must define:

- `ORACLE_ID: <DOMAIN>_TEST_ORACLE` (the `@DOC_ID`)

IDs are stable and never reused for different semantics.

### 6.3 Domain decomposition

Oracle specs must be decomposed by subsystem/domain. At minimum:

- core
    - `CORE_TEST_ORACLE.md` (core invariants + step semantics)
    - `SHAPES_ROTATION_TEST_ORACLE.md` (shape definitions + rotation rules)
    - `COLLISION_TEST_ORACLE.md` (collision and lock conditions)
    - `LINE_CLEAR_TEST_ORACLE.md` (line clear semantics)
    - `SCORING_TEST_ORACLE.md` (score deltas per event)
- shell
    - `RUNTIME_TEST_ORACLE.md` (tick orchestration invariants, scripted mode)
    - `RENDERING_TEST_ORACLE.md` (ASCII rendering semantics)

(These names may be refined, but the decomposition principle is mandatory.)

---

## 7. Oracle implementations (pytest translations)

### 7.1 Mapping rule

Each oracle spec should have a corresponding pytest module:

- `docs/testing/oracles/<domain>_TEST_ORACLE.md`
→ `tetris/tests/test_<domain>_from_oracle.py`

### 7.2 Traceability rule (mandatory)

Every pytest translation module must:

- reference the oracle spec path(s) it implements,
- list `ORACLE_ID(s)`,
- ensure each test case references the corresponding `CASE_ID`.

### 7.3 Assertion rule

Pytest translations must not assert behavior beyond the oracle spec,
except minimal harness constraints required to execute the test.

---

## 8. Run reports (observational)

Each full-suite execution by S7 or bug-fixer must produce a run report artifact:

- `artifacts/test_runs/TEST_RUN_REPORT_<timestamp>.md` (or repo-equivalent)

Run reports must include:

- command(s) executed
- scope (full vs focused)
- environment snapshot (Python + pytest versions)
- pass/fail summary
- failure enumeration (with tracebacks)
- failure grouping/classification
- recommended next action (S6 vs bug-fixer vs S4 update)

Run reports must not define expected behavior.

---

## 9. Change control (code vs tests vs oracle specs)

When a pytest test fails, the failure must be classified into exactly one primary bucket:

### A) Code violates oracle spec

- Oracle spec is valid and grounded in authority.
- Pytest translation is faithful.

→ Fix code.

### B) Pytest translation violates oracle spec / is brittle

- Oracle spec is valid.
- Test asserts extra behavior or is incorrectly implemented.

→ Fix pytest translation (keep oracle spec unchanged).

### C) Oracle spec is outdated or wrong

- Requires high-bar evidence that authoritative intent changed.

→ Update oracle spec, then update pytest translation.

### Global prohibitions

- “Just-to-pass” changes in code or tests.
- Any failure suppression (xfail/skip, warning filters, broad try/except).
- Aliases/stubs/shims/compat exports created to satisfy tests.
- Weakening assertions without replacement by equally meaningful assertions.

---

## 10. Skill responsibilities and I/O contracts

### S4 — Test Strategy Designer

**Inputs**

- `PROJECT.md`, `ARCHITECTURE.md`, `DECOMPOSITION.md`
- `PHASES.md`, `ACCEPTANCE_GATES.md` (when present)
- current test tree and configs

**Outputs**

- this file (`TEST_STRATEGY.md`) and optional conventions docs

**Constraints**

- no code/test mutation

### S6 — Test Author

**Inputs**

- `TEST_STRATEGY.md`
- authoritative behavior specs and docstrings
- relevant `*_TEST_ORACLE.md` files (existing or to be created)

**Outputs**

- new/updated `*_TEST_ORACLE.md` files
- pytest translations in `tetris/tests/`
- short authoring notes (where repo policy expects)

**Constraints**

- no invention of correctness without authority

### S7 — Test Runner & Failure Triage

**Inputs**

- repo state + requested scope
- triage references

**Outputs**

- run report artifact(s)

**Constraints**

- strictly no mutation

### bug-fixer

**Inputs**

- full-suite failures + run report
- `TEST_STRATEGY.md` + relevant oracle specs
- triage doc for fixing

**Outputs**

- minimal fixes to code/tests (strict constraints)
- focused re-runs + final full-suite pass report

**Constraints**

- does not fix config/environment failures; diagnoses only
- no aliasing/stubbing/suppression

---
