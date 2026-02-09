---
name: SKILL_DEV_PROMPT_TEMPLATE.md
description: Prompt template for interactive specification of agent skills used in skill-based, single-agent software development workflows that emulate multi-agent architectures.
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/698975ae-3688-8397-92a7-8c7fbe698b2e
---

# SKILL DEVELOPMENT PROMPT TEMPLATE

## PURPOSE

This prompt is used to **interactively design and refine an agent skill specification**.

A *skill* represents a reusable, role-focused capability that the controller agent can invoke during a structured development workflow. The goal of this
interaction is to produce a **clear, robust, and reusable skill specification** that can later be instantiated using a concrete skill template.

This prompt **does not implement the skill**. It defines the skill's contract, scope, assumptions, and constraints.

---

## TASK

You are assisting with the **development of a single agent skill specification**.

I will provide **preliminary notes** describing the intended role, scope, and motivations for the skill. These notes may be incomplete, informal, or partially ambiguous.

### Your immediate objectives are to:

1. **Extract and clarify intent**
    - Identify the core responsibility of the skill
    - Distinguish essential behavior from optional or future extensions
2. **Forge a precise skill specification**
    - Define the role the agent assumes when this skill is active
    - Specify inputs, outputs, and expected artifacts
    - Define boundaries: what the skill must do, may do, and must not do
3. **Align the skill with the overall workflow philosophy**
    - Single-agent execution
    - Skill-based role modulation
    - Project-agnostic orchestration
4. **Prepare the skill for later templating**
    - Ensure the specification is concrete enough to be converted into a formal skill definition
    - Avoid project-specific assumptions unless explicitly justified

This is an **interactive refinement step**. If ambiguities or design tradeoffs are discovered, surface them explicitly and propose resolution options.

---

## FRAMEWORK CONTEXT (READ CAREFULLY)

### Skill-Based Single-Agent Architecture

This project uses a **skill-based single-agent model** to emulate a multi-agent development environment.

- In a traditional multi-agent setup:
    - A controller agent delegates work to specialized task agents
    - Each task agent operates in an isolated context
    - Communication occurs via structured handoffs
- In this project:
    - There is **one agent**
    - Specialized task agents are replaced with **skills**
    - Skills modulate the agent's role, focus, and constraints without creating isolated contexts

The controller logic references **skills**, not agents.

---

### Workflow Characteristics

- Development workflows are:
    - Explicitly staged
    - Deterministic
    - Star-shaped (hub-and-spoke)
- Direct interaction between tasks/skills is discouraged.
- Information is passed **only via persisted artifacts** in the project directory or repository.

The workflow itself is **project-agnostic**.

All project-specific knowledge must be sourced from:

- `PROJECT.md`
- Files explicitly referenced from it

Swapping `PROJECT.md` should be sufficient to reuse the workflow for a different project.

---

### Assumptions About Agent State

When a skill is invoked, the agent may assume:

- `AGENTS.md` has already been read and operationalized
- Initial project discovery has been performed
- The repository is available as the sole source of truth

A skill **may request limited rediscovery**, but only as required for its role.

---

## SKILL DESIGN PRINCIPLES

When developing the skill specification, adhere to the following:

- **Role clarity**
    - The skill represents a *developer role*, not a concrete task script
- **Minimal coupling**
    - Skills should not depend on internal behavior of other skills
    - Any coordination occurs via files and workflow structure
- **Project agnosticism**
    - No hardcoded assumptions about languages, frameworks, or domains
    - If specialization is required, it must be parameterized or explicitly scoped
- **Non-overreach**
    - The skill must not perform orchestration, planning beyond its scope, or decision-making assigned to the controller

---

## SKILL ROLE AND CONTEXT (INPUT)

Below is the initial description of the skill role to be developed. Treat this as a **starting point**, not a finished specification.

```
{SKILL ROLE AND CONTEXT}
```

---

## EXPECTED OUTPUT (THIS STEP)

Produce a **well-structured draft skill specification**, including at minimum:

- Skill purpose and intent
- Role assumptions and responsibilities
- Inputs (files, artifacts, discovery steps)
- Outputs (files, decisions, reports)
- Explicit non-goals and prohibitions
- Open questions or design risks (if any)

Do **not** implement the skill yet.

---
