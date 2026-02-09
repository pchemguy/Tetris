---
name: SKILL_CATALOG.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# Canonical Skill Catalog

## Design Criteria (Implicit Contract)

A **canonical skill** must:

* Represent a **stable developer role**
* Be **project-agnostic**
* Have **clear scope boundaries**
* Be reusable across:
    * greenfield development
    * refactoring
    * maintenance
* Avoid orchestration and policy decisions (controller-only)

---

# Tier 0 — Meta / Controller (Not a Skill)

| Role                      | Notes                                                                            |
| ------------------------- | -------------------------------------------------------------------------------- |
| Controller / Orchestrator | Owns phase sequencing, gating, skill invocation. Never edits artifacts directly. |

---

# Tier 1 — Foundation Skills (Always Present)

These are **non-negotiable** for any serious project.

## S1. Project Discovery & Context Loader

**Role:** Repository cartographer

* Reads: `AGENTS.md`, `PROJECT.md`, `README.md`
* Discovers structure, configs, tests
* Produces a **context snapshot artifact**

---

## S2. Requirements Interpreter & Scope Freezer

**Role:** Intent stabilizer

* Converts narrative goals → constrained intent
* Identifies:
    * non-goals
    * assumptions
    * deferrals
* Freezes scope for downstream phases

---

## S3. Architecture & Decomposition Planner

**Role:** Structural designer

* Defines module boundaries
* Identifies stable interfaces
* Produces phased decomposition
* No implementation

---

## S4. Test Strategy Designer

**Role:** Verification architect

* Defines test layers and invariants
* Decides *what kinds* of tests exist
* No test writing

---

# Tier 2 — Construction Skills (Core Execution)

These implement or lock behavior **within constraints set by Tier 1**.

## S5. Feature Implementer

**Role:** Contract-respecting coder

* Implements exactly what is specified
* No scope expansion
* No refactoring beyond local necessity

---

## S6. Test Author

**Role:** Behavior lock-in specialist

* Writes tests from:
    * specs
    * observed behavior
* Strengthens regression protection
* No production code changes

---

## S7. Test Runner & Failure Triage

**Role:** Diagnostic analyst

* Executes tests
* Classifies failures:
    * implementation bug
    * spec gap
    * test defect
* Produces structured failure reports

---

# Tier 3 — Evolution & Maintenance Skills

These appear once code exists and must evolve safely.

## S8. Refactoring Planner

**Role:** Risk-aware transformer (planner only)

* Analyzes structural debt
* Produces refactoring plans
* Defines invariants to preserve

---

## S9. Refactoring Executor

**Role:** Mechanical transformer

* Executes an **approved** refactoring plan
* Preserves behavior and tests
* No design decisions

---

## S10. Performance & Complexity Analyst

**Role:** Constraint auditor

* Identifies hot paths
* Proposes optimization strategies
* No implementation

---

# Tier 4 — Boundary & Externalization Skills

Not always needed, but canonical.

## S11. Data / State Model Designer

**Role:** Invariant & persistence designer

* Defines data models and invariants
* Strongly applies to:
    * Zotero
    * moderately to Tetris (game state)

---

## S12. UI / Interaction Semantics Designer

**Role:** Interaction logic designer (non-visual)

* Defines states, transitions, events
* No HTML/CSS/graphics
* Logic-only UI semantics

---

## S13. Build, Packaging & Release Specialist

**Role:** Artifact assembler

* Defines build outputs
* Ensures installability & reproducibility
* No feature logic

---

## S14. Documentation Author

**Role:** Externalization specialist

* Produces user-facing documentation
* Aligns docs strictly with behavior
* No speculative promises

---

# Workflow Phases → Skill Mapping

This is the **canonical phase model** your controller should enforce.

---

## Phase 0 — Initialization

| Skill                                  | Mandatory |
| -------------------------------------- | --------- |
| S1. Project Discovery & Context Loader | ✅         |

**Outputs**

* Context snapshot
* Discovered structure

---

## Phase 1 — Intent Stabilization

| Skill                                        | Mandatory |
| -------------------------------------------- | --------- |
| S2. Requirements Interpreter & Scope Freezer | ✅         |

**Gate**

* Scope frozen
* Non-goals explicit

---

## Phase 2 — Structural Design

| Skill                                    | Mandatory |
| ---------------------------------------- | --------- |
| S3. Architecture & Decomposition Planner | ✅         |
| S4. Test Strategy Designer               | ✅         |
| S11. Data / State Model Designer         | ❓         |
| S12. UI / Interaction Semantics Designer | ❓         |

**Gate**

* Module boundaries defined
* Test philosophy locked

---

## Phase 3 — Construction (Iterative Loop)

This phase **loops**.

| Skill                            | Mandatory |
| -------------------------------- | --------- |
| S5. Feature Implementer          | ✅         |
| S6. Test Author                  | ❓         |
| S7. Test Runner & Failure Triage | ✅         |

**Gate**

* Tests passing
* No scope violations

---

## Phase 4 — Evolution & Hardening

| Skill                                 | Mandatory |
| ------------------------------------- | --------- |
| S8. Refactoring Planner               | ❓         |
| S9. Refactoring Executor              | ❓         |
| S10. Performance & Complexity Analyst | ❓         |

**Gate**

* Behavior preserved
* Measured improvement or justified no-op

---

## Phase 5 — Externalization & Release

| Skill                             | Mandatory |
| --------------------------------- | --------- |
| S13. Build & Packaging Specialist | ❓         |
| S14. Documentation Author         | ❓         |

---

# Explicit Non-Skills (Enforced Exclusions)

These must **never** become skills:

* “Fix failing tests”
* “Implement feature X”
* “Clean up code”
* “Make it modular”

Those are **tasks**, not roles.

---

# Minimal Viable Skill Set (Controller Bootstrap)

If you had to start lean:

1. S1 — Project Discovery
2. S2 — Requirements Interpreter
3. S3 — Architecture Planner
4. S4 — Test Strategy Designer
5. S5 — Feature Implementer
6. S7 — Test Runner & Failure Triage

Everything else layers cleanly.

---

## Key Structural Insight

A workflow phase answers:

> **“What kind of thinking is allowed now?”**

A skill answers:

> **“Who am I pretending to be while thinking?”**

This catalog keeps those two axes orthogonal — which is why it scales.

---

### Next logical steps (if you want)

* Freeze this as `SKILL_CATALOG.md`
* Define **skill invocation contracts** (inputs/outputs schema)
* Fully specify **one Tier-1 skill** using your `SKILL_DEV_PROMPT_TEMPLATE`

Tell me which direction you want to go.

