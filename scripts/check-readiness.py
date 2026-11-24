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
- whether the approval names a commit that exists, covers exactly the current
  rows, and none of those rows differs from that commit;
- whether docs/STATUS.md links the record and names every blocker.

It changes nothing. The guide's rules decide; this script only gathers the
mechanical facts. Exit status: 0 when the record is well formed, 1 when it has
errors, 2 when there is no record.
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


def check_approval(project: pathlib.Path, text: str, rows: dict[str, dict[str, str]]) -> tuple[str, list[str]]:
    """Return the approval state and the reasons it is not valid."""
    line = next((l for l in text.splitlines() if l.startswith("Move decision:")), None)
    if line is None:
        return "missing", ["no Move decision line"]
    if PENDING.match(line):
        return "pending", []
    match = APPROVED.match(line)
    if not match:
        return "unreadable", [f"Move decision line not in the guide's format: {line!r}"]
    reasons = []
    commit = match["commit"]
    covered = {i.strip() for i in match["ids"].replace(" and ", ",").split(",") if i.strip()}
    if covered != set(rows):
        missing, extra = sorted(set(rows) - covered), sorted(covered - set(rows))
        if missing:
            reasons.append(f"approval does not cover {', '.join(missing)}")
        if extra:
            reasons.append(f"approval covers rows that no longer exist: {', '.join(extra)}")
    shown = git(project, "show", f"{commit}:docs/readiness.md")
    if shown.returncode != 0:
        reasons.append(f"approved commit {commit} not found, or it has no docs/readiness.md")
    else:
        then, _ = gap_rows(shown.stdout)
        changed = sorted(rid for rid in rows if rid in then and then[rid] != rows[rid])
        added = sorted(rid for rid in rows if rid not in then)
        if changed:
            reasons.append(f"rows changed since {commit}: {', '.join(changed)}")
        if added:
            reasons.append(f"rows added since {commit}: {', '.join(added)}")
    return ("approved" if not reasons else "stale"), reasons


def check_status(project: pathlib.Path, blocking: list[str]) -> list[str]:
    path = project / "docs" / "STATUS.md"
    if not path.exists():
        return ["docs/STATUS.md is missing"]
    text = path.read_text()
    warnings = []
    if "readiness.md" not in text:
        warnings.append("docs/STATUS.md does not link docs/readiness.md")
    missing = [rid for rid in blocking if rid not in text]
    if missing:
        warnings.append(f"docs/STATUS.md does not name blocking gaps {', '.join(missing)}")
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
    approval, stale = check_approval(project, text, rows)
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
