# find-skills

A portable [Agent Skill](https://agentskills.io/specification) that matches each prompt to your installed
skills and tells the agent which one to use. Works with any tool that reads `SKILL.md`
(Claude Code, Codex, Gemini CLI, Cursor, Copilot).

## Install

```bash
python install.py                 # copies the skill into ~/.claude, ~/.agents, ~/.codex, ~/.gemini (those that exist)
python install.py --claude-hooks  # + Claude Code hooks: automatic on every prompt, with a counter line
```

Needs Python 3, no dependencies.

## What you get

- **Any agent:** the skill's description makes the agent call `scripts/find_skills.py match "<prompt>"` at the start of a task.
- **Claude Code with hooks:** automatic on every prompt, and after each reply a line such as
  `find-skills | ce prompt : 2 propose(s), 1 lance(s) | session : 14 / 6`
  (proposed / launched; launched = the Skill tool was actually called).

## Try it

```bash
python find-skills/scripts/find_skills.py match "create a landing page"
```

## Limits

- Keyword matching with a small French→English hint table. Not semantic search.
- Hooks exist only in Claude Code. Other agents rely on the skill description, so triggering is not guaranteed.
- The "launched" counter works only where a hook can see skill calls (Claude Code).
- State is kept in `~/.find-skills/state.json` (last 20 sessions).

## License

MIT
