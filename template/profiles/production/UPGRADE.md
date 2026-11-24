# Upgrade an MVP project to Production

An agent runs this in the project, on the owner's request. The upgrade adds to what exists: code, tests, Git history, decisions, the assumptions register and project-specific configuration stay. It is safe to run again, because every step says how to tell that its result is already there.

It has three stages, each needing its own approval from the owner:

1. **Preview:** read-only. Approving it means only "run the readiness stage".
2. **Readiness:** the audits and the evidence checks write reports and a decision record. The profile stays MVP throughout.
3. **Move:** only after the owner explicitly approves the move, recorded with a date, and only while no gap blocks it. A gap **blocks** the move while it is critical or high and not `fixed` or `accepted`. Medium and low gaps do not block, but every gap needs a decision before the owner is asked about the move.

Give the agent this prompt:

```text
Assess this MVP project for the Production profile. Follow
<absolute path to ai-starter-pack>/template/profiles/production/UPGRADE.md.
Start with the preview and change nothing until I approve it.
```

## The readiness record

Decisions about gaps live in `docs/readiness.md`, a durable, shareable record that is committed with the project. `docs/STATUS.md` is rewritten at every handoff, so it only links the record and names the blockers open right now; it is never the place a decision is kept.

The record has one row per gap: **id**, a shareable description, **severity** (critical, high, medium or low, from the audit or the agent's assessment), **decision**, **owner**, **date**, **reason**, and **evidence or backlog reference**. Use the audit finding id (`PRD-`, `SEC-`) where a finding exists, otherwise `RDY-NN`. Until a row is decided, its owner, date and reason are `—`. When the owner lowers a severity, the reason says so, for example "lowered from high by David: no deployment yet". A separate list, **Checks verified without a gap**, records evidence checks that passed or do not apply, with their evidence.

Decisions and what each one means:

| Decision | Meaning | Resolves a critical or high gap? |
| --- | --- | --- |
| `open` | Not decided yet | No |
| `fixed` | Evidence shows it is fixed: a commit, test, run or document, linked | Yes |
| `accepted` | The owner explicitly accepts the risk, with name, date and reason. Where the project's rules or agreements forbid accepting a kind of risk, it must be fixed instead; where they say nothing, the owner's explicit, dated acceptance is enough | Yes |
| `backlog` | Deferred to a backlog item, with its reference | No: only medium and low gaps |

After the gap rows comes the **Move decision** line, followed by an **Approval history** list of earlier approvals: `pending`, or `approved by <owner> on <YYYY-MM-DD> for the record at <commit>, covering <ids>`. `<ids>` lists every gap id the owner reviewed, or `none` when the record has no gaps. `<commit>` is the commit of `docs/readiness.md` that the owner reviewed, so the record is committed before it is approved. An approval covers exactly that readiness state: the ids it lists, the ids in the record now and the ids in that commit must be the same set, and each row must be unchanged from that commit. Compare with `git diff <commit> -- docs/readiness.md`; changes to the Move decision line and the Approval history alone do not count.

- **What resets it:** a new gap, or a changed severity, decision or evidence on any row, makes that approval stale. Set the line back to `pending` and move the old line to the Approval history with the reason it went stale. Rows that did not change keep their decisions. Refreshing a recorded revision or date while the observed state stays the same is not a change.
- **What keeps it:** a rerun that finds the same rows unchanged.

The pack's `scripts/check-readiness.py` reports the record's mechanical state, read-only: run `python3 <pack>/scripts/check-readiness.py <project>`. It checks:
- format errors: rows with an unknown severity or decision, a decision missing its owner, date, reason or reference, and a missing or unreadable Move decision line;
- blocking and undecided gaps;
- whether the approval names an existing commit, and its covered ids, the current ids and that commit's ids are the same set with every row unchanged;
- whether `docs/STATUS.md` has a Markdown link to the record and names every blocking gap, by exact id, in its blockers section.

It reads only the record, so finding new gaps stays the preview's job, and its output is evidence: the rules in this guide decide.

Write shareable wording only. Audit reports themselves omit credentials and personal data and redact other sensitive details, such as exploit steps. Evidence that must be kept is stored redacted in the approved private location: as the AI Audit Toolkit's handling rules say, in a public repository `docs/audits/` stays private or ignored until the fixes are in place. The committed record refers to private findings by id only.

## 1. Preview

Change nothing in this step: no file, no audit report, no setting.

1. Read the project's `AGENTS.md`, `docs/SPEC.md`, `docs/assumptions.md`, `docs/runbook.md`, `docs/STATUS.md`, `docs/readiness.md` if it exists, the backlog, `docs/decisions/`, any `docs/audits/` reports, the CI workflows and `git status`. Read the backlog where it lives, through the queue's tools when it is outside the repository, or report that it was not reviewed. Read this profile's [README](README.md), [AGENTS section](AGENTS-section.md) and the [MVP section](../mvp/AGENTS-section.md) it replaces.
2. If the working tree has uncommitted changes, stop and ask: the upgrade starts from a clean, committed state. Report the branch and revision; if it is not the default branch, for example an unmerged feature branch, ask which base to start from. Note the pack revision (`git -C <pack> rev-parse --short HEAD`) and whether the pack has uncommitted changes.
3. **Profile.** Report what the Governance section says. A project without one predates profiles and counts as Production by default. If the owner says it is really an MVP, compare it with the MVP section as well and list which MVP mechanisms it already has under other names.
4. **Readiness signals.** Report which of these the project shows, with evidence: paying or depended-on users, personal data at scale, a second regular contributor, availability commitments, real deployments. Report the core risk triggers that apply now and whether their controls exist.
5. **Gap list.** If `docs/readiness.md` exists, start from its rows and their decisions; never reopen a recorded decision without new evidence. Add the gaps this preview finds, numbered `RDY-NN` after the last existing one. For each Readiness and Move step, report **present** (its check is already true), **gap** or **owner decision**.
6. List the MVP rules the Production section would replace and where each project value would go. Nothing project-specific may be deleted.
7. If the project's core `AGENTS.md` sections differ from the pack's current `template/core/AGENTS.md`, list the differences. Updating them is a separate owner decision, except the Governance section, which the Move stage needs.
8. Ask the owner two questions: run the readiness stage, and run the audits within it? Both approve reports and the record only, not the move. In Confirm, skip this step.

## 2. Readiness

The profile stays MVP during this whole stage. Each step names its check; skip it when the check is already true.

1. **Audits.** Run `audit-production` and `audit-security` from the [AI Audit Toolkit](https://github.com/Phunkhouse/ai-audit-toolkit), following its installation, invocation and handling rules. Before running them, create `docs/audits/context.md` from the toolkit's `templates/project-context.md` if it is missing, and add under "Known limitations and intentional decisions" the line `Governance profile: <current profile>, assessed for Production on YYYY-MM-DD`. If a skill is missing, or the owner does not approve running it, record the review as an open gap instead of simulating it. _Present when_ both reports exist for a revision no older than the last change to deployment, data handling or sign-in, or the record holds the missing review as a gap.
2. **Evidence checks.** Each of these becomes a row in the record until its evidence exists. These are Production's gates, so their gaps count as high unless the owner records a lower severity with a reason:
   - **Runbook:** deploy and rollback, secrets, backups with a restore drill and its date and result, monitoring and alerts, incidents. Judge by meaning, not wording: "planned", "not yet", "to check" and anything without a date or evidence count as unverified.
   - **Hosted CI:** every required check passed in a hosted run on the default branch's head, or on the PR that merged it. Record the state, revision and run link. Use `not run` only when no hosted run has started, and "not observed" when the agent cannot see the result.
   - **Branch protection:** the owner confirms that the required checks are enforced. This is an owner action; never change the setting.
   - **Legal readiness**, when the project stores personal data or has real users: the [legal planning recipe](../../../recipes/legal-planning/README.md), with Planning first if it never ran, then Pre-launch.

   _Present when_ each item is verified with evidence or has a row in the record.
3. **Record.** Create or update `docs/readiness.md` with every gap from the preview, the audits and the evidence checks. Keep existing rows and their decisions; add only new ones. Set `Move decision: pending` if the line is missing. If this changes the readiness state an approval covers, reset the approval as [the readiness record](#the-readiness-record) describes. _Present when_ every known gap has a row, and the Move decision is `pending` or covers exactly the current rows.
4. **Owner decisions.** Present the record to the owner and record each decision with owner, date and reason. Critical and high gaps resolve only as `fixed` with linked evidence, or `accepted` by the owner explicitly, with a date, where the project's rules allow it; `backlog` does not resolve them. Fixes are separate, focused changes outside this guide. _Present when_ every row has a decision other than `open`.
5. **Readiness decision.** Stop while any critical or high gap is `open` or `backlog`, or while any other gap is still `open`. Report the blockers and the undecided gaps, rewrite `docs/STATUS.md` with a link to the record and both lists, and end. When nothing blocks and every row is decided, ask the owner whether to move to Production on the basis of the current record, as its own question. Commit the record first, then record the answer on the Move decision line with the date, that commit and the ids it covers, and commit that line on its own before the Move stage, so the Move conditions are checked on a committed record. _Present when_ the Move decision line approves the current record.

## 3. Move

Run only when all of these hold, which `scripts/check-readiness.py` reports as "Move conditions: met"; otherwise the profile stays MVP:
- every current gap has a decision other than `open`;
- no critical or high gap is unresolved;
- the Move decision line approves the current record: it covers exactly the current rows, and none of them differs from the approved commit.

1. **Governance.** Profile `Production (since YYYY-MM-DD)` with the pack revision. Keep the project's history, such as "MVP since …", when it is known; for a project that predates profiles, say so instead. Record approved overrides, such as agent merges, with their reason, and link `docs/readiness.md`. _Present when_ the Governance line says Production.
2. **Profile section.** Make `AGENTS.md` contain every rule of the Production [AGENTS section](AGENTS-section.md). If it has an MVP section, replace it with the Production section. If its rules sit under earlier headings, as in a project that predates profiles, keep that layout unless the owner asks for a restructure, and add only the Production rules it lacks. Carry over:
   - the CI strategy: for Standard, keep the Production section's CI line as it is; for Budget-conscious, replace that line with the CI strategy recipe's [AGENTS snippet](../../../recipes/ci-strategy/AGENTS-section.md), as that recipe says, instead of keeping both;
   - the assumptions register, backlog home, runbook and readiness record, as items in a `## Project-specific rules` section, since the Production section does not name them;
   - the verify command, which stays in the Commands section;
   - other project-specific rules, such as CI runner routing or review commands, into `## Project-specific rules`.

   A project rule that contradicts a Production rule, such as merging documentation-only PRs without CI, must already be a row in the record, resolved as an override the owner accepted; otherwise it ends. The MVP merge rule ends too: the owner merges, unless Governance records an override. _Present when_ `AGENTS.md` contains every Production rule, has no MVP section, and every contradicting project rule is an accepted override in the record.
3. **Milestones.** If the owner adopts milestones, copy `template/optional/docs/MILESTONES.md` to `docs/MILESTONES.md` and fill it from the backlog's agreed stages, each with observable acceptance checks. If not, record that decision. _Present when_ `docs/MILESTONES.md` exists or the decision not to use it is recorded.
4. **Status and commit.** Run the verify command. Rewrite `docs/STATUS.md` with the move, a link to the record, open owner actions, local verification, and hosted CI recorded separately. Then commit and open the PR as the next section describes. _Present when_ the commit exists (`git log --grep 'upgrade to the Production profile'`).

## What goes into the commit and PR

Commit only approved project changes and shareable summaries:

- **Included:** `AGENTS.md`, `docs/readiness.md`, `docs/STATUS.md`, the backlog entries that `backlog` decisions point to, and the milestone, runbook or SPEC changes the owner approved.
- **Never included:** audit reports or anything else the AI Audit Toolkit's handling rules keep private. In a public repository that means `docs/audits/` while security findings are unresolved.

Before committing:
1. Run `git status` and `git diff --cached --name-only`, and remove anything outside the approved list from the commit.
2. Check the staged diff for credentials, personal data, exploitable details and internal-only links.

Before opening the PR, check its description the same way. It gives the decision summary and links the record, never the reports. Evidence that must be kept stays redacted in its approved private location.

Use `chore: upgrade to the Production profile` as the commit subject, through a PR when the project has a remote. A Readiness stage that stops at step 5 commits only `docs/readiness.md`, `docs/STATUS.md` and the backlog entries its decisions point to, under the same checks, as `docs: record Production readiness decisions`.

## 4. Confirm

Run the preview again, together with `scripts/check-readiness.py`. It reads decisions from `docs/readiness.md`, never from `docs/STATUS.md`, so a rewritten status cannot reopen an accepted gap or hide an open one.

- **When the move was approved:** every Readiness and Move step must report present, apart from owner actions still pending.
- **When the move is pending:** the profile must still be MVP, and the blockers that `docs/STATUS.md` names must match the record's blocking rows. A later handoff may have rewritten `STATUS.md`; report the mismatch and, with the owner's approval, restore the link to the record and the current blockers.

Report any difference as an incomplete or non-idempotent step.
