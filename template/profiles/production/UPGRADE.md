# Upgrade an MVP project to Production

An agent runs this in the project, on the owner's request. The upgrade adds to what exists: code, tests, Git history, decisions, the assumptions register and project-specific configuration stay. It is safe to run again, because every step says how to tell that its result is already there.

Moving to Production is the owner's decision. This guide gives that decision evidence: a gap list from the project's own documents, and a readiness review from the AI Audit Toolkit.

Give the agent this prompt:

```text
Assess this MVP project for the Production profile. Follow
<absolute path to ai-starter-pack>/template/profiles/production/UPGRADE.md.
Start with the preview and change nothing until I approve it.
```

## 1. Preview

Change nothing in this step: no file, no audit report, no setting.

1. Read the project's `AGENTS.md`, `docs/SPEC.md`, `docs/assumptions.md`, `docs/runbook.md`, `docs/STATUS.md`, the backlog, `docs/decisions/`, any `docs/audits/` reports, the CI workflows and `git status`. Read this profile's [README](README.md), [AGENTS section](AGENTS-section.md) and the [MVP section](../mvp/AGENTS-section.md) it replaces. If the working tree has uncommitted changes, stop and ask: the upgrade starts from a clean, committed state. Report the branch and revision; if it is not the default branch, for example an unmerged feature branch, ask which base the upgrade starts from. Read the backlog where it lives, through the queue's tools when it is outside the repository, or report that it was not reviewed.
2. Note the pack revision (`git -C <pack> rev-parse --short HEAD`) and whether the pack has uncommitted changes.
3. **Profile.** Report what the Governance section says. A project without one predates profiles and counts as Production by default. If the owner says it is really an MVP, compare it with the MVP section as well and list which MVP mechanisms it already has under other names. Its rules may sit under the earlier headings instead of an MVP section; step 5 handles both layouts.
4. **Readiness signals.** Report which of these the project shows, with evidence: paying or depended-on users, personal data at scale, a second regular contributor, availability commitments, real deployments. Report the risk triggers in the core that apply now, and whether their controls exist.
5. For each step in Apply, report one of:
   - **present**: its check below is already true, so the step will be skipped;
   - **gap**: what is missing, the evidence, and what the step would add or require;
   - **owner decision**: a choice the step needs.
6. List the MVP rules the Production section replaces and the project values carried over. Nothing project-specific may be deleted; say where each piece goes.
7. If the project's core `AGENTS.md` sections differ from the pack's current `template/core/AGENTS.md`, list the differences. Updating them is a separate owner decision, not part of this upgrade, except for the Governance section, which step 4 adds because the profile has to be recorded.
8. Collect the owner's decisions in one list:
   - whether to run the readiness review now (it writes only reports);
   - whether agent merges, if the MVP rule allowed them, continue as an explicit override;
   - whether to adopt milestones now;
   - for each gap, whether it blocks the move, is accepted with a reason, or goes to the backlog.
9. Wait for the owner's approval and decisions. The preview alone is the gap list; nothing is decided by it.

## 2. Apply

Each step names its check. When the check is already true, skip the step. Never overwrite an existing file; merge into it.

1. **Readiness review.** Run `audit-production` and `audit-security` from the [AI Audit Toolkit](https://github.com/Phunkhouse/ai-audit-toolkit), following its installation and invocation rules. Before running them, create `docs/audits/context.md` from the toolkit's `templates/project-context.md` if it is missing, and add under "Known limitations and intentional decisions" the line `Governance profile: <current profile>, assessed for Production on YYYY-MM-DD`, so the audits know the question. The audits write only their reports under `docs/audits/`. If a skill is missing, report that instead of simulating it. _Present when_ both reports exist for a revision no older than the last change to deployment, data handling or sign-in.
2. **Gap decisions.** Merge the preview's gaps with the audits' findings into one list in the readiness report's follow-up or `docs/STATUS.md`. For each, record the owner's decision: blocks the move, accepted with a reason and date, or moved to the backlog with an id. Do not fix findings in this upgrade; fixes are separate, focused changes. _Present when_ every gap and every finding rated high or critical has a recorded decision.
3. **Blockers resolved.** Stop here while any blocker is open; report which, and resume this guide after they are fixed. _Present when_ no gap or finding is recorded as blocking.
4. **Governance.** Profile `Production (since YYYY-MM-DD)` with the pack revision. Keep the project's history, such as "MVP since …", when it is known; for a project that predates profiles, say so instead. Record approved overrides, such as agent merges, with their reason. _Present when_ the Governance line says Production.
5. **Profile section.** Make `AGENTS.md` contain every rule of the Production [AGENTS section](AGENTS-section.md). If it has an MVP section, replace it with the Production section. If its rules sit under earlier headings, as in a project that predates profiles, keep that layout unless the owner asks for a restructure, and add only the Production rules it lacks. Carry over:
   - the CI strategy: for Standard, keep the Production section's CI line as it is; for Budget-conscious, replace that line with the CI strategy recipe's [AGENTS snippet](../../../recipes/ci-strategy/AGENTS-section.md), as that recipe says, instead of keeping both;
   - the assumptions register, backlog home and runbook, as items in a `## Project-specific rules` section, since the Production section does not name them;
   - the verify command, which stays in the Commands section;
   - other project-specific rules, such as CI runner routing or review commands, into `## Project-specific rules`.

   A project rule that contradicts a Production rule, such as merging documentation-only PRs without CI, is a gap for step 2: the owner records it as an override in Governance, or it ends. The MVP merge rule ends too: the owner merges, unless Governance records an override. _Present when_ `AGENTS.md` contains every Production rule, has no MVP section, and every contradicting project rule is a recorded override.
6. **Milestones.** If the owner adopts milestones, copy `template/optional/docs/MILESTONES.md` to `docs/MILESTONES.md` and fill it from the backlog's agreed stages, each with observable acceptance checks. If not, record that decision. _Present when_ `docs/MILESTONES.md` exists or the decision not to use it is recorded.
7. **Runbook.** Production needs every section verified, not "not applicable yet": deploy and rollback, secrets, backups with a restore drill and its date and result, monitoring and alerts, incidents. Fill what the project shows; list what is missing as gaps from step 2. Judge each section by meaning, not wording: "planned", "not yet", "to check" and anything without a date or evidence count as unverified. _Present when_ every section is verified, with a date or evidence, or has an accepted gap.
8. **CI and protection.** Confirm the CI strategy is implemented as the [CI strategy recipe](../../../recipes/ci-strategy/README.md) describes, and record the observed hosted CI result: state, revision and run link, or `not run` only when no hosted run has started. When the agent cannot see the hosted result, for example without access to the repository host, record "not observed" and treat it as a gap. Branch protection or rulesets requiring the CI checks are owner actions: list them, never perform them. _Present when_ every required check passed in a hosted run on the revision that is now the default branch's head, or on the PR that merged it, and the owner confirmed the required checks are enforced.
9. **Legal readiness.** If the project stores personal data or has real users, offer the [legal planning recipe](../../../recipes/legal-planning/README.md): Planning mode first if it has never run, then Pre-launch mode. Record the owner's answer. _Present when_ the answer is recorded or the project has neither trigger.
10. **Status and commit.** Run the verify command. Rewrite `docs/STATUS.md` with the upgrade's state, open gaps and owner actions, local verification, and hosted CI recorded separately. Commit as `chore: upgrade to the Production profile`, through a PR when the project has a remote. _Present when_ that commit exists (`git log --grep 'upgrade to the Production profile'`).

## 3. Confirm

Run the preview again. Every step must report **present**, apart from owner actions still pending and gaps the owner accepted. If anything else reports **gap**, the upgrade is incomplete or a step is not idempotent; report which.
