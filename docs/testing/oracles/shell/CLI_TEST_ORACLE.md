---
doc_id: CLI_TEST_ORACLE
name: CLI_TEST_ORACLE.md
title: CLI Test Oracle
kind: testing
scope: shell:cli
status: active
authority: normative
gate_applies_to: 12
phase_applies_to: 2-5
description: Defines mandatory behavioral and error-handling tests for CLI commands.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - CLI_SPEC
---

# CLI TEST ORACLE

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
- If interactive mode is not implemented, behavior must still follow `CLI_SPEC.md`  (e.g., error with specified exit code), but the command must exist.

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
