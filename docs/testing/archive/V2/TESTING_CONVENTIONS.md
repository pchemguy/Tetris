---
doc_id: TESTING_CONVENTIONS
name: TESTING_CONVENTIONS.md
title: Testing Conventions
kind: testing
scope: global
status: active
authority: normative
references:
  - TEST_STRATEGY
url: https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# TESTING_CONVENTIONS

## 1. Purpose

This document defines repository-specific mechanical conventions for implementing the testing strategy defined in `TEST_STRATEGY.md`.

It specifies:

- Directory layout for test artifacts
- Oracle specification organization
- Naming patterns and ID formats
- Oracle-to-pytest translation rules
- Determinism implementation mechanics
- Run report conventions

It does **not** define:

- What correctness means
- What is allowed to be asserted
- Change-control policy
- Oracle authority sources

Those are defined in `TEST_STRATEGY.md`.

---

# 2. Test Artifact Structure

## 2.1 Oracle Specifications

Oracle specs are authoritative correctness documents.

They are organized as follows:

### Core-Level Oracles

Directory:
```

docs/testing/oracles/core/

```

Mandatory:

- `CORE_TEST_ORACLE.md`

This document defines correctness of the pure simulation core.

---

### Shell-Level Oracles

Directory:
```

docs/testing/oracles/shell/

```

Mandatory:

- `RENDERING_TEST_ORACLE.md`
- `RUNTIME_TEST_ORACLE.md`
- `CLI_TEST_ORACLE.md`
- `REPLAY_TEST_ORACLE.md`
- `CONFIG_TEST_ORACLE.md`

Each oracle file governs a single subsystem domain.

No monolithic oracle files are allowed.

---

## 2.2 Pytest Layout

All executable tests live under:

```

tetris/tests/

```

Recommended structure:

```

tetris/tests/
├── core/
├── rendering/
├── runtime/
├── cli/
├── replay/
└── config/

```

Each directory mirrors the oracle domain.

---

# 3. Naming Conventions

## 3.1 Oracle File Naming

Format:

```

<DOMAIN>_TEST_ORACLE.md

```

Examples:

- `CORE_TEST_ORACLE.md`
- `RENDERING_TEST_ORACLE.md`

---

## 3.2 ORACLE_ID Format

Format:

```

<DOMAIN>_TEST_ORACLE

```

Examples:

- CORE_TEST_ORACLE
- RUNTIME_TEST_ORACLE

Rules:

- IDs must be stable.
- IDs must never be reused.
- IDs must not be renumbered retroactively.

---

## 3.3 CASE_ID Format

Format:

```

CASE_<DOMAIN>_<NNN>

```

Examples:

- CASE_CORE_STEP_GRAVITY_001
- CASE_RENDER_FRAME_EMPTY_BOARD_002

Rules:

- Stable and unique.
- Never reused.
- Never semantically repurposed.

---

## 3.4 Pytest Module Naming

Format:

```

test_<domain>.py

```

Examples:

- `test_core.py`
- `test_rendering.py`

One translation module per oracle domain.

---

## 3.5 Test Function Naming

Format:

```

test_<case_id_lowercase>()

```

Example:

```

test_case_core_step_gravity_001()

```

CASE_ID must appear in:

- test name or
- comment directly above test.

---

# 4. Oracle-to-Pytest Translation Rules

## 4.1 Module Header (Mandatory)

Each pytest module must include:

- Path to oracle file
- Implemented ORACLE_ID(s)

Example header:

```

Implements:

* docs/testing/oracles/core/CORE_TEST_ORACLE.md
* ORACLE_CORE_001

```

---

## 4.2 Case Mapping

Each CASE_ID must map to:

- A distinct test function, OR
- A parametrized case with explicit CASE_ID reference.

No CASE_ID may exist without a pytest translation.

---

## 4.3 Parametrization

Allowed:

- Parametrize when structure identical and only inputs vary.

Not allowed:

- Dynamic test generation that obscures CASE_ID mapping.
- Indirect parameter generation without traceability.

---

# 5. Determinism Mechanics

This section defines mechanical enforcement of determinism.

## 5.1 Randomness

- All RNG must be seeded.
- Tests must inject deterministic seed values.
- No use of unseeded random sources.

---

## 5.2 Time

- No use of `time.sleep()` in tests.
- Runtime tests must use virtual time stepping.
- Frame advancement must be deterministic.

---

## 5.3 Replay Tests

Replay tests must:

- Load replay traces deterministically.
- Assert full-state equivalence where specified.
- Avoid partial or heuristic comparisons.

---

# 6. Fixtures and Utilities

## 6.1 Fixture Placement

- Domain-specific fixtures live inside their respective test directories.
- Shared fixtures go in `tetris/tests/conftest.py`.

---

## 6.2 Core Fixtures

Examples:

- `empty_board`
- `single_piece_state`
- `deterministic_seed`

Fixtures must not:

- Mutate global state.
- Depend on environment variables.
- Depend on filesystem unless explicitly part of shell tests.

---

# 7. Regression Test Additions

When bug-fixer introduces a regression test:

1. Add CASE_ID to appropriate oracle file.
2. Implement pytest translation.
3. Ensure naming and traceability rules are followed.

Mechanical rules only — authority rules are in `TEST_STRATEGY.md`.

---

# 8. Run Report Conventions

Test run reports must be named:

```

TEST_RUN_REPORT.md

```

Location:

```

docs/testing/reports/

```

Reports must contain:

- Timestamp
- Suite executed
- Python version
- pytest version
- Pass/fail counts
- Failing CASE_ID references

Reports are append-only unless explicitly reset.

---

# 9. Markers (Optional)

If pytest markers are used:

- `@pytest.mark.core`
- `@pytest.mark.shell`
- `@pytest.mark.replay`

Markers must reflect architectural domain only.
Markers must not encode policy decisions.

---

# 10. Mechanical Prohibitions

The following are mechanically forbidden:

- Tests without CASE_ID mapping.
- Multiple domains in a single translation module.
- Cross-domain imports violating architectural boundaries.
- Snapshot tests outside rendering oracle domain.
- Hidden state mutation across tests.

---

# 11. Relationship to Strategy

`TEST_STRATEGY.md` defines:

- What may be asserted.
- What constitutes correctness.
- When changes are allowed.

This document defines only how those decisions are encoded in this repository.

---
