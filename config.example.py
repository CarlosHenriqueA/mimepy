# ============================================================
# MimePy — config.example.py (modelo de configuração)
# ============================================================
# Use como modelo. Copie para 'config.py' (ou aponte o build para
# este caminho) e adapte por projeto.
#
# Dois modos:
#   "docs"    -> documentação multi-página (sidebar + TOC)
#   "landing" -> site de 1 página premium (hero + seções + cards) a partir de 1 .md
# Omita "mode" -> assume "docs".

PROJECT = {
    # Segurança: ative se o Markdown NÃO for 100% confiável (remove <script>,
    # on* e javascript: do conteúdo). Ver docs/SEGURANCA.md.
    # "sanitize": True,
    # ---- Identidade ----
    "name": "MeuProjeto",
    "brand": "⚖️",
    "subtitle": "Descrição curta do projeto",
    "lang": "pt-BR",

    # Logo opcional (imagem) — se definido, substitui o "brand" no topo:
    # "logo": "assets/logo.png",

    # ---- Modo ----
    # "mode": "landing",   # descomente para gerar landing page

    # ---- Tema (M8/N6) ----
    # "theme": "neon",     # "light" (padrão) | "dark" | "neon" | "paper" | "mono".
    #                      # N6: no modo landing, "theme":"light" faz a landing nascer clara
    #                      # (botão 🌙 alterna p/ escuro); padrão é escura.

    # ---- Cabeçalho / textos ----
    "page_title": "📚 Documentação — MeuProjeto",
    "intro": "Bem-vindo à documentação. Use a barra lateral para navegar.",
    "footer": "MeuProjeto · 2026",
    "meta_description": "Descrição curta p/ SEO e compartilhamento.",

    # (somente no modo landing) — hero do topo da página
    # "hero": {
    #     "emoji": "🚀",
    #     "tagline": "Uma manchete cativante para o seu produto.",
    #     "cta_text": "Começar",
    #     "cta_link": "#secoes",
    # },
    # (somente no modo landing) — arquivo .md de uma página.
    # Use `#` p/ título (hero), `##` p/ seções e `###` p/ itens que viram CARDS.
    # "landing_md": "LANDING.md",

    # ---- Diretórios ----
    "docs_dir": "docs",   # onde estão os .md (modo docs)
    "out_dir": ".",       # onde grava (padrão: raiz)
    "out_file": "index.html",

    # ---- Recursos (features) ----
    # "features": {
    #   "search": True, "dark": True, "prev_next": True, "copy": True,
    #   "back_top": True, "print": True, "share": True, "lang": True,
    # }

    # ---- Extensões python-markdown (opcional) ----
    "extensions": [
        "tables", "fenced_code", "sane_lists", "md_in_html",
        "attr_list", "def_list", "toc",
    ],

    # ---- Recursos (modo docs) ----
    # Todos default ON. Coloque False para desligar.
    "features": {
        "search": True,     # busca na sidebar
        "dark": True,       # toggle claro/escuro (persiste no navegador)
        "prev_next": True,  # navegação anterior/próximo
        "copy": True,       # botão 'copiar' nos blocos de código
        "back_top": True,   # botão voltar ao topo
        "print": True,      # estilos de impressão (Ctrl+P → PDF bom)
    },

    # ---- Sidebar (modo docs): ordem de renderização ----
    # ("arquivo.md", "Título no menu"). Só os listados são renderizados.
    "sidebar": [
        ("README.md", "Visão geral"),
        ("01_INTRO.md", "Introdução"),
        ("02_GUIA.md", "Guia técnico"),
    ],
}
