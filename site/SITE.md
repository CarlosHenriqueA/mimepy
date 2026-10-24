# MimePy — Sites e documentação bonitos, apenas a partir de textos Markdown

Uma ferramenta que transforma **Markdown puro** em **HTML profissional**:
documentação com menu e busca, landing pages e blog — **sem build complexo,
sem Node, sem servidor, 100% offline**.

## 🚀 Para começar em 30 segundos

| Passo | O que fazer |
|---|---|
| **1** | Tenha Python 3.9+ e rode `pip install markdown` (única dependência) |
| **2** | Escreva seus textos em `.md` e (se quiser) edite o `config.py` |
| **3** | `python src/build.py` → pronto, seu `index.html` está criado |

> 👶 **Nunca usou?** Veja o **[Guia para leigos →](docs/index.html#COMO_USAR)**,
> que ensina tudo do zero (instalar, escrever Markdown, os 3 modos).

## ✅ Por que usar o MimePy?

### 📄 Markdown simples
Escreva em Markdown puro. **Nada de sintaxe proprietária** — o que você já sabe continua igual.

### 📚 Três tipos de site
Documentação (**docs**), 1 página de apresentação (**landing**) e **blog** — escolha o modo no `config.py`.

### 🔍 Busca no conteúdo
O leitor filtra por título **e** conteúdo, com atalho e resultados instantâneos.

### 🌙 Dark / Light / Neon / Paper / Mono
Cinco temas com um clique — e **segue a preferência do sistema** automaticamente.

### ♿ Acessível (WCAG 2.2 AA)
Skip-link, foco visível, alto contraste e tamanho de fonte nativos de fábrica.

### 📱 100% Responsivo
Abre perfeitamente em **celular, tablet e desktop**, com menu hambúrguer no mobile.

### 🖨️ PDF de graça
Ctrl+P vira um **PDF limpo** — ou use o script dedicado de PDF.

### 🧩 Um arquivo só, offline
Saída leve e portátil. **Sem CDN, sem build complexo, sem Node, sem dor.**

## ⚙️ Estado do projeto

Versão **v0.5** · **45 testes** automáticos (build, segurança e temas) · **CI** que
gera todas as páginas e publica no **GitHub Pages** · **16 páginas** no site.

**Recursos confirmados:**
- 🧑‍💻 **Motor modular** (`build`/`render`/`security`/`themes`/`modes`) com
  sanitizador por parser real (stdlib) — bloqueia XSS sem dependência nova.
- 🧩 **Página conectada**: uma landing de vendas pode acompanhar um
  `thank-you.html` (resposta pós-clique), publicado junto no deploy.
- 📝 **Markdown é a única fonte** de entrada; design/JS ficam na camada de saída.
- 🖨️ **Impressão/PDF** nítida e opaca (Ctrl+P) ou via script dedicado.
- ♿ **Contraste AA** garantido no claro **e** no escuro (validado com medidor).

> **Backstory:** framework autoral, sem "vibe coding" — paleta esmeralda/teal +
> âmbar ousada, com acessibilidade de fábrica.

## 👶 O que dá para criar (exemplos reais)

### 📘 Documentação completa
Documentação **geral do framework** (mode docs): sidebar com ícones, busca,
temas, âncoras, TOC e mais — **10 guias** do simples ao técnico, incluindo o
**[Guia para leigos](docs/index.html#COMO_USAR)**, o **[Tutorial](docs/index.html#TUTORIAL)**
e a **[Documentação de construção](docs/index.html#COMO_FOI_FEITO)**.

[📘 Abrir a documentação →](docs/index.html)

### 🎯 Exemplos prontos (demos de verdade)
Cada exemplo é um projeto real e completo, só de Markdown — clique e veja:
**☕ Café Aurora** (negócio) · **🏗️ Showcase** (recursos) · **☀️ Solaris Kit**
(reuso em outro produto) · **📰 Blog** (posts por data).

[☕ Café Aurora →](examples/landing/out/index.html) · [🏗️ Showcase →](examples/recursos/out/index.html)
· [☀️ Solaris Kit →](examples/demo/out/solaris-kit.html) · [📰 Blog →](examples/blog/out/index.html)

### 🎨 Templates prontos (copie, edite e publique)
Oito modelos para você começar com conteúdo de exemplo e apenas trocar os
textos. Cada um já tem o layout, os cards e as seções montados.

**🚀 Startup** — institucional com valores/equipe/depoimentos · **🛠️ Produto** — funcionalidades + tabela comparativa + garantia
· **🎟️ Evento** — agenda + palestrantes + ingressos + FAQ · **📚 Docs** — documentação com sidebar
· **📬 Contato** — formulário de captura de leads · **✍️ Blog** — posts por data
· **🧞 Bio** — link-in-bio estilo Linktree · **💰 Vendas** — landing de alta conversão + página de obrigado

[🚀 Startup →](examples/templates/startup/out/index.html) · [🛠️ Produto →](examples/templates/produto/out/index.html)
· [🎟️ Evento →](examples/templates/evento/out/index.html) · [📚 Docs →](examples/templates/docs/out/index.html)
· [📬 Contato →](examples/templates/contato/out/index.html) · [✍️ Blog →](examples/templates/blog/out/index.html)
· [🧞 Bio →](examples/templates/bio/out/index.html) · [💰 Vendas →](examples/templates/landingpage/out/index.html) · [🙏 Obrigado →](examples/templates/landingpage/out/thank-you.html)

### 🌐 Publicar no GitHub Pages (grátis)
Hospede o HTML gerado e ganhe um endereço público. Guia completo no arquivo
`GUIA_GITHUB_PAGES.md` da raiz do projeto.

[🌐 Abrir o guia do GitHub Pages →](https://github.com/CarlosHenriqueA/mimepy/blob/main/GUIA_GITHUB_PAGES.md)

## 🎨 Design system & acessibilidade

- **Paleta autoral** esmeralda/teal + âmbar (CTA único) — distante do "vibe coding" roxo genérico.
- **Acessibilidade nativa (WCAG 2.2 AA)**: skip-link, foco visível, alto contraste, tamanho de fonte, `prefers-reduced-motion`.
- **Temas**: light / dark / neon / paper / mono.

## ⚖️ Licença

**GNU GPL v2** — código aberto com copyleft. Use, modifique e distribua livremente; obras derivadas também devem ser GPL-2.0.

<p>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#0d9488;border:1px solid #0f766e;">📦 v0.5</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#0f766e;border:1px solid #15803d;">⚖️ GPL-2.0</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#2dd4bf;border:1px solid #5eead4;color:#064e3b;">🐍 Python 3.9+</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#15803d;border:1px solid #166534;">👶 Leigos bem-vindos</span>
</p>
