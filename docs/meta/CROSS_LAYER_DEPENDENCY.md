---
doc_id: CROSS_LAYER_DEPENDENCY
name: CROSS_LAYER_DEPENDENCY.md
title: Cross-Layer YAML Reference Dependency Policy
kind: meta
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Diagnostic-only policy for validating cross-layer semantic dependencies declared via YAML references.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
supersedes:
  - YAML_REFERENCE_POLICY
references:
  - DOCUMENTATION_SYSTEM
---

# Cross-Layer YAML Reference Dependency Policy (Normative)

## 1. Purpose

The repository documentation system is organized into conceptual layers (L0–L5 defined in `DOCUMENTATION_SYSTEM.md`) that compartmentalize:

- structural intent,
- behavioral definitions,
- proof obligations,
- and recorded execution state.

Unrestricted semantic dependencies across these layers can introduce:

- circular reasoning,
- governance leakage into development layers,
- coupling between specifications and their own proof artifacts,
- and increased maintenance complexity.

This document addresses this concern by defining a **diagnostic-only** policy for validating cross-layer _semantic dependencies_ declared in YAML front matter `references`. This policy classifies whether a particular YAML `references` edge is **expected** or **suspicious** under the layering model.

It does **not** affect:

- the fixed L0–L5 _constraint/validity_ chain, or
- graph construction determinism.

This document is normative as a **documentation system policy**, but its enforcement output is **non-blocking by default**.

---

## 2. Authoritative machine-readable policy

The authoritative policy instance is stored in:

- `YAML_REFERENCE_POLICY.json`

and validated by:

- `YAML_REFERENCE_POLICY.schema.json`

Tooling MUST evaluate each YAML `references` edge `A → B` by computing:

- `layer(A)` from the mapping table in `DOCUMENTATION_SYSTEM.md`,
- `layer(B)` from the mapping table in `DOCUMENTATION_SYSTEM.md`,

and then checking:

- whether `layer(B)` is included in `allowed_reference_targets[layer(A)]`.

Handling of violations is governed by:

- `enforcement` in `YAML_REFERENCE_POLICY.json` (typically `warning`).

---

## 3. Terms

Let:

- `layer(A)` be the layer of the referencing document
- `layer(B)` be the layer of the referenced document

This policy applies only to:

- YAML `references` (normative semantic dependencies)

It does not apply to:

- prose `@DOC_ID` mentions (those remain separate and non-authoritative)

---

## 4. Interpretation model (normative)

The layered model distinguishes between:

- **Constraint / validity flow (L0 → L5)** — fixed structural validity chain
- **Semantic dependency flow** — explicit YAML `references`

Semantic dependencies should generally follow this principle:

> A document may depend on documents that define its meaning or governance, but should not depend on documents that merely validate or record it.

This is explicitly **not** a “who references whom” law.
It is a **drift diagnostic** intended to surface meta-leakage and self-referential coupling.

---

## 5. Recommended allowed reference directions (diagnostic baseline)

Tooling SHOULD treat the following as normal:

- `L0` → any layer (integration/meta surface)
- `L1` → `L2`, `L3`, `L4`, `L0`
- `L2` → `L2` (intra-layer only)
- `L3` → `L2`
- `L4` → `L3`, `L2`
- `L5` → any layer (reporting surface)

These correspond to the default `allowed_reference_targets` in `YAML_REFERENCE_POLICY.json`.

---

## 6. Suspicious patterns (emit warning)

Tooling SHOULD treat the following as suspicious and emit a warning:

- `L2–L4` → `L0`
  - Development layers should remain meta-agnostic.
- `L2` → `L1`
  - Architecture should not depend on governance rules.
- `L3` → `L1`
  - Specifications should not depend on workflow control.
- `L4` → `L1`
  - Proof obligations must not depend on process sequencing.
  - Oracles define proof obligations.
  - Phases/gates define workflow sequencing.
  - An oracle must not depend on how the project is managed.
- `L3` → `L4`
  - A specification must define behavior independently of how it is tested.

If strict mode exists, tooling MAY treat these as errors, but this is explicitly a tooling choice controlled by `enforcement`.

---

## 7. No hard blocking (normative)

Violations of this policy:

- MUST NOT block graph construction,
- MUST NOT be treated as schema failures,
- MUST be emitted in the validation report under a dedicated section, e.g.:
  - `Cross-layer reference warnings`

This keeps the system:

- structurally deterministic,
- semantically expressive,
- non-dogmatic.

---

## 8. Rationale

- The **constraint chain** expresses validity conditions.
- The **reference edges** express semantic dependence.
- These are distinct mechanisms and must not be conflated.

Layering is a **normative interpretation model**, not a rigid import system.
