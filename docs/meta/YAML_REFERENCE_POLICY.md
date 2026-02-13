---
doc_id: YAML_REFERENCE_POLICY
name: YAML_REFERENCE_POLICY.md
title: YAML Reference Policy
kind: meta
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines the diagnostic policy for validating cross-layer YAML `references` edges.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# YAML Reference Policy (Normative)

This document defines a **diagnostic-only** policy for validating cross-layer *semantic dependencies* declared in YAML front matter via `references: [...]`. It does not affect the fixed L0–L5 constraint chain; it only classifies whether a particular `references` edge is expected or suspicious under the repository’s layering model.

The authoritative policy instance is stored in `YAML_REFERENCE_POLICY.json` and validated by `YAML_REFERENCE_POLICY.schema.json`. Tooling evaluates each YAML `references` edge `A → B` by computing `layer(A)` and `layer(B)` and checking whether `layer(B)` is in `allowed_reference_targets[layer(A)]`; violations are handled according to `enforcement` (typically `warning`).

---
