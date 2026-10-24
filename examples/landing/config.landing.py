# ============================================================
# MimePy — exemplo de LANDING PAGE de negócio fictício
# ============================================================
# Este config gera um site de 1 página (landing) a partir do
# arquivo LANDING.md (Markdown). Modo = "landing".
# Uso: python <mimepy>/src/build.py <caminho>/config.landing.py

PROJECT = {
    "mode": "landing",                 # IMPORTANTE: landing page
    "name": "Café Aurora",
    "brand": "☕",
    "page_title": "Café Aurora — Torrefação Especial",
    "intro": "",

    # Hero (topo da página)
    "hero": {
        "emoji": "☕",
        "tagline": "Cafés especiais de origem, torrados artesanalmente em pequenos lotes.",
        "cta_text": "Ver nosso café",
        "cta_link": "#cafes",
    },
    "meta_description": "Café Aurora — torrefação de café especial artesanal, direto da origem.",

    "docs_dir": ".",                   # LANDING.md fica junto do config (modo landing)
    "out_dir": "out",
    "out_file": "index.html",


    # Home: caminho relativo até a página principal (raiz do site).
    "home_url": "../../../index.html",    "landing_md": "LANDING.md",

    "footer": "Café Aurora · Torrefação Especial · 2026",

    "extensions": ["tables", "fenced_code", "sane_lists", "attr_list", "def_list"],
}
