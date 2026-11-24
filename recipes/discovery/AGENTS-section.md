## Discovery handover

- `docs/discovery/<slug>/handover.md` is where this project's goal, scope, acceptance criteria, assumptions and decisions came from; `brief.md` beside it records why. `docs/SPEC.md` is the source of truth for what is built.
- Keep discovery IDs (`AC-`, `A-`, `D-`) in SPEC entries. Assumptions from the handover stay `assumption` until the owner confirms the fact or a reliable source verifies it.
- Handover non-goals and deferred work stay out of scope unless the owner moves them in.
- If implementation shows a discovery assumption is wrong or a criterion cannot be met, stop and tell the owner. Changes to the problem, scope or criteria go back through discovery (the brief, then a regenerated handover), then the SPEC. Never edit `handover.md` by hand.
