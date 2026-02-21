---
doc_id: TESTING_CONVENTIONS
name: TESTING_CONVENTIONS.md
title: Testing Conventions
status: active
authority: normative
urls:
  - https://chatgpt.com/c/698975ae-3688-8397-92a7-8c7fbe698b2e
  - https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [TEST_STRATEGY]
---

# TESTING_CONVENTIONS

## 1. Purpose

This document defines repository-specific **mechanical conventions** for implementing the testing strategy defined in `TEST_STRATEGY.md`.

It specifies:

- Directory layout for test artifacts
- Oracle specification organization
- Naming patterns and ID formats
- Oracle-to-pytest translation rules
- Determinism enforcement mechanics
- Run report conventions

It does **not** define:

- What correctness means
- What may be asserted
- Authority derivation rules
- Change-control policy

Those are defined in `TEST_STRATEGY.md`.

This document defines **how** testing decisions are encoded in this repository.

---

# 2. Test Artifact Structure

## 2.1 Oracle Specifications

Oracle specifications are normative testing documents:

- `kind: testing`
- `authority: normative`

They are organized by architectural scope:

Core-level:
```

docs/testing/oracles/core/

```

Shell-level:
```

docs/testing/oracles/shell/

```

Each oracle document governs exactly **one behavioral domain**.

Examples of domains:

- collision and bounds
- geometry and rotations
- spawn semantics
- gravity and locking
- line clearing
- scoring
- RNG behavior
- game-over conditions
- invariants
- rendering
- runtime orchestration
- CLI behavior
- replay execution
- configuration boundaries

No monolithic oracle documents are allowed.

If cross-domain traceability is required, it must be expressed in an index document (e.g., `ORACLE_*_INDEX.md` and corresponding machine-readable index).

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
├── config/
└── shared/

```

Each directory mirrors an oracle domain.

Cross-domain mixing inside a single module is forbidden.

---

# 3. Naming Conventions

## 3.1 Oracle File Naming

Format:

```

ORACLE_<SCOPE>_<DOMAIN>.md

```

Examples:

- `ORACLE_CORE_COLLISION.md`
- `ORACLE_CORE_GRAVITY_AND_LOCKING.md`
- `ORACLE_SHELL_RENDERING.md`

Rules:

- File name must match the declared `doc_id`.
- Exactly one domain per file.
- File renaming requires corresponding metadata update.
- Oracle files must not contain implementation guidance.

---

## 3.2 ORACLE_ID Format

Format:

```

ORACLE_<SCOPE>_<DOMAIN>

```

Examples:

- ORACLE_CORE_COLLISION
- ORACLE_CORE_RNG_7BAG
- ORACLE_SHELL_RUNTIME

Rules:

- ORACLE_ID equals the `doc_id`.
- Stable and never reused.
- Never semantically repurposed.

---

## 3.3 CASE_ID Format

Format:

```

CASE_<SCOPE>*<DOMAIN>*<NNN>

```

Examples:

- CASE_CORE_COLLISION_001
- CASE_CORE_GRAVITY_002
- CASE_SHELL_RUNTIME_004

Rules:

- Each CASE_ID belongs to exactly one ORACLE_ID.
- Stable and unique.
- Never reused.
- Never renumbered retroactively.
- Once published, must not change semantic meaning.

---

## 3.4 Pytest Module Naming

Format:

```

test_<domain>.py

```

Examples:

- `test_collision.py`
- `test_gravity.py`
- `test_runtime.py`

One translation module per oracle domain.

---

## 3.5 Test Function Naming

Format:

```

test_<case_id_lowercase>()

```

Example:

```

test_case_core_collision_001()

```

The CASE_ID must appear in:

- the test function name, or
- a comment directly above the test.

No test may exist without an associated CASE_ID.

---

# 4. Oracle-to-Pytest Translation Rules

## 4.1 Module Header (Mandatory)

Each pytest module must declare:

- The oracle document path
- The ORACLE_ID implemented

Example:

```

Implements:

* docs/testing/oracles/core/ORACLE_CORE_COLLISION.md
* ORACLE_CORE_COLLISION

```

---

## 4.2 Case Mapping

Each CASE_ID defined in an oracle document must:

- Be implemented exactly once in pytest, and
- Map to one deterministic assertion block.

No CASE_ID may:

- Exist without a test,
- Be implemented multiple times,
- Be merged across domains.

Parametrization is allowed only when:

- Structure is identical, and
- CASE_ID mapping remains explicit and visible.

Dynamic test generation that obscures CASE_ID traceability is forbidden.

---

# 5. Determinism Enforcement Mechanics

## 5.1 Randomness

- All RNG must be seeded.
- Tests must inject deterministic seed values.
- No use of unseeded random sources.
- No reliance on ambient entropy.

---

## 5.2 Time

- No use of `time.sleep()` in tests.
- Runtime tests must use virtual-time stepping.
- Tests must not depend on wall-clock timing.
- Frame advancement must be deterministic.

---

## 5.3 Replay Tests

Replay tests must:

- Load replay traces deterministically.
- Assert full-state equivalence when specified.
- Avoid heuristic comparisons.

Partial comparison is allowed only if explicitly defined in the oracle.

---

# 6. Fixtures and Utilities

## 6.1 Fixture Placement

- Domain-specific fixtures live inside their domain directory.
- Shared fixtures go in `tetris/tests/conftest.py` or `shared/`.

---

## 6.2 Fixture Constraints

Fixtures must not:

- Mutate global state.
- Depend on environment variables.
- Depend on filesystem unless explicitly required by shell tests.
- Introduce non-deterministic behavior.

---

# 7. Regression Test Additions

When a defect is discovered:

1. Update the appropriate `ORACLE_*` document first.
2. Add or refine the corresponding CASE_ID.
3. Implement the pytest translation.
4. Ensure ORACLE_ID and CASE_ID traceability.

Tests must not precede normative oracle definition.

Test-first changes are allowed only if the oracle is updated in the same change set.

---

# 8. Run Report Conventions

Test reports must be stored in:

```

docs/testing/reports/

```

Recommended naming:

```

TEST_RUN_<YYYYMMDD>_<HHMMSS>.md

```

Reports must include:

- Timestamp
- Python version
- pytest version
- Suite executed
- Pass/fail counts
- Failing CASE_ID references

Reports are append-only unless explicitly reset by governance decision.

---

# 9. Optional Pytest Markers

If markers are used, they must reflect architectural scope only:

- `@pytest.mark.core`
- `@pytest.mark.shell`
- `@pytest.mark.runtime`
- `@pytest.mark.rendering`
- `@pytest.mark.replay`
- `@pytest.mark.cli`
- `@pytest.mark.config`

Markers must not encode policy or gate status.

---

# 10. Mechanical Prohibitions

The following are mechanically forbidden:

- Tests without CASE_ID mapping.
- Multiple domains inside a single translation module.
- Cross-domain imports violating architectural boundaries.
- Snapshot tests outside renderer domain unless explicitly authorized.
- Weakening assertions without oracle update.
- Hardcoded values not traceable to normative documentation.
- Silent test skipping.
- Conditional weakening of invariants.

---

# 11. Relationship to Strategy

`TEST_STRATEGY.md` defines:

- What may be asserted.
- What constitutes correctness.
- Authority and governance rules.
- Change control policy.

This document defines only the mechanical encoding of those decisions.
