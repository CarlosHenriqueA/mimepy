# Changelog — MimePy

Todas as mudanças notáveis do MimePy. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/) · Versionamento `MAJOR.MINOR.PATCH`.

> Este arquivo é **complementado** por `docs/ROADMAP.md` (visão completa das
> melhorias) e pode ser regenerado/aumentado com `scripts/gen_changelog.py`.

## [v0.3] — 2026-08-05

### Adicionado (ciclo: melhorias M1–M16 + N1–N16)
- **Temas** `paper` e `mono` (além de light/dark/neon) via `THEMES_CSS`/`get_theme_css`.
- **Busca com snippet** (N4): mostra o trecho do conteúdo que casou, com o termo em destaque.
- **prefers-contrast automático** (N5): alto contraste via media query do SO, sem botão.
- **Tema claro/escuro em landing** por config (N6): `theme:"light"` faz a landing nascer clara.
- **CSP** (N10): meta Content-Security-Policy no HTML gerado (endurece script/style/img).
- **rel="noopener noreferrer"** (N11): automático em links externos.
- **CLI** (N3): `mimepy init <nome>` e `mimepy build` — cria projeto e gera HTML.
- **Testes pytest** (N12): suíte `tests/` (build+security+temas).
- **Ícones na sidebar** (N18): emojis dos títulos viram badges `.side-ic`.
- **Documentação técnica** `docs/TECNICO.md` (arquitetura, funções, config, segurança).
- **4 templates de landing** (startup, produto, evento, docs).
- **Toolbar à direita** + **badge no brand** + **TOC sticky** + **atalho `/`**.

### Corrigido
- XSS no highlighter (escapamento `& < >` antes do `innerHTML`).
- `_cardize` extrai badge de forma robusta (evita `/`, `%`, números).
- Grid de cards otimizado (máx. 3 colunas, sem vaga vazia).
- Toolbar movida para a direita (sem sobreposição do menu).
- Escape duplo `&amp;amp;` nos títulos da navbar.

### Segurança
- Sanitização `sanitize:true` para Markdown de terceiros.
- Bloqueio de `javascript:`/`data:` em CTAs.
- Zero dados sensíveis do autor nos saídas.

## [v0.2] — (anterior)
- Modo landing premium (navbar fixa, hero gradiente, cards) · busca no conteúdo ·
  dark automático · highlight offline · logo configurável · âncoras § · TOC recolhível.

## [v0.1] — (inicial)
- Base do framework: docs (mode docs) com sidebar, busca, dark, prev/next, copiar, print.
