import argparse
import sys
from common import ROOT

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-examples", action="store_true")
    parser.parse_args()
    errors = []
    if not (ROOT / "docs" / "index.md").exists():
        errors.append("Missing docs/index.md")
    if not (ROOT / "mkdocs.generated.yml").exists():
        errors.append("Missing mkdocs.generated.yml")
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    print("Contract validation passed.")

if __name__ == "__main__":
    main()
