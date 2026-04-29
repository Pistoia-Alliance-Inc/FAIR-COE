import argparse, sys
from common import ROOT, resolve_repo_paths, load_available_repo_slugs, is_bootstrap_mode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()

    available = load_available_repo_slugs()
    bootstrap = is_bootstrap_mode() or args.from_examples
    errors = []

    if not (ROOT / "docs" / "index.md").exists():
        errors.append("Missing docs/index.md")
    if not (ROOT / "mkdocs.generated.yml").exists():
        errors.append("Missing mkdocs.generated.yml")

    for entry, repo_path in resolve_repo_paths(args.from_examples):
        slug = entry["slug"]
        required = bool(entry.get("required", False))

        if available is not None and slug not in available:
            if required and not bootstrap:
                errors.append(f"Required repository unavailable: {slug}")
            continue

        mount = ROOT / "docs" / "domains" / slug
        if mount.exists() and not (mount / "index.md").exists():
            errors.append(f"Missing index.md for mounted repo {slug}")
        elif required and not mount.exists() and not bootstrap:
            errors.append(f"Required mounted repo missing: {slug}")

    if errors:
        print("Contract validation failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("Contract validation passed.")

if __name__ == "__main__":
    main()
