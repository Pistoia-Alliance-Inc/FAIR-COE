from common import ROOT, load_promotion
import json

def main():
    out_dir = ROOT / "site"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "promotion-manifest.json").write_text(json.dumps({"release_id": load_promotion().get("release_id")}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
