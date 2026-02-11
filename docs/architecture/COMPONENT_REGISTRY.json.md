```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "schema_version": "1.0.0",
  "registry_id": "TETRIS.COMPONENT_REGISTRY",
  "project_id": "TETRIS",
  "reserved_scopes": ["global", "core", "shell", "testing"],
  "scope_token_convention": {
    "format": "<layer>:<component_id>",
    "layers": ["core", "shell", "testing"],
    "example": ["core:core", "shell:runtime", "testing:testing"]
  },
  "components": [
    {
      "component_id": "core",
      "layer": "core",
      "title": "Core (Engine)",
      "description": "Pure deterministic simulation. Owns GameState evolution and game rules via new_game()/step().",
      "status": "active",
      "required": true,
      "package": "tetris.core",
      "public_api_modules": ["tetris.core"]
    },
    {
      "component_id": "renderer",
      "layer": "shell",
      "title": "Renderer (pure)",
      "description": "Pure presentation transformer. Converts GameState into a deterministic frame representation (e.g., ASCII text). No I/O.",
      "status": "active",
      "required": true,
      "package": "tetris.rendering",
      "public_api_modules": ["tetris.rendering"]
    },
    {
      "component_id": "presenter",
      "layer": "shell",
      "title": "Terminal Presenter (I/O)",
      "description": "Output adapter. Emits rendered frames to a terminal/stream (clear, write, flush). Treats frames as opaque text/bytes.",
      "status": "active",
      "required": true,
      "package": "tetris.presentation",
      "public_api_modules": ["tetris.presentation"]
    },
    {
      "component_id": "input_driver",
      "layer": "shell",
      "title": "Input Driver (I/O)",
      "description": "Raw input acquisition from OS/environment (keyboard/stdin). Produces raw signals for the Input Controller.",
      "status": "active",
      "required": false,
      "package": "tetris.input.driver",
      "public_api_modules": ["tetris.input.driver"]
    },
    {
      "component_id": "input_controller",
      "layer": "shell",
      "title": "Input Controller (Mapping/Policy)",
      "description": "Maps raw input signals to InputEvent sequences per tick, enforcing per-tick semantics and policy (no implicit repeat unless specified).",
      "status": "active",
      "required": false,
      "package": "tetris.input",
      "public_api_modules": ["tetris.input"]
    },
    {
      "component_id": "runtime",
      "layer": "shell",
      "title": "Runtime (Game Loop / Orchestrator)",
      "description": "Execution-time hub. Owns tick loop, calls step() once per tick, calls renderer, delegates output, terminates on game over.",
      "status": "active",
      "required": true,
      "package": "tetris.runtime",
      "public_api_modules": ["tetris.runtime"]
    },
    {
      "component_id": "cli",
      "layer": "shell",
      "title": "App Shell (CLI / Entrypoints)",
      "description": "Composition root. Parses CLI args, loads external inputs/config via persistence, wires dependencies, then hands control to runtime.",
      "status": "active",
      "required": true,
      "package": "tetris.cli",
      "public_api_modules": ["tetris.cli", "tetris.__main__"]
    },
    {
      "component_id": "persistence",
      "layer": "shell",
      "title": "Persistence (Optional)",
      "description": "Durable I/O services (config/replay/high scores). Invoked by CLI for loading; runtime may use injected sinks for explicit outputs only.",
      "status": "active",
      "required": false,
      "package": "tetris.persistence",
      "public_api_modules": ["tetris.persistence"]
    },
    {
      "component_id": "testing",
      "layer": "testing",
      "title": "Test & Evaluation Harness",
      "description": "Pytest suite + evaluation harness. Not importable by production code.",
      "status": "active",
      "required": true,
      "package": null,
      "source_paths": ["tetris/tests/"],
      "public_api_modules": []
    },
    {
      "component_id": "telemetry",
      "layer": "shell",
      "title": "Telemetry / Observability (Optional)",
      "description": "Passive diagnostics and tracing that must not affect core determinism or semantics.",
      "status": "reserved",
      "required": false,
      "package": "tetris.telemetry",
      "public_api_modules": ["tetris.telemetry"]
    }
  ],
  "doc_scope_enum": [
    "global",
    "core",
    "shell",
    "testing",
    "core:core",
    "shell:renderer",
    "shell:presenter",
    "shell:input_driver",
    "shell:input_controller",
    "shell:runtime",
    "shell:cli",
    "shell:persistence",
    "shell:telemetry",
    "testing:testing"
  ],
  "dependency_policy": {
    "rule": "deny_by_default",
    "allowed_component_edges": [
      ["runtime", "core"],
      ["runtime", "renderer"],
      ["runtime", "presenter"],
      ["runtime", "input_driver"],
      ["runtime", "input_controller"],
      ["cli", "runtime"],
      ["cli", "core"],
      ["cli", "renderer"],
      ["cli", "presenter"],
      ["cli", "input_driver"],
      ["cli", "input_controller"],
      ["cli", "persistence"],
      ["renderer", "core"]
    ],
    "forbidden_component_edges": [
      ["core", "runtime"],
      ["core", "cli"],
      ["core", "renderer"],
      ["core", "presenter"],
      ["core", "input_driver"],
      ["core", "input_controller"],
      ["core", "persistence"],
      ["core", "telemetry"],
      ["presenter", "core"],
      ["presenter", "runtime"],
      ["input_driver", "core"],
      ["input_driver", "runtime"],
      ["persistence", "runtime"],
      ["persistence", "cli"],
      ["telemetry", "runtime"],
      ["telemetry", "cli"]
    ],
    "notes": [
      "The dependency graph is component-level policy; module-level import rules should be derived from 'package' roots.",
      "Renderer may import core types only (enforced by code review / tooling)."
    ]
  },
  "enforcement": {
    "lint_targets": ["tetris/src/tetris/", "tetris/tests/"],
    "tooling_notes": [
      "Generate DOC_SCHEMA doc_scope enum from doc_scope_enum.",
      "Validate @DOC_ID references in markdown against YAML doc_id inventory.",
      "Optional: static import linter can map module imports to component_id via 'package'."
    ]
  }
}
```