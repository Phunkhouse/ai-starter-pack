# Local validation and CI strategy

Choose when validation runs without reducing what must pass before merge. This policy works with any CI provider; the optional examples below use GitHub Actions and the existing Next.js/pnpm and Playwright recipes. They are adaptations, not additional workflows to install alongside existing ones.

## Choose a strategy

| Strategy | During development | Before merge |
| --- | --- | --- |
| Standard (default) | Relevant local checks and automatic cloud CI on PR changes, including drafts. | All required cloud suites pass for the current revision. |
| Budget-conscious (opt-in) | Agents create draft PRs and run relevant checks locally. Drafts defer expensive cloud jobs. Only explicit user permission allows the agent to mark a PR ready. | Ready for review triggers full CI. Every later commit to a ready PR triggers it again. The same required suites must pass. |

Keep the existing one-PR-at-a-time cadence. Ready permission does not authorize merge; leave merging to the user unless explicitly authorized. Neither strategy permits bypassing checks or substituting local results for independent CI.

Record `CI strategy: Standard` or `CI strategy: Budget-conscious` in the target project's `AGENTS.md`. Keep the executable behavior in the provider's existing workflow configuration. No repository variables, strategy parser or generated configuration are needed. For another provider, implement equivalent draft/readiness events and a required result that only passes after actual validation.

## Local validation

- Prefer existing formatting, lint, typecheck, test and build commands. Run relevant checks during development and before handoff; use the full applicable local suite before requesting ready status.
- Add one verification command only if it simplifies a real sequence. For a pnpm project with those scripts, `verify` might run `pnpm format:check && pnpm lint && pnpm typecheck && pnpm test && pnpm build`. Omit nonexistent scripts; do not create placeholder tests. Existing required tests must not become optional when adopting this recipe.
- Keep E2E or integration commands separate when they need services or credentials. Run them locally when available and report any missing verification explicitly.
- In `docs/SPEC.md`, or `docs/DEVELOPMENT.md` when needed, document differences such as OS, runtime, database version, fonts, browser image, environment variables and unavailable credentials. Record actual results in the PR, including the revision and checks not run.
- Keep coverage and important failure cases unchanged. Optimize setup and scheduling before removing work. Local success does not prove that Linux, services or a production build will work in CI.

## GitHub Actions configuration

Runner location is independent of strategy: optionally use the [self-hosted Linux runner recipe](../self-hosted-runner/README.md) with either Standard or Budget-conscious CI. It includes an Oracle ARM example, manual GitHub-hosted fallback and a combined-job variant that preserves draft and required-check rules.

The existing [Next.js CI](../next-fullstack/files/.github/workflows/ci.yml) and [optional Playwright container workflow](../playwright-e2e/files/.github/workflows/e2e.yml) implement Standard. Both use PR events, dependency caching and per-workflow/per-PR cancellation. They run again on `ready_for_review`, including when no new commit was pushed.

For Budget-conscious, adapt the [single-job CI example](examples/budget-ci.yml) and, if applicable, the [E2E example](examples/budget-e2e.yml). Save them as the target project's existing `.github/workflows/ci.yml` and `e2e.yml` only after reconciling configuration, commands, services and required check names. The examples require the same project setup as their original recipes. Keep the Playwright image tag aligned with the installed package, or retain a verified runner-based browser setup.

| PR event | Standard | Budget-conscious |
| --- | --- | --- |
| `opened`, `synchronize`, `reopened` | Full CI. | Full CI if ready; deferred if draft. |
| `ready_for_review` | Full CI. | Full CI even without a new commit. |
| `converted_to_draft` | No additional run; existing run may finish. | Cancels the previous run through concurrency; starts a deferred result. |

Do not gate on the event action alone: a `synchronize` event can belong to either a draft or a ready PR. Use the PR's draft state. Do not replace `pull_request` with privileged `pull_request_target` to run PR code. Keep read-only workflow permissions and existing fork/secret restrictions; a fork approval or merge conflict can legitimately delay execution.

Avoid duplicate PR and branch-push validation. Preserve post-merge, security, migration and deployment workflows that serve different purposes. Cancellation is appropriate for replaceable validation; do not apply it to migrations or deployments without evaluating partial execution and rollback.

Cache dependencies using the lockfile and runtime/platform as appropriate. Keep lockfile-based installs. Do not share secrets through caches or assume cached build/test results establish validation. Add browser or build caches only after measuring complete job times; see the [Playwright guide](../playwright-e2e/README.md).

## Required checks must represent real validation

GitHub can accept a skipped required job as successful. A workflow skipped by path filters or skip instructions can instead leave checks pending. Therefore the examples do not use workflow-level path exclusions or commit-message skipping. A ready docs-only PR gets the full suite by default; a draft docs-only PR follows the draft policy. Introduce narrower suites only as a separately reviewed project decision with explicit coverage and required-result handling.

The budget single-job example keeps `check` unconditional. On a draft it fails at the first step, before checkout or dependency installation. The multi-job E2E example skips `browser_tests` before runner/container allocation and always schedules the small `playwright` result job. That job accepts only `success`, rejecting `skipped`, `failure` and `cancelled`.

This deliberately leaves a red, deferred cloud check on drafts. A short runner job still consumes some minutes, but the expensive work is deferred. Draft PRs cannot merge. Do not turn this deferred result into a successful no-op.

For a larger multi-job workflow, use the same pattern: the final required job uses `if: always()`, lists every mandatory worker in `needs`, and explicitly checks that every result is `success`. Extend both the dependency list and result checks when adding a suite. Do not add a draft condition to the final job, use `continue-on-error` for mandatory workers, or treat any skipped mandatory suite as passing. Keep separate required outcomes for separate workflows; this example's `check` does not attest to E2E.

Configure branch protection or rulesets to require the actual final check names. The examples retain the original `check` and `playwright` names. In an existing project inspect the names GitHub reports, including matrix naming; use unique names and preserve any additional required security or deployment results. If renaming is necessary, generate the new result and coordinate the protection change before relying on it. Select GitHub Actions as the expected source when supported.

Require successful validation of the current revision before merge. GitHub PR workflows normally test the synthetic merge commit; keep that behavior rather than silently switching checkout to an unrelated branch or unvalidated head. Require an up-to-date branch or a merge queue when protecting against changes in the target branch. Restrict direct pushes and bypasses according to the project's policy. Review changes to workflow and validation scripts: a required check name alone cannot guarantee that its implementation has not been weakened.

For a merge queue, add this alongside `pull_request` in **every required validation workflow**, in either strategy:

```yaml
merge_group:
  types: [checks_requested]
```

Run the complete suites on that event. The budget examples' conditions allow non-PR events, so they validate the merge-group commit instead of trying to read a missing PR. The concurrency fallback separates merge-group refs from PR runs. Do not enable a merge queue until all required workflows support it.

Check the target repository's plan and rules: GitHub branch protection and rulesets for private repositories require an eligible paid plan. Without enforceable protection, the merge requirement remains a human/agent procedure; this recipe cannot provide the same technical enforcement. Organization-required workflows may also impose additional runs that this recipe must preserve. Recheck compatibility when repository rules change.

## Retry and state changes

Use GitHub's rerun action on the failed **ready-state run for the current revision**. A rerun retains its original event and SHA; it does not validate new commits or refresh a draft event into a ready event. Rerunning a draft-state run can remain deferred after the PR becomes ready. Use the new `ready_for_review` run instead.

A new commit to a ready PR must obtain new successful checks. An older green run is insufficient. If the PR needs more development, the user can return it to draft. A stale rerun may still show a result based on its original state; verify the PR's current revision and readiness before any authorized merge. Do not repeatedly rerun failures without investigating their cause.

If a required run never started, inspect event configuration, fork approval, merge conflicts, Actions availability and branch rules. Do not solve a pending result by bypassing protections. Ready status must be changed by the user or by an agent with explicit user permission. This is an agent policy: GitHub permissions do not distinguish an agent from a human using the same account.

## Adopt or switch strategies

1. Inventory current CI, mandatory suites, services, security/deployment workflows, check names, rules and local commands. Keep the existing provider. Compare complete job times to identify what is expensive.
2. Choose the strategy with the user; default to Standard. Update `AGENTS.md` and workflow configuration together in one focused change. Preserve validation commands, coverage and required names. Returning to Standard removes draft deferral and restores automatic runs for drafts.
3. Run local checks and validate the YAML with `actionlint` for GitHub Actions. Coordinate any required-check changes with repository settings; do not disable protections just to merge the transition.
4. Exercise the acceptance scenarios below in a disposable test repository or a controlled PR, then confirm all required checks on the transition PR before merge. Check existing open PRs as well; workflow changes do not retroactively trigger all of them. Do not count old green runs as evidence that the new policy works.

## Acceptance scenarios

Static YAML validation checks syntax and expressions; it cannot prove GitHub event delivery or protection behavior. Test both strategies against the real provider. Use a controlled failing test and restore it before accepting the change.

| Scenario | Expected result |
| --- | --- |
| Open, update and reopen a draft | Standard runs all suites; budget defers expensive jobs and does not produce a successful final result. |
| Mark draft ready without a new commit | All suites run and required results pass only after real success. |
| Push after green ready CI | New revision runs all suites and cannot merge using only the previous revision's result. |
| Return a running ready PR to draft | Budget cancels the older run; expensive new jobs do not start. Deferred result is not green. |
| Fail, cancel or time out a mandatory worker | Required final result does not pass, including in multi-job CI. |
| Skip a mandatory worker | Required final result fails; the skipped worker cannot satisfy the final result. |
| Rerun failed current ready CI | Uses the same revision and reruns validation; a stale revision or draft run does not substitute for the current ready run. |
| Change only documentation | Ready PR still runs the full configured suite, with no indefinitely pending path-filtered check. |
| Push rapidly to two PRs | Obsolete runs of each workflow/PR are canceled; different PRs and CI/E2E do not cancel each other. |
| Test merge queue, if enabled | Every required suite runs against the merge-group commit. |
| Try merging with a failed/missing current check | Branch protection/ruleset blocks it for actors without bypass rights. |
| Switch each direction with open PRs | Instructions and workflows agree; current PR revisions receive the intended checks. |

Measure draft and ready runs, including the short result jobs and cold cache cases. Confirm that the savings come from scheduling and setup, with the same pre-merge test coverage.

## References

- [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): PR activity types, merge groups and event revisions.
- [Required check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks): latest revisions, skipped jobs, pending checks and protection availability.
- [Concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency): cancellation and grouping.
- [Rerunning workflows](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs): original event revision and permissions.
- [PR readiness](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/changing-the-stage-of-a-pull-request) and [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets): permissions and enforcement.
