---
name: RENDERING_TEMPLATE_SPEC.md
URL: https://chatgpt.com/g/g-p-698720f783d8819182dba46c5788315b-tetris/c/69872113-2c18-8392-8973-9f57ccc1aa41
---

> [!NOTE]
> 
> This document is a renderer specification template. When implementing a concrete renderer, removed this note.  
> Use `RENDERING_{X}_SPEC.md` name format for concrete specification files, such as `RENDERING_ANSI_SPEC.md`.  
> Use `RENDERING_{X}_TEST_ORACLE.md` for companion test oracle, such as `RENDERING_ANSI_TEST_ORACLE.md`.  
> The default ASCII renderer is the baseline classic implementation named `RENDERING_SPEC.md`

# RENDERING TEMPLATE SPEC

## 1. Purpose

This document defines the **{X} renderer contract**. It specifies **exactly how a `GameState` is rendered** into {X}-specific output. This is a **normative specification**.

If behavior is not defined here, it must not be implemented.

---

## 2. Scope and applicability

- Applies to Acceptance Gate {N}.
- Does **not** modify or extend:
    - core logic,
    - runtime semantics,
    - input processing.
- This renderer is **optional** unless explicitly required by a gate.

---

## 3. Renderer interface

The renderer MUST expose the following interface:

```python
render(state: GameState) -> {OUTPUT_TYPE}
```

Where:

* `state` is treated as **read-only**.
* Output must be **deterministic** and **pure**.

---

## 4. Output format

### 4.1 Output type

* Type: `{OUTPUT_TYPE}`
* Encoding / structure rules (exact).

### 4.2 Required elements

Specify explicitly, for example:

* Board representation
* Active piece visibility
* Metadata (score, level, lines, next, hold)
* Game-over indication

Ordering, formatting, and presence rules must be explicit.

---

## 5. Determinism and purity requirements

The renderer MUST:

* be a pure function of `GameState`,
* perform no I/O,
* perform no timing or animation,
* perform no mutation.

---

## 6. Prohibited behavior

The renderer MUST NOT:

* implement game logic,
* infer missing state,
* normalize or reinterpret core data,
* depend on environment, locale, or terminal features (unless explicitly specified).

---

## 7. Relationship to other renderers

* This renderer is **independent** of all other renderers.
* No behavior may be assumed from `RENDERING_ASCII_SPEC.md` unless restated here.
* Multiple renderers may coexist without semantic coupling.

---

## 8. Versioning and compatibility (optional)

If applicable:

* Version field
* Backward compatibility rules
* Deprecation policy

---

## 9. Test oracle

Correctness for this renderer is governed by:

* `RENDERING_{X}_TEST_ORACLE.md`

Only tests mandated by that document are required.

---
