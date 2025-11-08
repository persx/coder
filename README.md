# Claude Code Bot (24/7, repo-agnostic)

A minimal, **separate** project that runs a Claude-powered coding bot against *any* GitHub repo.
It clones the target, proposes **small, safe PRs** (tests, docs, refactors, a11y/SEO fixes), and leaves draft PRs for review.

## Quick start

### 1) Create a new private GitHub repo and push this folder
```bash
git init
git add -A
git commit -m "init: claude code bot starter"
git branch -M main
git remote add origin <YOUR_NEW_REPO_URL>
git push -u origin main
```

### 2) Add Actions Secrets to this **bot** repo
- `ANTHROPIC_API_KEY` — your Claude API key
- `GH_TOKEN` — GitHub **fine-grained** PAT with `Contents: Read/Write`, `Pull requests: Read/Write` on target repos

### 3) (Optional) Configure schedule in `.github/workflows/runner.yml`
It runs every 30 minutes and on manual dispatch.

### 4) First target: persx/persx (MVP)
Edit `targets/persx.env` if needed and commit. Then trigger the workflow (Actions → *Run workflow*).

### 5) Local run (good for smoke-tests)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export $(cat targets/persx.env | xargs)  # loads TARGET_* vars
python app/bot.py
```

## How it works
- `app/bot.py` — orchestrator using Anthropic tool-use.
- Tools exposed: read_repo, write_file, run_checks (npm lint/build), open_pr.
- `tasks/*.yaml` — tiny, scoped tasks the bot can choose from.
- `configs/safeops_*.json` — guardrails: forbidden/allowed globs, LOC limits, etc.
- `targets/*.env` — per-target environment (repo URL, owner/name).

## Safety rules
- Draft PRs only; never touch forbidden globs; small diffs; run checks.
- If checks fail, open an issue-like PR description rather than shipping a risky change.

## Notes
- Keep tasks **tiny**. One win per PR.
- Start with tests, a11y and SEO—high-ROI for content and growth.
