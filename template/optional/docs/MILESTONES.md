# Development milestones

Use this document only after the development approach and stages have been agreed. Keep it aligned with [the project specification](SPEC.md), and link it from the root README.

Describe each milestone in delivery order. Focus on the outcome and how completion will be recognized, not a running list of every implementation task. Add or remove milestones to match the actual plan. Write acceptance checks before implementation so the expected result is clear. A milestone may span several PRs; keep their review and merge sequence separate from milestone acceptance.

## Milestone 1: Name

**Status:** planned

**Goal:** What working outcome will this stage deliver?

**Scope:** Which workflows or capabilities are included?

**Acceptance checks:** Describe observable outcomes, including important failure cases. Name how each check will be verified (automated test, command, manual walkthrough or review). Avoid checks that merely list files or implementation tasks.

- [ ] A user can complete the main workflow; verify with [specific test or walkthrough].
- [ ] The important failure case behaves as specified; verify with [specific test or walkthrough].
- [ ] Any milestone-specific accessibility, design, performance or operational requirement is met; verify with [relevant check, if applicable].

**Completion evidence:** Record the result and link to relevant PRs, CI runs, screenshots or notes after verification. Note checks that could not be run and why. Mark the milestone complete only when its acceptance checks pass and its PRs have landed; request user validation where the outcome requires a product or visual judgment.

**Dependencies and risks:** What must be ready first, and what could change the plan?
