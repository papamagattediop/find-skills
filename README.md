<div align="center">

# 🔎 find-skills

**The right skill, found for every prompt.**

A portable [Agent Skill](https://agentskills.io/specification) that matches what you ask
to the skills you already have installed — and tells your AI to use them.

[![License: MIT](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![Python 3](https://img.shields.io/badge/python-3-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/standard-SKILL.md-8957e5?style=flat-square)](https://agentskills.io/specification)
[![Dependencies](https://img.shields.io/badge/dependencies-none-lightgrey?style=flat-square)](#)

Claude Code &nbsp;·&nbsp; Codex &nbsp;·&nbsp; Gemini CLI &nbsp;·&nbsp; Cursor

</div>

<br>

## Why

You install dozens of skills, then forget they exist. **find-skills** reads each prompt,
scores it against every installed skill, and points your agent to the best match —
so the right expertise is used without you having to remember its name.

<br>

## How it looks

```text
you     ›  create a landing page for my portfolio

claude  ›  find-skills suggests: design-taste-frontend
           …builds the page using that skill…

find-skills | this prompt: 1 suggested, 1 launched | session: 14 / 6
```

*Suggested* = skills found for the prompt. *Launched* = skills the agent actually called.
The line follows your system language (English, French, Spanish); set `FIND_SKILLS_LANG=fr` to force one.

<br>

## Install

```bash
git clone https://github.com/papamagattediop/find-skills.git
cd find-skills

python install.py                  # skill only (any SKILL.md-compatible agent)
python install.py --claude-hooks   # + automatic mode and counter in Claude Code
```

The installer copies the skill into `~/.claude`, `~/.agents`, `~/.codex` and `~/.gemini`
(whichever exist). No dependencies. Safe to re-run.

<br>

## Try it

```bash
python find-skills/scripts/find_skills.py match "audit this code for technical debt"
# → ponytail-debt
```

<br>

## Works with

| Agent | Skill | Automatic on every prompt | Counter |
| --- | :---: | :---: | :---: |
| Claude Code | ✅ | ✅ via hooks | ✅ |
| Codex · Gemini CLI · Cursor | ✅ | — the agent decides | — |

<br>

## How it works

1. **Index** — reads the name and description of every installed `SKILL.md`.
2. **Match** — scores the prompt by keyword overlap, with a French → English hint table.
3. **Suggest** — hands the top 3 to the agent, which decides whether to use them.

<br>

## Good to know

- Keyword matching, not semantic search: precise on clear requests, imperfect on vague ones.
- Outside Claude Code the skill relies on the agent choosing to call it.
- Check accuracy any time with `python eval_matching.py`.

<br>

## License

[MIT](LICENSE)

<div align="center">
<sub>Built on the open <a href="https://agentskills.io/specification">Agent Skills</a> standard.</sub>
</div>
