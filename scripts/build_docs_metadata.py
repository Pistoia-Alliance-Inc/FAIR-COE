from pathlib import Path
import argparse
import yaml

SITE_WIDE_PLUGINS_TO_IGNORE = {"search", "redirects"}

def load_yaml(path: Path) -> dict:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.Loader) or {}

def normalise_redirects(plugins):
    redirects = []
    for plugin in plugins or []:
        if isinstance(plugin, dict) and "redirects" in plugin:
            cfg = plugin.get("redirects") or {}
            maps = cfg.get("redirect_maps", {}) or {}
            for src, dst in maps.items():
                redirects.append({"from": src, "to": dst})
    return redirects

def normalise_plugin_requests(plugins):
    requests = []

    for plugin in plugins or []:
        if isinstance(plugin, str):
            if plugin in SITE_WIDE_PLUGINS_TO_IGNORE:
                continue
            requests.append({"name": plugin})
            continue

        if isinstance(plugin, dict):
            for name, cfg in plugin.items():
                if name in SITE_WIDE_PLUGINS_TO_IGNORE:
                    continue
                item = {"name": name}
                if cfg:
                    item["config"] = cfg
                requests.append(item)

    return requests

def normalise_theme_features(theme):
    if not isinstance(theme, dict):
        return []
    return list(theme.get("features", []) or [])

def normalise_list(values):
    return list(values or [])

def build_metadata(mkdocs: dict, slug: str, section: str) -> dict:
    plugins = mkdocs.get("plugins", []) or []

    metadata = {
        "slug": slug,
        "section": section,
        "docs_root": mkdocs.get("docs_dir", "docs"),
        "nav": mkdocs.get("nav", []),
        "redirects": normalise_redirects(plugins),
    }

    mkdocs_requests = {}

    theme_features = normalise_theme_features(mkdocs.get("theme", {}) or {})
    plugin_requests = normalise_plugin_requests(plugins)
    markdown_extensions = normalise_list(mkdocs.get("markdown_extensions", []))
    extra_css = normalise_list(mkdocs.get("extra_css", []))
    extra_javascript = normalise_list(mkdocs.get("extra_javascript", []))

    if theme_features:
        mkdocs_requests["theme_features"] = theme_features

    if plugin_requests:
        mkdocs_requests["plugins"] = plugin_requests

    if markdown_extensions:
        mkdocs_requests["markdown_extensions"] = markdown_extensions

    if extra_css:
        mkdocs_requests["extra_css"] = extra_css

    if extra_javascript:
        mkdocs_requests["extra_javascript"] = extra_javascript

    if mkdocs_requests:
        metadata["mkdocs_requests"] = mkdocs_requests

    return metadata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--slug")
    parser.add_argument("--section")
    parser.add_argument("--mkdocs-file", default="mkdocs.yml")
    parser.add_argument("--output")
    args = parser.parse_args()

    repo = args.source_repo.resolve()
    mkdocs_file = repo / args.mkdocs_file

    if not mkdocs_file.exists():
        raise SystemExit(f"mkdocs file not found: {mkdocs_file}")

    mkdocs = load_yaml(mkdocs_file)

    slug = args.slug or repo.name.lower().replace("_", "-")
    section = args.section or mkdocs.get("site_name") or repo.name

    metadata = build_metadata(mkdocs, slug, section)

    output = Path(args.output) if args.output else repo / "docs-metadata.yml"
    output.write_text(
        yaml.dump(metadata, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {output}")

if __name__ == "__main__":
    main()
