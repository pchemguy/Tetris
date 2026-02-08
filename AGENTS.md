---
name: AGENTS.md
---

## Mandatory Project Discovery Steps

Before writing, modifying, or deleting **any** files, the agent must:

1. Read and operationalize the following files and all referenced files:
    - `AGENTS.md` (this file)
    - `README.md`
    - `PROJECT.md`
2. Discover available skills:
    - Enumerate `.agent/skills/`.
    - Analyze all discovered skills.
      For each skill, perform baseline diagnostics to:
          - verify the skill is well-defined and usable,
          - identify and report ambiguities or inconsistencies,
          - abort execution on critical errors (e.g., malformed skills, missing required references), and provide detailed diagnostics.

**If any required files are missing or inaccessible**, the agent must immediately stop further processing and output:


```
BLOCKED
Missing or inaccessible artifacts:

* <list of files>
```

## Implementation Log

1. Read `IMPLEMENTATION_LOG.md` before starting work
2. Determine:
    * current **phase**
    * current **gate**
    * last known **status**
3. Append a new entry **before and after** any non-trivial work
4. Explicitly record:
    * success,
    * partial completion,
    * blockage,
    * or refusal to proceed

Failure to read and update this document is a **protocol violation**.
