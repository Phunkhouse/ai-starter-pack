# AI starter pack

A small, opinionated set of instructions and files for starting an application with Claude Code or Codex.

## Use it in a new repository

To delegate these steps to an agent, use the [bootstrap prompt](BOOTSTRAP.md); for a Sprint, use the short prompt in the [Sprint profile](template/profiles/sprint/README.md#set-up).

1. Choose a [governance profile](#governance-profiles).
2. Create the new project with its official generator. For the current Next.js recipe, choose TypeScript, the App Router, `src/`, pnpm and no Tailwind.
3. Copy the shared core and the profile's files, including dotfiles, into the target repository:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/core/ /absolute/path/to/new-project/
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/profiles/<profile>/files/ /absolute/path/to/new-project/
   ```

   Both copies are needed: `template/core/` alone is no longer a complete project, because the README, SPEC, design and decision templates moved into the profiles. `--ignore-existing` deliberately leaves existing files untouched, so **merge any file the generator already created by hand**. Next.js 16 generates its own `AGENTS.md`: keep its marked `nextjs-agent-rules` block (`next dev` re-adds it) and add the pack's `AGENTS.md` content below it. Compare the generator's `README.md` and ESLint config the same way.
4. Paste the profile's `AGENTS-section.md` where the core `AGENTS.md` marks it. Choose a stack recipe and any optional recipes from the [table below](#recipes); read each one before copying its files, and paste its `AGENTS-section.md` after the profile's.
5. Fill in the Governance section of `AGENTS.md`: the profile, the pack revision you applied (`git -C /absolute/path/to/ai-starter-pack rev-parse --short HEAD`), the recipes, the risk triggers that apply and any overrides. Replace the `TODO` command line with scripts that actually exist in the new `package.json`.
6. Adapt the target's root `README.md`, complete `docs/SPEC.md` and the profile's other documents, and write the first `docs/STATUS.md`. In an existing repository, reconcile any earlier project brief with `docs/SPEC.md` so there is one source of truth.
7. Set `origin` to the SSH URL with your host alias and record it in the Git remote section of `AGENTS.md` (see [Git over SSH](#git-over-ssh)).
8. Install and configure the tools described by the selected recipes, run the relevant checks, then commit and push the resulting project.

In a Production project, when development stages are agreed, copy the optional [milestone template](template/optional/docs/MILESTONES.md) into the target's `docs/` and replace its prompts with the actual plan. Each milestone needs observable acceptance checks, a way to verify them and completion evidence. A milestone can span several PRs, which still follow the one-at-a-time cadence.

## Governance profiles

Every project gets the same core: one source of truth, facts marked confirmed or assumed, a rewritten `docs/STATUS.md` for handover between sessions, scope and evidence rules, secret rules and risk triggers. A profile adds only the process the project's horizon needs.

| Profile | For | Adds to the core |
| --- | --- | --- |
| [Sprint](template/profiles/sprint/README.md) | Hours to days: assignments, hackathons, prototypes. | Time box, short SPEC with a decision log, test-first core logic, one local verify command, README as a deliverable. |
| MVP (planned) | Weeks to months of discovery and iteration. | Not yet available; use Production meanwhile. |
| [Production](template/profiles/production/README.md) | Long-lived applications. | Full SPEC, design and decision records, milestones, independent CI before merge, one PR at a time. This is the pack as it was before profiles. |

Risk is separate from the profile: the core's risk triggers (personal data, money, sign-in, real users, public reach) require their controls in any profile. A project's `AGENTS.md` records its profile, the risk triggers that apply and any overrides in its Governance section. A project without that section is treated as Production. Existing projects keep the files and pack revision they adopted. New Production setups get the new core rules on top of every earlier rule, and must copy the Production profile as well as `template/core/`; the [Production profile](template/profiles/production/README.md#compatibility-with-setups-from-before-profiles) explains the change.

## Git over SSH

Each project names its account explicitly through an SSH host alias, so an agent never guesses which identity to use and never falls back to HTTPS or a token. Define one alias per GitHub account in `~/.ssh/config`:

```sshconfig
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_work
  IdentitiesOnly yes
  AddKeysToAgent yes
  UseKeychain yes
```

`UseKeychain` (macOS) keeps the key's passphrase in the Keychain and `AddKeysToAgent` loads it on first use, so remotes keep working after a restart without `ssh-add`. On Linux, drop `UseKeychain` and rely on the desktop keyring or an agent started at login. Check an alias with `ssh -T git@github-work`.

Clone and add remotes with the alias, never with a plain `github.com` or HTTPS URL: `git clone git@github-work:owner/repo.git`. GitHub's "Code" button shows the plain form, so replace `github.com` with the alias when copying it. To fix an existing repository: `git remote set-url origin git@github-work:owner/repo.git`.

## Recipes

Every recipe except the stack recipe is optional. Each README holds that recipe's conditions and caveats. The profile columns match each profile's README: **default** is part of that profile's setup, **offered** is proposed at setup, **when needed** is adopted when the "Use when" condition arises, and **—** is not used in that profile.

| Recipe | Use when | Brings | Sprint | Production |
| --- | --- | --- | --- | --- |
| [Next.js full-stack](recipes/next-fullstack/README.md) | Stack recipe for a TypeScript Next.js app. | `files/`: CI workflow, ESLint, Prettier, `.nvmrc` | stack, without its CI step | stack |
| [CI strategy](recipes/ci-strategy/README.md) | Read at every Production setup. Standard is the default; Budget-conscious skips draft PR jobs until the user approves ready for review. | `examples/`: budget workflows; `AGENTS-section.md` for Budget-conscious | — | default |
| [Claude PR review](recipes/claude-pr-review/README.md) | You want on-demand `@claude review` comments on GitHub PRs. | `files/`: workflow | — | default |
| [Playwright E2E](recipes/playwright-e2e/README.md) | The project has browser tests and needs to choose a CI environment for them. | `files/`: container workflow | when needed | when needed |
| [Scalability and cost planning](recipes/scalability-planning/README.md) | Most useful when databases, uploads, paid APIs, jobs or reliability needs shape early decisions. | `AGENTS-section.md`; uses the external `audit-scalability-cost` skill | — | offered |
| [Legal planning](recipes/legal-planning/README.md) | After the first specification and before features, then a Pre-launch review. | `AGENTS-section.md`; uses the external `audit-legal-readiness` skill | when needed | offered |
| [Test and CI review](recipes/test-ci-review/README.md) | Real tests and CI exist and feedback is slow, costly or flaky. Not a bootstrap audit. | Uses the external `audit-test-ci` skill | — | when needed |
| [CI execution performance](recipes/ci-performance/README.md) | Bounded worker, cache and duplicate-work improvements under either strategy. | Guidance and a measured [case study](recipes/ci-performance/case-study.md) | — | when needed |
| [Self-hosted runner](recipes/self-hosted-runner/README.md) | A trusted private repository exhausts its included GitHub Actions minutes. | `examples/`: combined workflow | — | when needed |
| [Vercel deployment budget](recipes/vercel-deployment-budget/README.md) | A Vercel project under Budget-conscious CI hits deployment limits. | Config fragment, after a preview-dependency review | — | when needed |
| [Seed data](recipes/seed-data/README.md) | The project has a database: invented local data that shows every state and feature, with safety guards. | `examples/`, `AGENTS-section.md` | when needed | default once there is a database |
| [Vikunja task queue](recipes/vikunja-task-queue/README.md) | Ideas and findings arrive faster than they can be implemented, and you want a self-hosted owner/agent queue. | `examples/`, `AGENTS-section.md`, `task-sync` skill | — | when needed |

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
| `template/core/` | Shared foundation for every profile: agent instructions, `CLAUDE.md`, the status template and EditorConfig. |
| `template/profiles/` | One directory per profile: its `AGENTS-section.md`, its README and the `files/` it adds to the target. |
| `template/optional/` | Milestone template to copy when development stages are agreed. |
| `recipes/` | Stack and optional recipes, listed [above](#recipes). |
| `BOOTSTRAP.md` | Prompt for applying the pack to a new repository with an agent. |
| `scripts/`, `.github/` | The pack's own checks; not copied into target projects. |

More recipes can be added without making the core assume a framework or language. In particular, the Next.js ESLint config and Prettier preferences belong to its recipe, not to the core.

## Maintenance principles

- Agent instructions say **what** to do and **when**. Enforceable rules belong in configuration and CI. The reasons behind choices belong in decision records.
- Try a general rule in a real project before adding it here. Keep `AGENTS.md` short, accurate and relevant to the task; put profile-specific rules in the profile's `AGENTS-section.md` and recipe-specific rules in the recipe's.
- Profiles only add to the core. A rule every project needs belongs in the core, never copied into each profile.
- State each rule in one place. The README and bootstrap prompt point to recipes rather than restating their caveats.
- Compare recipes with the documentation for the framework version actually installed in the target project.
- Keep secrets, personal data, real customer examples and values from `.env` out of this potentially public pack.
- CI checks every PR for broken relative links and anchors (`python3 scripts/check-links.py`, with its regression cases in `python3 scripts/test-check-links.py`), that the Production profile keeps every pre-profile rule (`python3 scripts/check-production-parity.py`), shellcheck on every `.sh` file and actionlint on the pack's and the recipes' workflows. Run the same commands locally before opening a PR.

The core does not preselect a package manager, database, hosting provider, authentication system or testing framework. A recipe may make those choices for its own stack; confirm them for each new application.
