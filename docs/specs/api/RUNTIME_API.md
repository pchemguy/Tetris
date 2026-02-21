---
doc_id: RUNTIME_API
name: RUNTIME_API.md
title: Runtime API
kind: api
scope: shell:runtime
status: active
authority: normative
gate_applies_to: 11
phase_applies_to: 2-5
description: Defines the runtime interface responsible for orchestrating core execution.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - RUNTIME_SPEC
---

# Runtime Interface Specification

**Runtime API and Execution Contract (Normative)**

---

## 1. Purpose

This document defines the **Runtime API** and its role as the **execution-time orchestrator**.

The runtime is responsible for **running the simulation**, not defining it.

---

## 2. Role in the system

The runtime is the **hub** during execution.

```
Input stack → Runtime → Core → Renderer → Presenter
```

It owns:

* the tick loop,
* the current `GameState`,
* the order of operations.

---

## 3. API contract

### 3.1 Required interfaces

A runtime implementation MUST expose interfaces equivalent to:

```python
def run_scripted(
    initial_state: GameState,
    input_provider: Callable[[], tuple[InputEvent, ...]]
) -> None
```

```python
def run_interactive() -> None
```

(Exact signatures may vary; semantics are normative.)

---

## 4. Responsibilities

The runtime MUST:

1. Maintain the current `GameState`
2. For each tick:
    1. acquire inputs,
    2. call `step(state, inputs, config)` **exactly once**,
    3. replace state with returned state,
    4. call `renderer.render(state)`,
    5. pass frame to presenter,
3. terminate on `state.is_game_over`.

The runtime MAY:

* support multiple execution modes (scripted, replay, interactive),
* support configurable tick rates (interactive only).

---

## 5. Explicit non-responsibilities (normative)

The runtime MUST NOT:

* implement game rules,
* modify `GameState` outside `step()`,
* interpret rendered output,
* parse command-line arguments,
* load configuration or replay files,
* perform OS I/O directly.

Runtime is **not** the composition root.

---

## 6. Determinism rules

* Scripted and replay modes MUST be fully deterministic.
* Interactive mode MAY involve wall-clock time, but must not affect core logic.

---

## 7. Configuration boundary

The runtime:

* consumes **already-resolved configuration objects**,
* does not discover or load configuration,
* does not select components.

All wiring is performed by the **App Shell (CLI)**.

---

## 8. Error handling

If `step()` raises an exception:

* runtime MUST stop execution,
* runtime MUST surface the error,
* runtime MUST NOT attempt recovery.

---

## 9. Summary (non-normative)

* Runtime is the execution hub.
* Runtime orchestrates; it does not decide semantics.
* Runtime owns *when*, not *what*.

---
