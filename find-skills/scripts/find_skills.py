#!/usr/bin/env python3
"""find-skills: match a prompt to installed skills, and count skills proposed / launched.

Modes (first arg):
  suggest   UserPromptSubmit hook (stdin JSON) -> injects "use skill X" context
  launched  PostToolUse hook on the Skill tool  -> counts a launched skill
  status    Stop hook                           -> prints the counter line to the user
  match "<prompt>"   plain CLI for any agent without hooks (Codex, Gemini, Cursor...)
Stdlib only. Never raises inside a hook: a broken helper must not break the session."""
import json, math, re, sys
from pathlib import Path

HOME = Path.home()
ROOTS = [HOME / d / "skills" for d in (".claude", ".codex", ".gemini", ".agents", ".cursor")] + [HOME / ".claude/plugins/cache"]
STATE = HOME / ".find-skills" / "state.json"
STOP = set("the and for with that this from your you are use when user les des une pour dans avec que qui est sur pas plus mon son any all not can has have will".split())
# French -> English hints, because most skill descriptions are in English
SYN = {"tableau": "table spreadsheet", "tableaux": "table spreadsheet", "fichier": "file", "présentation": "presentation slide deck pptx",
       "powerpoint": "pptx presentation slide", "excel": "xlsx spreadsheet", "word": "docx document", "site": "website web",
       "créer": "create build", "crée": "create build", "fais": "create", "bug": "bug debug error", "erreur": "error debug",
       "sécurité": "security", "lent": "performance slow", "affiche": "poster design", "interface": "interface ui frontend",
       "recherche": "research search", "analyse": "analysis analyze", "revue": "review", "dette": "debt", "résume": "summarize summary",
       "résumer": "summarize summary", "projet": "project", "structuré": "structure architecture codebase", "dépôt": "repository codebase", "test": "test testing driven tdd",
       "lancement": "launch promo", "vidéo": "video launch promo", "animation": "animation motion polish", "bouton": "button ui component",
       "améliore": "improve polish", "plante": "crash bug error", "démarrage": "startup", "fusionner": "merge review", "code": "code"}
BUILTIN = {"anthropic-skills:pdf": "pdf extract text tables forms merge split documents",
           "anthropic-skills:docx": "word docx document report letter template",
           "anthropic-skills:xlsx": "excel xlsx spreadsheet csv table formulas data",
           "anthropic-skills:pptx": "powerpoint pptx presentation slides deck"}
MIN_SCORE, TOP = 1.6, 3  # ponytail: keyword overlap; swap for embeddings if recall is poor


def toks(s):
    return {w.rstrip("s") for w in re.findall(r"[a-zà-ÿ0-9]{3,}", s.lower()) if w not in STOP}


def load_skills():
    skills = {}
    for root in ROOTS:
        for f in root.rglob("SKILL.md") if root.exists() else []:
            head = f.read_text(encoding="utf-8", errors="ignore")[:3000]
            n = re.search(r"^name:\s*(.+)$", head, re.M)
            d = re.search(r"^description:\s*(.+)$", head, re.M)
            if n and d:
                name = n.group(1).strip().strip("\"'")
                if name != "find-skills":
                    skills[name] = (toks(name) | toks(d.group(1)), toks(name))
    for name, d in BUILTIN.items():
        skills.setdefault(name, (toks(name) | toks(d), toks(name)))
    return skills


def match(prompt, skills):
    p = toks(prompt)
    for w in list(p):
        p |= toks(SYN.get(w, ""))
    df = {}
    for t, _ in skills.values():
        for w in t:
            df[w] = df.get(w, 0) + 1
    n = len(skills) or 1
    scored = []
    for name, (t, nt) in skills.items():
        s = sum(math.log(n / df[w]) * (2 if w in nt else 1) for w in p & t) / len(t) ** 0.3
        if name.startswith("s4h-"):
            s *= 0.6  # ~190 generic thinking skills would otherwise drown the rest
        if s >= MIN_SCORE:
            scored.append((s, name))
    return [name for _, name in sorted(scored, reverse=True)[:TOP]]


def state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def sess(st, sid):
    if sid not in st and len(st) >= 20:
        st.pop(next(iter(st)))  # keep the file small
    return st.setdefault(sid, {"p": {"s": [], "l": []}, "t": {"s": 0, "l": 0}})


def save(st):
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(st), encoding="utf-8")


def status_line(s):
    p, t = s["p"], s["t"]
    return (f"find-skills | ce prompt : {len(p['s'])} propose(s), {len(p['l'])} lance(s)"
            f" | session : {t['s']} / {t['l']}")


def demo():
    sk = {"pdf": ({"pdf", "extract", "table"}, {"pdf"})}
    sk.update({f"o{i}": ({f"w{i}"}, set()) for i in range(30)})
    assert match("extract table from pdf", sk) == ["pdf"] and match("zzzz", sk) == []
    s = {"p": {"s": ["a", "b"], "l": ["a"]}, "t": {"s": 5, "l": 2}}
    assert "2 propose(s), 1 lance(s)" in status_line(s)


def main():
    demo()
    mode = sys.argv[1] if len(sys.argv) > 1 else "suggest"
    if mode == "match":
        print(", ".join(match(" ".join(sys.argv[2:]), load_skills())) or "(none)")
        return
    data = json.load(sys.stdin)
    st = state()
    s = sess(st, data.get("session_id", "default"))
    if mode == "suggest":
        hits = match(data.get("prompt", ""), load_skills())
        s["p"] = {"s": hits, "l": []}
        s["t"]["s"] += len(hits)
        save(st)
        if hits:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                  "additionalContext": "find-skills: relevant skill(s) for this prompt: " + ", ".join(hits)
                  + ". Invoke the best match with the Skill tool before answering, unless clearly irrelevant."}}))
    elif mode == "launched":
        name = (data.get("tool_input") or {}).get("skill")
        if name:
            s["p"]["l"].append(name)
            s["t"]["l"] += 1
            save(st)
    elif mode == "status":
        print(json.dumps({"systemMessage": status_line(s)}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # never break the session
