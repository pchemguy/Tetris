## [PythonForwardCompatibilityPolicy](PythonForwardCompatibilityPolicy.md)

- Classic implementation - Baseline core/shell (plain terminal output with classic chars)
- Solid filled blocks (both empty and filled cells have matching FG/BG, such as black for empty and white for filled) - With a single color for filled cells, no changes to the core necessary, so baseline core remains. The change affects the rendering part only (shell). Basic extension would be black empty and white filled. One more step still not requiring changes to the core is the ability to configure filled/empty colors. Rendering may be implemented on an ANSI terminal via ESC sequences. 
- Random colored tetrominoes or a fixed set of colors used to color tetrominoes. In such a case, color needs to be selected at spawning stage and filled cell colors would need to be tracked. This variant would require extending both core and shell components.

Forward compatibility statement and related design decisions would need to be reflected at least in `DECOMPOSITION.md` and `L3` and `L4` docs.

## Testing triage

## Test Oracles

- YAML oracle header per oracle file
- YAML oracle header per oracle case
- Oracle refs to regression oracles, implementation oracle, governing specs

## Test Structuring

- For oracle `ORACLE_CORE_COLLISION.md` create tests in `{PACKAGE}/tests/core_collision/` (drop `ORACLE_` and lower case the rest).
- Each test file must include tests for one oracle file only.
- Each test file should reference ORACLE_ID at the top (may be; the parent dir name contains the same info).
- Each test should reference ORACLE_CASE_ID.

## Reports

Test reports should be placed under `docs/reports/`. Further, two separate subdirs should be created:

- `docs/reports/regression/`
- `docs/reports/implementation/` 

When functionality scoped by a particular test oracle file, say `ORACLE_CORE_COLLISION.md`, is implemented, test reports for tests associated with this oracle file should be placed under - `docs/reports/implementation/core_collision/` (same algo as with tests). When the same tests are executed as part of a regression run, place report under `docs/reports/regression/core_collision/`

## Public and key private APIs

- see `CORE_API.md`

## DOC_ID

- Doc_id closure script
- Yaml doc_id -> path
- Doc_id compact definition
- Doc_id to (vpath, file_contents) script 
- If I resolve doc_id to virtual path and contents, texts can be moved to a db.

## Context Engineering

- Refactor gate 0 into context check point
- Each agent run starts with initial context formation. Assuming no cross-run context memory, this context must provide
    - a complete big picture (top-level key docs),
    - a means for agent to understand current project state (what is done? what to do next?),
    - doc closure and/or instructions how to compute it (ideally deterministically using a script).
- With formal YAML references and cross references (per doc, per spec file, per oracle file, per oracle case), it should be possible to define a doc closure for each gate (key top-level docs plus gate specific l3-l4 docs). For example, for regression tests, agent only need the set of related tests to run and no l3/l4 docs.
- Need a flag indicating completed gate.
- The final documentation base needs to be fully specified to the point where at least key terms - "tetris" and "tetromino" - can be replaced with neutral aliases bearing absolutely no semantics. Known to LLM semantics of Tetris is of course helpful in collaboratively developing this project documentation, but the whole point is to develop a generic harness, which means agent(s), which should use developed docs to actually implement the project must ideally rely solely on explicit specs and no hints/semantics shall come from those semantic bearing terms.


- This project uses a hierarchical markdown documentation system (`docs/meta/DOCUMENTATION_SYSTEM.md`) to organize development documentation and development process. Each normative markdown document carries YAML front matter (described in `docs/meta/DOC_SCHEMA.md` and related `docs/meta/DOC_INVENTORY.md`) defining a repository unique `DOC_ID` identifier (`^[A-Z][0-9A-Z_]+$`) that is used to cross reference documents without specifying their path. This ID is used with `@` prefix in prose (non-YAML), such as `@DOC_SCHEMA`. Formal references are included as a `YAML` array `references` without `@`. Similar IDs are also used to label (and reference) specific document sections within embedded secondary YAML blocks where necessary.
- Documentation system hierarchy reflects the structure of the development process. Additionally, for non-doc artifacts that may be produced and used by coding agents, conventional file-system-based structure is defined to compartmentalize artifacts and enable deterministic automated discovery.
- With formal YAML references and cross references (per doc, per spec file, per oracle file, per oracle case), it should be possible to define a doc closure for each gate (key top-level docs plus gate specific l3-l4 docs). For example, for regression tests, agent only need the set of related tests to run and no l3/l4 docs. Tests for each oracle are placed in a conventional tests/ subdir, also enabling automated deterministic selection of specific test set.
- Need a flag indicating completed gate.

## Context Engineering

- Each agent run starts with initial context formation. Assuming no cross-run context memory, this context must provide
    - a complete big picture (top-level key docs),
    - a means for agent to understand current project state (what is done? what to do next?),
    - doc closure and/or instructions how to compute it (ideally deterministically using a script).

Assume agents are instructed to create tests in 


- Tests
  For each test oracle spec `ORACLE_ID/DOC_ID: ORACLE_<SCOPE>_<TOPIC>` a dedicated test suite should be created under
    - `tetris/tests/<scope>_<topic>/`.
  When a gate listing given test oracle spec file as "implementation" (there should exactly one such gate), this test suite is created/updated and executed to validate implementation correctness. When this gate is identified as dependency for a later gate (via gate or family dependency), this test suite will need to be executed according to protocol as a regression test suite; each gate may declare multiple dependent gates, and for each such dependency their respective implementation test suite is executed as a regression test suite for the dependent gate.
- Reports
    - `docs/reports/regression/{GATE_ID_REGRESSION_GATE}/{GATE_ID_DEPENDENT_GATE}/`
    - `docs/reports/implementation/{GATE_ID}/` 

Acceptance Gates partition development process into logical blocks, such that each gate defines implementation scope that can be implemented next, provided all defined prereqs (prior gates and gate families) are already implemented. Implementation involves 

- developing source code according to gate scope and defined associated spec files
- creating associated test suite according to test oracle spec identified as implementation test oracle by the gate
- running regression test suites and creating reports under `docs/reports/regression/{GATE_ID_REGRESSION_GATE}/{GATE_ID_DEPENDENT_GATE}/` for each regression test suite
- running implementation test suite and creating reports under `docs/reports/implementation/{GATE_ID}/` 
- once all tests are passed successfully and all specs are otherwise fulfilled, a completion flag, such as `docs/reports/implementation/{GATE_ID}/completed.flag` can be created.

So, a basic deterministic algo for comprehensive context engineering for coding agent might involve (e.g., via Python scripts executed by the agent or externally by orchestrating process):

- add top-level key docs, architecture/decomposition, acceptance gates (control), documentation system overview, probably also harness describing file. JSON files may or may not needed to be added to the context: if required doc closure, as well as any other pieces necessary for specific work scope defined by acceptance gate to be implemented can be produced via a script deterministically, only those artifacts may need to be added to the initial context, possibly instructing agent how to locate other artifacts, if necessary.
- obtain the inventory of gate families and gates (probably from a JSON or YAML file from a predefined location).
- determine next target
    - verify that all previously started gates are completed:
        - list all subdirs in `docs/reports/implementation/` in ascending order
        - for each subdir matching a `FAMILY_ID` from the inventory, list all subdirs in `docs/reports/implementation/{FAMILY_ID}/` in ascending order.
        - for each subdir name matching `GATE_ID` from the inventory, verify that the `docs/reports/implementation/{FAMILY_ID}/{GATE_ID}/completed.flag` file exists.
            - If not, this is an incomplete gate. Agent would need to assess whether it can be resumed without a human intervention by analyzing report files
    - find the first `docs/reports/implementation/{FAMILY_ID}/{GATE_ID}/` not containing 
- 