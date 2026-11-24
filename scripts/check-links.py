#!/usr/bin/env python3
"""Check relative Markdown links and in-repo heading anchors.

External URLs are not fetched. template/core/, template/optional/ and each
template/profiles/<name>/files/ are copied into the same target project, so a
link inside one of them may point to a file from another. A profile's assembled
target is the core, optional, the profile's own files and the files of every
profile named in its `files-from` file (one name per line). Each file's links
must resolve in every assembled target that receives the file; a link that
works in only some of them is reported once per profile where it breaks.
"""
import pathlib
import re
import subprocess
import sys

LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
HEADING = re.compile(r"^#{1,6} +(.+?) *#*$", re.M)
SHARED = [pathlib.Path("template", "core"), pathlib.Path("template", "optional")]


def slug(heading: str) -> str:
    """GitHub-style anchor: link text kept, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path: pathlib.Path) -> set[str]:
    return {slug(h) for h in HEADING.findall(FENCE.sub("", path.read_text()))}


def profiles() -> list[pathlib.Path]:
    return sorted(pathlib.Path("template", "profiles").glob("*/files"))


def assembled() -> list[tuple[str, list[pathlib.Path]]]:
    """Every profile's assembled target: shared trees, its files and those of files-from."""
    result = []
    for files in profiles():
        roots = SHARED + [files]
        extra = files.parent / "files-from"
        if extra.exists():
            for name in extra.read_text().split():
                roots.append(pathlib.Path("template", "profiles", name, "files"))
        result.append((files.parent.name, roots))
    return result


def assemblies(source: pathlib.Path) -> tuple[pathlib.Path, list[tuple[str, list[pathlib.Path]]]] | None:
    """The template tree a file sits in, and every assembled target that receives it."""
    for tree in SHARED + profiles():
        if source.is_relative_to(tree):
            return tree, [(name, roots) for name, roots in assembled() if tree in roots]
    return None


def resolve_in(roots: list[pathlib.Path], inner: pathlib.Path) -> pathlib.Path | None:
    for root in roots:
        if (root / inner).exists():
            return root / inner
    return None


def check_link(name: str, source: pathlib.Path, url: str) -> list[str]:
    path, _, anchor = url.partition("#")
    if not path:
        targets = [(None, source)]
    else:
        direct = source.parent / path
        found = assemblies(source)
        if direct.exists() or found is None:
            targets = [(None, direct if direct.exists() else None)]
        else:
            tree, combos = found
            inner = source.relative_to(tree).parent / path
            targets = [(profile, resolve_in(roots, inner)) for profile, roots in combos]
    errors = []
    for profile, target in targets:
        where = f" (in the {profile} profile)" if profile else ""
        if target is None:
            errors.append(f"{name}: missing file {url}{where}")
        elif anchor and target.suffix == ".md" and anchor not in anchors(target):
            errors.append(f"{name}: missing anchor {url}{where}")
    return errors


def check(files: list[str]) -> list[str]:
    errors = []
    for name in files:
        source = pathlib.Path(name)
        for url in LINK.findall(FENCE.sub("", source.read_text())):
            if not re.match(r"^[a-z][a-z0-9+.-]*:", url):
                errors.extend(check_link(name, source, url))
    return errors


def main() -> int:
    files = subprocess.run(
        ["git", "ls-files", "*.md"], capture_output=True, text=True, check=True
    ).stdout.split()
    errors = check(files)
    for error in errors:
        print(error)
    print(f"Checked {len(files)} Markdown files: {len(errors)} broken links.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
