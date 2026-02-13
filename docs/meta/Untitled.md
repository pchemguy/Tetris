-

## Add to DOC_GRAPH_SPEC.md: Doc Inventory Artifact

### 9.x Machine-readable documentation inventory (required)

Tooling MUST be able to produce a machine-readable inventory artifact that captures the repository’s documentation graph inputs (doc nodes) in a deterministic form.

This inventory is the canonical target for “project discovery” calls in Gate 0 and agent workflows. Human-readable indices (e.g. `DOCUMENTATION_SYSTEM.md`) may exist, but they MUST NOT be required for discovery.

#### 9.x.1 Output: `DOC_INVENTORY.json`

Default location: `docs/meta/DOC_INVENTORY.json` (path may differ; the filename is normative).

The file MUST be valid JSON and MUST match the schema in `DOC_INVENTORY.schema.json`.

#### 9.x.2 Inventory content model

`DOC_INVENTORY.json` MUST contain:

* repository metadata (for determinism + provenance),
* a list of documents (one entry per participating artifact),
* derived fields needed by tooling (especially `layer`).

##### Top-level shape

```json
{
  "format": "DOC_INVENTORY",
  "version": 1,
  "generated_at": "2026-02-13T12:34:56Z",
  "repo": {
    "doc_system_doc_id": "DOCUMENTATION_SYSTEM",
    "root": "."
  },
  "docs": [ /* sorted list */ ]
}
```

Notes:

* `generated_at` is informational. It MUST NOT affect sorting or validation.
* `repo.root` is informational; tools MUST NOT assume it exists.

##### Document entry shape

Each entry in `docs[]` MUST include:

```json
{
  "doc_id": "DOC_SCHEMA",
  "name": "DOC_SCHEMA.md",
  "path": "docs/meta/DOC_SCHEMA.md",
  "kind": "meta",
  "layer": "L0",
  "scope": "global",
  "status": "active",
  "authority": "normative",
  "gate_applies_to": "all",
  "phase_applies_to": "all",

  "description": "…",               // optional
  "url": "https://…",               // optional
  "urls": ["https://…", "..."],     // optional (only when needed)

  "references": ["COMPONENT_REGISTRY"],  // optional: omitted if empty
  "supersedes": ["OLD_DOC"],             // optional: omitted if empty
  "superseded_by": "NEW_DOC"             // optional: omitted if null/absent
}
```

Normative rules:

1. `doc_id`, `name`, `path`, `kind`, `layer`, `scope`, `status`, `authority`, `gate_applies_to`, `phase_applies_to` are REQUIRED.
2. `references`, `supersedes` MUST be **omitted** if empty (not present as `[]`).
3. `superseded_by` MUST be **omitted** if not present / not applicable (not present as `null`).
4. `url` MUST be **omitted** if not present. It MUST NOT be `null` or empty string.
5. `urls` MUST be **omitted** unless it is present and non-empty.
6. A doc MUST NOT contain both `url` and `urls`.

(These rules match your “present or absent” preference and keep the inventory clean.)

#### 9.x.3 Source of truth and derivation rules

* For Markdown docs: all fields except `path` and `layer` are derived from YAML front matter.
* `path` is derived from filesystem location at generation time.
* `layer` is derived from `kind` using the canonical mapping in this spec.
* For JSON artifacts that participate (e.g., registries/schemas): the tool MAY include them as docs with synthetic entries, but the same required fields still apply.

#### 9.x.4 Determinism requirements

To ensure stable diffs and stable agent behavior:

* `docs[]` MUST be sorted by `doc_id` ascending (lexicographic).
* Within a doc entry, arrays MUST be sorted ascending (`references`, `supersedes`, `urls`).
* Tools MUST NOT emit duplicate doc entries.
* Tools MUST NOT emit duplicate values inside arrays.

#### 9.x.5 Relationship to discovery and Gate 0

* Gate 0 and agent discovery MUST refer to `DOC_INVENTORY.json` as the canonical “what documents exist” index.
* Human-readable indices (e.g., `DOCUMENTATION_SYSTEM.md`) MUST NOT be required to enumerate all documents; they may summarize or explain, but discovery MUST be possible without them.

---
