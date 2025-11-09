# Claude Code Bot (24/7, repo-agnostic)

A minimal, **separate** project that runs a Claude-powered coding bot against *any* GitHub repo.
It clones the target, proposes **small, safe PRs** (tests, docs, refactors, a11y/SEO fixes), and leaves draft PRs for review.

## 🚀 Quick Start

### Option 1: Local Development (Recommended First)

Test the bot against your local persx repository:

```bash
./run_local.sh
```

See [`LOCAL_DEVELOPMENT.md`](./LOCAL_DEVELOPMENT.md) for detailed guide.

### Option 2: Production Setup

Deploy to GitHub Actions for 24/7 automated PRs:

See [`LAUNCH_CHECKLIST.md`](./LAUNCH_CHECKLIST.md) for complete setup guide.

---

## 📁 Repository Structure

```
persx-coder/
├── app/
│   ├── bot.py              # Production bot (GitHub Actions)
│   └── bot_local.py        # Local development bot
├── configs/
│   └── safeops_persx.json  # Guardrails: forbidden paths, LOC limits
├── tasks/
│   └── persx.yaml          # Task backlog (8 MVP tasks)
├── targets/
│   └── persx.env           # Environment config
├── .github/
│   ├── workflows/
│   │   └── runner.yml      # GitHub Actions workflow
│   ├── CODEOWNERS.template # Template for persx/persx
│   ├── pr-size-gate.yml.template
│   └── SETUP.md            # Manual setup steps
├── run_local.sh            # Local development runner
├── LOCAL_DEVELOPMENT.md    # Local dev guide
└── LAUNCH_CHECKLIST.md     # Production setup guide
```

---

## 🎯 How It Works

1. **Bot orchestrator** (`app/bot.py`) uses Anthropic tool-use
2. **Tools exposed**: read_repo, write_file, run_checks, open_pr
3. **Tasks** (`tasks/*.yaml`) define tiny, scoped improvements
4. **Guardrails** (`configs/safeops_*.json`) enforce safety rules
5. **Target config** (`targets/*.env`) specifies which repo to target

### Safety Rules

- ✅ Draft PRs only
- ✅ Never touch forbidden paths (auth, billing, migrations)
- ✅ Small diffs (<250 LOC for first week)
- ✅ Run checks before PR
- ✅ Token budget enforcement
- ✅ Auto-assign reviewer

---

## 📋 Task Backlog (MVP)

Ordered for maximum marketing impact:

1. **vitest-setup** (180 LOC) - Testing foundation
2. **zod-roadmap** (180 LOC) - API validation
3. **seo-basics** (200 LOC) - SEO fundamentals
4. **a11y-sweep** (160 LOC) - Accessibility fixes
5. **schema-org** (120 LOC) - Structured data
6. **perf-preconnect** (150 LOC) - Performance hints
7. **copy-polish** (140 LOC) - Meta tag optimization
8. **routing-hygiene** (160 LOC) - Canonical URLs

---

## 🔧 Local Development Workflow

### Test a Task Locally

```bash
# Run bot against local persx repo
./run_local.sh

# Review changes
cd ../persx
git status
git diff

# Keep or discard
git commit -m "bot: vitest setup"
# OR
git restore .
```

### Iterate on Tasks

```bash
# Edit task
vim tasks/persx.yaml

# Test again
./run_local.sh

# Repeat until satisfied
```

See [`LOCAL_DEVELOPMENT.md`](./LOCAL_DEVELOPMENT.md) for details.

---

## 🚀 Production Deployment

### Prerequisites

- [ ] GitHub repo created (persx/coder)
- [ ] Secrets added (ANTHROPIC_API_KEY, GH_TOKEN)
- [ ] Labels created in target repo (bot, safe-change, needs-human, blocked)
- [ ] CODEOWNERS added to target repo
- [ ] Branch protection enabled on target repo main branch
- [ ] PR size gate added to target repo

### Deploy

1. Push this repo to GitHub
2. Complete manual setup steps (see [`LAUNCH_CHECKLIST.md`](./LAUNCH_CHECKLIST.md))
3. Trigger workflow: https://github.com/persx/coder/actions/workflows/runner.yml

### Monitor

- Workflow runs every 30 minutes
- Creates draft PRs in target repo
- Sends Slack notifications (if configured)
- Auto-assigns you as reviewer

---

## ⚙️ Configuration

### Adjust Guardrails

Edit `configs/safeops_persx.json`:

```json
{
  "max_loc": 250,
  "forbidden": ["auth/**", "billing/**", ...],
  "allowed_globs": ["app/**", "components/**", ...]
}
```

### Add Tasks

Edit `tasks/persx.yaml`:

```yaml
- slug: new-task
  goal: "Clear, specific goal in one sentence."
  constraints: { max_loc: 180 }
```

### Adjust Cost Caps

Edit `targets/persx.env`:

```bash
MAX_LOOPS=6                    # Loops per run
ANTHROPIC_BUDGET_TOKENS=120000 # Token budget
CLAUDE_MODEL=claude-sonnet-4-20250514
```

---

## 📊 Success Metrics

After first week, track:

- **PR merge rate**: Target 80%+
- **Review time**: Target <1 hour per PR
- **Failed checks**: Target <10%
- **Token usage**: Monitor daily average

---

## 🆘 Troubleshooting

See [`LAUNCH_CHECKLIST.md`](./LAUNCH_CHECKLIST.md#-troubleshooting) for common issues.

**Quick checks:**

- [ ] Secrets set correctly
- [ ] Branch protection enabled
- [ ] Labels exist
- [ ] Local test passes
- [ ] Task is clear and scoped

---

## 📚 Documentation

- [`LOCAL_DEVELOPMENT.md`](./LOCAL_DEVELOPMENT.md) - Test bot locally
- [`LAUNCH_CHECKLIST.md`](./LAUNCH_CHECKLIST.md) - Production setup
- [`.github/SETUP.md`](./.github/SETUP.md) - Manual setup steps

---

## 🎓 Best Practices

**Task Design:**
- One clear goal per task
- <200 LOC target
- Order by: tests → validation → SEO → performance

**Review Process:**
- Merge green PRs same day
- Use labels for tracking
- Comment with guidance if changes needed

**Scaling:**
- After 10 successful merges: increase max_loc to 300
- After 20 successful merges: add more tasks per cycle
- Monitor token usage and adjust budget

---

## 🏗️ Architecture

**Orchestrator** (Python service)
- Pulls tasks from YAML backlog
- Plans work with Claude via tool-use
- Loops until done or guardrails trip
- Runs on GitHub Actions or locally

**Claude** (planning + code generation)
- Uses Anthropic Python SDK
- Tool-use for read/write/check/PR operations
- Follows safety rules in system prompt

**Sandbox runner**
- Ephemeral Docker container (in Actions)
- Clones repo, installs deps, runs checks
- Produces artifacts (diff, test results)

**GitHub integration**
- Creates draft PRs with structured template
- Auto-labels, auto-assigns reviewer
- Posts test summaries

---

## 🔐 Security

- Never touches forbidden paths
- Never pushes to main
- Draft PRs require human approval
- Token budget prevents runaway costs
- All changes are reversible

---

## 📄 License

MIT

---

**Ready to ship continuous improvements?** Start with [`LOCAL_DEVELOPMENT.md`](./LOCAL_DEVELOPMENT.md)! 🚀
