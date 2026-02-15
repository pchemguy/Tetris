---
doc_id: CONFIG_TEST_ORACLE
name: CONFIG_TEST_ORACLE.md
title: Configuration Test Oracle
kind: oracle
scope: shell:persistence
status: draft
authority: normative
gate_applies_to: none
phase_applies_to: none
description: Defines validation requirements for configuration model and parsing behavior.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references:
  - CONFIG_API
---

# CONFIG TEST ORACLE

**Configuration Contract Test Oracle (Normative)**

---

## 1. Purpose

This document defines the **mandatory automated tests** that prove configuration handling is:

- structurally correct (typed objects, not ad-hoc dicts),
- deterministic (same inputs → same config objects),
- properly layered (core vs shell separation),
- correctly bounded (CLI composes; runtime consumes; core obeys),
- non-leaky (no hidden file/env reads in runtime/core).

This oracle is **normative**: passing ad-hoc tests is insufficient if the tests defined here are missing.

---

## 2. Scope and gate applicability

### 2.1 Applies to

- **Gate 0** (discovery / boundary compliance): structural checks required
- Any gate that introduces or changes configuration wiring (typically **Gate 12+**)

### 2.2 Out of scope

- Specific file formats (INI/JSON/YAML/SQLite) unless a persistence spec requires them.
- Interactive input timing correctness (belongs to runtime/presenter/input specs and oracles).

---

## 3. Preconditions

The following must exist and match `CONFIG_API.md`:

- `CoreConfig` (immutable dataclass or equivalent)
- `ShellConfig` (immutable dataclass or equivalent)

Runtime must accept already-resolved config objects and must not load configuration.

---

## 4. Mandatory tests

Each test below is **REQUIRED** unless explicitly marked optional.

### 4.1 Typed config objects exist and are immutable (REQUIRED)

**Goal:** Prove config objects are typed and immutable.

**Tests:**

1. `test_core_config_is_dataclass_and_frozen`
    - `dataclasses.is_dataclass(CoreConfig) is True`
    - attempting to assign `core_cfg.seed = ...` raises (e.g., `FrozenInstanceError`)
2. `test_shell_config_is_dataclass_and_frozen`
    - `dataclasses.is_dataclass(ShellConfig) is True`
    - attempting to assign `shell_cfg.mode = ...` raises

---

### 4.2 Core vs shell separation (REQUIRED)

**Goal:** Prove that core does not depend on shell configuration.

**Tests:**

1. `test_core_config_has_no_shell_fields`
    - `CoreConfig` contains only simulation parameters (seed/board dims/strictness, etc. per `CONFIG_API.md`)
    - no paths, renderer names, tick rate, etc.
2. `test_core_step_accepts_core_config_only`
    - `step(...)` signature accepts `CoreConfig` (directly or via a parameter named `config` documented as `CoreConfig`)
    - test fails if `ShellConfig` is required/accepted by core API.

---

### 4.3 Deterministic config composition (REQUIRED)

**Goal:** Given identical inputs, config objects must be identical.

**Test design note:** This requires a pure “composition” helper in CLI or config module, e.g. `resolve_configs(defaults, file_values, cli_overrides) -> (CoreConfig, ShellConfig)`. If such helper does not exist, add it; do **not** test by forking subprocesses unless CLI oracle requires it.

**Tests:**

1. `test_resolve_configs_is_deterministic`
    - Call the resolver twice with identical inputs.
    - Assert returned `CoreConfig` and `ShellConfig` are equal (`==`) and hash-stable if hashable.
2. `test_resolve_configs_cli_overrides_win`
    - Provide defaults + file values + CLI overrides with conflicts.
    - Assert the override precedence matches `CONFIG_API.md`:
        `defaults < file < CLI`.

---

### 4.4 Runtime consumes config; does not discover or load it (REQUIRED)

**Goal:** Prevent “runtime reads config files” and similar leakage.

**Tests (one of the following strategies is required):**

#### Strategy A — monkeypatch hard-fail on file/env access (preferred)

1. `test_runtime_does_not_read_env_or_files_during_init_or_run`
    - Monkeypatch:
        - `builtins.open` to raise if called
        - `os.environ.__getitem__` / `os.getenv` to raise if called
        - optionally `pathlib.Path.open` to raise if called
    - Instantiate runtime with valid configs and stubbed dependencies.
    - Run a tiny scripted loop (0–2 ticks).
    - Assert no exception from patched functions (i.e., they were not called).

#### Strategy B — import boundary assertions (allowed if you can’t patch)

2. `test_runtime_does_not_import_persistence_or_cli`
    - Import runtime module and inspect `sys.modules` / module attributes to ensure it did not import `tetris.persistence` or `tetris.cli`.
    - This is weaker than Strategy A but acceptable as supplement.

At least **one** of A or B must exist; A is strongly preferred.

---

### 4.5 Core is independent of persistence/CLI (REQUIRED)

**Goal:** Ensure core never depends on shell components.

**Tests:**

1. `test_core_does_not_import_shell_packages`
    - Import `tetris.core` (or its package root).
    - Assert that importing core does not trigger imports of:
        - `tetris.runtime`, `tetris.cli`, `tetris.persistence`, `tetris.presentation`, `tetris.input`.
    - Practical approach:
        - clear `sys.modules` entries for these packages before import,
        - import core,
        - assert those keys remain absent.

---

### 4.6 Optional: round-trip serialization stability (OPTIONAL)

Only add this if a persistence spec defines config file formats.

**Goal:** Saving and loading config yields the same config objects.

**Tests:**

- `test_config_round_trip_json` / `test_config_round_trip_ini` / etc.
- Assert `loaded_cfg == original_cfg`.

---

## 5. Required naming and placement

- Tests must live under `tetris/tests/`.
- Use explicit names matching the oracle items, e.g.:
    - `tests/test_config_api.py`
    - `tests/test_config_resolution.py`
    - `tests/test_config_boundaries.py`

---

## 6. Pass criteria

This oracle **passes** only if:

- all REQUIRED tests exist, and
- all REQUIRED tests pass, and
- no test is weakened to avoid enforcing the boundaries defined in `CONFIG_API.md`.

---

## 7. Prohibitions

Tests must not:

- permit runtime to load configuration implicitly,
- rely on “whatever the environment happens to provide”,
- silently skip assertions when components are missing.

If required components are missing, tests must **fail loudly** with actionable messages.

---
