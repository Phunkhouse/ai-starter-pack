# Prompt for starting a project with an agent

Copy this prompt into Claude Code or Codex while working in the **new target repository**. Fill in the paths and a short description of the application. The agent needs access to both locations.

```text
I am starting a new application: <one to three sentences about its purpose and users>.

The starter pack is at <absolute path to ai-starter-pack>.
The target repository is at <absolute path to the new repository>.
The relevant recipe is <recipe name, or none>.
The optional integrations are <integration recipe names, or none>.

Read the starter pack README.md, template/core/ and the selected recipes. Inspect the target repository and the documentation for the versions actually installed there.

First report a concise plan: the files you would copy or merge, package scripts and dependencies you would add, external integrations and repository secrets that need setup, checks you would run, and any conflicts or product choices that need my input. Wait for my approval before applying the plan.

After approval, adapt the applicable files without overwriting existing configuration blindly. Write a short root README.md explaining the project and how it works. Complete docs/SPEC.md from known information, reconciling any existing project brief so there is one source of truth; leave unknown product choices as open questions. Keep approved design decisions in docs/design/. Copy and complete template/optional/docs/MILESTONES.md only when the development stages are agreed; define observable acceptance checks and how to verify them for each milestone. Add focused documents such as docs/DEVELOPMENT.md when a procedure is too detailed for the specification. Keep only accurate rules and existing commands in AGENTS.md. Set up formatting, linting, type checking and a production build where applicable. Add test tooling when there is behavior worth testing; do not invent placeholder tests. Run the available checks and summarize the changes, results and unresolved questions.

If the work needs multiple pull requests, deliver one at a time and wait for me to merge or close each PR before starting the next one. Do not open parallel PRs unless I explicitly ask for them.
```

If the project does not use Next.js, do not copy files from `recipes/next-fullstack/files/`. Use the shared core and a recipe appropriate to its stack.
