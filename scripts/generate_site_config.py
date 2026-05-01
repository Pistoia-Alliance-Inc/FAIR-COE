import argparse
import os
import yaml

from common import (
    ROOT,
    resolve_repo_paths,
    load_repo_metadata,
    load_available_repo_slugs,
)


def load_mkdocs_base(path):
    """
    Load trusted master mkdocs.base.yml.

    This intentionally uses yaml.Loader rather than yaml.safe_load because
    MkDocs/PyMdown extensions may require Python YAML tags, e.g.

      !!python/object/apply:pymdownx.slugs.slugify
    """
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.Loader) or {}


def prefix_nav(item, prefix):
    if isinstance(item, list):
        return [prefix_nav(x, prefix) for x in item]

    if isinstance(item, dict):
        return {
            k: f"{prefix}/{v}" if isinstance(v, str) else prefix_nav(v, prefix)
            for k, v in item.items()
        }

    return item


def flatten_nav(item, out=None):
    if out is None:
        out = []

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
    site_url = os.environ.get("MKDOCS_SITE_URL", "").strip()

    if not site_url:
        if from_examples:
            return "http://127.0.0.1:8000/"
        raise SystemExit("MKDOCS_SITE_URL must be set for non-example builds.")

    return site_url if site_url.endswith("/") else site_url + "/"


def dedupe(seq):
    seen = set()
    out = []

    for item in seq:
        key = str(item)
        if key not in seen:
            seen.add(key)
            out.append(item)

    return out


def resolve_repo_asset(slug, asset_value, kind):
    if not isinstance(asset_value, str):
        raise FileNotFoundError(
            f"Asset value for {slug} must be a string: {asset_value!r}"
        )

    if kind == "javascript" and asset_value.startswith(("http://", "https://")):
        return asset_value

    repo_candidate = ROOT / "docs" / "domains" / slug / asset_value
    global_candidate = ROOT / "docs" / asset_value

    if repo_candidate.exists():
        return f"domains/{slug}/{asset_value}"

    if global_candidate.exists():
        return asset_value

    raise FileNotFoundError(
        f"Missing requested {kind} asset for {slug}: {asset_value} "
        f"(checked {repo_candidate} and {global_candidate})"
    )


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()

    cfg = load_mkdocs_base(ROOT / "mkdocs.base.yml")
    cfg["site_url"] = resolve_site_url(args.from_examples)

    shared_nav = [
        {"Home": "index.md"},
        {
            "Shared": [
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
                {
                    ".env.example and requirements.txt": (
                        "shared/config-env-and-requirements.md"
                    )
                },
                {"PAT Instructions": "shared/PAT_Instructions.md"},
            ]
        },
    ]

    available = load_available_repo_slugs()
    dynamic_nav = []
    redirects = {}
    errors = []

    extra_css = list(cfg.get("extra_css", []))
    extra_javascript = list(cfg.get("extra_javascript", []))

    for entry, repo_path in resolve_repo_paths(args.from_examples):
        slug = entry["slug"]

        if available is not None and slug not in available:
            continue

        if not repo_path.exists():
            continue

        meta = load_repo_metadata(repo_path)

        section = meta.get("section")
        nav = meta.get("nav", [])
        requests = meta.get("mkdocs_requests", {}) or {}

        if not section:
            errors.append(f"Metadata missing section: {repo_path / 'docs-metadata.yml'}")
            continue

        for rel in flatten_nav(nav):
            target = ROOT / "docs" / "domains" / slug / rel
            if not target.exists():
                errors.append(f"Missing nav target for {slug}: {rel}")

        dynamic_nav.append({section: prefix_nav(nav, f"domains/{slug}")})

        for redirect in meta.get("redirects", []) or []:
            src = f"domains/{slug}/{redirect['from']}"
            dst = f"domains/{slug}/{redirect['to']}"

            if src == dst:
                errors.append(f"Self redirect not allowed: {src}")
            elif src in redirects:
                errors.append(f"Duplicate redirect source: {src}")
            else:
                redirects[src] = dst

        for css in requests.get("extra_css", []):
            try:
                extra_css.append(resolve_repo_asset(slug, css, "css"))
            except FileNotFoundError as exc:
                errors.append(str(exc))

        for js in requests.get("extra_javascript", []):
            try:
                extra_javascript.append(resolve_repo_asset(slug, js, "javascript"))
            except FileNotFoundError as exc:
                errors.append(str(exc))

    has_loop, loop_start = detect_redirect_loops(redirects)

    if has_loop:
        errors.append(f"Redirect loop detected starting at: {loop_start}")

    for src, dst in redirects.items():
        if dst in redirects:
            errors.append(f"Redirect chain detected: {src} -> {dst} -> {redirects[dst]}")

    if errors:
        print("Site config generation failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    cfg["nav"] = shared_nav + dynamic_nav
    cfg["extra_css"] = dedupe(extra_css)
    cfg["extra_javascript"] = dedupe(extra_javascript)

    for plugin in cfg.get("plugins", []):
        if isinstance(plugin, dict) and "redirects" in plugin:
            plugin["redirects"]["redirect_maps"] = redirects

    out = ROOT / "mkdocs.generated.yml"
    out.write_text(
        yaml.dump(cfg, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    print(f"Generated {out}")


if __name__ == "__main__":
    main()

