import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    args = parser.parse_args()

    site_url = os.environ.get("MKDOCS_SITE_URL", "").strip()

    if args.from_examples:
        if not site_url:
            print("Example mode: MKDOCS_SITE_URL not set; local default will be used.")
            return
        if not site_url.startswith(("http://", "https://")):
            print("Site URL validation failed:")
            print(f" - MKDOCS_SITE_URL must start with http:// or https://, got: {site_url}")
            sys.exit(1)
        if not site_url.endswith("/"):
            print("Site URL validation failed:")
            print(f" - MKDOCS_SITE_URL must end with '/', got: {site_url}")
            sys.exit(1)
        print("Site URL validation passed for example mode.")
        return

    errors = []
    if not site_url:
        errors.append("MKDOCS_SITE_URL must be set for non-example builds.")
    else:
        if not site_url.startswith(("http://", "https://")):
            errors.append(f"MKDOCS_SITE_URL must start with http:// or https://, got: {site_url}")
        if not site_url.endswith("/"):
            errors.append(f"MKDOCS_SITE_URL must end with '/', got: {site_url}")
        if "127.0.0.1" in site_url or "localhost" in site_url:
            errors.append(f"MKDOCS_SITE_URL must not be a local URL for deployed builds, got: {site_url}")
    if errors:
        print("Site URL validation failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("Site URL validation passed.")

if __name__ == "__main__":
    main()
