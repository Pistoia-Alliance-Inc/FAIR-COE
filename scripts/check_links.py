import re
from common import ROOT

LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*$', re.MULTILINE)
EXPLICIT_ANCHOR_RE = re.compile(r'\[\]\(\)\{\s*#([A-Za-z0-9_-]+)\s*\}')

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[`*_~]', '', text)
    text = re.sub(r'[^a-z0-9\s_-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text

_anchor_cache = {}
def anchors_for(md):
    if md in _anchor_cache:
        return _anchor_cache[md]
    text = md.read_text(encoding="utf-8")
    anchors = set(m.group(1) for m in EXPLICIT_ANCHOR_RE.finditer(text))
    anchors.update(slugify(m.group(2)) for m in HEADING_RE.finditer(text))
    _anchor_cache[md] = anchors
    return anchors

def main():
    messages = []
    for md in (ROOT / "docs").rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                anchor = target[1:]
                if anchor and anchor not in anchors_for(md):
                    messages.append(f"{md.relative_to(ROOT)} -> missing local anchor #{anchor}")
                continue
            file_part, anchor = (target.split("#", 1) + [""])[:2]
            if not file_part.endswith(".md"):
                continue
            resolved = (md.parent / file_part).resolve()
            if not resolved.exists():
                messages.append(f"{md.relative_to(ROOT)} -> missing {file_part}")
                continue
            if anchor and anchor not in anchors_for(resolved):
                messages.append(f"{md.relative_to(ROOT)} -> missing anchor #{anchor} in {resolved.relative_to(ROOT)}")
    if messages:
        print("Link validation information:")
        for message in messages:
            print(f" - {message}")
        return
    print("Link and anchor validation passed.")

if __name__ == "__main__":
    main()
