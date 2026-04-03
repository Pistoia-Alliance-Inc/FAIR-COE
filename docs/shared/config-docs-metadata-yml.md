# `docs-metadata.yml`

`docs-metadata.yml` is the per-repository contribution contract.

It should sit at the root of each contributing repository.

## Canonical location

```text
<repo-root>/docs-metadata.yml
```

## Purpose

It tells the public/master site:

- where the repository's public docs live
- what navigation it contributes
- what redirects it contributes
- what optional MkDocs capability requests it has

## Example

```yaml
slug: repo-b
section: Semantic Model
docs_root: public-docs
nav:
  - Overview: index.md
  - Model:
      - Canonical Model: model/canonical-model.md
      - Account: model/account.md
redirects:
  - from: model/concepts.md
    to: model/canonical-model.md
mkdocs_requests:
  theme_features:
    - navigation.tabs
```

## Field reference

### `slug`
The canonical repository slug. Must match the slug expected by the public repo.

### `section`
The top-level navigation section title contributed by this repo.

### `docs_root`
The path inside the repo that contains publishable docs.

Typical values:

```yaml
docs_root: public-docs
docs_root: docs
```

### `nav`
The repo-scoped navigation contribution, written in familiar MkDocs nav syntax.

### `redirects`
Repo-scoped redirects.

### `mkdocs_requests`
Optional declaration of requested MkDocs capabilities.

Typical examples:

- theme feature requests
- plugin requests
- markdown extension requests
- CSS/JS asset requests

## Important distinction

`docs-metadata.yml` is **not** a cut-down `mkdocs.yml`.

- `mkdocs.yml` defines how to build a site
- `docs-metadata.yml` defines how a repo participates in a larger site

## Validation

`docs-metadata.yml` is validated against:

```text
schemas/docs-metadata.schema.json
```
