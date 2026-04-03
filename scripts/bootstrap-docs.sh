#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FROM_EXAMPLES="false"
if [[ "${1:-}" == "--from-examples" ]]; then
  FROM_EXAMPLES="true"
fi
python "$ROOT_DIR/scripts/check_workflow_actions.py"
if [[ "$FROM_EXAMPLES" == "false" ]]; then
  if [[ -f "$ROOT_DIR/.env" ]]; then
    set -a
    source "$ROOT_DIR/.env"
    set +a
  fi
  python "$ROOT_DIR/scripts/check_site_url.py"
  python "$ROOT_DIR/scripts/checkout_repos.py"
  python "$ROOT_DIR/scripts/validate_docs_metadata_schema.py"
  python "$ROOT_DIR/scripts/sync_public_docs.py"
  python "$ROOT_DIR/scripts/generate_site_config.py"
  python "$ROOT_DIR/scripts/write_promotion_manifest.py"
else
  python "$ROOT_DIR/scripts/check_site_url.py" --from-examples
  python "$ROOT_DIR/scripts/validate_docs_metadata_schema.py" --from-examples
  python "$ROOT_DIR/scripts/sync_public_docs.py" --from-examples
  python "$ROOT_DIR/scripts/generate_site_config.py" --from-examples
fi
