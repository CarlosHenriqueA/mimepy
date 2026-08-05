# ============================================================
# MimePy — config da landing oficial do site (GitHub Pages)
# ============================================================
# O site/ usa o PRÓPRIO framework (modo landing) para gerar o
# index.html público. Assim herda de graça: navbar fixa, hero,
# cards, dark mode, tamanho de fonte, alto contraste e o design
# system autoral (esmeralda/teal + âmbar).
# Uso: python src/build.py site/config.site.py
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

PROJECT = {
    "mode": "landing",
    "name": "MimePy",
    "brand": "🏗️",
    "page_title": "MimePy — Framework de Documentação",  # (estilo da URL)
    "intro": "",
    "lang": "pt-BR",
    "year": 2026,

    "hero": {
        "emoji": "🏗️",
        "tagline": "Documentação e landing pages bonitas e responsivas a partir de Markdown puro. Sem build complexo, sem Node, sem dor.",
        "cta_text": "Começar agora",
        "cta_link": "#uso",
    },
    "meta_description": "MimePy: gere documentação de projetos bonita e responsiva a partir de Markdown. HTML autocontido, offline, GPL-2.0.",

    # caminhos relativos (aponta para a própria pasta do site)
    "docs_dir": _HERE,
    "out_dir": _HERE,
    "out_file": "index.html",
    "landing_md": "SITE.md",

    # tema autoral (padrão esmeralda/teal; com dark/neon opcional)
    "theme": "dark",
    "extensions": ["tables", "fenced_code", "sane_lists", "attr_list", "def_list", "toc"],
}
