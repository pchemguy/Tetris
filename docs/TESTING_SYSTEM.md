---
name: TESTING_SYSTEM.md
description: Canonical, AI-oriented testing system specification for this repository. Defines governance (TEST_STRATEGY.md), normative oracle specs (*_TEST_ORACLE.md), executable implementations (pytest), and observational run reports (TEST_RUN_REPORT.md).
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

## Test Strategy Designer

### Role

Defines the _test system design_ for the repo: test layers, invariants, scope boundaries, and what “good coverage” means. *Test Strategy Designer* does **not** write tests or code; it writes **test strategy artifacts** that constrain downstream testing workflow.

### Inputs

- `AGENTS.md` (repo rules / workflow constraints) 
- `PROJECT.md` + referenced docs (project intent and contracts)
- Existing test tree and configs (`tests/`, `pytest.ini`, `pyproject.toml`, etc.)
- Architecture decomposition (if available) or current module structure (`ARCHITECTURE.md` and `DECOMPOSITION.md`)
- Development workflow decomposition (`PHASES.md`, `ACCEPTANCE_GATES.md`)
- Past `TEST_RUN_REPORT.md` / triage reports

### Outputs

- `TEST_STRATEGY.md` (canonical) 
- `TEST_PLAN.md` (phase-scoped checklist)
- `TESTING_CONVENTIONS.md` (naming, fixtures, markers)

### Behavioral contract

1. **Discovers** how testing is currently structured. 
2. **Defines** a stable taxonomy for tests aligned to architecture.
3. **Constrains** later workflow:
    `Test Author` should write tests that match this strategy.

### `TEST_STRATEGY.md`

At a minimum:

1. **Test layers & intent**
    - unit / integration / system
    - what kind of behavior is allowed to be asserted at each layer
2. **Oracle governance**
    - when an oracle spec is required
    - where oracle specs live
    - allowed oracle types (invariant, property, metamorphic, golden master, etc.).
    - authority sources for oracles
3. **Translation policy**
    - oracle spec → pytest mapping rules
    - traceability requirements (IDs, references)
    - what pytest may _not_ assert beyond the spec
4. **Change control**
    - when tests may be changed vs code
    - evidence required to modify an oracle spec
    - how bug-fixer arbitrates conflicts
5. **Execution conventions**
    - fast vs full suite
    - recommended scopes
    - CI expectations (if any)


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

`TEST_STRATEGY.md` establishes **what sources define correctness**, e.g.:

- docstrings
- `PROJECT.md`
- design notes
- mathematical invariants
- standards/specs

Strategy constrains **how specific** oracles are allowed to be.
Examples of strategy-level rules:

- “Do not assert exact floating-point values at integration level”    
- “Do not assert internal cache state”
- “Prefer behavioral invariants over sequence equality”

**Content of `TEST_STRATEGY.md` (what “done” looks like)**

- **Test layers** (e.g., unit / integration / end-to-end) and what belongs where
- **Invariants / contracts** per module boundary (what must never regress)
- **Test scope mapping**: subsystem → tests directory/module mapping
- **Failure triage policy hooks** (e.g., references to triage docs)
- **Coverage intent** (not coverage %, but coverage _semantics_)
- **Anti-patterns** to avoid (flaky timing tests, snapshot abuse, etc.)
- **Execution conventions** (fast subset vs full suite; recommended commands)

**`TEST_STRATEGY.md` should define:**

- **Which behaviors require oracle specs** vs ad hoc tests
- **How oracle specs are structured** (sections, allowed constructs, naming)
- **Where oracle specs live** (`docs/oracles/`, `tests/oracles/`, etc.)
- **Mapping rules**: oracle spec → pytest module naming/path
- **Allowed oracle types** (invariant, metamorphic, golden master, property-based)
- **Evidence/authority rules**:
    - what sources can justify changing an oracle spec
    - what sources can justify changing only the pytest translation
- **Layering rules**:
    - unit-oracle specs vs integration-oracle specs, etc.


If you want, I can draft a **minimal `TEST_STRATEGY.md` section** specifically for your “oracle-spec → pytest translation” pipeline, including:

- directory layout
- naming conventions
- required headers/IDs
- traceability rules
- bug-fixer decision rules (code vs translation vs spec)

### Governance & policy_ (how correctness may be asserted)

**Properties**

- Project-wide    
- Small (1–3 pages)
- No individual tests
- Defines:
    - what deserves an oracle
    - how oracle specs are structured
    - how they’re translated into pytest
    - evidence rules for changing oracles

> This is the constitution; it never enumerates test cases.

---
---

## Test Author

### Role

**Behavior lock-in specialist.** Writes test oracle specs and tests that encode the intended behavior (contracts/invariants) and prevent regressions. *Test Author* **does not implement features**; it only writes tests (and possibly shared test utilities if explicitly allowed by policy).

### Inputs

- *Test Strategy Designer* output — governs where/how tests are written
    - `TEST_STRATEGY.md` (canonical) 
    - `TEST_PLAN.md` (phase-scoped checklist)
    - `TESTING_CONVENTIONS.md` (naming, fixtures, markers)
- `PROJECT.md` and any module docstrings / contracts relevant to behavior
- Development workflow decomposition (`PHASES.md`, `ACCEPTANCE_GATES.md`)  
- Existing test tree and configs (`tests/`, `pytest.ini`, `pyproject.toml`, etc.)
- Existing test oracle specs
- Code under test

### Outputs

- New or updated test files under the repo’s test structure
- New or updated test oracle specs
- Small shared test utilities (`conftest.py`, helpers) **only if** consistent with test strategy and repo policy
- A short **test authoring report** (can be appended to `TEST_AUTHOR_REPORT.md`) documenting:
    - what behavior was encoded
    - why the test belongs at that layer
    - how to run it (focused scope)

### Behavioral contract

1. **Selects target behavior/invariant** from test strategy and/or specs.
2. **Finds correct placement** (unit vs integration; test file mapping).
3. **Writes minimal, meaningful assertions**:
    - no brittle over-specification
    - no “assert everything”
4. **Runs focused tests** to ensure:
    - tests fail when the bug exists (if applicable)
    - tests pass with correct behavior
5. **Avoids speculation**:
    - if desired behavior isn’t documented, flags ambiguity instead of inventing.


#### Mode A: Write/Update Oracle Specs

- Create or refine `*_TEST_ORACLE.md` per strategy
- Make them precise enough to translate
- Ensure each oracle is grounded in authority (docs/docstrings/PROJECT.md)

#### Mode B: Translate Oracle Specs → Pytest

- Implement each oracle spec as pytest tests
- Ensure traceability:
    - pytest module references the oracle spec file
    - ideally each test case references a spec section ID

**Outputs**

- `docs/oracles/foo_TEST_ORACLE.md` (or wherever)
- `tests/test_foo_from_oracle.py` (or equivalent)
- a short report: “what spec changed / what translation changed”

**Critical constraint**  
S6 should not “invent correctness” in pytest. If it’s not in the oracle spec, it should not be asserted (except incidental harness details).

---
---

## bug-fixer

- Treats failing oracles differently depending on strategy:
    - protected invariant → code must change
    - test-code drift → test may change _with evidence_
- Uses `TEST_STRATEGY.md` to decide:
    - whether an oracle is _legitimate_
    - whether it is _over-specified_
    - whether weakening it would violate policy

> bug-fixer arbitrates conflicts **using strategy as higher law**.


---
---

## Test Oracle Spec

`*_TEST_ORACLE.md` files are **oracle specifications** (formalized, human-readable, non-executable), and the executable pytest modules are a **compiled artifact** derived from them.

### `*_TEST_ORACLE.md`

**Oracle spec (declarative)**

- Defines _truth claims_ about behavior (preconditions → action → expected outcomes / invariants).
- Not executable.
- Should be stable across refactors unless the _spec_ changes.

### Pytest modules

**Oracle implementation (executable)**

- Concrete encoding of the oracle spec in Python assertions.
- May change more often (fixtures, helpers, parametrization), while preserving the same spec.


You effectively have a 2-stage verification pipeline:

1. **Oracle specification stage (declarative)**  
    `*_TEST_ORACLE.md`
2. **Oracle execution stage (imperative)**  
    pytest modules implementing those specs

A pytest test is “correct” if all are true

1. pytest test is a faithful implementation of an oracle spec governed by `TEST_STRATEGY.md`.
2. Oracle spec and `TEST_STRATEGY.md` are aligned with project documentation.
3. Local documentation (docstrings, comments, etc) agree with standalone references and docs (/docs/, README.md, PROJECT.md, etc).

When there are any ambiguous conflicts among `TEST_STRATEGY.md`, local docs, standalone docs, do not guess! Instead clearly identify conflicting sources and flag the issue.

### _Normative specifications_ (what “correct” means)

These define truth.

- `CORE_TEST_ORACLE.md`
- `ROTATION_TEST_ORACLE.md`
- `IO_CONTRACT_TEST_ORACLE.md`

**Properties**

- Define _individual tests / test cases_ (logically)
- Declarative, non-executable
- Stable across refactors
- Many files, scoped by domain or subsystem
- Authoritative for correctness

> These are where individual tests live conceptually.

```
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
```

```
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
```

---
---

## `TEST_RUN_REPORT.md`

```
# TEST_RUN_REPORT.md

## Run metadata

- Timestamp:
- Commit / working tree state:
- Invoking mode: test-runner | bug-fixer
- Command(s) executed:
- Scope: full suite | subset

## Environment

- Python version
- Test framework version
- OS (if relevant)
- Config files detected

## Results summary

- Total tests run:
- Passed:
- Failed:
- Errors:
- Skipped:

## Failure groups

### Group 1 — Import / resolution

- Tests:
- Shared traceback root:
- Classification confidence:

### Group 2 — Source code logic

- Tests:
- Likely shared cause:
- Evidence:

## Notes

- Suspected regressions:
- Suspected test drift:
- Unknowns / blockers:

## Next recommended action

- bug-fixer
- Test Author
- Strategy update
```

## Flow

### Example failure flow

1. `ROTATION_TEST_ORACLE.md` defines 12 rotation cases
2. Pytest translation creates ~20 parametrized tests
3. Test runner runs tests → produces `TEST_RUN_REPORT.md`
4. Report says:
    - tests linked to `ORACLE_ROTATION_003` and `_004` failed
5. bug-fixer:
    - checks oracle spec
    - checks pytest translation
    - checks code
6. Fix applied
7. New `TEST_RUN_REPORT.md` confirms clean run
