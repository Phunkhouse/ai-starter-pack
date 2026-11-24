# Project instructions

## Governance

- Profile: `<Sprint | MVP | Production>`, from starter pack `<revision>`, with recipes `<names, or none>`. The profile section below sets how much process this project uses.
- Risk triggers that apply: `<none, or the rows below>`. Overrides: `<none, or control: level, because reason>`.
- Only the owner changes the profile or an override.

## Sources of truth

- `README.md`: what the project is and how to run it. `docs/SPEC.md`: requirements, scope, facts and open questions. `docs/STATUS.md`: current state and next step. The profile section lists any further documents.
- Mark every fact with its status: **confirmed** (by whom, date), **assumption**, **proposal** or **decided** (with a link to the decision). Never present an assumption or proposal as confirmed.
- When the code, the docs and your assumptions disagree, the code is the truth for current behavior and the docs for intended behavior. Report the disagreement and ask; do not silently pick one or change the other to match.
- Before changing code, inspect the relevant files and the installed framework's documentation. Do not assume that remembered APIs match this project.

## Scope and evidence

- Work only within the agreed scope. Material product, scope or architecture changes need the owner's word.
- Propose work found outside the scope in your final message; do not do it.
- Report work with evidence: the checks actually run, on which revision, and what could not be run. Written but unverified is not done.

## Handover

- Read `docs/STATUS.md` at the start of every session and after a context reset.
- Before ending a session or after finishing a step, rewrite it, do not append: goal, current state, next step, blockers, last verified checks with revision. Keep it under one page; history lives in Git.

## Commands

- Use the package manager and scripts selected for this project. Check the manifest before running a command.
- Before finishing a code change, run the relevant checks. Record their results and any checks you could not run.
- When adding or changing a script, update this section with its exact command and purpose.

- TODO after setup: replace this line with the project's actual scripts and their purpose, e.g. `pnpm verify` runs format, lint, typecheck, tests and build.

## Changes

- Keep diffs focused.
- Name commits `type: short imperative summary`, using lowercase `feat`, `fix`, `docs`, `refactor`, `test` or `chore` as appropriate.
- Before finishing, run the relevant checks, update affected documentation and commands, and mention unrelated changes without folding them into the task.
- Keep this file short. Put long procedures in `docs/DEVELOPMENT.md` and link them from here.
- Do not commit secrets, `.env` files or personal data. If the project needs environment variables, create `.env.example` with names and safe examples only.

## Risk triggers

These apply whatever the profile. Record the ones that apply under Governance.

| When the project | It needs |
| --- | --- |
| Stores personal data | Only the data it needs, access checks on the server, no personal data in logs, seeds or tests. |
| Handles money | Amounts computed on the server, idempotent operations, tests for rounding and failures. |
| Has sign-in | Authorization checked on the server for every route, and tests that one user cannot reach another's data. |
| Has real users | Backups with a tested restore, error monitoring and a rollback path. |
| Is publicly reachable | Dependency and secret scanning, rate limits on endpoints open to abuse, security headers. |

## Git remote

- Remote: `<git@HOST_ALIAS:OWNER/REPOSITORY.git>`. Fetch and push only over SSH through this host alias, and use the same alias for any clone or added remote.
- If SSH fails (for example `Permission denied (publickey)`), stop and report it. Do not switch to HTTPS, a token or another account to get around it.

<!-- Paste the profile's AGENTS-section.md here, then any recipe snippets. -->
