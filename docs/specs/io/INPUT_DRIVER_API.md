---
doc_id: INPUT_DRIVER_API
name: INPUT_DRIVER_API.md
title: Input Driver API
status: active
authority: normative
description: Defines input driver interface and strict responsibility boundaries.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [INPUT_MODEL]
---

# Input Driver API

**Input Driver API and Responsibility Boundary (Normative)**

---

## 1. Purpose

This document defines the **Input Driver API** and its strict responsibility boundaries.

The input driver is the **environment-facing input adapter** responsible for acquiring **raw input signals** from the operating system or execution environment.

This document exists to:

* isolate OS/platform dependencies,
* prevent input policy from leaking into I/O code,
* ensure determinism and testability of the core.

---

## 2. Role in the system

The input driver is part of the **shell**, not the simulation.

It sits *before* input interpretation and *before* the runtime tick logic.

```
OS / Environment
   ↓
Input Driver (I/O)
   ↓  raw signals
Input Controller (policy)
   ↓  InputEvent
Runtime
```

The input driver **does not know what inputs mean**.

---

## 3. API contract

### 3.1 Required interface

An input driver MUST expose an interface equivalent to:

```python
def poll_raw_inputs() -> tuple[Any, ...]
```

Where:

* the return value is a finite collection of **raw input signals**,
* the contents are intentionally unspecified (keys, codes, tokens),
* no interpretation is performed at this level.

Blocking behavior must be explicitly documented by the implementation.

---

## 4. Responsibilities

The input driver MAY:

* read from stdin, keyboard, pipes, sockets, or files,
* perform non-blocking polling,
* normalize OS-specific input formats into a simpler raw representation,
* buffer raw input events between polls.

The input driver MUST:

* return raw input signals without semantic interpretation,
* avoid applying per-tick policies,
* avoid mapping inputs to game actions.

---

## 5. Explicit non-responsibilities (normative)

The input driver MUST NOT:

* emit `InputEvent` values,
* map keys to game actions,
* implement key repeat, debouncing, or ordering rules,
* mutate `GameState`,
* call `step()` or access the core,
* control tick timing,
* load configuration or read CLI arguments.

Any such behavior is **policy leakage** and fails Gate 0.

---

## 6. Relationship to Input Controller (normative)

* The **input driver** acquires *signals*.
* The **input controller** applies *meaning and policy*.

Only the input controller:

* maps raw signals to `InputEvent` values,
* enforces per-tick semantics defined in `INPUT_MODEL.md`,
* decides which inputs are accepted, rejected, or ignored.

---

## 7. Determinism constraints

In scripted or replay modes:

* the input driver SHOULD be replaced by a deterministic input provider,
* or bypassed entirely.

Non-deterministic drivers (e.g. live keyboard input):

* must not affect core determinism,
* must be isolated to interactive runtime modes.

---

## 8. Configuration boundary

The input driver:

* may accept configuration at construction time (e.g. device selection),
* must not discover configuration itself,
* must not read files unless explicitly designed as a file-backed driver.

All configuration loading belongs to the **App Shell (CLI)**.

---

## 9. Testability expectations

Input driver implementations:

* are not required for core correctness,
* should be replaceable with mocks or scripted drivers,
* must not be required for passing core test oracles.

---

## 10. Summary (non-normative)

* Input Driver: *“What signals happened?”*
* Input Controller: *“What do they mean for this tick?”*
* Core: *“Given these events, what happens?”*

---
