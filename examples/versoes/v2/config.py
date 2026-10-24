# ============================================================
# MimePy — Exemplo de MULTI-VERSÃO de docs (v2 / preview)
# ============================================================
# Mesmo Markdown do v1, mas para a versão 2 (ex.: em desenvolvimento).
# Só muda: page_title/subtitle e out_dir -> out_v2.
#   python src/build.py examples/versoes/v2/config.py  -> out_v2/index.html
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DOCS = os.path.join(os.path.dirname(_HERE), "docs_versao")

PROJECT = {
    "mode": "docs",
    "name": "Meu Produto",
    "brand": "📦",
    "page_title": "📚 Meu Produto — Documentação (v2)",
    "subtitle": "Versão 2.x — em desenvolvimento (preview)",
    "intro": "Documentação v2 do produto. Inclui os recursos novos planejados.",
    "lang": "pt-BR",
    "year": 2026,

    # Só-Markdown: mesmos .md, mas gera na pasta v2
    "docs_dir": _DOCS,
    "out_dir": os.path.join(_HERE, "..", "out_v2"),
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