from pathlib import Path
import os
import yaml
import json

ROOT = Path(__file__).resolve().parent.parent

def load_yaml(path: Path) -> dict:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.Loader) or {}

def load_registry():
    return load_yaml(ROOT / "repositories.yml").get("repositories", [])

def load_repositories():
    return load_registry()

def load_promotion():
    return load_yaml(ROOT / "promotion.yml").get("promotion", {})

def promotion_map():
    return {r["slug"]: r["ref"] for r in load_promotion().get("repositories", [])}

def load_repo_metadata(repo_path: Path) -> dict:
    meta = repo_path / "docs-metadata.yml"
    if not meta.exists():
        raise FileNotFoundError(f"{meta} does not exist")
    return load_yaml(meta)

def resolve_repo_paths(from_examples: bool):
    repos = []
    for entry in load_registry():
        repo_path = ROOT / entry["local_example_path"] if from_examples else ROOT / entry["checkout_path"]
        repos.append((entry, repo_path))
    return repos

def is_bootstrap_mode() -> bool:
    return os.environ.get("DOCS_BOOTSTRAP_MODE", "").strip().lower() == "true"

def available_repos_manifest_path() -> Path:
    return ROOT / ".cache" / "available-repos.json"

def load_available_repo_slugs():
    p = available_repos_manifest_path()
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    return set(data.get("available_slugs", []))
