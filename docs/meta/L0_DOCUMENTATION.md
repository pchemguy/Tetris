---
doc_id: L0_DOCUMENTATION
name: L0_DOCUMENTATION.md
title: L0 — Documentation Infrastructure (Meta-layer)
status: active
authority: normative
description: Defines the documentation infrastructure, metadata rules, graph model, inventory, and cross-layer validation policy.
references:
  - DOCUMENTATION_SYSTEM
  - DOC_SCHEMA
  - DOC_GRAPH_SPEC
  - DOC_INVENTORY
  - CROSS_LAYER_DEPENDENCY
---

# L0 — Documentation Infrastructure

## Position of meta-layer

The L0 layer serves two distinct roles:

1. **Enablement and validation**
   It provides the mechanism that makes the documentation system machine-checkable: stable identifiers, scope inventory, graph extraction, and validation rules. L0 is logically prior (tooling depends on it), but it is semantically external to L2–L4. Development layers do not depend on L0 for meaning.
2. **System integration surface**
   The main documentation document, `DOCUMENTATION_SYSTEM.md`, integrates and explains the documentation base as a whole, including L0 itself.

Consequences:

* L0 artifacts are required for enforcement and automation.
* A human can understand L2–L4 without knowing L0 exists, though it would be more difficult.
* While not strictly required, L0 is even more important for tooling and agents.

Development layers remain **meta-agnostic** by design.

## Document Index

**Directory**: `docs/meta/`

| Title                                               | Filename                            | Function / Role                                                                 |
| --------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------- |
| Documentation Infrastructure System (this file)     | `DOCUMENTATION_SYSTEM.md`           | Defines the documentation infrastructure                                        |
| Documentation Metadata Schema (Spec)                | `DOC_SCHEMA.md`                     | Normative specification of documentation metadata semantics                     |
| Documentation Metadata Schema (JSON)                | `DOC_SCHEMA.json`                   | Machine-validated schema for YAML front matter in Markdown docs                 |
| Documentation Graph Specification                   | `DOC_GRAPH_SPEC.md`                 | Rules for extracting and rendering documentation dependency graphs              |
| Documentation Inventory (Spec)                      | `DOC_INVENTORY.md`                  | Defines the machine-readable inventory artifact and required invariants         |
| Documentation Inventory                             | `DOC_INVENTORY.json`                | Generated machine inventory (tool output / discovery input)                     |
| Documentation Inventory (Schema)                    | `DOC_INVENTORY.schema.json`         | JSON Schema validating `DOC_INVENTORY.json`                                     |
| Cross-Layer YAML Reference Dependency Policy (Spec) | `CROSS_LAYER_DEPENDENCY.md`         | Normative rationale/interpretation for diagnostic cross-layer YAML dependencies |
| YAML Reference Policy                               | `YAML_REFERENCE_POLICY.json`        | Machine-readable cross-layer validation policy (diagnostic by default)          |
| YAML Reference Policy (Schema)                      | `YAML_REFERENCE_POLICY.schema.json` | JSON Schema validating `YAML_REFERENCE_POLICY.json`                             |
| Documentation Authority Map                         | `DOCS_AUTHORITY_MAP.md`             | Hierarchy and conflict-resolution rules among normative documents               |

