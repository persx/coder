#!/bin/bash
# Create GitHub labels for persx/persx repo
# Usage: ./create-labels.sh
# Requires: gh CLI installed and authenticated

set -e

REPO="persx/persx"

echo "Creating labels for $REPO..."
echo ""

# Label 1: bot
gh label create "bot" \
  --repo "$REPO" \
  --description "Automated changes from Claude bot" \
  --color "0e8a16" \
  --force || echo "Label 'bot' already exists"

# Label 2: safe-change
gh label create "safe-change" \
  --repo "$REPO" \
  --description "Low-risk change verified by guardrails" \
  --color "bfdadc" \
  --force || echo "Label 'safe-change' already exists"

# Label 3: needs-human
gh label create "needs-human" \
  --repo "$REPO" \
  --description "Requires human review and decision" \
  --color "fbca04" \
  --force || echo "Label 'needs-human' already exists"

# Label 4: blocked
gh label create "blocked" \
  --repo "$REPO" \
  --description "Bot cannot proceed - manual intervention needed" \
  --color "d93f0b" \
  --force || echo "Label 'blocked' already exists"

echo ""
echo "✅ Labels created! View them at: https://github.com/$REPO/labels"
