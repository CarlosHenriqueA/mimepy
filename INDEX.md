# 🔑 MimePy — INDEX (guia para o Hermes / quem for usar)

> **Leia este arquivo para "acionar" o framework.** Ele diz exatamente o que o Hermes precisa saber para trabalhar em cima do MimePy.

## O que é
Framework **próprio e reutilizável** que gera a partir de Markdown: **documentação** (HTML responsiva, estilo GitBook) **e landing pages** (site de 1 página).

> **Versão 0.2** — docs (busca, dark mode, prev/next, copiar, print) **+ modo landing page premium** (navbar fixa com blur, hero com gradiente, cards animados). Licença: **GPL-2.0**.

## Dois modos
- `"mode": "docs"` (padrão) → multi-seção com sidebar + TOC.
- `"mode": "landing"` → site de 1 página (hero + seções) a partir de 1 `.md` (`landing_md`). Hero via `"hero": {emoji, tagline, cta_text, cta_link}`.

## Como o Hermes deve usá-lo (workflow padrão)

1. **Localizar a pasta** → `$MIMEPY` (onde você clonou/extraiu o MimePy)
2. **Identificar o projeto alvo** → o usuário diz qual projeto documentar, ou qual landing criar.
3. **Preparar entradas** → colocar/garantir os `.md` (em `docs/` p/ docs, ou `*.md` p/ landing).
4. **Editar `config.py`** → identidade (nome, brand), `mode`, `page_title`/`intro`/`footer`, `hero` (se landing), e `sidebar`/`landing_md`.
5. **Rodar o gerador**:
   ```bash
   cd $MIMEPY        # substitua pelo seu diretório do MimePy
   python src/build.py
   ```
6. **Entregar** → o `index.html` na raiz (ou `out/`). Offline, desktop e celular.

## Estrutura (o que não editar)

| Arquivo | Papel |
|---|---|
| `src/build.py` | **Motor** (docs + landing) — não editar |
| `src/assets/style.css` | Tema (docs + landing CSS) |
| **`DESIGN.md`** | **Design system autoral** (tokens p/ devs e agentes) |
| `config.py` | Config central — edite por projeto |
| `docs/*.md` | Docs do framework |
| `index.html` | Saída gerada |
| `LICENSE` | GPL-2.0 |
| `site/` | Landing oficial p/ GitHub Pages |
| `examples/` | `landing/` (negócio fictício) · `recursos/` (showcase) · `demo/` (reuso fictício) |

## Recursos v0.2
Busca · dark mode · prev/next · copiar código · voltar ao topo · impressão/PDF · **modo landing**.
Ligados por padrão; desligue em `config.py → "features"` (só no modo docs). Config antigo (sem `features`/`mode`) continua funcionando (assume `docs`).

## Regras importantes
- **Uma página única** por build (docs: `sidebar`; landing: um `.md`).
- **`mode`** decide o template (docs vs landing).
- **Responsivo automático** (computador + celular).
- **Dependência única:** `pip install markdown`.
- **Landing:** `LANDING.md` com `#` (título→hero) e `##` (seções); use `docs_dir: "."` quando o `.md` estiver junto do config (senão o caminho duplica — bug já corrigido/evitado).
- **Fidelidade:** usa `python-markdown` (tabelas, código, citações de verdade).

## Configuração rápida

### Modo docs
```python
PROJECT = {
    "name": "MeuProjeto", "brand": "⚖️", "subtitle": "Descrição curta",
    "page_title": "📚 Documentação — MeuProjeto", "intro": "Boas-vindas...",
    "docs_dir": "docs", "out_dir": ".", "out_file": "index.html",
    "sidebar": [("README.md", "Visão geral"), ("02_GUIA.md", "Guia técnico")],
}
```

### Modo landing
```python
PROJECT = {
    "mode": "landing",
    "name": "MeuNegócio", "brand": "🚀",
    "page_title": "MeuNegócio — Site", "landing_md": "LANDING.md",
    "docs_dir": ".", "out_dir": ".", "out_file": "index.html",
    "hero": {"emoji": "🚀", "tagline": "Uma manchete cativante.",
             "cta_text": "Começar", "cta_link": "#secoes"},
}
```

## Roadmap (nuances futuras)
Ver `docs/ROADMAP.md` (highlight, CLI, multi-idioma, GitHub Actions, formulário landing).

---
*Framework validado (docs e landing geram HTML limpo: tags balanceadas, sem markdown cru, viewport + table-scroll + dark + print). Feito com o próprio MimePy.*
