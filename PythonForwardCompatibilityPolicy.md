---
url: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/699e9baf-aa38-838f-a530-eca1521685af
---

## Python Forward Compatibility Policy

### Synopsis

Public and inter-component APIs SHALL support controlled forward evolution through additive, backward-safe changes only. Additive changes (e.g., new keyword-only parameters with defaults, optional structured fields, or explicitly negotiated capabilities) are permitted only when baseline contract semantics remain preserved. Unknown or unsupported extensions must be either safely ignored under documented degradation rules or rejected with explicit, deterministic errors - never silently misinterpreted. Extensibility must be explicit, typed, validated, and capability-aware; it must not weaken type guarantees or obscure contract clarity. Silent semantic changes are prohibited.

Governing documentation, public APIs, and key private architectural boundaries MUST explicitly declare compliance with this policy, define baseline and extension capabilities, articulate degradation semantics, and document compatibility direction. Capability definitions SHALL be architecturally grounded and consistently referenced across decomposition, behavioral specifications, API documentation, and tests. Compatibility claims MUST be test-backed.

### 1. Objective and non-goals

**Objective:** Design APIs and internal contracts so that newer components can interoperate with older ones and vice versa, within defined limits, while enabling additive evolution without breaking existing callers.

**Non-goals:**

* This policy does not require permanent support for all historical behaviors.
* This policy does not justify "anything-goes" extensibility (e.g., unvalidated `**kwargs`, untyped dicts, or opaque blobs) that erodes contract clarity.

---

### 2. Terminology

* **Contract:** The observable behavior of an API: accepted inputs, produced outputs, error modes, side effects, performance expectations (if relevant), and invariants.
* **Baseline contract:** The minimum stable subset that all implementations must support.
* **Extension:** An additive capability that builds on the baseline contract.
* **Capability:** A named, testable feature a component may support (e.g., `supports_color`, `supports_effects`, `supports_compression`).
* **Negotiation:** A mechanism by which components discover and agree on which capabilities to use at runtime.
* **Graceful degradation:** When an extension is not supported, behavior falls back to baseline (or fails with an explicit, documented error if fallback is unsafe).

---

### 3. Compatibility goals (what must work)

When two components interact (module A calls module B; "producer" sends data to "consumer"; "core" talks to "shell"), design so that:

1. **New caller -> old callee:** A newer component can call an older component and either:
    * use only baseline features automatically, or
    * detect missing capability and degrade predictably (or fail explicitly).
2. **Old caller -> new callee:** An older component can call a newer component without modification. Newer callee must preserve baseline behavior and default semantics.
3. **New data -> old consumer (if applicable):** Older consumers must either ignore unknown fields safely or reject them with an explicit "unsupported version/capability" error - never silent misinterpretation.
4. **Old data -> new consumer:** New consumers must accept and interpret baseline data without requiring extension fields.

This is the minimum interoperability envelope. If you choose to support more (e.g., multi-step negotiations), document it as a project-specific addition.

---

### 4. Contract versioning and capability negotiation

#### 4.1 Prefer capabilities over "version integers" for feature gating

* Use **explicit capability flags** (or feature descriptors) rather than "if version >= 3 do X".
* Capabilities are:
    * named (stable identifiers),
    * independently testable,
    * documented with semantics and constraints.

#### 4.2 Provide a discovery mechanism where meaningful

If two components must interoperate across baselines/extensions, define **one** of the following:

* A method/property returning supported capabilities (e.g., `capabilities() -> frozenset[str]`).
* A handshake/negotiation call (e.g., `negotiate(requested_caps) -> agreed_caps`).
* A schema/version tag on exchanged data (e.g., `"schema_version": 1` plus optional `"extensions": [ ...]`).

Keep discovery *simple* and stable. Avoid implicit introspection hacks.

#### 4.3 Unknown capability handling must be defined

* Unknown requested capability: **ignore** (if safe) or **reject explicitly** (if unsafe).
* Unknown provided capability: ignore.

---

### 5. Additive evolution rules (what you may change without breaking)

These changes are allowed under forward compatibility **if defaults preserve baseline semantics**:

#### 5.1 Function and method signatures

Allowed:

* Add **keyword-only** parameters with sensible defaults.
* Add parameters encapsulated via a **typed options/config object**.
* Add new enum variants if unknown variants are handled explicitly.

Avoid:

* Adding new **positional** parameters.
* Reordering parameters.
* Changing parameter meaning without renaming.

#### 5.2 Return types

Allowed:

* Add optional fields to structured return objects (dataclasses/TypedDict/model objects) if older consumers can ignore them.
* Add richer return information via an *alternative* method, not by mutating the existing return type in-place, unless it remains backward-safe.

Avoid:

* Changing return type shape in a way that breaks destructuring/unpacking.
* Switching from scalar -> container without a compatibility wrapper.

#### 5.3 Data structures and serialized forms

Allowed:

* Add new fields that are optional and have defaults.
* Add extension sections keyed by stable identifiers (e.g., `"extensions": {"cap_x": { ...}}`).

Avoid:

* Repurposing an existing field for new semantics.
* Changing meaning of sentinel values.

---

### 6. Controlled extensibility patterns (preferred tools)

#### 6.1 Prefer typed options/config objects over `**kwargs`

Use:

* `@dataclass(frozen=True)` options
* `TypedDict` (for dict-like configs)
* Pydantic / attrs (if your stack already uses them)

Benefits:

* Typed defaults
* Validation centralization
* Predictable evolution

#### 6.2 If you accept `**kwargs`, it must be *explicit and validated*

`**kwargs` is permitted only when:

* Each recognized key is documented with type and semantics.
* Unknown keys are either:
    * rejected (`TypeError` / `ValueError`) **by default**, or
    * accepted only under an explicit "allow_unknown" mode with documented behavior.
* Runtime validation exists (do not rely solely on type hints).

#### 6.3 Use "extension slots" deliberately

If you need "unknown fields tolerated" behavior, prefer:

* a dedicated `extensions: Mapping[str, Any]` field, or
* a dedicated `metadata: Mapping[str, JsonValue]` field

...instead of letting unknown keys leak into the top-level namespace.

---

### 7. Defaults must preserve baseline semantics

For any additive feature:

* The default configuration must produce **baseline-equivalent behavior**.
* If baseline-equivalent behavior is impossible, the API must:
    * require explicit opt-in (no silent activation), and
    * fail fast with an actionable error message when incompatible components are detected.

---

### 8. Error handling and degradation rules

#### 8.1 No silent misinterpretation

If an extension affects semantics (not just cosmetics), and the callee cannot safely emulate baseline behavior:

* raise a **specific**, documented exception (e.g., `UnsupportedCapabilityError`, `IncompatibleContractError`).

#### 8.2 Degradation must be deterministic

If degradation is allowed:

* document exactly what is dropped/approximated,
* ensure it is test-covered,
* keep it consistent across versions.

---

### 9. Type safety requirements

Forward compatibility must not be achieved by weakening typing:

* Avoid "escape hatches" like `dict[str, Any]` for core contracts.
* Prefer structured types for boundaries.
* If a boundary must accept semi-structured data, isolate it and validate early ("parse/validate at the edge, keep internals typed").

---

### 10. Deprecation policy (how to move fast without breaking)

* Deprecation must be:
    * announced in docstrings/changelog,
    * optionally emitted as a `DeprecationWarning`,
    * accompanied by migration guidance.
* Remove deprecated behavior only with:
    * a documented major contract change, or
    * a clearly stated "support window" policy in the project.

---

### 11. Testing Requirements

Forward compatibility claims are meaningless without explicit, classified, and enforced test coverage.

Testing MUST validate:

* Baseline contract conformance
* Cross-version interoperability
* Extension handling behavior
* Degradation semantics
* Unknown-field behavior
* Capability negotiation logic (if applicable)

Documentation claims without test support constitute non-compliance.

---

#### 11.1 Baseline Conformance

Baseline tests MUST:

* Validate only baseline-defined features
* Avoid relying on extension-specific fields or behavior
* Fail if baseline semantics change

Baseline tests establish the minimum invariant contract.

These tests:

* MUST pass for all compliant implementations
* MUST pass regardless of supported extensions
* MUST NOT assume extension presence

---

#### 11.2 Cross-Version / Cross-Capability

If multiple implementations or contract generations exist, tests MUST include:

1. **New caller -> old callee**
    * Verify degradation behavior is deterministic or
    * Verify explicit compatibility error
2. **Old caller -> new callee**
    * Verify baseline semantics remain preserved
    * Verify no unexpected behavioral changes

If capability negotiation exists:

* Test successful negotiation
* Test partial negotiation
* Test unsupported capability requests

---

#### 11.3 Unknown-Field / Extension-Field

For structured data contracts:

* Tests MUST verify behavior when:
    * Unknown fields appear in input
    * Unknown extension sections appear
    * Unknown enum variants appear (if allowed)

Expected behavior MUST be explicitly asserted:

* Ignored safely or
* Rejected deterministically

Silent acceptance without validation is prohibited.

---

#### 11.4 Strict vs Forward-Compatible Classification

All tests that exercise compatibility-sensitive contracts SHOULD declare their compatibility intent.

Tests MUST be classified as one of:

---

##### A. Strict Tests

Strict tests assert baseline-only behavior.

Characteristics:

* May assume absence of extensions
* May assert exact structure equality
* May fail if additional fields appear
* Validate minimal invariant behavior

Strict tests protect:

* Baseline semantics
* Contract clarity
* Structural stability

They prevent unintended semantic drift.

---

##### B. Forward-Compatible Tests

Forward-compatible tests assert behavior that must remain valid under additive extensions.

Characteristics:

* Do not assert full structural equality if extension fields are allowed
* Assert only required baseline invariants
* Permit additional extension data
* Remain valid if optional fields are added

Forward-compatible tests protect:

* Additive evolution
* Extension tolerance
* Backward-safe expansion

---

#### 11.5 Test Oracles and Compatibility Intent

If the project uses test oracles or structured test specifications:

* Each oracle MUST explicitly declare compatibility intent:
    * `"compatibility_mode": "strict"`
    * `"compatibility_mode": "forward"`

If no structured oracle system exists:

* Tests SHOULD include explicit markers or naming conventions
    * e.g., `test_xxx_strict`
    * e.g., `test_xxx_forward_compatible`

Compatibility intent must be visible and reviewable.

Implicit compatibility assumptions are prohibited.

---

#### 11.6 Structural Equality vs Semantic Equality

Tests interacting with extensible contracts MUST prefer semantic assertions over structural equality when forward-compatible behavior is intended.

Avoid:

```python
assert result == expected_dict
```

Prefer:

```python
assert result.required_field == expected_value
assert result.status == "ok"
```

unless the test is explicitly marked strict.

---

#### 11.7 Compatibility Regression Protection

If a project claims forward compatibility support:

* Removing a capability MUST require updating compatibility tests.
* Tightening unknown-field rejection MUST require test updates.
* Modifying degradation behavior MUST be covered by regression tests.

No compatibility-affecting change may be merged without updating classified tests.

---

### 12. Documentation Compliance and Governance Requirements

Forward compatibility SHALL be treated as a first-class governance objective. Compatibility is an architectural property and MUST be reflected explicitly in project-level design documentation.

#### 12.1 Mandatory Declaration of Compliance

The following artifacts MUST explicitly state whether they:

* adopt this Forward Compatibility Policy,
* partially adopt it (with documented scope limits), or
* explicitly opt out (with justification).

Required artifacts include:

* Governing project documentation (e.g., architecture, design, strategy documents)
* Public API documentation
* Key private/internal API documentation that define inter-component contracts
* Data format/schema documentation for persisted or transmitted structures

The declaration MUST be explicit. Silence is non-compliance.

---

#### 12.2 Required Content in API Documentation

For each public API and each key private boundary, documentation MUST clearly specify:

1. **Baseline Contract**
    * Required inputs
    * Required outputs
    * Guaranteed invariants
    * Error semantics
    * Supported baseline capabilities
2. **Extension Model**
    * Whether additive parameters are permitted
    * Whether structured extension fields are supported
    * How unknown fields are handled
    * Whether capability negotiation exists and how it works
3. **Compatibility Direction**
    * Whether the component supports:
         * New caller -> old callee degradation
         * Old caller -> new callee compatibility
    * Any explicitly unsupported cross-version interactions
4. **Degradation Semantics**
    * What happens when an extension is unsupported
    * Whether degradation is silent-but-safe or explicit failure
    * Deterministic behavior guarantees
5. **Versioning or Capability Conventions**
    * Version fields (if used)
    * Capability identifiers (if used)
    * Extension namespaces or slots (if used)

---

#### 12.3 Structured Conventions Must Be Declared

If the project adopts conventions such as:

* keyword-only additive parameters,
* dataclass-based options objects,
* `extensions` or `metadata` slots,
* capability enumeration patterns,
* strict unknown-field rejection,

those conventions MUST be:

* listed explicitly in governing documentation,
* applied consistently across boundaries,
* referenced in API documentation.

Implicit conventions are not acceptable.

---

#### 12.4 Private APIs

Private APIs that:

* form architectural boundaries,
* support plugin mechanisms,
* mediate core-shell separation,
* define serialization formats, or
* coordinate major subsystems

MUST be treated as contract-bearing interfaces.

They are subject to the same compatibility documentation requirements as public APIs.

---

#### 12.5 Traceability

Governing documentation SHOULD:

* reference this Forward Compatibility Policy directly,
* identify baseline feature sets,
* identify extension sets,
* define the project's compatibility envelope,
* specify support window expectations (if any).

Compatibility policy must be discoverable from the top-level project governance documentation.

---

#### 12.6 Architectural Capability Decomposition

Projects that claim forward extensibility SHOULD adopt explicit capability-based decomposition at the architectural level.

High-level architectural documentation (e.g., system overview, decomposition documents, behavioral specifications) SHOULD:

1. Define the **Baseline Capability Set**

   * The minimal feature set guaranteed across all compliant implementations.
   * The canonical behavioral contract.
   * The invariant data model subset.

2. Define **Extension Capability Sets**

   * Named, stable capability identifiers.
   * Behavioral deltas relative to baseline.
   * Data model extensions relative to baseline.
   * Dependency relationships between capabilities.

3. Define **Capability Hierarchy or Matrix**

   * Which components may implement which capabilities.
   * Whether capabilities are orthogonal or layered.
   * Whether some capabilities imply others.

Capabilities SHOULD be named using stable identifiers suitable for use in:

* Code-level capability enumeration
* API documentation
* Behavioral specifications
* Test oracles
* Compatibility negotiation (if applicable)

---

#### 12.7 Capability Roadmap and Variants

If multiple architectural variants are anticipated (e.g., baseline implementation, extended core, extended shell, plugin-enabled mode), documentation SHOULD include:

* A capability roadmap identifying:

  * Baseline implementation
  * Planned extension capabilities
  * Optional capability combinations
* A matrix showing:

  * Which architectural variants implement which capabilities
  * Expected compatibility interactions

This roadmap MUST avoid speculative commitments. It defines structure, not delivery promises.

The roadmap enables:

* Controlled additive evolution
* Predictable compatibility boundaries
* Consistent naming of extensions
* Clear separation of baseline vs optional behavior

---

#### 12.8 Decomposition and Behavioral Specifications Alignment

Capability names defined at architectural level MUST:

* Be referenced in behavioral specifications.
* Be referenced in API documentation.
* Be referenced in compatibility tests (if applicable).

Behavioral specifications SHOULD:

* Explicitly declare which capabilities they depend on.
* Describe behavioral deltas introduced by each capability.
* Define degradation semantics when a capability is absent.

Capabilities MUST NOT be introduced implicitly in lower-level documentation.

---

#### 12.9 Capability-Based Extensibility Preference

Even when no runtime negotiation mechanism exists, capability-based design is RECOMMENDED.

Benefits:

* Clear separation of baseline vs optional features
* Easier extension planning
* Reduced risk of semantic drift
* Test matrix clarity
* Explicit compatibility reasoning

Projects SHOULD prefer:

* Capability declarations over version checks.
* Behavioral capability flags over hidden structural assumptions.
* Named extension sets over ad-hoc boolean feature toggles.

Version numbers MAY be used, but version numbers alone are insufficient to describe extension semantics.

---

#### 12.10 Capability Naming Conventions

Projects adopting capability-based extensibility MUST:

* Use stable, documented capability identifiers.
* Avoid transient or implementation-specific naming.
* Avoid renaming capabilities without deprecation process.
* Avoid overloading a capability name with evolving semantics.

Capabilities represent behavioral contracts, not temporary implementation details.

---

#### 12.11 Cross-Document Traceability

Capability definitions SHOULD be traceable across:

* Architectural decomposition documents
* Behavioral specifications
* API documentation
* Test classifications
* Compatibility tests
* Release notes (if applicable)

Each capability SHOULD have a single canonical definition location, referenced elsewhere.

---
