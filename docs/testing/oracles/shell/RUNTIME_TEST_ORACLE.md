---
doc_id: RUNTIME_TEST_ORACLE
name: RUNTIME_TEST_ORACLE.md
title: Runtime Test Oracle
kind: oracle
scope: shell:runtime
status: active
authority: normative
gate_applies_to: 11
phase_applies_to: 2-5
description: Defines deterministic execution and orchestration tests for scripted runtime mode.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - RUNTIME_SPEC
  - RUNTIME_API
---

# RUNTIME TEST ORACLE

**Scripted Runtime (Virtual-Time) – Mandatory Test Oracles (Normative)**

## 1. Purpose

This document maps `RUNTIME_SPEC.md` to mandatory automated tests for the scripted runtime.

It is a contract: a scripted runtime is considered “correct” only if it satisfies these oracles.

This document corresponds to **Acceptance Gate 11**.

---

## 2. Test harness assumptions

Tests must be able to:

- execute the scripted runtime in-process,
- provide a deterministic `CoreConfig` (seeded),
- provide per-tick input sequences,
- observe:
    - how many ticks executed,
    - whether `step()` is called exactly once per tick,
    - whether rendering is invoked at the required cadence,
    - termination conditions.

Tests must not rely on wall-clock behavior.

---

## 3. Virtual-time execution oracles

### ORACLE V1: No sleeping / no wall-clock dependency

- Scripted runtime must not call `time.sleep` (or equivalent).
- In tests, runtime should complete without delays proportional to number of ticks.

### ORACLE V2: Exactly one `step()` call per tick

- For N executed ticks, `step()` must be invoked exactly N times.
- Runtime must not call `step()` more than once per tick.

### ORACLE V3: Inputs are applied per tick

- For tick `i`, runtime must pass the exact input list specified for tick `i` to `step()`.

### ORACLE V4: Rendering cadence

- Runtime must render at least once per tick in scripted mode.
- If you later permit “render every N ticks”, that option must be explicitly specified and tested.
  (Current default: every tick.)

### ORACLE V5: Deterministic final state

- Given identical:
    - seed/config,
    - scripted inputs,
    - max tick count,
      the final state must be identical across runs.

### ORACLE V6: Early termination on game over

- If `state.is_game_over` becomes true at tick `k`, runtime must terminate immediately after rendering the final state for that tick.
- Runtime must not execute tick `k+1`.

---

## 4. Error propagation oracles

### ORACLE E1: Core exceptions are not suppressed

- If `step()` raises, runtime must stop and surface the exception to the caller (or return an error result explicitly documented by the runtime API).
- Silent recovery fails the oracle.

---

## 5. Minimum required test set (Gate 11)

Gate 11 is accepted only if at least the following pass:

- V1, V2, V3, V4, V5, V6
- E1

---
