from pathlib import Path
import argparse
import yaml

IGNORE = {"search", "redirects"}

def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def normalise_redirects(plugins):
    out = []
    for plugin in plugins or []:
        if isinstance(plugin, dict) and "redirects" in plugin:
            for src, dst in (plugin["redirects"] or {}).get("redirect_maps", {}).items():
                out.append({"from": src, "to": dst})
    return out

def normalise_plugins(plugins):
    out = []
    for plugin in plugins or []:
        if isinstance(plugin, str):
            if plugin not in IGNORE:
                out.append({"name": plugin})
        elif isinstance(plugin, dict):
            for name, cfg in plugin.items():
                if name not in IGNORE:
                    out.append({"name": name, "config": cfg or {}})
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--slug")
    parser.add_argument("--section")
    parser.add_argument("--mkdocs-file", default="mkdocs.yml")
    parser.add_argument("--output")
    args = parser.parse_args()
    repo = args.source_repo.resolve()
    mk = load_yaml(repo / args.mkdocs_file)
    slug = args.slug or repo.name.lower().replace("_", "-")
    section = args.section or mk.get("site_name") or repo.name
    data = {
        "slug": slug,
        "section": section,
        "docs_root": mk.get("docs_dir", "docs"),
        "nav": mk.get("nav", []),
        "redirects": normalise_redirects(mk.get("plugins", []))
    }
    requests = {}
    theme = mk.get("theme", {}) or {}
    if isinstance(theme, dict) and theme.get("features"):
        requests["theme_features"] = theme["features"]
    plugins = normalise_plugins(mk.get("plugins", []))
    if plugins:
        requests["plugins"] = plugins
    if mk.get("markdown_extensions"):
        requests["markdown_extensions"] = mk["markdown_extensions"]
    if mk.get("extra_javascript"):
        requests["extra_javascript"] = mk["extra_javascript"]
    if mk.get("extra_css"):
        requests["extra_css"] = mk["extra_css"]
    if requests:
        data["mkdocs_requests"] = requests
    out = Path(args.output) if args.output else repo / "docs-metadata.yml"
    out.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
