# `promotion.yml`

`promotion.yml` defines which promoted refs are eligible for assembly into the published site.

## Structure

```yaml
promotion:
  release_id: public-docs-example-release
  repositories:
    - slug: repo-a
      ref: refs/tags/docs-public-v1.0.0
```

## Field reference

### `release_id`
A human-readable release label for the assembled site.

### `repositories`
List of promoted refs to check out for the current release.

Each item contains:

- `slug` — must match an entry in `repositories.yml`
- `ref` — the promoted Git ref, usually a tag

## Promotion model

The recommended pattern is tag-driven promotion:

```text
refs/tags/docs-public-v1.0.0
refs/tags/docs-public-v1.1.0
```

## Behaviour in bootstrap mode

When `DOCS_BOOTSTRAP_MODE=true`:

- missing promotion refs for optional repositories produce warnings
- missing optional repositories do not fail the build

When bootstrap mode is disabled and a repository is required:

- missing promoted refs fail the build

## Governance note

`promotion.yml` is the release-control layer.  
`repositories.yml` says what *may* participate.  
`promotion.yml` says what *does* participate for this release.
