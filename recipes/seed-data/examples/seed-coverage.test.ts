// Example only: adapt names, imports and the database setup to the project.
// Load every seed through the same commands developers use, then check that
// each status or enum value appears at least once. A new state fails this test
// until the seed shows it, and so does a seed row the database rejected.
import { describe, expect, it } from 'vitest'

// Replace with the project's own helpers: a fresh, throwaway database with all
// migrations, then the reference and development seeds applied exactly as
// `db:reset` applies them.
import { createSeededTestDb } from '../src/db/testing'
// Single source of truth for allowed values, shared with the schema.
import { ORDER_SOURCES, ORDER_STATUSES } from '../src/db/schema'

const covered = [
  { table: 'order', column: 'status', values: ORDER_STATUSES },
  { table: 'order', column: 'source', values: ORDER_SOURCES },
] as const

describe('development seed', () => {
  it.each(covered)('has every $table.$column value', async ({ table, column, values }) => {
    const db = await createSeededTestDb()
    const rows = await db.query<{ value: string }>(
      `select distinct "${column}" as value from "${table}"`,
    )
    const present = new Set(rows.map((row) => row.value))
    expect(values.filter((value) => !present.has(value))).toEqual([])
  })

  it('keeps every inventory record', async () => {
    const db = await createSeededTestDb()
    // Ids from seeds/README.md marked `present`; a rejected row fails here.
    // Entries marked `comes with <feature>` join this list in that feature's PR.
    const expected = ['org-deal-and-own-margin']
    const rows = await db.query<{ id: string }>(
      `select id from "organisation" union all select id from "order"`,
    )
    const ids = new Set(rows.map((row) => row.id))
    expect(expected.filter((id) => !ids.has(id))).toEqual([])
  })
})
