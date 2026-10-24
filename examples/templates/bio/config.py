# MimePy — Template: Bio (link-in-bio estilo Linktree / bio.site)
# Copie esta pasta, edite e publique. Rode:
#   python src/build.py examples/templates/bio/config.py
#
# Bio = página de perfil com um link para sua rede (o link que você cola no
# Instagram/TikTok/WhatsApp). Replica o padrão Linktree + monetização (card de
# produto/captura de e-mail) + customização de tema — 100% offline e sem conta,
# o diferencial do MimePy frente aos concorrentes.
PROJECT = {
    "mode": "landing",
    "name": "MeuPerfil",
    "brand": "🧞",
    "page_title": "@meuperfil — links e bio",
    "lang": "pt-BR",
    "theme": "dark",

    # Home: caminho relativo até a página principal (raiz do site).
    "home_url": "../../../../index.html",
    "landing_md": "LANDING.md",

    "docs_dir": ".",
    "out_dir": "out",
    "out_file": "index.html",

    "hero": {
        "emoji": "🧞",
        "tagline": "@meuperfil · Criador de conteúdo · [sua mini-bio persuasiva aqui]",
        "cta_text": "Meus links",
        "cta_link": "#secoes",
    },
}
