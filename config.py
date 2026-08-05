# ============================================================
# MimePy — CONFIG ativa (este é o config.py lido pelo build)
# ============================================================
# Para usar em outro projeto: copie esta pasta (ou o src/build.py +
# src/assets/) e ajuste este arquivo. Nada mais muda.

PROJECT = {
    # Identidade
    "name": "MimePy",
    "brand": "🏗️",
    "subtitle": "Framework de Documentação de Projetos",
    "lang": "pt-BR",
    "year": 2026,

    # Cabeçalho
    "page_title": "📚 MimePy — Documentação do Framework",
    "intro": (
        "Framework próprio para gerar documentação de projetos em HTML "
        "bonita (estilo GitBook), responsiva (computador e celular), "
        "a partir de arquivos Markdown."
    ),
    "footer": "MimePy · Framework de Documentação · 2026",
    "meta_description": "MimePy — framework de documentação de projetos em Markdown para HTML bonito e responsivo.",

    # Diretórios
    "docs_dir": "docs",
    "out_dir": ".",
    "out_file": "index.html",

    # Extensões python-markdown (opcional)
    "extensions": ["tables", "fenced_code", "sane_lists", "md_in_html",
                   "attr_list", "def_list", "toc"],

    # Recursos (v0.2) — todos com default ON; desligue pondo False
    "features": {
        "search": True,      # busca na sidebar
        "dark": True,        # toggle claro/escuro
        "prev_next": True,   # navegação anterior/próximo
        "copy": True,        # botão copiar nos blocos de código
        "back_top": True,    # botão voltar ao topo
        "print": True,       # estilos de impressão (Ctrl+P → PDF bom)
    },

    # Sidebar (ordem de renderização)
    "sidebar": [
        ("README.md", "O que é & como usar"),
        ("TUTORIAL.md", "Tutorial passo a passo"),
        ("TECNICO.md", "Documentação técnica"),
        ("REGRAS_DE_ESTILO.md", "Regras de estilo"),
        ("SEGURANCA.md", "Segurança"),
    ("ACESSIBILIDADE.md", "Acessibilidade"),
    ("ROADMAP.md", "Roadmap & futuras melhorias"),
    ("MELHORIAS_FUTURAS.md", "Novas melhorias ideadas"),
    ],
}
