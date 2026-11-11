# CI execution performance

Optional guidance for making an existing CI run faster and less wasteful while retaining meaningful regression coverage, security and required gates. Use with **Standard or Budget-conscious CI**. The [CI strategy](../ci-strategy/README.md) controls when validation runs; this recipe helps improve the execution that still has to run. Runner placement is a separate decision. Selecting this recipe does not switch strategy, defer checks or require self-hosting.

For an evidence-based diagnosis, use [Test and CI efficiency review](../test-ci-review/README.md) with the external `audit-test-ci` skill. Its [review method](https://github.com/Phunkhouse/ai-audit-toolkit/blob/main/references/test-ci-review.md) owns the detailed audit methodology. This recipe guides targeted implementation choices after review; a full audit is optional, not required for every small improvement. Do not add placeholder tests or compulsory instrumentation to an empty scaffold.

## Establish the target and evidence

Agree whether feedback latency, resource consumption, billed cost, reliability or maintenance matters most. A faster job need not consume less CPU, and lower compute need not reduce the current bill. Compare against keeping the setup. Preserve existing security, deployment/migration controls and required pre-merge coverage; scheduling changes remain a separate project decision.

Use existing run/job/step reports first. When instrumentation is useful, propose only the missing signals in a focused change:

- Installed tool/runtime versions, runner OS/architecture, CPU availability to the process, effective container/affinity limits, memory and competing jobs. In Node projects, `os.availableParallelism()` can help; a nominal core count alone does not establish effective capacity.
- Queue/setup/build/test/reporting intervals, observed worker count, slow test files and failures/retries. Distinguish whole-job/step time from a tool's own summary.
- Cache type/location, cold or warm state, invalidation inputs and restore/save overhead. Keep cold-start costs visible as well as comparable warm runs.
- Selected/passed/failed/skipped tests and important assertions, so a quicker result cannot hide lost coverage.

Label numeric evidence `measured (CI)`, `measured (local <environment>)` or `estimate`, with revision, event, source, sample size and conditions. Local results select candidates; they do not establish cloud savings. Record variability and unrelated phase changes. Prefer small, separately revertible experiments; bundled changes cannot establish individual contributions. The [Kultomat case study](case-study.md) illustrates both the improvements and these limits.

## Choose a bounded improvement

Use only relevant rows. Keep the current configuration when evidence does not justify a change; there is no universal worker count, cache or duration target.

| Candidate | Conditions and acceptance evidence | Rollback |
| --- | --- | --- |
| Tune workers per phase/project | Inspect installed defaults and actual workers; compare a small bounded set against CPU/memory, service contention, complete phase time and unchanged required coverage. Preserve intended serial cases and isolated data. | Restore the previous worker setting. |
| Remove repeated setup or builds | Trace wrappers, global setup and framework hooks. Reuse only compatible output from the tested revision; retain an actual production-mode build and every required validation. Compare complete job time and feedback ordering. | Restore separate setup/build steps and required outcomes. |
| Retain safe compiler or incremental state | Verify installed-tool behavior, invalidation after source/configuration/dependency changes and a cold-run path. Recompute current output and rerun required checks. | Drop cache/metadata and use clean execution. |
| Correct unnecessary waits/assertions | Demonstrate the same intended behavior and failure detection; a missing expected result must fail. Diagnose flaky product behavior rather than hiding it with retries. | Keep a correct failure-producing assertion; do not restore swallowed errors. |
| Control test environment inputs | Pin behavior-critical test-server variables, inspect local env-file precedence and reused servers, and verify both positive and negative feature states without exposing secrets. | Restore a known isolated test setup, preserving explicit intended states. |

Before an experiment, set scenario, allowed commands, sample/run count, concurrency, time/resource limits, stop conditions and acceptance checks. Local artifact-producing work belongs in an isolated disposable copy with isolated dependencies. Cloud reruns, billable experiments, runner provisioning and changes outside the authorized task need separate authorization. Do not turn a review request into implementation.

## Adapt cache handling to the runner

**Ephemeral hosted runner:** include download/restore/save time, cold misses, storage and compatibility in the comparison. A remote cache helps only when it beats recomputation without weakening verification. Browser caches are not automatically useful; follow the [Playwright guide](../playwright-e2e/README.md) for that decision.

**Persistent self-hosted runner:** inspect checkout cleanup first. Default `actions/checkout` cleanup deletes ignored output too, so an appropriate repository-scoped cache outside checkout may survive while source/build output stays clean. Avoid redundant remote upload when local persistence already works, but measure the actual job. Bound size/age, coordinate concurrent writes/cleanup and restrict access to trusted compatible jobs. Follow the [self-hosted runner recipe](../self-hosted-runner/README.md); private visibility alone does not provide isolation.

For either environment, cache compiler/dependency work rather than application data, authentication state or prior passing test results. ESLint's content cache and a lockfile key do not track all cross-file dependencies: type-aware and import-resolution rules can produce stale results for unchanged files. Inspect actual rules and use uncached checks or proven complete invalidation where needed. Missing type-aware rules alone is insufficient.

## Keep advanced changes conditional

- **Shared test modules:** retain isolation by default. Consider a project-scoped exemption only after checking mocks, globals, mutable singletons, imported helpers and resources, with repeated file-order experiments and retained isolation elsewhere. A source-pattern guard supports maintenance but cannot prove absence of all leaks.
- **Template databases:** include template preparation, real fixture count, lock waits, migration/server compatibility, safe publication/cleanup and per-test data isolation. Preserve fresh-migration coverage and role/RLS/backup/restore checks. PostgreSQL does not copy database-level settings/grants; verify them explicitly. Advisory locks taken in different databases do not coordinate cluster-wide role changes.
- **Duplicate typecheck exemption:** first prove equivalent coverage of the same revision, generated types, configuration and packages, and that required outcomes fail on a relevant type error. Keep production/deployment checks intact. Next's `ignoreBuildErrors` bypasses checking entirely; it is not a safe shared default or incremental checking.

High load average is a contention signal, not a universal saturation threshold. Correlate it with CPU usage/throttling, memory/I/O and complete job results before increasing workers or proposing more hardware. Do not move CI onto a production host with secrets to avoid a runner bill.

## Validate and hand off

Document expected versus observed effects independently for feedback, compute/cost, reliability and maintenance. Reconcile changed test selection/assertions and run the actual required checks on the current revision. Preserve the pack's PR/readiness/merge rules and [owner-action handoff](../../README.md#pull-request-cadence). A skipped job or earlier green revision is not testing evidence. Keep a tested or clearly specified rollback, including any coordinated required-check names.

Record lasting choices and measurement conditions in the target project's decision/development documents. Revisit after tool, runner, workload or objective changes; retain earlier evidence when a recommendation changes. Neither these docs nor the case study proves another project's savings.

## Source checks

Relevant sources checked on 2026-11-11; recheck installed versions and project applicability before adoption:

- [Vitest workers](https://vitest.dev/config/maxworkers) and [isolation](https://vitest.dev/config/isolate): defaults and shared-module behavior depend on the installed release.
- [ESLint cache](https://eslint.org/docs/latest/use/command-line-interface#--cache) and [actions/checkout](https://github.com/actions/checkout): invalidation limits and clean behavior.
- [Next.js TypeScript](https://nextjs.org/docs/app/api-reference/config/next-config-js/typescript): build-check bypass semantics.
- [PostgreSQL template databases](https://www.postgresql.org/docs/17/sql-createdatabase.html) and [advisory lock scope](https://www.postgresql.org/docs/17/view-pg-locks.html): verify the actual server version.
- [Linux load average](https://man7.org/linux/man-pages/man5/proc_loadavg.5.html): runnable and I/O-waiting tasks.
