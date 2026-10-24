# MimePy — Template: Contato (formulário de captura de leads)
# Copie esta pasta, edite e publique. Rode:
#   python src/build.py examples/templates/contato/config.py
#
# Foco: landing page LIMPA e otimizada para captura de contatos/mensagens.
# O formulário é criado com um bloco de código ```form ... ``` no LANDING.md —
# o MimePy o transforma em um <form> real (offline: abre o app de e-mail).
PROJECT = {
    "mode": "landing",
    "name": "NomeDoContato",
    "brand": "📬",
    "page_title": "Fale conosco — NomeDoContato",
    "lang": "pt-BR",
    "theme": "dark",
    "docs_dir": ".",
    "out_dir": "out",
    "out_file": "index.html",

    # Home: caminho relativo até a página principal (raiz do site).
    "home_url": "../../../../index.html",
    "landing_md": "LANDING.md",

    "hero": {
        "emoji": "📬",
        "tagline": "Fale com a gente. Resposta rápida, sem burocracia.",
        "cta_text": "Enviar mensagem",
        "cta_link": "#contato",
    },
}