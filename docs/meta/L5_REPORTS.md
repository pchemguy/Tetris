---
doc_id: L5_REPORTS
name: L5_REPORTS.md
title: L5 — Execution State (Reports)
kind: report
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines execution state artifacts, including append-only implementation reports and evaluation logs.
references:
  - IMPLEMENTATION_REPORTS
---

# L5 — Execution State

## Document Index

**Directory**: `docs/reports/`

| Title                  | Filename                    | Function / Role                                                       |
| ---------------------- | --------------------------- | --------------------------------------------------------------------- |
| Implementation Reports | `IMPLEMENTATION_REPORTS.md` | Append-only execution record of phase/gate progress and agent actions |

## Detailed description

These documents record the **actual execution history** of agentic development. Unlike specifications or gates (which define what is allowed or correct), these documents

- define **state**, not policy,
- are **authoritative** for “current progress”,
- are required reading for any agent resuming work.

### Implementation reports (`IMPLEMENTATION_REPORTS.md`) — *Authoritative execution state*

The implementation log is an **append-only record** of:

- which phases and gates have been attempted,
- what actions were taken,
- what artifacts were modified,
- what passed, failed, or was blocked,
- what the next intended step is.

It answers questions such as:

- *Where did development stop last time?*
- *Which gate was last attempted, and with what outcome?*
- *What assumptions or blockers were discovered?*

All agents must:

- read it before acting,
- append to it after acting,
- never rewrite or delete history.

---
