---
doc_id: L4_TESTING
name: L4_TESTING.md
title: L4 — Test Oracles (Proof Obligations)
status: active
authority: normative
description: Defines normative proof obligations and the role of test oracles in validating L3 contracts.
references:
  - ORACLE_CORE
  - ORACLE_SHELL_RENDERING
  - ORACLE_SHELL_RUNTIME
  - ORACLE_SHELL_CLI
  - ORACLE_SHELL_REPLAY
  - ORACLE_SHELL_CONFIG
---

# L4 — Test Oracles (Proof Obligations)

L4 defines **what must be proven** for an implementation to be considered correct.

L3 defines behavioral contracts.  
L4 defines the **proof obligations** that demonstrate those contracts are satisfied.

Tests that are not grounded in L4 oracles do not constitute authoritative proof.

---

## Document index

### Core test oracle

**Directory**: `docs/testing/oracles/core/`

| Title                         | Filename         | Role |
| ----------------------------- | ---------------- | ---- |
| Composite Core Test Oracle    | `ORACLE_CORE.md` | Defines mandatory core proof obligations and references decomposed oracle documents. |

---

### Shell-level test oracles

**Directory**: `docs/testing/oracles/shell/`

| Title                 | Filename                    | Role |
| --------------------- | --------------------------- | ---- |
| Rendering Test Oracle | `ORACLE_SHELL_RENDERING.md` | Proof obligations for ASCII rendering behavior. |
| Runtime Test Oracle   | `ORACLE_SHELL_RUNTIME.md`   | Proof obligations for deterministic runtime orchestration. |
| CLI Test Oracle       | `ORACLE_SHELL_CLI.md`       | Proof obligations for CLI behavior and exit semantics. |
| Replay Test Oracle    | `ORACLE_SHELL_REPLAY.md`    | Proof obligations for replay validation and deterministic execution. |
| Config Test Oracle    | `ORACLE_SHELL_CONFIG.md`    | Proof obligations for configuration handling and boundary enforcement. |

---

## What an oracle is

A test oracle document is a **normative specification of required proofs**.

It defines:

- mandatory test categories,
- required invariants,
- minimum acceptable test sets,
- determinism requirements,
- rejection vs error expectations.

Oracles do not describe implementation.
They describe **what must be demonstrated**.

---

## Relationship to other layers

- L3 defines behavior.
- L4 defines proof of that behavior.
- L1 defines which proofs are required for each gate.
- L2 constrains what tests are allowed to depend on (architectural boundaries).

An implementation is correct only if:

1. It conforms to L3 contracts, and  
2. It satisfies all required L4 oracles applicable to the current gate.

---

## Determinism requirement

All oracle-mandated tests must be:

- deterministic,
- reproducible,
- independent of wall-clock time,
- independent of environment state unless explicitly specified.

Determinism violations invalidate proof.

---

## Prohibitions

The following are forbidden:

- Implementing behavior to satisfy tests that is not defined in L3.
- Weakening oracle requirements without prior specification change.
- Encoding behavior only in tests without updating L3.
- Using snapshot or golden tests outside explicitly authorized oracle domains.
- Introducing architectural coupling (L2 violations) within test code.

Tests must not become a secondary source of truth.

---

## Gate applicability

Which oracle documents apply to which acceptance gates is defined exclusively in:

- `ACCEPTANCE_GATES.md`
- `TEST_PLAN.md`

L4 defines proof obligations; L1 defines when those proofs are required.
