## 1. Purpose and acceptance semantics

This document defines **acceptance gates** for this project. Acceptance gates are **ordered, testable milestones** used to evolve the repository from one well-defined state to the next.

Acceptance gates:

- constrain development/agent scope,
- prevent premature feature creep,
- provide objective "done / not done" criteria,

A gate is considered **passed** only when:

1. All **mandatory scope** for that gate is implemented, and
2. All **mandatory proofs** (tests) required by the gate pass, as defined by the gate’s associated **test oracle(s)**.

Gate rules:

- **cumulative**: each gate subsumes all prior gates (earlier gates must remain passing),
- **minimal-scope**: each gate advances the system by the smallest practical step,
- **testable**: a gate’s scope must be verifiable,
- **strict**: failing any criterion fails the gate; “almost correct” does not pass,
- **non-speculative**: behavior not explicitly required is not credited; behavior explicitly prohibited fails the gate.

An agent may not advance to a later gate unless **all criteria** of the current gate are satisfied.

---

## 2. Organization model

This repository uses the following structural hierarchy:

- **Domain**: high-level architectural scope grouping.
- **Family**: an ordered set of gates with a shared objective and acceptance character.
- **Gate**: the smallest testable incremental milestone.

### 2.1 Domains

Domains are defined here so `PHASES.md` can reference them without redefining meanings.

Domains are **scope categories**, not a separate axis of correctness.

Recognized domains:

- `DOC_INFRA`
- `CORE`
- `SHELL_BASELINE`
- `CORE_EXTENSIONS`
- `VARIANTS`
- `BENCHMARK`

### 2.2 Families

Families are **navigational and governance partitions** over the single ordered gate
sequence.

Families:

- provide a stable table-of-contents,
- separate core vs shell vs integration milestones,
- keep the document scalable (avoid flat numbering drift).

### 2.3 Oracle policy for gates (normative)

A gate:

- defines a **target delta** (“what becomes true after this gate”), and
- names the **oracle(s)** that must pass to accept it.

Oracle policy:

- A gate MAY require multiple oracles.
- Exactly **one** oracle is the **primary oracle** for that gate (covers the newly
  introduced or expanded behavior).
- Any additional oracles listed by the gate MUST be **regression proofs** that were
  already introduced by earlier gates (re-run because the new change may affect them).
- Gates MUST NOT introduce “use-once” oracles. Oracles are reusable and remain valid as
  the system grows.