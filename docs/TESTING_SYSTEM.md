---
name: TESTING_SYSTEM.md
description: Canonical, AI-oriented testing system specification for this repository. Defines governance (TEST_STRATEGY.md), normative oracle specs (*_TEST_ORACLE.md), executable implementations (pytest), and observational run reports (TEST_RUN_REPORT.md).
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

## Test Strategy Designer

Defines the _test system design_ for the repo: test layers, invariants, scope boundaries, and what “good coverage” means. *Test Strategy Designer* does **not** write tests or code; it writes **test strategy artifacts** that constrain downstream testing workflow.

### Inputs

- `AGENTS.md` (repo rules / workflow constraints) 
- `PROJECT.md` + referenced docs (project intent and contracts)
- Existing test tree and configs (`tests/`, `pytest.ini`, `pyproject.toml`, etc.)
- Architecture decomposition (if available) or current module structure (`ARCHITECTURE.md` and `DECOMPOSITION.md`)
- Development workflow decomposition (`PHASES.md`, `ACCEPTANCE_GATES.md`)
- Past `TEST_RUN_REPORT.md` / triage reports (to spot systemic pain) 

### Outputs

- `TEST_STRATEGY.md` (canonical) 
- `TEST_PLAN.md` (phase-scoped checklist)
- `TESTING_CONVENTIONS.md` (naming, fixtures, markers)


### `TEST_STRATEGY.md`

At a minimum:

1. **Test layers & intent**
    - unit / integration / system
    - what kind of behavior is allowed to be asserted at each layer
2. **Oracle governance**
    - when an oracle spec is required
    - where oracle specs live
    - allowed oracle types (invariant, property, golden master, etc.)
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
