# Manual Setup Steps - Complete Within 24 Hours

## ✅ Completed (Automated)

- Guardrails tightened (max_loc=250, forbidden: auth/**, billing/**, etc.)
- Cost caps added (MAX_LOOPS=6, token budget=120,000)
- Token usage tracking with budget enforcement
- Auto-label PRs with 'bot' tag
- Auto-assign owner as reviewer
- Slack/Teams webhook support ready
- CODEOWNERS template created

## 🔧 TODO: Manual Steps Required

### 1. GitHub Labels (persx/persx) - 5 minutes

Add these labels at: https://github.com/persx/persx/labels/new

| Name | Color | Description |
|------|-------|-------------|
| `bot` | `#0e8a16` (green) | Automated changes from Claude bot |
| `safe-change` | `#bfdadc` (light blue) | Low-risk change verified by guardrails |
| `needs-human` | `#fbca04` (yellow) | Requires human review and decision |
| `blocked` | `#d93f0b` (red) | Bot cannot proceed - manual intervention needed |

### 2. CODEOWNERS File (persx/persx) - 2 minutes

Copy `.github/CODEOWNERS.template` from this repo to `persx/persx/.github/CODEOWNERS`

Or create manually at: https://github.com/persx/persx/new/main?filename=.github/CODEOWNERS

```
# Core application code requires review
/app/**           @persx
/components/**    @persx
/lib/**           @persx

# Auth and billing are critical
/auth/**          @persx
/billing/**       @persx

# Database and migrations
/supabase/**      @persx
```

### 3. Branch Protection (persx/persx) - 3 minutes

Configure at: https://github.com/persx/persx/settings/branches

**Branch name pattern:** `main`

**Required settings:**
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging
  - Add required checks after first workflow run: `lint`, `build`
- ✅ Do not allow bypassing the above settings
- ✅ Require approval from code owners

### 4. Slack/Teams Webhook (Optional) - 2 minutes

For PR notifications, add this secret to the **bot repo**:

**Repository:** https://github.com/persx/coder/settings/secrets/actions/new

**Secret name:** `SLACK_WEBHOOK_URL` (or `TEAMS_WEBHOOK_URL`)

**Value:** Your webhook URL

**Get Slack webhook:**
1. Go to https://api.slack.com/messaging/webhooks
2. Create incoming webhook
3. Select channel for bot notifications
4. Copy webhook URL

### 5. First Bot Run - 1 minute

Trigger the workflow manually:
https://github.com/persx/coder/actions/workflows/runner.yml

Click "Run workflow" → Select "main" → Click "Run workflow"

---

## Safety Features Now Active

✅ **Max LOC:** 250 lines per PR (reduced from 400 for first week)
✅ **Forbidden paths:** auth/**, billing/**, supabase/seed.sql, configs
✅ **Max loops:** 6 (reduced from 10)
✅ **Token budget:** 120,000 tokens per run
✅ **Auto-labeling:** All PRs tagged with `bot`
✅ **Auto-reviewer:** Owner assigned to all PRs
✅ **Draft PRs:** All PRs created as drafts until checks pass

## Testing Checklist

After manual setup:
- [ ] Labels created in persx/persx
- [ ] CODEOWNERS file added to persx/persx
- [ ] Branch protection enabled on main
- [ ] Slack webhook configured (optional)
- [ ] First workflow run triggered
- [ ] First PR created successfully
- [ ] PR has `bot` label
- [ ] You are assigned as reviewer
- [ ] Checks run (lint & build)
