---
doc_id: ORACLE_SHELL_REPLAY
name: ORACLE_SHELL_REPLAY.md
title: Replay Test Oracle
status: active
authority: normative
description: Defines deterministic replay validation and execution correctness requirements.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [REPLAY_SPEC, RUNTIME_SPEC]
---

# REPLAY TEST ORACLE

**Replay – Mandatory Test Oracles (Normative)**

## 1. Purpose

This document maps `REPLAY_SPEC.md` to mandatory automated tests for replay loading and execution.

It is a contract: replay support is considered “correct” only if it satisfies these oracles.

This document corresponds to **Acceptance Gate 13**.

---

## 2. Test harness assumptions

Tests must be able to:

- load replay JSON files (fixtures),
- run replay execution using scripted runtime (virtual-time),
- compare resulting final `GameState` deterministically,
- assert that malformed replay files are rejected strictly.

---

## 3. Replay loading and validation oracles

### ORACLE L1: Schema validation

Replay loader must reject:

- missing required keys (`version`, `seed`, `ticks`),
- invalid `version`,
- non-integer `seed`,
- non-list `ticks`,
- ticks entries that are not lists.

### ORACLE L2: Input validation

Replay loader must reject:

- unknown input event names,
- non-string event entries.

### ORACLE L3: Strictness (no auto-correction)

- Malformed replays must not be “fixed” or normalized.
- Any invalidity is an error.

---

## 4. Replay execution oracles

### ORACLE E1: Seed governs RNG deterministically

- Replay execution must initialize the core RNG using replay `seed`.
- Given identical replay file, the piece sequence must be identical.

### ORACLE E2: One tick per replay entry

- For replay with `len(ticks) == N`:
    - execution must attempt exactly N ticks unless terminated early by game over.
- Tick `i` must apply exactly `ticks[i]` as its inputs.

### ORACLE E3: Early termination on game over

- If game over occurs at tick `k`, replay execution terminates immediately after tick `k`  (and must not attempt tick `k+1`).

### ORACLE E4: Deterministic final state

- Running the same replay twice produces identical final `GameState`.
- This must include all state fields relevant to determinism (board, score, level, RNG state, etc.).

---

## 5. Minimum required test set (Gate 13)

Gate 13 is accepted only if at least the following pass:

- L1, L2, L3
- E1, E2, E3, E4

---
