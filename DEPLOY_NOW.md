# 🚀 Deploy Claude Bot - Final Steps

The bot code is ready and pushed to GitHub! Complete these final steps to launch.

---

## ✅ Prerequisites Complete

- ✅ Bot code pushed to: https://github.com/persx/coder
- ✅ Bug fixes applied (glob parameter, message format)
- ✅ Debug logging added
- ✅ Setup documentation created
- ✅ Model configured for Sonnet (claude-3-5-sonnet-20241022)

---

## 🔐 Step 1: Add GitHub Secrets (5 min)

Visit: https://github.com/persx/coder/settings/secrets/actions/new

### Secret 1: ANTHROPIC_API_KEY
- **Name:** `ANTHROPIC_API_KEY`
- **Value:** Your Anthropic API key **with Sonnet access**
- **Where to get it:** https://console.anthropic.com/settings/keys
- **Must start with:** `sk-ant-`
- **Important:** Key must have access to `claude-3-5-sonnet-20241022`

### Secret 2: GH_TOKEN
- **Name:** `GH_TOKEN`
- **Value:** GitHub fine-grained PAT
- **How to create:** See `setup/CREATE_GITHUB_PAT.md`
- **Quick link:** https://github.com/settings/tokens?type=beta
- **Permissions needed:**
  - Repository: `persx/persx`
  - Contents: Read and write
  - Pull requests: Read and write

### Secret 3: SLACK_WEBHOOK_URL (Optional)
- **Name:** `SLACK_WEBHOOK_URL`
- **Value:** Your Slack webhook URL (if you want notifications)
- **Skip if:** You don't want Slack notifications

**Verify secrets added:**
https://github.com/persx/coder/settings/secrets/actions

---

## 🏷️ Step 2: Create Labels in persx/persx (5 min)

### Option A: Quick Web UI Creation

Visit these URLs and create each label:

1. **Label: bot**
   - URL: https://github.com/persx/persx/labels/new
   - Name: `bot`
   - Description: `Automated changes from Claude bot`
   - Color: `#0e8a16` (green)

2. **Label: safe-change**
   - URL: https://github.com/persx/persx/labels/new
   - Name: `safe-change`
   - Description: `Low-risk change verified by guardrails`
   - Color: `#bfdadc` (light blue)

3. **Label: needs-human**
   - URL: https://github.com/persx/persx/labels/new
   - Name: `needs-human`
   - Description: `Requires human review and decision`
   - Color: `#fbca04` (yellow)

4. **Label: blocked**
   - URL: https://github.com/persx/persx/labels/new
   - Name: `blocked`
   - Description: `Bot cannot proceed - manual intervention needed`
   - Color: `#d93f0b` (red)

### Option B: Detailed Instructions
See: `setup/create-labels-manual.md`

---

## 📄 Step 3: Add CODEOWNERS to persx/persx (2 min)

Visit: https://github.com/persx/persx/new/main?filename=.github/CODEOWNERS

Copy/paste this content:

```
# CODEOWNERS for persx/persx

# Core application code requires review
/app/**           @persx
/components/**    @persx
/lib/**           @persx

# Auth and billing are critical
/auth/**          @persx
/billing/**       @persx

# Database and migrations
/supabase/**      @persx

# Configuration files
/next.config.*    @persx
/tsconfig.json    @persx
/package.json     @persx

# CI/CD and scripts
/.github/**       @persx
/scripts/**       @persx
```

Click **"Commit new file"**

---

## ⚙️ Step 4: Add PR Size Gate to persx/persx (2 min)

Visit: https://github.com/persx/persx/new/main?filename=.github/workflows/pr-size.yml

Copy/paste this content:

```yaml
name: PR size gate
on: [pull_request]

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR size
        uses: actions/github-script@v7
        with:
          script: |
            const pr = context.payload.pull_request;
            const added = pr.additions || 0;
            const removed = pr.deletions || 0;
            const total = added + removed;

            console.log(`PR size: +${added} -${removed} = ${total} LOC`);

            if (total > 250) {
              core.setFailed(`❌ PR too large (${total} LOC). Keep changes under 250 LOC for easy review.`);
            } else {
              console.log(`✅ PR size OK (${total}/250 LOC)`);
            }
```

Click **"Commit new file"**

---

## 🛡️ Step 5: Enable Branch Protection (3 min)

Visit: https://github.com/persx/persx/settings/branches

Click **"Add branch protection rule"**

**Branch name pattern:** `main`

**Enable these settings:**

- ✅ **Require a pull request before merging**
  - ✅ Require approvals: `1`

- ✅ **Require status checks to pass before merging**
  - Search and add: `PR size gate` (after step 4 creates it)
  - Note: Add `lint`, `build`, `test` after first workflow run

- ✅ **Require approval from Code Owners**

- ✅ **Do not allow bypassing the above settings**

Click **"Create"** or **"Save changes"**

---

## 🚀 Step 6: Trigger First Bot Run (1 min)

Visit: https://github.com/persx/coder/actions/workflows/runner.yml

1. Click **"Run workflow"** button
2. Select branch: **main**
3. Click green **"Run workflow"** button

**Watch it run:**
https://github.com/persx/coder/actions

**Expected duration:** 2-5 minutes

---

## 🔍 Step 7: Monitor First PR (10 min)

### Watch for bot PR

The bot will create a draft PR in persx/persx for the first task (vitest-setup).

**Check here:**
https://github.com/persx/persx/pulls?q=is%3Apr+label%3Abot+is%3Adraft

### Review checklist

When PR appears:

- [ ] PR is labeled with `bot`
- [ ] You're assigned as reviewer
- [ ] PR is in draft status
- [ ] Changes are under 250 LOC
- [ ] PR description explains what changed
- [ ] `PR size gate` check passes (green)

### If PR looks good:

1. Click **"Ready for review"**
2. Review the code changes
3. Click **"Approve"**
4. Click **"Merge pull request"**

### After first merge:

Visit: https://github.com/persx/persx/settings/branches

- Add `test` to required status checks (after test workflow exists)
- Bot will pick next task automatically in 30 minutes

---

## 📊 Success Metrics

After 24 hours, check:

**PRs created:**
https://github.com/persx/persx/pulls?q=is%3Apr+label%3Abot

**Bot runs:**
https://github.com/persx/coder/actions/workflows/runner.yml

**Expected:** 1-2 PRs per day (bot runs every 30 min, but only creates PR when task is complete)

---

## 🆘 Troubleshooting

### No PR created after 30 minutes

1. Check workflow logs: https://github.com/persx/coder/actions
2. Look for errors in the latest run
3. Common issues:
   - API key doesn't have Sonnet access → Update secret with new key
   - GitHub token missing permissions → Recreate with correct permissions
   - Bot stopped early → Check logs for tool call failures

### PR too large (>250 LOC)

- Bot will mention in PR description
- PR size gate will fail (red X)
- Edit task in `tasks/persx.yaml` to reduce scope
- Push update to bot repo
- Wait for next run

### Checks failing

- Bot leaves PR in draft
- Review error messages in PR description
- Fix issues in persx/persx manually if needed
- Bot will try next task on next run

---

## 🎯 Quick Links

| Resource | URL |
|----------|-----|
| **Bot repo** | https://github.com/persx/coder |
| **Add secrets** | https://github.com/persx/coder/settings/secrets/actions |
| **Trigger workflow** | https://github.com/persx/coder/actions/workflows/runner.yml |
| **View PRs** | https://github.com/persx/persx/pulls?q=is%3Apr+label%3Abot |
| **Bot runs** | https://github.com/persx/coder/actions |
| **Branch protection** | https://github.com/persx/persx/settings/branches |
| **Create labels** | https://github.com/persx/persx/labels/new |

---

## ✅ Deployment Checklist

- [ ] Step 1: Add GitHub secrets (ANTHROPIC_API_KEY, GH_TOKEN)
- [ ] Step 2: Create 4 labels in persx/persx
- [ ] Step 3: Add CODEOWNERS file to persx/persx
- [ ] Step 4: Add PR size gate workflow to persx/persx
- [ ] Step 5: Enable branch protection on main
- [ ] Step 6: Trigger first bot run
- [ ] Step 7: Review and merge first PR

**Estimated total time:** 30 minutes

---

## 🎉 You're Done!

Once deployed, the bot will:

✅ Run every 30 minutes
✅ Pick tasks from `tasks/persx.yaml` in order
✅ Create draft PRs for you to review
✅ Auto-label and assign you
✅ Respect all guardrails (forbidden paths, LOC limits)
✅ Run checks before opening PRs

**First task:** vitest-setup (add Vitest + React Testing Library)

**Happy automating! 🤖**
