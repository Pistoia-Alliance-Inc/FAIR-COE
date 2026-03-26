import argparse, sys
from common import ROOT, resolve_repo_paths, load_repo_metadata

def detect_loop(redirects):
    for start in redirects:
        seen = set()
        cur = start
        while cur in redirects:
            if cur in seen:
                return True, start
            seen.add(cur)
            cur = redirects[cur]
    return False, None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()
    redirects = {}
    errors = []
    for entry, repo_path in resolve_repo_paths(args.from_examples):
        metadata = load_repo_metadata(repo_path)
        slug = metadata["slug"]
        for r in metadata.get("redirects", []):
            src = f"domains/{slug}/{r['from']}"
            dst = f"domains/{slug}/{r['to']}"
            if src == dst:
                errors.append(f"Self redirect: {src}")
            if src in redirects:
                errors.append(f"Duplicate redirect source: {src}")
            if not (ROOT / "docs" / dst).exists():
                errors.append(f"Missing redirect target: {dst}")
            redirects[src] = dst
    has_loop, start = detect_loop(redirects)
    if has_loop:
        errors.append(f"Redirect loop detected starting at: {start}")
    for src, dst in redirects.items():
        if dst in redirects:
            errors.append(f"Redirect chain detected: {src} -> {dst} -> {redirects[dst]}")
    if errors:
        print("Redirect validation failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("Redirect validation passed.")

if __name__ == "__main__":
    main()
