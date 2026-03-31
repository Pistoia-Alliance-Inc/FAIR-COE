# Deployment Pattern

## `site_url` handling

`generate_site_config.py` injects `site_url` into `mkdocs.generated.yml` from `MKDOCS_SITE_URL`.

Rules:

- example builds default to `http://127.0.0.1:8000/`
- real builds must set `MKDOCS_SITE_URL`
- CI validates the value with `check_site_url.py`

## Node 24-ready workflow principles

- use `actions/checkout@v5`
- use `actions/setup-python@v6`
- set `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`
- fail builds if deprecated workflow actions are detected
