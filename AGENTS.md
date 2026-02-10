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

If any required files are missing or inaccessible, the agent must immediately stop and output:

```
BLOCKED
Missing or inaccessible artifacts:

* <list of files>
```

No further reasoning or action is permitted after this output.

---

## Implementation Reports (MANDATORY)

`reports/IMPLEMENTATION_REPORTS.md` is the **authoritative execution state** of this repository.

Before performing **any non-trivial action**, the agent must:

1. Read `IMPLEMENTATION_REPORTS.md` in full.
2. Determine and explicitly acknowledge:
    - current **repository phase**,
    - current **acceptance gate** (if any),
    - last recorded **status** (`completed`, `blocked`, etc.).

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
