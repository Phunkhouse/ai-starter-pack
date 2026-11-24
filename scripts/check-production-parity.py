#!/usr/bin/env python3
"""Check that the Production profile keeps every rule from before profiles.

Composes template/core/AGENTS.md with template/profiles/production/AGENTS-section.md
and requires every sentence of the baseline (scripts/fixtures/agents-before-profiles.md,
the core AGENTS.md at abff43f) to appear in it word for word. The only exceptions
are listed in REWORDED: sentences whose content moved into new wording, each
with the pointers the composed text must still contain.

Run with --self-test to confirm the check fails when a rule or a pointer is lost.
"""
import pathlib
import re
import sys

BASELINE = pathlib.Path("scripts/fixtures/agents-before-profiles.md")
CORE = pathlib.Path("template/core/AGENTS.md")
PRODUCTION = pathlib.Path("template/profiles/production/AGENTS-section.md")

# The old one-line document map, split between the core map and the
# Production "further sources" line.
REWORDED = {
    "Project overview: `README.md`.": ["`README.md`"],
    "Detailed scope, workflows, limitations and open questions: `docs/SPEC.md`.": ["`docs/SPEC.md`"],
    "Approved design: `docs/design/`.": ["`docs/design/`"],
    "Agreed development stages, when present: `docs/MILESTONES.md`.": ["`docs/MILESTONES.md`"],
    "Decision records: `docs/decisions/`.": ["`docs/decisions/`"],
}


def sentences(text: str) -> list[str]:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^#.*$", "", text, flags=re.M)
    found = []
    for line in text.splitlines():
        line = line.strip().removeprefix("- ").strip()
        for part in re.split(r"(?<=[.;])\s+(?=[A-Z`(])", line):
            if len(part.strip()) > 3:
                found.append(part.strip())
    return found


def problems(baseline: str, composed: str) -> list[str]:
    present = set(sentences(composed))
    errors = []
    for sentence in sentences(baseline):
        if sentence in present:
            continue
        pointers = REWORDED.get(sentence)
        if pointers is None:
            errors.append(f"missing rule: {sentence}")
        else:
            errors.extend(f"missing pointer {p} (from: {sentence})" for p in pointers if p not in composed)
    return errors


def self_test(baseline: str, composed: str) -> int:
    rule = "Leave the final merge to the user unless they explicitly ask you to perform it."
    cases = [
        ("unchanged text passes", composed, 0),
        ("a dropped rule fails", composed.replace(rule, ""), 1),
        ("a lost pointer fails", composed.replace("`docs/decisions/`", "`docs/adr/`"), 1),
    ]
    failures = 0
    for title, text, expected in cases:
        got = len(problems(baseline, text))
        ok = (got == 0) if expected == 0 else (got > 0)
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {title} ({got} problems)")
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
    print(f"Production parity: {total - len(errors)} of {total} baseline rules kept ({len(REWORDED)} reworded pointers checked).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
