#!/usr/bin/env python3
"""Regression checks for check-links.py, run against small throwaway trees."""
import importlib.util
import os
import pathlib
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_links", HERE / "check-links.py")
check_links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_links)


def write(root: pathlib.Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def run(files: dict[str, str]) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        write(root, files)
        previous = os.getcwd()
        os.chdir(root)
        try:
            return check_links.check(sorted(n for n in files if n.endswith(".md")))
        finally:
            os.chdir(previous)


PROFILES = {
    "template/profiles/production/files/docs/decisions/README.md": "# Decisions\n",
    "template/profiles/production/files/docs/SPEC.md": "# Spec\n\n## Scope\n",
    "template/profiles/sprint/files/docs/SPEC.md": "# Spec\n\n## Goal\n",
}

CASES = [
    (
        "shared link to a Production-only file breaks only in Sprint",
        {"template/core/AGENTS.md": "[d](docs/decisions/README.md)\n"},
        ["template/core/AGENTS.md: missing file docs/decisions/README.md (in the sprint profile)"],
    ),
    (
        "shared link to a file every profile provides passes",
        {"template/core/AGENTS.md": "[s](docs/SPEC.md)\n"},
        [],
    ),
    (
        "shared anchor that exists only in one profile's file breaks in the other",
        {"template/core/AGENTS.md": "[s](docs/SPEC.md#goal)\n"},
        ["template/core/AGENTS.md: missing anchor docs/SPEC.md#goal (in the production profile)"],
    ),
    (
        "a profile file may link to its own profile's files",
        {"template/profiles/production/files/README.md": "[d](docs/decisions/README.md)\n"},
        [],
    ),
    (
        "a profile file may not link to another profile's files",
        {"template/profiles/sprint/files/README.md": "[d](docs/decisions/README.md)\n"},
        ["template/profiles/sprint/files/README.md: missing file docs/decisions/README.md (in the sprint profile)"],
    ),
    (
        "ordinary repository links are unchanged",
        {"README.md": "[ok](template/core/AGENTS.md) [bad](nope.md)\n", "template/core/AGENTS.md": "# A\n"},
        ["README.md: missing file nope.md"],
    ),
]


def main() -> int:
    failures = 0
    for title, files, expected in CASES:
        got = run({**PROFILES, **files})
        if got != expected:
            failures += 1
            print(f"FAIL {title}\n  expected {expected}\n  got      {got}")
        else:
            print(f"ok   {title}")
    print(f"{len(CASES) - failures} of {len(CASES)} link-check cases passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
