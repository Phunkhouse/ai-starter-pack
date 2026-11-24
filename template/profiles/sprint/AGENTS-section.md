## Sprint profile

- **Time box:** the deadline, goal, acceptance criteria, non-goals and deferred work are in `docs/SPEC.md`. When the remaining work will not fit before the deadline, stop and propose what to cut or defer; never widen the scope or move the deadline yourself. When the owner cuts or defers something, move it to Deferred, add a decision-log line and update `docs/STATUS.md`, in one commit.
- **One approval before code:** before implementing any behavior, present the acceptance criteria, the assumptions and the planned tests together and wait for the owner's approval. Record it in the decision log, and mark each approved assumption confirmed (owner, date). A changed criterion is approved the same way.
- **Tests first:** after approval, add the test runner and a `test` script if the project has none, write the approved tests for business logic and the critical path, see them fail, then implement until they pass. Skip tests for trivial glue code. Never add placeholder tests.
- **Checks:** `<verify command>` runs `<format:check, lint, typecheck, test and build>` and changes no files. Until the first approved tests exist it runs the other checks; from then on it includes `test`, and a run without tests does not count. Every commit you report as done passes it. CI: `<none | one workflow that runs the verify command>`.
- **Decisions:** one line each in the decision log in `docs/SPEC.md`. A decision a reviewer would ask about also goes into the README's trade-offs.
- **Git:** `<commit straight to main | short branches merged by the owner>`. Each commit is one meaningful step that leaves the checks passing. No PR reviews unless the owner asks. Never rewrite pushed history.
- **README is a deliverable:** how to run it, what was built, decisions and trade-offs, limitations and deferred work. Keep it current as you go, not at the end.
- **AI usage**, when the owner wants it recorded: a short, curated README section on where AI helped, where it was wrong and how its output was checked. Not a running log.
- **Deploy:** `<none | the simplest documented way>`, described in the README.
