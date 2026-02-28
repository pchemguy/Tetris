---
doc_id: GLOSSARY_NORMATIVE
name: GLOSSARY_NORMATIVE.md
title: Normative Glossary
status: active
authority: normative
description: Canonical definitions of behaviorally relevant terms used in normative specifications.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69a27bc9-5f60-838f-b2dc-e7a32de243ca
---

# Normative Glossary

## 1. Purpose

This document defines canonical, semantically-neutral terms used in normative specifications.

Normative requirements MUST reference these canonical terms. Domain-loaded aliases (e.g., “tetromino”) MUST NOT introduce additional semantics beyond what is defined here.

## 2. Definition Structure

Each glossary entry MUST include:

- **Canonical Term**
- **Category** (entity, state, transition, invariant, rule, etc.)
- **Formal Definition**
- **Defined In** (authoritative section reference)
- **Behavioral Impact** (Yes/No)

---

## 3. Canonical Terms

### 3.1 Unit

- **Category:** entity
- **Formal Definition:**  
  A finite ordered set of grid offsets defining occupied cells relative to a reference coordinate.
- **Defined In:** `@SHAPES_AND_ROTATIONS` §2
- **Behavioral Impact:** Yes

---

### 3.2 Orientation

- **Category:** state attribute
- **Formal Definition:**  
  A discrete transformation index selecting one of the enumerated rotational states of a Unit.
- **Defined In:** `@SHAPES_AND_ROTATIONS` §2
- **Behavioral Impact:** Yes

---

### 3.3 Grid

- **Category:** state container
- **Formal Definition:**  
  A bounded two-dimensional discrete coordinate system with occupancy state per cell.
- **Defined In:** `@GAME_STATE` §1
- **Behavioral Impact:** Yes
