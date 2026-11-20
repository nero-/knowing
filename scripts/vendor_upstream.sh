#!/usr/bin/env bash
# Recreate the pristine upstream reference copy used for diffing translations.
# vendor/ is gitignored on purpose: it is a working aid, not part of the fork.
set -euo pipefail
SHA=e2337975f6b3845b4067d65462f7953cd3d13e46
DEST="$(cd "$(dirname "$0")/.." && pwd)/vendor/deepdive"
mkdir -p "$(dirname "$DEST")"
if [ ! -d "$DEST/.git" ]; then
  git clone --quiet https://github.com/Socialpranker/deepdive "$DEST"
fi
git -C "$DEST" fetch --quiet origin
git -C "$DEST" checkout --quiet "$SHA"
echo "vendor/deepdive @ $SHA"
echo "diff a translated file:  diff -u vendor/deepdive/<path> <path>"
