# Legal planning

Optional legal preparation after the first project specification, before dependent feature implementation. It produces source-backed product decisions, implementation requirements and acceptance checks. Follow it with a Pre-launch review of the actual product. This recipe coordinates the existing `audit-legal-readiness` skill rather than embedding a second legal methodology or generic legal documents.

## Prerequisite and model choice

Install `audit-legal-readiness` from the [AI Audit Toolkit](https://github.com/Phunkhouse/ai-audit-toolkit) using that repository's installation instructions. Use a version supporting both Planning and Pre-launch modes. Keep the toolkit's shared references and templates available; do not copy only `SKILL.md` and lose its supporting sources. No absolute machine path or specific provider is required by this recipe. If the skill is unavailable or outdated, report that dependency and resolve it before claiming the review has run.

**Use a top-tier reasoning model with high reasoning effort, or the closest supported equivalent, for either mode. Prioritize thorough research and completeness over token cost or speed.** The agent should announce the model and reasoning setting when reliably known; if weaker, warn and recommend switching, and if unknown, say that it cannot verify the setup. A prompt is not a model-switching mechanism: do not claim a switch without actually performing one through supported controls. Record known settings and limitations in the report. No fixed vendor/model name is embedded because available models change.

## Planning workflow

1. Enable legal planning in the bootstrap prompt or ask for it later. Read the current `docs/SPEC.md`, README, milestones, approved design decisions and any proposed suppliers. An existing project can still use Planning for a new feature; keep its planned and current behavior distinct.
2. Invoke the skill in **Planning** mode. Establish the operator, relevant markets, audience, paid/free model, planned launch date, proposed data uses and suppliers from evidence. Ask only for material missing facts. Do not infer jurisdiction or exemptions from language, hosting location, project size or a noncommercial label.
3. Apply the skill's primary-source method to relevant requirements and conditional options. The report belongs at `docs/audits/YYYY-MM-DD/legal-planning.md`, with a collision-safe dated directory when needed. It records facts, assumptions, source provisions and dates, applicability, implementation requirements, acceptance checks and open questions. Future fulfillment is `Not yet assessed`; unreadable sources or missing evidence remain explicitly unverified. A proposed feature without implementation is not an observed violation.
4. Present material choices and uncertainties to the user. The review itself writes only its report. In a separate planning task, transfer approved requirements and source/report references into `docs/SPEC.md` and, when present, `docs/MILESTONES.md`. Track requirement IDs so acceptance checks and later reviews remain traceable. Resolve missing inputs before implementing behavior that depends on them; unrelated work can continue.
5. Revisit the preparation when markets, business model, features, suppliers, data purposes or relevant sources materially change. Do not let a historical report become an assumed permanent clearance.

Use this invocation with the skill available in the target project:

```text
Use audit-legal-readiness in Planning mode for this project's specification.
Use a top-tier reasoning model and high reasoning effort or the closest
supported equivalent. Announce the model/settings when known; warn if the
setup is weaker or cannot be verified. Prioritize thorough source verification
and applicability analysis over token cost or speed.

Read docs/SPEC.md, README.md and any existing milestones/design decisions.
Distinguish confirmed facts, proposed choices and unknowns. Verify relevant
primary sources, their applicability and dates. Ask for material missing facts.
Write a legal-planning report under docs/audits/ with requirements, decisions,
observable acceptance checks, unresolved facts and re-review triggers.
Do not treat missing future implementation as a current violation.
Keep specifications, implementation and public legal documents unchanged
during this review; present proposed follow-up work separately.
```

## Before launch

Invoke the same skill in **Pre-launch** mode, referencing the planning report and the actual product revision. Revalidate source currency and applicability, compare the implemented behavior and operational evidence with planned requirements, and retain existing `LEG-` IDs where the same requirement continues. Write `legal-readiness.md` in a dated audit directory without overwriting prior reports.

A completed planning report does not establish actual fulfillment or overall compliance. Request complete legal document drafting separately, once the relevant facts and decisions are confirmed; publication is also a separate action. Do not demand a banner, checkbox, standard contract or lawyer review for every project automatically. Keep the skill's distinction between verified requirements, recommendations and interpretation questions.

## Integration checks

- Planning works from a specification without application code and does not call missing future controls confirmed violations.
- Pre-launch compares actual evidence to earlier requirements and does not treat a planned control as verified implementation.
- Both modes announce model limitations, read actual primary sources and retain uncertainty for inaccessible or outdated evidence.
- The review writes only its report; promoting requirements or drafting/publishing documents remains a separate task.
- Material unknowns produce precise questions. Unrelated work can proceed without guessing the answers.
- Earlier reports remain intact, requirements keep their IDs across modes, and sources and assumptions are checked again before release.
