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

## 2.1 Governance hierarchy

This repository uses the following structural hierarchy: **Gates → Gate Families → Domains**. While gates define the smallest testable incremental milestones, defining the smallest work scope, an ordered set of gates with a shared objective forms a family. Gate families are aligned with architectural `@DECOMPOSITION`, enabling scalable definition of development workflow and ensuring that development process systematically implements project design. Development domains 
defined in `@DECOMPOSITION` provide the highest organizational level, grouping architecturally close gate families. Domains define scope of development `@PHASES`.

## 2.2 Oracle policy for gates

- A gate MAY require multiple test oracles.
- Exactly **one** oracle is the **primary oracle** for that gate (covers the newly introduced or expanded behavior).
- Any additional oracles listed by the gate MUST be **regression proofs** that were already introduced by earlier gates (re-run because the new change may affect them).
- Gates MUST NOT introduce "use-once" oracles. Oracles are reusable and remain valid as the system grows.

