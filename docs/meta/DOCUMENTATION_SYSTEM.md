---
doc_id: DOCUMENTATION_SYSTEM
name: DOCUMENTATION_SYSTEM.md
title: Documentation Infrastructure System
kind: meta
scope: global
status: active
authority: normative
gate_applies_to: all
phase_applies_to: all
description: Defines the structure, authority rules, and roles of the repository's documentation infrastructure.
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

# Documentation Infrastructure System (Normative)

## 1. Overview

Documentation is an essential first-class subsystem of any technical project (not just coding. This project attempts to adapt a number of software engineering concepts and apply them to this documentation system. The documentation base adopts hierarchical layered structure. At its top are the most abstract system-wide documents (meta documents) that establish structure, organization, and conventions employed by the documentation system itself. The lower level documents become progressively more specific and focused, gradually developing foundation established by higher level documents. This documentation system also attempts do develop modular focused (single responsibility) documents with weak well-defined couplings (more specific/focused documents reference more general/abstract documents, on which the former are based, not the other way around or "spurious" references).

Whenever practical:

- Refactor documents to minimize repetition (DRY) and circular references.
- Develop conventions that can be readily
    - Encoded as machine readable structured artifacts (such as, JSON and YAML documents).
    - Accompanied by machine readable validation artifacts (such as, JSON schema).
- Describe each important non-Markdown artifact, such as document metadata validation schema, in a Markdown document having identical name part of filename, so that purpose/meaning/organization of the artifact could be easily discovered. Then reference this artifact descriptor where relevant (this is preferable to having back references within the artifact descriptor, as it will likely create increase document couplings and created circular references).
  
  For example, the documentation prescribes that each document should include a `YAML` metadata described in `DOC_SCHEMA.md` and validated by accompanied `DOC_SCHEMA.json`. `DOC_SCHEMA.md` should
    - provide context/motivation,
    - describe the metadata,
    - indicate that `DOC_SCHEMA.json` should be used for validating metadata,
    - possibly suggest how this metadata might be used, while avoiding **prescribing** or **referencing** any such use.
  
  Then more general documents may reference `DOC_SCHEMA.md`. For example, `DOC_INVENTORY.json` and `DOC_INVENTORY.schema.json` are concerned about providing a machine readable document index as described in associated `DOC_INVENTORY.md`. While `DOC_INVENTORY.json` might include not just paths, but also `YAML` metadata from individual documents, providing essentially a metadata cache, specific metadata format in individual documents is clearly out of scope for `DOC_INVENTORY.json`. Therefore, `DOC_INVENTORY.md` must only define explicitly only metadata related to repository discovery (such as file paths/names), while referencing `DOC_SCHEMA.md` for other metadata. Similarly, file location / index is clearly out of scope for `DOC_SCHEMA.md`, which is concerned about document's metadata irrespective of document's location. Hence, the two artifacts should not be collapsed. 

---

## 2. Naming conventions, metadata, and cross-document references

This repository adopts the following document naming convention:

- capital English letters, possibly numbers, and underscores,
- at least two characters with first being a letter (`^[A-Z][A-Z0-9_]+$`),
- all document names within the repository should have unique filename regardless of location.

Every document should include a `YAML` frontmatter header defined in `DOC_SCHEMA.md`. This header should declare a stable identifier (`doc_id`). Documents may reference one another in prose using `@DOC_ID` markers (for example, `@DOC_SCHEMA`) as a convenience mechanism. Documents may still reference other documents within the same directory using filenames. The primary motivation for introducing `@DOC_ID` references is to reduce the chances of agents resolving document references to documents not within the same directory incorrectly (such as potentially creating new empty file locally or substituting a similar name). YAML metadata remains authoritative, and `@DOC_ID` markers are validated against the repository’s declared identifiers. Tooling may use YAML metadata and `@DOC_ID` markers to validate references and construct a deterministic documentation graph.

---

## 3. Layered organization

The repository documentation system is organized into conceptual layers **L0–L5**. The normative definition of the layering model (meaning, constraint/validity vs diagnosis flows, meta-layer positioning, conflict resolution, and the layer index) is specified in `DOC_LAYERS.md`. Tooling uses this layer model to classify documents deterministically (via `kind`) and to support diagnostic validation of cross-layer semantic coupling.

