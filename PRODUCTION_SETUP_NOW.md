# 🚀 Production Setup - Do This Now! (20 minutes)

Complete these 5 steps to go live with your Claude coding bot.

---

## ✅ Step 1: Add Labels to persx/persx (5 min)

### Method A: Using GitHub UI (Recommended)

Visit each URL and fill in the form:

**1. Create 'bot' label:**
- URL: https://github.com/persx/persx/labels/new
- Name: `bot`
- Description: `Automated changes from Claude bot`
- Color: `#0e8a16` (green)
- Click "Create label"

**2. Create 'safe-change' label:**
- URL: https://github.com/persx/persx/labels/new
- Name: `safe-change`
- Description: `Low-risk change verified by guardrails`
- Color: `#bfdadc` (light blue)
- Click "Create label"

**3. Create 'needs-human' label:**
- URL: https://github.com/persx/persx/labels/new
- Name: `needs-human`
- Description: `Requires human review and decision`
- Color: `#fbca04` (yellow)
- Click "Create label"

**4. Create 'blocked' label:**
- URL: https://github.com/persx/persx/labels/new
- Name: `blocked`
- Description: `Bot cannot proceed - manual intervention needed`
- Color: `#d93f0b` (red)
- Click "Create label"

### Method B: Using gh CLI (Faster)

```bash
gh label create "bot" --color "0e8a16" --description "Automated changes from Claude bot" --repo persx/persx
gh label create "safe-change" --color "bfdadc" --description "Low-risk change verified by guardrails" --repo persx/persx
gh label create "needs-human" --color "fbca04" --description "Requires human review and decision" --repo persx/persx
gh label create "blocked" --color "d93f0b" --description "Bot cannot proceed - manual intervention needed" --repo persx/persx
```

✅ **Verify:** Visit https://github.com/persx/persx/labels - should see 4 new labels

---

## ✅ Step 2: Add CODEOWNERS to persx/persx (2 min)

### Create the file:

Visit: https://github.com/persx/persx/new/main?filename=.github/CODEOWNERS

### Paste this content:

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

### Commit:
- Click "Commit changes..."
- Commit message: `Add CODEOWNERS for bot PRs`
- Click "Commit changes"

✅ **Verify:** File exists at https://github.com/persx/persx/blob/main/.github/CODEOWNERS

---

## ✅ Step 3: Add PR Size Gate to persx/persx (2 min)

### Create the file:

Visit: https://github.com/persx/persx/new/main?filename=.github/workflows/pr-size.yml

### Paste this content:

```yaml
name: PR size gate
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const pr = context.payload.pull_request;
            const added = pr.additions || 0, removed = pr.deletions || 0;
            if (added + removed > 250) {
              core.setFailed(`PR too large (${added+removed} LOC). Keep it tiny.`);
            }
```

### Commit:
- Click "Commit changes..."
- Commit message: `Add PR size gate workflow`
- Click "Commit changes"

✅ **Verify:** File exists at https://github.com/persx/persx/blob/main/.github/workflows/pr-size.yml

---

## ✅ Step 4: Enable Branch Protection on persx/persx (3 min)

### Configure protection:

1. Visit: https://github.com/persx/persx/settings/branches
2. Click **"Add branch protection rule"**

### Settings:

**Branch name pattern:**
```
main
```

**Enable these checkboxes:**

- ✅ **Require a pull request before merging**
  - ✅ Require approvals: `1`
  - ✅ Require approval from code owners

- ✅ **Require status checks to pass before merging**
  - Click "Search for status checks" and type: `lint`
  - Add: `lint`
  - Type: `build`
  - Add: `build`
  - Type: `PR size gate`
  - Add: `PR size gate`
  - ✅ Require branches to be up to date before merging

- ✅ **Do not allow bypassing the above settings**

**Click "Create"** at the bottom

✅ **Verify:** Visit https://github.com/persx/persx/settings/branches - should see protection rule for `main`

---

## ✅ Step 5: (Optional) Configure Slack Webhook (2 min)

### Skip if you don't want Slack notifications

### Create webhook:

1. Visit: https://api.slack.com/messaging/webhooks
2. Click "Create your Slack app"
3. Choose "From scratch"
4. App name: `Claude Bot`
5. Select your workspace
6. Click "Incoming Webhooks"
7. Turn on "Activate Incoming Webhooks"
8. Click "Add New Webhook to Workspace"
9. Select channel (e.g., `#bot-prs`)
10. Click "Allow"
11. **Copy the Webhook URL** (starts with `https://hooks.slack.com/services/...`)

### Add secret to bot repo:

1. Visit: https://github.com/persx/coder/settings/secrets/actions/new
2. Name: `SLACK_WEBHOOK_URL`
3. Secret: Paste your webhook URL
4. Click "Add secret"

✅ **Verify:** Visit https://github.com/persx/coder/settings/secrets/actions - should see `SLACK_WEBHOOK_URL`

---

## 🎯 Launch! Trigger First Workflow Run

### Trigger the workflow:

1. Visit: https://github.com/persx/coder/actions/workflows/runner.yml
2. Click **"Run workflow"** button (top right)
3. Select branch: **main**
4. Click **"Run workflow"**

### Watch it run:

1. Refresh the page - you'll see a new workflow run
2. Click on it to watch live output
3. Wait ~2-5 minutes for completion

### What the bot will do:

1. ✅ Clone persx/persx
2. ✅ Read the codebase
3. ✅ Pick first task (vitest-setup)
4. ✅ Make changes
5. ✅ Run `npm ci`, `npm run lint`, `npm run build`
6. ✅ Create draft PR
7. ✅ Auto-label with `bot`
8. ✅ Assign you as reviewer
9. ✅ Send Slack notification (if configured)

### Check for your first PR:

Visit: https://github.com/persx/persx/pulls

You should see a new **draft PR** with:
- ✅ `bot` label
- ✅ You assigned as reviewer
- ✅ CI checks running (lint & build)
- ✅ Detailed description of changes

---

## 📋 Checklist (Mark as you complete)

- [ ] Labels created (bot, safe-change, needs-human, blocked)
- [ ] CODEOWNERS file added
- [ ] PR size gate workflow added
- [ ] Branch protection enabled
- [ ] Slack webhook configured (optional)
- [ ] First workflow triggered
- [ ] First PR created successfully
- [ ] PR has bot label
- [ ] You are assigned as reviewer
- [ ] CI checks ran

---

## 🎉 You're Live!

Once the first PR is created:

1. **Review the PR** - Check the changes are sensible
2. **Approve if green** - If tests pass and changes look good
3. **Merge it** - Click "Ready for review" → Approve → Merge
4. **Wait 30 min** - Bot will pick next task automatically
5. **Repeat** - Review → Approve → Merge

### The bot will now:
- ✅ Run every 30 minutes
- ✅ Pick one task at a time
- ✅ Create small, safe PRs
- ✅ Never touch forbidden paths
- ✅ Auto-assign you for review

---

## 🆘 Troubleshooting

### No PR created after workflow run?

Check workflow logs:
- Visit: https://github.com/persx/coder/actions
- Click latest run
- Check for errors

Common causes:
- API key invalid
- GH_TOKEN permissions insufficient
- Forbidden path blocking task
- No tasks in backlog

### Checks failing?

First PR might fail checks if:
- Dependencies not installed
- Lint errors in existing code
- Build configuration issues

**Fix:** Review the PR, fix issues manually, or skip to next task

### Bot makes no changes?

Increase verbosity or check task is clear enough.
May need to refine task description in `tasks/persx.yaml`

---

## 📞 Need Help?

Review documentation:
- `LOCAL_DEVELOPMENT.md` - Test locally first
- `LAUNCH_CHECKLIST.md` - Detailed setup guide
- `.github/SETUP.md` - Manual setup reference

---

**Ready? Start with Step 1!** ⬆️
