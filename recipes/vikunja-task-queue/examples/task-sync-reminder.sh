#!/bin/sh
# Claude Code PostToolUse hook: after `gh pr create` or `gh pr ready`, tell the agent when the PR is
# linked to a Vikunja task (a `Task: ` line in its body), so it runs the task-sync `pr` or `review`
# step. It makes no Vikunja call and never blocks: any failure prints nothing and exits 0.
# Install: copy to ~/.claude/hooks/task-sync-reminder.sh (chmod 755) and add the hook from the
# recipe README to ~/.claude/settings.json.
input=$(cat)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)
[ -n "$cwd" ] && cd "$cwd" 2>/dev/null || exit 0

case "$cmd" in
  *"gh pr ready"*) step="review" ;;
  *) step="pr" ;;
esac

# The PR of the current branch; a short timeout keeps the hook cheap.
body=$(timeout 8 gh pr view --json body,number -q '"#\(.number)\n\(.body)"' 2>/dev/null) || exit 0
task=$(printf '%s\n' "$body" | sed -n 's/^Task: *\([A-Z][A-Z0-9]*-[0-9][0-9]*\).*/\1/p' | head -n 1)
[ -n "$task" ] || exit 0
pr=$(printf '%s\n' "$body" | head -n 1)

jq -n --arg t "$task" --arg p "$pr" --arg s "$step" '{
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    additionalContext: "PR \($p) is linked to Vikunja task \($t). The task-sync \($s) step for it has not run in this command."
  }
}'
