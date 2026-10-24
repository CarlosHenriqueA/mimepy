# 🧑‍💻 MimePy — Documentação de Construção (para desenvolvedores)

> **Perspectiva:** escrita por um desenvolvedor, para desenvolvedores. Explica,
> **item por item**, como o MimePy foi construído — quais arquivos foram criados
> e por quê, como cada parte funciona, e o contexto por trás das decisões.
>
> Se você vai dar manutenção, estender ou simplesmente se **inspirar** no código,
> este é o mapa do território. Complementa o `TECNICO.md` (referência) com a
> **história e o raciocínio** de como cada peça se encaixa.

---

## 1. A visão de arquitetura

O MimePy nasceu de um princípio simples e dogmático:

> **Markdown é a única fonte de entrada. Tudo o resto (design, JS, CSS) é camada
> de saída gerada pelo motor.**

Isso define cada decisão de código. Em vez de um gerador que "vira gente"
complexa, o MimePy é uma **função pura**: recebe `.md` → devolve um **único
HTML autocontido** (CSS+JS embutidos). Um arquivo, offline, portátil.

A intenção por trás disso:
- **Mantenibilidade** — tudo que "se mexe" (visual, interação) mora num lugar
  previsível e regenerável.
- **Portabilidade** — o HTML sai pronto para qualquer hospedagem estática
  (GitHub Pages, Netlify, SFTP) sem backend.
- **Longevidade** — o que importa (seu conteúdo) fica em texto simples, imune a
  quebras de framework.

---

## 2. Estrutura de pastas e arquivos (o mapa)

```
mimepy/
├── src/                       ← O MOTOR (Python)
│   ├── build.py               ← Orquestrador: monta DOCS + despacha modos
│   ├── modes.py               ← build_landing() + build_blog() + LANDING_CSS
│   ├── render.py              ← Markdown → HTML + frontmatter
│   ├── security.py            ← Sanitizador HTML por parser real (stdlib)
│   ├── themes.py              ← Temas: light/dark/neon/paper/mono
│   ├── _meta.py               ← VERSION (fonte única, sem drift)
│   ├── cli.py                 ← CLI: build / init / --watch
│   └── assets/style.css       ← CSS global das docs
├── docs/                      ← A DOCUMENTAÇÃO do próprio framework
│   ├── README.md              ← O que é & como usar
│   ├── COMO_USAR.md           ← Guia para leigos (novos usuários)
│   ├── TECNICO.md             ← Referência técnica (funções, config)
│   ├── COMO_FOI_FEITO.md      ← ESTE arquivo (a história da construção)
│   ├── REGRAS_DE_ESTILO.md    ← Regras de estilo do motor
│   ├── SEGURANCA.md           ← Modelo de segurança
│   ├── ACESSIBILIDADE.md      ← Conformidade WCAG 2.2 AA
│   ├── ROADMAP.md             ← Roadmap
│   └── MELHORIAS_FUTURAS.md   ← Melhorias ideadas/feitas
├── examples/                  ← Demos e templates de reuso
│   ├── landing/               ← Café Aurora (landing premium)
│   ├── recursos/              ← Showcase de recursos
│   ├── demo/                  ← "Solaris Kit" (reuso em outro produto)
│   ├── blog/                  ← Exemplo de modo blog
│   ├── versoes/               ← Exemplo de multi-versão (/v1/, /v2/)
│   └── templates/             ← 8 templates de landing (startup, produto,
│                                evento, docs, contato, blog, bio, vendas)
├── scripts/                   ← Ferramentas auxiliares
│   ├── check_a11y.py          ← Valida a11y (WCAG + npx designmd)
│   ├── deploy_pages.py        ← Monta _site/ para GitHub Pages
│   ├── export_tokens.py       ← Exporta design tokens (DTCG/Tailwind)
│   ├── gen_changelog.py       ← Gera CHANGELOG do ROADMAP
│   └── gen_pdf.py             ← Gera PDF (via headless)
├── tests/                     ← Suíte pytest (45 testes)
├── .github/workflows/ci.yml   ← CI: pytest + deploy GitHub Pages
├── config.py                  ← Config da documentação principal
└── GUIA_GITHUB_PAGES.md       ← Guia de publicação + blogs + multi-página
```

---

## 3. Como o motor foi construído — item por item

### 3.1 `src/render.py` — o coração: Markdown → HTML

**O que faz:** converte `.md` em `(html, meta)`, onde `meta` são os metadados do
`frontmatter` (title/description/order).

**Por quê separado:** é a função mais reutilizada (docs, landing, blog) e a mais
fácil de testar isoladamente. Isolá-la permitiu 45+ testes sem tocar no resto.

**Decisões técnicas:**
- Usa a única dependência do projeto, `python-markdown`, com extensões
  `tables`, `fenced_code`, `sane_lists`, `md_in_html`, `attr_list`, `def_list`.
- `parse_frontmatter()` extrai `--- title: X ... ---` com uma regex simples —
  suficiente e sem peso de uma lib YAML.
- `_robust_tables()` insere linha em branco antes do separador de tabela quando
  necessário — um bug real que fazia tabelas quebrarem após parágrafos soltos.

### 3.2 `src/security.py` — sanitização por parser real

**O que faz:** limpa HTML bruto (vindo de Markdown potencialmente não confiável)
removendo vetores XSS.

**Por quê parser real (e não regex):** a versão original usava regex, que é
frágil com markup malformado e aspas aninhadas. Trocamos por `html.parser`
(stdlib, zero dependência) que reconstrói a árvore e decide tag a tag.

**O que bloqueia:**
- Tags: `<script>`, `<style>`, `<iframe>`, `<object>`, `<embed>`, `<link>`,
  `<meta>`, `<base>`, `<form>`, `<input>`, `<svg>`, `<math>`, `<template>`.
- Atributos: `on*` (onclick, onerror, onload...).
- Protocolos: `javascript:`, `data:`, `vbscript:`, `file:`.
- `style` com `url(...)`/`@import`/`expression(`.

**O que preserva:** links `http(s)`/`mailto`/âncoras, `<code class="language-*">`
(necessário ao highlight), tabelas, texto formatado. Este é o equilíbrio entre
segurança e flexibilidade.

### 3.3 `src/themes.py` — identidade visual em CSS variables

**O que faz:** contém os 5 temas (`light`, `dark`, `neon`, `paper`, `mono`) como
blocos de CSS variables + `get_theme_css()` que decide qual aplicar.

**Decisões técnicas:**
- Todo o design depende das variáveis `--bg`, `--fg`, `--accent`, `--cta`, etc.
- Trocar de tema = trocar as variáveis. Zero duplicação de composição.
- `default_theme` decide o que o JS aplica antes do paint (evita *flash*).

### 3.4 `src/modes.py` — os modos landing e blog

**O que faz:** `build_landing()` (site de 1 página) e `build_blog()` (lista de
posts). Foram extraídos do monolítico `build.py` para manter cada preocupação
em seu arquivo.

**Decisões técnicas:**
- `LANDING_CSS` vive aqui (só faz sentido na landing).
- O formulário de contato é um marcador: ` ```form ... ``` ` no Markdown que vira um
  `<form class="contact-form">` real — **offline**, abrindo `mailto`.
- `build_blog()` usa o `frontmatter` (`date`) para ordenar posts do mais recente
  ao mais antigo — tudo a partir de Markdown.

### 3.5 `src/build.py` — o orquestrador (docs)

**O que faz:** monta a página de **documentação** (mode docs) com sidebar, busca,
TOC, prev/next, e despacha para os modos correto por `mode`.

**Por quê "orquestrador":** após a refatoração, ele passou de 1156 para ~536
linhas. Não guarda mais a lógica de landing/blog — **importa de `modes.py`** e
reexporta os nomes para preservar compatibilidade (ninguém quebra ao atualizar).

### 3.6 `src/cli.py` — a porta de entrada para não-devs

**O que faz:** `mimepy init <nome>` (cria projeto + config + docs) e
`mimepy build` (gera HTML) com `--watch` para rebuild ao salvar.

**Decisões técnicas:** democratizar — quem não é dev cria e publica sem tocar no
motor. Mantém a única dependência (`markdown`) e o HTML 1-arquivo.

---

## 4. Como a segurança foi pensada (defesa em profundidade)

1. **Entrada confiável por padrão**: o Markdown é do próprio autor (confiável).
   O sanitize é **opcional** (`sanitize: true`) para conteúdo de terceiros.
2. **Escaping dos valores de config**: `brand`, `emoji`, `name` sempre escapados
   (evita XSS via emoji).
3. **CSP** no `<head>`: `default-src 'self'` limita fontes de recursos.
4. **`rel="noopener noreferrer"`** em links externos (anti-tabnabbing).
5. **Block de `javascript:`/`data:`** em CTAs.
6. **Sem `shell=True`** no backend (sem command injection).

Isso está documentado em `docs/SEGURANCA.md`.

---

## 5. Como a acessibilidade foi garantida (WCAG 2.2 AA)

Não é uma feature; é embutida na estrutura do HTML gerado:
- **skip-link** (2.4.1) → salta para o conteúdo.
- **`:focus-visible`** (2.4.7) → foco visível em qualquer fundo.
- **`prefers-reduced-motion`** (2.3.3) → respeita quem odeia animação.
- **Alto contraste** manual (botão ◐) **e** automático (`prefers-contrast: more`).
- **`aria-current`** no scrollspy (navegação por leitor de tela).
- **Tamanho de fonte** ajustável (A/A+/A++).

`scripts/check_a11y.py` valida estrutura + contraste em CI.

---

## 6. Como o projeto é mantido e testado

- **45 testes** pytest em `tests/`: render, build (docs/landing/blog), CLI,
  temas, e **21 vetores de segurança** em `tests/test_security.py`.
- **CI** (`.github/workflows/ci.yml`): roda pytest + gera todos os builds + monta
  `_site/` e publica no GitHub Pages (`deploy_pages.py`).
- **`check_a11y.py`** roda junto para garantir WCAG.

---

## 7. O tom que queremos transmitir

> Este projeto começou com uma pergunta: *"e se eu pudesse ter sites bonitos e
> documentação profissional só de textos simples, sem sofrer?"* A resposta é o
> MimePy. Ele é pequeno de propósito, dogmático de propósito — **Markdown dentro,
> HTML impecável fora**.
>
> Ao manter ou estender este código, lembre-se das três regras que o mantêm
> saudável:
> 1. **Nunca adicione um passo que o usuário não pediu.** Simplicidade é recurso.
> 2. **Novas features devem preservar o pilar**: 1 dependência, 1 arquivo HTML,
>    offline.
> 3. **Segurança e a11y não são "depois do PR"** — são parte do design (é mais
>    barato e mais correto embutir do que consertar).

---

*Documentação de construção — MimePy v0.5. Se algo aqui divergir do código, o
código é a fonte da verdade; atualize este documento.*