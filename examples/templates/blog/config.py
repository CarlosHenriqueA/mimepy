# MimePy — Template: NomeDoBlog (mode blog)
# Copie esta pasta, edite e publique. Rode:
#   python src/build.py examples/templates/blog/config.py
#
# O blog faz parte do ecossistema de templates: cada `.md` em `blog/` é um post
# (frontmatter: title / description / date). A lista sai ordenada do mais
# recente ao mais antigo. Mantém offline / 1 arquivo.
PROJECT = {
    "mode": "blog",
    "name": "NomeDoBlog",
    "brand": "✍️",
    "page_title": "📰 NomeDoBlog — publicando com MimePy",
    "intro": "Exemplo de blog gerado pelo MimePy a partir de arquivos Markdown, "
             "com postagem via frontmatter (título, descrição e data).",
    "footer": "NomeDoBlog · MimePy · GPL-2.0",
    "lang": "pt-BR",
    "theme": "dark",

    # Home: caminho relativo até a página principal (raiz do site).
    "home_url": "../../../../index.html",

    "blog_dir": "blog",     # pasta com os posts (.md)
    "docs_dir": "blog",
    "out_dir": "out",
    "out_file": "index.html",

    "extensions": ["tables", "fenced_code", "sane_lists", "attr_list", "def_list"],
}
