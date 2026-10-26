# Playwright E2E CI recipe

Guidance for keeping Playwright end-to-end tests reliable without making CI setup unnecessarily slow. The included workflow is an **optional container variant**, not a default replacement for a fast, verified runner-based job. Measure the complete E2E job, including dependency setup, browser setup, services and tests, before changing its environment.

## Choose the CI environment

1. Keep an existing runner-based job if browser setup and the full E2E run are already fast and reliable. If `playwright install --with-deps` is slow because of `apt`, first try installing only the browsers the suite uses. Omitting `--with-deps` can be faster when the chosen runner image already has every required system library and font. Verify browser startup, test results and font-sensitive output on CI before relying on that shortcut. Pin an Ubuntu release rather than `ubuntu-latest`, and recheck after runner image updates.
2. Use the [container workflow](files/.github/workflows/e2e.yml) when system dependencies are missing, `apt` remains unstable, or a consistent browser environment is worth the image-pull and integration cost. The official Playwright image includes browsers and Linux browser dependencies, so this variant does not run `playwright install --with-deps`. A fresh GitHub-hosted runner still has to pull the image, which can outweigh a short host install.
3. Cache browser binaries only after measuring both a cache miss and a cache hit. Playwright [does not recommend browser caching](https://playwright.dev/docs/ci#caching-browsers) by default: restoring the cache can take as long as downloading browsers, and it cannot cache Linux system packages. If the browser download is already quick, omit the cache.

After verifying that the runner has the required dependencies, a Chromium-only host job can use this step instead of `--with-deps`:

```yaml
- name: Install Chromium
  run: pnpm exec playwright install chromium
  timeout-minutes: 5
```

## Add the container variant

1. Install `@playwright/test` at an exact version and commit the lockfile. Add a `test:e2e` script that runs the configured Playwright suite, for example `playwright test`. Keep browser tests out of the fast `test` script used by the main CI job.
2. Set the container tag in [the workflow](files/.github/workflows/e2e.yml) to **exactly** the installed Playwright version. The included tag is an example, not a version to impose on the project. Update the package and image tag together in dependency update PRs; do not assume Dependabot keeps them synchronized. Playwright requires the browser binaries in the image to match the package version.
3. Inspect any existing E2E workflow, then copy this recipe's files without overwriting existing files:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/recipes/playwright-e2e/files/ /absolute/path/to/new-project/
   ```

   Adapt the web server, database or other services, environment variables, test script and timeout to the project. In a container job, a service such as Postgres is reached by its service name and container port (for example `postgres:5432`), rather than a host-mapped address such as `localhost:5433`. Review database URLs, Playwright configuration and file permissions for the container user. If the repository already has a workflow for browser tests, replace or merge it instead of running two suites.
4. Run the workflow on a PR. Confirm that browsers launch, the suite passes and any screenshot or font-sensitive checks still behave as expected. Compare a cold run and a subsequent run, including image pull and dependency installation time.

The E2E job is separate from the main format, lint, typecheck, unit test and build checks. The container workflow does not cache browser binaries or call `playwright install --with-deps`. Playwright's [Docker image](https://playwright.dev/docs/docker) includes the browsers and system dependencies but not the Playwright package, which is installed from the project's lockfile. GitHub documents the [different service hostnames for runner and container jobs](https://docs.github.com/en/actions/tutorials/use-containerized-services/use-docker-service-containers).

For a runner-based job, consider Playwright's `--only-shell` option for headless Chromium and install only the browser projects the suite uses. If a measured browser cache helps, key it by Playwright version and operating system. See Playwright's [CI](https://playwright.dev/docs/ci) and [browser installation](https://playwright.dev/docs/browsers) guides.
