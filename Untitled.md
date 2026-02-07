

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
```

---

## `docs/CLI_TEST_ORACLE.md`

```md
# CLI_TEST_ORACLE.md
**CLI – Mandatory Test Oracles (Normative)**

## 1. Purpose

This document maps `CLI_SPEC.md` to mandatory automated tests for the CLI layer.

It is a contract: the CLI is considered “correct” only if it satisfies these oracles.

This document corresponds to **Acceptance Gate 12**.

---

## 2. Test harness assumptions

Tests must be able to invoke the CLI:

- via `python -m tetris ...` (preferred), or
- via the CLI entry function if one exists.

Tests must be able to assert:

- process exit code (or returned code),
- stdout/stderr content (at least minimally),
- that core/runtime exceptions are not suppressed.

---

## 3. Command availability oracles

### ORACLE C1: `run` command exists

- `tetris run` is accepted by argument parsing.
- If interactive mode is not implemented, behavior must still follow `CLI_SPEC.md`
  (e.g., error with specified exit code), but the command must exist.

### ORACLE C2: `script` command exists

- `tetris script <script_file>` is accepted and routes to scripted execution.

### ORACLE C3: `replay` command exists

- `tetris replay <replay_file>` is accepted and routes to replay execution.

---

## 4. Exit code oracles

### ORACLE X1: Normal termination exits 0

- A valid invocation that completes normally must exit code `0`.

### ORACLE X2: Invalid CLI usage exits 1

- Missing required arguments (e.g., `tetris script` without file) exits `1`.

### ORACLE X3: Runtime error exits 2

- Runtime failures that are not core invariant violations exit `2`.

### ORACLE X4: Core invariant violation exits 3

- If a core invariant violation occurs and is surfaced as such, exit `3`.

---

## 5. Error propagation oracles

### ORACLE P1: CLI does not suppress core exceptions

- CLI must not catch-and-ignore core invariant violations.
- CLI must not silently downgrade invariant violations into success.

---

## 6. Minimum required test set (Gate 12)

Gate 12 is accepted only if at least the following pass:

- C1, C2, C3
- X1, X2
- P1

Additionally, at least one test must assert exit codes for error cases:
- either X3 or X4 (or both).

---
```

---

## `docs/REPLAY_TEST_ORACLE.md`

```md
# REPLAY_TEST_ORACLE.md
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

- If game over occurs at tick `k`, replay execution terminates immediately after tick `k`
  (and must not attempt tick `k+1`).

### ORACLE E4: Deterministic final state

- Running the same replay twice produces identical final `GameState`.
- This must include all state fields relevant to determinism (board, score, level, RNG state, etc.).

---

## 5. Minimum required test set (Gate 13)

Gate 13 is accepted only if at least the following pass:

- L1, L2, L3
- E1, E2, E3, E4

---
```

---

