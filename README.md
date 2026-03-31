# MkDocs Multi-Repository Starter v9 — Bootstrap Mode

This starter repo extends the site-url, Node 24-ready, policy-enforced, tag-driven promotion pattern with:

- optional vs required private repository handling
- bootstrap mode for public repo deployment without private repositories
- graceful checkout, mount, and nav generation when private repositories are absent
- generated `site_url` from `MKDOCS_SITE_URL`
- Node 24-ready workflows
- promotion policy, workflow guardrails, redirects, links, and anchor validation

## Core behaviour

- `required: false` repositories may be absent without failing the build
- `required: true` repositories must be available in strict mode
- `DOCS_BOOTSTRAP_MODE=true` allows safe initial deployment from shared/public pages only
- shared pages always build, even if zero private repositories are mounted

## Quick start with bundled examples

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/bootstrap-docs.sh --from-examples
python scripts/check_workflow_actions.py
python scripts/check_site_url.py --from-examples
python scripts/check_promotion_policy.py --from-examples
python scripts/validate_contract.py --from-examples
python scripts/check_redirects.py --from-examples
python scripts/check_links.py
mkdocs serve -f mkdocs.generated.yml
```

## Real bootstrap deployment

```bash
export DOCS_BOOTSTRAP_MODE=true
export MKDOCS_SITE_URL=https://your-org.github.io/your-public-repo/
python scripts/check_site_url.py
python scripts/check_promotion_policy.py
python scripts/generate_site_config.py
mkdocs build -f mkdocs.generated.yml --strict
```
