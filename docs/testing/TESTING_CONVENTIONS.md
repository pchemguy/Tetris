---
name: docs/testing/TESTING_CONVENTIONS.md
description: Project-specific testing conventions for the Tetris project. Supplements TEST_STRATEGY.md with concrete naming, layering, and implementation rules.
---

# TESTING CONVENTIONS

This document defines **concrete conventions** for implementing the testing system described in `TEST_STRATEGY.md`. It defines **how correctness is encoded and organized** in this Tetris codebase.

---

# 1. Test Layer Structure

This project uses the following layers:

## 1.1 Unit Layer — Engine-Level Logic

Scope:

- Pure game engine logic
- No rendering
- No UI
- No file I/O
- No randomness unless explicitly seeded

Typical modules:

- piece rotation
- collision detection
- board state transitions
- scoring logic
- line clearing
- game state machine transitions

Allowed:

- Exact structural assertions (matrix equality, coordinate sets)
- Deterministic state comparisons
- Exception assertions

Prohibited:

- Pixel comparisons
- Timing-based assertions
- UI-related state
- Event-loop dependent behavior

---

## 1.2 Integration Layer — Engine + State Coordination

Scope:

- Interaction between:
    - engine
    - game state manager
    - input dispatcher (logical only)
- No rendering surface
- No real-time timing assumptions

Allowed:

- Contract-level assertions:
    - "given X input sequence, resulting board state satisfies Y"
    - "score increases by expected delta"
    - "piece locks after collision"

Prohibited:

- Direct inspection of private internal fields
- Assertions on intermediate transient states unless documented invariant

---

## 1.3 System Layer — Full Game Loop (Optional)

Only if implemented.

Scope:

- High-level loop interactions
- Deterministic simulated stepping only

Allowed:

- Outcome-based assertions
- State invariants after full move sequences

Prohibited:

- Real-time frame timing
- Visual/pixel comparison
- Flaky time-based expectations

---

# 2. Oracle Spec Organization

All oracle specs live in:

```
docs/testing/oracles/
```

Tetris domains must be split logically:

- CORE_TEST_ORACLE.md
- ROTATION_TEST_ORACLE.md
- COLLISION_TEST_ORACLE.md
- SCORING_TEST_ORACLE.md
- LINE_CLEAR_TEST_ORACLE.md
- STATE_MACHINE_TEST_ORACLE.md

---

# 3. Naming Conventions

Oracle ID Format:

```
<DOMAIN>_ТЕСТ_ORACLE
```

Examples:

- CLI_TEST_ORACLE
- RUNTIME_TEST_ORACLE

IDs must never be reused for different semantics.

---

# 4. Pytest Translation Conventions

All pytest translations must follow:

```

tests/test_<python_package>_<python_module>.py

```

Examples:

- test_tetris_core_state.py
- test_tetris_runtime_loop

---

## 4.1 Module Header (Mandatory)

Each translation module must begin with:

- Reference to oracle spec file DOC_ID

Example:

```
Implements:

RUNTIME_TEST_ORACLE
```

---

## 4.2 Parametrization Policy

Use pytest parametrization when:

- Multiple cases share structure
- Inputs vary but invariant logic is identical

Avoid:

- Deep nested parametrization that hides intent

---

# 5. Determinism Rules

## 5.1 Randomness

- All randomness must be seeded in tests.
- No unseeded RNG allowed.
- If random piece generation is tested:
    - Inject deterministic generator or
    - Mock generator

---

## 5.2 Time / Frame Stepping

Tests must:

- Use deterministic step functions
- Avoid real-time delays
- Avoid sleep()
- Avoid frame-based race conditions

If the engine supports `advance_time(ms)` or equivalent:

- Tests must use it.

---

## 5.3 Floating Point

If floats are used:

- Use tolerance-based comparison at integration layer.
- Exact equality only at unit layer where deterministic.

---

# 6. What Tests Must NOT Do

- Assert on internal private attributes unless documented invariant.
- Assert exact board representation formatting (string layout) unless explicitly specified in oracle.
- Assert visual rendering output.
- Assert frame timing.
- Couple to current implementation of rotation algorithm (only to documented behavior).
- Assume specific internal matrix orientation unless defined in oracle.

---

# 7. Fixture Conventions

## 7.1 Board Fixtures

- Provide small board fixtures for minimal cases.
- Provide standard test boards:
    - Empty board
    - Nearly full board
    - Wall-adjacent board
    - One-line-clear setup
    - Multi-line-clear setup

Keep fixtures simple and local to test modules unless shared across domains.

---

## 7.2 Piece Fixtures

- Provide deterministic piece shapes.
- Use canonical orientation definitions defined in oracle spec.
- Do not redefine shapes ad hoc in tests.

---

# 8. Regression Test Rules

When a bug is fixed:

- Add or update a focused test.
- If the bug reveals missing coverage:
    - Add a new case to oracle spec.
    - Then translate into pytest.

Do NOT:

- Modify existing test semantics silently.
- Merge multiple semantic bugs into one test.

---

# 9. Run Report Expectations

Each full suite execution must produce a run report containing:

- Command executed
- Python version
- pytest version
- Pass/fail counts
- Failing tests listed
- Failure grouping

Failure grouping should reflect core domains:

- Rotation failures
- Collision failures
- Scoring failures
- State machine failures

---

# 10. Example Domain Mapping

| Domain        | Oracle File                  |
| ------------- | ---------------------------- |
| Rotation      | ROTATION_TEST_ORACLE.md      |
| Collision     | COLLISION_TEST_ORACLE.md     |
| Line Clear    | LINE_CLEAR_TEST_ORACLE.md    |
| Scoring       | SCORING_TEST_ORACLE.md       |
| State Machine | STATE_MACHINE_TEST_ORACLE.md |

---

# 11. Enforcement Summary

- `TEST_STRATEGY.md` defines governance.
- `TESTING_CONVENTIONS.md` defines Tetris-specific structure.
- Oracle specs define correctness.
- Pytest implements oracle cases.
- Run reports record what happened.
- bug-fixer must follow oracle and strategy strictly.

---

# 12. Golden Rule

> Core engine correctness is defined by oracle specs. Tests enforce invariants, not implementation details. Determinism is mandatory. Flaky tests are structural defects.
