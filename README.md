# stash

Personal config files, mirrored at their home-relative paths.

## Contents

| File | What it is |
|---|---|
| `.zshrc` | zsh + oh-my-zsh setup |
| `.config/starship.toml` | starship prompt |
| `.config/zed/settings.json` | Zed editor settings |
| `.config/gh/config.yml` | GitHub CLI preferences |
| `.claude/CLAUDE.md` | Claude Code global instructions |
| `.claude/settings.json` | Claude Code settings + hooks |
| `.claude/settings.local.json` | Claude Code local permission allowlist |
| `.claude/statusline.py` | Claude Code status line script |
| `.claude/hooks/herdr-agent-state.sh` | Herdr agent-state hook |

## Deliberately excluded

- `~/.config/gh/hosts.yml` — contains the GitHub OAuth token
- `~/.config/zed/prompts/` — binary prompts-library database
- `~/.zsh_history`, caches, session state

## Usage

Pull latest copies from the home directory into the repo:

```sh
./sync.sh
```

Restore onto a new machine (copies repo files into `~`, backing up anything it would overwrite):

```sh
./restore.sh
```
