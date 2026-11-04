"""Accuracy check: expected skill must be in the top 3 (cases whose skill isn't installed are skipped).
Run: python eval_matching.py"""
import importlib.util, sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("fs", Path(__file__).parent / "find-skills/scripts/find_skills.py")
fs = importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)

CASES = [  # (prompt, expected skill, "" = nothing should match)
    ("extrais le tableau de ce PDF", "pdf"),
    ("fais moi un powerpoint de 10 slides", "pptx"),
    ("create a landing page for my portfolio", "design-taste-frontend"),
    ("audit this code for technical debt", "ponytail-debt"),
    ("comment est structuré ce projet", "graphify"),
    ("il y a un bug, ça plante au démarrage", "debugging-and-error-recovery"),
    ("fais une affiche pour mon évènement", "canvas-design"),
    ("analyse ce fichier excel", "xlsx"),
    ("rédige un document word", "docx"),
    ("mon site est lent", "performance-optimization"),
    ("fais une vidéo de lancement de mon projet", "brag"),
    ("revue de code avant de fusionner", "code-review-and-quality"),
    ("écris des tests pour cette fonction", "test-driven-development"),
    ("améliore l'animation de ce bouton", "emil-design-eng"),
    ("bonjour, ça va ?", ""),
    ("merci beaucoup", ""),
]
skills = fs.load_skills()
ok = tot = 0
for prompt, want in CASES:
    hits = fs.match(prompt, skills)
    if want and not any(want == h.split(":")[-1] for h in skills):
        print("SKIP", want); continue
    tot += 1
    good = (not hits) if not want else any(want == h.split(":")[-1] for h in hits)
    ok += good
    print("OK  " if good else "FAIL", prompt, "->", hits, "(want:", want or "none", ")")
print(f"{ok}/{tot}")
sys.exit(ok != tot)
