# MkDocs Multi-Repository Starter v11 — Full Base Config

This starter repo includes:

- Node 24-ready GitHub Actions workflows
- updated Pages actions (`upload-pages-artifact@v4`, `deploy-pages@v5`)
- dynamic `MKDOCS_SITE_URL` injection
- bootstrap mode so the public repo can deploy without private repos
- optional vs required private repository handling
- anonymous HTTPS fallback for public repositories
- tag-driven promotion policy
- helper to generate `docs-metadata.yml` from a source repo `mkdocs.yml`
- JSON Schema validation for `docs-metadata.yml`
- full `mkdocs.base.yml` with Material, minify, graph, macros, MathJax, consent, and CSS/JS hooks

## Quick start with bundled examples

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/bootstrap-docs.sh --from-examples
mkdocs serve -f mkdocs.generated.yml
```


## Included configuration documentation

This release includes full documentation for the principal configuration files:

- `repositories.yml`
- `promotion.yml`
- `mkdocs.base.yml`
- `docs-metadata.yml`
- `.env.example`
- `requirements.txt`

These are documented in `docs/shared/` and included in the generated navigation.
