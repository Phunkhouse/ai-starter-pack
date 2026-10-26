# AI starter pack

A small, opinionated set of instructions and files for starting an application with Claude Code or Codex.

## Use it in a new repository

1. Create the new project with its official generator. For the current Next.js profile, choose TypeScript, the App Router, `src/`, pnpm and no Tailwind.
2. Copy the shared files, including dotfiles, into the target repository:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/core/ /absolute/path/to/new-project/
   ```

3. Choose a [stack recipe](recipes/next-fullstack/README.md). For Next.js, inspect its `files/` directory and copy the files that fit your generated project. Compare any existing configuration before merging it; `--ignore-existing` deliberately leaves existing files untouched.
4. Add optional integrations when useful: [Claude PR review](recipes/claude-pr-review/README.md) for on-demand GitHub reviews, or [Playwright E2E CI](recipes/playwright-e2e/README.md) for browser tests.
5. Adapt the target project's root `README.md` (the generator may already provide one), complete `docs/SPEC.md` and `docs/design/`, and adapt `AGENTS.md`. Add `docs/MILESTONES.md` when development stages are agreed. Replace the command placeholder in `AGENTS.md` with scripts that actually exist in the new `package.json`.
6. Install and configure the tools described by the selected recipes, run the relevant checks, then commit the resulting project.

To delegate setup to an agent, use the [bootstrap prompt](BOOTSTRAP.md).

When development stages are agreed, copy the optional [milestone template](template/optional/docs/MILESTONES.md) into the target project's `docs/` directory and replace its prompts with the actual plan.

When applying the pack to an existing repository, reconcile any earlier project brief or specification with `docs/SPEC.md` so the project does not keep competing sources of truth.

## Commit messages

Use a lowercase type followed by a colon, a space and a short imperative summary: `type: summary`. Choose `feat` for a new feature, `fix` for a bug fix, `docs` for documentation, `refactor` for a behavior-preserving code change, `test` for tests and `chore` for maintenance. For example: `feat: add search filters` or `docs: clarify setup steps`.

## Layout

| Location | Purpose |
| --- | --- |
| `template/core/` | Project README, specification, design and decision templates, agent instructions and EditorConfig. |
| `template/optional/` | Milestone template to copy when development stages are agreed. |
| `recipes/next-fullstack/` | Next.js setup guide and optional Next.js and JavaScript tooling files. |
| `recipes/claude-pr-review/` | Optional GitHub workflow and setup guide for `@claude review` on pull requests. |
| `recipes/playwright-e2e/` | Optional container-based CI workflow and setup guide for Playwright browser tests. |
| `BOOTSTRAP.md` | Prompt for applying the pack to a new repository. |

More recipes can be added without making the core assume a framework or language. In particular, the Next.js ESLint config and Prettier preferences belong to its recipe, not to the core.

## Maintenance principles

- Agent instructions say **what** to do and **when**. Enforceable rules belong in configuration and CI. The reasons behind choices belong in decision records.
- Try a general rule in a real project before adding it here. Keep `AGENTS.md` short, accurate and relevant to the task.
- Compare recipes with the documentation for the framework version actually installed in the target project.
- Keep secrets, personal data, real customer examples and values from `.env` out of this potentially public pack.

The core does not preselect a package manager, database, hosting provider, authentication system or testing framework. A recipe may make those choices for its own stack; confirm them for each new application.
