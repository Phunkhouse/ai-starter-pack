# MVP profile

For products in discovery: weeks to months of building, showing it to users and changing course. The aim is to learn quickly without building production machinery too early, while keeping the structure that lets the product mature without a rewrite.

MVP keeps the core's context rules and adds what an evolving product needs: hypotheses with a way to confirm them, one backlog the owner prioritizes, decision records for choices that are hard to reverse, risk-based tests, independent CI before merge, and a written deploy. It leaves out Production's milestone ceremony, its rule that only the owner merges, and its full audit set.

## What it adds to the foundation

| Mechanism | Where |
| --- | --- |
| Assumptions register with how each gets confirmed | `files/docs/assumptions.md` |
| Deploy, rollback, secrets, backup and incidents | `files/docs/runbook.md` |
| One backlog, prioritized by the owner | [`template/optional/docs/BACKLOG.md`](../../optional/docs/BACKLOG.md), the [Vikunja recipe](../../../recipes/vikunja-task-queue/README.md) or GitHub issues |
| README, specification, decision records and design | Production's document templates, listed in [`files-from`](files-from) |
| Process rules: hypotheses, scope, decisions, architecture, tests, CI, PRs, deploy | [AGENTS section](AGENTS-section.md) |

## Set up

New projects follow the pack's [bootstrap prompt](../../../BOOTSTRAP.md) with `MVP` as the profile. It copies `template/core/`, Production's `files/` (because of `files-from`) and this profile's `files/`, then composes `AGENTS.md` from the core and this profile's [AGENTS section](AGENTS-section.md).

A Sprint project that keeps going follows the [upgrade guide](UPGRADE.md) instead. It adds to the project and never resets it.

## Recipes and audits

- **Default:** [CI strategy](../../../recipes/ci-strategy/README.md), Standard unless the owner chooses Budget-conscious.
- **Opt-in:** [Claude PR review](../../../recipes/claude-pr-review/README.md), when the owner selects it.
- **Offered with the first database migration:** [seed data](../../../recipes/seed-data/README.md).
- **Offered at setup:** [scalability and cost planning](../../../recipes/scalability-planning/README.md) and [legal planning](../../../recipes/legal-planning/README.md).
- **Audits:** risk-based. `audit-security` and `audit-correctness` after a significant feature, and `audit-production` with `audit-security` before the first real users. The same pair is the readiness review before moving to Production.

## When it is ready for Production

Signs: paying users, personal data at scale, a second regular contributor, or availability commitments. The readiness review then lists what Production still needs, and the owner decides. Moving to Production adds rules; it does not reset the project.
