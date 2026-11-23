## Seed data

- Layers: reference data in `<migrations or seeds/reference.*>` (every environment, production included); the development seed in `seeds/` (local and staging, never production); test fixtures next to the tests. Tests never depend on the development seed: a test that counts rows or expects an id creates its own data.
- `seeds/README.md` lists the personas and the inventory of seeded scenarios. Read it before adding seed data and keep it true: an entry is `present` only when the seed has it.
- Every state and feature the app has gets an example in the development seed, added in the same PR as the feature, state or rule, like its tests. A bug that depends on production data gets an invented record with the same shape and a regression test, never a copy of real rows.
- Write seed records with scenario ids and obviously invented data on reserved domains (`example.test`). Compute date-dependent states from one `now` at seed time. Use the project's upsert or reset, never a skip-on-conflict insert that can hide rejected rows.
- Run seed commands only against the local database, or staging when the owner asks; never against production. Local sign-in as a persona is for localhost only.
- Every feature PR description has a seed line: `Seed: added <record ids>` or `Seed: not needed because <reason>`. <Optional, stricter: before the first code change of a feature PR, ask the owner in one short question whether the seed needs new examples, and record the answer in the PR.>
