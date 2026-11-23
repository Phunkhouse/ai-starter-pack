# Seed data

Copy to the target project's `seeds/README.md` and replace the examples. This file is the inventory of what the development seed shows; keep it true. Rules: the project's `AGENTS.md` ("Seed data").

## Commands

| Command | Does |
| --- | --- |
| `<pnpm db:reset>` | Drops the local database, applies migrations, reference and development seeds. |
| `<pnpm dev>` | Resets when migrations or seeds changed, then starts the app. |
| `<pnpm db:seed:volume>` | Optional: adds generated volume data locally. |
| `<staging command>` | Staging only, on the owner's word. Refresh policy: <reset on deploy / by hand / kept>. |

## Personas

Sign in locally at `<local sign-in URL>`.

| Persona | Id | Shows |
| --- | --- | --- |
| Owner | `usr-owner` | All administration screens. |
| Customer with history | `usr-customer-history` | Past orders, repeat order, usual goods. |
| New customer | `usr-customer-new` | Empty states and first-order flow. |

## Inventory

Enum values are covered by the coverage test automatically; list here only shapes no enum expresses.

| Scenario | Record | How to see it | Status |
| --- | --- | --- | --- |
| Negotiated price and own margin on one organisation | `org-deal-and-own-margin` | Customer with history → catalogue | present |
| Order changed by the owner after submission | `ord-changed-by-owner` | Customer with history → orders | comes with <feature> |
| Day closed for deliveries | `day-closed-holiday` | Owner → calendar | comes with <feature> |
