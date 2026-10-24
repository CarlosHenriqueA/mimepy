# MimePy — Template: MeuProjeto (modo docs)
# Copie esta pasta, edite e publique. Rode:
#   python src/build.py examples/templates/docs/config.py
#
# Este é um exemplo REAL de MODO DOCS: barra lateral esquerda com os itens
# (definidos em `sidebar`) e o conteúdo de cada item no lado direito.
# Ao clicar num item da barra, o navegador rola até a seção correspondente
# na MESMA página — igual à documentação principal do framework.
PROJECT = {
    "mode": "docs",
    "name": "MeuProjeto",
    "brand": "📚",
    "page_title": "MeuProjeto — Documentação de exemplo",
    "subtitle": "Um exemplo de modo docs com barra lateral e conteúdo à direita",
    "intro": ("Template de documentação no modo `docs`: barra lateral esquerda "
              "com os itens, conteúdo no lado direito. É o mesmo layout da "
              "documentação principal do MimePy."),
    "lang": "pt-BR",
    "theme": "dark",
    "docs_dir": "docs",
    "out_dir": "out",
    "out_file": "index.html",

    # Home: caminho relativo até a página principal (raiz do site).
    "home_url": "../../../../index.html",

    "extensions": ["tables", "fenced_code", "sane_lists", "md_in_html",
                   "attr_list", "def_list", "toc"],

    "features": {"search": True, "dark": True, "prev_next": True,
                 "copy": True, "back_top": True},

    # Barra lateral (modo docs): (arquivo, título do item).
    "sidebar": [
        ("instalacao.md",       "🔧 Instalação"),
        ("primeiros-passos.md", "🚀 Primeiros passos"),
        ("conceitos.md",        "💡 Conceitos"),
        ("exemplos.md",         "🧪 Exemplos"),
        ("api.md",              "🧩 API"),
        ("configuracao.md",     "⚙️ Configuração"),
    ],
}
