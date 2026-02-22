## 1. Purpose and acceptance semantics

This document defines **acceptance gates** for this project. Acceptance gates are **ordered, testable milestones** that evolve the repository from one well-defined state to the next.

Acceptance gates:

- constrain development and agent scope,
- prevent premature feature creep,
- provide objective “done / not done” criteria.

A gate is considered **passed** only when:

1. All **mandatory scope** defined for that gate is implemented, and
2. All **mandatory proofs** required by that gate pass, as defined by its associated **test oracle(s)**.

Gate rules:

- **Cumulative** — Each gate subsumes all prior gates. Earlier gates must remain passing.
- **Minimal-scope** — Each gate advances the system by the smallest practical, independently testable step.
- **Testable** — A gate’s scope must be verifiable through explicit proof obligations.
- **Strict** — Failing any criterion fails the gate. “Almost correct” does not pass.
- **Non-speculative** — Behavior not explicitly required is not credited. Behavior explicitly prohibited fails the gate.

An agent or developer may not advance to a later gate unless **all criteria of the current gate are satisfied**.

---

## 2. Organization model

### 2.1 Governance hierarchy

Acceptance governance is structured as:

**Gates → Gate Families → Domains**

Each level serves a distinct purpose:

- **Gate**  
  The smallest testable incremental milestone. A gate defines a concrete scope delta and its associated proof obligations.
- **Gate Family**  
  An ordered set of related gates with a shared architectural objective. Families organize gates along architectural boundaries defined in `@DECOMPOSITION`.
- **Domain**  
  A higher-level architectural grouping derived from `@DECOMPOSITION`. Domains group architecturally related families and define structural development blocks.

Domains define architectural scope and are referenced by `@PHASES` to constrain allowed development areas.

This hierarchy ensures that:

- Implementation proceeds in alignment with architectural design,
- Structural boundaries defined in `@DECOMPOSITION` are respected,
- Development workflow remains scalable as the project grows.

---

### 2.2 Oracle policy for gates

Test oracles define the proof obligations required to accept a gate.

The following rules apply:

- A gate MAY require multiple test oracles.
- Exactly **one** oracle must be designated as the **primary oracle** for that gate. The primary oracle covers the newly introduced or expanded behavior.
- Any additional oracles listed by the gate must be **regression oracles** introduced by earlier gates and re-run because the new change may affect previously validated behavior.
- Gates must not introduce “use-once” oracles. Oracles are reusable proof artifacts and remain valid as the system evolves.

No gate may rely on undefined or implicit proof criteria. All acceptance conditions must be traceable to explicit oracle documents.
