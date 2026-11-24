#!/usr/bin/env python3
"""Check a project's Production readiness record. Read-only.

Usage: python3 check-readiness.py [project directory]

Reads the Governance profile from AGENTS.md, the gap rows and Move decision
from docs/readiness.md, and the blockers in docs/STATUS.md, then reports what
the Production upgrade guide (template/profiles/production/UPGRADE.md) needs
to know:

- rows with an unknown severity or decision, or a decision missing its owner,
  date, reason or reference;
- gaps that block the move (critical or high, not fixed or accepted) and gaps
  still open;
- whether the approval names a commit that exists, and the ids it covers, the
  current ids and the ids in that commit are the same set, with every row
  unchanged (`covering none` is the empty set);
- whether docs/STATUS.md has a Markdown link to the record and names every
  blocking gap, by exact id, in its blockers section.

It changes nothing. The guide's rules decide; this script only gathers the
mechanical facts. Exit status: 0 when the record is well formed, even if the
Move conditions are not met; 1 when it has errors, including a missing or
unreadable Move decision line; 2 when there is no record.
"""
import pathlib
import re
import subprocess
import sys

SEVERITIES = {"critical", "high", "medium", "low"}
DECISIONS = {"open", "fixed", "accepted", "backlog"}
EMPTY = {"", "—", "-", "–"}
APPROVED = re.compile(
    r"^Move decision:\s*approved by (?P<owner>.+?) on (?P<date>\d{4}-\d{2}-\d{2}) "
    r"for the record at (?P<commit>[0-9a-f]{7,40}), covering (?P<ids>.+?)\s*$"
)
PENDING = re.compile(r"^Move decision:\s*pending\s*$")
PROFILE = re.compile(r"Profile:\s*`?(Sprint|MVP|Production)\b")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def gap_rows(text: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Rows of the first table whose header starts with Id, keyed by id."""
    rows: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    header: list[str] | None = None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            if header is not None and rows:
                break
            continue
        values = cells(line)
        if header is None:
            if values and values[0].lower() == "id":
                header = [v.lower() for v in values]
            continue
        if set(values[0]) <= set("-: "):
            continue
        row = dict(zip(header, values))
        rid = row.get("id", "")
        if rid in rows:
            errors.append(f"{rid}: listed twice")
        rows[rid] = row
    if header is None:
        errors.append("no gap table found (a table whose first column is Id)")
    return rows, errors


def field(row: dict[str, str], *names: str) -> str:
    for name in names:
        for key, value in row.items():
            if key.startswith(name):
                return value
    return ""


def check_rows(rows: dict[str, dict[str, str]]) -> tuple[list[str], list[str], list[str]]:
    errors, blocking, undecided = [], [], []
    for rid, row in rows.items():
        severity = field(row, "severity").lower()
        decision = field(row, "decision").lower().strip("`")
        if severity not in SEVERITIES:
            errors.append(f"{rid}: unknown severity {severity!r}")
        if decision not in DECISIONS:
            errors.append(f"{rid}: unknown decision {decision!r}")
            continue
        if decision == "open":
            undecided.append(rid)
        else:
            for name in ("owner", "date", "reason"):
                if field(row, name) in EMPTY:
                    errors.append(f"{rid}: decision {decision} has no {name}")
            if field(row, "date") not in EMPTY and not DATE.match(field(row, "date")):
                errors.append(f"{rid}: date {field(row, 'date')!r} is not YYYY-MM-DD")
        if decision in {"fixed", "backlog"} and field(row, "evidence") in EMPTY:
            errors.append(f"{rid}: decision {decision} has no evidence or backlog reference")
        if severity in {"critical", "high"} and decision in {"open", "backlog"}:
            blocking.append(rid)
    return errors, blocking, undecided


def git(project: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True)


def covered_ids(text: str) -> set[str]:
    text = text.strip()
    if text.lower() == "none":
        return set()
    return {i.strip() for i in text.replace(" and ", ",").split(",") if i.strip()}


def check_approval(project: pathlib.Path, text: str, rows: dict[str, dict[str, str]]) -> tuple[str, list[str], list[str]]:
    """Return the approval state, why it is stale, and format errors."""
    line = next((l for l in text.splitlines() if l.startswith("Move decision:")), None)
    if line is None:
        return "missing", [], ["no Move decision line"]
    if PENDING.match(line):
        return "pending", [], []
    match = APPROVED.match(line)
    if not match:
        return "unreadable", [], [f"Move decision line not in the guide's format: {line!r}"]
    reasons = []
    commit = match["commit"]
    covered, current = covered_ids(match["ids"]), set(rows)
    shown = git(project, "show", f"{commit}:docs/readiness.md")
    if shown.returncode != 0:
        return "stale", [f"approved commit {commit} not found, or it has no docs/readiness.md"], []
    then, then_errors = gap_rows(shown.stdout)
    if then_errors:
        # The owner approved something that is not a readable record; it cannot cover the current one.
        return "stale", [f"docs/readiness.md at {commit} cannot be read as a record: {e}" for e in then_errors], []
    approved = set(then)
    for label, ids in (
        ("covered but not in the record now", covered - current),
        ("in the record now but not covered", current - covered),
        (f"covered but not in {commit}", covered - approved),
        (f"in {commit} but not covered", approved - covered),
        (f"added since {commit}", current - approved),
        (f"removed since {commit}", approved - current),
    ):
        if ids:
            reasons.append(f"rows {label}: {', '.join(sorted(ids))}")
    changed = sorted(rid for rid in current & approved if then[rid] != rows[rid])
    if changed:
        reasons.append(f"rows changed since {commit}: {', '.join(changed)}")
    return ("approved" if not reasons else "stale"), reasons, []


LINK = re.compile(r"\[[^\]]*\]\([^)\s]*readiness\.md(?:#[^)\s]*)?\)")


def blockers_section(text: str) -> str:
    """The current blockers: the section under a heading that names blockers, or a "Blockers:" line."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s.*\bblockers?\b", line, re.I):
            body = []
            for following in lines[i + 1:]:
                if re.match(r"^#{1,6}\s", following):
                    break
                body.append(following)
            return "\n".join(body)
    return "\n".join(l for l in lines if re.match(r"^\s*[-*]?\s*\**blockers?\**\s*:", l, re.I))


def check_status(project: pathlib.Path, blocking: list[str]) -> list[str]:
    path = project / "docs" / "STATUS.md"
    if not path.exists():
        return ["docs/STATUS.md is missing"]
    text = path.read_text()
    warnings = []
    if not LINK.search(text):
        warnings.append("docs/STATUS.md has no Markdown link to docs/readiness.md")
    section = blockers_section(text)
    if blocking and not section:
        warnings.append("docs/STATUS.md has no blockers section")
    missing = [rid for rid in blocking if not re.search(rf"(?<![\w-]){re.escape(rid)}(?![\w-])", section)]
    if missing:
        warnings.append(f"docs/STATUS.md blockers section does not name {', '.join(missing)}")
    return warnings


def main() -> int:
    project = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    record = project / "docs" / "readiness.md"
    agents = project / "AGENTS.md"
    profile_match = PROFILE.search(agents.read_text()) if agents.exists() else None
    profile = profile_match[1] if profile_match else "none declared (counts as Production)"
    print(f"Project: {project}")
    print(f"Profile: {profile}")
    if not record.exists():
        print("No docs/readiness.md: no Production readiness assessment recorded.")
        return 2
    text = record.read_text()
    rows, errors = gap_rows(text)
    row_errors, blocking, undecided = check_rows(rows)
    errors += row_errors
    approval, stale, format_errors = check_approval(project, text, rows)
    errors += format_errors
    warnings = check_status(project, blocking)

    print(f"Gaps: {len(rows)} ({', '.join(rows) or 'none'})")
    print(f"Blocking: {', '.join(blocking) or 'none'}")
    print(f"Undecided: {', '.join(undecided) or 'none'}")
    print(f"Move decision: {approval}" + (f" ({'; '.join(stale)})" if stale else ""))
    allowed = not errors and not blocking and not undecided and approval == "approved"
    reasons = (
        (["record has errors"] if errors else [])
        + ([f"blocking: {', '.join(blocking)}"] if blocking else [])
        + ([f"undecided: {', '.join(undecided)}"] if undecided else [])
        + ([] if approval == "approved" else [f"approval {approval}"])
    )
    print("Move conditions: " + ("met" if allowed else "not met (" + "; ".join(reasons) + ")"))
    if profile == "Production" and not allowed:
        warnings.append("profile is Production but the Move conditions are not met now; check whether the record changed after the move")
    for error in errors:
        print(f"error: {error}")
    for warning in warnings:
        print(f"warning: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
