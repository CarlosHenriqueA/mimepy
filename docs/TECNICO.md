# 🧑‍💻 MimePy — Documentação Técnica (para dev / IA)

Guia **técnico de referência** de todo o código do MimePy. Se você vai
manter, estender ou integrar o framework, comece aqui. Complementa o
`README.md` (visão de produto) e o `TUTORIAL.md` (uso prático).

> **Nível:** descreve arquitetura, cada função, o config e como adicionar
> recursos com segurança. Requer conhecimento básico de Python/HTML/CSS/JS.

---

## 1. Visão geral da arquitetura

**v0.4 — motor modular.** O `src/build.py` agora é um **orquestrador** que
importa módulos internos especializados (refactor que mantém total compat:

```
Markdown (.md)  ──►  src/build.py (orquestrador)  ──►  HTML autocontido
                      │
                      ├─ src/render.py    → Markdown → HTML + frontmatter
                      ├─ src/security.py  → sanitização HTML (parser real)
                      ├─ src/themes.py    → temas light/dark/neon/paper/mono
                      ├─ src/modes.py     → build_landing() + build_blog() (+ LANDING_CSS)
                      ├─ src/_meta.py     → VERSION (fonte única)
                      ├─ build()          → monta DOCS (mode docs)
                      └─ build.py (main)  → despacha docs/landing/blog

src/assets/style.css   → CSS global (docs): variáveis, a11y, responsivo, dark
src/build.py (APP_JS)  → JS inline (docs): busca, dark, âncoras, TOC, highlight...
src/modes.py (LANDING_CSS) → CSS da landing (navbar, hero, cards, tema claro)
```

O motor tem **zero dependências além de `markdown`** (os módulos internos usam
só a stdlib — `html.parser` no security, por ex.) e gera um **único arquivo
HTML** (CSS+JS embutidos) — por isso é offline e portátil.

> **Nomes públicos preservados:** o `build` (módulo) reexporta `render_md`,
> `get_theme_css`, `THEMES_CSS`, `sanitize_html`, `build_landing`, `build_blog`,
> `_cardize` e `LANDING_CSS` dos módulos, para que código/imports existentes
> continuem funcionando sem alteração. `VERSION` vem de `_meta` (fonte única,
> sem drift entre módulos).

---

## 2. Estrutura de arquivos

| Arquivo | Papel |
|---|---|
| `src/build.py` | O motor: CLI + `load_config`, `render_md`, `sanitize_html`, `build`, `get_theme_css`, `_cardize`, `build_landing`. Contém também `APP_JS` (JS das docs) e `LANDING_CSS` (CSS da landing) como strings. |
| `src/assets/style.css` | CSS global usado pelo modo **docs** (variables, sidebar, main, tabela, pre, dark, responsivo, print, a11y). |
| `config.py` | Config ativo do framework (gera `index.html` dele mesmo). |
| `config.example.py` | Config modelo para outros projetos. |
| `scripts/check_a11y.py` | Valida a11y (estrutura + contraste WCAG via linter do DESIGN.md). |
| `scripts/gen_pdf.py` | Gera PDF do `index.html` via navegador headless ou WeasyPrint. |
| `site/` | Landing oficial (mode landing) — provou o framework em si. |
| `examples/` | `landing/` (Café Aurora, negócio) · `recursos/` (showcase) · `demo/` (reuso fictício). |
| `docs/` | Documentação do framework (que este arquivo integra). |
| `DESIGN.md` | Design system formal (tokens consumíveis por devs/agentes). |

---

## 3. `src/build.py` — funções (API interna)

> **CLI** (`src/cli.py`) também existe: `mimepy init <nome>` / `mimepy build`.
> Ver §9.

### `load_config(config_path) -> dict`
Carrega o `PROJECT` de um arquivo de config via `importlib` (executa o .py).
> ⚠️ **Segurança:** o config é executado como Python. Só carregue configs **de
> sua confiança** (não de terceiros sem revisão).

### `sanitize_html(html) -> str` *(segurança)*
Remove vetores XSS de HTML **bruto** vindo do Markdown (usado só se
`config["sanitize"] == True`):
- tags `<script>`/`<style>` (com conteúdo)
- atributos `on*` (`onclick`, `onerror`, `onload`...)
- prefixos perigosos em href/src (`javascript:`, `data:`)

### `render_md(path, extensions) -> (html, meta)`
Converte um `.md` em HTML com `python-markdown`, retornando **também** os
metadados do frontmatter (N22):
- remove/extrai bloco YAML `--- title/description/order ---` → dict `meta`
- **corrige tabelas**: insere linha em branco antes do separador quando
  necessário (regex robusto — melhor fidelidade ao Markdown)
- usa as extensões do config (`tables`, `fenced_code`, `sane_lists`,
  `md_in_html`, `attr_list`, `def_list`, `toc`)

### `get_theme_css(cfg) -> (css_str, default_theme)`
Retorna o CSS extra do tema configurado e o tema padrão:
- `dark` / `neon` → base escura (alternativos ao light)
- `paper` / `mono` → temas de base própria (claro/mono)
- `light` (padrão) → vazio

### `build(cfg, base_dir)`
Monta a página de **documentação** (mode docs):
1. lê `docs_dir`, monta `sidebar` a partir de `cfg["sidebar"]`
2. renderiza cada doc; aplica `sanitize_html` se habilitado
3. injeta `style.css` + `APP_JS` + script de tema + meta
4. gera nav (com links + busca), conteúdo, prev/next, footer

### `_cardize(block) -> str`
Extrai o **emoji inicial** de um `<h3>` de card e o envolve num `.ic` (badge),
deixando o card com ícone destacado. Só atua se a 1ª palavra for um símbolo
puro (não letras/números) — evita pegar `/`, `%`, `100` etc.

### `build_landing(cfg, base_dir)`
Monta a **landing page** (mode landing) a partir de UM `.md`:
- `<h1>` → título do hero; `<h2>` → seções (navbar + âncoras)
- `<h3>` consecutivos → grade de **cards** (com badge via `_cardize`)
- listas `- **Título**: desc` → viram cards (recuso M5)
- bloco ` ```form ` → formulário de contato (mailto, offline)
- injeta tema (dark/light) + botão de tema na navbar

### `build_blog(cfg, base_dir)`
Monta um **blog** (mode blog) a partir de uma pasta de `.md` (padrão Docusaurus):
- cada `.md` é um post; `frontmatter` (title/description/date) alimenta o card
- ordena por `date` (mais recente primeiro); cada post abre por âncora
- mantém offline/1-arquivo

### Modos disponíveis (`cfg["mode"]`)
- `docs` (padrão) · `landing` · `blog`
- **Sidebar agrupada** (N19): no mode docs, a `sidebar` pode ser
  `[("Grupo", [(arquivo,titulo), ...]), ...]` em vez de lista plana.
- **Modo "texto simples"** (N20): `features:{"highlight":false}` desliga o
  colorização de código (render determinístico, sem spans).

---

## 4. `config.py` — todas as chaves

| Chave | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | str | ✅ | Nome exibido (brand + nav) |
| `brand` | str | ⬜ | Emoji/símbolo do projeto (vira badge) |
| `subtitle` | str | ⬜ | Subtítulo abaixo do brand |
| `lang` | str | ⬜ | `pt-BR`, `en`, ... |
| `page_title` | str | ✅ | Título do `<title>` e h1 do main |
| `intro` | str | ⬜ | Texto de introdução |
| `footer` | str | ⬜ | Rodapé |
| `docs_dir` | str | ✅ | Pasta dos `.md` |
| `out_dir` / `out_file` | str | ✅ | Onde gravar (ex.: `.` / `index.html`) |
| `mode` | str | ⬜ | `docs` (padrão) ou `landing` |
| `landing_md` | str | ⬜ | nome do `.md` único (mode landing) |
| `theme` | str | ⬜ | `light`(padrão)/`dark`/`neon`/`paper`/`mono` |
| `extensions` | list | ⬜ | extensões python-markdown |
| `features` | dict | ⬜ | liga/desliga recursos (default: ON) |
| `hero` | dict | ⬜ | (landing) `emoji`, `tagline`, `cta_text`, `cta_link` |
| `logo` | str | ⬜ | caminho de imagem p/ logo (substitui brand) |
| `sanitize` | bool | ⬜ | liga `sanitize_html` (Markdown não confiável) |

### `features` (todas default `True`)
`search` (busca) · `dark` (toggle tema) · `prev_next` (anterior/próximo) ·
`copy` (copiar código) · `back_top` (voltar ao topo) · `print` (estilo PDF) ·
`share` (compartilhar) · `lang` (toggle pt/en).

---

## 5. Recursos do JS (`APP_JS`) — por seção

O JS das docs é um único `IIFE` com seções numeradas e comentadas:
1. **Busca** — filtra nav por título **e** conteúdo das seções (M4) + **snippet** com
   o trecho que casou em destaque (N4)
1b. **Atalho `/`** — foca a busca (M14)
2. **Dark mode** — alterna `data-theme`, salva em `localStorage` (cicla em neon)
3. **Copiar código** — botão em cada `<pre>` (fallback `execCommand`)
4. **Voltar ao topo** · 4b **Compartilhar** (copia URL)
5. **Scrollspy `aria-current`** — destaca a seção ativa na sidebar (a11y)
6. **Tamanho de fonte** (A/A+/A++) · 6b **Alto contraste** (◐)
6c. **Idioma** (🌐 pt/en)
7. **Highlight de sintaxe** — tokenizador em 1 passada, sem lib (M2)
7b. **`rel=noopener noreferrer`** em links externos (N11)
8. **Âncoras §** + **TOC recolhível** (M6) + **TOC sticky** (M13)

> Detalhe de segurança: o highlight escapa `& < >` antes de injetar em
> `innerHTML` (evita XSS de código não confiável).

---

## 6. Segurança (resumo para quem mantém)

- **escapando valores de config**: `brand`, `emoji`, títulos, labels → `html.escape`
- **CTA**: bloqueia `javascript:`/`data:` em links
- **sanitize_html opcional**: para Markdown de terceiros
- **highlight**: escapa antes do `innerHTML`
- **backend**: nenhum `shell=True`; `subprocess` com lista de args
- **`.gitignore`**: protege `.env`, `*.key`, `out/`, checkpoints pessoais

> Consulte `docs/SEGURANCA.md` para o modelo completo.

---

## 7. Como estender (guia rápido)

**Novo recurso de interface (docs):**
1. Adicione o HTML no template de `build()` (f-string).
2. Adicione o CSS no `src/assets/style.css` (use as variables do `:root`).
3. Adicione o JS na seção correspondente do `APP_JS`.
4. Se for opcional, respeite o dict `features` (`F["x"]`).

**Novo tema:**
Adicione um bloco `[data-theme="x"]` em `THEMES_CSS` e o mapeie em
`get_theme_css` (voltando o `default_theme`).

**Novo tipo de bloco de landing (ex.: cards de lista):**
Adicione a transformação no loop de `build_landing` (após o `_cardize`).

**Sempre:** rode `python scripts/check_a11y.py` e gere os 5 builds
(`config.py`, `demo`, `landing`, `recursos`, `site`) para validar.

---

## 8. Notas de decisão (ADR curto)

- **Markdown é a única fonte de entrada** — todo o resto é camada de saída.
- **1 dependência (`markdown`)** — qualquer coisa que exija mais é avaliada.
- **Offline**: sem CDN — badges externos só no README (não no HTML gerado).
- **Design system autoral** (esmeralda/teal + âmbar) — anti "vibe coding".
- **A11y WCAG 2.2 AA de fábrica** — skip-link, focus-visible, reduced-motion.

---

## 9. CLI (`src/cli.py`), Testes e CI

### CLI
`python src/cli.py build [config.py]` — gera HTML.
`python src/cli.py init <nome> [-d DIR] [--template docs|landing]` — cria projeto novo
a partir de modelo (config + `docs/` ou `LANDING.md`). Democratiza para não-devs.

### Testes
Suíte `tests/` (pytest): build docs/landing, sanitize/XSS, temas, `_cardize`,
`_side_label`, CSP e noopener presentes.
```bash
python -m pytest -q
```

### CI (GitHub Actions)
`.github/workflows/ci.yml`:
- `test`: instala `markdown pytest` → roda pytest → gera builds.
- `build-pages` (branch `main`): gera a landing `site/` e publica no **GitHub Pages**.

---

## 10. Endurecimento (CSP / prefers-contrast / noopener)

- **CSP**: o HTML gerado inclui meta `Content-Security-Policy`
  (`default-src 'self'; script-src 'self' 'unsafe-inline'; style-src ...; img-src 'self' data: ...`).
  Como o JS/CSS são inline, `'unsafe-inline'` é necessário; ainda assim bloqueia
  recursos de origem externa (reforça o offline).
- **prefers-contrast**: modo alto contraste automático via `@media (prefers-contrast: more)`.
- **noopener**: todo link externo ganha `rel="noopener noreferrer"` (anti-tabnabbing).

