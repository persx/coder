# How to Create GitHub Fine-Grained PAT

## Step 1: Go to GitHub Settings
Visit: https://github.com/settings/tokens?type=beta

Click **"Generate new token"**

## Step 2: Configure Token

### Basic Information
- **Token name:** `claude-bot-persx` (or similar)
- **Expiration:** 90 days (or custom - you'll need to rotate it)
- **Description:** `Claude Code bot access to persx/persx repo`

### Repository Access
- Select: **"Only select repositories"**
- Choose: **persx/persx**

### Permissions (Repository permissions section)

Set these permissions:

| Permission | Access Level |
|------------|--------------|
| **Contents** | Read and write |
| **Pull requests** | Read and write |
| **Metadata** | Read-only (automatic) |

### Permissions NOT needed
- Issues: No
- Actions: No
- Workflows: No
- Administration: No

## Step 3: Generate & Copy Token

1. Click **"Generate token"** at bottom
2. **IMMEDIATELY COPY** the token (starts with `github_pat_...`)
3. Store it securely - you won't see it again!

## Step 4: Add to Bot Repo Secrets

Visit: https://github.com/persx/coder/settings/secrets/actions/new

- **Name:** `GH_TOKEN`
- **Secret:** Paste the token you just copied
- Click **"Add secret"**

## Step 5: Add Anthropic API Key

While you're there, add:

- **Name:** `ANTHROPIC_API_KEY`
- **Secret:** Your Claude API key
- Click **"Add secret"**

## Verification

After adding both secrets, you should see:
- `ANTHROPIC_API_KEY` ✓
- `GH_TOKEN` ✓

at: https://github.com/persx/coder/settings/secrets/actions

---

## Quick Links

- Create PAT: https://github.com/settings/tokens?type=beta
- Add secrets: https://github.com/persx/coder/settings/secrets/actions/new
- Verify secrets: https://github.com/persx/coder/settings/secrets/actions
