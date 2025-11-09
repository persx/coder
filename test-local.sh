#!/bin/bash
# Local test script for Claude Code bot
# Run this before triggering the GitHub Action to verify everything works

set -e

echo "🧪 Claude Code Bot - Local Test"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "app/bot.py" ]; then
    echo "❌ Error: Run this from the bot repo root directory"
    echo "   Expected: /Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx-coder"
    exit 1
fi

# Check for required environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo ""
    echo "   Set it with:"
    echo "   export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

if [ -z "$GH_TOKEN" ]; then
    echo "❌ Error: GH_TOKEN not set"
    echo ""
    echo "   Set it with:"
    echo "   export GH_TOKEN='your-token-here'"
    exit 1
fi

# Load target configuration
echo "📋 Loading target configuration..."
if [ ! -f "targets/persx.env" ]; then
    echo "❌ Error: targets/persx.env not found"
    exit 1
fi

export $(cat targets/persx.env | xargs)
echo "   ✓ Target: $TARGET_OWNER_REPO"
echo "   ✓ Model: $CLAUDE_MODEL"
echo "   ✓ Max loops: $MAX_LOOPS"
echo "   ✓ Token budget: $ANTHROPIC_BUDGET_TOKENS"
echo ""

# Check Python environment
echo "🐍 Checking Python environment..."
if [ ! -d ".venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
echo "   ✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "   ✓ Dependencies installed"
echo ""

# Verify required files exist
echo "📂 Verifying configuration files..."
if [ ! -f "$TASK_FILE" ]; then
    echo "❌ Error: $TASK_FILE not found"
    exit 1
fi
echo "   ✓ Task file: $TASK_FILE"

if [ ! -f "$SAFEOPS" ]; then
    echo "❌ Error: $SAFEOPS not found"
    exit 1
fi
echo "   ✓ Safeops config: $SAFEOPS"
echo ""

# Show what will happen
echo "🤖 Bot will:"
echo "   1. Clone $TARGET_REPO_URL"
echo "   2. Select first incomplete task from $TASK_FILE"
echo "   3. Run checks (npm ci, lint, build)"
echo "   4. Create a draft PR to $TARGET_OWNER_REPO"
echo "   5. Auto-label PR with 'bot'"
echo "   6. Assign owner as reviewer"
echo ""

# Confirm before running
read -p "Continue with local test? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "🚀 Running bot..."
echo "================================"
echo ""

# Run the bot
python app/bot.py

echo ""
echo "================================"
echo "✅ Local test complete!"
echo ""
echo "Next steps:"
echo "1. Check if a draft PR was created in persx/persx"
echo "2. Review the PR and verify it looks correct"
echo "3. If successful, add secrets to GitHub and trigger workflow"
echo "4. Workflow URL: https://github.com/persx/coder/actions/workflows/runner.yml"
