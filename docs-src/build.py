#!/usr/bin/env python3
"""Génère docs/<nom>.pdf à partir de docs-src/<nom>.html (fragment) avec Chrome headless.
Usage : python3 docs-src/build.py [nom ...]   (sans argument : tous les fragments)"""
import pathlib, subprocess, sys, tempfile, shutil

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent / "docs"
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")

HEAD = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans+Condensed:wght@600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}"></head><body>
"""
FOOT = """<footer class="doc">Constant Segrétain · BTS SIO SISR · constantsegretain@gmail.com</footer></body></html>"""

def build(frag: pathlib.Path):
    body = frag.read_text(encoding="utf-8")
    title = body.split("<h1>", 1)[1].split("</h1>", 1)[0] if "<h1>" in body else frag.stem
    html = HEAD.format(title=title, css=(SRC / "doc.css").as_uri()) + body.replace('src="img/', f'src="{(SRC / "img").as_uri()}/') + FOOT
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(html)
    out = OUT / f"{frag.stem}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={out}", pathlib.Path(t.name).as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pathlib.Path(t.name).unlink()
    print("ok", out.name)

names = sys.argv[1:]
frags = [SRC / f"{n}.html" for n in names] if names else sorted(p for p in SRC.glob("*.html"))
for f in frags:
    build(f)
