#!/bin/sh
# Copy the tracked config files from $HOME into this repo.
set -eu
cd "$(dirname "$0")"

git ls-files | grep -v -e '^README.md$' -e '^sync.sh$' -e '^restore.sh$' | while read -r f; do
  if [ -f "$HOME/$f" ]; then
    cp "$HOME/$f" "$f"
  else
    echo "missing in \$HOME: $f" >&2
  fi
done

git status --short
