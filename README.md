# AI starter pack

A small, opinionated set of instructions and files for starting an application with Claude Code or Codex.

## Use it in a new repository

1. Create the new project with its official generator. For the current Next.js profile, choose TypeScript, the App Router, `src/`, pnpm and no Tailwind.
2. Copy the shared files, including dotfiles, into the target repository:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/core/ /absolute/path/to/new-project/
   ```

3. Choose a [stack recipe](recipes/next-fullstack/README.md). For Next.js, inspect its `files/` directory and copy the files that fit your generated project. Compare any existing configuration before merging it; `--ignore-existing` deliberately leaves existing files untouched.
4. Add optional integrations when useful: [Claude PR review](recipes/claude-pr-review/README.md) for on-demand GitHub reviews, or the [Playwright E2E CI guide](recipes/playwright-e2e/README.md) for choosing a browser-test setup.
5. Adapt the target project's root `README.md` (the generator may already provide one), complete `docs/SPEC.md` and `docs/design/`, and adapt `AGENTS.md`. Add `docs/MILESTONES.md` when development stages are agreed. Replace the command placeholder in `AGENTS.md` with scripts that actually exist in the new `package.json`.
6. Install and configure the tools described by the selected recipes, run the relevant checks, then commit the resulting project.

To delegate setup to an agent, use the [bootstrap prompt](BOOTSTRAP.md).

At setup, offer [lightweight scalability and cost planning](recipes/scalability-planning/README.md) when workloads, storage, external APIs, jobs or reliability needs affect early decisions. It uses the external `audit-scalability-cost` skill in Planning mode. A simple static project may need only a brief relevance assessment. Start with the smallest sufficient setup, explicit assumptions and measurable triggers for revisiting it.

Optionally enable [legal planning](recipes/legal-planning/README.md) after the first specification and before feature implementation. It uses the external `audit-legal-readiness` skill in Planning mode, followed by a Pre-launch review of the built product. Both modes recommend a top-tier reasoning model with high reasoning effort and prioritize verified sources over token savings.

Choose [Standard or Budget-conscious CI](recipes/ci-strategy/README.md) during setup or later. Standard is the default. Both use local validation and require the same independent cloud checks before merge; Budget-conscious skips draft PR jobs until the user authorizes ready for review. Inspect actual ready-state suite results before merging; a skipped draft check is not validation evidence. The policy is provider-independent, with optional GitHub Actions examples.

Optionally use [Test and CI efficiency review](recipes/test-ci-review/README.md) once real tests/CI exist, especially when feedback is slow, compute or maintenance is costly, failures recur or runner changes are being considered. It invokes the external `audit-test-ci` skill for an evidence-based report before a separate implementation task. It preserves meaningful coverage and required gates, can recommend keeping the setup, and is not a mandatory bootstrap audit or a CI strategy switch.

When development stages are agreed, copy the optional [milestone template](template/optional/docs/MILESTONES.md) into the target project's `docs/` directory and replace its prompts with the actual plan. Each milestone should have observable acceptance checks, a way to verify them and completion evidence. A milestone can span multiple PRs, which still follow the one-at-a-time review cadence.

When applying the pack to an existing repository, reconcile any earlier project brief or specification with `docs/SPEC.md` so the project does not keep competing sources of truth.

## Commit messages

Use a lowercase type followed by a colon, a space and a short imperative summary: `type: summary`. Choose `feat` for a new feature, `fix` for a bug fix, `docs` for documentation, `refactor` for a behavior-preserving code change, `test` for tests and `chore` for maintenance. For example: `feat: add search filters` or `docs: clarify setup steps`.

## Pull request cadence

For work that needs several PRs, deliver one at a time. Let the user review and merge or close the current PR before starting the next implementation. Parallel PR work is an exception that the user must request explicitly.

When a PR needs owner actions around merge or deployment, put them first in an `IMPORTANT` block and repeat them in the chat handoff. Give the responsible person, target environment, order, verified commands and success checks; distinguish merge from deployment and pending work from completed steps. Inspect schema, configuration and operational changes for these requirements. Omit the block when no action is needed.

For example, replace these placeholders with verified project details and choose the timing from the actual deployment process:

```markdown
> [!IMPORTANT]
> **Owner actions required**
>
> 1. **Before deployment — owner, production database:** run `<verified migration command>`. Confirm successful completion before deploying; stop if it fails.
> 2. **After deployment — owner, worker machine:** run `<verified service restart command>`. Confirm the worker reconnects and completes a test job.
```

## Layout

| Location | Purpose |
| --- | --- |
| `template/core/` | Project README, specification, design and decision templates, agent instructions and EditorConfig. |
| `template/optional/` | Milestone template to copy when development stages are agreed. |
| `recipes/next-fullstack/` | Next.js setup guide and optional Next.js and JavaScript tooling files. |
| `recipes/claude-pr-review/` | Optional GitHub workflow and setup guide for `@claude review` on pull requests. |
| `recipes/playwright-e2e/` | E2E CI decision guide and optional Playwright container workflow. |
| `recipes/ci-strategy/` | Local validation policy, CI strategy selection and optional budget GitHub Actions examples. |
| `recipes/test-ci-review/` | Optional evidence-based test/CI efficiency review and handoff to the external audit skill before implementation. |
| `recipes/self-hosted-runner/` | Optional private-repository Linux CI runner, Oracle ARM setup and GitHub-hosted fallback for either CI strategy. |
| `recipes/legal-planning/` | Optional specification-based legal preparation and handoff to the external legal readiness skill. |
| `recipes/scalability-planning/` | Lightweight capacity and cost planning, relevance assessment and handoff to the external scalability/cost skill. |
| `BOOTSTRAP.md` | Prompt for applying the pack to a new repository. |

More recipes can be added without making the core assume a framework or language. In particular, the Next.js ESLint config and Prettier preferences belong to its recipe, not to the core.

## Maintenance principles

- Agent instructions say **what** to do and **when**. Enforceable rules belong in configuration and CI. The reasons behind choices belong in decision records.
- Try a general rule in a real project before adding it here. Keep `AGENTS.md` short, accurate and relevant to the task.
- Compare recipes with the documentation for the framework version actually installed in the target project.
- Keep secrets, personal data, real customer examples and values from `.env` out of this potentially public pack.

The core does not preselect a package manager, database, hosting provider, authentication system or testing framework. A recipe may make those choices for its own stack; confirm them for each new application.
