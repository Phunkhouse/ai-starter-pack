# Assumptions register

Every working assumption and confirmed fact the product depends on, in one place. Approving a plan does not confirm an assumption: it stays open until the owner explicitly confirms the underlying fact or a reliable source verifies it.

When an entry changes, update the rules and tests that depend on it in the same change.

## Confirmed

| Id   | Fact or decision         | Source and date           | Depends on it           |
| ---- | ------------------------ | ------------------------- | ----------------------- |
| C-01 | <What is known for sure> | <Who or what, YYYY-MM-DD> | <Rules, specs or tests> |

## Open

| Id   | Working assumption | Depends on it           | How it gets confirmed                     |
| ---- | ------------------ | ----------------------- | ----------------------------------------- |
| O-01 | <What is assumed>  | <Rules, specs or tests> | <Who confirms it, or the evidence needed> |

## Disproved

| Id  | Assumption | What showed it wrong, and when | What changed |
| --- | ---------- | ------------------------------ | ------------ |
