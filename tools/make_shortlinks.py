"""Crée des pages de redirection courtes (GitHub Pages) : /v /p /l /j /b /t et /1 à /13 (jours)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = {"v": "vols", "p": "suivi", "l": "logements", "j": "jours", "b": "budget", "t": "todo"}
T.update({str(n): "j%d" % n for n in range(1, 14)})
for k, anchor in T.items():
    os.makedirs(os.path.join(ROOT, k), exist_ok=True)
    open(os.path.join(ROOT, k, "index.html"), "w", encoding="utf-8").write(
        '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>La Réunion</title>'
        '<link rel="canonical" href="../#%s"><meta http-equiv="refresh" content="0;url=../#%s">'
        '<script>location.replace("../#%s")</script><a href="../#%s">La Réunion</a>' % ((anchor,) * 4))
print(len(T), "redirections")
