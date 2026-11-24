# Production profile

For mature, long-lived applications: real users, several contributors or agents over months, and changes that must not break what already works. This is the starter pack as it was before profiles, unchanged. A project whose `AGENTS.md` has no Governance section is treated as Production.

## What it adds to the foundation

| Mechanism | Where |
| --- | --- |
| Full specification, design source of truth, decision records | `files/`: `docs/SPEC.md`, `docs/design/`, `docs/decisions/` |
| Milestones with acceptance checks and completion evidence | [`template/optional/docs/MILESTONES.md`](../../optional/docs/MILESTONES.md), once stages are agreed |
| Independent CI on every PR before merge | [CI strategy recipe](../../../recipes/ci-strategy/README.md); Standard by default |
| One PR at a time, owner merges, owner-action blocks | [AGENTS section](AGENTS-section.md) |
| Architecture, UI and testing rules for web applications | [AGENTS section](AGENTS-section.md) |

## Set up

Follow the pack's [bootstrap prompt](../../../BOOTSTRAP.md) with `production` as the profile. It copies `template/core/` and this profile's `files/`, then composes `AGENTS.md` from the core and this profile's [AGENTS section](AGENTS-section.md).

## Recipes and audits

- **Usually adopted:** [CI strategy](../../../recipes/ci-strategy/README.md), [Claude PR review](../../../recipes/claude-pr-review/README.md), [seed data](../../../recipes/seed-data/README.md) once there is a database.
- **Offered at setup:** [scalability and cost planning](../../../recipes/scalability-planning/README.md) and [legal planning](../../../recipes/legal-planning/README.md).
- **Audits:** the AI Audit Toolkit's full set, repeated after material changes, with `audit-production` and `audit-security` before each major release.
