from common import ROOT, load_registry, promotion_map, is_bootstrap_mode, available_repos_manifest_path
import json
import os
import subprocess
import sys

def run(cmd):
    subprocess.run(cmd, check=True)

def current_sha(path):
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()

def main():
    token = os.environ.get("DOCS_READ_TOKEN", "")
    promotions = promotion_map()
    bootstrap = is_bootstrap_mode()
    errors = []
    warnings = []
    audit = []
    available = []
    for r in load_registry():
        slug = r["slug"]
        required = bool(r.get("required", False))
        ref = promotions.get(slug)
        repo_name = r["repository"]
        target = ROOT / r["checkout_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if not ref:
            (errors if required and not bootstrap else warnings).append(f"No promoted ref declared for slug {slug} in promotion.yml")
            continue
        if (target / ".git").exists():
            try:
                run(["git", "-C", str(target), "fetch", "--all", "--tags"])
            except subprocess.CalledProcessError:
                (errors if required and not bootstrap else warnings).append(f"Failed to fetch repository for {slug}")
                continue
        else:
            if token:
                url = f"https://x-access-token:{token}@github.com/{repo_name}.git"
            else:
                env_name = r["remote_url_env"]
                url = os.environ.get(env_name, "").strip() or f"https://github.com/{repo_name}.git"
            try:
                run(["git", "clone", url, str(target)])
                run(["git", "-C", str(target), "fetch", "--all", "--tags"])
            except subprocess.CalledProcessError:
                (errors if required and not bootstrap else warnings).append(f"Failed to clone repository for {slug}")
                continue
        try:
            run(["git", "-c", "advice.detachedHead=false", "-C", str(target), "checkout", "--force", ref])
        except subprocess.CalledProcessError:
            (errors if required and not bootstrap else warnings).append(f"Failed to checkout ref {ref} for {slug}")
            continue
        available.append(slug)
        audit.append({"slug": slug, "repository": repo_name, "ref": ref, "commit_sha": current_sha(target), "required": required})
    cache = ROOT / ".cache"
    cache.mkdir(parents=True, exist_ok=True)
    available_repos_manifest_path().write_text(json.dumps({"available_slugs": available}, indent=2), encoding="utf-8")
    (cache / "promotion-audit.json").write_text(json.dumps({"repositories": audit}, indent=2), encoding="utf-8")
    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    print(f"Available repositories: {', '.join(available) if available else 'none'}")

if __name__ == "__main__":
    main()
