
# COMPONENT_REGISTRY

**Component Registry (Normative)**

---

## 1. Purpose

`COMPONENT_REGISTRY.json` is the **authoritative inventory of system components**, their **layer classification**, and their **identity within the documentation system**.

It exists to make the system decomposition:

* machine-checkable,
* metadata-driven,
* enforceable by tooling.

Specifically, it enables:

* deterministic generation and validation of `doc_scope` values in `DOC_SCHEMA.json`,
* automated validation of documentation scope tokens,
* mechanical enforcement of architectural layer boundaries (`core`, `shell`, `testing`),
* static import policy validation (when integrated with tooling).

If a component does not exist in `COMPONENT_REGISTRY.json`, it is **not a recognized component** for documentation, dependency, or scope purposes.

Although documentation tooling uses this registry to validate `scope` tokens, the registry is an architectural artifact: it is the authoritative machine-readable representation of the system's component decomposition and permitted component dependencies.

---

## 2. Relationship to other documents

### 2.1 `DECOMPOSITION.md`

* `DECOMPOSITION.md` defines **semantic responsibilities and architectural boundaries**.
* `COMPONENT_REGISTRY.json` defines the **canonical identifiers and layer classification** of those components.

In short:

* Decomposition defines *what a component is*.
* The registry defines *how it is named and classified*.

Decomposition is the semantic contract.
The registry is the canonical naming and classification authority.

---

### 2.2 `DOC_SCHEMA.json`

* `DOC_SCHEMA.json` defines the **metadata schema** embedded in each document.
* The registry defines the **allowed values for `doc_scope`** via `doc_scope_enum`.

There is no regex-based guessing of valid scopes.

`COMPONENT_REGISTRY.json` is the authoritative source for valid scope tokens.

---

### 2.3 Dependency policy

`COMPONENT_REGISTRY.json` may also encode a `dependency_policy` section defining:

* allowed component-level import edges,
* forbidden component-level edges,
* deny-by-default rules.

This makes architectural boundaries auditable at the component level.

---

## 3. Layer model

This repository uses a strict multi-layer architecture:

* **core** — pure deterministic simulation
    * no I/O
    * no timing
    * no environment interaction
* **shell** — orchestration and external interaction
    * runtime
    * rendering
    * presentation
    * input
    * CLI
    * persistence
    * telemetry
* **testing** — test harness and evaluation infrastructure
    * must not be imported by production components

This layer classification is encoded in the registry and must not be inferred heuristically.

---

## 4. Scope token convention

The registry defines a deterministic scope-token format:

```
<layer>:<component_id>
```

Examples:

* `core:core`
* `shell:runtime`
* `shell:renderer`
* `testing:testing`

### Reserved top-level scopes

The following scopes are always valid:

* `global`
* `core`
* `shell`
* `testing`

These represent layer-wide applicability.

---

### Intended usage in document metadata

Layer-wide document:

```yaml
doc_scope: core
```

Component-specific document:

```yaml
doc_scope: shell:runtime
```

All values must exist in `doc_scope_enum`.

---

## 5. `doc_scope_enum` (authoritative list)

`COMPONENT_REGISTRY.json` contains an explicit `doc_scope_enum` array.

This list must include:

* all reserved top-level scopes,
* one token per registered component:
    * `<layer>:<component_id>`

Tooling must treat `doc_scope_enum` as the **source of truth** for valid `doc_scope` values.

Any document whose `doc_scope` is not present in this list is invalid.

---

## 6. Component identity rules

Each component entry in `COMPONENT_REGISTRY.json` must define:

* `component_id` — lowercase snake_case
* `layer` — `core`, `shell`, or `testing`
* `title`
* `description`
* `status` — `active`, `reserved`, or `deprecated`
* `required` — boolean
* `package` — Python import root (or `null` for testing layer)
* `public_api_modules` — explicit list of importable public modules

Testing-layer components:

* must have `package: null`
* must define `source_paths`

---

## 7. Normative procedure: adding a component

Introducing a new component requires **all** of the following steps.

### Step 1 — Update `DECOMPOSITION.md`

* Add the component to the top-level list (if applicable).
* Define responsibilities.
* Define explicit non-responsibilities.
* Define allowed interfaces.

### Step 2 — Update `COMPONENT_REGISTRY.json`

Add a new entry under `components[]` with:

* `component_id`
* `layer`
* `title`
* `description`
* `status`
* `required`
* `package`
* `public_api_modules`

If testing-layer:

* `package` must be `null`
* `source_paths` must be defined

### Step 3 — Update `doc_scope_enum`

Add:

```
<layer>:<component_id>
```

### Step 4 — Update document metadata

All documentation targeting this component must use the new `doc_scope`.

---

### Failure to complete all steps

If a component appears in:

* code,
* documentation,
* dependency policy,

but is not present in `COMPONENT_REGISTRY.json`,

this constitutes a **Gate 0 boundary violation** until resolved.

---

## 8. Reserved vs active components

Component `status` has formal meaning:

* `active` — recognized and usable
* `reserved` — defined but not yet implemented
* `deprecated` — legacy; must not be used in new work

Reserved components:

* are valid scope targets,
* may not be implemented unless phases/gates permit,
* must not be assumed to exist in code.

---

## 9. Common pitfalls

### Invalid scope token

If a document claims:

```yaml
doc_scope: shell:new_ui
```

but that token does not exist in `doc_scope_enum`:

* tooling must reject it,
* the component must be formally registered,
* or the document must be corrected.

---

### Implicit component creation

If code introduces a new logical component but:

* it is not in the registry,
* and not in decomposition,

then component identity is ambiguous.

This is a **Gate 0 architectural violation**.

---

## 10. Non-goals

This registry does **not**:

* define correctness criteria (see `ACCEPTANCE_GATES.md` and test oracles),
* define behavioral rules (see spec documents),
* authorize implementation (see `PHASES.md`),
* replace architectural reasoning (see `ARCHITECTURE.md`).

It defines only:

* canonical component identity,
* layer classification,
* documentation scope determinism,
* dependency graph constraints.

---

## 11. Enforcement model (informative)

Tooling may:

* validate YAML `doc_scope` against `doc_scope_enum`,
* validate component-level import edges against `dependency_policy`,
* ensure every registered component has at least one normative doc,
* flag documents referencing unknown components.

All such tooling must treat `COMPONENT_REGISTRY.json` as authoritative.
