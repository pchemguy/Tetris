---
doc_id: L1_GOVERNANCE
name: L1_GOVERNANCE.md
title: L1 — Governance (Process Control)
kind: control
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines repository evolution phases, acceptance gates, and scope-control rules governing when work is permitted and evaluated.
supersedes: []
superseded_by: null
references: [
  PHASES,
  ACCEPTANCE_GATES
]
---

# L1 — Governance

## Position of meta-layer

L1 defines **workflow governance**.

* L2–L4 define the system and correctness independent of phases or gates.
* L1 defines how change is managed in a controlled way (compartmentalization, sequencing, permission to attempt work).

Therefore:

* Architecture and decomposition (L2) can exist without governance (L1).
* Governance (L1) is meaningful only insofar as it governs L2–L4.

L1 is not “above” L2 in the semantic stack. It is above in the **control stack**. L2 does not depend on L1 for meaning; L1 depends on L2–L4 for substance.

---

## Document Index

Directory**: `docs/control/`

| Title                       | Filename              | Function / Role                                             |
| --------------------------- | --------------------- | ----------------------------------------------------------- |
| Repository Evolution Phases | `PHASES.md`           | Allowed scope of work at each stage of repository evolution |
| Acceptance Gates            | `ACCEPTANCE_GATES.md` | Milestone-based acceptance criteria and progression rules   |

---

## Detailed description

Documents in this class control the **development process itself**, not system behavior. They define **when certain kinds of work are permitted**, and **under what conditions progress is considered acceptable**. This class consists of two distinct, complementary documents with **non-overlapping authority**:

### Acceptance gates (`ACCEPTANCE_GATES.md`) — *Correctness and progression control*

**Role**  
Defines **when the agent is allowed to advance**.

**Contents**

- Ordered development gates
- Mandatory criteria per gate
- Prohibited behaviors
- MVP definition

**Usage**

- Prevents “all-at-once” implementations.
- Enables human-in-the-loop approval per stage.
- Ideal for automated evaluation harnesses.

Acceptance gates define **what must be implemented and proven** to advance development. They answer questions such as:

* *What concrete functionality is required at this stage?*
* *What correctness properties must hold?*
* *Which tests and oracles must pass?*

Acceptance gates constrain:

* **what constitutes “done”**,
* **what evidence of correctness is required**,
* **when progression is allowed**.

A gate failure is a **correctness failure**, even if the work is in-scope for the current phase.

---

### Phases (`PHASES.md`) — *Scope control*

**Role**   
Defines the **allowed scope of work** at each stage of the repository’s evolution.

**Contents**

- Named repository evolution phases
- Scope boundaries per phase
- Relationship between phases and acceptance gates
- Phase ↔ Gate matrix

**Usage**

- Prevents premature refactors, extensions, or generalization.
- Constrains *what kinds of changes are allowed*, independent of correctness.
- Works in tandem with `ACCEPTANCE_GATES.md`, which governs *whether an implementation is correct*.
- Agents must determine the current phase before selecting a target gate.
- Humans should advance phases deliberately and explicitly, not implicitly.

Phases define the **allowed scope of change** at a given point in the repository’s evolution. They answer questions such as:

* *What kinds of changes are permitted right now?*
* *Which subsystems may exist at all at this stage?*
* *Is this work premature, even if it could be implemented correctly?*

Phases constrain:

* **what may be attempted**,
* **which components may be introduced**,
* **what kinds of refactors or extensions are in-bounds**.

A phase violation is a **scope failure**, even if all acceptance criteria would otherwise pass.

---

### Relationship between phases and gates

* **Phases** decide *whether work is allowed to be attempted*.
* **Acceptance gates** decide *whether attempted work is correct and complete*.

Both must be satisfied:

* correct work in the wrong phase **fails**,
* in-phase work that fails gate criteria **fails**.

Together, these documents prevent:

* premature generalization,
* scope creep disguised as “cleanup”,
* skipping validation steps,
* implementing features “because they’re easy”.

---

### Gate applicability rules (normative)

The applicability of documents to acceptance gates defined in `ACCEPTANCE_GATES.md` is governed by the following rules:

- **Gate 0** applies universally as a discovery and compliance gate and therefore requires awareness of all normative documents, even if they are not yet implemented.
- **System-level contracts** apply to **all gates**. They constrain the system globally and must be obeyed at all stages.
- **Core / engine contracts** apply to **core gates (0–9)**. They define the pure simulation and must not be violated during core development or extension.
- **Shell contracts** apply to **Gate 0** (discovery and scope awareness) and to their respective **shell gates (10–13)** when implementation is permitted.
- **Core test oracle** (`CORE_TEST_ORACLE.md`) applies to **Gates 1–6**, and additionally to **Gates 7–9** if those optional core extensions are enabled.
- **Shell-level test oracles** apply to **exactly one gate each**, corresponding to the shell component they validate.

These rules are authoritative and supersede any informal interpretation of document scope.

---

### Phase ↔ Gate matrix

The following table defines which acceptance gates are expected to be exercised within each repository evolution phase. This matrix is **normative** and constrains scope. It does not replace the detailed gate definitions in `docs/ACCEPTANCE_GATES.md`.

| Phase | Phase name                                 | Applicable gates |
| ----- | ------------------------------------------ | ---------------- |
| 0     | Contract spine & evaluation framework      | 0                |
| 1     | Core-only MVP benchmark                    | 0–6              |
| 2     | System / shell completeness (baseline app) | 0, 10–13         |
| 3     | Optional extensions & hardening            | 0, 7–9           |
| 4     | Variant shells & alternative interfaces    | 0, 10–13 (+ext.) |
| 5     | Benchmark scaling & agent evaluation       | 0–13             |

### Notes

- **Gate 0** applies in *all phases* as a discovery and compliance gate.
- Gates **1–6** define the **mandatory core MVP**.
- Gates **7–9** are optional core extensions and may be completed in Phase 1 or Phase 3.
- Gates **10–13** define shell/system completeness and must not be attempted before Phase 2.
- “(+ext.)” indicates that additional gates may be introduced for new shell variants.

---

