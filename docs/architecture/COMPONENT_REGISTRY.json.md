```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "schema_version": "1.0.0",
  "registry_id": "TETRIS.COMPONENT_REGISTRY",
  "project_id": "TETRIS",
  "reserved_scopes": ["global", "core", "shell"],
  "scope_token_convention": {
    "format": "<layer>:<component_id>",
    "layers": ["core", "shell"],
    "example": ["core:engine", "shell:runtime"]
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
      "public_api_modules": ["tetris.presenter"]
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
      "title": "Input Controller (mapping/policy)",
      "layer": "shell",
      "status": "active",
      "normative": true,

      "package_roots": ["tetris.input"],
      "source_paths": ["tetris/src/tetris/input/"],

      "public_api_modules": ["tetris.input"],
      "notes": "Maps raw signals to InputEvent per INPUT_MODEL."
    },
    {
      "component_id": "runtime",
      "title": "Runtime (Game Loop / Orchestrator)",
      "layer": "shell",
      "status": "active",
      "normative": true,

      "package_roots": ["tetris.runtime"],
      "source_paths": ["tetris/src/tetris/runtime/"],

      "public_api_modules": ["tetris.runtime"],
      "notes": "Execution-time hub. Owns tick loop; calls core once per tick."
    },
    {
      "component_id": "cli",
      "title": "App Shell (CLI / Entrypoints)",
      "layer": "shell",
      "status": "active",
      "normative": true,

      "package_roots": ["tetris.cli", "tetris.__main__"],
      "source_paths": ["tetris/src/tetris/"],

      "public_api_modules": ["tetris.cli", "tetris.__main__"],
      "notes": "Composition root. Parses args, loads config, wires dependencies."
    },
    {
      "component_id": "persistence",
      "title": "Persistence (Optional)",
      "layer": "shell",
      "status": "optional",
      "normative": true,

      "package_roots": ["tetris.persistence"],
      "source_paths": ["tetris/src/tetris/persistence/"],

      "public_api_modules": ["tetris.persistence"],
      "notes": "I/O services: config/replay load; optional save outputs."
    },
    {
      "component_id": "test_harness",
      "title": "Test & Evaluation Harness",
      "layer": "testing",
      "status": "active",
      "normative": true,

      "package_roots": [],
      "source_paths": ["tetris/tests/"],

      "public_api_modules": [],
      "notes": "Pytest suite + evaluation harness. Not importable by production code."
    },
    {
      "component_id": "telemetry",
      "title": "Telemetry / Observability (Optional)",
      "layer": "shell",
      "status": "optional",
      "normative": true,

      "package_roots": ["tetris.telemetry"],
      "source_paths": ["tetris/src/tetris/telemetry/"],

      "public_api_modules": ["tetris.telemetry"],
      "notes": "Passive instrumentation. Must not become controller."
    }
  ],

  "doc_scope_enum": [
    "global",
    "core",
    "shell",
    "component:core",
    "component:renderer",
    "component:presenter",
    "component:input_driver",
    "component:input_controller",
    "component:runtime",
    "component:cli",
    "component:persistence",
    "component:test_harness",
    "component:telemetry"
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
      "The dependency graph is component-level policy; module-level import rules should be derived from package_roots.",
      "Renderer may import core types only (enforced by code review / tooling)."
    ]
  },

  "enforcement": {
    "lint_targets": [
      "tetris/src/tetris/",
      "tetris/tests/"
    ],
    "tooling_notes": [
      "Generate DOC_SCHEMA doc_scope enum from doc_scope_enum.",
      "Validate @DOC_ID references in markdown against YAML doc_id inventory.",
      "Optional: static import linter can map module imports to component_id via package_roots."
    ]
  }
}
```