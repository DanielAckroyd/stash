#!/bin/sh
# Copy the tracked config files from this repo into $HOME.
# Existing files are backed up with a .bak suffix.
set -eu
cd "$(dirname "$0")"

git ls-files | grep -v -e '^README.md$' -e '^sync.sh$' -e '^restore.sh$' | while read -r f; do
  mkdir -p "$HOME/$(dirname "$f")"
  if [ -f "$HOME/$f" ] && ! cmp -s "$f" "$HOME/$f"; then
    cp "$HOME/$f" "$HOME/$f.bak"
    echo "backed up: ~/$f -> ~/$f.bak"
  fi
  cp "$f" "$HOME/$f"
  echo "restored: ~/$f"
done
