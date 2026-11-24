#!/usr/bin/env python3
"""Regression checks for check-readiness.py, run against throwaway Git repositories."""
import pathlib
import subprocess
import sys
import tempfile

SCRIPT = pathlib.Path(__file__).resolve().parent / "check-readiness.py"
HEADER = "| Id | Gap | Severity | Decision | Owner | Date | Reason | Evidence or backlog reference |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n"
ROWS = {
    "RDY-01": "| RDY-01 | Audits not run | high | accepted | Owner | 2026-11-24 | Demo only | — |",
    "RDY-02": "| RDY-02 | Runbook unverified | medium | backlog | Owner | 2026-11-24 | No deployment | [Backlog](BACKLOG.md#later) |",
}


def record(rows: dict[str, str], move: str, intro: str = "Assessed on 2026-11-24.") -> str:
    return f"# Production readiness record\n\n{intro}\n\n## Gaps\n\n{HEADER}" + "\n".join(rows.values()) + f"\n\nMove decision: {move}\n"


GOOD_STATUS = "# Status\n\nReadiness: [record](readiness.md).\n\n## Blockers and open questions\n\n- RDY-01: audits not run.\n"


def run(steps: list[dict[str, str]], status: str = GOOD_STATUS) -> tuple[int, str]:
    """Commit each step's files in turn, then run the checker on the last state."""
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        git = lambda *a: subprocess.run(["git", "-C", tmp, *a], capture_output=True, text=True, check=True)
        git("init", "-q")
        (root / "docs").mkdir()
        (root / "AGENTS.md").write_text("## Governance\n\n- Profile: `MVP (since 2026-11-24)`.\n")
        (root / "docs" / "STATUS.md").write_text(status)
        for i, files in enumerate(steps):
            for name, text in files.items():
                (root / name).write_text(text.replace("{prev}", git("rev-parse", "--short", "HEAD").stdout.strip() if i else ""))
            git("add", "-A")
            git("-c", "user.name=t", "-c", "user.email=t@example.test", "commit", "-qm", f"step {i}")
        done = subprocess.run([sys.executable, str(SCRIPT), tmp], capture_output=True, text=True)
        return done.returncode, done.stdout


APPROVE = "approved by Owner on 2026-11-24 for the record at {prev}, covering RDY-01, RDY-02"
R = "docs/readiness.md"

CASES = [
    ("unchanged approved record meets the Move conditions",
     [{R: record(ROWS, "pending")}, {R: record(ROWS, APPROVE)}],
     0, ["Move decision: approved", "Move conditions: met"]),
    ("a row added after the approval makes it stale",
     [{R: record(ROWS, "pending")}, {R: record(ROWS, APPROVE)},
      {R: record({**ROWS, "RDY-03": "| RDY-03 | Assumption unconfirmed | medium | open | — | — | — | — |"}, "approved by Owner on 2026-11-24 for the record at {prev}, covering RDY-01, RDY-02")}],
     0, ["Move decision: stale", "rows in the record now but not covered: RDY-03", "rows added since", "Undecided: RDY-03"]),
    ("a decision changed after the approval makes it stale",
     [{R: record(ROWS, "pending")}, {R: record(ROWS, APPROVE)},
      {R: record({**ROWS, "RDY-02": ROWS["RDY-02"].replace("No deployment", "Changed reason")}, "approved by Owner on 2026-11-24 for the record at {prev}, covering RDY-01, RDY-02")}],
     0, ["Move decision: stale", "rows changed since"]),
    ("a change outside the gap rows keeps the approval",
     [{R: record(ROWS, "pending")}, {R: record(ROWS, APPROVE, intro="Assessed again on 2026-11-25; no new gaps.")}],
     0, ["Move decision: approved", "Move conditions: met"]),
    ("an open high gap blocks and is undecided",
     [{R: record({**ROWS, "RDY-01": "| RDY-01 | Audits not run | high | open | — | — | — | — |"}, "pending")}],
     0, ["Blocking: RDY-01", "Undecided: RDY-01", "Move conditions: not met"]),
    ("a high gap moved to the backlog still blocks",
     [{R: record({**ROWS, "RDY-01": "| RDY-01 | Audits not run | high | backlog | Owner | 2026-11-24 | Later | [Backlog](BACKLOG.md) |"}, "pending")}],
     0, ["Blocking: RDY-01"]),
    ("an unknown decision is an error",
     [{R: record({**ROWS, "RDY-02": ROWS["RDY-02"].replace("backlog", "deferred")}, "pending")}],
     1, ["error: RDY-02: unknown decision 'deferred'"]),
    ("a decision without an owner is an error",
     [{R: record({**ROWS, "RDY-01": ROWS["RDY-01"].replace("| Owner |", "| — |")}, "pending")}],
     1, ["error: RDY-01: decision accepted has no owner"]),
    ("an approval naming a missing commit is stale",
     [{R: record(ROWS, "approved by Owner on 2026-11-24 for the record at 0000000, covering RDY-01, RDY-02")}],
     0, ["Move decision: stale", "approved commit 0000000 not found"]),
    ("STATUS without a link, saying no blockers and naming only RDY-010, is reported",
     [{R: record({**ROWS, "RDY-01": "| RDY-01 | Audits not run | high | open | — | — | — | — |"}, "pending")}],
     0, ["warning: docs/STATUS.md has no Markdown link to docs/readiness.md", "blockers section does not name RDY-01"],
     "# Status\n\nBlockers: none.\n\nSee readiness.md for the record.\n\n## History\n\n- RDY-010 archived on 2026-11-20.\n"),
    ("a removed row with covering edited to match keeps the approval stale",
     [{R: record(ROWS, "pending")},
      {R: record({"RDY-01": ROWS["RDY-01"]}, "approved by Owner on 2026-11-24 for the record at {prev}, covering RDY-01")}],
     0, ["Move decision: stale", "removed since", "in ", "but not covered: RDY-02", "Move conditions: not met"]),
    ("an empty gap table approved as covering none meets the Move conditions",
     [{R: record({}, "pending")}, {R: record({}, "approved by Owner on 2026-11-24 for the record at {prev}, covering none")}],
     0, ["Gaps: 0 (none)", "Move decision: approved", "Move conditions: met"]),
    ("a missing Move decision line is an error",
     [{R: record(ROWS, "pending").replace("Move decision: pending\n", "")}],
     1, ["error: no Move decision line", "Move conditions: not met"]),
    ("an unreadable Move decision is an error",
     [{R: record(ROWS, "yes")}],
     1, ["error: Move decision line not in the guide's format: 'Move decision: yes'", "Move conditions: not met"]),
    ("no record exits 2",
     [{"docs/other.md": "nothing"}],
     2, ["No docs/readiness.md"]),
]


def main() -> int:
    failures = 0
    for case in CASES:
        title, steps, code, expected = case[:4]
        got_code, out = run(steps, case[4] if len(case) > 4 else GOOD_STATUS)
        missing = [e for e in expected if e not in out]
        ok = got_code == code and not missing
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {title}")
        if not ok:
            print(f"  exit {got_code} (expected {code}); missing {missing}\n" + "\n".join("  | " + l for l in out.splitlines()))
    print(f"{len(CASES) - failures} of {len(CASES)} readiness-check cases passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
