#!/usr/bin/env bash
# macOS Claude Code helper. stdout contains credentials: never run it for display.
set -euo pipefail
set +x
account=$(id -un)
VIKUNJA_MCP_TOKEN=$(security find-generic-password -a "$account" -s '<PREFIX>.claude.vikunja-token' -w)
CF_ACCESS_CLIENT_ID=$(security find-generic-password -a "$account" -s '<PREFIX>.claude.cf-client-id' -w)
CF_ACCESS_CLIENT_SECRET=$(security find-generic-password -a "$account" -s '<PREFIX>.claude.cf-client-secret' -w)
export VIKUNJA_MCP_TOKEN CF_ACCESS_CLIENT_ID CF_ACCESS_CLIENT_SECRET
python3 - <<'PY'
import json, os
print(json.dumps({
    'Authorization': 'Bearer ' + os.environ['VIKUNJA_MCP_TOKEN'],
    'CF-Access-Client-Id': os.environ['CF_ACCESS_CLIENT_ID'],
    'CF-Access-Client-Secret': os.environ['CF_ACCESS_CLIENT_SECRET'],
}))
PY
