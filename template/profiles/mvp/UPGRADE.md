# Upgrade a Sprint project to MVP

An agent runs this in the project, on the owner's request. The upgrade adds to what exists: code, tests, Git history, decisions and project-specific configuration stay. It is safe to run again, because every step says how to tell that its result is already there.

Give the agent this prompt:

```text
Upgrade this Sprint project to the MVP profile. Follow
<absolute path to ai-starter-pack>/template/profiles/mvp/UPGRADE.md.
Start with the preview and change nothing until I approve it.
```

## 1. Preview

Change nothing in this step.

1. Read the project's `AGENTS.md` (Governance and the Sprint section), `docs/SPEC.md`, `docs/STATUS.md`, `README.md` and `git status`. Read this profile's [README](README.md), [AGENTS section](AGENTS-section.md) and templates. If the working tree has uncommitted changes, stop and ask: the upgrade starts from a clean, committed state.
2. Note the pack revision (`git -C <pack> rev-parse --short HEAD`). If the pack has uncommitted changes, say so; the owner decides whether to commit them first.
3. For each step in Apply, report one of:
   - **present**: its check below is already true, so the step will be skipped;
   - **to add**: what will be added or moved, from where to where, and why MVP needs it;
   - **owner decision**: a choice the step needs.
4. List the Sprint rules the MVP section replaces and the project values carried over. Nothing project-specific may be deleted; say where each piece goes.
5. If the project's core `AGENTS.md` sections differ from the pack's current `template/core/AGENTS.md`, list the differences. Updating them is a separate owner decision, not part of this upgrade.
6. Collect the owner's decisions in one list:
   - the backlog's home: `docs/BACKLOG.md`, the Vikunja queue or GitHub issues;
   - the CI strategy, Standard or Budget-conscious, and the merge rule;
   - whether open acceptance criteria stay as current scope or become backlog items;
   - which Sprint decisions deserve a decision record;
   - whether to set up what the MVP README offers: scalability and cost planning, legal planning, Claude PR review.
7. Wait for the owner's approval and decisions.

## 2. Apply

Each step names its check. When the check is already true, skip the step. Never overwrite an existing file; merge into it.

1. **Governance.** Profile `MVP (since YYYY-MM-DD)` with the pack revision, noting uncommitted pack changes if there were any. Keep where the project came from, such as "upgraded from Sprint, set up from pack `<old revision>`". Add `ci-strategy` to the recipes. _Present when_ the Governance line says MVP.
2. **Profile section.** Replace the Sprint section in `AGENTS.md` with the MVP [AGENTS section](AGENTS-section.md). Carry over the verify command. The CI line becomes the chosen strategy, because MVP requires CI even when the Sprint had none; the deploy note moves to the runbook. Fill in the backlog home and merge rule. Update the Commands section so its description of the verify command matches `package.json`. Keep project lines the owner wants from the Sprint section, such as how AI use is recorded, in a `## Project-specific rules` section after the MVP section. _Present when_ `AGENTS.md` has the MVP section and no Sprint section.
3. **Templates.** Copy what is missing, without overwriting:

   ```sh
   rsync -a --ignore-existing <pack>/template/profiles/production/files/ ./
   rsync -a --ignore-existing <pack>/template/profiles/mvp/files/ ./
   ```

   `README.md` and `docs/SPEC.md` already exist, so these copies skip them. _Present when_ `docs/decisions/`, `docs/design/`, `docs/assumptions.md` and `docs/runbook.md` exist.
4. **Assumptions register.** Replace the register template's placeholder rows with the SPEC's "Facts and assumptions" table: `confirmed` rows under Confirmed with their source and date, `assumption` rows under Open. Keep each row's reason in its text. "Depends on it" names the criteria, rules or tests that rely on it when the project shows them; "How it gets confirmed" comes from the SPEC or is marked for the owner. Keep statuses as they are; moving a row never confirms it. Replace the SPEC table with a link to the register. _Present when_ the SPEC has no facts table and the register has no placeholder rows.
5. **Specification.** Keep the Sprint SPEC's content and change its opening line from "this sprint" to "this product". Add only those Production SPEC sections whose content the SPEC does not already cover, such as purpose and users, data and trust boundaries, technical approach, and known limitations. Fill them from what the project shows, with unknowns as open questions; where a Sprint section already covers one, such as scope or workflows, link to it instead of repeating it. Rename "Decision log" to "Sprint decision log" and keep it as history. Write decision records only for the decisions the owner picked. _Present when_ the SPEC has a "Sprint decision log" and a technical approach section.
6. **Backlog.** Move the SPEC's Deferred items, and any open criteria the owner moved, to the chosen backlog with their decision ids. For `docs/BACKLOG.md`, copy `template/optional/docs/BACKLOG.md` first if it is missing and replace its placeholder lines. Leave a link to the backlog in place of Deferred. _Present when_ the SPEC's Deferred section lists no items (a heading with only the link is fine) and every deferred item is in the backlog.
7. **Deadline.** The Sprint deadline becomes history: keep the line and add the outcome: met, missed, or superseded by this upgrade on its date if it has not passed. Remove no acceptance criteria. _Present when_ the deadline line has an outcome.
8. **Runbook.** Replace the runbook template's placeholders with what the project shows about environments, running and deploying, and "not applicable yet" where there is nothing, such as backups without data. Mark everything not verified as unverified. _Present when_ `docs/runbook.md` has no template placeholders.
9. **README.** If the README is still the Sprint template, write it from the SPEC: what the project is, how to run it, decisions and trade-offs, limitations and deferred work. Otherwise keep its content. In both cases add links to the specification, the assumptions register, decision records, the runbook and the backlog. _Present when_ the README has no template placeholders and links to all five.
10. **CI.** If the project has no CI workflow, add one following the [CI strategy recipe](../../../recipes/ci-strategy/README.md) for the chosen strategy: Standard uses the stack recipe's workflow, such as the Next.js recipe's `ci.yml`; Budget-conscious adapts the CI strategy recipe's example. If the project has no remote yet, the workflow cannot run and the MVP rule "independent CI before merge" cannot be met. List creating the repository with the Git remote alias, pushing, and branch protection as pending owner actions under "Blockers and open questions" in `docs/STATUS.md`. Never perform them. _Present when_ the workflow file exists. (`STATUS.md` is rewritten at every handoff, so it is not part of the check.)
11. **Offers.** Record the owner's answers on what the MVP README offers in the SPEC's open questions or the backlog. Set up only what the owner accepted, following its recipe. _Present when_ each offer has a recorded answer.
12. **Status and checks.** Run the verify command. Rewrite `docs/STATUS.md` with the upgrade's state, the pending owner actions, open register rows that still need a way to be confirmed, and what the verification covered. Verification runs before the commit exists, so record it as the base revision plus the upgrade's uncommitted changes. Commit everything as one change, `chore: upgrade to the MVP profile`, through a PR once the project has a remote. _Present when_ the upgrade commit exists (`git log --grep 'upgrade to the MVP profile'`).

## 3. Confirm

Run the preview again. Every step must report **present**, apart from owner actions still pending. If anything else reports **to add**, the upgrade is incomplete or a step is not idempotent; report which.
