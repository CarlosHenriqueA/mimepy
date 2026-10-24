# Changelog — MimePy

Todas as mudanças notáveis do MimePy. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/) · Versionamento `MAJOR.MINOR.PATCH`.

> Este arquivo é **complementado** por `docs/ROADMAP.md` (visão completa das
> melhorias) e pode ser regenerado/aumentado com `scripts/gen_changelog.py`.

## [v0.5] — 2026-10-24

### Adicionado (ciclo de templates + exemplos)
- **Templates aprimorados**: `startup` (sobre, valores, equipe, métricas, depoimentos,
  CTA), `produto` (destaques, comparativo em tabela, depoimentos, planos, garantia) e
  `evento` (agenda, 5 palestrantes, localização, ingressos, FAQ) — agora com dados de
  demonstração realistas e todas as camadas que o motor renderiza.
- **Template `blog`** movido para o módulo de templates (`examples/templates/blog/`),
  padronizado com os demais.
- **Template `bio`** (link-in-bio estilo Linktree/bio.site): perfil, botões de link,
  card de produto, mídia, newsletter; publicamos a pesquisa prévia obrigatória em
    `examples/templates/bio/PESQUISA_CONCORRENTES.md` (Linktree, Beacons, Bio.site, Taplink, Lnk.bio, Carrd).
- **Template `landingpage`** de alta conversão: hero, prova social, dor/solução,
  módulos, quem-é/não-é, bio do autor, depoimentos, garantia, oferta/preço e FAQ +
  **página conectada `thank-you.html`** (fluxo venda → confirmação).
- **Página conectada** no motor: `build_landing` copia um `thank-you.html` que exista na
  pasta do config para a saída; `deploy_pages.py` também o publica no `_site`.
- **Home** atualizada com acesso direto a todos os templates/exemplos (15 links OK).

### Aprimorado (ciclo v0.5 — contraste/a11y)
- **Contraste no modo claro** da landing: textos base em quase-preto (#111827/#1f2937),
  links em esmeralda-escura AA (#0d9488) e navbar em texto escuro — antes usavam as
  cores claras do tema escuro (esmeralda-clara/cinza), ilegíveis sobre fundo branco.
- **Contraste nos temas claros das docs** (light/paper/mono): `--fg` e `--muted`
  escurecidos (ex.: `--muted #64748b` → `#374151`) para legibilidade AA mesmo em
  textos secundários.
- Modo escuro mantém letras claras (inalterado).

## [v0.4] — 2026-10-23

### Adicionado (ciclo de reformulação: motor + segurança + testes)
- **Motor modular**: `src/build.py` virou orquestrador; lógica extraída para
  `src/render.py` (Markdown+frontmatter), `src/security.py` (sanitizador),
  `src/themes.py` (temas). Compat total (nomes públicos preservados).
- **Refactor total de landing/blog**: `build_landing()`, `build_blog()`,
  `_cardize()` e `LANDING_CSS` movidos para `src/modes.py`; `src/_meta.py` é a
  fonte única de `VERSION`. `build.py` agora tem ~536 linhas (era ~1040).
- **Sanitizador por parser real** (`html.parser`, stdlib — sem nova dependência):
  remove `<script>/<style>/<iframe>/<object>/<form>/<input>/<svg>` etc.,
  atributos `on*`, `javascript:`/`data:`/`vbscript:`/`file:`, `style` com
  `url(...)`/`@import`. Preserva links seguros, âncoras, tables e código.
- **45 testes** pytest (era 12): +21 vetores XSS, CLI, temas, modo blog.
- **Polish de UI** preservando identidade: `text-wrap: pretty/balance` em
  docs/landing (melhor ritmo tipográfico sem trocar a paleta esmeralda/âmbar).

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
