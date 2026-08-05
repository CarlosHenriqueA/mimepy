# ============================================================
# MimePy — exemplo de uso em OUTRO projeto (demonstração fictícia)
# ============================================================
# Este config constrói um site de exemplo FICTÍCIO ("Solaris Kit"),
# comprovando que o framework é genérico e reutilizável em qualquer
# projeto. Copie este padrão para o seu próprio.
#
# Uso: python <MIMEPY>/src/build.py examples/demo/config.demo.py
# (paths relativos — sem nenhum caminho pessoal)
import os

# Pasta raiz do MimePy = ../.. (a partir do config)
_HERE = os.path.dirname(os.path.abspath(__file__))

PROJECT = {
    "name": "Solaris Kit",
    "brand": "☀️",
    "subtitle": "Kit de componentes para times ágeis — exemplo fictício",
    "lang": "pt-BR",
    "year": 2026,

    "page_title": "☀️ Solaris Kit — Kit de componentes",
    "intro": (
        "Bem-vindo ao Solaris Kit: componentes leves e reutilizáveis para "
        "equipes ágeis. Navegue pelas seções na barra lateral."
    ),
    "footer": "Solaris Kit (fictício) · exemplo de reuso · 2026",

    # Exemplo usa caminhos RELATIVOS (recomendado para portabilidade)
    "docs_dir": os.path.join(_HERE, "docs"),
    "out_dir": os.path.join(_HERE, "out"),
    "out_file": "solaris-kit.html",

    "extensions": ["tables", "fenced_code", "sane_lists", "md_in_html",
                   "attr_list", "def_list", "toc"],

    "sidebar": [
        ("README.md", "Visão geral"),
        ("01_instalacao.md", "Instalação"),
        ("02_componentes.md", "Componentes"),
        ("03_exemplos.md", "Exemplos de uso"),
    ],
}
