import argparse
import os
import yaml
from common import ROOT, resolve_repo_paths, load_repo_metadata, load_available_repo_slugs, load_yaml

def prefix_nav(item, prefix):
    if isinstance(item, list):
        return [prefix_nav(x, prefix) for x in item]
    if isinstance(item, dict):
        out = {}
        for k, v in item.items():
            out[k] = f"{prefix}/{v}" if isinstance(v, str) else prefix_nav(v, prefix)
        return out
    return item

def flatten_nav(item, out=None):
    out = out or []
    if isinstance(item, list):
        for x in item:
            flatten_nav(x, out)
    elif isinstance(item, dict):
        for _, v in item.items():
            if isinstance(v, str):
                out.append(v)
            else:
                flatten_nav(v, out)
    return out

def resolve_site_url(from_examples):
    v = os.environ.get("MKDOCS_SITE_URL", "").strip()
    if not v:
        if from_examples:
            return "http://127.0.0.1:8000/"
        raise SystemExit("MKDOCS_SITE_URL must be set for non-example builds.")
    return v if v.endswith("/") else v + "/"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()
    cfg = load_yaml(ROOT / "mkdocs.base.yml")
    cfg["site_url"] = resolve_site_url(args.from_examples)
    shared_nav = [
        {"Home": "index.md"},
        {"Shared": [
            {"Glossary": "shared/glossary.md"},
            {"Conventions": "shared/conventions.md"},
            {"Deployment Pattern": "shared/deployment-pattern.md"},
            {"Script Guide": "shared/script-guide.md"},
            {"Policy Enforcement": "shared/policy-enforcement.md"},
            {"Configuration Reference": "shared/configuration-reference.md"},
            {"Configuration Overview": "shared/configuration-overview.md"},
            {"repositories.yml": "shared/config-repositories-yml.md"},
            {"promotion.yml": "shared/config-promotion-yml.md"},
            {"mkdocs.base.yml": "shared/config-mkdocs-base-yml.md"},
            {"docs-metadata.yml": "shared/config-docs-metadata-yml.md"},
            {".env.example and requirements.txt": "shared/config-env-and-requirements.md"}
        ]}
    ]
    dyn = []
    redirects = {}
    available = load_available_repo_slugs()
    errors = []
    for entry, repo_path in resolve_repo_paths(args.from_examples):
        slug = entry["slug"]
        if available is not None and slug not in available:
            continue
        if not repo_path.exists():
            continue
        meta = load_repo_metadata(repo_path)
        section = meta.get("section")
        nav = meta.get("nav", [])
        if not section:
            errors.append(f"Metadata missing section: {repo_path / 'docs-metadata.yml'}")
            continue
        for rel in flatten_nav(nav):
            if not (ROOT / "docs" / "domains" / slug / rel).exists():
                errors.append(f"Missing nav target for {slug}: {rel}")
        dyn.append({section: prefix_nav(nav, f"domains/{slug}")})
        for r in meta.get("redirects", []):
            src = f"domains/{slug}/{r['from']}"
            dst = f"domains/{slug}/{r['to']}"
            redirects[src] = dst
    if errors:
        for e in errors:
            print(e)
        raise SystemExit(1)
    cfg["nav"] = shared_nav + dyn
    for plugin in cfg.get("plugins", []):
        if isinstance(plugin, dict) and "redirects" in plugin:
            plugin["redirects"]["redirect_maps"] = redirects
    out = ROOT / "mkdocs.generated.yml"
    out.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Generated {out}")

if __name__ == "__main__":
    main()
