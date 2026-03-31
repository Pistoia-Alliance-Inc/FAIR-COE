# Script Guide

- `check_workflow_actions.py` validates workflow action versions against guardrails
- `check_site_url.py` validates `MKDOCS_SITE_URL` policy for deployed builds
- `checkout_repos.py` reads `repositories.yml` and `promotion.yml`, then checks out promoted refs
- `check_promotion_policy.py` validates tag-driven promotion policy
- `sync_public_docs.py` mounts `public-docs/` into `docs/domains/<slug>/`
- `generate_site_config.py` generates `mkdocs.generated.yml`
- `validate_contract.py` validates the mounted estate
- `check_redirects.py` validates redirects
- `check_links.py` validates links and anchors
- `write_promotion_manifest.py` writes a build audit manifest
