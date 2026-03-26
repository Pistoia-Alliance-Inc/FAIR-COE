from common import ROOT, load_registry, promotion_map
import os, subprocess, sys, json

def run(cmd):
    subprocess.run(cmd, check=True)

def current_sha(path):
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()

def main():
    token = os.environ.get("DOCS_READ_TOKEN", "")
    promotions = promotion_map()
    errors = []
    audit = []
    for r in load_registry():
        slug = r["slug"]
        repo_name = r["repository"]
        target = ROOT / r["checkout_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        ref = promotions.get(slug)
        if not ref:
            errors.append(f"No promoted ref declared for slug {slug} in promotion.yml")
            continue
        if (target / ".git").exists():
            run(["git", "-C", str(target), "fetch", "--all", "--tags"])
        else:
            if token:
                url = f"https://x-access-token:{token}@github.com/{repo_name}.git"
            else:
                env_name = r["remote_url_env"]
                url = os.environ.get(env_name, "")
                if not url:
                    errors.append(f"No checkout method for {repo_name}; set DOCS_READ_TOKEN or {env_name}")
                    continue
            run(["git", "clone", url, str(target)])
            run(["git", "-C", str(target), "fetch", "--all", "--tags"])
        try:
            run(["git", "-C", str(target), "checkout", "--force", ref])
        except subprocess.CalledProcessError:
            errors.append(f"Failed to checkout ref {ref} for {slug}")
            continue
        audit.append({"slug": slug, "repository": repo_name, "ref": ref, "commit_sha": current_sha(target)})
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    out = ROOT / ".cache" / "promotion-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"repositories": audit}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
