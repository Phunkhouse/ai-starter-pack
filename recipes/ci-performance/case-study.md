# Kultomat: a CI job from 12m 07s to 5m 19s

Case date and source verification: 2026-11-11. The two durations in the title are **measured (CI)** job elapsed times, expressed in minutes/seconds. This is a selected before/after sequence from a private project, not a controlled benchmark or a performance promise. Use the [shared recipe](README.md) with either Standard or Budget-conscious CI.

## Environment and evidence

Kultomat used Budget-conscious scheduling, with ready-PR validation in a combined `verify` job on a dedicated persistent Linux ARM64 self-hosted runner. The final run's machine log reported two available CPUs via `nproc` (**measured (CI)**); that alone does not establish every container quota. Exact account quotas, billing, production configuration and private log contents are outside this public case study. The execution changes below do not require Budget-conscious scheduling or a particular cloud vendor.

The maintainer read job timestamps/step results and relevant logs through GitHub on the verification date. The source repository, PRs and Actions links are private: readers without access cannot independently inspect them. No raw logs, customer data, credentials or host identifiers are reproduced here. Local experiments supplied by the project informed candidate selection, but their timings are not independently reproduced or included as CI results.

For an authorized reader, reproduce the timing extraction with:

```sh
gh api repos/Phunkhouse/kultomat/actions/runs/43043517344/jobs
gh run view 43043517344 --repo Phunkhouse/kultomat --log
```

Use each job/step's `started_at` and `completed_at`, conclusion, event and tested revision. These commands read existing evidence; they do not rerun CI. Logs may contain sensitive information; inspect privately rather than copying them into a public report.

## Selected sequence: measured (CI)

Every duration in this table is **measured (CI)** in seconds, calculated from the job/step timestamps. The E2E column covers the whole E2E step, including application preparation/build and Playwright; it is not browser-test-only time. All selected jobs concluded successfully.

| State and source run | Complete verify job | Test step | E2E step, including preparation/build | Lint step | Typecheck step |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Selected baseline](https://github.com/Phunkhouse/kultomat/actions/runs/43026860307) | 727 | 289 | 366 | 11 | 29 |
| [After Vitest worker adjustment](https://github.com/Phunkhouse/kultomat/actions/runs/43034020380) | 433 | 150 | 210 | 10 | 30 |
| [After E2E workers, cache/typecheck changes](https://github.com/Phunkhouse/kultomat/actions/runs/43037631477) | 382 | 151 | 163 | 10 | 30 |
| [After shared modules and template fixtures](https://github.com/Phunkhouse/kultomat/actions/runs/43043517344) | 319 | 110 | 162 | 1 | 17 |

### Worker adjustment

[#296](https://github.com/Phunkhouse/kultomat/pull/296) explicitly set Vitest's maximum workers to two for the test step. The installed version's default and the runner's effective capacity had previously limited concurrency. The test-step drop is the relevant observation; the untouched E2E phase also became substantially faster in that run, so the full-job improvement cannot be credited to this change alone. Defaults must be inspected per installed release, not encoded as a universal cores-minus-one rule.

### E2E concurrency, persistent caches and duplicate checking

[#297](https://github.com/Phunkhouse/kultomat/pull/297) set two Playwright workers, added persistent ESLint/incremental TypeScript state and confined a duplicate Next build-typecheck exemption to the test-build path after independent checking. Production hosting paths retained type checking. These were bundled changes; the table cannot isolate each one's contribution. The first run after the change did not yet show the final lint/typecheck benefit, consistent with cache-state differences that must remain explicit.

Cache acceptance depended on the project's actual rules/configuration and invalidation. The outcome does not make ESLint caching safe for arbitrary cross-file rules, make all compiler output reusable or justify a generic production typecheck bypass.

### Shared modules and template fixtures

[#298](https://github.com/Phunkhouse/kultomat/pull/298) reduced per-file module isolation only in eligible Node test projects; the web project retained isolation. A source-pattern guard and file-order experiments supported that choice, without proving absence of every possible shared-state leak.

The same PR introduced migration-derived template databases for disposable fixtures, with completed-template publication, coordinated locking and database-grant handling. This was project-specific test infrastructure. Dedicated fresh-migration and permission/isolation checks remain important acceptance criteria when adapting the approach.

The final run was associated with PR head `a43c1a928ad80934502b0b84ec701a497a9e6b57`, but the checkout log's `git log -1 --format=%H` shows that it actually tested GitHub's synthetic merge commit `6d4ca2874aa700cd0f19c8e392bb7a983c8d803b`. It finished before the PR merged as `6f8a00472f83942d4dc452e4ed4097c087c0f3fa`; the measured result therefore does not establish a later merged-commit run. Shared modules and template fixtures changed together, so their individual CI contributions were not measured.

## Interpret the result and earlier audit

The baseline is a selected slower run, not a representative median. Different revisions, cache states and host conditions prevent a controlled causal estimate. Read the complete job time and per-step results together; do not add rounded tool summaries or attribute all E2E variation to Playwright workers. A successful job alone does not independently prove that selected/skipped coverage and every assertion stayed equivalent.

The earlier `TCI-001` recommendation had deferred template-database adoption after a bounded local comparison under a compute-saving objective. Later work prioritized wall time on the self-hosted environment and evaluated a broader combined change. Retain the original evidence and append a dated reconciliation: implemented in the later PR, combined CI test-step improvement observed, template-only contribution unknown, CI CPU and monetary savings not measured. A local compute proxy and CI elapsed time answer different questions; neither erases the other.

The supplied remediation record also marked compiler-cache persistence (`TCI-003`) and the search assertion (`TCI-004`) fixed in code in [#295](https://github.com/Phunkhouse/kultomat/pull/295). Those earlier changes are context, not separately attributed savings in this sequence. A finding's implementation status, focused verification and independently measured CI impact must remain distinct.

## Reusable conclusions and open work

Instrument effective resources and full phases, inspect actual workers, then tune one relevant area at a time. Preserve clean source/output while retaining only compatible safe cache state. Keep test flags explicit so local env files cannot change the scenario. Compare cold/warm cohorts, failure behavior and selected/skipped coverage; measure CPU separately if it is an objective.

The project's proposed follow-ups included narrower E2E change selection, trimming browser combinations and a larger paid runner. They are **not implemented or measured by this case study**. Selection needs dependency-aware coverage and required-outcome handling; browser reductions need a justified coverage decision; hardware changes need an overall benefit comparison. No estimated seconds or guaranteed savings are assigned here.

This documentation update read existing evidence only. It did not rerun tests/CI, reproduce local experiments, alter the application or change workflows/settings. The transferable result is a measured decision process with conditional optimizations, not a default configuration to copy.
