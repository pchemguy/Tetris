---
doc_id: TEST_SUITE_LAYOUT
name: TEST_SUITE_LAYOUT.md
title: Test Suite Layout and Oracle Mapping Rules
status: active
authority: normative
description: Defines the directory structure, ownership rules, and mapping conventions between ORACLE_* documents and automated test suites.
references:
---

# TEST_SUITE_LAYOUT

**Test Suite Layout and Oracle Mapping Rules (Normative)**

---

## 1. Purpose

This document defines:

* how oracle documents map to test directories,
* how test ownership is determined,
* how regression execution resolves test suites,
* structural constraints on the test tree.

This document is independent of acceptance gates.
Acceptance gates reference this document for execution semantics.

---

## 2. Test Root

All automated tests MUST reside under:

```
tetris/tests/
```

No tests may exist outside this directory.

---

## 3. Oracle-to-Test Directory Mapping

### 3.1 Canonical mapping rule

For any oracle document with:

```
doc_id: ORACLE_<SCOPE>_<TOPIC>
```

the corresponding test directory MUST be:

```
tetris/tests/<scope>_<topic>/
```

Transformation rules:

1. Remove the `ORACLE_` prefix.
2. Convert the remainder to lowercase.
3. Preserve underscores exactly.
4. Do not introduce additional normalization.

### 3.2 Examples

| Oracle ID                | Test Directory                  |
| ------------------------ | ------------------------------- |
| `ORACLE_CORE_COLLISION`  | `tetris/tests/core_collision/`  |
| `ORACLE_CORE_API_TYPES`  | `tetris/tests/core_api_types/`  |
| `ORACLE_CORE_RNG_7BAG`   | `tetris/tests/core_rng_7bag/`   |
| `ORACLE_SHELL_RENDERING` | `tetris/tests/shell_rendering/` |

---

## 4. Oracle Ownership Rule

Each oracle owns exactly one test directory.

Rules:

* All tests proving an oracle MUST reside in its mapped directory.
* Tests for different oracles MUST NOT be mixed in a single directory.
* Tests MUST NOT exist without an owning oracle document.
* An oracle directory MUST NOT contain tests that assert behavior outside that oracle's scope.

This ensures:

* traceability,
* deterministic test discovery,
* clean regression recursion,
* elimination of "floating tests".

---

## 5. Oracle Execution Semantics

This document defines how test suites are resolved once an oracle is selected for execution.

Given an oracle ID:

1. Determine its canonical test directory via §3.
2. Execute all tests under that directory.
3. No implicit test discovery outside mapped directories is permitted.

This document does not define when or why an oracle is executed.  

---

## 6. Directory Structure Constraints

### 6.1 Allowed structure inside an oracle directory

Within:

```
tetris/tests/<oracle_dir>/
```

the following are allowed:

* multiple `test_*.py` files,
* helper modules,
* local fixtures,
* static test data files.

### 6.2 Forbidden structure

The following are prohibited:

* importing tests across oracle directories,
* cross-oracle helper reuse unless placed in a neutral shared helper module under:

```
tetris/tests/_shared/
```

* defining tests outside an oracle directory.

---

## 7. Shared Test Utilities

Shared utilities MUST reside under:

```

tetris/tests/_shared/

```

Rules:

* `_shared/` MUST NOT contain tests.
* `_shared/` may contain:
    * fixture builders,
    * deterministic state constructors,
    * reusable assertions.

This prevents circular oracle coupling.

---

## 8. Determinism Requirement

Unless explicitly allowed by the referenced oracle document:

* Tests MUST be deterministic.
* Randomness MUST be seeded.
* No wall-clock time dependency is allowed.
* No filesystem side effects outside temporary directories are allowed.

---

## 9. Compliance Conditions

The test suite is compliant only if:

* Every oracle document has exactly one corresponding directory.
* No orphan test directories exist.
* No tests exist outside `tetris/tests/`.
* No test directory exists without a corresponding `ORACLE_*` document.

Violation invalidates regression semantics.

---
