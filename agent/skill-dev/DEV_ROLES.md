---
name: DEV_ROLES.md
description: Brainstorm developer role candidates for skill implementation.
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# 1. Core, Project-Agnostic Developer Roles (Always Present)

These skills exist in *almost every* non-trivial project and should be considered **baseline**.

## 1.1 Controller / Orchestrator (Non-Skill)

*Not a skill; included for completeness.*

* Owns workflow execution
* Selects and invokes skills
* Enforces phase ordering and gating
* Never edits code directly

---

## 1.2 Project Discovery & Context Loader

**Role:** Repository cartographer

**Responsibilities**

* Read and operationalize `PROJECT.md`, `README.md`, `AGENTS.md`
* Identify relevant directories, configs, tests
* Produce a *context snapshot artifact*

**Applies to**

* Tetris: rules, loop structure, input/output surfaces
* Zotero: storage model, sync boundaries, UI layers

---

## 1.3 Requirements Interpreter / Scope Freezer

**Role:** Intent stabilizer

**Responsibilities**

* Translate prose goals into constrained development intent
* Identify non-goals and deferred features
* Detect scope creep

**Applies to**

* Tetris: “classic behavior” vs modern variants
* Zotero: citation formats, sync guarantees, plugin boundaries

---

## 1.4 Architecture & Decomposition Planner

**Role:** Structural designer

**Responsibilities**

* Define module boundaries
* Identify stable interfaces
* Propose phased decomposition

**Applies to**

* Tetris: engine vs renderer vs input
* Zotero: database, sync engine, UI, citation processor

---

## 1.5 Test Strategy Designer

**Role:** Verification architect

**Responsibilities**

* Decide *what kinds* of tests exist
* Define invariants and contracts
* Specify test layering

**Applies to**

* Tetris: deterministic tick outcomes, collision invariants
* Zotero: database migrations, citation rendering fidelity

---

# 2. Implementation-Phase Roles (Common but Optional)

These skills are invoked once structure exists.

## 2.1 Feature Implementer

**Role:** Contract-respecting coder

**Responsibilities**

* Implement functionality exactly as specified
* Avoid architectural drift
* No speculative extensions

**Applies to**

* Tetris: rotation logic, scoring rules
* Zotero: import/export formats, UI actions

---

## 2.2 Refactoring Planner

**Role:** Risk-aware transformer

**Responsibilities**

* Analyze existing code for structural debt
* Propose refactoring plans (not execution)
* Define safety constraints

---

## 2.3 Refactoring Executor

**Role:** Mechanical transformer

**Responsibilities**

* Apply an approved refactoring plan
* Preserve tests and behavior
* Produce before/after artifacts

---

## 2.4 Test Author

**Role:** Behavior lock-in specialist

**Responsibilities**

* Write tests from specs or observed behavior
* Expand coverage without altering behavior
* Encode regression protection

---

## 2.5 Test Runner / Failure Triage

**Role:** Diagnostic analyst

**Responsibilities**

* Execute test suites
* Classify failures (bug, spec gap, test error)
* Produce structured failure reports

---

# 3. Domain-Sensitive but Reusable Roles

These appear depending on project type.

## 3.1 State & Data Model Designer

**Role:** Persistence and invariants designer

**Applies strongly to**

* Zotero (primary)
* Tetris (secondary: game state snapshots)

---

## 3.2 UI / Interaction Designer (Logic-Only)

**Role:** Interaction semantics designer

**Responsibilities**

* Define UI states and transitions
* No HTML/CSS/visual styling
* Event → effect mapping

**Applies to**

* Tetris: input timing, pause/restart semantics
* Zotero: selection, editing, sync conflict UX

---

## 3.3 Performance & Complexity Analyst

**Role:** Constraint auditor

**Responsibilities**

* Identify performance-critical paths
* Propose optimizations without implementation
* Define acceptable bounds

---

# 4. Integration & Release Roles

Often postponed but structurally distinct.

## 4.1 Build & Packaging Specialist

**Role:** Artifact assembler

**Responsibilities**

* Define build outputs
* Verify installability
* Ensure reproducibility

---

## 4.2 Documentation & User-Facing Explanation Author

**Role:** Externalization specialist

**Responsibilities**

* Produce user-level documentation
* Keep docs aligned with behavior
* No speculative promises

---

# 5. What Should *NOT* Be Skills

Explicit exclusions (important for your framework):

❌ “Fix failing tests”
❌ “Implement feature X”
❌ “Clean up codebase”
❌ “Make it more modular”

These are **tasks**, not **roles**.
Skills must represent **stable cognitive positions**, not actions.

---

# 6. Minimal Skill Set for a “Typical” Project

If you had to start lean:

1. Project Discovery & Context Loader
2. Requirements Interpreter
3. Architecture & Decomposition Planner
4. Test Strategy Designer
5. Feature Implementer
6. Test Runner / Failure Triage

Everything else can be layered later.

---

## Key Insight (Framework-Level)

A good skill answers:

> *“Who am I pretending to be?”*
> not
> *“What exact change am I making?”*

---
---

