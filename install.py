#!/usr/bin/env python3
"""Install find-skills. `python install.py` copies the skill into every agent folder that exists
(~/.claude, ~/.agents, ~/.codex, ~/.gemini). Add `--claude-hooks` to also register the Claude Code
hooks (auto-suggest on each prompt + counter line). Safe to re-run."""
import json, shutil, sys
from pathlib import Path

HOME = Path.home()
SRC = Path(__file__).parent / "find-skills"
AGENTS = [".claude", ".agents", ".codex", ".gemini"]

for a in AGENTS:
    if (HOME / a).exists():
        dest = HOME / a / "skills" / "find-skills"
        shutil.copytree(SRC, dest, dirs_exist_ok=True)
        print("installed ->", dest)

if "--claude-hooks" in sys.argv:
    settings = HOME / ".claude" / "settings.json"
    cfg = json.loads(settings.read_text(encoding="utf-8")) if settings.exists() else {}
    script = (HOME / ".claude/skills/find-skills/scripts/find_skills.py").as_posix()
    def entry(mode, matcher=None):
        e = {"hooks": [{"type": "command", "command": f"python {script} {mode}"}]}
        return ({"matcher": matcher, **e} if matcher else e)
    hooks = cfg.setdefault("hooks", {})
    for event, e in (("UserPromptSubmit", entry("suggest")), ("PostToolUse", entry("launched", "Skill")), ("Stop", entry("status"))):
        # drop any previous find-skills entry, then add ours
        hooks[event] = [h for h in hooks.get(event, []) if "find_skills" not in json.dumps(h)] + [e]
    settings.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print("hooks registered in", settings)
