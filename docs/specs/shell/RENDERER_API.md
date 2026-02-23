---
doc_id: RENDERER_API
name: RENDERER_API.md
title: Renderer API
status: active
authority: normative
description: Defines the pure renderer interface and its strict non-mutation guarantees.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [RENDERING_SPEC]
---

# Renderer Interface Specification

**Renderer API and Purity Contract (Normative)**

---

## 1. Purpose

This document defines the **Renderer API** and its strict purity guarantees.

The renderer is a **pure transformation layer** that converts a `GameState` into a **fully-rendered frame representation**.

This document exists to:

* prevent I/O and environment coupling,
* prevent presentation logic from leaking into runtime or presenter,
* enable deterministic snapshot testing.

---

## 2. Role in the system

The renderer sits **between the core and the presenter**.

```
GameState
   ↓
Renderer (pure)
   ↓  frame (str or bytes)
Presenter (I/O)
```

The renderer is the **only component allowed to interpret game state for presentation purposes**.

---

## 3. API contract

### 3.1 Required interface

A renderer implementation MUST expose an interface equivalent to:

```python
def render(state: GameState) -> str
```

Where:

* `state` is an immutable `GameState` defined by `CORE_API.md`,
* the return value is a **complete, final frame representation**,
* rendering is deterministic.

---

## 4. Responsibilities

The renderer MUST:

* interpret `GameState` fields as defined by `CORE_API.md`,
* apply all presentation rules defined in `RENDERING_SPEC.md`,
* produce a complete frame with no placeholders or deferred logic,
* return identical output for identical input state.

The renderer MAY:

* embed ANSI escape sequences,
* embed color or styling information,
* produce alternative representations (ASCII, ANSI, debug),
* select symbols, colors, or glyphs.

---

## 5. Explicit non-responsibilities (normative)

The renderer MUST NOT:

* perform any I/O (stdout, files, sockets),
* inspect terminal size or capabilities,
* sleep or depend on wall-clock time,
* mutate `GameState`,
* call `step()` or interact with runtime,
* load configuration or read environment variables.

Any violation is a **Gate 0 failure**.

---

## 6. Determinism guarantees

Rendering MUST be deterministic with respect to:

* `GameState`,
* renderer configuration (if any, passed explicitly).

Rendering MUST NOT depend on:

* random number generation,
* environment variables,
* system locale,
* terminal capabilities.

---

## 7. Renderer variants (normative)

Multiple renderers MAY exist, for example:

* ASCII renderer (baseline, Gate 10),
* ANSI-colored renderer,
* Debug renderer.

Each renderer MUST:

* conform to this API,
* have its own specification document if semantics differ.

The **ASCII renderer** defined by `RENDERING_SPEC.md` is the **baseline** and must always exist.

---

## 8. Testing expectations

Renderers MUST be testable via:

* pure snapshot (golden) tests,
* byte-for-byte comparison of output.

Renderers MUST NOT require a presenter to be tested.

---

## 9. Summary (non-normative)

* Renderer decides *what the frame looks like*.
* Renderer is pure, deterministic, and stateless.
* Any visual semantics (including color) belong here.

---
