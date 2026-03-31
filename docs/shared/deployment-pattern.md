# Deployment Pattern

## Bootstrap mode

Set:

```text
DOCS_BOOTSTRAP_MODE=true
```

This allows the public repo to deploy from shared/public pages only, even when private repositories are unavailable.

## Strict mode

Mark repositories as `required: true` and disable bootstrap mode when they become mandatory.

## `site_url` handling

`generate_site_config.py` injects `site_url` into `mkdocs.generated.yml` from `MKDOCS_SITE_URL`.
