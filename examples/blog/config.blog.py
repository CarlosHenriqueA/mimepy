# ============================================================
# MimePy — Exemplo de BLOG (mode blog)
# ============================================================
# Cada .md em `blog/` é um post (usamos frontmatter title/description/date).
# Rode:  python src/build.py examples/blog/config.blog.py
PROJECT = {
    "mode": "blog",
    "name": "Blog de Exemplo",
    "brand": "✍️",
    "page_title": "📰 Blog de Exemplo — publicando com MimePy",
    "intro": "Exemplo de blog gerado pelo MimePy a partir de arquivos Markdown, "
             "com postagem via frontmatter (título, descrição e data).",
    "footer": "Blog de Exemplo · MimePy · 2026",
    "lang": "pt-BR",

    "blog_dir": "blog",        # pasta com os posts (.md)
    "docs_dir": "blog",
    "out_dir": "out",
    "out_file": "index.html",

    # Home: na publicação GitHub Pages, o blog vive em /examples/blog/out/,
    # então subir até a home (raiz do site) exige 4 níveis.
    "home_url": "../../../../index.html",

    "extensions": ["tables", "fenced_code", "sane_lists", "attr_list", "def_list"],
}
