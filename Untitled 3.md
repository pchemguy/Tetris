Below is a **clean, scalable ACCEPTANCE_GATES.md structure** that matches your intent:

* Gates define **implementation order** and **acceptance criteria**.
* Domains are **architectural scope groupings** (primarily for phases), but gates still live “in” a domain so you can classify scope.
* Families are **gate groupings** (a navigational + governance unit), not a second semantics system.
* L2/L3 define **what exists + what it must do**.
* L4 defines **what must be proven**.
* Gates reference **L3 (contracts)** and **L4 (oracles)**, but **do not interpret oracle dependencies**.

You can paste this as the new spine of `ACCEPTANCE_GATES.md` and then fill in details gate-by-gate.

---

# ACCEPTANCE_GATES.md (proposed structure)

## 1. What acceptance gates are

Acceptance gates are **ordered, testable milestones** used to evolve the repository from one well-defined state to the next.

A gate is considered **passed** only when:

1. All **mandatory scope** for that gate is implemented, and
2. All **mandatory proofs** (tests) required by the gate pass, as defined by the gate’s associated **oracle(s)**.

Gates are:

* **cumulative** (later gates assume earlier gates remain passing),
* **minimal-scope** (each gate advances the system by the smallest sensible step),
* **testable** (a gate’s scope must be verifiable).

Phases constrain **what is allowed to be modified**. Gates constrain **what must be built and proven**.

---

## 2. Organization model

This repository uses the following structural hierarchy:

* **Domain**: high-level architectural scope grouping (used primarily by `PHASES.md`).
* **Family**: an ordered set of gates with a shared objective and acceptance character.
* **Gate**: the smallest testable incremental milestone.

### 2.1 Domains

Domains are defined here so **PHASES.md can reference them** without redefining meanings.

Domains are not “another axis of correctness.” They are **scope categories**.

**Recognized domains:**

* `DOC_INFRA`
* `CORE`
* `SHELL_BASELINE`
* `CORE_EXTENSIONS`
* `VARIANTS`
* `BENCHMARK`

### 2.2 Gate families

Families are **navigational + governance partitions** over the single ordered gate sequence.

Families:

* provide a stable table-of-contents,
* separate core vs shell vs integration milestones,
* keep the document scalable (no flat numbering drift).

### 2.3 Gates

A gate:

* defines a **target delta** (“what becomes true after this gate”), and
* names the **oracle(s)** that must pass to accept it.

**Oracle policy for gates (normative):**

* A gate MAY require multiple oracles.
* Exactly **one** oracle is the *primary oracle* for that gate (the oracle covering the newly introduced/expanded behavior).
* Any additional oracles listed by the gate MUST be **regression proofs** already introduced by earlier gates (i.e., re-run because the new change may affect them).
* Gates MUST NOT introduce “use-once” oracles. Every oracle is reusable and remains valid as the system grows.

---

## 3. How families and domains align with L2/L3/L4

### 3.1 L2 and L3 are the authority for “what to build”

* **L2 (Structure)** defines *what components exist* and *allowed boundaries*.
* **L3 (Behavior)** defines *what each component must do*.

Gates never derive behavior from tests or implementation. Gates point to **L2/L3**.

### 3.2 L4 is the authority for “what must be proven”

* **L4 (Test Oracles)** defines *mandatory correctness proofs*.
* Tests are considered valid only insofar as they implement L4 oracles.

Gates never reinterpret oracle dependencies. They only **name which oracle(s) apply**.

---

## 4. Domain and family tables

### 4.1 Domains table

| Domain          | Meaning (scope)                                                              |
| --------------- | ---------------------------------------------------------------------------- |
| DOC_INFRA       | Documentation system, inventories, governance tooling, meta validation       |
| CORE            | Pure deterministic simulation core (no IO, no timing, no shell)              |
| SHELL_BASELINE  | Baseline deterministic shell (renderer/runtime/cli/replay/config)            |
| CORE_EXTENSIONS | Optional core mechanics or hardening that preserve baseline semantics        |
| VARIANTS        | Alternative shells/interfaces/runtimes (separate components)                 |
| BENCHMARK       | Evaluation scaling: corpora, scoring harnesses, automation, comparative runs |

### 4.2 Families table

| Family | Name                                  | Primary domain(s)               |
| -----: | ------------------------------------- | ------------------------------- |
|     G0 | Governance & Compliance               | DOC_INFRA                       |
|     G1 | Core Structural Readiness             | CORE                            |
|     G2 | Core Behavioral Completion            | CORE                            |
|     G3 | Core Robustness & Auditability        | CORE, CORE_EXTENSIONS           |
|     G4 | Shell Completion                      | SHELL_BASELINE                  |
|     G5 | Integration & System-Level Guarantees | DOC_INFRA, CORE, SHELL_BASELINE |

**Notes (normative):**

* The “Primary domain(s)” field is classificatory only. Gates remain strictly ordered by gate numbering, not by domain.

---

# Family sections

Each family section must:

1. State the family purpose and what “done” means at the family level.
2. State which L3 contracts are primarily involved.
3. State which L4 oracles are used as proof obligations.
4. Provide a **family gate table**.
5. Provide **gate details** for each gate in the family.

Below is the canonical pattern.

---

## G0 — Governance & Compliance

### G0. Purpose

Establish deterministic project discovery and enforce governance rules that prevent speculative implementation.

### G0. Alignment to L2/L3/L4

* **L2 alignment:** ensures the repo structural contracts are discoverable and enforceable.
* **L3 alignment:** ensures behavioral contracts are discoverable before implementation.
* **L4 alignment:** ensures oracle system exists and is machine-checkable before tests claim correctness.

### G0. Gate table

| Gate | Name                             | Domain    | Primary oracle | Regression oracles |
| ---- | -------------------------------- | --------- | -------------- | ------------------ |
| G0.1 | Repository & Contract Compliance | DOC_INFRA | ORACLE: TBD    | —                  |

### G0.1 Repository & Contract Compliance

**Objective (delta):**

* After this gate, an agent/tool can discover authoritative docs deterministically and validate metadata invariants.

**Scope (mandatory):**

* Documentation inventory is generatable and valid (schema-valid, deterministic ordering).
* YAML metadata is valid per `DOC_SCHEMA.json`.
* Duplicate DOC_ID is a hard failure.
* YAML references resolve to existing documents.

**Proof obligations (mandatory):**

* Primary oracle: `ORACLE_DOC_INFRA_*` (define this oracle family in L4 if not present yet).
* Regression: none.

**Failure conditions (hard):**

* Missing required YAML front matter on normative docs (per DOC_SCHEMA/Gate-0 policy).
* Duplicate doc_id.
* Schema invalid.
* Broken YAML reference graph.

---

## G1 — Core Structural Readiness

### G1. Purpose

Create the **core API + state model skeleton** so later behavioral gates can be implemented incrementally without API churn.

### G1. Alignment to L3/L4

* **L3 authority:** `CORE_API`, `GAME_STATE`, `INPUT_MODEL`, `ERROR_HANDLING`
* **L4 proof:** core structural oracle(s) (e.g. `ORACLE_CORE_*` subset that only asserts type/API structure)

### G1. Gate table

| Gate | Name                  | Domain | Primary oracle        | Regression oracles |
| ---- | --------------------- | ------ | --------------------- | ------------------ |
| G1.1 | Core Skeleton & Types | CORE   | ORACLE_CORE_STRUCTURE | —                  |

### G1.1 Core Skeleton & Types

**Objective (delta):**

* Core public API exists; state objects exist; step exists with permitted stub semantics.

**Scope (mandatory):**

* Implement public types and functions defined by `CORE_API.md`.
* `new_game()` returns structurally valid `GameState`.
* `step()` exists and returns a `StepResult` with allowed stub behavior.

**Proof obligations:**

* Primary oracle: `ORACLE_CORE_STRUCTURE.md` (or equivalent slice under `ORACLE_CORE.md` that is explicitly structural).
* Regression: none.

---

## G2 — Core Behavioral Completion

### G2. Purpose

Implement the complete deterministic Tetris core behavior (MVP semantics), gate-by-gate.

### G2. Alignment to L3/L4

* **L3 authority:** `GAME_RULES`, `GAME_STATE`, `INPUT_MODEL`, `ERROR_HANDLING`, `SHAPES_AND_ROTATIONS`
* **L4 proof:** `ORACLE_CORE_*` documents (behavioral)

### G2. Family gate table

| Gate | Name                    | Domain | Primary oracle                  | Regression oracles                                    |
| ---- | ----------------------- | ------ | ------------------------------- | ----------------------------------------------------- |
| G2.1 | Geometry & Collision    | CORE   | ORACLE_CORE_GEOMETRY            | ORACLE_CORE_COLLISION (if separate)                   |
| G2.2 | Gravity & Line Clearing | CORE   | ORACLE_CORE_GRAVITY_AND_LOCKING | ORACLE_CORE_LINE_CLEAR, ORACLE_CORE_COLLISION         |
| G2.3 | Scoring & RNG           | CORE   | ORACLE_CORE_SCORING             | ORACLE_CORE_RNG_7BAG, ORACLE_CORE_LINE_CLEAR          |
| G2.4 | Input Semantics         | CORE   | ORACLE_CORE_COLLISION           | ORACLE_CORE_GEOMETRY, ORACLE_CORE_GRAVITY_AND_LOCKING |
| G2.5 | Game Over               | CORE   | ORACLE_CORE_GAME_OVER           | ORACLE_CORE_SPAWN, ORACLE_CORE_COLLISION              |

> The table above is illustrative. The real table must match your final oracle set. The key rule: **one primary oracle**, other listed oracles are regression only.

Then for each gate (G2.1 … G2.5) you provide “Objective / Scope / Proof obligations / Failure conditions” in the same format as G1.1.

---

## G3 — Core Robustness & Auditability

### G3. Purpose

Optional mechanics and hardening that preserve baseline semantics while improving strictness and auditability.

### G3. Alignment to L3/L4

* **L3 authority:** `ERROR_HANDLING`, plus any extension specs (e.g. hold) if present.
* **L4 proof:** `ORACLE_CORE_INVARIANTS`, `ORACLE_CORE_HOLD`, etc.

### G3. Family gate table

| Gate | Name                           | Domain          | Primary oracle             | Regression oracles        |
| ---- | ------------------------------ | --------------- | -------------------------- | ------------------------- |
| G3.1 | Hold (Optional)                | CORE_EXTENSIONS | ORACLE_CORE_HOLD           | ORACLE_CORE_COLLISION     |
| G3.2 | Invariants & Strictness        | CORE            | ORACLE_CORE_INVARIANTS     | ORACLE_CORE_* (as needed) |
| G3.3 | Regression & Determinism Audit | CORE            | ORACLE_CORE_AUDIT (if any) | ORACLE_CORE_*             |

---

## G4 — Shell Completion

### G4. Purpose

Implement the baseline deterministic shell (renderer/runtime/cli/replay/config) without contaminating core purity.

### G4. Alignment to L3/L4

* **L3 authority:** `RENDERING_SPEC`, `RUNTIME_SPEC`, `CLI_SPEC`, `REPLAY_SPEC`, `CONFIG_API` etc.
* **L4 proof:** `ORACLE_SHELL_*` documents

### G4. Family gate table

| Gate | Name              | Domain         | Primary oracle         | Regression oracles                       |
| ---- | ----------------- | -------------- | ---------------------- | ---------------------------------------- |
| G4.1 | ASCII Renderer    | SHELL_BASELINE | ORACLE_SHELL_RENDERING | ORACLE_CORE_*                            |
| G4.2 | Scripted Runtime  | SHELL_BASELINE | ORACLE_SHELL_RUNTIME   | ORACLE_CORE_*                            |
| G4.3 | CLI               | SHELL_BASELINE | ORACLE_SHELL_CLI       | ORACLE_SHELL_RUNTIME                     |
| G4.4 | Replay            | SHELL_BASELINE | ORACLE_SHELL_REPLAY    | ORACLE_SHELL_RUNTIME, ORACLE_CORE_*      |
| G4.5 | Config (if gated) | SHELL_BASELINE | ORACLE_SHELL_CONFIG    | ORACLE_SHELL_CLI (if config affects CLI) |

(Only include config as a gate if you want it explicitly staged; otherwise keep it inside the relevant shell gate.)

---

## G5 — Integration & System-Level Guarantees

### G5. Purpose

Define system-level acceptance conditions (“what does it mean to declare MVP complete?”) without introducing new behavior.

G5 gates are about **cross-cutting guarantees**, not additional features.

### G5. Alignment to L3/L4

* **L3 authority:** cross-document system guarantees (core + shell specs)
* **L4 proof:** orchestration of previously defined oracles + system-level proofs (if you define any).

### G5. Family gate table

| Gate | Name                           | Domain    | Primary oracle | Regression oracles                         |
| ---- | ------------------------------ | --------- | -------------- | ------------------------------------------ |
| G5.1 | Core MVP Acceptance (G0–G2)    | DOC_INFRA | (none)         | ORACLE_CORE_* + G0 oracle                  |
| G5.2 | Full System Acceptance (G0–G4) | DOC_INFRA | (none)         | ORACLE_CORE_* + ORACLE_SHELL_* + G0 oracle |

**Normative rule:** G5 gates must not introduce new functional requirements; they only define acceptance composition and required evidence sets.

---

# What you should decide next (so this stays consistent)

1. Do you want a dedicated **DOC_INFRA oracle** in L4 (recommended), or keep Gate 0 as “policy-only”?
   If you want machine-checkable compliance, make it an oracle.

2. Confirm whether `CONFIG` is:

   * a standalone shell gate, or
   * embedded into CLI/runtime gates.

3. Finalize the “primary oracle per gate” mapping for G2.* so each gate introduces only one new oracle as primary.

If you want, I can now take your existing Gate 0–13 content and **rewrite it into this exact structure**, without changing semantics yet (pure refactor), and with your new numbering (`G0.1`, `G1.1`, …).
