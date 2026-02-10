---
name: AGENTS.md
---

## Mandatory Project Discovery Steps

Before writing, modifying, or deleting **any** files, the agent must:

1. Read and operationalize the following files and all files they reference:
    - `AGENTS.md` (this file)
    - `README.md`
    - `PROJECT.md`
2. Discover available agent skills:
    - Enumerate `.agent/skills/`.
    - Analyze all discovered skills.
    - For each skill, perform baseline diagnostics to:
        - verify the skill is well-defined and usable,
        - identify and report ambiguities or inconsistencies,
        - abort execution on critical errors (e.g. malformed skills, missing required references).

**IMPORTANT**: Ideas are non-normative and inert; agents must not implement, infer intent from, or act on anything in `docs/ideas/`.

If any required files are missing or inaccessible, the agent must immediately stop and output:

```
BLOCKED
Missing or inaccessible artifacts:

* <list of files>
```

No further reasoning or action is permitted after this output.

---

## Implementation Reports (MANDATORY)

`IMPLEMENTATION_REPORTS.md` is the **authoritative execution state** of this repository.

Before performing **any non-trivial action**, the agent must:

1. Read `IMPLEMENTATION_REPORTS.md` in full.
2. Determine and explicitly acknowledge:
    - current **repository phase**,
    - current **acceptance gate** (if any),
    - last recorded **status** (`completed`, `blocked`, etc.).

---

### Reporting rules

3. The agent must append **exactly one new entry** to `IMPLEMENTATION_REPORTS.md`:
    - **before** starting a unit of work *only if* recording intent was explicitly requested, **or**
    - **after** completing, blocking, aborting, or refusing the unit of work.
4. Each entry must:
    - follow the schema defined in `IMPLEMENTATION_REPORTS.md`,
    - truthfully record:
        - success,
        - partial completion,
        - blockage,
        - failure,
        - or refusal to proceed,
    - list all relevant artifacts read and modified.
5. The agent must **not**:
    - edit or delete existing log entries,
    - create speculative or placeholder entries,
    - create multiple entries for the same unit of work unless explicitly instructed.

Failure to read or correctly append to `IMPLEMENTATION_REPORTS.md` is a **protocol violation**.

---

Below is a **drop-in clause** you can paste directly into **`AGENTS.md`**.
It is written to be **unambiguous, enforceable, and agent-safe**, and it fits cleanly with your existing discovery + implementation-log protocol.

---

## Treatment of Non-Normative “Ideas” Documents

### Scope

The directory:

```
docs/ideas/
```

contains **non-normative, speculative documents**.

These documents exist solely to record **future possibilities, rejected options, or exploratory thoughts**.
They do **not** define requirements, constraints, or permissions.

---

### Mandatory agent rules

Agents **must** obey the following rules when encountering `docs/ideas/`:

1. **No authority**
    * Documents under `docs/ideas/` have **zero normative authority**.
    * They do not override, amend, or supplement any specification, gate, or phase.
2. **No action**
    * Agents must **not implement**, partially implement, or prepare code for anything described solely in `docs/ideas/`.
    * Agents must **not treat ideas as backlog, TODOs, or implied future work**.
3. **No inference**
    * Agents must **not infer intent, roadmap, or priorities** from the presence of an idea.
    * The existence of an idea does **not** imply that it will ever be implemented.
4. **No scope expansion**
    * Ideas must **never** be used to justify:
         * expanding scope,
         * adding features,
         * refactoring existing components,
         * introducing new components,
         * modifying tests or acceptance criteria.
5. **Logging requirement**
    * If an agent reads or references a document in `docs/ideas/`, it must:
         * explicitly list it under `artifacts.read` in `IMPLEMENTATION_REPORTS.md`,
         * state that no action was taken based on it.

---

### Allowed uses (strictly limited)

Agents **may**:

* Read ideas for **context only**, when explicitly instructed.
* Cite ideas in discussion or analysis **without acting on them**.
* Assist a human in **rewriting or promoting** an idea into a normative document *only when explicitly requested*.

---

### Disallowed phrasing (hard rule)

Agents must **never** use phrases such as:

* “planned feature”
* “future requirement”
* “will be implemented later”
* “next step according to ideas”

Unless a **normative document explicitly says so**.

---

### Violation severity

Any of the following constitutes a **protocol violation**:

* Implementing behavior described only in `docs/ideas/`
* Treating an idea as a requirement or TODO
* Using ideas to justify scope expansion
* Failing to log idea access when relevant

Protocol violations must result in **immediate halt** and a `BLOCKED` status.

---

### Summary (agent-facing)

> **Ideas are inert.
> They inform humans, not agents.
> Nothing happens unless a spec changes.**

---
