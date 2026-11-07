# Test and CI efficiency review

Optional review of an existing test suite and development/CI execution using the external `audit-test-ci` skill. Use it to reduce waiting, unnecessary compute, unreliable failures and maintenance while preserving meaningful regression coverage and security. This recipe coordinates the audit and its handoff; the [AI Audit Toolkit methodology](https://github.com/Phunkhouse/ai-audit-toolkit/blob/main/references/test-ci-review.md) remains the source of truth.

## When to use it

Offer a review when a real test/CI setup exists and feedback is slow, compute or maintenance is becoming costly, failures/retries recur, or changes to test layers, scheduling or runners are being considered. A project can explicitly request a bounded review without those symptoms. Do not turn it into a required check on every PR or a mandatory bootstrap audit.

For a new scaffold without meaningful tests or execution evidence, choose a simple initial strategy using the [CI strategy recipe](../ci-strategy/README.md) and existing project requirements. Do not invent inefficiencies, create placeholder tests or add infrastructure merely to justify an audit. Revisit after the first representative suite/runs or a material change.

Select `test-ci-review` in the bootstrap's optional integrations or request it later in the target project. During bootstrap, include it in the initial plan and follow the existing setup-plan approval step before running it. Selecting the recipe does not authorize workflow changes, cloud reruns, runner provisioning or paid experiments. Missing timing data does not prevent code/configuration review of an existing setup; it limits conclusions about impact.

## Dependency and invocation

Install `audit-test-ci` from the [AI Audit Toolkit](https://github.com/Phunkhouse/ai-audit-toolkit) following its installation instructions. Use a version containing this skill and preserve access to its shared references/templates. Record the toolkit revision in the report. If the skill or its source cannot be accessed, identify the missing dependency rather than claiming the audit ran. No specific framework, CI provider, runner, model or paid plan is required.

Invoke the skill in the target project:

```text
Use audit-test-ci to review this project's actual testing strategy and CI.
Read README, SPEC, relevant architecture decisions, real test/workflow
commands and prior audit reports. Establish critical risks and the current
merge/deployment process; use available read-only run and account evidence.

Preserve meaningful regression coverage, security and required quality gates.
Separate measured results, code-proven mechanisms, estimates and hypotheses.
Keep queue time, execution time, runner-minutes, billing, reliability and
maintenance distinct. When evidence is missing, propose bounded measurements
without inventing a baseline or savings.

Follow the skill's test-ci.md report path, TCI finding IDs and repeat-audit
rules. Include risk-to-test/gate mapping, smoke/regression criteria and a
prioritized backlog with benefit, confidence, risk, effort, validation and
rollback. Include keeping the current setup and options not recommended.

Write only the report under docs/audits/. Do not change tests, workflows,
dependencies, CI strategy, protections or runner settings. Any useful local
checks must follow the skill's isolation and resource limits; do not dispatch
cloud CI or perform billable experiments without separate authorization.
Present findings before a separate implementation plan.
```

## Review output and implementation handoff

Expect `docs/audits/YYYY-MM-DD/test-ci.md`, following the skill's collision-safe directory naming and continuing `TCI-` IDs. The report should establish current test and CI architecture, protected risks and gates, evidence/coverage limits, bottlenecks, infrastructure tradeoffs, proposed suite boundaries, prioritized changes and a reproducible measurement plan. Unknown account settings, impact or run evidence remain `Not verified`; packaging or local checks alone do not establish cloud performance.

Keep the report and implementation separate. After review, agree which recommendations to implement and their acceptance checks. Use a focused implementation task to update applicable configuration, development instructions and decision records. Follow the pack's existing PR cadence, readiness permissions, required-check policy and owner-action handoff. Document the actual current-revision validation and unresolved evidence before merge; permission to review is not permission to merge.

Choose implementation candidates only when their conditions fit:

| Existing recipe | Use after the audit establishes |
| --- | --- |
| [CI strategy](../ci-strategy/README.md) | Scheduling or local/cloud validation changes would help while retaining the required pre-merge coverage. Standard remains the default; Budget-conscious requires the user's choice. |
| [Playwright E2E](../playwright-e2e/README.md) | The project actually uses Playwright and measured environment/setup tradeoffs justify adapting its runner, container or caching approach. |
| [Self-hosted runner](../self-hosted-runner/README.md) | Overall benefit justifies operating the host, compatibility is verified and the code/trust boundaries meet the recipe's conditions. Neither ARM nor a migration is automatic. |

Compare against keeping the setup. Treat recipe examples as adaptations to existing workflows, not additional suites to install alongside them. Inspect the recipe revision and installed tool versions before implementation; do not copy workflows blindly or assume a configured fallback has been tested. Shared-host capacity, isolation and recovery remain part of the decision.

## Revisit and integration checks

Re-audit after meaningful suite, workflow, runner, release-policy or workload changes, or when measured results contradict the expected benefit. Reuse prior finding IDs and compare representative runs under comparable conditions. Record whether the change improved feedback, compute/cost, reliability or maintenance separately, alongside retained coverage and actual gates.

- A new scaffold does not launch an unsolicited full audit or gain placeholder tests.
- An existing setup without telemetry receives evidence-based inspection and a measurement plan, not fabricated durations or savings.
- Missing/outdated skill access is reported explicitly; this recipe is not a second implementation of the audit.
- The review changes only its report; selecting it does not change CI strategy, weaken protections or authorize cloud work.
- Accepted follow-up work demonstrates both its intended benefit and preserved regression coverage, with safe rollback and existing PR/owner-action rules.
