# Manual Setup Steps

## GitHub Labels (persx/persx)

Add these labels at: https://github.com/persx/persx/labels/new

| Name | Color | Description |
|------|-------|-------------|
| `bot` | `#0e8a16` (green) | Automated changes from Claude bot |
| `safe-change` | `#bfdadc` (light blue) | Low-risk change verified by guardrails |
| `needs-human` | `#fbca04` (yellow) | Requires human review and decision |
| `blocked` | `#d93f0b` (red) | Bot cannot proceed - manual intervention needed |

## Branch Protection (persx/persx)

Configure at: https://github.com/persx/persx/settings/branches

**Branch name pattern:** `main`

**Settings:**
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging
  - Add required checks: `lint`, `build`
- ✅ Do not allow bypassing the above settings

## Slack/Teams Webhook (Optional)

For PR notifications, add this secret to the bot repo:

**Repository:** https://github.com/persx/coder/settings/secrets/actions

**Secret name:** `SLACK_WEBHOOK_URL`

**Value:** Your Slack incoming webhook URL (https://hooks.slack.com/services/...)

Or for Teams: Your Teams webhook URL
