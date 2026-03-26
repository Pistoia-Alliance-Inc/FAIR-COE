from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent

def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def load_registry():
    return load_yaml(ROOT / "repositories.yml").get("repositories", [])

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
