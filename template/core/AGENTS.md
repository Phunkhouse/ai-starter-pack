# Project instructions

Project overview: `README.md`. Detailed scope, workflows, limitations and open questions: `docs/SPEC.md`. Approved design: `docs/design/`. Agreed development stages, when present: `docs/MILESTONES.md`. Decision records: `docs/decisions/`.

Before changing code, inspect the relevant files and the installed framework's documentation. Do not assume that remembered APIs match this project.

## Commands

- Use the package manager and scripts selected for this project. Check the manifest before running a command.
- Before finishing a code change, run the relevant checks. Record their results and any checks you could not run.
- When adding or changing a script, update this section with its exact command and purpose.

<!-- After project setup, replace this block with actual scripts, e.g. pnpm check and pnpm format:check. -->

## Validation strategy

- CI strategy: Standard (default). Change this to Budget-conscious only when the user chooses it and the CI configuration implements it.
- During development and before handing off work, run the relevant local formatting, lint, type, test and build checks using existing project commands. Use a unified verification command when useful; report results and local/cloud environment differences, including checks that could not run.
- Standard runs cloud validation on relevant PR updates. Budget-conscious skips validation jobs on draft PRs until ready for review; every subsequent commit to a ready PR still needs full cloud validation. A skipped draft check is not evidence of testing: before merge, inspect the current revision's ready-state run and actual suite results.
- In Budget-conscious mode, create draft PRs and obtain explicit user permission before marking them ready. Permission to request review is not permission to merge. Do not bypass checks or change the strategy to avoid a failure.
- Before any authorized merge, confirm successful independent CI for the current revision, including every required suite. Local results and earlier commits' CI do not replace it. Respect existing security, migration, deployment and branch rules.

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
- If `docs/MILESTONES.md` exists, use its acceptance checks to guide the current milestone. Before calling a milestone complete, verify each check, record evidence and unresolved gaps there, and request user validation for product or visual judgments. A passing CI run alone does not establish that the intended outcome works.
- Do not commit secrets, `.env` files or personal data. If the project needs environment variables, create `.env.example` with names and safe examples only.

## Scalability and cost planning (when enabled)

- Use `audit-scalability-cost` in Planning mode for specification-based capacity and cost decisions. Prefer the smallest sufficient setup; distinguish proposed workloads and conditional estimates from measured usage or capacity.
- Verify material prices, quotas and terms from current official sources. Include shared limits, CI/preview costs and operational effort when relevant; do not assume free service or billing caps.
- Keep the report under `docs/audits/`; promote approved decisions, monitoring and measurable action triggers into `docs/SPEC.md` and milestone acceptance checks separately. Revisit assumptions after meaningful scope changes or first real usage data, using Audit mode for actual operation. Reviews do not authorize paid experiments or infrastructure changes.

## Legal planning (when enabled)

- Use `audit-legal-readiness` in Planning mode after the initial specification and before dependent implementation, then Pre-launch mode against the built product. Revisit the plan after material changes to markets, business model, features, suppliers or data uses.
- Run either mode with a top-tier reasoning model and high reasoning effort or the closest supported equivalent. Announce the model/settings when known; warn if weaker or unverified. Prioritize source verification and completeness over token savings, and do not claim a model switch or review that did not occur.
- Keep review output in `docs/audits/`. Promote approved requirements into `docs/SPEC.md` and milestone acceptance checks separately. Planned controls do not prove launch readiness; do not publish legal documents as part of the review.

## Pull requests

- Inspect schema, configuration and operational changes for owner actions such as database migrations, service restarts or steps on a separate machine. When actions are required, put a `> [!IMPORTANT]` block at the very top of the PR description and repeat the actions in the chat handoff. Omit the block when no action is needed.
- List actions in execution order, naming the responsible person, target environment/machine, timing relative to merge or deployment, and how to verify success. Include the exact verified command (a one-liner for migrations when available); state unverified details explicitly rather than inventing commands. Identify failures that block the next step. Determine timing from deployment behavior and compatibility, not from an assumption that every migration runs before merge.
- Keep the action block current as the PR changes and distinguish pending actions from confirmed completed steps. Documenting an action does not mean it has been performed or authorize executing it.
- Work through multiple PRs sequentially. Keep at most one agent-authored PR awaiting user review at a time.
- Finish checks and address feedback in the current PR. Wait for the user to merge or close it before starting the next PR's implementation, unless the user explicitly requests parallel PR work.
- Leave the final merge to the user unless they explicitly ask you to perform it.
