# Prompt for starting a project with an agent

Copy this prompt into Claude Code or Codex while working in the **new target repository**. Fill in the paths and a short description of the application. The agent needs access to both locations.

```text
I am starting a new application: <one to three sentences about its purpose and users>.

The starter pack is at <absolute path to ai-starter-pack>.
The target repository is at <absolute path to the new repository>.
The relevant recipe is <recipe name, or none>.
The optional integrations are <integration recipe names, or none>.
The CI strategy is <Standard (default) or Budget-conscious>.
Legal planning is <enabled or omitted>.
Scalability and cost planning is <offer (default), enabled or omitted>.

Read the starter pack README.md, template/core/ and the selected recipes. Inspect the target repository and the documentation for the versions actually installed there.

Read recipes/ci-strategy/README.md. Keep the project's CI provider and existing protections. Include its current triggers, required checks, available branch protections, local/cloud differences and any merge queue in the plan. Default to Standard when no strategy is specified. Record the selected strategy in AGENTS.md and adapt the existing CI without reducing pre-merge coverage. Prefer existing verification commands; add one unified command only when useful. Do not disable security, migration or deployment workflows to save validation minutes.

If test-ci-review is selected in the optional integrations, follow recipes/test-ci-review/README.md and include it in the initial plan. After setup-plan approval, use the external audit-test-ci skill when a real test/CI setup exists; a new scaffold needs a simple initial strategy and a later revisit, not an automatic full audit or placeholder tests. Missing telemetry stays explicit and can lead to a measurement plan; missing skill access must be reported. The review writes only its report under docs/audits/ and does not authorize changes to tests, workflows, CI strategy, protections or runners, or cloud reruns/paid experiments. Present findings before a separate implementation plan and preserve meaningful coverage and all required gates.

First report a concise plan: the files you would copy or merge, package scripts and dependencies you would add, external integrations and repository secrets that need setup, checks you would run, and any conflicts or product choices that need my input. Wait for my approval before applying the plan.

Follow recipes/scalability-planning/README.md. Unless explicitly omitted, assess relevance from the initial specification and offer lightweight scalability and cost planning in the initial plan. Explain the material cost drivers or why a simple static project needs little further analysis; do not launch an audit merely because it was offered. When enabled or accepted, use audit-scalability-cost in Planning mode before dependent infrastructure decisions. Keep estimates conditional on explicit workload assumptions, verify material provider prices/limits, and include CI/preview costs when relevant. Keep the report under docs/audits/ and promote approved decisions, monitoring and acceptance checks into SPEC.md and milestones separately. Reconcile estimates with an Audit after real usage data is available.

When legal planning is enabled, follow recipes/legal-planning/README.md. After the initial specification and before feature implementation, invoke audit-legal-readiness in Planning mode with a top-tier reasoning model and high reasoning effort or the closest supported equivalent. Announce the known setup and warn if it is weaker or cannot be verified; prioritize thorough research over token savings. If the skill is unavailable, report the missing dependency rather than claiming the review ran. Keep its output under docs/audits/. Present the findings and material open questions before implementing dependent features; incorporate approved requirements into SPEC.md and milestone acceptance checks as a separate planning step. Plan a Pre-launch review against the actual product before release.

After approval, adapt the applicable files without overwriting existing configuration blindly. Write a short root README.md explaining the project and how it works. Complete docs/SPEC.md from known information, reconciling any existing project brief so there is one source of truth; leave unknown product choices as open questions. Keep approved design decisions in docs/design/. Copy and complete template/optional/docs/MILESTONES.md only when the development stages are agreed; define observable acceptance checks and how to verify them for each milestone. Add focused documents such as docs/DEVELOPMENT.md when a procedure is too detailed for the specification. Keep only accurate rules and existing commands in AGENTS.md. Set up formatting, linting, type checking and a production build where applicable. Add test tooling when there is behavior worth testing; do not invent placeholder tests. Run the available checks and summarize the changes, results and unresolved questions.

If the work needs multiple pull requests, deliver one at a time and wait for me to merge or close each PR before starting the next one. Do not open parallel PRs unless I explicitly ask for them.

In Budget-conscious CI, skip draft validation jobs rather than failing them. Run the full suite on ready_for_review and every subsequent ready-state commit. Before any authorized merge, confirm the current revision's ready-state run actually executed and passed all mandatory suites; skipped checks do not prove validation.

For PRs requiring owner actions such as migrations or remote-machine steps, put an IMPORTANT alert at the top of the PR description and repeat it in chat. List who acts, where, the order and timing relative to merge/deployment, verified commands and success checks. Keep pending and completed steps distinct; omit the alert when no action is needed.
```

If the project does not use Next.js, do not copy files from `recipes/next-fullstack/files/`. Use the shared core and a recipe appropriate to its stack.
