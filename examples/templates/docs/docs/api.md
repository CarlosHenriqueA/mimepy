# API

Todas as funções e parâmetros principais.

## `build.py`

| Função | Descrição |
|---|---|
| `load_config(path)` | Carrega `PROJECT` de um `config.py` |
| `build(cfg, base_dir)` | Monta a página de **docs** (mode docs) |
| `build_landing(cfg, base_dir)` | Monta a **landing** (mode landing) |
| `build_blog(cfg, base_dir)` | Monta o **blog** (mode blog) |

## `render_md(path, extensions)`

Converte Markdown → `(html, meta)`, onde `meta` traz o frontmatter.

## `security.sanitize_html(html)`

Sanitiza HTML bruto removendo vetores XSS (opcional via `sanitize: true`).

> Veja `docs/TECNICO.md` do framework para a referência completa.