#!/usr/bin/env python3
"""Check relative Markdown links and in-repo heading anchors.

External URLs are not fetched. A link in template/optional/ may point to a
file that lives in template/core/ once both are copied into a target project,
so those links also resolve against the matching template/core/ path.
"""
import pathlib
import re
import subprocess
import sys

LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
HEADING = re.compile(r"^#{1,6} +(.+?) *#*$", re.M)


def slug(heading: str) -> str:
    text = re.sub(r"[`*_\[\]]|\(.*?\)", "", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path: pathlib.Path) -> set[str]:
    return {slug(h) for h in HEADING.findall(FENCE.sub("", path.read_text()))}


def resolve(source: pathlib.Path, target: str) -> pathlib.Path | None:
    candidates = [source.parent / target]
    parts = source.parts
    if parts[:2] == ("template", "optional"):
        candidates.append(pathlib.Path("template", "core", *parts[2:]).parent / target)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def main() -> int:
    files = subprocess.run(
        ["git", "ls-files", "*.md"], capture_output=True, text=True, check=True
    ).stdout.split()
    errors = []
    for name in files:
        source = pathlib.Path(name)
        for url in LINK.findall(FENCE.sub("", source.read_text())):
            if re.match(r"^[a-z][a-z0-9+.-]*:", url):
                continue
            path, _, anchor = url.partition("#")
            target = resolve(source, path) if path else source
            if target is None:
                errors.append(f"{name}: missing file {url}")
            elif anchor and target.suffix == ".md" and anchor not in anchors(target):
                errors.append(f"{name}: missing anchor {url}")
    for error in errors:
        print(error)
    print(f"Checked {len(files)} Markdown files: {len(errors)} broken links.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
