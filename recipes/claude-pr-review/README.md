# Claude PR review recipe

An optional GitHub Actions workflow for requesting Claude feedback on a pull request by commenting `@claude review`. It responds to that phrase in a PR conversation, inline comment or review body. It does not run on every push or on issues. Claude responds in a comment; this is not a formal GitHub review or approval.

## Set up in a repository

1. Install the [Claude GitHub App](https://github.com/apps/claude) for the target repository. A repository administrator must approve the installation.
2. Generate a Claude Code OAuth token with `claude setup-token` on your own machine and save it as the repository Actions secret `CLAUDE_CODE_OAUTH_TOKEN`. Do not put the token in a file, commit, issue, PR or chat. The token uses the Claude account that generated it. If that account belongs to someone else, agree on ownership and usage before storing it in the repository.
3. Inspect any existing `.github/workflows/claude.yml`, then copy this recipe's workflow into the target repository without overwriting existing files:

   ```sh
   rsync -a --ignore-existing /absolute/path/to/ai-starter-pack/recipes/claude-pr-review/files/ /absolute/path/to/new-project/
   ```

   Adapt the workflow if the repository already has a Claude workflow or different review requirements.
4. Merge the workflow into the repository's default branch. Comment `@claude review` on a test PR and check the workflow run and Claude's response. GitHub requires the workflow to exist on the default branch for `issue_comment` to trigger it.

The workflow grants `actions: read` and requests the same additional permission from Claude so it can inspect CI results. Remove both if that is unnecessary. Only repository users with write access can trigger the action by default; do not enable `allowed_non_write_users` or broad bot access without reviewing the action's security guidance.

## Access and usage

The workflow's `permissions` limit the GitHub Actions `GITHUB_TOKEN`. The official Claude GitHub App uses its own installation token and has write access to repository contents, pull requests and issues. Asking for a review does not enforce read-only behavior. Review the App's permissions and protect branches according to the target repository's policy; if strict read-only operation is required, design and verify a separate authentication setup before enabling the workflow.

Private repositories consume the owner's included GitHub Actions minutes and may incur charges after that allowance. OAuth runs also count against the Claude account's plan limits; an Anthropic API key instead uses separate API billing. Check the current [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [Claude plan usage](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan) and [Claude Code Action setup and security guidance](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md) before enabling it.
