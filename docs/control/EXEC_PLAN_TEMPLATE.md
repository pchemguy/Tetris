---
doc_id: EXEC_PLAN_TEMPLATE
name: EXEC_PLAN_TEMPLATE.md
title: Execution Plan — {Short Action-Oriented Description}
status: draft
authority: non_normative
references: [WORKFLOW, TEST_PLAN, ACCEPTANCE_GATES, PHASES]
---

# Execution Plan — {Short Description}

This document is an L1 orchestration artifact.

It governs the execution of a specific gate within the constraints of:

- normative specifications (L2/L3),
- test oracles (L4),
- repository workflow (WORKFLOW.md),
- and acceptance gates (ACCEPTANCE_GATES.md).

This document is not normative.  
It does not redefine behavior.  
If normative behavior must change, documentation must be updated first.

---

# 1. Target

## Target Phase

`{Phase number and justification}`

## Target Gate

`{Gate number and description}`

This ExecPlan must not implement behavior beyond this gate.

---

# 2. Normative Closure

List the exact DOC_IDs that form the normative closure for this gate.

Include:

- Core specs (L3)
- Relevant architecture contracts (L2)
- Oracle documents (L4)
- Test governance docs (if applicable)

Example:

- `@GAME_RULES`
- `@GAME_STATE`
- `@CORE_API`
- `@CORE_ORACLE_INDEX`
- `@ORACLE_CORE`
- `@ORACLE_CORE_GRAVITY_AND_LOCKING`
- `@ORACLE_CORE_INVARIANTS`

No other documents are authoritative for this plan.

If additional documents become necessary, this section must be updated.

---

# 3. Required Test Suites

From TEST_PLAN.md:

- {Suite name}
- {Suite name}

No additional suites may be used to justify gate completion.

---

# 4. Implementation Boundaries

The following are explicitly allowed:

- {List constrained changes}

The following are explicitly forbidden:

- Changing normative documentation.
- Modifying behavior from future gates.
- Introducing speculative features.
- Weakening oracles.

All code changes must remain within architectural boundaries defined in L2.

---

# 5. Execution Narrative

Describe the implementation sequence in prose. 

This must:

- Explain why each change is necessary.
- Name files by full repository-relative path.
- Describe observable effects.
- Avoid redefining specification content.
- Avoid embedding duplicated spec text.

Do not describe behavior that is not defined in normative specs.

---

# 6. Milestones

Each milestone must be independently verifiable and mapped to required suites.

For each milestone:

- Describe the incremental capability added.
- State which suite(s) should pass after completion.
- State observable acceptance behavior.

Milestones must not cross gate boundaries.

---

# 7. Progress

This section must always reflect actual state.

- [ ] Inventory built and validated
- [ ] Normative closure computed
- [ ] Code changes implemented
- [ ] Oracle translations complete
- [ ] Required suites pass
- [ ] Implementation report appended

Timestamps must be included.

---

# 8. Failure Classification

Failures encountered during execution must be classified as:

- implementation_defect
- test_encoding_defect
- normative_gap_or_conflict

If classification is normative_gap_or_conflict, execution must stop and escalate.

---

# 9. Decision Log

Record decisions that affect implementation within normative constraints.

Format:

Decision:
Rationale:
Date:

No decision may contradict normative documentation.

---

# 10. Determinism Verification

Describe:

- How RNG is controlled (if applicable)
- How time-based behavior is avoided
- How reproducibility is verified

Determinism violations invalidate this plan.

---

# 11. Escalation Criteria

Escalation is mandatory if:

- A spec ambiguity is discovered.
- Oracles contradict spec.
- Required behavior is undefined.
- Gate cannot be satisfied within phase constraints.

Escalation must occur before modifying normative documents.

---

# 12. Completion Criteria

This ExecPlan is complete only when:

- All required suites pass.
- No lower gate regresses.
- Determinism holds.
- An entry is appended to IMPLEMENTATION_REPORTS.md.
- Gate baseline advances.

---

# 13. Outcomes & Retrospective

Summarize:

- What was achieved.
- Whether scope was respected.
- Any spec clarifications required.
- Lessons for future plans.

---

# 14. Archive Policy

After completion:

- status must be updated to `completed`.
- This plan becomes immutable historical record.
- It must remain reproducible using only its contents and the repository state at completion.
