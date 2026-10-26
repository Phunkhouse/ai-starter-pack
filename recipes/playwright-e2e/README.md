# Playwright E2E CI recipe

An optional GitHub Actions job for projects with Playwright end-to-end tests. It runs in the official Playwright container, which includes browsers and Linux browser dependencies. This avoids running `apt` through `playwright install --with-deps` on each GitHub-hosted runner. The image still has to be pulled, so compare complete job times before calling it faster.

## Add it to a project

1. Install `@playwright/test` at an exact version and commit the lockfile. Add a `test:e2e` script that runs the configured Playwright suite, for example `playwright test`. Keep browser tests out of the fast `test` script used by the main CI job.
2. Set the container tag in [the workflow](files/.github/workflows/e2e.yml) to **exactly** the installed Playwright version. The included tag is an example, not a version to impose on the project. Playwright requires the browser binaries in the image to match the package version.
3. Inspect any existing E2E workflow, then copy this recipe's files without overwriting existing files:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/recipes/playwright-e2e/files/ /absolute/path/to/new-project/
   ```

   Adapt the web server, database or other services, environment variables, test script and timeout to the project. If the repository already has a workflow for browser tests, merge this approach into it instead of running two suites.
4. Run the workflow on a PR. Confirm that browsers launch, the suite passes and any screenshot or font-sensitive checks still behave as expected. Compare a cold run and a subsequent run, including image pull and dependency installation time.

The E2E job is separate from the main format, lint, typecheck, unit test and build checks. It does not cache browser binaries or call `playwright install --with-deps`. Playwright [does not recommend browser caching](https://playwright.dev/docs/ci#caching-browsers) as a default CI optimization because cache restore can take as long as downloading the browsers, while Linux system dependencies are not cached. Its [Docker image](https://playwright.dev/docs/docker) includes the browsers and system dependencies but not the Playwright package, which is installed from the project's lockfile.

If a container is unsuitable, first measure where the time goes. Limit installation to the browsers actually used and consider Playwright's `--only-shell` option for headless Chromium. Skipping `--with-deps` on a hosted runner is a project-specific optimization: verify browser startup and font-dependent output on the chosen runner image, and recheck after runner image changes. Cache browser binaries only if measured download time justifies cache restore time; key the cache by the Playwright version and operating system. See Playwright's [CI](https://playwright.dev/docs/ci) and [browser installation](https://playwright.dev/docs/browsers) guides.
