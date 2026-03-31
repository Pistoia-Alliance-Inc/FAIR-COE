import re
import sys
import argparse
from common import load_registry, promotion_map, is_bootstrap_mode

TAG_PATTERN = re.compile(r"^refs/tags/docs-public-v\d+\.\d+\.\d+$")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()

    registry = load_registry()
    promotions = promotion_map()
    bootstrap = is_bootstrap_mode() or args.from_examples
    errors = []
    warnings = []

    for r in registry:
        slug = r["slug"]
        required = bool(r.get("required", False))
        ref = promotions.get(slug)

        if not ref:
            msg = f"Missing promoted ref for slug: {slug}"
            if required and not bootstrap:
                errors.append(msg)
            else:
                warnings.append(msg)
            continue

        if not TAG_PATTERN.match(ref):
            msg = f"Promoted ref does not match required tag pattern for {slug}: {ref}"
            if required and not bootstrap:
                errors.append(msg)
            else:
                warnings.append(msg)

    extra = set(promotions.keys()) - {r['slug'] for r in registry}
    for slug in sorted(extra):
        warnings.append(f"Promotion declared for unknown slug: {slug}")

    for w in warnings:
        print(f"WARNING: {w}")

    if errors:
        print("Promotion policy validation failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)

    print("Promotion policy validation passed.")

if __name__ == "__main__":
    main()
