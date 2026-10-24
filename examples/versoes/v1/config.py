# ============================================================
# MimePy — Exemplo de MULTI-VERSÃO de docs (/v1/, /v2/)
# ============================================================
# Como funciona: o MimePy gera UM HTML por execução do build, e o
# `out_dir`/`out_file` determinam ONDE o HTML sai. Assim, para ter
# docs em múltiplas versões (/v1/, /v2/...), basta rodar o build
# com configs diferentes — cada um apontando para uma pasta própria.
#
#   python src/build.py examples/versoes/v1/config.py  -> out_v1/index.html
#   python src/build.py examples/versoes/v2/config.py  -> out_v2/index.html
#
# Ambos partem SOMENTE de Markdown (docs/ compartilhadas) — a versão
# é só uma questão de config + out_dir, sem nenhuma dependência nova.
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DOCS = os.path.join(os.path.dirname(_HERE), "docs_versao")  # Markdown compartilhado

PROJECT = {
    "mode": "docs",
    "name": "Meu Produto",
    "brand": "📦",
    "page_title": "📚 Meu Produto — Documentação (v1)",
    "subtitle": "Versão 1.x — estável",
    "intro": "Documentação v1 do produto. Esta versão é a linha estável/atual.",
    "lang": "pt-BR",
    "year": 2026,

    # Só-Markdown: aponta para a mesma pasta de .md, mas gera na pasta v1
    "docs_dir": _DOCS,
    "out_dir": os.path.join(_HERE, "..", "out_v1"),
    "out_file": "index.html",

    "extensions": ["tables", "fenced_code", "sane_lists", "md_in_html",
                   "attr_list", "def_list", "toc"],

    "features": {"search": True, "dark": True, "prev_next": True,
                 "copy": True, "back_top": True},

    "sidebar": [
        ("README.md", "🚀 Visão geral"),
        ("instalacao.md", "🔧 Instalação"),
    ],
}