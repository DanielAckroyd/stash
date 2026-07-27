#!/usr/bin/env python3
"""Custom Claude Code status line.
Shows: 5h & 7d usage %, model + thinking/effort, shortened cwd, git branch.
Must never crash — always print a line."""
import sys, os, json, subprocess, time

# --- ANSI helpers ---------------------------------------------------------
def c(code): return f"\033[{code}m"
RESET = c(0); DIM = c(2); BOLD = c(1)
CYAN = c("38;5;44"); MAGENTA = c("38;5;176"); BLUE = c("38;5;75")
GREEN = c("38;5;42"); YELLOW = c("38;5;179"); RED = c("38;5;203")
GREY = c("38;5;245")

def usage_color(p):
    try: p = float(p)
    except (TypeError, ValueError): return GREY
    if p >= 80: return RED
    if p >= 50: return YELLOW
    return GREEN

def fmt_tokens(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return str(n)
    if n >= 1_000_000:
        v = n / 1_000_000
        return (f"{v:.1f}".rstrip("0").rstrip(".")) + "M"
    if n >= 1_000:
        return f"{round(n / 1000)}k"
    return str(n)

def shorten_path(path):
    home = os.path.expanduser("~")
    if path == home:
        return "~"
    if path == "/":
        return "/"
    if path.startswith(home + os.sep):
        path = "~" + os.sep + path[len(home) + 1:]
    parts = path.split(os.sep)
    out = []
    for i, seg in enumerate(parts):
        if i == len(parts) - 1 or seg in ("", "~"):
            out.append(seg)          # keep last segment (and ~ / leading root) full
        else:
            out.append(seg[0])       # abbreviate intermediate segments
    return os.sep.join(out)

def git_branch(cwd):
    try:
        b = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=0.5,
        )
        if b.returncode != 0:
            return None
        branch = b.stdout.strip()
        if branch == "HEAD":  # detached — show short sha instead
            sha = subprocess.run(
                ["git", "-C", cwd, "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=0.5,
            )
            return sha.stdout.strip() or None
        return branch or None
    except Exception:
        return None

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    segs = []

    # 1. Model + thinking / effort
    model = (data.get("model") or {}).get("display_name") or "?"
    think = data.get("thinking") or {}
    effort = (data.get("effort") or {}).get("level")
    if think.get("enabled"):
        tag = f"thinking:{effort}" if effort else "thinking"
    elif effort:
        tag = effort
    else:
        tag = "no-think"
    fast = "⚡" if data.get("fast_mode") else ""
    segs.append(f"{CYAN}{BOLD}{model}{RESET}{fast} {MAGENTA}{tag}{RESET}")

    # 2. Context window token count
    cw = data.get("context_window") or {}
    ctx_tokens = cw.get("total_input_tokens")
    if ctx_tokens is not None:
        col = usage_color(cw.get("used_percentage"))
        tok = fmt_tokens(ctx_tokens)
        size = cw.get("context_window_size")
        cap = f"/{fmt_tokens(size)}" if size else ""
        pct = cw.get("used_percentage")
        pct_str = f" {col}{round(float(pct))}%{RESET}" if pct is not None else ""
        segs.append(f"{GREY}ctx{RESET} {col}{tok}{RESET}{GREY}{cap}{RESET}{pct_str}")

    # 3. Usage: 5h + 7d
    rl = data.get("rate_limits") or {}
    def fmt_countdown(resets_at):
        try:
            secs = int(resets_at) - int(time.time())
        except (TypeError, ValueError):
            return None
        if secs <= 0:
            return None
        h, m = secs // 3600, (secs % 3600) // 60
        if h:
            return f"{h}h{m:02d}m"
        if m:
            return f"{m}m"
        return "<1m"
    def usage_seg(label, key, show_reset=False):
        w = rl.get(key) or {}
        p = w.get("used_percentage")
        if p is None:
            return None
        col = usage_color(p)
        try:
            pv = round(float(p))
        except (TypeError, ValueError):
            pv = p
        seg = f"{GREY}{label}{RESET} {col}{pv}%{RESET}"
        if show_reset:
            cd = fmt_countdown(w.get("resets_at"))
            if cd:
                seg += f" {DIM}↻{cd}{RESET}"
        return seg
    u5 = usage_seg("5h", "five_hour", show_reset=True)
    u7 = usage_seg("7d", "seven_day")
    usage = " ".join(x for x in (u5, u7) if x)
    if usage:
        segs.append(usage)

    # 4. Shortened directory
    cwd = (data.get("workspace") or {}).get("current_dir") or data.get("cwd") or ""
    if cwd:
        segs.append(f"{BLUE}{shorten_path(cwd)}{RESET}")

    # 5. Git branch
    br = git_branch(cwd) if cwd else None
    if br:
        segs.append(f"{GREEN}⎇ {br}{RESET}")

    sep = f" {DIM}│{RESET} "
    sys.stdout.write(sep.join(segs))

if __name__ == "__main__":
    main()
