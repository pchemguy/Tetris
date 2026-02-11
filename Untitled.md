## IMPORTANT Convention for Documentation References

This repository adopts the following convention related to Markdown documentation. Only `AGENTS.md`, `PROJECT.md`, and `README.md` are located in the root of project/repository. Other Markdown files referenced by name only (including this `AGENTS.md`) are located either within `docs/` (directly or its subdirectory) or in the same directory as the referring file. Documents within `docs/` are organized hierarchically using meaningful directory structure, which is described in `PROJECT.md`. You must consult with


## Mandatory Project Discovery Protocol

Before writing, modifying, or deleting **any** files, the agent must:

1. Read and operationalize the following files and all files they reference:
    - `AGENTS.md` (this file)
    - `PROJECT.md`
    - `README.md`
2. Discover available agent skills:
    - Enumerate `.agent/skills/`.
    - Analyze all discovered skills.
    - For each skill, perform baseline diagnostics to:
        - verify the skill is well-defined and usable,
        - identify and report ambiguities or inconsistencies,
        - abort execution on critical errors (e.g. malformed skills, missing required references).

If any required files are missing or inaccessible, the agent must immediately stop and output:

```
BLOCKED
Missing or inaccessible artifacts:

* <list of files>
```

No further reasoning or action is permitted after this output.

---

## Non-normative “Ideas” (hard rules)

The directory:

```
docs/ideas/
```

contains **non-normative, speculative documents**. These documents have **zero authority** and exist only to preserve future possibilities or rejected options.

Agents must obey:

1. **No authority**
    - Nothing in `docs/ideas/` overrides, amends, or supplements any normative document.
2. **No action**
    - Do not implement, partially implement, refactor toward, or prepare code for anything described solely in `docs/ideas/`.
3. **No inference**
    - Do not infer intent, roadmap, priorities, or “next steps” from the existence of ideas.
4. **No scope expansion**
    - Do not use ideas to justify adding features, introducing components, changing tests, or modifying acceptance criteria.
5. **Logging**
    - If an agent reads a document under `docs/ideas/`, it must list it under `artifacts.read` in `IMPLEMENTATION_REPORTS.md` and explicitly state that **no action** was taken based on it.

Allowed uses (strictly limited):

- Read for context only **when explicitly instructed**.
- Help a human rewrite/promote an idea into a **normative** document **when explicitly requested**.

---

## Implementation Reports (MANDATORY)

`IMPLEMENTATION_REPORTS.md` is the **authoritative execution record** of this repository.

Before performing **any non-trivial action**, the agent must:

1. Read `IMPLEMENTATION_REPORTS.md` in full.
2. Determine and explicitly acknowledge:
    - current **repository phase** (`PHASES.md`),
    - current **acceptance gate** (`ACCEPTANCE_GATES.md`),
    - last recorded **status** (`completed`, `blocked`, `failed`, etc.).

---

### Reporting rules (strict)

For each non-trivial unit of work, the agent must append **two entries** to
`IMPLEMENTATION_REPORTS.md`:

1. **Start entry** (before work begins)
    - status: `planned` or `in_progress`
    - records intended phase, target gate, and scope
2. **End entry** (after work ends)
    - status: `completed`, `blocked`, `failed`, or `aborted`
    - records actual outcome, tests executed, and results

Each entry must:

- follow the schema defined in `IMPLEMENTATION_REPORTS.md`,
- truthfully record outcome and next steps,
- list all relevant artifacts read / modified / added / deleted,
- include blockers and assumptions when applicable.

The agent must **not**:

- edit or delete existing report entries,
- create speculative or placeholder entries,
- collapse multiple distinct units of work into one entry.

Failure to read or correctly append to `IMPLEMENTATION_REPORTS.md` is a **protocol violation**.

If a protocol violation is detected mid-run, the agent must stop and output:

```

BLOCKED
Protocol violation:

* <short description>

```

---

### Summary (agent-facing)

> Documentation defines what is allowed.  
> Acceptance gates define what is correct.  
> Phases define when work is allowed.  
> Implementation reports define what actually happened.
```

---

If you want, next we can:

* Update `PROJECT.md` to reference `IMPLEMENTATION_REPORTS.md` instead of `IMPLEMENTATION_LOG.md`
* Update the report schema file itself to reflect the rename cleanly
* Add a Gate 0 check that verifies the file exists and contains valid YAML entries

Let’s keep the authority chain airtight.
