# Seed data for local development

Optional policy for projects with a database. The goal: anyone, human or agent, can run the app locally and see every state and feature it has, on invented data, in seconds. That keeps local testing, review and bug reproduction easy without ever touching production data. The recipe works with any database, migration tool or framework; it prescribes no seed tool.

Adopt it when the project gets its first migration, or later when local testing starts to need hand-made data. Paste the [AGENTS snippet](AGENTS-section.md) into the target `AGENTS.md`, and keep the project's own inventory, personas and commands next to its seed, starting from the [seeds README example](examples/seeds-README.md).

## Quick path

1. Split data by purpose into the [layers](#layers) below, and give each layer one command.
2. Add `db:reset`, and make the dev command use it: [Commands](#commands).
3. Name seeded records by scenario and list them in `seeds/README.md`: [Writing seeds](#writing-seeds).
4. Add a test that loads every seed and checks coverage: [Coverage](#coverage).
5. Add the target guard and the fake-data rules: [Safety](#safety).
6. Add the seed line to the PR template: [Process](#process).

## Layers

| Layer | Holds | Runs on | Typical home |
| --- | --- | --- | --- |
| Reference | Data the app cannot run without: categories, roles, price groups, settings rows. | Every environment, production included. | Migrations, or a reference seed that is safe to repeat. |
| Development | One example of every state and feature, plus personas to sign in as. | Local, and staging when it is used for review. Never production. | `seeds/` |
| Volume (optional) | Many generated rows for pagination, reports and performance. | Local on request. | `seeds/`, behind its own command |
| Test fixtures | The minimum each test needs, built by the test or a factory. | Unit and integration tests. | Next to the tests |
| End-to-end scenarios | Named states a browser test starts from, such as sessions. | The throwaway end-to-end database. | Next to the end-to-end tests |

Tests never depend on the development seed. A test that counts rows or expects a specific id creates its own data, so the seed can grow without breaking tests.

## Commands

- `db:reset` drops the local database, applies all migrations, then the reference and development seeds. It should finish in seconds; it is the normal way to get a fresh local state.
- The dev command (for example `pnpm dev`) resets when migrations or seed files changed since the last run, for instance by storing a hash of them next to the local database, and otherwise keeps local data.
- `db:seed:volume` (optional) adds the volume layer to an already seeded local database.
- Staging, when seeded, uses an explicit command and an upsert (`INSERT … ON CONFLICT DO UPDATE` or the tool's equivalent) so seed changes reach existing rows. Write down in the runbook whether staging is reset on each deploy, refreshed by hand or kept as it is.

Prefer rebuilding over patching. Avoid SQLite's `INSERT OR IGNORE` and similar "skip on conflict" forms: they keep stale rows when a seed changes, and SQLite's also drops rows that break a CHECK or NOT NULL constraint without any error.

## Writing seeds

- **Name records after the scenario they show.** Use ids such as `org-deal-and-own-margin` or `ord-changed-by-owner`, and display names that read as invented. A scenario nobody can find is not useful.
- **Personas.** Seed one user per role and per interesting situation (new customer, customer with history, owner). The local sign-in lists them, and `seeds/README.md` says what each one shows.
- **Build seeds from code once they grow.** Plain SQL is fine for small reference data. A larger development seed is better as a script that uses the app's typed insert layer or its test factories, so a schema change shows up as a type or constraint error instead of a silently wrong row.
- **Compute time from one `now`.** States that depend on the date (closes tomorrow, overdue, expired) are computed at seed time, so they stay true whenever someone resets. Keep fixed dates only for history that is meant to be in the past.
- **Stay deterministic.** Fixed, readable ids. A random generator, when used for volume, gets a fixed seed. Hand-written records for the example states; generated rows only for volume.
- **Keep it fast.** The default seed is small enough that a reset takes seconds. Volume goes in its own layer.

## Coverage

Two checks keep the development seed showing everything the app can do.

1. **Automatic: every enum value appears.** A test loads all seeds into a fresh database through the same commands developers use and asserts that every value of every status or enum column appears at least once. A new state then fails CI until the seed shows it, and a seed row dropped by a constraint fails it too. See [the example test](examples/seed-coverage.test.ts).
2. **Manual: the inventory.** `seeds/README.md` lists shapes no enum expresses, such as "an order the owner changed" or "a closed day", each with its record id, how to see it (persona and page) and its status: `present` or `comes with <feature>`. Keep the inventory next to the seed, not in `AGENTS.md`, so it cannot claim states the seed does not have.

The coverage test also runs against the newest migration on every PR, so a schema change cannot break the local setup unnoticed.

## Safety

- **The seed script checks its target.** It refuses any database that is not local unless it receives an explicit staging flag, and it never accepts production. Check the actual connection (host, binding or database name), not only an environment variable that might be set wrong.
- **Local sign-in is gated twice.** A development sign-in route (sign in as a persona without email) is left out of production builds by a build-time flag, and at runtime also requires a local-only variable that no deployed configuration sets and a localhost request. A test asserts that it answers 404 without them.
- **Data is invented and looks invented.** Reserved domains (`example.test`, `.invalid`), obviously fictional names, no real phone numbers, bank accounts, addresses or company identifiers. Never copy production rows, not even to reproduce a bug.
- **Email never leaves a developer's machine.** Locally, mail goes to a capture file or the outbox table. On staging, synthetic recipients on reserved domains cannot receive mail and may count as bounces against the sender's reputation, so route staging mail to the provider's test or sandbox addresses or to an allowlist of real inboxes, following the provider's current documentation.
- **Production bugs come back as invented shapes.** When a bug depends on production data, describe its shape (states, counts, edge values), add an invented record with that shape and a regression test, then fix it. Copying production data to a developer machine is a separate decision with its own anonymisation step; for personal data it is a data protection question, not a convenience.

## Process

- **A seed line in every feature PR.** The PR description says `Seed: added <record ids>` or `Seed: not needed because <reason>`. The reviewer sees it, and the coverage test catches what the line misses. A project that wants a stricter rule can have agents ask the owner about the seed before their first code change; record that choice in the snippet.
- **Seed changes ship with the change that needs them.** A feature, state or rule adds its example in the same PR, like its tests. A migration that changes the data shape updates the seed in the same PR.
- **Test risky migrations on populated data.** Production may start empty while local databases are seeded, so test a migration that rewrites tables against both an empty database and a seeded one.

## Adopt in an existing project

1. Inventory what exists: seed files, fixtures, local scripts, staging data and how each is applied. Note which tests depend on seed data.
2. Propose the layer split and commands to the owner, including what staging gets and how it is refreshed. Wait for agreement before moving data or changing commands.
3. Add the coverage test first, against the current seed, and record which states are missing in `seeds/README.md` as `comes with` or as gaps to fill.
4. Fill the gaps in focused PRs, one area at a time, following the project's PR cadence.

## Acceptance checks

- [ ] A fresh clone gets a fully seeded local app with the documented commands, and `db:reset` finishes in seconds.
- [ ] The coverage test loads every seed through the real commands and fails when a status value is missing from the seed or a seed row is rejected.
- [ ] The seed script refuses a production target, and a staging target without the explicit flag.
- [ ] The local sign-in answers 404 in a production build, without the local variable, and on a non-localhost host.
- [ ] Every persona and inventory entry in `seeds/README.md` exists in the seed; entries not yet built are marked `comes with`.
- [ ] No seed contains real personal data, real company identifiers or deliverable addresses, and staging mail cannot reach a synthetic recipient.

## Status of these practices

The layers, invented data, local-only scripts that refuse other databases, the gated local sign-in and test independence are in use in several projects. The feature-parity coverage rule and the seed line in PRs started in one project in November 2026 and are still on trial; revisit them after a few feature PRs.
