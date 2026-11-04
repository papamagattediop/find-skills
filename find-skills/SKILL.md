---
name: find-skills
description: Finds which installed skill best fits the user's request and tells you to use it. Use at the start of every task or new user prompt, when the user asks which skill to use, or when unsure whether a specialised skill exists for the job (documents, design, code review, research, testing, video, security...).
license: MIT
compatibility: Needs Python 3. Works in any agent that reads SKILL.md (Claude Code, Codex, Gemini CLI, Cursor, Copilot). Automatic per-prompt mode needs Claude Code hooks.
---

# find-skills

At the start of each task, run the matcher on the user's request:

```
python scripts/find_skills.py match "<the user's prompt>"
```

(path relative to this skill's folder). It prints up to 3 installed skill names, best first.

- If one clearly fits, invoke it before doing the work.
- If it prints `(none)`, continue normally. Do not invent a skill.
- Do not run it twice for the same prompt.

In Claude Code the installer can also register hooks so this happens automatically on every prompt,
and a line `find-skills | this prompt: N suggested, M launched | session: X / Y` (in your system language) is shown after each reply.
