#!/bin/bash
# Debug script for local bot testing
# Usage:
#   export ANTHROPIC_API_KEY='your-key'
#   export GH_TOKEN='your-token'
#   ./run-bot-debug.sh

set -e

# Check environment variables are set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY not set"
    exit 1
fi

if [ -z "$GH_TOKEN" ]; then
    echo "Error: GH_TOKEN not set"
    exit 1
fi

source .venv/bin/activate
export $(cat targets/persx.env | xargs)

echo "Running bot with full output..."
python app/bot.py
