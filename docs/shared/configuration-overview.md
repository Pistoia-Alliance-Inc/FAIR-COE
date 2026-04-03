# Configuration Overview

This starter uses a small set of configuration files with clear ownership boundaries.

## Design principle

The public/master repository owns:

- site build configuration
- deployment workflows
- dependency installation
- promotion policy
- schema validation
- generated site assembly

Contributing repositories own:

- documentation content
- their `docs-metadata.yml` contract
- repo-local navigation contribution
- repo-local redirects
- optional MkDocs capability requests

## Configuration file map

| File | Purpose | Owned by |
|---|---|---|
| `mkdocs.base.yml` | Global MkDocs baseline for the aggregated site | public repo |
| `mkdocs.generated.yml` | Generated runtime MkDocs config used for the build | generated |
| `repositories.yml` | Registry of contributing repositories | public repo |
| `promotion.yml` | Tag-driven promotion manifest | public repo |
| `requirements.txt` | Installed Python runtime for the build | public repo |
| `schemas/docs-metadata.schema.json` | Validation schema for `docs-metadata.yml` | public repo |
| `docs-metadata.yml` | Per-repository contribution contract | contributing repo |
| `.env.example` | Local development environment template | public repo |

## Build flow

1. validate workflow guardrails
2. validate `MKDOCS_SITE_URL`
3. check out promoted repositories
4. validate `docs-metadata.yml`
5. mount available public docs
6. generate `mkdocs.generated.yml`
7. validate links, redirects, and contract
8. build with MkDocs
