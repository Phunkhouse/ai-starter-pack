#!/usr/bin/env python3
"""Check relative Markdown links and in-repo heading anchors.

External URLs are not fetched. template/core/, template/optional/ and each
template/profiles/<name>/files/ are copied into the same target project, so a
link inside one of them may point to a file from another. A profile's files
resolve against the core, optional and that profile; core and optional files
resolve against any one profile.
"""
import pathlib
import re
import subprocess
import sys

LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
HEADING = re.compile(r"^#{1,6} +(.+?) *#*$", re.M)


def slug(heading: str) -> str:
    """GitHub-style anchor: link text kept, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path: pathlib.Path) -> set[str]:
    return {slug(h) for h in HEADING.findall(FENCE.sub("", path.read_text()))}


SHARED = [pathlib.Path("template", "core"), pathlib.Path("template", "optional")]
PROFILES = sorted(pathlib.Path("template", "profiles").glob("*/files"))


def target_trees(source: pathlib.Path) -> tuple[pathlib.Path, list[list[pathlib.Path]]] | None:
    """The tree a template file sits in, and the tree sets it is copied with."""
    for tree in SHARED + PROFILES:
        if source.is_relative_to(tree):
            if tree in PROFILES:
                return tree, [SHARED + [tree]]
            return tree, [SHARED + [profile] for profile in PROFILES]
    return None


def resolve(source: pathlib.Path, target: str) -> pathlib.Path | None:
    direct = source.parent / target
    if direct.exists():
        return direct
    found = target_trees(source)
    if found is None:
        return None
    tree, combinations = found
    inner = source.relative_to(tree).parent / target
    for combination in combinations:
        for root in combination:
            if (root / inner).exists():
                return root / inner
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
