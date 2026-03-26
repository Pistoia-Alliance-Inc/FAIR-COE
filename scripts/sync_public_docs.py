import argparse, shutil
from common import ROOT, resolve_repo_paths, load_repo_metadata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()
    mount_root = ROOT / "docs" / "domains"
    mount_root.mkdir(parents=True, exist_ok=True)
    for entry, repo_path in resolve_repo_paths(args.from_examples):
        metadata = load_repo_metadata(repo_path)
        docs_root = metadata.get("docs_root", "public-docs")
        slug = metadata["slug"]
        public_docs = repo_path / docs_root
        if not public_docs.exists():
            raise FileNotFoundError(f"{public_docs} does not exist")
        target = mount_root / slug
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(public_docs, target)
    print("Mounted public-docs into docs/domains")

if __name__ == "__main__":
    main()
