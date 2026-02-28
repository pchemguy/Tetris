---
doc_id: ALIAS_MAP
name: ALIAS_MAP.md
title: Alias Map
status: active
authority: normative
description: Human-readable representation of the canonical alias mapping used for alias-invariance validation.
url: 
references:
  - ALIAS_MAP
  - GLOSSARY_NORMATIVE
---

# Alias Map

## 1. Purpose

This document defines the mapping between domain-loaded terminology and canonical semantically-neutral terms.

The purpose of this mapping is to enforce **Alias-Invariance**: mechanical renaming of domain terms MUST NOT alter implementability, correctness, or testability.

---

## 2. Mapping Table

| Domain Term | Canonical Term   | Category             | Behavioral Semantics Allowed |
| ----------- | ---------------- | -------------------- | ---------------------------- |
| tetris      | system           | system_identifier    | No                           |
| tetromino   | unit             | entity               | No                           |
| line        | full_row         | structural_condition | No                           |
| rotation    | orientation      | state_attribute      | No                           |
| bag         | permutation_pool | generator_mechanism  | No                           |

---

## 3. Normative Constraints

1. Canonical terms MUST be defined in GLOSSARY_NORMATIVE.md.
2. Normative specifications MUST use canonical terms.
3. Domain terms MAY appear only as informative aliases.
4. No behavioral requirement may depend on domain-term semantics.
5. A mechanical rename pass using ALIAS_MAP.yaml MUST preserve:
    - cross-reference integrity,
    - oracle interpretability,
    - full implementability.

---

## 4. Validation Procedure

The Alias-Invariance Gate MUST verify:

- Mechanical rename of normative docs using ALIAS_MAP.yaml.
- Zero semantic loss.
- Zero unresolved references.
- All behavioral invariants remain provable via existing test oracles.
