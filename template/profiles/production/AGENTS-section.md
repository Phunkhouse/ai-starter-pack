## Production profile

- Further sources of truth: approved design in `docs/design/`; agreed development stages, when present, in `docs/MILESTONES.md`; decision records in `docs/decisions/`.
- If `docs/MILESTONES.md` exists, use its acceptance checks to guide the current milestone. Before calling a milestone complete, verify each check, record evidence and unresolved gaps there, and request user validation for product or visual judgments. A passing CI run alone does not establish that the intended outcome works.

## Validation strategy

- CI strategy: Standard. Cloud validation runs on every relevant PR update, including drafts. Budget-conscious CI is opt-in; see the starter pack's CI strategy recipe.
- During development and before handing off work, run the relevant local formatting, lint, type, test and build checks using existing project commands. Use a unified verification command when useful; report results and local/cloud environment differences, including checks that could not run.
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

## Testing

- Test important behavior and failure cases at the lowest useful level. Use real database integration tests for concurrency and transaction behavior.
- Prefer role-based queries in UI tests. Do not use fixed sleeps to make tests pass.
- Explain meaningful dependency, schema and architecture decisions in the change description; record lasting trade-offs in `docs/decisions/`.

## Pull requests

- Inspect schema, configuration and operational changes for owner actions such as database migrations, service restarts or steps on a separate machine. When actions are required, put a `> [!IMPORTANT]` block at the very top of the PR description and repeat the actions in the chat handoff. Omit the block when no action is needed.
- List actions in execution order, naming the responsible person, target environment/machine, timing relative to merge or deployment, and how to verify success. Include the exact verified command (a one-liner for migrations when available); state unverified details explicitly rather than inventing commands. Identify failures that block the next step. Determine timing from deployment behavior and compatibility, not from an assumption that every migration runs before merge.
- Keep the action block current as the PR changes and distinguish pending actions from confirmed completed steps. Documenting an action does not mean it has been performed or authorize executing it.
- Work through multiple PRs sequentially. Keep at most one agent-authored PR awaiting user review at a time.
- Finish checks and address feedback in the current PR. Wait for the user to merge or close it before starting the next PR's implementation, unless the user explicitly requests parallel PR work.
- Leave the final merge to the user unless they explicitly ask you to perform it.
