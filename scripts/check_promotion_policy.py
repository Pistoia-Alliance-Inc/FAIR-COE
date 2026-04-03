import argparse
import re
import sys
from common import load_registry, promotion_map, is_bootstrap_mode

TAG_PATTERN = re.compile(r"^refs/tags/docs-public-v\d+\.\d+\.\d+$")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()
    bootstrap = is_bootstrap_mode() or args.from_examples
    promotions = promotion_map()
    errors = []
    warnings = []
    registry = load_registry()
    for r in registry:
        slug = r["slug"]
        required = bool(r.get("required", False))
        ref = promotions.get(slug)
        if not ref:
            (errors if required and not bootstrap else warnings).append(f"Missing promoted ref for slug: {slug}")
            continue
        if not TAG_PATTERN.match(ref):
            (errors if required and not bootstrap else warnings).append(f"Promoted ref does not match required tag pattern for {slug}: {ref}")
    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    print("Promotion policy validation passed.")

if __name__ == "__main__":
    main()
