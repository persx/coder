# Install CODEOWNERS and PR Size Gate

These files need to be added to the **persx/persx** repo (not the bot repo).

## Option 1: Manual Creation (Recommended)

### 1. Create CODEOWNERS
Visit: https://github.com/persx/persx/new/main?filename=.github/CODEOWNERS

Copy/paste contents from: `setup/CODEOWNERS`

Click **"Commit new file"**

### 2. Create PR Size Gate Workflow
Visit: https://github.com/persx/persx/new/main?filename=.github/workflows/pr-size.yml

Copy/paste contents from: `setup/pr-size.yml`

Click **"Commit new file"**

---

## Option 2: Using Git CLI

Clone persx/persx and add files:

```bash
# Clone the target repo
cd /tmp
git clone https://github.com/persx/persx.git
cd persx

# Create .github directory if it doesn't exist
mkdir -p .github/workflows

# Copy files
cp /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx-coder/setup/CODEOWNERS .github/CODEOWNERS
cp /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx-coder/setup/pr-size.yml .github/workflows/pr-size.yml

# Commit and push
git add .github/CODEOWNERS .github/workflows/pr-size.yml
git commit -m "Add CODEOWNERS and PR size gate workflow"
git push origin main
```

---

## Verification

After adding files, verify:

1. **CODEOWNERS exists:**
   https://github.com/persx/persx/blob/main/.github/CODEOWNERS

2. **PR size workflow exists:**
   https://github.com/persx/persx/blob/main/.github/workflows/pr-size.yml

3. **Workflow is active:**
   https://github.com/persx/persx/actions
   (After first PR, you should see "PR size gate" in the workflows list)
