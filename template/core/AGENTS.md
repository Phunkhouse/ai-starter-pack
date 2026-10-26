# Project instructions

Project overview: `README.md`. Detailed scope, workflows, limitations and open questions: `docs/SPEC.md`. Approved design: `docs/design/`. Agreed development stages, when present: `docs/MILESTONES.md`. Decision records: `docs/decisions/`.

Before changing code, inspect the relevant files and the installed framework's documentation. Do not assume that remembered APIs match this project.

## Commands

- Use the package manager and scripts selected for this project. Check the manifest before running a command.
- Before finishing a code change, run the relevant checks. Record their results and any checks you could not run.
- When adding or changing a script, update this section with its exact command and purpose.

<!-- After project setup, replace this block with actual scripts, e.g. pnpm check and pnpm format:check. -->

## Architecture

- Keep business rules separate from route handlers and UI components. Put validation and trust-boundary checks on the server.
- If a framework-free server layer exists, keep its dependency boundary enforced by lint. Do not create layers or directories just to match a template.
- Introduce external-service interfaces when they make a real dependency replaceable or testable.
- Keep files and APIs close to the workflows they serve; avoid broad barrel exports.

## UI

- Prefer semantic HTML, keyboard access, visible focus and useful alternative text.
- Follow the approved design in `docs/design/`; keep repeated visual values consistent.
- Put user-facing copy in the project's chosen content or localization system when one exists.

## Testing and changes

- Test important behavior and failure cases at the lowest useful level. Use real database integration tests for concurrency and transaction behavior.
- Prefer role-based queries in UI tests. Do not use fixed sleeps to make tests pass.
- Keep diffs focused. Explain meaningful dependency, schema and architecture decisions in the change description; record lasting trade-offs in `docs/decisions/`.
- Name commits `type: short imperative summary`, using lowercase `feat`, `fix`, `docs`, `refactor`, `test` or `chore` as appropriate.
- Before finishing, run the relevant checks, update affected documentation and commands, and mention unrelated changes without folding them into the task.
- Do not commit secrets, `.env` files or personal data. If the project needs environment variables, create `.env.example` with names and safe examples only.

## Pull requests

- Work through multiple PRs sequentially. Keep at most one agent-authored PR awaiting user review at a time.
- Finish checks and address feedback in the current PR. Wait for the user to merge or close it before starting the next PR's implementation, unless the user explicitly requests parallel PR work.
- Leave the final merge to the user unless they explicitly ask you to perform it.
