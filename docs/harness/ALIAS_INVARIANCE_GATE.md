## G?.X — Alias-Invariance

### Objective

Prove that the documentation base is semantically independent of domain-loaded terminology and can be implemented using canonical neutral terms only.

### Mandatory Criteria

1. ALIAS_MAP.yaml exists and is normative.
2. All canonical terms listed in ALIAS_MAP.yaml exist in GLOSSARY_NORMATIVE.md.
3. Normative specifications use canonical terms for behavioral definitions.
4. Domain-loaded terms do not define behavior.
5. A deterministic mechanical rename pass produces a fully consistent documentation set.
6. All referenced test oracles remain interpretable after renaming.

### Evidence Artifacts

- ALIAS_MAP.yaml
- ALIAS_MAP.md
- Renamed documentation output (docs/_derived/alias_invariant/)
- Rename validation report
- Confirmation that all referenced oracles pass under renamed terminology

### Failure Conditions

Gate fails if:

- Any behavioral rule depends on implicit domain knowledge.
- Any canonical term lacks formal glossary definition.
- Mechanical rename breaks cross-references.
- Any oracle becomes ambiguous or semantically incomplete.

### References

- GLOSSARY_NORMATIVE
- ALIAS_MAP
- TEST_ORACLE_FORMAT_CONVENTION
- CORE_API
