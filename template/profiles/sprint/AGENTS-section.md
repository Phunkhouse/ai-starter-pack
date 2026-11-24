## Sprint profile

- **Time box:** deadline `<date, time and time zone>`. Goal, acceptance criteria, non-goals and deferred work are in `docs/SPEC.md`. When the remaining work will not fit before the deadline, stop and propose what to cut or defer; never widen the scope or move the deadline yourself.
- **Decisions:** one line each in the decision log in `docs/SPEC.md` (date, decision, reason, status). A decision a reviewer would ask about also goes into the README's trade-offs.
- **Tests:** write the tests for business logic and the critical path first and show them to the owner before implementing. Skip tests for trivial glue code. Never add placeholder tests.
- **Checks:** `<verify command>` runs `<format, lint, typecheck, tests and build>`. Every commit you report as done passes it. CI: `<none | one workflow that runs the verify command>`.
- **Git:** commit straight to `main` or use short branches, as the owner prefers. Each commit is one meaningful step that leaves the checks passing. No PR reviews unless the owner asks. Never rewrite pushed history.
- **README is a deliverable:** how to run it, what was built, decisions and trade-offs, limitations and deferred work. Keep it current as you go, not at the end.
- **AI usage**, when the owner wants it recorded: a short, curated README section on where AI helped, where it was wrong and how its output was checked. Not a running log.
- **Deploy:** `<none | the simplest documented way>`, described in the README.
