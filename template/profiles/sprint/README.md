# Sprint profile

For time-boxed work measured in hours or days: technical assignments, hackathons, experiments and prototypes. The aim is a small, working, verifiable result by the deadline, with nothing lost between sessions.

Sprint keeps everything that protects context: one source of truth, fact status, decision records, handover, scope control, evidence and secret rules (the [core](../../core/AGENTS.md)). It drops the process that protects long-lived code: PR reviews, a CI gate before merge, design and milestone documents, and the full audit set.

**The trade-off:** without CI and review, nothing independent checks the work. The local verify command, test-first core logic and the evidence in `docs/STATUS.md` replace them. That is acceptable for hours or days, not for software people depend on.

## Set up

The order matters. Setup ends with a passing `verify` and one approval; tests and behavior come after that approval.

**How long it takes.** On a disposable Next.js project with a short brief (2026-11-24, packages already in the local pnpm store), the mechanical steps 1–4 took about 10 seconds and the first `verify` about 7 seconds. A cold install adds download time. Filling in the specification from a brief is judgement work and depends on the brief; a few minutes is realistic for a short assignment, but the whole setup has not been timed end to end with a real brief, so treat "under five minutes" as a target, not a measurement.

1. **Generate the project** with its official generator. For Next.js, follow the [Next.js recipe](../../../recipes/next-fullstack/README.md) steps 1–5: the generator, `packageManager`, Prettier at an exact version, and the `lint`, `typecheck`, `format` and `format:check` scripts. Skip its CI step unless the owner wants CI.
2. **Copy the core and this profile**, including dotfiles:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/core/ /absolute/path/to/project/
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/template/profiles/sprint/files/ /absolute/path/to/project/
   ```

3. **Compose `AGENTS.md`:** paste this profile's [AGENTS section](AGENTS-section.md) where the core `AGENTS.md` says so. Generators often create their own files, which the copy then skips:
   - `AGENTS.md` (Next.js 16): keep its block and add the pack's content below it.
   - `README.md`: replace it with this profile's [README template](files/README.md); it is a deliverable, not generator boilerplate.
4. **Add `verify`** with only the checks that can run on a project without tests. It must change no files, so it uses `format:check`, never `format`. For Next.js:

   ```json
   "verify": "pnpm format:check && pnpm lint && pnpm typecheck && pnpm build"
   ```

   Generator output does not follow the recipe's Prettier style, so run `pnpm format` once, then `pnpm verify`, and commit the result as the starting point.

5. **Hand over to an agent** with the prompt below. It fills in the placeholders and ends at the single approval: acceptance criteria, assumptions and planned tests together.
6. **After approval, tests first:** the agent adds the test runner and a `test` script (for Next.js, Vitest as the installed version's testing guide describes), writes the approved tests, sees them fail, and adds `pnpm test` to `verify` before `build`. From then on a `verify` without tests does not count.

```text
This is a Sprint project (starter pack, template/profiles/sprint).
The brief: <paste the assignment or describe the goal>.
Deadline: <date, time and time zone>. Stack: <stack>.
Git remote: <git@HOST_ALIAS:OWNER/REPOSITORY.git>.

Read AGENTS.md, then fill in from the brief only:
- AGENTS.md: Governance (profile Sprint, pack revision, risk triggers that
  apply), the verify command, the Git remote;
- docs/SPEC.md: goal, deadline, acceptance criteria, planned tests, non-goals,
  facts with status, deferred work. Everything the brief does not state is an
  assumption.
Run verify and write docs/STATUS.md with what it covered. Then present the
acceptance criteria, assumptions and planned tests together and wait for my
approval. Do not add a test runner or any behavior before I approve.
```

## Recipes and audits

- **Recipes:** none by default. Add one only when the work needs it; [seed data](../../../recipes/seed-data/README.md) when there is a database.
- **Audits:** before handing in, `audit-security` for secrets and input handling and `audit-correctness` on the core logic, from the AI Audit Toolkit. A risk trigger in the core can call for more.
- **CI:** optional. One workflow that runs the verify command is enough; a green run can matter to someone reviewing an assignment.

## When it outgrows the profile

Signs: the deadline keeps moving, real users arrive, a second person joins, or the work will be maintained. Ask the owner to move the project to MVP. The upgrade adds mechanisms to what exists and never resets the project.
