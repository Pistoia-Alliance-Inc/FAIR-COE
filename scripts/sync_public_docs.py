import argparse
import shutil
from common import ROOT, resolve_repo_paths, load_repo_metadata, load_available_repo_slugs, is_bootstrap_mode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()
    mount_root = ROOT / "docs" / "domains"
    mount_root.mkdir(parents=True, exist_ok=True)
    available = load_available_repo_slugs()
    bootstrap = is_bootstrap_mode() or args.from_examples
    for entry, repo_path in resolve_repo_paths(args.from_examples):
        slug = entry["slug"]
        required = bool(entry.get("required", False))
        if available is not None and slug not in available:
            if required and not bootstrap:
                raise SystemExit(f"Required repository unavailable for mount: {slug}")
            print(f"WARNING: Skipping unavailable repository mount: {slug}")
            continue
        if not repo_path.exists():
            continue
        metadata = load_repo_metadata(repo_path)
        public_docs = repo_path / metadata.get("docs_root", "public-docs")
        if not public_docs.exists():
            continue
        target = mount_root / slug
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(public_docs, target)
    print("Mounted available public-docs into docs/domains")

if __name__ == "__main__":
    main()
