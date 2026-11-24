# Sprint profile

For time-boxed work measured in hours or days: technical assignments, hackathons, experiments and prototypes. The aim is a small, working, verifiable result by the deadline, with nothing lost between sessions.

Sprint keeps everything that protects context: one source of truth, fact status, decision records, handover, scope control, evidence and secret rules (the [core](../../core/AGENTS.md)). It drops the process that protects long-lived code: PR reviews, a CI gate before merge, design and milestone documents, and the full audit set.

**The trade-off:** without CI and review, nothing independent checks the work. The local verify command, test-first core logic and the evidence in `docs/STATUS.md` replace them. That is acceptable for hours or days, not for software people depend on.

## Set up in five minutes

1. Create the project with its official generator (for Next.js see the [Next.js recipe](../../../recipes/next-fullstack/README.md), steps 1–5 only).
2. Copy the core and this profile, including dotfiles:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/core/ /absolute/path/to/project/
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/profiles/sprint/files/ /absolute/path/to/project/
   ```

3. Paste this profile's [AGENTS section](AGENTS-section.md) where the core `AGENTS.md` says so. Generators often create their own files, which the copy then skips:
   - `AGENTS.md` (Next.js 16): keep its block and add the pack's content below it.
   - `README.md`: replace it with this profile's [README template](files/README.md); it is a deliverable, not generator boilerplate.
4. Give an agent the prompt below, or fill in the placeholders yourself.

```text
This is a Sprint project (starter pack, template/profiles/sprint).
The brief: <paste the assignment or describe the goal>.
Deadline: <date, time and time zone>. Stack: <stack>.
Git remote: <git@HOST_ALIAS:OWNER/REPOSITORY.git>.

Fill in AGENTS.md (Governance with profile Sprint, the pack revision, risk
triggers that apply, the deadline, the verify command and the remote) and
docs/SPEC.md (goal, acceptance criteria, non-goals, facts with status, deferred
work) from the brief only. Mark everything not stated in the brief as an
assumption. Add a verify script that runs format, lint, typecheck, tests and
build. Write docs/STATUS.md. Then show me the acceptance criteria, assumptions
and the tests you plan to write first, and wait for my approval before
implementing.
```

## Recipes and audits

- **Recipes:** none by default. Add one only when the work needs it; [seed data](../../../recipes/seed-data/README.md) when there is a database.
- **Audits:** before handing in, `audit-security` for secrets and input handling and `audit-correctness` on the core logic, from the AI Audit Toolkit. A risk trigger in the core can call for more.
- **CI:** optional. One workflow that runs the verify command is enough; a green run can matter to someone reviewing an assignment.

## When it outgrows the profile

Signs: the deadline keeps moving, real users arrive, a second person joins, or the work will be maintained. Ask the owner to move the project to MVP. The upgrade adds mechanisms to what exists and never resets the project.
