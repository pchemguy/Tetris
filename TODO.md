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
