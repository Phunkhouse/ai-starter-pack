#!/usr/bin/env bash
# Separate Codex bot/service credentials; exported only to this process tree.
set -euo pipefail
set +x
account=$(id -un)
VIKUNJA_MCP_TOKEN=$(security find-generic-password -a "$account" -s '<PREFIX>.codex.vikunja-token' -w)
CF_ACCESS_CLIENT_ID=$(security find-generic-password -a "$account" -s '<PREFIX>.codex.cf-client-id' -w)
CF_ACCESS_CLIENT_SECRET=$(security find-generic-password -a "$account" -s '<PREFIX>.codex.cf-client-secret' -w)
export VIKUNJA_MCP_TOKEN CF_ACCESS_CLIENT_ID CF_ACCESS_CLIENT_SECRET
exec codex "$@"
