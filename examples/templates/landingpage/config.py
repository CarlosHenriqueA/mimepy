# MimePy — Template: Página de Vendas (landingpage) de alta conversão
# Copie esta pasta, edite e publique. Rode:
#   python src/build.py examples/templates/landingpage/config.py
#
# Estrutura consagrada de vendas: hero forte → prova social → dor/solução →
# módulos → quem é x não é → potência do autor → depoimentos → garantia →
# oferta/preço → FAQ. Todas as camadas são blocos do motor MimePy (hero, cards,
# tabela, blockquote de depoimento, formulário). O botão de checkout leva à
# página de OBRIGADO (thank-you.html).
PROJECT = {
    "mode": "landing",
    "name": "CursoNome",
    "brand": "🎓",
    "page_title": "Curso [Nome] — Transforme [resultado]",
    "lang": "pt-BR",
    "theme": "dark",

    # Home: caminho relativo até a página principal (raiz do site).
    "home_url": "../../../../index.html",
    "landing_md": "LANDING.md",
    "docs_dir": ".",
    "out_dir": "out",
    "out_file": "index.html",

    "hero": {
        "emoji": "🎓",
        "tagline": "O método passo a passo para você [alcançar resultado] em [prazo] — mesmo que esteja começando do zero.",
        "cta_text": "Quero garantir minha vaga",
        "cta_link": "#oferta",
    },
}
