### “Which tests to run for this gate?” (normative)

When executing gate `GX.Y`:

1. **Implementation oracle**:
    * If `implementation_oracle` is not null: include that oracle’s test suite.
2. **Regression gates**:
    * For each `gid` in `regression_gates`:
        * Load that gate’s metadata.
        * Include *its* `implementation_oracle` test suite **if non-null**.
        * Then recursively process its `regression_gates`.
3. **De-duplication**:
    * If the same oracle is reached multiple times, run it once.
4. **Cycle handling**:
    * If a cycle is detected in `regression_gates`, execution is invalid (hard failure). Keep this as a governance rule.

This gives you exactly what you want: **gates reference gates; gates own oracles; oracles remain decoupled**.

---

