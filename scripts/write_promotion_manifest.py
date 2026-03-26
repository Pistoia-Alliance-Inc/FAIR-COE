from common import ROOT, load_promotion
import json

def main():
    audit_path = ROOT / ".cache" / "promotion-audit.json"
    promotion = load_promotion()
    out_dir = ROOT / "site"
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {"release_id": promotion.get("release_id"), "repositories": []}
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        payload["repositories"] = audit.get("repositories", [])
    (out_dir / "promotion-manifest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
