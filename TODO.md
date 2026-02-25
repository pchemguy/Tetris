## [PythonForwardCompatibilityPolicy](PythonForwardCompatibilityPolicy.md)

- Classic implementation - Baseline core/shell (plain terminal output with classic chars)
- Solid filled blocks (both empty and filled cells have matching FG/BG, such as black for empty and white for filled) - With a single color for filled cells, no changes to the core necessary, so baseline core remains. The change affects the rendering part only (shell). Basic extension would be black empty and white filled. One more step still not requiring changes to the core is the ability to configure filled/empty colors. Rendering may be implemented on an ANSI terminal via ESC sequences. 
- Random colored tetrominoes or a fixed set of colors used to color tetrominoes. In such a case, color needs to be selected at spawning stage and filled cell colors would need to be tracked. This variant would require extending both core and shell components.

Forward compatibility statement and related design decisions would need to be reflected at least in `DECOMPOSITION.md` and `L3` and `L4` docs.
