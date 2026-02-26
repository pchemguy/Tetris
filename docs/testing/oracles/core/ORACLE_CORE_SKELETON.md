---
doc_id: ORACLE_CORE_SKELETON
name: ORACLE_CORE_SKELETON.md
title: Core Package Skeleton Test Oracles
status: active
authority: normative
description: Mandatory test oracles for establishing an importable `tetris` package skeleton with no implementation behavior and no shell components.
references:
  - CORE_API
---

# ORACLE_CORE_SKELETON

**Core — Package Skeleton Test Oracles (Normative)**

## 1. Purpose

This document defines the **mandatory automated test oracles** for:

* creating the `tetris` Python package namespace from an empty source tree,
* ensuring the package is importable in editable mode,
* enforcing strict absence of shell components at this stage,
* enforcing import-time isolation (no side effects; no subsystem initialization).

It applies to the **core package skeleton only**.

## 2. Harness assumptions

The test harness must be able to:

* import Python modules (`import tetris`, `import tetris.core`) within the test runner environment,
* inspect the filesystem for presence/absence of specific files and directories,
* introspect module attributes (e.g., `hasattr(module, "__all__")`),
* detect that forbidden modules are not importable (expecting `ModuleNotFoundError`).

Tests MUST run in a clean Python process environment (no pre-imported `tetris` modules).

## 3. Oracle set

### ORACLE API1: Package root directory exists

Construct/Given:

* repository checkout.

Assert/Then:

* directory `tetris/src/tetris/` MUST exist.

### ORACLE API2: Package root marker exists

Assert/Then:

* file `tetris/src/tetris/__init__.py` MUST exist.

### ORACLE API3: Root package is importable

Action/When:

* `import tetris`

Assert/Then:

* the import MUST succeed.
* importing `tetris` MUST NOT raise warnings-as-errors due to side effects (tests may treat warnings as failures).

### ORACLE API4: Root import is isolated (no implicit shell import)

Action/When:

* In a fresh Python process (or after clearing `sys.modules` of any `tetris*` entries), execute: `import tetris`.

Assert/Then:

* `tetris` import MUST NOT implicitly import any shell component packages.

Operationally, immediately after `import tetris`:

* `sys.modules` MUST NOT contain any of:
    - `"tetris.runtime"`
    - `"tetris.rendering"`
    - `"tetris.cli"`
    - `"tetris.persistence"`
    - `"tetris.input"`
    - `"tetris.presentation"`
    - `"tetris.telemetry"`

Optional (allowed as an additional check, not a substitute):

* Attempting to import the above modules MAY be asserted to fail with `ModuleNotFoundError` at this stage, but this is a *separate* property from "not implicitly imported".

> This oracle enforces import-time isolation: importing the package root must not drag in shell subsystems or produce hidden coupling.

## 4. Forbidden behavior

The following are prohibited during the scope governed by this oracle:

* requiring `tetris.core` to exist,
* introducing any shell component modules/packages (see ORACLE API4),
* import-time side effects that initialize UI, start loops, perform I/O, read environment configuration, or touch the filesystem outside test-controlled paths.

## 5. Minimum required test set

For compliance, the minimum required set is:

* API1, API2, API3, API4

### Notes for implementers and test authors (non-normative)

* Prefer a single test that asserts API1–API4, but keep assertions granular for diagnostics.
* A simple "forbidden import list" loop is acceptable as long as it is deterministic.
