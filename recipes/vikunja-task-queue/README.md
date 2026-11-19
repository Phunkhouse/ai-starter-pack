# Vikunja task queue

Optional self-hosted work queue when ideas and findings arrive faster than the owner and coding agents can implement them. GitHub remains authoritative for code, CI and PRs; SPEC/milestones remain the product plan. Queue entries do not dispatch agents, authorize implementation or merge PRs. No default changes to `template/core/AGENTS.md` are needed: paste and adapt the separate [project snippet](AGENTS-section.md) only when opting in.

## Reference and architecture

Checked **2026-11-18** against official Vikunja **v2.8.0**, commit `6e788bf87cebe50e2b8d034b213fcf94ae5449ee`. The official changelog lists it as the latest stable release on that date. Recheck releases and security advisories before deployment; no image digest or production installation is certified by this recipe.

```text
Owner browser -- Access email PIN --+
                                   +-- Cloudflare Tunnel -- Vikunja -- SQLite + uploads
Agent -- Access service headers ---+                         |
         + Vikunja bot API token                       restic -> private S3 bucket
```

Vikunja's native MCP is available since 2.7.0, at **POST `https://tasks.example.com/api/v2/mcp`**, using stateless Streamable HTTP. It accepts scoped API bearer tokens (`tk_…`), not login JWTs. Each needs `mcp:access`, action permissions and project access; expiry/revocation still applies. Native MCP is not license-gated as a Pro feature in the inspected source. Cloudflare service credentials pass the outer gate; they do not replace Vikunja authentication. [Official MCP help](https://vikunja.io/help/mcp/), [release notes](https://vikunja.io/changelog/), [MCP source](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/modules/mcp/mcp.go) (read 2026-11-18).

This is a single-instance, small-queue deployment: SQLite, no Redis/Postgres, one tunnel ingress and no published host port. A 384 MB container limit is a starting constraint, not measured capacity; inspect OOMs, DB contention, uploads and backup duration before relying on it. Keep it off a machine where untrusted CI has root-equivalent access.

## Owner deployment checklist

1. Prepare a dedicated Linux deployment directory such as `/opt/vikunja`, Docker Compose, private backups, an owner-approved hostname and recovery access. Copy [compose.yaml](examples/compose.yaml) as `compose.yaml`. Provision `data/db` and `data/files` with the dedicated host UID/GID; set both in a root-owned, mode-600 `.env`. Override the image's default UID 1000 deliberately rather than granting root inside it.
2. In `.env`, set `VIKUNJA_IMAGE=vikunja/vikunja:2.8.0@sha256:<DIGEST>` and `CLOUDFLARED_IMAGE=cloudflare/cloudflared:<VERSION>@sha256:<DIGEST>` to owner-verified registry digests for the deployment architecture. Also set `VIKUNJA_UID`, `VIKUNJA_GID`, a non-overlapping private `APP_SUBNET=<STACK_SUBNET_CIDR>`, a strong stable `VIKUNJA_SERVICE_SECRET` and the connector `TUNNEL_TOKEN`. Generate secrets locally without logging them; never commit `.env` or copy real values into this public repository. Add deployment secrets/data to the target project's ignore rules.
3. Adapt `tasks.example.com` in the compose environment and clients. Leave `read_only`, `cap_drop: ALL`, `no-new-privileges` and no host port. Only DB/uploads and `/tmp` are writable; healthcheck invokes `/app/vikunja/vikunja healthcheck`, not a shell/curl in the scratch image. The app network is internal; the tunnel also has an egress network. Trust only that stack's proxy subnet with `service.ipextractionmethod=xff`; do not trust arbitrary networks or expose the origin elsewhere.
4. Configure Access **before** publishing the tunnel hostname: an explicit email allowlist using one-time PIN for humans, and a **Service Auth** policy restricted to one Access service token per agent. Do not use a Bypass policy. Set the tunnel's published application route to `http://vikunja:3456` and reject unmatched hosts; never expose a second unauthenticated origin. Verify the forwarded client IP at the app and the trusted-proxy boundary instead of assuming correct rate limiting from a successful login. [Cloudflare tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/local-management/configuration-file/), [service tokens](https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/) (read 2026-11-18).
5. Run `docker compose up -d` only after owner approval. `docker compose config --quiet` checks interpolation without printing expanded secrets. Verify health, external Access protection and resource use. Create the owner through the binary CLI; registration is disabled. Use the same procedure for separate `claude-agent` and `codex-agent` identities (or the release's owner-managed bot UI), never one shared owner token.

The image is `FROM scratch`: the entrypoint **is** the Vikunja binary. For example, `docker compose exec vikunja /app/vikunja/vikunja user create --username '<BOT_NAME>' --email '<BOT_EMAIL>'` prompts for the password without placing it in argv. `user reset-password --direct <USER_ID>` resets locally when no mailer is configured. Check `user change-status --help` for an account still locked after reset; v2.8.0 locks accounts after ten failed logins. Access email PIN is not the Vikunja password. The stable service secret matters: omitting it generates a new secret on startup and invalidates sessions. [Dockerfile](https://github.com/go-vikunja/vikunja/blob/v2.8.0/Dockerfile), [config](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/config/config.go), [CLI](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/cmd/user.go), [lockout](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/user/lockout.go) (read 2026-11-18).

## Projects, bots and narrow tokens

Owner creates each project and its Kanban view, then shares read/write access with each agent identity, **not** project/instance admin. Record `<PROJECT_ID>`, project identifier `<PROJECT_IDENTIFIER>`, `<VIEW_ID>` and each `<BUCKET_ID>` in the opt-in project snippet. Create Inbox → Backlog → Ready → In Progress → Review → Done, with bucket limits Ready **10**, In Progress **2**, Review **1**; configure Done as the view's done bucket. Moving into it marks a task done (and out of it unmarks it); repeating tasks have additional behavior. Limits reject moves with 412. The owner sets up buckets; the bot does not need bucket-management permissions. [Bucket move contract](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/routes/api/v2/task_bucket.go) (read 2026-11-18).

For each bot, create an expiring API token starting with **Typed tools read + write**, then narrow it:

| Permission group | Allowed capability |
| --- | --- |
| MCP | Access (required) |
| Projects | Read All/One, Tasks By Index, Views Buckets, Views Buckets Tasks, Views Buckets Tasks Update |
| Projects Views | Read All/One |
| Projects Views Tasks | Read All |
| Tasks | Read All/One, Create, Update |
| Task comments | Read All/One, Create, Update (the agent edits its own status comment in place); no Delete |
| Task assignees | Read All, Create for claims |
| Labels | Read All/One only; no definition Create/Update/Delete |
| Tasks Labels | Read All, Create/Delete **associations**, not label definitions |
| Tasks Relations | Create |
| Users | Search |

Remove preset permissions not needed by this table, especially task/project/comment deletes, project create/update and label definition changes. UI titles are derived from route permissions; compare the installed release's MCP settings and live `tools/list`/`find_action` result. The deliberate Tasks Labels Delete exception removes an association only. Token scope does not restrict writes to assigned tasks or prevent moving to Done; those are policy boundaries, not server-enforced isolation.

Owner creates the existing type/provenance labels listed in [AGENTS-section.md](AGENTS-section.md). Labels are creator-owned; bots may only see another user's label once attached to a task they can access. Keep a completed **Label reference (keep)** task per project carrying every approved label. A 403 while attaching can mean label visibility, not missing write access. Do not solve it by granting label administration. [Label permissions](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/models/label_permissions.go) (read 2026-11-18).

## MCP tools and conflict handling

First-class tools include `projects_*`, `tasks_*`, `task_comments_*`, `labels_*`, `task_assignees_*`, `users_search` and `filter_syntax`, filtered by token permissions. Request `fields` and `format: "markdown"` where the advertised schema accepts them. Other operations use `find_action` then `do_action`, for example `task_bucket_update`, `tasks_read_by_index`, `task_labels_create/delete`, `tasks_relations_create`, `buckets_list` and `project_views_list`. Discover the schema rather than inventing argument names; by-index lookup accepts a project identifier string such as `<PROJECT_IDENTIFIER>`, not just a numeric ID. Catalog reads still go through `do_action`, which can also write: do not blanket-auto-approve that tool.

The allowlist excludes account settings, token administration, webhooks, link shares and file uploads. `tasks_update` dispatches PATCH of changed fields; the inspected task write path has no `If-Match` concurrency guard. Re-read task/comments before a write, send only changed fields and read back claims/updates. Assignment + bucket + comment are separate operations, not an atomic lock; serialize work through owner assignment when contention matters. Do not overwrite another agent's assignment. [Exposure map](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/modules/mcp/exposure.go), [dispatch](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/modules/mcp/tools.go), [catalog](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/modules/mcp/catalog.go) (read 2026-11-18).

## Agent clients: local secrets, explicit writes

Create six separate macOS Keychain generic-password items using Keychain Access, with account equal to the local login name. Use service names `<PREFIX>.claude.vikunja-token`, `.claude.cf-client-id`, `.claude.cf-client-secret`, and corresponding `.codex.*` items. Store each bot's Vikunja token and its own Cloudflare service credentials. Replace prefixes in the examples, install reviewed scripts outside project repos with owner-only permissions, and allow intentional Keychain access. The Claude helper also requires Python 3. Do not run helpers in a terminal to inspect their output, turn on shell tracing or export credentials globally. A client and its subprocesses can access inherited credentials: use only trusted workspaces.

**Claude Code:** install [headers.sh](examples/headers.sh) at a private absolute path, then register without literal secrets:

```sh
claude mcp add-json --scope user vikunja '{"type":"http","url":"https://tasks.example.com/api/v2/mcp","headersHelper":"/ABS/PATH/headers.sh"}'
```

The helper prints JSON string headers to stdout for the client only. Check `/mcp` privately. Review each write and especially catalog dispatch under the client's permissions; task content never supplies authorization. Absolute paths avoid helper working-directory differences. [Official Claude MCP guide](https://code.claude.com/docs/en/mcp) (read 2026-11-18).

**Codex:** merge [codex-config.toml](examples/codex-config.toml) into the owner's `~/.codex/config.toml`. Use [codex-with-vikunja.sh](examples/codex-with-vikunja.sh) as a separately named launcher, not a globally exported shell environment. It reads the Codex-specific Keychain items and supplies the three environment variables only to that invocation. A desktop launch does not inherit this wrapper automatically. The example restricts tools, defaults to `prompt`, and uses per-tool `approval_mode = "approve"` for inspected reads. `do_action` stays prompted, including catalog reads. The v2.8.0 server does not attach read-only annotations to these tools, so do not rely on `writes` mode to classify them; verify actual prompts in the installed client. Policy cannot override enterprise controls or a task's need for owner authorization. [Official Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) (read 2026-11-18).

## Lifecycle skill and reminder hook (optional)

[skills/task-sync/SKILL.md](skills/task-sync/SKILL.md) keeps a task in step with the work: **start** (one read with comments and column, then claim at the first real change), **checkpoint**, **pr**, **review**, **ci**, **close** (Done per the project's Done policy), **capture** (propose, create on the owner's yes) and **reconcile** (one `tasks_list` per project filtered on the In Progress and Review buckets, then `gh pr view` per linked PR). Each agent keeps one `**Agent status**` comment per task and edits it in place. Project values come from the project's AGENTS.md section, so the skill holds none. It uses about a dozen Vikunja calls per task.

Install it like other shared Skills, as links from a local clone of this repository: `ln -s <CLONE>/recipes/vikunja-task-queue/skills/task-sync ~/.claude/skills/task-sync` (Claude Code) and the same into `~/.agents/skills/` (Codex). Start a new session to load it.

Nothing runs while no agent is running. Merges are noticed by the next **reconcile** ("sync the board"); a GitHub Action posting merge comments would need a comment-only bot, its tokens as Actions secrets and hosted-runner minutes, and it should never move tasks.

When Vikunja is unreachable, the skill appends intended updates to a per-bot `~/.local/state/task-sync/outbox-<bot user>.md` (no secrets) and that bot's next reconcile applies them. Column state can always be derived again from GitHub.

**Claude Code reminder hook:** [task-sync-reminder.sh](examples/task-sync-reminder.sh) runs after `gh pr create` and `gh pr ready`. When the branch's PR body has a `Task:` line, it tells the agent that the task-sync `pr` or `review` step has not run. It makes no Vikunja call and exits silently on any failure. It needs `jq`, `gh` and `timeout`. Copy it to `~/.claude/hooks/` with mode 755 and add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "if": "Bash(gh pr create *)", "command": "~/.claude/hooks/task-sync-reminder.sh" },
          { "type": "command", "if": "Bash(gh pr ready *)", "command": "~/.claude/hooks/task-sync-reminder.sh" }
        ]
      }
    ]
  }
}
```

The `if` filter is best-effort per the [hooks reference](https://code.claude.com/docs/en/hooks) (read 2026-11-18). That's fine for a reminder, but not for enforcement.

**Prompts:** keeping the board current without the owner approving each write means allowing the Vikunja tools in the client (`"allow": ["mcp__vikunja__*"]` in Claude Code), `do_action` included. Do this only when the bot's token is narrow (no deletes, no project or label administration), because the token is then the real limit. Otherwise keep `do_action` prompted, as above.

## Backups and restore drill

SQLite uses WAL. Never copy just `vikunja.db` from a running app: freeze the writer and copy the whole DB directory, WAL/SHM if present, and uploads as one consistent set. [Database source](https://github.com/go-vikunja/vikunja/blob/v2.8.0/pkg/db/db.go) (read 2026-11-18). Outage is copy duration, not a promised one second.

Install Bash, `flock`, curl, tar and restic on the Linux host. Install [backup.sh](examples/backup.sh) root-owned as `/usr/local/sbin/vikunja-backup`, mode 750; copy the [service](examples/vikunja-backup.service) and [timer](examples/vikunja-backup.timer) into `/etc/systemd/system/`. Keep the deployment directory, compose file and `.env` root-owned and not writable by a CI user. The script expects regular local `data/db`, `data/files`, `compose.yaml` and `.env`. It serializes backups with `flock`, requires the app already running, stops it, copies the data and configuration, restarts it even after a copy failure, then uploads an encrypted tar of that frozen copy. It does not prune retention automatically. A host crash, SIGKILL or systemd's final forced kill cannot be repaired by an EXIT trap; alert and check app state after interruption.

Create `/etc/vikunja-backup.env` mode 600 with `COMPOSE_DIR=/opt/vikunja`, `RESTIC_REPOSITORY=s3:https://<S3_ENDPOINT>/<BUCKET_ID>/<PREFIX>`, `RESTIC_PASSWORD_FILE=<PRIVATE_PASSWORD_FILE>`, the backend's scoped `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` and optional `HEALTHCHECKS_URL=<PRIVATE_PING_URL>`. Use a separate S3-compatible bucket/key limited to that bucket/prefix and restic's required list/read/write permissions. Keep encryption-password recovery and S3 credentials outside the deployment backup. Do not commit that environment file. Initialize the restic repository once in a protected owner shell, validate a backup manually, then `systemctl daemon-reload` and `systemctl enable --now vikunja-backup.timer`.

The snapshot contains **secrets** from `.env`, including the service secret and connector token: restrict local staging and remote access and rely on restic encryption, not bucket privacy alone. The script sends Healthchecks start/success/failure without uploading logs; configure a missing-ping alert. An unreachable Healthchecks endpoint does not stop the backup, but a failed success ping still marks the run failed. Check `systemctl status`, `journalctl` privately, snapshots and periodic `restic check`; set retention and restore frequency as owner policy. [Restic backend/password documentation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html), [Healthchecks signals](https://healthchecks.io/docs/http_api/) (read 2026-11-18).

Test recovery **before relying on backups**:

1. In a private disposable directory, restore an explicit known snapshot with `restic restore <SNAPSHOT_ID> --target <RESTORE_DIR>`. Inspect and extract its `vikunja.tar` into a separate empty directory. Never overwrite the running deployment and never use restored tunnel credentials to start a second public ingress.
2. Start **only** the restored app image at the original tag/digest with `docker run --detach --name vikunja-restore-check --network none --read-only --cap-drop ALL --security-opt no-new-privileges:true --user '<UID>:<GID>' --tmpfs /tmp:rw,nosuid,nodev,noexec,size=64m --env-file '<RESTORE_TEST_ENV>' --mount 'type=bind,src=<RESTORED_DB_DIR>,dst=/db' --mount 'type=bind,src=<RESTORED_FILES_DIR>,dst=/app/vikunja/files' '<ORIGINAL_PINNED_IMAGE>'`. Use a private test env with the original stable service secret, `VIKUNJA_SERVICE_PUBLICURL=https://tasks.example.com/` (required by the default CORS configuration), and SQLite/files paths from compose, registration/mailer/Redis off. No tunnel, published ports or external network.
3. Run `docker exec vikunja-restore-check /app/vikunja/vikunja healthcheck` and inspect expected users with the CLI; check task/project counts using read-only SQLite inspection of the disposable restored database. A healthcheck verifies dependencies, not the full UI or Access path. Record snapshot/image/date and actual results. Remove this specifically named test container and private restored data after verification, preserving the remote snapshot.

The binary's `dump` and `restore` commands are another backup format: consult their `--help`. **Do not pass this script's tar to Vikunja `restore`**; it is a filesystem snapshot, not a Vikunja dump. The network-none drill above is a required owner acceptance step, not a claim that this recipe has exercised a live S3/Cloudflare deployment.

## Verification and operations

- Before enabling agents, check unauthenticated browser access redirects to Access login (normally 302). With a wrong service secret and no browser session, access must be denied (often 401; exact edge policy may return another denial). An unexpected 2xx is a failure. Then check valid service headers **without** a Vikunja token are still denied by the app; the outer gate must not bypass the inner one.
- As each bot, initialize MCP and inspect `tools/list` plus catalog discovery privately. Verify only shared projects are visible, allowed reads and a deliberately authorized Inbox create/comment/move succeed, forbidden task/project/label-definition deletes are absent/refused, and expired/revoked tokens fail. A JSON-RPC HTTP 200 can contain `isError`; inspect the tool result. Use disposable tasks for all write tests, never a real task for a refused-delete probe.
- Verify label discovery/attachment, full-column 412 handling, done-bucket side effects and a simulated competing claim. Test neither agent can infer permission to execute just from a Ready task. Paste the opt-in snippet with real project/view/bucket mappings only in the private target project; leave the core template unchanged.
- Upgrades: back up and complete a restore drill, review migrations/advisories, then update tag **and** digest and verify app, MCP schemas/permissions and client prompts. Rollback restores pre-upgrade data **and** the old image; do not run an old binary against a newly migrated production DB.
- Rotate one agent at a time: create scoped replacement API/Access tokens, update that agent's Keychain entries, verify reads and approved writes, then revoke old tokens at both layers. Removing a client entry does not revoke server tokens. Preserve service-secret recovery separately; do not rotate it incidentally at every restart.
- Check RAM/disk, backup delivery, alerts, token expiry and recovery access. None of the example files provisions accounts, starts agents or schedules implementation. Record any unperformed verification in the adoption PR; put actual owner setup/backup/client steps in the pack's top IMPORTANT handoff block.
