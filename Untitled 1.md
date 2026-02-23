
|      |                                           |
| ---- | ----------------------------------------- |
| G0   | **Governance & Compliance**               |
| G0.1 | Repository & Contract Compliance          |
| G1   | **Core Structural Readiness**             |
| G1.1 | Core Skeleton & Types                     |
| G2   | **Core Behavioral Completion**            |
| G2.1 | Geometry & Collision                      |
| G2.2 | Gravity & Line Clearing                   |
| G2.3 | Scoring & RNG                             |
| G2.4 | Input Semantics                           |
| G2.5 | Game Over                                 |
| G3   | **Core Robustness & Auditability**        |
| G3.1 | Hold (Optional)                           |
| G3.2 | Invariants & Strictness                   |
| G3.3 | Regression & Determinism Audit            |
| G4   | **Shell Completion**                      |
| G4.1 | ASCII Renderer                            |
| G4.2 | Scripted Runtime                          |
| G4.3 | CLI                                       |
| G4.4 | Replay                                    |
| G5   | **Integration & System-Level Guarantees** |
| G5.1 | Core MVP Acceptance (G0-G2)               |
| G5.2 | Full System Acceptance (G0-G4)            |

| Domain          | Typical Families |
| --------------- | ---------------- |
| DOC_INFRA       | G0, G5           |
| CORE            | G1, G2, G3       |
| SHELL_BASELINE  | G4, G5           |
| CORE_EXTENSIONS | G3, G5           |
| SHELL_VARIANTS  | G4, G5           |
| BENCHMARK       | G5               |


```json
{
  "domains": {
    "DOC_INFRA"       : ["G0", "G5"],
    "CORE"            : ["G1", "G2", "G3"],
    "SHELL_BASELINE"  : ["G4", "G5"],
    "CORE_EXTENSIONS" : ["G3", "G5"],
    "SHELL_VARIANTS"  : ["G4", "G5"],
    "BENCHMARK"       : ["G5"]
  }
}
```




G0 — Governance & Compliance
G1 — Core Structural Readiness
G2 — Core Behavioral Completion
G3 — Core Robustness & Auditability
G4 — Shell Completion
G5 — Integration & System-Level Guarantees


- `G0` Governance & Compliance
- `G1` Core Structural Readiness
- `G2` Core Behavioral Completion
- `G3` Core Robustness & Auditability
- `G4` Shell Completion
- `G5` Integration & System-Level Guarantees

### G0 — Governance & Repository Compliance

* existing Gate 0

### G1 — Core Structural Readiness

* existing Gate 1 (skeleton & types)

### G2 — Core Behavioral Completion (Pure Simulation)

* Gate 2 — Geometry & collision
* Gate 3 — Gravity & line clearing
* Gate 4 — Scoring & RNG
* Gate 5 — Input semantics
* Gate 6 — Game over

### G3 — Core Robustness & Auditability

* Gate 7 — Hold (optional core extension)
* Gate 8 — Invariants & strictness
* Gate 9 — Regression & determinism audit

### G4 — Shell Completion

* Gate 10 — Renderer
* Gate 11 — Runtime
* Gate 12 — CLI
* Gate 13 — Replay

### G5 — Integration & System-Level Guarantees (MVP / Full System)

* G5.1 — Core MVP Acceptance (requires G0–G2)
* G5.2 — Full System Acceptance (requires G0–G4)

---