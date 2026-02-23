---
doc_id: CONFIG_API
name: CONFIG_API.md
title: Configuration API
status: active
authority: normative
description: Defines typed configuration model used to parameterize runtime and CLI behavior.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# Config API

**Typed Configuration Objects (Normative)**

---

## 1. Purpose

This document defines the **typed configuration model** used to parameterize the application.

It exists to:

- separate configuration from control flow,
- prevent ad-hoc dicts and magic constants,
- make configuration explicit, testable, and injectable,
- allow CLI and Persistence to remain thin.

Configuration objects are **data**, not logic.

---

## 2. Authority

This document is normative.

- Configuration **structure** is defined here.
- Configuration **values** may come from CLI flags, files, or defaults.
- Configuration **loading** is defined elsewhere (CLI + Persistence).
- Runtime consumes **fully-resolved config objects only**.

---

## 3. Configuration categories

Configuration is split into **two top-level categories**:

1. **CoreConfig** — affects simulation behavior
2. **ShellConfig** — affects execution, presentation, and I/O

They must never be merged.

---

## 4. CoreConfig (simulation parameters)

```python
@dataclass(frozen=True)
class CoreConfig:
    seed: int
    board_width: int
    board_height: int
    strict_mode: bool
```

### Rules

* `CoreConfig`:
    * is immutable,
    * is passed into `new_game()` and `step()`,
    * must not contain I/O, timing, or UI concerns.
* Any change to `CoreConfig` **affects determinism** and must be reflected in tests.

---

## 5. ShellConfig (execution parameters)

```python
@dataclass(frozen=True)
class ShellConfig:
    mode: Literal["run", "script", "replay"]
    tick_rate_hz: Optional[int]        # None for virtual-time
    renderer: str                      # e.g. "ascii"
    presenter: Optional[str]           # e.g. "terminal"
    input_mode: Optional[str]          # e.g. "keyboard"
    replay_path: Optional[Path]
    config_path: Optional[Path]
```

### Rules

* `ShellConfig`:
    * is resolved **before runtime starts**,
    * may affect component selection and wiring,
    * must not affect core semantics.
* Runtime must not read files or environment variables to construct it.

---

## 6. Construction and flow

### Construction order (normative)

1. CLI parses arguments
2. Persistence loads config files (if any)
3. CLI merges:
    * defaults,
    * config file values,
    * CLI overrides
4. CLI constructs:
    * `CoreConfig`
    * `ShellConfig`
5. CLI injects both into runtime

```
CLI
 ├─ parse args
 ├─ load config (Persistence)
 ├─ build CoreConfig
 ├─ build ShellConfig
 └─ runtime = Runtime(core_cfg, shell_cfg, ...)
```

---

## 7. Prohibitions

* Runtime must not:
    * load config files,
    * inspect CLI arguments,
    * mutate config objects.
* Core must not:
    * depend on `ShellConfig`,
    * read configuration implicitly.
* Presenter and Input Driver must not:
    * read config files directly.

---

## 8. Extension rule

Adding a new configuration parameter requires:

1. Updating this document
2. Updating relevant specs (if behavior changes)
3. Updating test oracles if determinism or behavior is affected

Config changes without spec changes are invalid.

---

## 9. Summary

Configuration is **data**, not behavior.

> CLI decides.
> Persistence loads.
> Runtime consumes.
> Core obeys.

---
