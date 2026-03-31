# Script Guide

- `check_workflow_actions.py` validates workflow action versions against guardrails
- `check_site_url.py` validates `MKDOCS_SITE_URL` policy
- `checkout_repos.py` checks out available repositories and tolerates missing optional ones in bootstrap mode
- `check_promotion_policy.py` validates tag-driven promotion policy
- `sync_public_docs.py` mounts only repositories that are available
- `generate_site_config.py` generates `mkdocs.generated.yml` from shared content plus mounted repositories
- `validate_contract.py` validates the mounted estate
- `check_redirects.py` validates redirects for available repositories
- `check_links.py` validates links and anchors
- `write_promotion_manifest.py` writes a build audit manifest
