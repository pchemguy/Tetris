---
name: ARCHITECTURE.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
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
- **Impure shell** (I/O, rendering, input polling, timing)

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

---

## 4. Component diagram (conceptual)

```
+-------------------+        inputs        +-------------------+
|    Input Layer    |--------------------->|                   |
| (poll / mapping)  |                      |                   |
+-------------------+                      |                   |
|     Runtime       |                      |                   |
+-------------------+       state          | (tick loop)       |
|     Renderer      |<---------------------|                   |
|   (ASCII MVP)     |                      |                   |
+-------------------+                      +---------+---------+
|
| step()
v
+-------------------+
|       Core        |
| (pure simulation) |
+-------------------+
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

Options:

- (A) None (MVP) ✅
- (B) High score file (JSON)
- (C) Replay traces (seed + input stream)
- (D) Full state snapshots

Decision:

- Out of MVP unless explicitly requested.
- Replay traces are the most valuable next step for agent evaluation.

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

## 7. Extension docs required for non-core components

The existing spec set is core-heavy. To expand cleanly, the following docs are introduced (or reserved) as architecture-level contracts:

- `DECOMPOSITION.md` (component boundaries) ✅
- `RENDERING_SPEC.md` (ASCII view conventions) (planned)
- `RUNTIME_SPEC.md` (tick rate, modes, loop semantics) (planned)
- `CLI_SPEC.md` (commands, flags, modes) (planned)
- `REPLAY_SPEC.md` (seed + inputs trace format) (optional, planned)

Agents must not implement shell behavior until the corresponding spec exists.

---

## 8. Architectural invariants (system-level)

- The core is the single source of truth for game rules.
- Renderer is side-effect free and does not mutate state.
- Runtime is the only component that calls `step()` in interactive mode.
- Tests must be able to run without any interactive UI.
- Deterministic scripted runs must be supported for evaluation.

---

## 9. Near-term roadmap (architecture-driven)

1. Complete core (Gates 0–6).
2. Add ASCII renderer under `tetris.rendering`.
3. Add scripted runtime mode (virtual time).
4. Add CLI entrypoint:
    - run scripted scenario
    - run interactive (optional)
5. Optional: replay format + runner (for evaluation harness).

---

