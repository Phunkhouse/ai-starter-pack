#!/usr/bin/env bash
# Root-owned deployment and environment, invoked by the example systemd unit.
set -Eeuo pipefail
umask 077

: "${COMPOSE_DIR:?Set COMPOSE_DIR}"
: "${RESTIC_REPOSITORY:?Set RESTIC_REPOSITORY}"
: "${RESTIC_PASSWORD_FILE:?Set RESTIC_PASSWORD_FILE}"

exec 9>/run/lock/vikunja-backup.lock
flock -n 9 || exit 1
cd -- "$COMPOSE_DIR"
compose=(docker compose --project-directory "$COMPOSE_DIR" -f "$COMPOSE_DIR/compose.yaml")
stage=''
needs_start=0

ping_check() {
  [[ -n "${HEALTHCHECKS_URL:-}" ]] || return 0
  # Do not put the secret ping URL in argv, output or uploaded diagnostic bodies.
  printf 'url = "%s"\n' "${HEALTHCHECKS_URL%/}$1" |
    curl --config - --silent --fail --max-time 10 --output /dev/null 2>/dev/null
}

cleanup() {
  result=$?
  trap - EXIT
  if (( needs_start )); then
    "${compose[@]}" start vikunja || result=1
  fi
  if [[ -n "$stage" ]]; then
    rm -rf -- "$stage"
  fi
  if (( result == 0 )); then
    ping_check '' || result=1
  else
    ping_check /fail || true
  fi
  exit "$result"
}
trap cleanup EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
# An unreachable monitor must not prevent the backup itself.
ping_check /start || true

# Never start an intentionally stopped deployment as a side effect of a backup.
"${compose[@]}" ps --status running --services | grep -Fxq vikunja
[[ -f compose.yaml && -f .env && -d data/db && -d data/files ]]
install -d -m 700 /var/lib/vikunja-backup
stage=$(mktemp -d /var/lib/vikunja-backup/snapshot.XXXXXXXX)
needs_start=1
"${compose[@]}" stop vikunja
# Copy the WHOLE database directory, including any WAL/SHM files, plus uploads.
cp -a -- data "$stage/data"
cp -a -- compose.yaml .env "$stage/"
"${compose[@]}" start vikunja
needs_start=0

# Upload the frozen copy after resuming the app. pipefail rejects partial archives.
tar -C "$stage" -cf - . |
  restic backup --stdin --stdin-filename vikunja.tar --tag vikunja
