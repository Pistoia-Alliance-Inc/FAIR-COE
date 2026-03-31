import re
import sys
from common import load_registry, promotion_map

TAG_PATTERN = re.compile(r"^refs/tags/docs-public-v\d+\.\d+\.\d+$")

def main():
    registry = load_registry()
    promotions = promotion_map()
    errors = []
    for r in registry:
        slug = r["slug"]
        ref = promotions.get(slug)
        if not ref:
            errors.append(f"Missing promoted ref for slug: {slug}")
            continue
        if not TAG_PATTERN.match(ref):
            errors.append(f"Promoted ref does not match required tag pattern for {slug}: {ref}")
    extra = set(promotions.keys()) - {r["slug"] for r in registry}
    for slug in sorted(extra):
        errors.append(f"Promotion declared for unknown slug: {slug}")
    if errors:
        print("Promotion policy validation failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("Promotion policy validation passed.")

if __name__ == "__main__":
    main()
