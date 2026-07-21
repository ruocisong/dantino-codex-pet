#!/usr/bin/env bash
set -euo pipefail

CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
DEST="$CODEX_ROOT/pets/dantino"

if [[ -d "$DEST" ]]; then
  rm -rf "$DEST"
  printf 'Removed Dantino from %s\n' "$DEST"
else
  printf 'Dantino is not installed at %s\n' "$DEST"
fi
