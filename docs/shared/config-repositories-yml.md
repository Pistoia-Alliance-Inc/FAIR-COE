# `repositories.yml`

`repositories.yml` is the source-controlled registry of repositories that may contribute documentation to the aggregated site.

## Structure

```yaml
repositories:
  - id: repo-a
    slug: repo-a
    repository: your-org/private-repo-a
    local_example_path: examples/private-repo-a
    checkout_path: .cache/repos/repo-a
    remote_url_env: REPO_A_URL
    required: false
```

## Field reference

### `id`
A short internal identifier for the repository entry.

### `slug`
The canonical documentation mount name.

This becomes the mounted path:

```text
docs/domains/<slug>/
```

It is also used in generated navigation and cross-repository links.

### `repository`
The GitHub `owner/repo` value used by checkout logic.

Examples:

```yaml
repository: chris-day/FAIR-Maturity-Matrix
repository: your-org/private-repo-a
```

### `local_example_path`
Path used for local example-mode builds.

### `checkout_path`
Where the repository is cloned in non-example builds.

### `remote_url_env`
Environment variable name that may contain a clone URL override.

Examples:

```text
REPO_A_URL
FAIR_MATURITY_MATRIX_URL
```

### `required`
Controls strictness.

- `false`: repository may be absent in bootstrap mode
- `true`: repository is required when strict mode is enforced

## Recommended usage

Start with all repositories set to:

```yaml
required: false
```

Then promote stable repositories to:

```yaml
required: true
```

when they become mandatory for successful publication.

## Governance note

`repositories.yml` is the authoritative catalogue of candidate repositories.  
If a repository is not listed here, it does not participate in checkout, validation, mounting, or navigation.
