import argparse
import os
import yaml
from common import ROOT, resolve_repo_paths, load_repo_metadata, load_available_repo_slugs

def prefix_nav_paths(item, prefix: str):
    if isinstance(item, list):
        return [prefix_nav_paths(x, prefix) for x in item]
    if isinstance(item, dict):
        out = {}
        for key, value in item.items():
            if isinstance(value, str):
                out[key] = f"{prefix}/{value}".replace("//", "/")
            else:
                out[key] = prefix_nav_paths(value, prefix)
        return out
    return item

def flatten_nav_targets(item, acc=None):
    if acc is None:
        acc = []
    if isinstance(item, list):
        for x in item:
            flatten_nav_targets(x, acc)
    elif isinstance(item, dict):
        for _, value in item.items():
            if isinstance(value, str):
                acc.append(value)
            else:
                flatten_nav_targets(value, acc)
    return acc

def detect_redirect_loops(redirects):
    for start in redirects:
        seen = set()
        cur = start
        while cur in redirects:
            if cur in seen:
                return True, start
            seen.add(cur)
            cur = redirects[cur]
    return False, None

def resolve_site_url(from_examples: bool) -> str:
    site_url = os.environ.get("MKDOCS_SITE_URL", "").strip()
    if not site_url:
        if from_examples:
            return "http://127.0.0.1:8000/"
        raise SystemExit("MKDOCS_SITE_URL must be set for non-example builds.")
    return site_url if site_url.endswith("/") else site_url + "/"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()

    with open(ROOT / "mkdocs.base.yml", "r", encoding="utf-8") as fh:
        base_config = yaml.safe_load(fh) or {}
    base_config["site_url"] = resolve_site_url(args.from_examples)

    shared_nav = [
        {"Home": "index.md"},
        {"Shared": [
            {"Glossary": "shared/glossary.md"},
            {"Conventions": "shared/conventions.md"},
            {"Deployment Pattern": "shared/deployment-pattern.md"},
            {"Script Guide": "shared/script-guide.md"},
            {"Policy Enforcement": "shared/policy-enforcement.md"},
        ]}
    ]

    available = load_available_repo_slugs()
    dynamic_nav = []
    redirect_maps = {}
    errors = []

    for entry, repo_path in resolve_repo_paths(args.from_examples):
        slug = entry["slug"]
        if available is not None and slug not in available:
            continue
        if not repo_path.exists():
            continue

        metadata = load_repo_metadata(repo_path)
        section = metadata.get("section")
        nav = metadata.get("nav", [])
        redirects = metadata.get("redirects", [])

        if not section:
            errors.append(f"Metadata missing section: {repo_path / 'docs-metadata.yml'}")
            continue

        for rel in flatten_nav_targets(nav):
            p = ROOT / "docs" / "domains" / slug / rel
            if not p.exists():
                errors.append(f"Missing nav target for {slug}: {p}")

        dynamic_nav.append({section: prefix_nav_paths(nav, f"domains/{slug}")})

        for r in redirects:
            src = f"domains/{slug}/{r['from']}"
            dst = f"domains/{slug}/{r['to']}"
            if src == dst:
                errors.append(f"Self redirect not allowed: {src}")
            elif src in redirect_maps:
                errors.append(f"Duplicate redirect source: {src}")
            elif not (ROOT / "docs" / dst).exists():
                errors.append(f"Redirect target does not exist: {dst}")
            else:
                redirect_maps[src] = dst

    has_loop, loop_start = detect_redirect_loops(redirect_maps)
    if has_loop:
        errors.append(f"Redirect loop detected starting at: {loop_start}")

    for src, dst in redirect_maps.items():
        if dst in redirect_maps:
            errors.append(f"Redirect chain detected: {src} -> {dst} -> {redirect_maps[dst]}")

    if errors:
        print("Site config generation failed:")
        for e in errors:
            print(f" - {e}")
        raise SystemExit(1)

    base_config["nav"] = shared_nav + dynamic_nav
    for plugin in base_config.get("plugins", []):
        if isinstance(plugin, dict) and "redirects" in plugin:
            plugin["redirects"]["redirect_maps"] = redirect_maps

    out = ROOT / "mkdocs.generated.yml"
    out.write_text(yaml.safe_dump(base_config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Generated {out}")

if __name__ == "__main__":
    main()
