from pathlib import Path
import argparse
import json
import sys
from jsonschema import Draft202012Validator
from common import ROOT, resolve_repo_paths, load_available_repo_slugs, load_yaml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()
    schema = json.loads((ROOT / "schemas" / "docs-metadata.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    available = load_available_repo_slugs()
    errors = []
    for entry, repo_path in resolve_repo_paths(args.from_examples):
        slug = entry["slug"]
        if available is not None and slug not in available and not args.from_examples:
            continue
        path = repo_path / "docs-metadata.yml"
        if not path.exists():
            continue
        data = load_yaml(path)
        for err in validator.iter_errors(data):
            errors.append(f"{path}: {err.message}")
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    print("docs-metadata schema validation passed.")

if __name__ == "__main__":
    main()
