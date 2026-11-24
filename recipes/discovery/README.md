# Discovery handover

Use before the first specification when the problem, the users or the scope are not settled yet, and whenever a project starts from a discovery handover. It connects the external [AI Discovery Toolkit](https://github.com/Phunkhouse/ai-discovery-toolkit), which decides *what* to build and *whether* to, with the pack's governance of *how* it is built. This recipe coordinates the toolkit's Skills rather than copying its method.

## When to offer it

Offer it at setup when the brief describes a solution without a confirmed problem ("build us an app"), several stakeholders want different things, the owner is unsure what to build first, or a wrong guess would be expensive. Skip it when the brief already states the goal, scope and acceptance criteria, or when a discovery handover is supplied: then use the handover directly (step 3).

Discovery depth is independent of the governance profile. A Sprint usually needs only **Rapid** Discovery (10–30 minutes); a new product or a client engagement usually needs **Standard**. A small feature in a Production project can still need only Rapid.

## Dependency

Install the toolkit once per machine. Its installer links the Skills from a local clone into `~/.claude/skills` and `~/.agents/skills`; `git pull` in the clone updates them:

```sh
git clone https://github.com/Phunkhouse/ai-discovery-toolkit.git <TOOLKIT_DIR>
cd <TOOLKIT_DIR> && ./scripts/install.sh
```

The handover is plain Markdown, so a project that received a handover from someone else needs no installation to use it. If a Skill is missing when discovery is wanted, report that dependency rather than improvising a discovery.

## Workflow

1. **Discover.** In the target repository (or any folder, before the repository exists; move `docs/discovery/` into it later), run `discovery-rapid` or `discovery-standard` with the brief. The output is `docs/discovery/<slug>/brief.md`. The owner approves the problem, direction, scope and acceptance criteria in chat.
2. **Hand over.** When approved, run `discovery-handover` (or ask the discovery Skill to hand over). It checks a readiness gate and writes `docs/discovery/<slug>/handover.md`. If the recommended direction is not a build (a process change, an existing product, a validation test, don't build), stop here: there is nothing for this pack to set up yet.
3. **Specify.** Fill `docs/SPEC.md` (and, in MVP, `docs/assumptions.md`) from the handover following the toolkit's [handover contract](https://github.com/Phunkhouse/ai-discovery-toolkit/blob/main/docs/ecosystem.md#the-handover-contract). In the pack's terms:
   - acceptance criteria keep their `AC-` IDs;
   - confirmed facts and approved requirements become `confirmed`, approved decisions `decided`, open or accepted assumptions `assumption` (MVP: Open, with how each gets confirmed);
   - non-goals stay non-goals; deferred work goes to Deferred or the backlog;
   - put the discovery ID in the source column ("discovery brief A-3") so the trail survives.

   Do not add requirements, criteria or rationale the handover does not contain; list anything missing as an open question.
4. **Govern.** Paste this recipe's [AGENTS snippet](AGENTS-section.md) into the target `AGENTS.md`. For a Sprint, the set-up prompt's "The brief" can simply name `docs/discovery/<slug>/handover.md`.

## Keeping them in step

- `docs/SPEC.md` is the source of truth for what is built. `brief.md` stays as the record of why; it is not kept in step afterwards.
- When building shows that a discovery assumption is wrong or a criterion cannot be met, the change goes back through discovery: the owner decides in the brief, the handover is regenerated, then the SPEC is updated. `handover.md` is never edited by hand.
- A handover whose source date is older than its brief's `Updated` date is stale; regenerate it with `discovery-handover` before relying on it.

## Integration checks

- The SPEC's goal, scope, non-goals and acceptance criteria can each be traced to a handover entry, and nothing in them is absent from the handover.
- Open assumptions from the handover appear as assumptions, not as confirmed facts.
- Deferred work and non-goals from the handover are not in the current scope unless the owner moved them there.
- A non-build recommendation did not lead to a project being set up anyway.
