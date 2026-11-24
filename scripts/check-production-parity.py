#!/usr/bin/env python3
"""Check that the Production profile keeps every rule from before profiles.

Composes template/core/AGENTS.md with template/profiles/production/AGENTS-section.md
and requires every sentence of the baseline (scripts/fixtures/agents-before-profiles.md,
the core AGENTS.md at abff43f) to appear in it word for word. Markdown line
wrapping inside a list item is ignored: an item's continuation lines are joined
and runs of whitespace become one space before comparing. Nothing else about
the wording is relaxed.

The only exceptions are the sentences of the old one-line document map, listed
in REWORDED. Each must still be found in its new home: the core's source map
(the "Sources of truth" item that starts with `README.md`) or the Production
"Further sources of truth" item. A path mentioned anywhere else does not count.

Run with --self-test to confirm the check fails when a rule or a map pointer is
lost, and passes when a rule is only re-wrapped.
"""
import pathlib
import re
import sys

BASELINE = pathlib.Path("scripts/fixtures/agents-before-profiles.md")
CORE = pathlib.Path("template/core/AGENTS.md")
PRODUCTION = pathlib.Path("template/profiles/production/AGENTS-section.md")

CORE_MAP = "core source map"
PRODUCTION_MAP = "Production further sources"
MAP_STARTS = {CORE_MAP: "`README.md`:", PRODUCTION_MAP: "Further sources of truth:"}

REWORDED = {
    "Project overview: `README.md`.": (CORE_MAP, "`README.md`"),
    "Detailed scope, workflows, limitations and open questions: `docs/SPEC.md`.": (CORE_MAP, "`docs/SPEC.md`"),
    "Approved design: `docs/design/`.": (PRODUCTION_MAP, "`docs/design/`"),
    "Agreed development stages, when present: `docs/MILESTONES.md`.": (PRODUCTION_MAP, "`docs/MILESTONES.md`"),
    "Decision records: `docs/decisions/`.": (PRODUCTION_MAP, "`docs/decisions/`"),
}


def items(text: str) -> list[str]:
    """List items and paragraphs, each with its wrapped lines joined."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    found: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        starts_new = not stripped or stripped.startswith(("#", "- ", "|"))
        if starts_new and current:
            found.append(" ".join(current))
            current = []
        if not stripped or stripped.startswith(("#", "|")):
            continue
        current.append(stripped.removeprefix("- ").strip())
    if current:
        found.append(" ".join(current))
    return [re.sub(r"\s+", " ", item) for item in found]


def sentences(text: str) -> list[str]:
    found = []
    for item in items(text):
        for part in re.split(r"(?<=[.;])\s+(?=[A-Z`(])", item):
            if len(part.strip()) > 3:
                found.append(part.strip())
    return found


def map_entries(composed: str) -> dict[str, str]:
    entries = {}
    for item in items(composed):
        for name, start in MAP_STARTS.items():
            if item.startswith(start) and name not in entries:
                entries[name] = item
    return entries


def problems(baseline: str, composed: str) -> list[str]:
    present = set(sentences(composed))
    entries = map_entries(composed)
    errors = [f"missing map entry: {name} (starts with {start})" for name, start in MAP_STARTS.items() if name not in entries]
    for sentence in sentences(baseline):
        if sentence in present:
            continue
        if sentence not in REWORDED:
            errors.append(f"missing rule: {sentence}")
            continue
        where, pointer = REWORDED[sentence]
        if where in entries and pointer not in entries[where]:
            errors.append(f"missing pointer {pointer} in the {where} (from: {sentence})")
    return errors


def self_test(baseline: str, composed: str) -> int:
    rule = "Leave the final merge to the user unless they explicitly ask you to perform it."
    wrapped = rule.replace(" unless ", "\n  unless ")
    further = next(i for i in composed.splitlines() if i.lstrip("- ").startswith(MAP_STARTS[PRODUCTION_MAP]))
    cases = [
        ("unchanged text passes", composed, True),
        ("a rule wrapped over two lines passes", composed.replace(rule, wrapped), True),
        ("a missing rule fails", composed.replace(f"- {rule}\n", ""), False),
        ("a missing rule fails while others are wrapped", composed.replace(f"- {rule}\n", "").replace("Keep the action block", "Keep the\n  action block"), False),
        ("a reworded rule fails", composed.replace(rule, rule.replace("final merge", "merge")), False),
        (
            "the design path changed in the map but kept in the UI rule fails",
            composed.replace(further, further.replace("`docs/design/`", "`docs/ui/`")),
            False,
        ),
    ]
    assert "Follow the approved design in `docs/design/`" in cases[-1][1], "the UI rule must keep docs/design/"
    failures = 0
    for title, text, should_pass in cases:
        found = problems(baseline, text)
        ok = (not found) if should_pass else bool(found)
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {title} ({len(found)} problems)")
    print(f"{len(cases) - failures} of {len(cases)} parity self-test cases passed.")
    return 1 if failures else 0


def main() -> int:
    baseline = BASELINE.read_text()
    composed = CORE.read_text() + "\n" + PRODUCTION.read_text()
    if "--self-test" in sys.argv:
        return self_test(baseline, composed)
    errors = problems(baseline, composed)
    for error in errors:
        print(error)
    total = len(sentences(baseline))
    print(f"Production parity: {total - len(errors)} of {total} baseline rules kept ({len(REWORDED)} map pointers checked in place).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
