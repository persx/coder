# Local Development Guide

Test the Claude bot against your local persx repository before running it in production.

## Quick Start

### 1. Verify Your Setup

Your directory structure should look like this:

```
/Users/alexharrispro/Dropbox/2025/persx/dev/claude/
├── persx/              # Your local persx repo
└── persx-coder/        # The bot repo (this directory)
```

### 2. Set Your API Key

```bash
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

### 3. Run the Bot Locally

```bash
./run_local.sh
```

That's it! The bot will:
1. Read your local persx repo
2. Pick a task from `tasks/persx.yaml`
3. Make changes to your local files
4. Run checks (lint & build)
5. Show you what PR it would create

**No GitHub interactions** - everything stays local for testing.

---

## What Happens in Local Mode?

### ✅ The Bot WILL:
- Read files from your local persx repo
- Write changes to your local persx repo
- Run `npm ci`, `npm run lint`, `npm run build`
- Show detailed output of what it's doing
- Display the PR title/body it would create
- Track token usage

### ❌ The Bot WON'T:
- Push to GitHub
- Create actual PRs
- Modify remote repositories
- Use the GH_TOKEN

---

## Inspecting Changes

After the bot runs:

```bash
# Go to your persx repo
cd /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx

# See what changed
git status
git diff

# Review specific files
git diff app/page.tsx

# If you like the changes
git add -A
git commit -m "vitest setup (bot-generated)"

# If you don't like the changes
git restore .
```

---

## Manual Run (Without Script)

If you want more control:

```bash
# Activate venv
source .venv/bin/activate

# Set environment
export LOCAL_REPO_PATH="/Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx"
export ANTHROPIC_API_KEY='your-key-here'
export CLAUDE_MODEL=claude-sonnet-4-20250514
export MAX_LOOPS=6
export ANTHROPIC_BUDGET_TOKENS=120000
export TASK_FILE=tasks/persx.yaml
export SAFEOPS=configs/safeops_persx.json
export TARGET_OWNER_REPO=persx/persx
export PR_BASE=main

# Run bot
python app/bot_local.py
```

---

## Testing Different Tasks

### Force a Specific Task

Edit `tasks/persx.yaml` and comment out all but the task you want to test:

```yaml
# - slug: vitest-setup
#   goal: "Install Vitest + RTL + jsdom; add one smoke test for app/page.tsx."
#   constraints: { max_loc: 180 }

- slug: seo-basics
  goal: "Add robots.txt + sitemap route; default <meta> (& canonical) in app/layout.tsx."
  constraints: { max_loc: 200 }

# ... (comment out the rest)
```

Then run `./run_local.sh` again.

### Test With Different Constraints

Temporarily modify `configs/safeops_persx.json`:

```json
{
  "max_loc": 100,  // Stricter for testing
  "forbidden": ["app/**"],  // Test forbidding a path
  ...
}
```

---

## Common Workflows

### Workflow 1: Test a New Task

1. Add new task to `tasks/persx.yaml`
2. Run `./run_local.sh`
3. Review changes in persx repo
4. If good: commit to persx, push task to persx-coder
5. If bad: restore changes, refine task

### Workflow 2: Test Guardrails

1. Add a forbidden path to `configs/safeops_persx.json`
2. Create a task that tries to touch it
3. Run bot - should see error message
4. Verify guardrails work

### Workflow 3: Iterative Development

```bash
# Run bot
./run_local.sh

# Review changes
cd ../persx && git diff

# Not quite right? Restore and adjust task
git restore .

# Tweak the task in persx-coder/tasks/persx.yaml
cd ../persx-coder
vim tasks/persx.yaml

# Try again
./run_local.sh
```

---

## Troubleshooting

### "Local repo not found"

Update `LOCAL_REPO_PATH` in `run_local.sh`:

```bash
export LOCAL_REPO_PATH="/path/to/your/persx/repo"
```

### "ANTHROPIC_API_KEY not set"

Set it in your shell:

```bash
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

Or add to your `~/.zshrc` or `~/.bashrc`:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.zshrc
source ~/.zshrc
```

### "Module not found"

Install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Bot makes no changes

Check:
1. Is the task clear enough?
2. Are the target files in allowed paths?
3. Check bot output for errors
4. Try increasing `MAX_LOOPS` to 10

### Checks fail (lint/build)

This is expected if:
- Your local repo has uncommitted changes
- Dependencies aren't installed (`npm ci` might fail)

Fix:
```bash
cd /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx
npm ci
npm run lint
npm run build
```

---

## Comparing Local vs Production

| Feature | Local Mode | Production (GitHub Actions) |
|---------|-----------|----------------------------|
| Repo source | Your local clone | Fresh clone each run |
| Changes | Written locally | Pushed to branch |
| PR creation | Simulated (prints only) | Real draft PR |
| GitHub API | Disabled | Enabled |
| Frequency | Manual | Every 30 min |
| Safe to test | ✅ Yes | ⚠️ Only after local testing |

---

## Best Practices

### ✅ DO:
- Test all new tasks locally first
- Review diffs before committing
- Keep local persx repo on main branch
- Commit/push persx changes separately from bot changes

### ❌ DON'T:
- Run bot on a dirty working tree (commit your work first)
- Push bot-generated changes without review
- Run production workflow until local testing passes
- Mix manual edits with bot edits in same commit

---

## Advanced: Custom Local Config

Create `targets/local.env` for local-specific settings:

```bash
LOCAL_REPO_PATH=/Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx
TARGET_OWNER_REPO=persx/persx
PR_BASE=main
TASK_FILE=tasks/persx.yaml
SAFEOPS=configs/safeops_persx.json
CLAUDE_MODEL=claude-sonnet-4-20250514
MAX_LOOPS=6
ANTHROPIC_BUDGET_TOKENS=120000
```

Then run:

```bash
export $(cat targets/local.env | xargs)
python app/bot_local.py
```

---

## Next Steps

Once local testing passes:

1. ✅ Commit bot changes to persx-coder repo
2. ✅ Push to GitHub
3. ✅ Complete manual setup (labels, CODEOWNERS, branch protection)
4. ✅ Trigger production workflow
5. ✅ Review first real PR

**Local development = confidence before production!** 🚀
