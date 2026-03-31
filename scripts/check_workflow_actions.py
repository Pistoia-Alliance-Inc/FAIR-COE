from pathlib import Path
import re
import sys

WORKFLOWS_DIR = Path(__file__).resolve().parent.parent / ".github" / "workflows"
BANNED = {
    "actions/checkout@v4": "Use actions/checkout@v5",
    "actions/setup-python@v5": "Use actions/setup-python@v6",
    "actions/checkout@main": "Pin to actions/checkout@v5 or a commit SHA",
    "actions/setup-python@main": "Pin to actions/setup-python@v6 or a commit SHA",
}
RECOMMENDED = {
    "actions/checkout": "v5",
    "actions/setup-python": "v6",
    "actions/upload-pages-artifact": "v3",
    "actions/deploy-pages": "v4",
}
USES_RE = re.compile(r"uses:\s*([^\s#]+)")

def main():
    errors = []
    for wf in WORKFLOWS_DIR.glob("*.yml"):
        text = wf.read_text(encoding="utf-8")
        for banned, message in BANNED.items():
            if banned in text:
                errors.append(f"{wf.name}: banned action '{banned}'. {message}.")
        uses = USES_RE.findall(text)
        for item in uses:
            if item.startswith("./"):
                continue
            if item.count("@") != 1:
                errors.append(f"{wf.name}: malformed uses entry '{item}'.")
                continue
            action, version = item.split("@", 1)
            recommended = RECOMMENDED.get(action)
            if recommended is None:
                continue
            if re.fullmatch(r"[0-9a-fA-F]{40}", version):
                continue
            if version != recommended:
                errors.append(
                    f"{wf.name}: '{action}@{version}' is not approved. "
                    f"Use '{action}@{recommended}' or a 40-char commit SHA."
                )
        if "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true" not in text:
            errors.append(f"{wf.name}: missing FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true workflow guardrail.")
    if errors:
        print("Workflow action guardrail validation failed:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("Workflow action guardrail validation passed.")

if __name__ == "__main__":
    main()
