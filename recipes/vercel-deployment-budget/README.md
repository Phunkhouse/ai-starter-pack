# Vercel deployment budget

Optional for Vercel-hosted projects using Budget-conscious development: propose automatic Git deployments only for the actual production branch, plus an explicit preview branch namespace when useful. Use after reviewing preview dependencies and obtaining the user's agreement. This recipe does not impose Vercel or change the default hosting choice.

## Why this is separate from CI

Skipping draft GitHub Actions jobs or moving them to a self-hosted runner does not disable Vercel's Git integration. Branch pushes can still create previews while CI is skipped. Deployment selection must be reviewed separately; production validation and required test coverage remain intact.

Verified **2026-11-11**: Vercel lists Hobby at **100 deployments per 86,400 seconds**, with the deployment rate limit scoped to **owner**. Projects under the same owner share that budget; it is not 100 per project. Exhausting it requires waiting for the limit to recover, so reducing future deployments does not immediately reset it. Recheck the actual plan and owner scope rather than assuming every project uses Hobby. [Vercel limits](https://vercel.com/docs/limits)

An **Ignored Build Step** can cancel a build, but Vercel says those canceled builds still count toward deployment quotas and concurrency slots. Do not use `ignoreCommand` alone as a deployment-count saving mechanism. Preserve existing ignore behavior until its purpose is understood. [Project settings](https://vercel.com/docs/project-configuration/project-settings), read **2026-11-11**.

## Inspect the target project first

1. Read the existing `vercel.json` or `vercel.ts` (and any other active configuration format), project root/monorepo layout and relevant configuration tooling. Preserve unrelated settings; do not create a competing configuration file. Establish the actual Vercel production branch from authorized project evidence, not from the Git default branch alone. Inspect real branch names and naming conventions.
2. Identify `git.deploymentEnabled`, legacy Git settings, `ignoreCommand` and any known dashboard Ignored Build Step. If project settings are unavailable, list the precise unknowns and ask the owner; do not guess. Do not read or print tokens or secret environment files to discover settings.
3. Search workflows, test configuration, scripts and docs for preview URLs, Vercel deployment wait steps, deployed E2E targets, deployment-status triggers, deploy hooks/CLI deployments, PR comments/checks and required branch rules. Report what depends on previews, what does not, and what could not be inspected. If tests use a local built app, confirm that from configuration rather than assuming it.
4. Read the current [Git configuration documentation](https://vercel.com/docs/project-configuration/git-configuration) for the target setup. Propose a minimal merge into the active config, explain trade-offs below, and wait for agreement before applying it. A Budget-conscious CI selection alone is not approval to remove previews.

## Suggested branch policy

The following is a **configuration fragment**, not a file to copy blindly. Replace `<production-branch>` with the verified branch identifier and confirm that `preview/**` fits the project's conventions. Omit that preview rule if the user chooses production-only deployment.

```json
{
  "git": {
    "deploymentEnabled": {
      "**": false,
      "<production-branch>": true,
      "preview/**": true
    }
  }
}
```

Verified **2026-11-11**: Vercel uses minimatch patterns; unspecified branches default to enabled, and **any matching `true` wins** when rules overlap. Rule order is not a last-match override. `**` is essential to cover slash-separated branch names; a plain `*` does not cover `feat/example`. Check for other broad `true` rules when merging configuration. [Git configuration](https://vercel.com/docs/project-configuration/git-configuration)

Test the patterns with the project's installed `minimatch` when available. Use its actual production branch, flat and slash-separated feature/fix/agent branches, and both shallow and nested preview branches. Expected outcomes: production enabled, ordinary work branches disabled, opted-in previews enabled. Include an overlap case demonstrating that a matching `true` enables deployment despite `**: false`. If minimatch is unavailable, report that limitation rather than claiming an executable check; do not add a runtime dependency just for this configuration review.

For `vercel.ts`, adapt the existing exported config using its installed types. Do not introduce JSON alongside it. Keep a single source of truth and check applicable config/schema validation without reading credentials or performing a deployment.

## Trade-offs to present before applying

- Ordinary PR branches no longer get a new automatic preview URL or deployment-derived Vercel check/comment to review. Existing previews may be stale; a previous link is not evidence for the latest commit. Do not assume a required Vercel check will still appear or pass: coordinate any dependency/rules change with the owner, preserving independent CI gates.
- Preview-based E2E, deployment hooks, review procedures and documented links may need an approved alternative before disabling previews. Keep necessary deployed-environment verification; do not silently remove it or repoint it to production to save deployments.
- An opted-in `preview/**` branch deploys on its pushes, including draft development. It is not a readiness gate or a one-deployment allowance. Explain how the owner requests a preview and avoids continuing routine work on an opted-in branch.
- This policy targets automatic Git deployments. Inventory manual, CLI and hook paths separately; do not promise a cap on all deployment creation or disable unrelated production/release workflows. It does not remove old deployments or guarantee immediate recovery from an exhausted quota.

## Apply and hand off

After agreement, make the focused config change on a branch following the target project's PR rules. Record the reason, decision date, verified production branch, opt-in convention, affected preview consumers and remaining unknowns in its existing development docs or decision records. Validate patterns and existing configuration checks; keep tests and builds required by that project.

State clearly in the adoption PR: **Vercel configuration change delivered on merge; no shell command is required to activate it.** Do not change dashboard settings, environment variables or domains. Confirm the actual integration behavior on subsequent Git events and check that existing work branches carry the new configuration as needed; do not claim every existing branch is retroactively covered merely because the default branch changed. If settings or branch rules need a separate owner action, put that specific action at the top in an IMPORTANT block and repeat it in chat. Otherwise do not invent a manual command.

## Acceptance checks

- [ ] The user saw the preview-dependency inventory, unknown settings and trade-offs and agreed before the target config changed.
- [ ] The actual production branch remains enabled, ordinary slash-containing branches are disabled, and the agreed preview namespace is enabled; overlap behavior was checked with minimatch when available.
- [ ] Existing config and ignore behavior are preserved or intentionally reconciled; branch protections and preview-dependent tests have an approved working path.
- [ ] After adoption, subsequent ordinary branch pushes create no automatic preview, opted-in preview pushes deploy as intended, and production still deploys. Observe this when authorized events occur; do not create test deployments while the account is quota-blocked.
- [ ] Actual ready-state CI still runs and passes. The PR records its merge-based rollout, no-command handoff, dated sources and any checks that could not be performed.
