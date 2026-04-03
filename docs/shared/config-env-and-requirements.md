# `.env.example` and `requirements.txt`

## `.env.example`

`.env.example` documents the local environment variables expected by the helper scripts.

Example:

```text
REPO_A_URL=git@github.com:your-org/private-repo-a.git
MKDOCS_SITE_URL=http://127.0.0.1:8000/
DOCS_BOOTSTRAP_MODE=true
```

### Typical variables

#### `MKDOCS_SITE_URL`
Used by `generate_site_config.py` to inject `site_url` into `mkdocs.generated.yml`.

#### `DOCS_BOOTSTRAP_MODE`
Controls whether optional repositories may be absent without failing the build.

#### `*_URL`
Per-repository clone URL overrides.

## `requirements.txt`

`requirements.txt` defines the centrally installed Python runtime for the site build.

This is intentionally controlled by the public/master repo.

Contributing repositories may request capabilities, but they do not directly install packages into the shared build.

## Governance principle

Private repos may declare requirements.  
Only the public/master repo approves and installs them.
