# Prompt for starting a project with an agent

Copy this prompt into Claude Code or Codex while working in the **new target repository**. It sets up an MVP or Production project; for a time-boxed Sprint use the shorter prompt in the [Sprint profile](template/profiles/sprint/README.md#set-up) instead. Fill in the paths, a short description of the application and the recipe choices. The agent needs access to both locations. Recipe names are the directory names under `recipes/`; the [README's recipe table](README.md#recipes) says when each one fits.

```text
I am starting a new application: <one to three sentences about its purpose and users>.

The starter pack is at <absolute path to ai-starter-pack>.
The target repository is at <absolute path to the new repository>.
Its Git remote is <SSH URL with my host alias, e.g. git@github-work:owner/repo.git>.
The governance profile is <Production (default) or MVP>.
The stack recipe is <next-fullstack, or none>.
The optional recipes are <any of: claude-pr-review, discovery, playwright-e2e, seed-data, test-ci-review, ci-performance, self-hosted-runner, vercel-deployment-budget, vikunja-task-queue; or none>.
The CI strategy is <Standard (default) or Budget-conscious>.
Legal planning is <enabled or omitted>.
Scalability and cost planning is <offer (default), enabled or omitted>.
For MVP: the backlog lives in <docs/BACKLOG.md, the Vikunja queue or GitHub issues>, and merges are done by <me | the agent once CI passes and I have approved>.

1. Read
Read the starter pack README.md, template/core/, template/profiles/<profile>/ (for MVP also template/profiles/production/files/, named in its files-from), recipes/ci-strategy/README.md, recipes/scalability-planning/README.md and the README of every selected recipe (plus legal-planning when enabled). Follow each recipe's own conditions; where this prompt and a recipe differ, the recipe wins. Inspect the target repository and the documentation for the versions actually installed there.

2. Plan, then wait
Report a concise plan and wait for my approval before changing anything. Include:
- the files you would copy, and the files you would merge because the generator or project already has them (Next.js generates its own AGENTS.md: keep its nextjs-agent-rules block and add the pack's content below it);
- the files from template/core/, template/profiles/<profile>/files/ and, for MVP, template/profiles/production/files/, and the AGENTS.md composed from the core, the profile's AGENTS-section.md and each selected recipe's AGENTS-section.md;
- the risk triggers that apply and any overrides you propose for the Governance section;
- for MVP, the backlog location, CI strategy and merge rule you will write into the MVP section, and which of them I still need to choose;
- package scripts and dependencies you would add;
- the CI plan: current provider, triggers, required checks, branch protections, local/cloud differences and any merge queue, and how the chosen strategy (Standard when unspecified) would be applied without reducing pre-merge coverage or disabling security, migration or deployment workflows;
- the scalability and cost relevance assessment, unless omitted, and whether you recommend running Planning now;
- if the project uses Vercel with Budget-conscious CI, an offer of vercel-deployment-budget after its preview-dependency review;
- external integrations and repository secrets the owner must set up, the checks you would run, and any conflicts or product choices that need my input.

3. Apply the approved plan
Adapt files without overwriting existing configuration blindly. Write a short root README.md. Complete docs/SPEC.md from known information, reconciling any existing project brief into one source of truth, marking each fact confirmed or assumption and leaving unknown product choices as open questions. Fill in AGENTS.md's Governance section with the profile, the starter pack revision (git -C <pack path> rev-parse --short HEAD), the recipes applied, the risk triggers and any approved overrides. Write the first docs/STATUS.md. Keep approved design decisions in docs/design/. Copy template/optional/docs/MILESTONES.md only when development stages are agreed, with observable acceptance checks for each milestone. Keep only accurate rules and existing commands in AGENTS.md, replacing its TODO command line. Set up formatting, linting, type checking and a production build where applicable. Add test tooling when there is behavior worth testing; do not invent placeholder tests.

For MVP, also:
- Add a verify script that changes no files: format:check, lint, typecheck and build, plus test once tests exist. Write its exact command, the CI strategy and the merge rule into the MVP section of AGENTS.md, and the backlog location into its first item. For docs/BACKLOG.md, copy template/optional/docs/BACKLOG.md and replace its placeholder lines with known work, or "None yet".
- Initialize docs/assumptions.md from what the brief and I have said: facts I stated as confirmed, with source and date; everything else as Open, with how it gets confirmed, or "owner to decide". Remove the template's placeholder rows.
- Initialize docs/runbook.md from what is known: how to run it locally, and "not decided yet" or "not applicable yet" for deploy, rollback, secrets, backups and incidents. Mark anything not tried as unverified.
- Record declined or omitted offers (legal planning, scalability and cost planning, Claude PR review) with their date in docs/SPEC.md under "Planning and open questions".
- If there is no remote yet, say so in AGENTS.md's Git remote section, do not add one or push, and list creating the repository, pushing, branch protection and the first hosted CI run as pending owner actions. Until then the MVP rule "independent CI before merge" cannot be met.
- Commit the setup, run verify on that commit, and record it in docs/STATUS.md with the revision; a later commit that changes only STATUS.md does not make that verification stale. Record hosted CI separately from local verification: write "not run" only when no hosted run has started. Otherwise record what was observed (passed, failed, pending, cancelled or skipped), the revision it ran on and a link to the run when available. A failed, pending, cancelled or skipped run does not satisfy the merge gate: merge still needs every required hosted check to pass on the current PR revision.
- List every choice still open for me (for example hosting, the merge rule if I gave none, or assumptions without a way to confirm them) under "Blockers and open questions" in docs/STATUS.md, and repeat them in your handoff.

Run audits only as their recipes describe: each external skill writes only its report under docs/audits/, and a missing skill is reported, not simulated. Present their findings before any separate implementation or SPEC/milestone update.

Run the available checks and summarize the changes, results and unresolved questions.

4. Git and pull requests
Set origin to the Git remote above, record it in AGENTS.md's Git remote section, and fetch and push only over SSH through that alias. If SSH fails, stop and tell me; do not switch to HTTPS or a token. Follow AGENTS.md: one PR at a time, waiting for me to merge or close each before starting the next; an IMPORTANT owner-actions block at the top of the PR description when migrations, secrets or remote-machine steps are needed, repeated in chat. Leave the merge to me, unless the MVP merge rule says otherwise.
```

If the project does not use Next.js, do not copy files from `recipes/next-fullstack/files/`. Use the shared core and a recipe appropriate to its stack.
