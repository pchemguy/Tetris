# Documentation Infrastructure System (Normative)

## 1. Overview

This repository treats documentation as a first-class subsystem. The documentation base is designed to be readable by humans, executable by agents, and auditable by tooling. This document defines the repository's documentation _infrastructure_: the rules that make the rest of the documentation coherent, discoverable, and enforceable. It governs how documents are identified, how their authority is interpreted, how conflicts are resolved, and how an agent is expected to discover and consume them.

## 2. The core problem this system solves

Without explicit structure, documentation drifts into a pile of partially overlapping notes where authority is unclear, references break when files move, and agents "fill in gaps" with invented behavior. In a normal software project, humans patch this through experience and informal norms. In an agent-evaluated project, that approach fails. The system must be explicit.

This repository's documentation system therefore enforces three invariants:

First, **identity is stable**. A document is identified by its `doc_id`, not by its filename or directory. Files may move; identities must not.

Second, **authority is explicit**. Documents declare whether they are normative or non-normative, and the system defines how conflicts are resolved.

Third, **discovery is total**. An agent cannot operate safely if it reads only “the most obvious doc” or stops at a single index. The system defines what it means to discover the documentation base and requires agents to do so deterministically.

## 3. Layers are a meaning model, not a folder structure

The documentation base is organized into conceptual layers, L0 through L5. These layers are not a development sequence and they are not an “import graph” like code modules. They are a semantic model that separates concerns so that (a) higher-level contracts constrain lower-level artifacts, and (b) lower-level evidence can be interpreted against higher-level intent without circularity.

The essential idea is simple: higher layers define **validity conditions** for lower layers. Lower layers produce **evidence** that those validity conditions are or are not being met.

This creates two opposed flows.

There is a _constraint flow_ from L0 down to L5: rules about documentation constrain governance; governance constrains what may be attempted; architecture constrains what exists; specs constrain behavior; oracles constrain what counts as proof; reports record what actually occurred.

There is also a _diagnosis flow_ from L5 up to L0: reports are meaningless without the oracles that interpret them; oracles exist to evaluate specs; repeated failure against a spec may force reconsideration of structural assumptions; and governance determines when such reconsideration is permitted.

This bidirectional relationship is why the layer model matters: it prevents the common failure mode where tests start defining behavior, or a report starts acting like a spec, or an “idea” becomes an implicit requirement.

## 4. How layer membership is determined

Layer membership is determined by YAML metadata, not by path. Folder organization is helpful for humans, but it is not authoritative and it should not be used as a substitute for metadata discipline.

A document’s `kind` field is the canonical classifier. The mapping from `kind` to layer is fixed and normative. It exists so that both humans and tooling can reason about cross-layer coupling without “guessing based on filenames”.

| `kind`         | Layer interpretation                    |
| -------------- | --------------------------------------- |
| `meta`, `map`  | L0 (documentation infrastructure)       |
| `control`      | L1 (governance)                         |
| `architecture` | L2 (system structure)                   |
| `spec`, `api`  | L3 (behavior contracts)                 |
| `oracle`       | L4 (proof obligations)                  |
| `report`       | L5 (execution state)                    |
| `idea`         | outside L0–L5; explicitly non-normative |

This mapping is not “for convenience”; it is the basis for authority resolution and for diagnostics around suspicious reference patterns (for example, a spec that depends on a report is almost always a conceptual error).

## 5. Authority and conflict resolution

A documentation system is only as strong as its conflict resolution rules. This repository uses a strict precedence model.

When two documents conflict, the system resolves conflicts in the following order:

1. **Authority wins first**. A normative document overrides a non-normative one. Non-normative text is never allowed to “silently become binding” through implication or repetition.
    
2. **Supersession wins second**. If a document declares that it supersedes another (or is superseded by another), that relationship is decisive.
    
3. **Layer precedence wins third**. Higher layers define validity conditions for lower layers. When there is unresolved conflict after authority and supersession, the higher layer’s terms govern. This is not “because the higher layer is wiser”; it is because a lower layer cannot redefine the validity terms that constrain it without breaking the system.
    

This model prevents a very specific failure: turning the repository into a situation where test code or a report can “outvote” a spec, or where an implementation detail can “outvote” the decomposition boundaries.

## 6. Identity, naming, and references

Every participating document carries YAML front matter that conforms to `DOC_SCHEMA.json` (the machine schema) and is described in `DOC_SCHEMA.md` (the human contract). The YAML header is the authoritative metadata record for that document.

The `doc_id` is the stable identity. Filenames exist for human navigation; they are not authoritative identifiers. Moving or renaming a file must not require changing `doc_id`. Conversely, changing a `doc_id` is treated as an identity change and must be modeled as deprecation + supersession, not as “just a rename”.

Within prose, the system allows a convenience marker for references: `@DOC_ID`. This marker is deliberately easy to extract with simple tooling and is meant to reduce “wrong file resolution” errors when agents operate across directories. The marker is not authoritative; it is a convenience overlay on top of the YAML-defined inventory. Tooling may extract `@DOC_ID` tokens outside fenced code blocks and validate them against the set of declared YAML `doc_id` values.

The system therefore distinguishes between two things:

- YAML references are authoritative declarations of dependency.
    
- `@DOC_ID` is a convenience signal in prose.
    

The combination is intentional: YAML gives structure; prose gives readability; `@DOC_ID` reduces ambiguity without turning the body text into a machine format.

## 7. Discovery and reading obligations

Agents are not allowed to “sample” the documentation base. They must either discover it fully or stop.

Discovery is defined as acquiring a complete set of normative documents sufficient to determine (a) what is allowed right now, (b) what behavior is defined, and (c) what evidence is required to claim success. In practice, this means that an agent must obtain all normative documents reachable through the reference graph from the composition roots, and it must do so recursively.

To make this deterministic and not dependent on clever graph traversal, the repository also defines a machine inventory artifact: `DOC_INVENTORY.json`. This file exists to provide direct access to the full document set and their metadata without requiring reference traversal first. It functions as a “catalog”, not as an authority source. If inventory and YAML headers disagree, the YAML headers are authoritative and the inventory is considered stale or incorrect.

The intended operational contract is: use `DOC_INVENTORY.json` for discovery efficiency, then read documents as required by the current task and by the recursive reference obligations.

## 8. Where the layer entry documents fit

This file defines the layer model and the rules of the infrastructure. The per-layer entry documents exist to keep this file from turning into a directory listing while still giving humans and agents a structured way to orient inside a layer.

Each layer entry document is expected to do two things well: (1) define the purpose and invariants of that layer in prose, and (2) provide a curated index of documents in that layer (with paths) so that navigation is practical.

This split is deliberate. A composition root should not become a pile of tables; but the system still needs navigable indexes. The entry docs are where indexes belong.

## 9. Non-normative ideas are inert by default

The repository supports non-normative “idea” documents, typically under `docs/ideas/`. Their role is to preserve possibilities and rejected options without exerting any authority. Ideas are not requirements. They do not imply roadmap. They are inert unless explicitly promoted into normative documents through the governance process.

This is a hard boundary: agents may not implement behavior described only in ideas.

## 10. What to read next

To understand how to operate inside this system, read the layer entry documents in order:

- `L0_DOCUMENTATION.md` for tooling and metadata rules,
    
- `L1_GOVERNANCE.md` for when work is allowed and how it’s evaluated,
    
- `L2_STRUCTURE.md` for what exists and how boundaries are defined,
    
- `L3_SPECS.md` for behavior contracts,
    
- `L4_ORACLES.md` for proof obligations,
    
- `L5_REPORTS.md` for execution state and resumption rules.
    

---

If you want, I can now rewrite `L0_DOCUMENTATION.md` … `L5_REPORTS.md` in the same narrative style (each with a small, non-dominant index section), so the whole system reads like a coherent book rather than a checklist.


| Layer | Responsibility                         | Top Layer Directory  | Main Entry            | `kind`         |
| ----- | -------------------------------------- | -------------------- | --------------------- | -------------- |
| L0    | Documentation infrastructure           | `docs/meta/`         | `L0_DOCUMENTATION.md` | `meta`         |
| L1    | Governance (process control)           | `docs/control/`      | `L1_GOVERNANCE.md`    | `control`      |
| L2    | System structure (global contracts)    | `docs/architecture/` | `L2_STRUCTURE.md`     | `architecture` |
| L3    | Behavioral specs (component contracts) | `docs/specs/`        | `L3_BEHAVIOR.md`      | `spec`, `api`  |
| L4    | Testing (proof obligations)            | `docs/testing/`      | `L4_TESTING.md`       | `testing`      |
| L5    | Execution state (reports)              | `docs/reports/`      | `L5_REPORTS.md`       | `report`       |
| OUT   |                                        | `docs/ideas/`        | -                     | `idea`         |
