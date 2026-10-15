#!/usr/bin/env python3
"""Récupère les dernières alertes du CERT-FR et les écrit dans veille.html.

Le flux RSS du CERT-FR n'autorise pas la lecture depuis un navigateur (pas
d'en-tête CORS) : on le lit ici, côté serveur, et la page reste statique.
Lancé chaque jour par .github/workflows/veille.yml, ou à la main :

    python3 scripts/cert-fr.py
"""
import html
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://www.cert.ssi.gouv.fr/feed/"
PAGE = pathlib.Path(__file__).resolve().parent.parent / "veille.html"
COUNT = 8
MOIS = "janv. févr. mars avr. mai juin juil. août sept. oct. nov. déc.".split()


def kind(link):
    if "/alerte/" in link:
        return "Alerte"
    if "/avis/" in link:
        return "Avis"
    if "/actualite/" in link:
        return "Actualité"
    return "CERT-FR"


def main():
    req = urllib.request.Request(FEED, headers={"User-Agent": "portfolio-veille"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())

    items = []
    for it in root.iter("item"):
        link = it.findtext("link", "").strip()
        title = it.findtext("title", "").strip()
        title = re.sub(r"\s*\(\d{1,2} \w+ \d{4}\)$", "", title)  # la date est déjà affichée
        d = parsedate_to_datetime(it.findtext("pubDate"))
        items.append((d, kind(link), title, link))
    items.sort(reverse=True)

    rows = []
    for d, k, title, link in items[:COUNT]:
        date = f"{d.day} {MOIS[d.month - 1]} {d.year}"
        rows.append(
            f'      <li>\n'
            f'        <a class="row" href="{html.escape(link)}" target="_blank" rel="noopener">\n'
            f'          <span class="year">{date}</span>\n'
            f'          <div><h3>{html.escape(title)}</h3></div>\n'
            f'          <div class="side"><span class="stack">{k}</span></div>\n'
            f'        </a>\n'
            f'      </li>')

    block = ('<!-- cert-fr:start -->\n'
             '    <ul class="projects feed">\n' + "\n".join(rows) + '\n    </ul>\n'
             f'    <p class="section-note">Mis à jour automatiquement chaque jour depuis le flux RSS du CERT-FR.</p>\n'
             '<!-- cert-fr:end -->')

    text = PAGE.read_text(encoding="utf-8")
    new = re.sub(r"<!-- cert-fr:start -->.*?<!-- cert-fr:end -->", lambda _: block, text, flags=re.S)
    if new != text:
        PAGE.write_text(new, encoding="utf-8")
        print(f"{len(rows)} alertes écrites dans {PAGE.name}")
    else:
        print("Aucun changement")


if __name__ == "__main__":
    main()
