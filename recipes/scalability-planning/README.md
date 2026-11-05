# Scalability and cost planning

Offer a short review after the first specification, before dependent infrastructure decisions. Its purpose is to select the smallest sufficient setup, expose cost drivers and limits, and define when to revisit decisions. It works with any stack, provider or hosting model and coordinates the external `audit-scalability-cost` skill rather than copying its methodology.

## Offer according to relevance

Bootstrap defaults to **offer**: assess relevance and include the option in the initial plan, then run Planning when the user accepts it or has selected **enabled**. An explicit **omitted** selection skips it. Do not make it a compulsory audit or block unrelated development.

Assess features, not labels such as microsite or large application. Useful signals include a database, user-generated content, growing storage, uploads/media, paid APIs or AI, email, background jobs/imports, bursty demand and availability/recovery requirements. A small site can still have an expensive external operation. For a bounded static site without material variable costs or operational needs, explain briefly why deeper planning is unnecessary. Do not invent growth risks to justify running the skill.

## Dependency and invocation

Install `audit-scalability-cost` from the [AI Audit Toolkit](https://github.com/Phunkhouse/ai-audit-toolkit), following its installation instructions. Use a version with **Planning** and **Audit** modes, keeping its shared references and templates available. If it is missing or outdated, report that dependency rather than claiming the review ran. No particular provider, model or paid plan is imposed by this recipe.

```text
Use audit-scalability-cost in Planning mode for this project's specification.
Read SPEC, README and relevant milestones, proposed services and existing
implementation. Keep proposed choices separate from observed operation.

Keep the review lightweight and proportional to the decisions needed now.
Establish expected workload, relevant peaks, retention, budget and reliability
needs; ask for material missing inputs. Label assumptions and uncertainty.
Verify material provider prices, quotas, limit behavior and applicable terms
from current official sources. Include CI, builds and previews when material.

Recommend the smallest sufficient initial setup, conditional cost ranges,
first likely constraints, monitoring and measurable action triggers. Add
growth scenarios only when they help a current decision. Do not invent usage
or claim measured capacity. Write a dated scalability-planning report under
docs/audits/ without changing infrastructure, billing or project documents.
```

## Expected output and handoff

Keep the report as short as the scope allows, usually a page or two plus necessary sources. Use `docs/audits/YYYY-MM-DD/scalability-planning.md`, following the skill's collision and ID rules. Cover:

- Critical operations and material resources, including fixed and variable costs, shared allowances and operator effort.
- Explicit expected workload and a relevant peak over a stated horizon; retention and accumulating storage when applicable. Unknown inputs stay unknown or become visibly labeled assumptions, not observed metrics.
- Conditional cost ranges with equations, units, currency, source dates and first likely constraints. Public prices do not verify account eligibility or actual billing controls. Model limit behavior, not just the monthly bill.
- A minimal initial setup or retention of the existing one, with reasons tied to the requirements. Do not add queues, caches, paid plans or migration work solely for hypothetical scale.
- What to monitor and measurable triggers for reconsideration, with a window, justified threshold, preparation lead time and next action. Where the threshold depends on missing requirements or telemetry, identify the input needed rather than inventing a number.

Planning does not require mechanical 10x/100x projections. Use larger scenarios only where they inform decisions. In an existing project, retain available observed evidence while separating it from the new feature's estimates. A hypothetical growth constraint is not automatically a current release blocker.

Present material choices and unknowns to the user. The review writes only its report; separately promote approved decisions and report/requirement references into `docs/SPEC.md`, milestone acceptance checks and existing decision records where useful. Define observable checks for necessary monitoring or safeguards. Purchases, infrastructure changes, migrations and paid/load experiments require separate authorization.

## Revisit after implementation

Reassess when actual usage/billing becomes available or when workload, scope, retention, suppliers, prices or reliability needs materially change. Invoke the same skill in **Audit** mode to reconcile the planning report with observed usage over a stated window. Audit keeps the existing `scalability-cost.md` filename and `SCE-` IDs; it tests the assumptions rather than treating an earlier projection as measured capacity.

Include developer operations when material: CI minutes, builds, preview deployments and retained artifacts. Coordinate with the [CI strategy recipe](../ci-strategy/README.md) without weakening validation, security or recovery requirements to reduce cost. Cross-reference legal planning for supplier terms rather than counting the same issue twice.

## Integration checks

- A bounded static site gets a concise relevance assessment, without mandatory growth modeling or invented infrastructure needs.
- A specification with API/AI calls, uploads or background work produces explicit workload assumptions, cost drivers and useful action triggers even without telemetry.
- Missing budgets, account settings, prices or usage remain explicit uncertainties; zero is not substituted for unknowns.
- Planning leaves code, infrastructure and specifications unchanged, and does not represent forecasts as benchmarks.
- A later Audit reconciles actual evidence, source changes and continuing `SCE-` IDs with earlier planning decisions.
