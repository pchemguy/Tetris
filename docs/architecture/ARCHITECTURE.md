---
doc_id: ARCHITECTURE
name: ARCHITECTURE.md
title: System Architecture
status: active
authority: normative
description: High-level system architecture and design decisions (Functional Core / Shell).
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
references: [DECOMPOSITION]
---

# ARCHITECTURE

**System Architecture, Options, and Chosen Defaults (Normative)**

## 1. Purpose

This document describes the overall architecture of the Tetris application and records key architectural decisions and options.

It exists to:

- make “the big picture” explicit,
- constrain non-core development,
- prevent UI/runtime decisions from contaminating the core,
- provide a stable target for agent roles/skills.

---

## 2. Architectural goal

A modular system with a strict separation between:

- **Pure deterministic core** (simulation)
- **Impure shell** (input acquisition, input policy, presentation, I/O, timing)

This ensures:

- correctness is provable via tests,
- interactive behavior is replaceable,
- agentic development can proceed incrementally.

---

## 3. Primary architectural pattern

### 3.1 Pattern: Functional Core, Imperative Shell

- Core is referentially transparent at the API level:
    - `step()` is deterministic and returns a new state.
- Shell handles:
    - time scheduling,
    - user interaction,
    - output formatting,
    - persistence.

This is the chosen pattern.

Within the imperative shell, responsibilities are further separated into:

- pure transformation components (e.g. rendering),
- I/O adapters (input drivers, presenters),
- coordination logic (runtime).

These separations are architectural requirements, not implementation details. Concrete component boundaries are defined in `@DECOMPOSITION`; this document defines architectural intent only.

---

## 4. Component diagram (conceptual)

```
+----------------------+        raw input       +----------------------+
|   Input Driver (I/O) |----------------------->|                      |
+----------------------+                        |                      |
        |                                       |                      |
        v                                       |                      |
+----------------------+     InputEvent(s)      |                      |
| Input Controller     |----------------------->|        Runtime       |
| (mapping / policy)   |                        |    (orchestrator)    |
+----------------------+                        |          |           | 
                                                |          v           | 
                                                |      render()        | 
                                                |          |           | 
                                                |          v           | 
                                                |     Renderer (pure)  | 
                                                |          |           | 
                                                |          v           | 
                                                |   Presenter (I/O)    | 
                                                +----------+-----------+ 
                                                           |
                                                           | step()
                                                           v 
                                                +----------------------+
                                                |        Core          |
                                                |  (pure simulation)   | 
                                                +----------------------+
                                                
```

### 4.1 Data flow

```
Input Driver  →  
                \
Input Controller → Runtime → Core → Renderer → Presenter
```

### 4.2 Control flow

```
                +------------------+
                |   Input Driver   |
                +------------------+
                         |
                         v
                +------------------+
                | Input Controller |
                +------------------+
                         |
 ========                v
+--------+      +------------------+      +----------+
|| Core || <--- |     Runtime      | ---> | Renderer |
+--------+      +------------------+      +----------+
 ========                |
                         v
                +------------------+
                |    Presenter     |
                +------------------+
```

---

## 5. Technology options and decisions

### 5.1 Rendering options

Options:

- (A) ASCII terminal renderer (no deps) ✅ chosen for MVP
- (B) curses-based terminal UI (more capability, more complexity)
- (C) pygame / SDL (graphics, extra deps)
- (D) web UI (overkill for benchmark)

Decision:

- Implement (A) first: deterministic, minimal, reviewable.

### 5.2 Input options

Options:

- (A) Scripted inputs (from file / list) ✅ required for tests and replays
- (B) Blocking terminal input (simple but awkward)
- (C) Non-blocking terminal input (platform complexity)
- (D) curses-based input

Decision:

- MVP supports (A) and optionally (B).
- Non-blocking interactive input can be added later, isolated in `tetris.input`.

### 5.3 Runtime timing options

Options:

- (A) Virtual-time stepping (no sleep) ✅ required for deterministic runs
- (B) Real-time loop (sleep-based) ✅ optional for interactive play
- (C) Event-driven async loop (unnecessary)

Decision:

- Provide a runtime that can run in:
    - deterministic “scripted/virtual” mode, and
    - optional “interactive real-time” mode.

### 5.4 Persistence options

Persistence is out of MVP unless explicitly requested. When introduced, persistence splits into:

- **Persisted artifacts (what):**
    - (A) None (MVP) ✅
    - (B) Configuration (shell-level settings)
    - (C) High scores
    - (D) Replay traces (seed + per-tick inputs) ✅ highest evaluation value
    - (E) Full state snapshots (debugging / audit)
- **Storage formats (how):**
    - (1) INI
    - (2) JSON
    - (3) YAML
    - (4) SQLite

#### Options: storage formats (how)

**INI**
- Pros: stdlib (`configparser`), human-editable, stable.
- Cons: limited typing/structure; awkward for nested schemas; poor fit for replay traces.

**JSON**
- Pros: stdlib (`json`), strict typing surface, deterministic serialization achievable, excellent for replay traces and snapshots.
- Cons: less ergonomic for comments; schema validation needs explicit code.

**YAML**
- Pros: very human-friendly for config; supports comments and richer structures.
- Cons: requires third-party dependency; parser behavior and type coercion can add accidental complexity; less ideal for a minimal benchmark.

**SQLite**
- Pros: structured querying, robust for growing datasets (many replays, telemetry), transactional integrity.
- Cons: introduces schema management; overkill for early benchmark artifacts; adds operational surface not needed for determinism.

**Practical guidance (aligned to gates/phases)**

- **Phase 2 / Gate 13 (Replay)**: JSON is the right default (stdlib + deterministic + diffable).
- **Config files** (when you add them): INI or JSON both fit “no extra deps”; YAML only if you explicitly value human authoring/comments enough to justify a dependency.
- **SQLite** only makes sense when you have _many_ artifacts (hundreds/thousands of replays, telemetry records) and want query ability—i.e., later “benchmark scaling” phase.

#### Default decisions (current)

- MVP: **no persistence**.
- If persistence is introduced for evaluation (recommended first): use **JSON replay traces**.
    - Rationale: deterministic, minimal dependencies, diffable, CI-friendly.

Non-goals (until explicitly added):

- YAML dependency for baseline benchmark.
- SQLite database management for baseline benchmark.

---

## 6. Codebase layering and allowed dependencies

### 6.1 Core purity constraints

Core must not depend on:

- terminal libraries,
- windowing systems,
- filesystem IO,
- time.sleep / clocks,
- random sources other than the seeded RNG encapsulated in state.

### 6.2 Shell dependencies

Shell may depend on:

- standard library I/O
- terminal utilities
- optional third-party UI libs (only if kept isolated)

---

## 7. Architectural invariants (system-level)

- The core is the single source of truth for game rules.
- Renderer is side-effect free and does not mutate state.
- Runtime is the only component that calls `step()` in interactive mode.
- Tests must be able to run without any interactive UI.
- Deterministic scripted runs must be supported for evaluation.
- Rendering semantics and output side effects are strictly separated.
- The App Shell (CLI) is the composition root: it loads external data (config/replay) via Persistence and wires dependencies; the runtime does not load files or discover configuration.

---

## 8. Near-term roadmap (architecture-driven)

1. Complete core (Gates 0–6).
2. Add ASCII renderer under `tetris.rendering`.
3. Add scripted runtime mode (virtual time).
4. Add CLI entrypoint:
    - run scripted scenario
    - run interactive (optional)
5. Optional: replay format + runner (for evaluation harness).

---
