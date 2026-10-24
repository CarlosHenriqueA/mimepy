# 🗺️ MimePy — Roadmap & Futuras Melhorias

Evolução do framework. **Prioridade: 🔴 alta · 🟡 média · 🟢 baixa.**

## ✅ Feito (v0.1)

- [x] Gerar **1 página HTML** a partir de múltiplos Markdown
- [x] **Sidebar de navegação** (TOC com âncoras), estilo GitBook
- [x] **Responsivo**: desktop + celular (menu hambúrguer mobile, sem JS)
- [x] Tabelas com **rolagem horizontal** no mobile (`table-scroll`)
- [x] Código com fundo escuro + rolagem horizontal
- [x] **Config-driven**: só editar `config.py`
- [x] Zero dependência além de `markdown`

## ✅ Feito (v0.2)

- [x] **Busca** na sidebar (filtra links por título)
- [x] **Dark mode** (toggle claro/escuro, persistente via localStorage)
- [x] **Navegação anterior/próximo** no fim de cada documento
- [x] **Botão copiar** nos blocos de código (com feedback)
- [x] **Voltar ao topo** (botão fixo)
- [x] **Estilos de impressão/PDF** (Ctrl+P → PDF limpo)
- [x] **Robustez de tabelas** (blank line antes do separador)
- [x] **meta description** p/ SEO e compartilhamento
- [x] **Modo LANDING PAGE** (`"mode": "landing"`) — site de 1 página a partir de Markdown
- [x] **Hero configurável** (emoji, tagline, CTA) no modo landing
- [x] **Landing premium** — navbar fixa com blur (links às seções), hero com gradiente no título (fallback seguro), cards animados com hover
- [x] **Cards automáticos** — blocos `###` dentro de uma seção viram uma grade de cards
- [x] **Compatibilidade cross-browser** validada (Chrome/Edge/Firefox): `inset`→offsets explícitos, `background-clip:text` com fallback + `@supports`, clipboard com fallback `execCommand`
- [x] **Design system autoral** (`DESIGN.md` + tokens via CSS variables): paleta esmeralda/teal + âmbar (CTA), fuga do gradiente índigo/roxo "vibe coding", cards variados (anti-slop), tipografia/espaçamento coerentes
- [x] **Acessibilidade nativa (WCAG 2.2 AA)**: skip-link (2.4.1), foco visível `:focus-visible` (2.4.7), `prefers-reduced-motion` (2.3.3), `aria-label` em sidebar/nav/main, `role="main"`, `lang` no `<html>`
- [x] **Bug de tabelas corrigido**: pré-processamento quebrava tabelas legítimas (header+separador); agora só insere linha em branco quando necessário → tabelas viraram `<table>` reais (acessíveis a leitores de tela)
- [x] **Exemplos de landing**: negócio fictício (Café Aurora) + showcase de recursos (ambos com o visual premium)

## 🔴 Alta (concluído — v0.3)

- [x] **Tema escuro automático** por preferência do sistema (`prefers-color-scheme`) como default (sem "flash")
- [x] **Highlight de sintaxe** de código (tokenizador leve offline, sem Pygments)
- [x] **Logo/imagem** da marca configurável no `config.py` (`logo`)
- [x] **Busca no conteúdo** (não só no título) — filtra o texto renderizado das seções
- [x] **Modo landing**: itens de seção sem `###` (listas de itens `- **Título**: ...`) também viram cards
- [x] `aria-current` nos links da sidebar (scrollspy destaca a seção atual) [a11y]
- [x] **Validação de contraste WCAG AA** automática via `scripts/check_a11y.py` (linter do DESIGN.md) [a11y]
- [x] **Âncoras compartilháveis** por seção (botão § copia `URL#id`) + **TOC recolhível** no topo de docs longas

## 🟡 Média (concluído — v0.3)

- [x] **Gerar PDF** a partir do mesmo config (script dedicado `scripts/gen_pdf.py` — headless Chrome/Edge ou WeasyPrint; opcional, mantém 1 dependência)
- [x] **Múltiplos idiomas** (toggle 🌐 pt⇄en — textos da interface)
- [x] **Botões de compartilhamento** (botão 🔗 copia link da página + âncoras § por seção)
- [x] **Temas alternativos** pré-prontos (`theme: light/dark/neon/paper/mono`)
- [x] **TOC sticky** em docs longas (`.df-toc` fixo ao rolar)
- [x] **Atalho de teclado `/`** para focar a busca (padrão GitBook/Mintlify)
- [x] **Templates de landing prontos** (startup, produto, evento, docs, contato, blog, bio, vendas) em `examples/templates/`
- [x] **Documentação técnica** `docs/TECNICO.md` (para dev/IA)
- [x] **Modo landing**: formulário de contato via Markdown (bloco `fence form`, offline)
- [x] **Página de "Acessibilidade"** na doc do framework (declarar conformidade WCAG e recursos nativos) [a11y]
- [x] Opção de **tamanho de fonte** e **alto contraste** no topo (recurso WAI) [a11y]

## ✅ Feito (v0.5)

- [x] **Templates aprimorados** — `startup`, `produto` e `evento` com mais camadas
  (sobre, valores, equipe/métricas, depoimentos, comparativo, agenda, palestrantes,
  ingressos, FAQ) e dados de demonstração realistas.
- [x] **Template `blog`** movido para o módulo de templates (padrão com os demais).
- [x] **Template `bio`** (link-in-bio estilo Linktree): perfil, botões, produto,
  newsletter — com `PESQUISA_CONCORRENTES.md` (pesquisa prévia do mercado).
- [x] **Template `landingpage`** de alta conversão + **página conectada `thank-you.html`**.
- [x] **Página conectada** no motor: `build_landing` copia `thank-you.html` da pasta
  do config para a saída; `deploy_pages.py` também publica no `_site`.
- [x] **Home** com acesso direto a todos os templates/exemplos (15 links, 0 quebrados).
- [x] **Contraste no modo claro** (a11y): landing e temas claros das docs usam texto
  quase-preto e links esmeralda-escura AA — antes herdavam as cores claras do tema
  escuro, ilegíveis sobre o fundo branco.

## 🟡 Média (concluído — v0.3)

- [x] **`prefers-contrast` automático** (alto contraste via media query do SO, sem botão)
- [x] **Busca com snippet/destaque** do trecho que casou
- [x] **Tema claro na landing por config** (`theme:"light"` → nasce clara)
- [x] **CLI**: `mimepy build`, `mimepy init <projeto>` (cria pasta + config + docs)
- [x] **Ícones na sidebar** (emojis viram badges `.side-ic`)
- [x] **Testes pytest** (`tests/`) — build + security + temas

## 🟢 Baixa / publicidade

- [x] **GitHub Actions** que roda `build.py` e publica no GitHub Pages
- [x] **Changelog** (`CHANGELOG.md`) + gerador `scripts/gen_changelog.py`
- [ ] **Imagens responsivas** (lazy-load / width no Markdown)
- [ ] **Exportação DTCG/Tailwind** do `DESIGN.md` (`tokens.json`/`theme.css`)
- [ ] **Multi-versão de docs** (`/v1/`, `/v2/`) via `out_dir` por versão
- [ ] **Site/changelog** público em GitHub Pages

---

## 💡 Ideias de mercado (para tornar o MimePy atraente/publicável)

Concorrência: GitBook, ReadTheDocs, Docusaurus, Mintlify, MkDocs. Diferenciais que **o MimePy pode explorar** para se destacar:

### Diferenciais competitivos (foco)
1. **Simplicidade radical** — 1 dependência (`markdown`), 1 comando, 1 arquivo HTML. Nada de Node/JS build complexo.
2. **Zero lock-in** — entrada é Markdown puro; saída é HTML autocontido (liberta de indexação própria).
3. **Full offline** — serve por e-mail, pen-drive, GitHub Pages; sem CDN nem analítica obrigatória.
4. **Leve** — HTML de dezenas de KB, não MB (ótimo p/ GitHub Pages e carregamento rápido).
5. **Pronto para GitHub Pages** — só subir o `index.html` num branch/`docs`; publicado de graça.

### Posicionamento de mercado
- **Público-alvo:** devs solo, pequenos times, projetos open source que querem docs bonitas **sem configurar um framework pesado** (Docusaurus/MkDocs exigem setup Node/Python+plugins).
- **Mensagem:** "Documentação bonita em 30 segundos, sem build complexo."
- **Canais:** GitHub, DEV.to, Reddit (r/webdev), Hacker News — engajando via "simplicidade".

### Monetização (se quiser evoluir)
- **Open source core (GPL-2.0)** + opcional **tema Pro / templates pagos** (diferente da GPL, em arquivo separado).
- **Serviço**: "monte sua documentação" (pago) usando o framework.
- **Sponsor/GitHub Sponsors** para o projeto.

> **Estratégia sugerida:** manter o core **gratuito e GPL-2.0** (maior adoção/adota liberdade), e monetizar com **temas/serviços** opcionais — padrão do mercado (ex.: Vite, Astro).

---

*Framework open source (GPL-2.0) criado a partir da necessidade de gerar documentação bonita e reutilizável a partir de Markdown. Publicação futura planejada.*
