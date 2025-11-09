# Quick Start Guide - Complete Setup in Order

Follow these steps to get the Claude Code bot running.

## ✅ Pre-Flight Checklist

Before starting, verify:
- [ ] Bot code exists at: `/Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx-coder`
- [ ] You have an Anthropic API key
- [ ] You have GitHub admin access to `persx/persx` repo
- [ ] Python 3.11+ installed

---

## Step 1: Create GitHub Fine-Grained PAT (~5 min)

📖 **Guide:** `setup/CREATE_GITHUB_PAT.md`

**Quick version:**
1. Visit: https://github.com/settings/tokens?type=beta
2. Click "Generate new token"
3. Configure:
   - Name: `claude-bot-persx`
   - Expiration: 90 days
   - Repository access: Only select repositories → `persx/persx`
   - Permissions:
     - Contents: Read and write
     - Pull requests: Read and write
4. Generate and **COPY TOKEN** (starts with `github_pat_...`)
5. Save it securely - you'll need it in Step 3

---

## Step 2: Create Labels in persx/persx (~5 min)

**Option A: Using gh CLI (recommended)**
```bash
cd /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx-coder
./setup/create-labels.sh
```

**Option B: Manual creation**
📖 **Guide:** `setup/create-labels-manual.md`

Visit: https://github.com/persx/persx/labels/new

Create 4 labels: `bot`, `safe-change`, `needs-human`, `blocked`
(See guide for exact colors/descriptions)

---

## Step 3: Add Files to persx/persx (~5 min)

📖 **Guide:** `setup/INSTALL_FILES.md`

**Quick version - Manual (recommended):**

### 3a. Create CODEOWNERS
1. Visit: https://github.com/persx/persx/new/main?filename=.github/CODEOWNERS
2. Copy contents from: `setup/CODEOWNERS`
3. Commit

### 3b. Create PR Size Gate
1. Visit: https://github.com/persx/persx/new/main?filename=.github/workflows/pr-size.yml
2. Copy contents from: `setup/pr-size.yml`
3. Commit

---

## Step 4: Push Bot Repo to GitHub (~3 min)

**Check if already pushed:**
```bash
cd /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx-coder
git remote -v
```

**If no remote, push now:**
```bash
git init
git add -A
git commit -m "init: claude code bot"
git remote add origin https://github.com/persx/coder.git
git branch -M main
git push -u origin main
```

---

## Step 5: Add Secrets to Bot Repo (~2 min)

Visit: https://github.com/persx/coder/settings/secrets/actions/new

Add these two secrets:

**Secret 1:**
- Name: `ANTHROPIC_API_KEY`
- Value: Your Anthropic API key

**Secret 2:**
- Name: `GH_TOKEN`
- Value: The GitHub PAT you created in Step 1

**Optional (for Slack notifications):**
- Name: `SLACK_WEBHOOK_URL`
- Value: Your Slack webhook URL

Verify at: https://github.com/persx/coder/settings/secrets/actions

---

## Step 6: Run Local Test (~5 min)

This verifies everything works before triggering the GitHub Action.

```bash
cd /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx-coder

# Set environment variables
export ANTHROPIC_API_KEY='your-anthropic-key'
export GH_TOKEN='your-github-pat'

# Run test script
./test-local.sh
```

**What happens:**
- Creates virtual environment
- Installs dependencies
- Clones persx/persx
- Selects first task (vitest-setup)
- Creates draft PR
- Labels it 'bot'
- Assigns you as reviewer

**If successful:** You'll see a draft PR at https://github.com/persx/persx/pulls

**If it fails:** Check error messages and verify:
- API keys are correct
- GitHub PAT has correct permissions
- You can access persx/persx repo

---

## Step 7: Enable Branch Protection (~3 min)

Visit: https://github.com/persx/persx/settings/branches

**Add rule for:** `main`

**Enable:**
- ✅ Require a pull request before merging
- ✅ Require approvals: 1
- ✅ Require status checks to pass before merging
  - Wait for first PR to run, then add: `PR size gate`
- ✅ Require approval from code owners
- ✅ Do not allow bypassing the above settings

**Note:** Add `lint`, `build`, and `test` status checks after workflows exist.

---

## Step 8: Trigger First Workflow Run (~1 min)

Visit: https://github.com/persx/coder/actions/workflows/runner.yml

1. Click **"Run workflow"**
2. Select branch: **main**
3. Click **"Run workflow"**

Watch the workflow run at: https://github.com/persx/coder/actions

---

## Step 9: Review First PR (~10 min)

The bot will create a draft PR for the `vitest-setup` task.

**Review checklist:**
- [ ] Diff is under 250 LOC
- [ ] Changes look reasonable
- [ ] Tests pass (if checks run)
- [ ] PR is labeled with 'bot'
- [ ] You're assigned as reviewer

**If good:**
1. Approve the PR
2. Mark as "Ready for review" (if draft)
3. Merge it

**After first merge:**
- Add `test` to branch protection required checks
- Bot will pick up next task (zod-roadmap) in 30 minutes

---

## Step 10: Monitor & Iterate

**Watch for new PRs:**
https://github.com/persx/persx/pulls?q=is%3Apr+label%3Abot

**Check workflow runs:**
https://github.com/persx/coder/actions

**Add more tasks:**
Edit `tasks/persx.yaml` in the bot repo

**Adjust constraints:**
Edit `configs/safeops_persx.json` in the bot repo

---

## 🆘 Troubleshooting

**Local test fails with "permission denied":**
- Verify GH_TOKEN has correct permissions
- Re-create token with Contents + Pull Requests access

**Bot creates no PR:**
- Check workflow logs at: https://github.com/persx/coder/actions
- Verify all secrets are set correctly
- Check if task constraints are too restrictive

**PR too large:**
- Bot will detect and mention in PR description
- PR size gate will fail
- Adjust task constraints in tasks/persx.yaml

**Checks failing:**
- Bot leaves PR in draft status
- Review errors in workflow logs
- May need to adjust safeops forbidden paths

---

## 📊 Success!

Once everything is running:

- Bot runs every 30 minutes
- Creates draft PRs for tasks
- Auto-labels and assigns you
- You review and merge
- Bot picks next task automatically

**Expected pace:** 1-2 merged PRs per day (tiny incremental improvements)

---

## Quick Links

- **Bot repo:** https://github.com/persx/coder
- **Target repo:** https://github.com/persx/persx
- **Workflow:** https://github.com/persx/coder/actions/workflows/runner.yml
- **Draft PRs:** https://github.com/persx/persx/pulls?q=is%3Apr+label%3Abot+is%3Adraft
