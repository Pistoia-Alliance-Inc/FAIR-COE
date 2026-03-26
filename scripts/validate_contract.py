import argparse, sys
from common import ROOT, resolve_repo_paths, load_repo_metadata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()
    errors = []
    for entry, repo_path in resolve_repo_paths(args.from_examples):
        metadata = load_repo_metadata(repo_path)
        slug = metadata.get("slug")
        if not slug:
            errors.append(f"Missing slug in {repo_path / 'docs-metadata.yml'}")
            continue
        mount = ROOT / "docs" / "domains" / slug
        if not mount.exists():
            errors.append(f"Missing mount: {mount}")
        elif not (mount / "index.md").exists():
            errors.append(f"Missing index.md for {slug}")
    if not (ROOT / "mkdocs.generated.yml").exists():
        errors.append("Missing mkdocs.generated.yml")
    if errors:
        print("Contract validation failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("Contract validation passed.")

if __name__ == "__main__":
    main()
