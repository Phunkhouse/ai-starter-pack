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

Follow the pack's [bootstrap prompt](../../../BOOTSTRAP.md), which sets up Production. It copies `template/core/` and this profile's `files/`, then composes `AGENTS.md` from the core and this profile's [AGENTS section](AGENTS-section.md).

An MVP project moves here with the [upgrade guide](UPGRADE.md): a read-only gap list first, then a readiness stage with `audit-production`, `audit-security` and evidence checks that records every decision in `docs/readiness.md`, and the move only after the owner has approved it and no critical or high gap is unresolved.

## Compatibility with setups from before profiles

- **Existing projects keep the revision they adopted.** Their copied files do not change until the owner applies a newer pack revision to them. Without a Governance section they are treated as Production.
- **New Production setups get the new core rules as well:** Governance, fact status, the conflict rule, scope and evidence, handover through `docs/STATUS.md`, and risk triggers. Every earlier rule is still there: the composed core and Production section were compared sentence by sentence with the earlier `AGENTS.md`, and the only reworded sentences are the one-line list of documents, now split between the core map and this profile's "further sources" line. CI enforces this with `scripts/check-production-parity.py` against a stored copy of the earlier file.
- **Setup steps that copied only `template/core/` must change.** The core no longer contains the README, SPEC, design or decision templates, nor the validation, architecture, UI, testing, milestone and pull request rules. A script, prompt or habit that copied only `template/core/` now also needs to copy `template/profiles/production/files/` and paste this profile's [AGENTS section](AGENTS-section.md).

## Recipes and audits

- **Default:** [CI strategy](../../../recipes/ci-strategy/README.md).
- **Opt-in:** [Claude PR review](../../../recipes/claude-pr-review/README.md), when the owner selects it in the bootstrap prompt.
- **Offered with the first database migration:** [seed data](../../../recipes/seed-data/README.md).
- **Offered at setup:** [scalability and cost planning](../../../recipes/scalability-planning/README.md) and [legal planning](../../../recipes/legal-planning/README.md).
- **Audits:** the AI Audit Toolkit's full set, repeated after material changes, with `audit-production` and `audit-security` before each major release.
