# Self-hosted CI runner

An optional, owner-managed Linux runner for trusted private repositories that exhaust their included GitHub Actions compute. Oracle Cloud Always Free ARM is the primary example; a paid Linux VM or a dedicated home machine works too. Runner location is independent of the [Standard or Budget-conscious strategy](../ci-strategy/README.md): choose when validation runs separately from where it runs. Required validation and user control over readiness/merge stay unchanged.

For execution improvements after runner adoption, use [CI execution performance](../ci-performance/README.md) with either CI strategy. Its [Kultomat case study](../ci-performance/case-study.md) records source-verified job/step timings and attribution limits. Results depend on the project and run conditions. This recipe provisions nothing automatically.

## Suitability and security

Use this persistent-machine recipe only for private repositories whose code, contributors, dependencies and workflow changes you trust. Do not use it for public/fork PR code. Private status alone is not an isolation boundary: an untrusted collaborator or compromised dependency can control the machine. GitHub recommends private repositories for self-hosting because public fork PRs can execute dangerous code ([adding runners](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners), read **2026-11-06**).

- Register each runner at repository level, or use organization runner groups restricted to the intended repositories. Labels route jobs; they are not access controls. Keep workflows with sensitive credentials, such as Claude PR review or deployments, explicitly on GitHub-hosted runners. Do not replace `runs-on` globally or use `pull_request_target` to execute PR code.
- Use a single-purpose VM with no production data, cloud API keys, SSH private keys or privileged instance identity. Restrict network access to other systems, including the home LAN. Persistent workspaces and caches can retain malicious changes or secrets between jobs; another runner folder/user on the same Docker host does not isolate repositories.
- Docker-group membership grants root-level control. Accept that only for this dedicated machine and its trusted jobs; the absence of passwordless sudo does not contain a job with Docker access ([Docker post-installation](https://docs.docker.com/engine/install/linux-postinstall/), read **2026-11-06**). Remove a compromised runner and rebuild its host; cleaning the checkout alone is insufficient.

## Costs and machine options

Facts below were checked against the linked official pages on **2026-11-06**. Recheck before provisioning or changing plans; neither a free runner nor a free VM makes storage, network, maintenance and other services universally free.

| Topic | Verified position and source (read 2026-11-06) |
| --- | --- |
| GitHub runner compute | Self-hosted usage is free and does not reduce included compute usage. Artifact/cache storage has separate allowances and possible charges. [GitHub billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) |
| Announced platform fee | The December 2025 announcement proposed a March 2026 self-hosted fee; its update postpones that change. Treat the current billing documentation as authoritative, not the superseded text below the update. [GitHub announcement](https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/) |
| Oracle A1 allowance | 1,500 OCPU-hours and 9,000 GB-hours monthly, described as a total of 2 OCPUs / 12 GB for Always Free tenancies, not per VM. Total block storage is 200 GB including boot volumes. Do not use old 4/24 instructions. [Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) |
| Oracle location | Always Free compute must be in the home region. [Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm). Home region is chosen at signup and cannot be changed after tenancy provisioning. [Managing regions](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingregions.htm) |
| Idle reclamation | Over seven days, CPU 95th percentile below 20%, network below 20%, and (A1 only) memory below 20% together qualify an idle instance for reclamation. [Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) |
| Pay As You Go | Always Free resources remain free within allowances after upgrading; usage beyond them becomes billable. The cited page does **not** establish a blanket PAYG exemption from idle reclamation. Do not rely on that claim without current Oracle confirmation. [Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) |
| Budget alerts | Budgets are soft limits, not spending caps, and alerts may lag. A budget amount of 1 in the account currency is supported. [Budgets](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm), [creating a budget](https://docs.oracle.com/en-us/iaas/Content/Billing/Tasks/create-budget.htm) |

Choose a small paid ARM VM when predictable paid provisioning is preferable to waiting for Oracle capacity; for example, review [Hetzner Cloud](https://www.hetzner.com/cloud/) for current plans/architecture and availability (read **2026-11-06**; no price is promised here). A home Linux machine trades rental cost for power, connectivity and recovery work. Container actions and GitHub `services:` require Linux with Docker; macOS/Windows hosts do not fit this example ([runner requirements](https://docs.github.com/en/actions/reference/runners/self-hosted-runners), read **2026-11-06**).

## Owner setup: Oracle example

These are manual owner actions, not permission for an agent to create resources or change billing. Replace angle-bracket placeholders locally. Keep registration credentials out of chat, commits, screenshots and CI logs.

### Adding another repository to an existing runner VM

Skip account/VM creation (steps 1–2). Use `sudo ls /home/runner` to inspect existing folders; a folder alone does not prove registration. Reuse the dedicated user and install only missing project dependencies from steps 3 and 5. As `runner`, create a **new** `/home/runner/<folder>`; do not reconfigure another repository's folder or service.

**Always repeat step 4 for the new repository:** open the **new repository's** Settings → Actions → Runners, register with **its URL/token**, and choose its own runner name and unique label. A repository-level runner registered to one repository never picks up another repository's jobs; a matching label does not register it. Organization runners with permitted repository access are a different setup ([runner scope](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners), read **2026-11-06**). Install its separate service, check the shared-VM checklist below, and set `CI_RUNNER` only after the new runner shows **Idle in the new repository**.

For either setup path, the adoption PR must put owner steps in an `> [!IMPORTANT]` block at the top and repeat them in chat, per the pack's PR rules. State whether to reuse a VM or create one, registration/dependency steps, the Idle-before-variable ordering, and a ready-run verification. Include who acts, where, timing and success checks; do not mark setup complete merely because the variable was saved.

### 1. Account, budget and access

Create an individual account if appropriate for the owner; use accurate identity/contact details and a real billing address matching the payment card. Enable MFA. Oracle permits one free account per person and excludes virtual/single-use/prepaid cards and PIN debit cards; some debit cards functioning as credit cards are accepted ([Free Tier FAQ](https://www.oracle.com/cloud/free/faq/), read **2026-11-06**).

Choose the home region carefully. Create a recurring monthly budget of **1 account-currency unit**, scoped to the runner compartment (or root compartment if tracking all resources), with an actual-spend alert at 100% and a monitored recipient. Confirm the alert rule was saved, not just the budget. This is a recommended notification threshold, not a guaranteed maximum bill. Review resource totals before accepting any PAYG upgrade.

Generate a dedicated SSH key on your own machine:

```sh
ssh-keygen -t ed25519 -f ~/.ssh/ci_runner -C ci-runner
```

Upload only `ci_runner.pub`. Optional local `~/.ssh/config` entry:

```sshconfig
Host ci-runner
  HostName <PUBLIC_IP>
  User ubuntu
  IdentityFile ~/.ssh/ci_runner
  IdentitiesOnly yes
```

Verify the server's host key through a trusted channel before accepting it. Restrict inbound SSH to your administration source; the runner needs outbound HTTPS, not a public CI/database/web-server listener. Keep the VM's cloud and host firewalls consistent.

### 2. Create the VM

Use these starting choices and review the Console's actual eligibility/cost summary:

- Home region, Ubuntu **24.04 non-minimal ARM64** image, `VM.Standard.A1.Flex`, **2 OCPU / 12 GB**, showing **Always Free-eligible**. Check aggregate tenancy use first; reduce allocation if other resources consume the allowance.
- A new VCN with an internet route and public subnet; assign an ephemeral public IPv4 for SSH. Keep CI service ports closed externally.
- A **100 GB boot volume**, leaving room within the aggregate 200 GB allowance, at **Balanced / 10 VPU per GB**. Balanced is documented at 10 VPU; confirm the selected combination's eligibility rather than assuming every storage/performance option is free ([Block Volume performance](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/blockvolumeperformance.htm), read **2026-11-06**).

Wait for Running, connect with `ssh ci-runner`, and maintain OS security updates. The UI selections are a starting configuration, not a guarantee of regional capacity or image availability.

### 3. Install packages and create the runner user

As the Ubuntu administration user:

```sh
sudo apt-get update
sudo apt-get install -y docker.io git curl jq unzip libatomic1
sudo systemctl enable --now docker
sudo adduser --disabled-password --gecos '' runner
sudo usermod -aG docker runner
sudo -iu runner
docker run --rm hello-world
mkdir -p ~/<folder>
cd ~/<folder>
```

The new login applies Docker group membership. Keep `runner` out of the sudo group. `libatomic1` supports newer Node Linux binaries; select Node with the project's `.nvmrc` and `setup-node`, not an unverified `apt nodejs/npm` version. This recipe's single-user Docker access is deliberately privileged; do not put unrelated workloads on the VM.

### 4. Register per repository and install the service

In the intended **private** repository, open **Settings → Actions → Runners → New self-hosted runner**, selecting **Linux / ARM64** for A1 (x64 for an x64 host). As `runner` in its dedicated folder, follow GitHub's current download/checksum/extraction instructions. Do not pin an old runner archive from a blog. Run `config.sh` with that repository's URL and its fresh registration token using the private terminal instructions. Choose Default at the runner-group prompt, then a distinct name and a unique custom label such as `<label>`.

Registration tokens expire after one hour ([adding runners](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners), read **2026-11-06**). If exposed, treat the token as compromised, review/remove unauthorized registrations and generate a fresh token; refreshing the page is not evidence that the old token was revoked. Never paste it into this recipe or chat.

Exit back to the sudo-capable administration user. Install, start and check the service:

```sh
sudo bash -c 'cd /home/runner/<folder> && ./svc.sh install runner && ./svc.sh start && ./svc.sh status'
```

This enters the private home directory as root and runs the service as `runner`; do not grant that user sudo just to run `svc.sh`. GitHub documents the optional service-user argument ([service setup](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/configure-the-application), read **2026-11-06**). Keep runner auto-updates enabled and schedule owner-managed OS/Docker updates in drained maintenance windows.

### 5. Prepare browser libraries once

The workflow downloads Chromium as the unprivileged runner using `pnpm exec playwright install chromium`; it never runs `--with-deps` or sudo. The owner installs the system dependencies separately for the project's **exact Playwright version**, and repeats this after upgrades as needed on **each** possible host.

After `setup-node` has populated its cache, read the example job's `tool_cache`/Node version output and verify the exact Node binary path. A typical ARM installation can be prepared as follows; replace both versions and adjust the cache path to the actual log:

```sh
sudo bash -c 'export PATH="/home/runner/<folder>/_work/_tool/node/<node-version>/arm64/bin:$PATH"; node --version; npx --yes playwright@<version> install-deps chromium'
ldconfig -p | grep libatk-1.0
```

Use a Node version supported by that Playwright release; do not choose the last cache directory by sorting or execute project scripts as root. If the first ready run exposes missing libraries, leave it failed, provision the verified dependencies and rerun that revision. A matching `ldconfig` entry is a diagnostic, not a substitute for a complete browser launch/test. With the variable unset, verify Ubuntu-hosted fallback has all required libraries/fonts too; this example does not reinstall apt dependencies on every fallback run ([Playwright CI](https://playwright.dev/docs/ci), read **2026-11-06**).

### 6. Set routing and housekeeping

**Only after the new runner shows Idle in this repository's Settings → Actions → Runners**, set its **Actions variable** `CI_RUNNER` to that runner's unique custom label, not its display name. An Idle runner listed only in a different repository is insufficient. The example uses:

```yaml
runs-on: ${{ vars.CI_RUNNER || 'ubuntu-24.04' }}
```

Only an **unset/empty variable** selects GitHub-hosted fallback. If no matching runner is online and idle, the job remains queued; it does not fall back automatically. After more than 24 hours queued, GitHub reports the job as **failed**, not a successful skip ([routing reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners), read **2026-11-06**). Register the missing runner or clear the variable and start a new current-revision run. Keep sensitive workflows explicitly GitHub-hosted.

Monitor disk (`df -h`, `docker system df`), workspace/browser caches and runner logs. An optional weekly root cron entry for a **drained maintenance window** is:

```cron
0 4 * * 0 /usr/bin/docker system prune --force --filter 'until=168h'
```

Add it with `sudo crontab -e` only after arranging that all runner services are stopped and all jobs completed during that window; resume afterward. Pruning across shared repositories can race container startup, so skip unattended scheduling if you cannot guarantee a quiet window. This command removes old unused Docker data and build cache, not volumes; it does not clean runner workspaces ([Docker prune](https://docs.docker.com/reference/cli/docker/system/prune/), read **2026-11-06**). Do not add `--volumes` or delete workspaces while jobs may use them.

## One VM, several repositories

Use one folder, registered runner name and custom label per repository, for example `/home/runner/project-a` with `project-a-ci` and `/home/runner/project-b` with `project-b-ci`. A runner process handles one job at a time; multiple registrations can run simultaneously. Start with one active workload on a 2-core VM. The supplied experience suggests roughly 2–3 concurrent jobs as a practical ceiling to investigate, not guaranteed capacity; Next builds and browsers may need serialization. Measure CPU, memory, disk and complete job time before increasing concurrency.

Fixed host ports (PostgreSQL, Playwright/Next web servers) permit only one conflicting job per machine at a time, even across repositories. The example assigns a random database port, but a web server on port 3000 still conflicts. Keep one registration for a repository's label, use distinct web ports across simultaneously running repositories, or serialize all conflicting jobs. Per-PR concurrency only replaces runs of the **same PR**; it does not serialize other PRs or repositories. Folder separation does not fix port conflicts or provide security isolation.

Before allowing overlap on a shared VM:

- List each repository's fixed host ports (database services and web/E2E servers), confirm no overlap, and record assignments/serialization in each project's development docs. Dynamic container ports do not eliminate fixed web-server conflicts.
- Watch memory and complete job time during the first overlapping runs; reduce concurrency if either workload becomes unstable or slower.
- Confirm that all repositories are the owner's own trusted private projects. They share a machine with root-equivalent Docker access and are not isolated from one another.

## Adapt the combined workflow

The [example](examples/ci.yml) is a **Budget-conscious combined-job alternative**, replacing the applicable existing CI/E2E jobs after review. Unlike the default separate-job recipe, it reuses one install, database service and production build for format → lint → typecheck → unit tests → integration tests → build → Playwright. It suits a small runner that executes jobs sequentially. Preserve every existing required suite; it is not permission to drop tests or browsers to fit ARM.

Adapt these contracts before installing it as `.github/workflows/ci.yml`:

- `.nvmrc`, an exact `packageManager` field, lockfile, and existing format/lint/typecheck/build scripts. `test:unit` and `test:integration` are example required script names; map them to real suites. The integration script must apply the test schema/migrations and test only the disposable database. Configure any additional app/E2E database variables in the same isolated environment; never point them at production.
- PostgreSQL 17 is an example image, not a project requirement. Match the application's version and verify ARM64 support for all native dependencies, actions and container images; a GitHub-hosted x64 pass does not prove ARM compatibility. Dummy `ci` database credentials apply only to the disposable service.
- Adapt the existing Playwright config to start the already-built app, such as `webServer.command: 'pnpm exec next start --hostname 127.0.0.1 --port 3000'`, with the matching URL and `reuseExistingServer: false` in CI. Do not rebuild in global setup or a `test:e2e` wrapper. Keep existing fixtures/migrations and important browser coverage; the Chromium-only install assumes the suite actually uses Chromium. Install every browser the suite requires.
- Use low worker counts on the small VM. The example uses one Playwright worker and a 40-minute job timeout; set a smaller test-level timeout so the suite can finish reporting first. Tune Vitest workers using the installed version's supported options.

For a project already using job-level draft skipping, keep that condition and its readiness triggers. Add runner routing, the identity step and a private-repository guard before checkout. In an existing private-project workflow that retains its hosted behavior, the guard can be scoped to `if: runner.environment == 'self-hosted' && !github.event.repository.private`; the supplied example remains private-only on either host. The pack's Budget-conscious default skips drafts. GitHub can count skipped required jobs as passing, so the current ready-state run must still actually validate the revision before merge.

Keep any existing sudo-based tool installation **only** on `if: runner.environment == 'github-hosted'`. On self-hosted, check tools and fail with an owner action instead of attempting sudo. For example, before tests using `pg_dump`/`psql`, adapt the expected major to the project's server and verified client requirement:

```yaml
- name: Check owner-provisioned PostgreSQL client
  if: runner.environment == 'self-hosted'
  env:
    PG_CLIENT_MAJOR: '17'
  run: |
    set -euo pipefail
    for tool in pg_dump psql; do
      if ! command -v "$tool" >/dev/null || ! "$tool" --version | grep -Eq " ${PG_CLIENT_MAJOR}([.]|$)"; then
        echo "::error::Owner: install PostgreSQL ${PG_CLIENT_MAJOR} client (pg_dump and psql) once on this runner, then retry."
        exit 1
      fi
    done
```

The hosted install must use the project's verified package/repository setup for that client version; do not assume the OS default matches the service. For existing caches of persistent local data such as `~/.cache/ms-playwright`, gate the cache action (or both separate restore/save steps) with `if: runner.environment == 'github-hosted'`. The VM keeps that data on disk; downloading missing browser binaries is still required. Preserve deliberate dependency-cache choices rather than disabling all caching. These are step-level conditions; `runner.environment` is unavailable in job-level `if` ([runner context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#runner-context), read **2026-11-06**).

Budget-conscious skips the entire job while the PR is a draft, so it allocates no runner or PostgreSQL service. Its conditional PostgreSQL image also stays empty for drafts. Returning to draft cancels an older run through per-PR concurrency; `ready_for_review` and every new ready commit run the full suite. A skipped draft status does not prove validation, even if GitHub accepts it for a required check: inspect the current revision's ready-state run before merge. No path filters or automatic merge/readiness changes are introduced.

For **Standard**, remove the job-level draft `if`, and change the service image to `${{ github.event.repository.private && 'postgres:17' || '' }}` so private draft PRs also receive the full suite. Keep the private-repository guard, permissions, mandatory commands and concurrency. Both variants can add `merge_group: { types: [checks_requested] }` alongside `pull_request` if all required workflows support the merge queue; the service/draft expressions allow that non-PR event.

The combined job retains `check`, but it replaces a separate `playwright` result. Coordinate branch protection/rulesets with the owner before retiring the old workflow: require the combined real-validation result and preserve other required checks. Do not leave `playwright` expected forever, add an empty success job to satisfy it, or remove a required suite. Keeping separate jobs is also valid; apply runner routing and draft/service guards to each and retain strict final results as described in the [CI strategy](../ci-strategy/README.md).

## Known problems

Console issues below came from the supplied working setup; UI behavior and fraud-check explanations were **not independently reproduced**. Use them as troubleshooting hints, not provider guarantees.

- **Generic signup error:** first try signing in at `cloud.oracle.com` with the cloud account name; signup may have succeeded. Avoid creating duplicate free accounts. VPN/privacy-email explanations are anecdotal, not verified fraud rules. Follow Oracle's documented card eligibility rather than assuming all debit cards fail.
- **A1 out of capacity:** try another available domain, then retry later or try 1 OCPU with suitable memory. Domain success varies; there is no universal working AD. Oracle documents the alternative-domain/retry approach in the Always Free page cited above.
- **Public IPv4 disabled while creating a subnet:** the supplied workaround is to create the VM, then open Networking → VNIC → IPv4 addresses → Edit and assign an ephemeral public IP. Confirm the subnet/route/security configuration; Console wording may differ. A VNIC-like hostname is cosmetic unless application configuration relies on it.
- **Runner-group prompt:** choose Default first; the runner name is a later prompt. Entering the name as a group can fail registration. Follow current repository instructions if prompts differ.
- **Permission denied for `svc.sh`:** use the administration-user `sudo bash -c` command above to enter the runner's private home. Do not install it from a shell that lacks sudo or weaken home permissions to fix this.
- **`libatk-1.0.so.0` or other Chromium library missing:** provision the exact Playwright version's dependencies with the owner-run cache-Node command, verify the binary path, and rerun. Do not assume the distribution's Node package meets current tooling requirements. Recheck library/font compatibility after Playwright upgrades.
- **Early database error in E2E:** a readiness probe before test database setup can emit an expected error in some projects. Confirm that the project's lifecycle explains it and all tests pass against the intended database. Do not dismiss unexplained errors merely because a later step is green.
- **Queued/offline runner or canceled leftovers:** an offline configured label does not trigger fallback. After cancellation, inspect lingering app processes/ports and disk state before rerunning; do not kill other repositories' work blindly.
- **Requested label but zero repository runners:** logs show `Requested labels: <label>` and `Waiting for a runner to pick up this job`, while this repository's runner list is empty. A variable alone does not register a runner, even if the VM serves another repository. Follow the existing-VM path and register for this repository, or clear `CI_RUNNER` and start a new run for hosted fallback. Do not wait for the 24-hour queue failure to fix registration.

## Acceptance checklist

- [ ] Owner reviewed billing dates/sources, VM eligibility, aggregate allowances, a saved budget alert, SSH access and host/network isolation.
- [ ] New runner shows **Idle in the target repository** before `CI_RUNNER` is set; its separate systemd service runs as `runner` and reconnects after a controlled reboot. Shared-VM ports and first-overlap memory/job time are checked.
- [ ] A ready PR executes every mandatory suite. Check `runner_name`, architecture and environment in the job logs (or the job API's `runner_name`), not just the green badge; confirm the intended VM actually ran it.
- [ ] Draft open/update/reopen skips the complete job in Budget-conscious mode, allocating no runner or PostgreSQL service; a skipped status is not validation evidence. Ready without a new commit starts full CI; the next commit requires its own successful result. Standard validates drafts fully.
- [ ] A deliberate test failure blocks the combined required result. Cancellation/retry and any merge queue are checked with current-revision runs; required names match the actual protection settings.
- [ ] Clearing `CI_RUNNER` and starting a new run lands on GitHub-hosted Ubuntu and passes the same tests, including browser libraries/fonts; restore the label only after checking the results. Document that this fallback can consume included compute or incur charges.
- [ ] Build runs once and Playwright serves that output; test databases and ports are isolated, no secret-bearing workflow moved, and concurrency fits measured machine resources.
- [ ] Maintenance/recovery and cleanup are documented; no live VM, billing setting or credential was provisioned by copying this recipe alone.
