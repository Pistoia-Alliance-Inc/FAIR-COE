# `mkdocs.base.yml`

`mkdocs.base.yml` is the public/master repo's baseline MkDocs configuration.

It contains global settings that apply to the entire aggregated site.

## Included responsibilities

- site identity
- theme selection
- approved plugins
- approved markdown extensions
- global JavaScript and CSS hooks
- global consent and UI settings

## Current structure

```yaml
site_name: Enterprise Documentation Hub

theme:
  name: material

plugins:
  - search
  - redirects:
      redirect_maps: {}
  - minify:
      minify_html: true
  - graph:
      name: "title"
  - macros:
      on_error_fail: true
```

## Why this file is centralised

A multi-repository documentation hub still produces one final MkDocs site.

That means these values must be controlled centrally:

- theme
- plugin activation
- markdown extension behaviour
- consent policy
- shared CSS/JS

Contributing repositories should not own these directly.

## Generated companion: `mkdocs.generated.yml`

`mkdocs.base.yml` is not the final build file.

The build process generates `mkdocs.generated.yml` by combining:

- `mkdocs.base.yml`
- generated nav
- generated redirect maps
- injected `site_url`

The final build command uses:

```bash
mkdocs build -f mkdocs.generated.yml --strict
```

## Governance note

Treat `mkdocs.base.yml` as the platform baseline.  
Treat `mkdocs.generated.yml` as an ephemeral build artefact.
