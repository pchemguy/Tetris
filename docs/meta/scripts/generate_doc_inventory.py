"""Generate docs/meta/DOC_INVENTORY.json from Markdown YAML front matter.

Implements DOC_INVENTORY.md business logic:
- Finds the repo root by CLI arg or flexible conventions.
- Locates docs/ (lowercase) and docs/meta/.
- Validates YAML front matter against docs/meta/DOC_SCHEMA.json.
- Builds an inventory and validates it against docs/meta/DOC_INVENTORY.schema.json.
- Writes docs/meta/DOC_INVENTORY.json (fails if it already exists).

Exit codes:
  0  success
  1  usage / validation / IO failure

Dependencies (expected in the environment running the script):
  - PyYAML (yaml)
  - jsonschema

Example:
  python scripts/generate_doc_inventory.py
  python generate_doc_inventory.py -r ../my_repo
  python generate_doc_inventory.py --root:../my_repo

https://chatgpt.com/c/6996ea76-e490-838b-8031-47111ad4132d
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


# ----------------------------
# Constants / configuration
# ----------------------------

ROOT_ALIASES = {"-r", "--root", "--repo", "-p", "--prefix"}

IGNORE_DIR_NAMES = {
  "idea",
  "ideas",
  "archive",
  "archives",
  "draft",
  "drafts",
  "note",
  "notes",
}

KIND_TO_LAYER = {
  "meta": "L0",
  "control": "L1",
  "architecture": "L2",
  "spec": "L3",
  "api": "L3",
  "testing": "L4",
  "report": "L5",
  "idea": "OUT",
}

REQUIRED_ENTRY_FIELDS = {
  "doc_id",
  "name",
  "kind",
  "scope",
  "status",
  "authority",
  "gate_applies_to",
  "phase_applies_to",
}


# ----------------------------
# Utilities
# ----------------------------


def _utc_now_z() -> str:
  # ISO 8601 with trailing Z, seconds precision.
  return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace(
    "+00:00", "Z"
  )


def _posix_rel(p: Path) -> str:
  # Ensure forward slashes in JSON regardless of OS.
  return p.as_posix()


def _preprocess_argv(argv: list[str]) -> list[str]:
  """Normalize tokens like '--root:some/path' -> '--root', 'some/path'.

  Also supports '-r:some/path'.
  """

  out: list[str] = []
  for tok in argv:
    if tok.startswith("--") and ":" in tok:
      k, v = tok.split(":", 1)
      if k in ROOT_ALIASES:
        out.extend([k, v])
      else:
        out.append(tok)
      continue

    if tok.startswith("-") and not tok.startswith("--") and ":" in tok:
      k, v = tok.split(":", 1)
      if k in ROOT_ALIASES:
        out.extend([k, v])
      else:
        out.append(tok)
      continue

    out.append(tok)
  return out


def _import_or_die() -> tuple[Any, Any]:
  """Import PyYAML and jsonschema or fail with a crisp message."""

  try:
    import yaml  # type: ignore
  except Exception as exc:  # pragma: no cover
    raise SystemExit(
      "Missing dependency 'PyYAML'. Install it (e.g., 'pip install pyyaml')."
    ) from exc

  try:
    import jsonschema  # type: ignore
  except Exception as exc:  # pragma: no cover
    raise SystemExit(
      "Missing dependency 'jsonschema'. Install it (e.g., 'pip install jsonschema')."
    ) from exc

  return yaml, jsonschema


def _is_ignored_dir(path: Path) -> bool:
  # Ignore if any path component matches ignored names (case-insensitive).
  for part in path.parts:
    if part.lower() in IGNORE_DIR_NAMES:
      return True
  return False


def _iter_md_files(repo_root: Path, docs_dir: Path) -> Iterable[Path]:
  """Enumerate *.md in repo root and recursively under docs/ excluding ignored dirs."""

  # 1) root-level MD files
  for p in repo_root.glob("*.md"):
    if p.is_file():
      yield p

  # 2) docs/ subtree
  for p in docs_dir.rglob("*.md"):
    if not p.is_file():
      continue
    if _is_ignored_dir(p.relative_to(repo_root)):
      continue
    yield p


def _extract_yaml_front_matter(md_path: Path, yaml_mod: Any) -> dict[str, Any] | None:
  """Return YAML front matter dict or None if missing/invalid."""

  try:
    text = md_path.read_text(encoding="utf-8")
  except UnicodeDecodeError:
    # Be strict: if it can't be read as UTF-8, treat as no valid YAML.
    return None

  lines = text.splitlines()
  if not lines:
    return None
  if lines[0].strip() != "---":
    return None

  # Find the closing '---'
  end_idx: int | None = None
  for i in range(1, len(lines)):
    if lines[i].strip() == "---":
      end_idx = i
      break
  if end_idx is None:
    return None

  yaml_block = "\n".join(lines[1:end_idx]).strip()
  if not yaml_block:
    return None

  try:
    data = yaml_mod.safe_load(yaml_block)
  except Exception:
    return None

  if not isinstance(data, dict):
    return None

  # Normalize keys to str
  out: dict[str, Any] = {}
  for k, v in data.items():
    if isinstance(k, str):
      out[k] = v
  return out


def _load_json(path: Path) -> Any:
  return json.loads(path.read_text(encoding="utf-8"))


def _sorted_unique_str_list(values: Any) -> list[str] | None:
  """Return sorted unique list[str], or None if empty/unusable."""

  if values is None:
    return None

  if isinstance(values, str):
    # If someone wrote a scalar by mistake, treat it as a single-item list.
    items = [values]
  elif isinstance(values, list):
    items = values
  else:
    return None

  out: list[str] = []
  seen: set[str] = set()
  for x in items:
    if not isinstance(x, str):
      continue
    s = x.strip()
    if not s:
      continue
    if s in seen:
      continue
    seen.add(s)
    out.append(s)

  out.sort()
  return out or None


# ----------------------------
# Repo/docs discovery
# ----------------------------


def _find_repo_root_from_cli(cli_root: str | None, script_dir: Path) -> Path | None:
  if not cli_root:
    return None

  p = Path(cli_root)
  if not p.is_absolute():
    p = (script_dir / p).resolve()
  else:
    p = p.resolve()

  if not p.exists() or not p.is_dir():
    raise SystemExit(f"Provided root does not exist or is not a directory: {p}")

  if not (p / "docs").is_dir():
    raise SystemExit(
      "Provided root does not contain a lowercase 'docs/' directory: " f"{p}"
    )

  return p


def _find_repo_root_by_convention(script_path: Path) -> Path:
  """Resolve repo root using flexible conventions.

  Conventions (script is in):
    - {root}/                  -> docs/ must be in same dir
    - {root}/scripts/          -> docs/ must be next to scripts/
    - {root}/docs/             -> repo root is parent of docs/
    - {root}/docs/script/      -> repo root is parent of docs/
    - {root}/docs/meta/        -> repo root is parent of docs/
    - {root}/docs/meta/scripts/-> repo root is parent of docs/
  """

  sdir = script_path.resolve().parent

  candidates: list[Path] = []

  # script in root
  candidates.append(sdir)

  # script in root/scripts
  if sdir.name.lower() == "scripts":
    candidates.append(sdir.parent)

  # script under docs-like locations
  # Walk up a few levels looking for 'docs' as a direct child.
  p = sdir
  for _ in range(0, 6):
    candidates.append(p)
    p = p.parent

  # Unique, in order
  seen: set[Path] = set()
  uniq: list[Path] = []
  for c in candidates:
    c = c.resolve()
    if c in seen:
      continue
    seen.add(c)
    uniq.append(c)

  for base in uniq:
    docs_dir = base / "docs"
    if docs_dir.is_dir():
      return base

  raise SystemExit(
    "Could not locate repo root containing lowercase 'docs/' using CLI or conventions."
  )


# ----------------------------
# Inventory construction
# ----------------------------


@dataclass(frozen=True)
class DocRecord:
  doc_id: str
  name: str
  path: str
  kind: str
  layer: str
  scope: str
  status: str
  authority: str
  gate_applies_to: str
  phase_applies_to: str
  optional_fields: dict[str, Any]

  def to_json_obj(self) -> dict[str, Any]:
    # Emit a stable key order: required fields first, then optional.
    obj: dict[str, Any] = {
      "doc_id": self.doc_id,
      "name": self.name,
      "path": self.path,
      "kind": self.kind,
      "layer": self.layer,
      "scope": self.scope,
      "status": self.status,
      "authority": self.authority,
      "gate_applies_to": self.gate_applies_to,
      "phase_applies_to": self.phase_applies_to,
    }

    for k in sorted(self.optional_fields.keys()):
      obj[k] = self.optional_fields[k]

    return obj


def _compute_layer(kind: str, authority: str) -> str:
  layer = KIND_TO_LAYER.get(kind)
  if layer is None:
    raise ValueError(f"Unknown kind '{kind}' (cannot compute layer)")

  return layer


def _doc_entry_from_yaml(
  *,
  yaml_data: dict[str, Any],
  md_path: Path,
  repo_root: Path,
) -> DocRecord:
  missing = [k for k in REQUIRED_ENTRY_FIELDS if k not in yaml_data]
  if missing:
    raise ValueError(f"Missing required YAML fields: {sorted(missing)}")

  # Enforce name matches actual filename.
  name = str(yaml_data.get("name"))
  if name != md_path.name:
    raise ValueError(
      f"YAML 'name' does not match filename: yaml={name!r}, file={md_path.name!r}"
    )

  kind = str(yaml_data.get("kind"))
  authority = str(yaml_data.get("authority"))
  layer = _compute_layer(kind, authority)

  rel_dir = md_path.parent.relative_to(repo_root)
  if rel_dir == Path("."):
    rel_dir_str = "."  # root sentinel
  else:
    # Include trailing slash for directories to match typical examples.
    rel_dir_str = _posix_rel(rel_dir) + "/"

  optional: dict[str, Any] = {}

  # Optional fields per DOC_SCHEMA.md are allowed, but we do not attempt
  # to enumerate them exhaustively here. We apply normalization rules:
  # - omit empty values
  # - sort+dedupe arrays for known array fields
  # - a doc MUST NOT contain both 'url' and 'urls'

  if "url" in yaml_data and "urls" in yaml_data:
    raise ValueError("Doc YAML must not contain both 'url' and 'urls'.")

  array_fields = {"references", "supersedes", "urls"}

  for k, v in yaml_data.items():
    if k in REQUIRED_ENTRY_FIELDS:
      continue

    if k == "layer":
      # Not allowed in YAML; computed.
      continue

    if v is None:
      continue

    if isinstance(v, str) and not v.strip():
      continue

    if isinstance(v, list) and len(v) == 0:
      continue

    if k in array_fields:
      norm = _sorted_unique_str_list(v)
      if norm:
        optional[k] = norm
      continue

    optional[k] = v

  return DocRecord(
    doc_id=str(yaml_data["doc_id"]),
    name=name,
    path=rel_dir_str,
    kind=kind,
    layer=layer,
    scope=str(yaml_data["scope"]),
    status=str(yaml_data["status"]),
    authority=authority,
    gate_applies_to=str(yaml_data["gate_applies_to"]),
    phase_applies_to=str(yaml_data["phase_applies_to"]),
    optional_fields=optional,
  )


def _validate_yaml_schema(
  *,
  jsonschema_mod: Any,
  doc_schema: dict[str, Any],
  yaml_data: dict[str, Any],
) -> list[str]:
  """Return list of human-readable validation errors (empty if ok)."""

  validator = jsonschema_mod.Draft202012Validator(doc_schema)
  errors = sorted(validator.iter_errors(yaml_data), key=lambda e: e.path)
  out: list[str] = []
  for e in errors:
    path = "/".join(str(p) for p in e.path) if e.path else "<root>"
    out.append(f"{path}: {e.message}")
  return out


def _validate_json_schema(
  *,
  jsonschema_mod: Any,
  schema: dict[str, Any],
  instance: Any,
) -> list[str]:
  validator = jsonschema_mod.Draft202012Validator(schema)
  errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
  out: list[str] = []
  for e in errors:
    path = "/".join(str(p) for p in e.path) if e.path else "<root>"
    out.append(f"{path}: {e.message}")
  return out


def _build_inventory(
  *,
  repo_root: Path,
  docs: list[DocRecord],
) -> dict[str, Any]:
  docs_sorted = sorted(docs, key=lambda d: (d.path, d.doc_id))

  return {
    "format": "DOC_INVENTORY",
    "generated_at": _utc_now_z(),
    "repo": {
      "doc_system_doc_id": "DOCUMENTATION_SYSTEM",
      "root": ".",
    },
    "docs": [d.to_json_obj() for d in docs_sorted],
  }


# ----------------------------
# Main
# ----------------------------


def _parse_args(argv: list[str]) -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    prog="generate_doc_inventory.py",
    description="Generate docs/meta/DOC_INVENTORY.json from Markdown YAML front matter.",
  )

  parser.add_argument(
    "-r",
    "--root",
    "--repo",
    "-p",
    "--prefix",
    dest="repo_root",
    default=None,
    help=(
      "Repo root path (must contain lowercase 'docs/'). If relative, resolved "
      "relative to the script's parent directory. Supports '--root:PATH' form."
    ),
  )

  return parser.parse_args(argv)


def main() -> int:
  yaml_mod, jsonschema_mod = _import_or_die()

  argv = _preprocess_argv(list(os.sys.argv[1:]))
  args = _parse_args(argv)

  script_path = Path(__file__).resolve()
  script_dir = script_path.parent

  repo_root = _find_repo_root_from_cli(args.repo_root, script_dir)
  if repo_root is None:
    repo_root = _find_repo_root_by_convention(script_path)

  docs_dir = repo_root / "docs"
  meta_dir = docs_dir / "meta"

  if not meta_dir.is_dir():
    raise SystemExit(f"Missing required directory: {meta_dir}")

  out_path = meta_dir / "DOC_INVENTORY.json"
  if out_path.exists():
    raise SystemExit(f"Refusing to overwrite existing file: {out_path}")

  doc_inventory_schema_path = meta_dir / "DOC_INVENTORY.schema.json"
  doc_schema_path = meta_dir / "DOC_SCHEMA.json"

  missing = [
    str(p)
    for p in [doc_inventory_schema_path, doc_schema_path]
    if not p.is_file()
  ]
  if missing:
    raise SystemExit(
      "Missing required schema file(s):\n  - " + "\n  - ".join(missing)
    )

  doc_schema = _load_json(doc_schema_path)
  inventory_schema = _load_json(doc_inventory_schema_path)

  # Enumerate + parse + validate YAML
  yaml_validation_failures: list[str] = []
  records: list[DocRecord] = []

  for md_path in _iter_md_files(repo_root, docs_dir):
    yaml_data = _extract_yaml_front_matter(md_path, yaml_mod)
    if yaml_data is None:
      continue

    errs = _validate_yaml_schema(
      jsonschema_mod=jsonschema_mod, doc_schema=doc_schema, yaml_data=yaml_data
    )
    if errs:
      rel = _posix_rel(md_path.relative_to(repo_root))
      for e in errs:
        yaml_validation_failures.append(f"{rel}: {e}")
      continue

    # Convert to inventory record.
    try:
      rec = _doc_entry_from_yaml(yaml_data=yaml_data, md_path=md_path, repo_root=repo_root)
    except Exception as exc:
      rel = _posix_rel(md_path.relative_to(repo_root))
      yaml_validation_failures.append(f"{rel}: {exc}")
      continue

    records.append(rec)

  if yaml_validation_failures:
    yaml_validation_failures.sort()
    msg = "YAML front matter validation failed:\n  - " + "\n  - ".join(
      yaml_validation_failures
    )
    raise SystemExit(msg)

  # Hard failure: duplicate doc_id
  doc_id_to_paths: dict[str, list[str]] = {}
  for r in records:
    doc_id_to_paths.setdefault(r.doc_id, []).append(r.path + r.name)

  dupes = {k: v for k, v in doc_id_to_paths.items() if len(v) > 1}
  if dupes:
    parts: list[str] = ["Duplicate doc_id detected:"]
    for doc_id in sorted(dupes.keys()):
      parts.append(f"  - {doc_id}: {sorted(dupes[doc_id])}")
    raise SystemExit("\n".join(parts))

  # Hard failure: references target missing from inventory
  all_doc_ids = {r.doc_id for r in records}
  missing_refs: list[str] = []
  for r in records:
    refs = r.optional_fields.get("references")
    if not isinstance(refs, list):
      continue
    for ref in refs:
      if ref not in all_doc_ids:
        missing_refs.append(f"{r.doc_id} -> {ref}")

  if missing_refs:
    missing_refs.sort()
    raise SystemExit(
      "YAML 'references' target missing from inventory:\n  - "
      + "\n  - ".join(missing_refs)
    )

  inventory = _build_inventory(repo_root=repo_root, docs=records)

  # Validate inventory JSON against schema.
  inv_errors = _validate_json_schema(
    jsonschema_mod=jsonschema_mod, schema=inventory_schema, instance=inventory
  )
  if inv_errors:
    inv_errors.sort()
    raise SystemExit(
      "Generated DOC_INVENTORY.json failed schema validation:\n  - "
      + "\n  - ".join(inv_errors)
    )

  out_path.write_text(
    json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
  )

  print(f"Wrote {out_path}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
