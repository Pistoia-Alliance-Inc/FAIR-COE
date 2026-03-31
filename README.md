# MkDocs Multi-Repository Starter v8 — `site_url` Injection

This starter repo extends the Node 24-ready, policy-enforced, tag-driven promotion pattern with:

- `site_url` injection from `MKDOCS_SITE_URL`
- CI validation of `MKDOCS_SITE_URL`
- generated `mkdocs.generated.yml` with environment-specific `site_url`
- registry-driven repository discovery
- tag-driven promotion via `promotion.yml`
- generated navigation and redirects
- link and anchor validation
- policy-enforcement and deployment workflows

## Key `site_url` behaviour

- example builds default to `http://127.0.0.1:8000/` if `MKDOCS_SITE_URL` is not set
- non-example builds must set `MKDOCS_SITE_URL`
- CI validates the setting with `scripts/check_site_url.py`

## Quick start with bundled examples

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/bootstrap-docs.sh --from-examples
python scripts/check_workflow_actions.py
python scripts/check_site_url.py --from-examples
python scripts/check_promotion_policy.py
python scripts/validate_contract.py --from-examples
python scripts/check_redirects.py --from-examples
python scripts/check_links.py
mkdocs serve -f mkdocs.generated.yml
```

## Real build example

```bash
export MKDOCS_SITE_URL=https://your-org.github.io/your-public-repo/
python scripts/generate_site_config.py
```
