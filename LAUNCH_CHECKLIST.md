# 🚀 Claude Bot Launch Checklist

## ✅ Automated Setup (COMPLETE)

All code changes have been pushed to https://github.com/persx/coder

- ✅ Bot repository initialized and pushed
- ✅ Indentation fixes in bot.py
- ✅ Guardrails configured (max_loc=250, forbidden paths)
- ✅ Cost caps added (MAX_LOOPS=6, 120K token budget)
- ✅ Token usage tracking implemented
- ✅ Auto-labeling PRs with 'bot'
- ✅ Auto-assign owner as reviewer
- ✅ Slack/Teams webhook support ready
- ✅ 8 explicit MVP tasks defined
- ✅ PR size gate template created
- ✅ Slack notification step added to workflow
- ✅ CODEOWNERS template created
- ✅ Setup documentation complete

## 📋 Manual Steps Required (~20 minutes total)

### 1. Add GitHub Labels to persx/persx (5 min)

Visit: https://github.com/persx/persx/labels/new

Create these 4 labels:

| Name | Color | Description |
|------|-------|-------------|
| `bot` | `#0e8a16` | Automated changes from Claude bot |
| `safe-change` | `#bfdadc` | Low-risk change verified by guardrails |
| `needs-human` | `#fbca04` | Requires human review and decision |
| `blocked` | `#d93f0b` | Bot cannot proceed - manual intervention needed |

### 2. Add CODEOWNERS to persx/persx (2 min)

Create file: https://github.com/persx/persx/new/main?filename=.github/CODEOWNERS

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

### 3. Add PR Size Gate to persx/persx (2 min)

Create file: https://github.com/persx/persx/new/main?filename=.github/workflows/pr-size.yml

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

### 4. Enable Branch Protection on persx/persx (3 min)

Visit: https://github.com/persx/persx/settings/branches

**Add rule for:** `main`

**Enable:**
- ✅ Require a pull request before merging
- ✅ Require approvals: 1
- ✅ Require status checks to pass before merging
  - Select: `lint`, `build` (after first workflow run creates them)
  - Add: `PR size gate` (after step 3)
- ✅ Require approval from code owners
- ✅ Do not allow bypassing the above settings

### 5. Configure Slack Webhook (2 min) - OPTIONAL

**Create webhook:**
1. Visit: https://api.slack.com/messaging/webhooks
2. Create incoming webhook
3. Select channel: `#bot-prs` or similar
4. Copy webhook URL

**Add secret to bot repo:**

Visit: https://github.com/persx/coder/settings/secrets/actions/new

- **Name:** `SLACK_WEBHOOK_URL`
- **Value:** Your webhook URL from above

### 6. Trigger First Bot Run (1 min)

Visit: https://github.com/persx/coder/actions/workflows/runner.yml

Click **"Run workflow"** → Select branch: **main** → Click **"Run workflow"**

The bot will:
1. Clone persx/persx
2. Select first task (vitest-setup)
3. Run npm ci, lint, build
4. Open draft PR with changes
5. Auto-label with `bot`
6. Assign you as reviewer
7. Send Slack notification (if configured)

---

## 🎯 MVP Task Sequence (Recommended Order)

The bot will automatically pick tasks in order. Expected timeline:

### Week 1: Foundation (Days 1-3)
1. **vitest-setup** - Install Vitest + RTL + jsdom; add smoke test
   - After merge: Add `test` to branch protection required checks
2. **zod-roadmap** - Add validation to submit-roadmap API route
3. **seo-basics** - robots.txt, sitemap, meta tags

### Week 2: Polish & Performance (Days 4-7)
4. **a11y-sweep** - Fix alt text and labels (no layout changes)
5. **schema-org** - Add JSON-LD structured data
6. **perf-preconnect** - Preconnect hints + lazy loading
7. **copy-polish** - Title case + length limits on meta tags
8. **routing-hygiene** - Canonical tags per page

**After 3-4 successful merges:** Add `test` to required status checks

---

## 📊 Safety Features Active

| Feature | Value | Purpose |
|---------|-------|---------|
| Max LOC | 250 | Keep PRs tiny and reviewable |
| Max Loops | 6 | Prevent runaway API usage |
| Token Budget | 120,000 | Hard cap on cost per run |
| Run Frequency | Every 30 min | Continuous small improvements |
| PR Status | Draft | Require manual review & approval |

### Forbidden Paths
The bot CANNOT touch:
- `auth/**` - Authentication code
- `billing/**` - Payment/subscription code
- `supabase/seed.sql` - Database seed data
- `supabase/migrations/**` - Database migrations
- `.env*` - Environment variables
- `next.config.*` - Next.js configuration
- `scripts/**` - Build/deploy scripts
- `package.json`, `package-lock.json`, `tsconfig.json` - Config files

### Allowed Paths
The bot CAN modify:
- `app/**` - Application routes & pages
- `components/**` - React components
- `lib/**` - Utility libraries
- `types/**` - TypeScript types
- `public/**` - Static assets
- `docs/**` - Documentation

---

## 🔍 First PR Acceptance Path (Today)

1. Wait for bot to create vitest-setup PR
2. Review the draft PR:
   - Check diff is <250 LOC
   - Verify tests pass
   - Check smoke test works
3. Approve and merge
4. **Important:** Add `test` to branch protection required checks
5. Next cycle: bot picks zod-roadmap task

---

## 📈 Success Metrics

Track these after first week:

- **PR merge rate:** Target 80%+ (high = good task quality)
- **Review time:** Target <1 hour per PR (tiny PRs are fast)
- **Failed checks:** Target <10% (low = guardrails working)
- **Token usage:** Monitor daily average, should stay <120K

---

## 🆘 Troubleshooting

**Bot creates no PR:**
- Check workflow logs: https://github.com/persx/coder/actions
- Verify secrets are set correctly
- Check if forbidden paths were blocking the task

**PR too large:**
- PR size gate will fail
- Check if task constraints need tightening
- May need to split task into smaller pieces

**Checks failing:**
- Bot will leave PR in draft status
- Review errors in PR description
- May need to manually fix + amend

**No Slack notifications:**
- Verify `SLACK_WEBHOOK_URL` secret is set
- Check webhook URL is valid
- Test webhook with curl

---

## 🎓 Best Practices

**Weekly backlog grooming:**
- Keep 6-12 tiny tasks queued
- Order by: tests → validation → SEO → performance → polish
- Each task should target one specific improvement

**PR review guidelines:**
- Merge green PRs quickly (same day if possible)
- Comment with guidance if changes needed
- Use `needs-human` label for complex decisions

**Scaling up:**
- After 10 successful merges, increase max_loc to 300
- After 20 successful merges, add more tasks per cycle
- Monitor token usage and adjust budget if needed

---

## ✅ Pre-Flight Checklist

Before triggering first run, verify:

- [ ] Labels created in persx/persx
- [ ] CODEOWNERS added to persx/persx
- [ ] PR size gate workflow added to persx/persx
- [ ] Branch protection enabled on persx/persx main
- [ ] Secrets set in persx/coder (ANTHROPIC_API_KEY, GH_TOKEN)
- [ ] Slack webhook configured (optional)
- [ ] All manual setup steps completed

**Ready to launch?** → https://github.com/persx/coder/actions/workflows/runner.yml

---

**Questions?** Review `.github/SETUP.md` for detailed instructions.
