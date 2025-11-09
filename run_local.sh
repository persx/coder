#!/bin/bash

# Claude Bot - Local Development Runner
# Runs the bot against your local persx repo for testing

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 Claude Bot - Local Development Mode${NC}"
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Check if dependencies installed
if [ ! -f ".venv/lib/python3.10/site-packages/anthropic/__init__.py" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Set local repo path (adjust if your persx repo is elsewhere)
export LOCAL_REPO_PATH="/Users/alexharrispro/Dropbox/2025/persx/dev/claude/persx"

# Check if local repo exists
if [ ! -d "$LOCAL_REPO_PATH" ]; then
    echo -e "${RED}❌ ERROR: Local repo not found at: $LOCAL_REPO_PATH${NC}"
    echo ""
    echo "Please update LOCAL_REPO_PATH in run_local.sh to point to your persx repo"
    exit 1
fi

# Load environment from targets/persx.env
export $(cat targets/persx.env | xargs)

# Override model to correct version
export CLAUDE_MODEL=claude-sonnet-4-20250514

# Override for local mode (no GitHub interactions)
unset GH_TOKEN  # Disable GitHub API calls

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}❌ ERROR: ANTHROPIC_API_KEY not set${NC}"
    echo ""
    echo "Set it in your environment or run:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

echo -e "${GREEN}Configuration:${NC}"
echo "  Local repo: $LOCAL_REPO_PATH"
echo "  Model: $CLAUDE_MODEL"
echo "  Max loops: $MAX_LOOPS"
echo "  Token budget: $ANTHROPIC_BUDGET_TOKENS"
echo ""

# Confirm before running
read -p "Ready to run bot locally? Changes will be written to your local repo. (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${GREEN}🚀 Running bot...${NC}"
echo ""

# Run local bot
python app/bot_local.py

echo ""
echo -e "${GREEN}✅ Done!${NC}"
echo ""
echo "Next steps:"
echo "  1. cd $LOCAL_REPO_PATH"
echo "  2. git status"
echo "  3. git diff"
echo "  4. Review changes before committing"
