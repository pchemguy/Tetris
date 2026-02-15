---
doc_id: TERMINAL_PRESENTER_API
name: TERMINAL_PRESENTER_API.md
title: Terminal Presenter API
kind: api
scope: shell:presenter
status: active
authority: normative
gate_applies_to: 10-12
phase_applies_to: 2-5
description: Defines presenter interface and output responsibility boundaries.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - RENDERING_SPEC
---

# Terminal Presenter API

**Presenter API and Responsibility Boundary (Normative)**

---

## 1. Purpose

This document defines the **Presenter API** and its strict responsibility boundaries.

The presenter is a **terminal / output adapter** whose sole purpose is to **emit already-rendered frames** to a concrete output medium (e.g. stdout).

This document exists to:

* prevent rendering logic from leaking into I/O code,
* prevent game semantics from being re-derived from rendered output,
* keep terminal-specific behavior isolated and replaceable.

---

## 2. Role in the system

The presenter is part of the **shell**, not the simulation.

It sits *after* rendering and *before* the operating system.

```
GameState
   ↓
Renderer (pure)
   ↓  str (frame)
Presenter (I/O)
   ↓
Terminal / Output stream
```

The presenter **does not know what the game is**.

---

## 3. API contract

### 3.1 Required interface

A presenter implementation MUST expose an interface equivalent to:

```python
def present(frame: str) -> None
```

Where:

* `frame` is a **fully rendered, final representation** of the game state,
* the presenter produces **side effects only** (e.g. writes to stdout),
* no value is returned.

---

## 4. Responsibilities

The presenter MAY:

* write the frame to an output stream (stdout, stderr, file),
* clear the terminal screen,
* reposition the cursor,
* flush output buffers,
* apply terminal-specific mechanics (e.g. ANSI escape sequences),
* optionally throttle output rate *if explicitly configured* (but timing policy belongs to runtime).

The presenter MUST:

* treat the frame as **complete and authoritative**,
* emit the frame exactly as provided (byte-for-byte, modulo terminal control sequences),
* avoid inspecting or modifying the frame contents.

---

## 5. Explicit non-responsibilities (normative)

The presenter MUST NOT:

* receive or inspect `GameState`,
* parse the frame to infer gameplay semantics,
* interpret characters as “blocks”, “pieces”, or “cells”,
* decide colors, layout, symbols, or formatting rules,
* re-implement any part of `RENDERING_SPEC.md`,
* call `step()` or access the core in any way,
* control tick timing or execution flow.

Any violation of these rules is **responsibility leakage** and fails Gate 0.

---

## 6. Clarification: “opaque frame” (normative)

The phrase **“treat the frame as opaque”** means:

> The presenter must not derive *semantic meaning* from the frame content.

It does **not** prohibit:

* ANSI escape codes inside the frame,
* colored output,
* terminal control sequences.

It **does** prohibit:

* detecting filled cells by scanning characters,
* assigning colors based on parsed symbols,
* changing output based on frame structure.

If coloring, styling, or layout is desired, it must be produced by the **renderer**, not inferred by the presenter.

---

## 7. ANSI and colored output (normative)

ANSI-colored output is supported **only** under the following rule:

* If ANSI escape sequences appear in `frame`, they are treated as literal output and emitted unchanged.

Therefore:

* ANSI coloring logic belongs in the **renderer**,
* the presenter remains a dumb emitter.

To support multiple render styles (ASCII, ANSI, debug):

* use **multiple renderers**,
* not multiple presenter behaviors.

---

## 8. Configuration boundary

The presenter:

* may accept configuration parameters at construction time (e.g. output stream),
* must not load configuration files,
* must not parse CLI arguments.

Configuration discovery belongs to the **App Shell (CLI)**.

---

## 9. Testability expectations

Presenter implementations:

* are not required to be pure,
* should be mockable or replaceable in tests,
* should not be required for core or renderer tests.

Presenter behavior is typically validated indirectly via runtime/CLI tests.

---

## 10. Summary (non-normative)

* Renderer decides *what the frame looks like*.
* Presenter decides *where and how bytes are emitted*.
* Presenter never decides *what anything means*.

---
