from common import ROOT, load_registry, promotion_map, is_bootstrap_mode, available_repos_manifest_path
import os, subprocess, sys, json

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
    available_slugs = []

    for r in load_registry():
        slug = r["slug"]
        repo_name = r["repository"]
        required = bool(r.get("required", False))
        target = ROOT / r["checkout_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        ref = promotions.get(slug)

        if not ref:
            msg = f"No promoted ref declared for slug {slug} in promotion.yml"
            if required and not bootstrap:
                errors.append(msg)
            else:
                warnings.append(msg)
                continue

        if (target / ".git").exists():
            try:
                run(["git", "-C", str(target), "fetch", "--all", "--tags"])
            except subprocess.CalledProcessError:
                msg = f"Failed to fetch repository for {slug}"
                if required and not bootstrap:
                    errors.append(msg)
                else:
                    warnings.append(msg)
                    continue
        else:
            if token:
                url = f"https://x-access-token:{token}@github.com/{repo_name}.git"
            else:
                env_name = r["remote_url_env"]
                url = os.environ.get(env_name, "")
                if not url:
                    msg = f"No checkout method for {repo_name}; set DOCS_READ_TOKEN or {env_name}"
                    if required and not bootstrap:
                        errors.append(msg)
                    else:
                        warnings.append(msg)
                        continue
            try:
                run(["git", "clone", url, str(target)])
                run(["git", "-C", str(target), "fetch", "--all", "--tags"])
            except subprocess.CalledProcessError:
                msg = f"Failed to clone repository for {slug}"
                if required and not bootstrap:
                    errors.append(msg)
                else:
                    warnings.append(msg)
                    continue

        try:
            run(["git", "-C", str(target), "checkout", "--force", ref])
        except subprocess.CalledProcessError:
            msg = f"Failed to checkout ref {ref} for {slug}"
            if required and not bootstrap:
                errors.append(msg)
            else:
                warnings.append(msg)
                continue

        available_slugs.append(slug)
        audit.append({
            "slug": slug,
            "repository": repo_name,
            "ref": ref,
            "commit_sha": current_sha(target),
            "required": required,
        })

    cache_dir = ROOT / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    available_repos_manifest_path().write_text(json.dumps({"available_slugs": available_slugs}, indent=2), encoding="utf-8")
    (cache_dir / "promotion-audit.json").write_text(json.dumps({"repositories": audit}, indent=2), encoding="utf-8")

    for w in warnings:
        print(f"WARNING: {w}")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print(f"Available repositories: {', '.join(available_slugs) if available_slugs else 'none'}")

if __name__ == "__main__":
    main()
