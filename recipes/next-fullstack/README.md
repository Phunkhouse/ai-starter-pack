# Next.js full-stack recipe

An optional profile for a new TypeScript application. Lucy's Bookshop used Next.js 16 when this recipe was drafted. Check the docs in the target project's installed `node_modules/next/dist/docs/` before writing Next.js code or adopting these configuration files; paths and APIs can change between versions.

## Foundation

1. Generate a fresh App Router project with `src/`, TypeScript, pnpm and no Tailwind. Keep the generator's `package.json`, lockfile, `tsconfig.json` and `next.config.ts` as the starting point.
2. Copy `template/core/` as described in the pack's root README. Inspect the optional files in this recipe's `files/` directory. To copy files that do not yet exist, including dotfiles, use `rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/recipes/next-fullstack/files/ /absolute/path/to/new-project/`. Compare an existing ESLint config or CI workflow before merging.
3. Set the new project's `packageManager` field to the exact pnpm version used to create its lockfile. This recipe includes `.nvmrc` with Node 24 as its initial choice; change it and the CI version together if the project needs another supported version.
4. Install Prettier as a dev dependency at a deliberate exact version. This recipe uses `semi: false` and `singleQuote: true`, following Lucy's Bookshop. Change the preference before the first commit if needed. The generator should provide compatible `eslint` and `eslint-config-next` dependencies for its Next.js version.
5. Add scripts in the new `package.json`: `lint: eslint .`, `typecheck: next typegen && tsc --noEmit`, `format: prettier --write .`, `format:check: prettier --check .`. Add a `test` script when there are tests. Next.js 16 runs ESLint directly; `next lint` was removed.
6. Adapt the included pull-request CI workflow to the scripts actually installed. It runs format, lint, typecheck, optional tests and build. Add required services only when tests or the build need them. Keep branch protection aligned with the job name. CI is the required gate; a pre-commit hook is optional.

## Architecture

- Start with route files and components. Create `src/server/` when there is real business logic to isolate. If created, enforce its framework boundary with `no-restricted-imports` in ESLint.
- Keep route handlers and server actions thin: parse input, call services and return a result. Recompute trusted values on the server.
- Add database migrations and integration tests when the application has a database. The database and migration tool are project choices, not starter defaults.

## UI and CSS

- CSS Modules plus SCSS are a suitable default when the project needs component-scoped styles and a few Sass utilities. Install `sass` only if selected. Next.js supports `.module.scss` after installing it.
- Put design tokens in CSS custom properties. Keep global CSS to tokens, resets and document-level defaults; put component styles beside components.
- Use semantic elements, visible `:focus-visible` states and responsive layouts. Decide whether the project needs i18n before placing interface text directly in components.

## Tests

- Add Vitest unit tests for business rules when they exist, component tests with Testing Library for interactive UI, and a few Playwright tests for critical end-to-end flows.
- Test async Server Components via end-to-end tests; the Next.js Vitest guide does not support them directly.
- Add real database integration tests for transactional and concurrency risks. Do not copy Lucy's Bookshop's backup restore drill without that requirement.

## References to check when applying

- The guide paths above were verified in Lucy's Bookshop's installed Next.js 16 package: `01-app/03-api-reference/05-config/03-eslint.md`, `01-app/02-guides/sass.md` and `01-app/02-guides/testing/vitest.md` under `node_modules/next/dist/docs/`. Find their equivalents in the target project; do not assume the same paths exist in a later version.
