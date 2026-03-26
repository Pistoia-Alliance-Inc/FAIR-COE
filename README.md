# MkDocs Multi-Repository Starter v6 — Policy Enforcement

This starter repo adds CI policy enforcement to the tag-driven promotion pattern.

## Included

- registry-driven repository discovery
- tag-driven promotion via `promotion.yml`
- generated navigation and redirects
- link and anchor validation
- promotion policy validation
- PR policy workflow
- deployment workflow

## Quick start with bundled examples

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/bootstrap-docs.sh --from-examples
python scripts/check_promotion_policy.py
python scripts/validate_contract.py --from-examples
python scripts/check_redirects.py --from-examples
python scripts/check_links.py
mkdocs serve -f mkdocs.generated.yml
```
