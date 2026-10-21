# AI starter pack

A small, opinionated set of instructions and files for starting an application with Claude Code or Codex.

## Use it in a new repository

1. Create the new project with its official generator. For the current Next.js profile, choose TypeScript, the App Router, `src/`, pnpm and no Tailwind.
2. Copy the shared files, including dotfiles, into the target repository:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/core/ /absolute/path/to/new-project/
   ```

3. Choose a [stack recipe](recipes/next-fullstack/README.md). For Next.js, inspect its `files/` directory and copy the files that fit your generated project. Compare any existing configuration before merging it; `--ignore-existing` deliberately leaves existing files untouched.
4. If you want on-demand Claude reviews on GitHub pull requests, follow the optional [Claude PR review recipe](recipes/claude-pr-review/README.md).
5. Complete `docs/project.md` and adapt `AGENTS.md`. Replace its command placeholder with scripts that actually exist in the new `package.json`.
6. Install and configure the tools described by the selected recipes, run the relevant checks, then commit the resulting project.

To delegate setup to an agent, use the [bootstrap prompt](BOOTSTRAP.md).

## Commit messages

Use a lowercase type followed by a colon, a space and a short imperative summary: `type: summary`. Choose `feat` for a new feature, `fix` for a bug fix, `docs` for documentation, `refactor` for a behavior-preserving code change, `test` for tests and `chore` for maintenance. For example: `feat: add search filters` or `docs: clarify setup steps`.

## Layout

| Location                    | Purpose                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ |
| `template/core/`            | Shared agent instructions, project brief, decision record template and EditorConfig. |
| `recipes/next-fullstack/`   | Next.js setup guide and optional Next.js and JavaScript tooling files.               |
| `recipes/claude-pr-review/` | Optional GitHub workflow and setup guide for `@claude review` on pull requests.       |
| `BOOTSTRAP.md`              | Prompt for applying the pack to a new repository.                                    |

More recipes can be added without making the core assume a framework or language. In particular, the Next.js ESLint config and Prettier preferences belong to its recipe, not to the core.

## Maintenance principles

- Agent instructions say **what** to do and **when**. Enforceable rules belong in configuration and CI. The reasons behind choices belong in decision records.
- Try a general rule in a real project before adding it here. Keep `AGENTS.md` short, accurate and relevant to the task.
- Compare recipes with the documentation for the framework version actually installed in the target project.
- Keep secrets, personal data, real customer examples and values from `.env` out of this potentially public pack.

The core does not preselect a package manager, database, hosting provider, authentication system or testing framework. A recipe may make those choices for its own stack; confirm them for each new application.
