# ============================================================
# MimePy — exemplo de LANDING de "Recursos do framework"
# ============================================================
# Demonstra o que o MimePy consegue criar em um site de 1 página,
# usando apenas Markdown. Modo = "landing".
# Uso: python <mimepy>/src/build.py <caminho>/config.recursos.py

PROJECT = {
    "mode": "landing",
    "name": "MimePy",
    "brand": "🏗️",
    "page_title": "MimePy — Crie sites a partir de Markdown",
    "intro": "",

    "hero": {
        "emoji": "🏗️",
        "tagline": "Docs e landing pages responsivos a partir de Markdown puro. Sem build complexo.",
        "cta_text": "Ver exemplo de negócio →",
        "cta_link": "../landing/out/index.html",
    },
    "meta_description": "MimePy — transforme Markdown em sites e landing pages responsivos.",

    "docs_dir": ".",                   # RECURSOS.md fica junto do config (modo landing)
    "out_dir": "out",
    "out_file": "index.html",


    # Home: caminho relativo até a página principal (raiz do site).
    "home_url": "../../../index.html",    "landing_md": "RECURSOS.md",

    "footer": "© 2026 MimePy",
    "extensions": ["tables", "fenced_code", "sane_lists", "attr_list", "def_list"],
}
