# AI starter pack

A small, opinionated set of instructions and files for starting an application with Claude Code or Codex.

## Use it in a new repository

To delegate these steps to an agent, use the [bootstrap prompt](BOOTSTRAP.md).

1. Create the new project with its official generator. For the current Next.js profile, choose TypeScript, the App Router, `src/`, pnpm and no Tailwind.
2. Copy the shared files, including dotfiles, into the target repository:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/core/ /absolute/path/to/new-project/
   ```

   `--ignore-existing` deliberately leaves existing files untouched, so **merge any file the generator already created by hand**. Next.js 16 generates its own `AGENTS.md`: keep its marked `nextjs-agent-rules` block (`next dev` re-adds it) and add the pack's `AGENTS.md` content below it. Compare the generator's `README.md` and ESLint config the same way.
3. Choose a stack recipe and any optional recipes from the [table below](#recipes). Read each one before copying its files, and paste its `AGENTS-section.md` into the target `AGENTS.md` when it has one.
4. Adapt the target's root `README.md`, complete `docs/SPEC.md` and `docs/design/`, and replace the `TODO` command line in `AGENTS.md` with scripts that actually exist in the new `package.json`. In an existing repository, reconcile any earlier project brief with `docs/SPEC.md` so there is one source of truth.
5. Record the pack revision you applied (`git -C /absolute/path/to/ai-starter-pack rev-parse --short HEAD`) in the target's `docs/SPEC.md` under Technical approach, so later pack changes can be compared with what the project received.
6. Install and configure the tools described by the selected recipes, run the relevant checks, then commit the resulting project.

When development stages are agreed, copy the optional [milestone template](template/optional/docs/MILESTONES.md) into the target's `docs/` and replace its prompts with the actual plan. Each milestone needs observable acceptance checks, a way to verify them and completion evidence. A milestone can span several PRs, which still follow the one-at-a-time cadence.

## Recipes

Every recipe except the stack recipe is optional. Each README holds that recipe's conditions and caveats.

| Recipe | Use when | Brings |
| --- | --- | --- |
| [Next.js full-stack](recipes/next-fullstack/README.md) | Stack recipe for a TypeScript Next.js app. | `files/`: CI workflow, ESLint, Prettier, `.nvmrc` |
| [CI strategy](recipes/ci-strategy/README.md) | Always read at setup. Standard is the default; Budget-conscious skips draft PR jobs until the user approves ready for review. | `examples/`: budget workflows; `AGENTS-section.md` for Budget-conscious |
| [Claude PR review](recipes/claude-pr-review/README.md) | You want on-demand `@claude review` comments on GitHub PRs. | `files/`: workflow |
| [Playwright E2E](recipes/playwright-e2e/README.md) | The project has browser tests and needs to choose a CI environment for them. | `files/`: container workflow |
| [Scalability and cost planning](recipes/scalability-planning/README.md) | Offered at setup by default; most useful when databases, uploads, paid APIs, jobs or reliability needs shape early decisions. | `AGENTS-section.md`; uses the external `audit-scalability-cost` skill |
| [Legal planning](recipes/legal-planning/README.md) | After the first specification and before features, then a Pre-launch review. | `AGENTS-section.md`; uses the external `audit-legal-readiness` skill |
| [Test and CI review](recipes/test-ci-review/README.md) | Real tests and CI exist and feedback is slow, costly or flaky. Not a bootstrap audit. | Uses the external `audit-test-ci` skill |
| [CI execution performance](recipes/ci-performance/README.md) | Bounded worker, cache and duplicate-work improvements under either strategy. | Guidance and a measured [case study](recipes/ci-performance/case-study.md) |
| [Self-hosted runner](recipes/self-hosted-runner/README.md) | A trusted private repository exhausts its included GitHub Actions minutes. | `examples/`: combined workflow |
| [Vercel deployment budget](recipes/vercel-deployment-budget/README.md) | A Vercel project under Budget-conscious CI hits deployment limits. | Config fragment, after a preview-dependency review |
| [Seed data](recipes/seed-data/README.md) | The project has a database: invented local data that shows every state and feature, with safety guards. | `examples/`, `AGENTS-section.md` |
| [Vikunja task queue](recipes/vikunja-task-queue/README.md) | Ideas and findings arrive faster than they can be implemented, and you want a self-hosted owner/agent queue. | `examples/`, `AGENTS-section.md`, `task-sync` skill |

How recipes are packaged:

- `files/` mirrors the target repository and can be copied with `rsync -a --ignore-existing <recipe>/files/ <target>/`, then adapted.
- `examples/` holds starting points to adapt into the target's existing files, not to install alongside them.
- `AGENTS-section.md` is pasted into the target `AGENTS.md` only when the recipe is adopted, so the core instructions stay short.

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
| `recipes/` | Stack and optional recipes, listed [above](#recipes). |
| `BOOTSTRAP.md` | Prompt for applying the pack to a new repository with an agent. |
| `scripts/`, `.github/` | The pack's own checks; not copied into target projects. |

More recipes can be added without making the core assume a framework or language. In particular, the Next.js ESLint config and Prettier preferences belong to its recipe, not to the core.

## Maintenance principles

- Agent instructions say **what** to do and **when**. Enforceable rules belong in configuration and CI. The reasons behind choices belong in decision records.
- Try a general rule in a real project before adding it here. Keep `AGENTS.md` short, accurate and relevant to the task; put recipe-specific rules in that recipe's `AGENTS-section.md`.
- State each rule in one place. The README and bootstrap prompt point to recipes rather than restating their caveats.
- Compare recipes with the documentation for the framework version actually installed in the target project.
- Keep secrets, personal data, real customer examples and values from `.env` out of this potentially public pack.
- CI checks every PR for broken relative links and anchors (`python3 scripts/check-links.py`), shellcheck on every `.sh` file and actionlint on the pack's and the recipes' workflows. Run the same commands locally before opening a PR.

The core does not preselect a package manager, database, hosting provider, authentication system or testing framework. A recipe may make those choices for its own stack; confirm them for each new application.
