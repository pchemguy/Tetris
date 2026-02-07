---
name: SEED.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

## Q1

This project focuses on development of prompting system for agentic software development. It will focus on implementing the classic Tetris game.

## A1

Got it: you are building a **prompting system for agentic software development**, and the **reference implementation target is classic Tetris**.

Here is a tight project framing you can drop straight into your repo docs and start iterating on.

## Project intent

### Primary deliverable

A **prompting system** (templates + protocols + evaluation harness) that reliably guides an agent through:

* planning,
* implementing,
* validating,
* and refactoring
  a non-trivial, self-contained software product.

### Reference product

**Classic Tetris** is the *vehicle* - useful because it forces:

* state machines + deterministic simulation,
* real-time input handling,
* rendering loop,
* collision + rotation rules,
* scoring/levels,
* persistence/config,
* tests around pure logic.

## What "success" looks like

### Prompting-system success criteria

* **Repeatability**: the same prompts produce consistent outcomes across runs.
* **Controllability**: constraints (no speculative behavior, tests-first, limited scope edits, etc.) are actually obeyed.
* **Auditability**: every agent action yields artifacts: plan, diffs, rationale, test results, checkpoints.
* **Progress under friction**: when ambiguity or failures occur, the agent escalates correctly (asks, isolates, probes) instead of thrashing.

### Tetris success criteria (MVP)

* Standard 10x20 playfield
* 7 tetrominoes, SRS-like rotation (or explicitly defined rotation system)
* Gravity + soft drop + hard drop
* Lock delay (or an explicit simplified rule)
* Line clear + scoring + level speed-up
* Game over rules
* Next piece preview + hold (optional for MVP - decide explicitly)

## Architecture boundary (to keep the prompting system clean)

Split *implementation* into two layers so prompts can target them differently:

1. **Pure core (testable)**
    * board representation
    * piece geometry + rotation
    * collision checks
    * line clear
    * scoring/level
    * RNG / 7-bag
    * step function: `(state, input, dt) -> new_state + events`
2. **Shell (UI/runtime)**
    * event loop
    * keyboard mapping
    * rendering
    * audio (optional)
    * platform packaging

This lets your prompting system prove it can build and test the core deterministically, while UI work is iterative.

## Repo skeleton I'd use for this project

* `prompts/`
    * `protocols/` (plan/execute/review templates)
    * `roles/` (planner, implementer, reviewer)
    * `rubrics/` (what "good" means)
* `eval/`
    * `scenarios/` (feature tasks the agent must complete)
    * `golden/` (expected behaviors or reference outputs)
    * `reports/` (run logs)
* `tetris/`
    * `src/`
    * `tests/`
    * `docs/` (game rules chosen; rotation system; input mapping)
* `AGENTS.md` (agent operating constraints + discovery steps)
* `DECISIONS/` (ADRs: rotation rules, lock delay, RNG, etc.)

## Immediate next step (no questions needed)

Create a single "North Star" spec artifact for the agent to obey:

**`tetris/docs/GAME_RULES.md`**

* field size
* coordinate system
* spawn positions
* rotation system definition
* gravity model
* lock/clear timing rules
* scoring table
* RNG method (7-bag)
* input mapping
* what's explicitly *out of scope* for MVP

Once that exists, your prompting system can be evaluated on whether it implements *that* spec, not "generic Tetris".

If you want, paste your current `AGENTS.md` (or tell me you don't have one yet) and I'll produce a **paired** starting set:

* `AGENTS.md` tailored for this single-agent environment,
* plus `REVIEW.md` that defines the acceptance gates for each evolution step.
