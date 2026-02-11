---
name: AGENTS.md
---

## IMPORTANT - Documentation Reference Convention

Only the following Markdown files reside at repository root:

- `AGENTS.md`
- `PROJECT.md`
- `README.md`

All other Markdown documents referenced by filename only (e.g., `IMPLEMENTATION_REPORTS.md`, `PHASES.md`, `ACCEPTANCE_GATES.md`) are located:

- under `docs/` (directly or within its subdirectories), or
- in the same directory as the referring document.

Agents must consult the "`docs/` structure" section of `PROJECT.md` to resolve document paths correctly.

If a referenced document cannot be resolved deterministically, the agent must halt with:

```
BLOCKED  
Unresolved documentation reference: <filename>
```

Failure to resolve documentation location correctly is a protocol failure.

---

## Mandatory Project Discovery Protocol

Before writing, modifying, or deleting **any files**, the agent must:

1. Read and operationalize:
    - `AGENTS.md`
    - `PROJECT.md`
    - `README.md`
2. Resolve and read all documents referenced by those files.
3. Discover available agent skills:
    - Enumerate `.agent/skills/`.
    - Analyze all discovered skills.
    - For each skill:
        - verify it is well-defined and usable,
        - identify ambiguities or inconsistencies,
        - abort execution on critical errors (e.g., malformed skills, missing required references).

If any required files are missing, inaccessible, or unresolved, the agent must immediately stop and output:

```

BLOCKED
Missing or inaccessible artifacts:

* <list of files>

```

No further reasoning or action is permitted after this output.

---

## Non-normative "Ideas" (Hard Rules)

The directory:

```

docs/ideas/

```

contains **non-normative, speculative documents**. These documents have **zero authority** and exist only to preserve future possibilities or rejected options.

Agents must obey:

1. **No authority**
    - Nothing in `docs/ideas/` overrides or supplements any normative document.
2. **No action**
    - Do not implement, partially implement, refactor toward, or prepare code for anything described solely in `docs/ideas/`.
3. **No inference**
    - Do not infer roadmap, intent, priorities, or implied requirements from ideas.
4. **No scope expansion**
    - Do not use ideas to justify adding features, introducing components, modifying tests, or changing acceptance criteria.
5. **Logging requirement**
    - If an idea document is read, it must:
        - be listed under `artifacts.read` in `IMPLEMENTATION_REPORTS.md`,
        - explicitly state that **no action was taken** based on it.

Allowed (strictly limited):

- Read for context only when explicitly instructed.
- Assist in rewriting/promoting an idea into a normative document when explicitly requested.

Violation of any rule in this section is a **protocol failure**.

---

## Implementation Reports (MANDATORY)

`IMPLEMENTATION_REPORTS.md` is the **authoritative execution state** of this repository.

Before performing any **non-trivial action**, the agent must:

1. Confirm `IMPLEMENTATION_REPORTS.md` exists.
2. Read it in full.
3. Determine and explicitly acknowledge:
    - current **repository phase** (`PHASES.md`),
    - current **acceptance gate** (`ACCEPTANCE_GATES.md`),
    - last recorded **status**.

If `IMPLEMENTATION_REPORTS.md` does not exist:

```

BLOCKED
Missing required execution state:

* IMPLEMENTATION_REPORTS.md

```

No action is permitted without execution state.

---

### Reporting Rules (Strict)

For each non-trivial unit of work, the agent must append **two entries** to `IMPLEMENTATION_REPORTS.md`:

1. **Start entry**
    - status: `planned` or `in_progress`
    - records intended phase and target gate
2. **End entry**
    - status: `completed`, `blocked`, `failed`, or `aborted`
    - records actual outcome and test results

Each entry must:

- follow the schema defined in `IMPLEMENTATION_REPORTS.md`,
- list all artifacts read / modified / added / deleted,
- record blockers and assumptions when applicable,
- reflect truthful execution state.

The agent must not:

- edit or delete existing entries,
- create speculative or placeholder entries,
- collapse multiple independent work units into one entry.

Failure to comply is a **protocol violation**.

If a protocol violation is detected mid-run, the agent must stop and output:

```
BLOCKED
Protocol violation:

* <short description>
```

---

## Gate 0 Self-Verification Requirement

Before attempting any gate beyond 0, the agent must confirm:

- All normative documents referenced in `PROJECT.md` are resolved.
- Import boundaries defined in `DECOMPOSITION.md` are understood.
- Applicable test oracle documents are identified.
- Current phase permits the target gate.

Failure to perform this verification is a Gate 0 failure.

---

## Summary (Agent-Facing)

> Documentation defines what is allowed.  
> Acceptance gates define what is correct.  
> Phases define when work is allowed.  
> Implementation reports define what actually happened.  
> Ideas define nothing.
