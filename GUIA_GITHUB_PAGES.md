# 🌐 GitHub Pages com MimePy — Guia completo (multi-página + blog)

Este documento explica como o **MimePy** publica sites no **GitHub Pages**, como
**conectar uma página a outra** (site multi-página) e como criar um **blog** com
GitHub + GitHub Pages. É um guia de referência para quem for manter o projeto
ou replicar a publicação.

> **Resumo:** o repositório é `github.com/CarlosHenriqueA/mimepy` e o site fica
> em **https://carloshenriquea.github.io/mimepy/** · o Pages é servido a partir
> do diretório `_site/`, montado automaticamente pelo `scripts/deploy_pages.py`
> dentro do GitHub Actions (workflow `.github/workflows/ci.yml`).

---

## 1. Como o GitHub Pages funciona

O **GitHub Pages** transforma um repositório em site estático (HTML/CSS/JS puro,
sem backend). Pontos-chave (da documentação oficial do GitHub):

- O site é servido a partir de uma **fonte de publicação**: uma *branch* + pasta
  (ex.: `main` + `/`) **ou** um **workflow do GitHub Actions**.
- Neste projeto usamos a configuração **workflow** (`build_type=workflow`): um
  `.github/workflows/ci.yml` gera os arquivos e os publica.
- O resultado fica em `https://<user>.github.io/<repo>/`.
- Por ser **estático**, é **gratuito** e perfeito para docs, landing e blogs.

### Fontes de publicação (como o Pages sabe o que servir)

| Fonte | Como ativa | Quando usar |
|---|---|---|
| **Workflow** (usado aqui) | `gh api` define `build_type=workflow` | build customizado |
| **Branch + pasta** | Settings → Pages → escolhe branch | repo é o site direto |

---

## 2. Como o MimePy monta o site (`scripts/deploy_pages.py`)

O problema que este script resolve: se publicássemos **apenas a landing**, os
links para as demais páginas (documentação, exemplos, blog, templates)
**quebrariam** online, porque essas pastas não existiriam no site publicado.

O `deploy_pages.py` monta o diretório **`_site/`** com a **árvore completa**:

```
_site/
  index.html              <- HOME: landing principal (site/index.html)
  docs/index.html         <- documentação geral (index.html da raiz)
  examples/...            <- exemplos e templates (examples/**/out/*.html)
  sitemap.xml             <- p/ SEO
  robots.txt              <- rastreadores
  404.html                <- página 404 amigável
```

Assim, **cada link relativo resolve para um arquivo dentro do próprio site**
(`docs/`, `examples/...`), e nada quebra online. O `.gitignore` cobre `_site/`
(é artefato gerado — não vai para o repositório).

### Comando
```bash
python scripts/deploy_pages.py site/config.site.py
# -> monta _site/ com home + docs + exemplos + sitemap/robots/404
```

> No CI, o workflow roda o build de **todas** as páginas (doc, landing, exemplos,
> templates) e então chama o `deploy_pages.py` **antes** do `upload-pages-artifact`.

---

## 3. O workflow (`ci.yml`) — passo a passo

`.github/workflows/ci.yml` tem 2 jobs:

1. **`test`** — em todo push/PR: instala `markdown pytest`, roda `python -m pytest`
   (suíte `tests/`), e gera os builds para garantir que nada quebrou.
2. **`build-pages`** — só na `main`: gera todas as páginas → roda
   `deploy_pages.py` (monta `_site/`) → `upload-pages-artifact` (path: `_site`) →
   `deploy-pages`.

Permissions necessárias: `contents: read`, `pages: write`, `id-token: write`.

Config do Pages (uma vez):
```bash
gh api -X POST repos/CarlosHenriqueA/mimepy/pages -f build_type=workflow
```

---

## 4. 📝 Criar um BLOG com GitHub + GitHub Pages

O MimePy tem um **`mode: blog`** de fábrica (arquivo de exemplo: `examples/blog/`).
É a forma mais simples de ter um blog estático e grátis.

### Passo a passo

**1. Crie uma pasta de posts** (ex.: `blog/`) com arquivos `.md`. Cada post usa
`frontmatter` (título, descrição e data):
```markdown
---
title: Meu primeiro post
description: Um resumo do post.
date: 2026-08-05
---

Aqui vai o conteúdo do post em **Markdown**.
```

**2. Configure o `config.py`** com `mode: blog`:
```python
PROJECT = {
    "mode": "blog",
    "name": "Meu Blog",
    "page_title": "✍️ Meu Blog",
    "blog_dir": "blog",      # pasta com os posts
    "docs_dir": "blog",
    "out_dir": "out",
    "out_file": "index.html",
}
```

**3. Gere localmente:**
```bash
python src/build.py config.py      # -> out/index.html (lista de posts)
```

**4. Publique no GitHub Pages** — duas opções:

- **A (rápida, manual):** suba `out/index.html` e ative Pages por branch (`main` / `/`).
- **B (recomendada, automática):** use o workflow deste projeto — cada `git push`
  na `main` roda o build e publica. Para seu blog, crie um workflow equivalente
  que rode `python src/build.py <seu-config>.py` e faça upload do `out/`.

**5. Undeploy/atualizar:** como é estático, basta fazer novo `git push` que o
CI regenera e publica. Grátis, sem servidor.

### Pontos de atenção (segurança/pré-publicação)
- Não publique **dados pessoais** em posts/config (emails reais, caminhos do PC,
  chaves). Use placeholders (ex.: `<pasta-do-framework>`) e revisor `grep`.
- O MimePy gera **HTML autocontido/offline** — ideal para GitHub Pages (sem backend).
- O `frontmatter` suporta `title`, `description` e `date` (ordenação do blog).

---

## 5. 🔗 Conectar páginas entre si (site multi-página)

Este é o coração do que você viu no MimePy: **várias páginas HTML se linkando
umas às outras**, servidas por **um único site no GitHub Pages**. Funciona como
um site normal: cada `.html` é uma página, e os links `<a href>` levam de uma
à outra.

### 5.1 Como a navegação funciona no GitHub Pages

Um site no Pages é **apenas uma pasta de arquivos**. O que decide qual página
abre é a **URL relativa** no `href`:

```
https://seusite.github.io/            -> index.html  (página inicial / home)
https://seusite.github.io/sobre/      -> sobre/index.html
https://seusite.github.io/sobre.html  -> sobre.html
```

Para **ir de uma página a outra**, o `href` usa caminhos **relativos** (a partir
da página atual) ou **absolutos** (a partir da raiz do site):

```html
<!-- página: contato.html -->
<a href="index.html">Voltar ao início</a>        <!-- relativo: mesma pasta -->
<a href="/sobre.html">Sobre nós</a>              <!-- absoluto: a partir da raiz -->

<!-- página em subpasta: blog/post1.html -->
<a href="../index.html">Voltar à home</a>        <!-- sobe 1 nível -->
<a href="../sobre.html">Sobre</a>                <!-- sobe e acha sobre.html -->
```

> 💡 **Regra de ouro:** use **caminhos relativos** (`docs/...`, `../...`) e não
> URLs fixas com domínio. Assim o site funciona em qualquer lugar (localhost,
> Pages, outros domínios) sem quebrar.

### 5.2 Estrutura de um site multi-página (exemplo com o MimePy)

O MimePy gera **um HTML por config/build**. Para ter um site de várias páginas,
você mantém várias pastas/`out` — e o `scripts/deploy_pages.py` copia tudo para
o `_site/`, preservando **exatamente** a árvore de pastas:

```
_site/                          <- a raiz do site publicado
  index.html                    <- home (a página inicial)
  sobre.html                    <- página "Sobre"
  contato.html                  <- página "Contato"
  blog/
    index.html                  <- lista de posts
    post1.html                  <- um post
    post2.html                  <- outro post
  docs/
    index.html                  <- documentação
```

Cada página "sabe" como chegar às outras pelos `href` relativos.

### 5.3 Como criar, no MimePy, páginas que se conectam

**Passo 1 — crie cada página com seu próprio config/`out_file`:**
```python
# config.home.py -> gera a home (index.html)
PROJECT = {
    "mode": "landing",
    "page_title": "Meu Site",
    "out_dir": "out_home", "out_file": "index.html",
    # ... seções com links de navegação
}
```
```python
# config.sobre.py -> gera a página "Sobre"
PROJECT = {
    "mode": "landing",
    "page_title": "Sobre",
    "out_dir": "out_sobre", "out_file": "index.html",
}
```

**Passo 2 — nos Markdown, escreva os links entre páginas**
(no conteúdo `LANDING.md` de cada uma):

```markdown
# Minha Landing

[Conheça a página Sobre →](sobre/index.html)

## 🔗 Navegação
| Ir para | Link |
|---|---|
| Home | [index.html](index.html) |
| Blog | [blog/index.html](blog/index.html) |
| Documentação | [docs/index.html](docs/index.html) |
```

**Passo 3 — publique tudo no `_site`** (automático no CI deste projeto). O
`deploy_pages.py` já copia cada `out_*/index.html` para a posição certa com os
links relativos resolvendo.

### 5.4 Como o MimePy já resolve isso "de graça"

Com o `scripts/deploy_pages.py`, a home (landing) já vem **linkada** para:
- `/docs/index.html` (documentação geral)
- `/examples/landing/out/index.html` (Café Aurora)
- `/examples/blog/out/index.html` (blog)
- `/examples/templates/*/out/index.html` (templates)

Ou seja: **uma página aponta para as outras**, e tudo é servido pelo Pages.
Validamos os **9 links da home** — todos resolvem para arquivos reais no `_site`.

### 5.5 Checklist para não quebrar links online

1. [ ] Use **href relativos** (nunca `C:\...` nem domínio fixo).
2. [ ] Confira que o destino **existe** dentro do `_site` (ex.: `docs/index.html`).
3. [ ] Teste **localmente**: abra `_site/index.html` (duplo clique) e clique nos links.
4. [ ] Não publique dados pessoais nos caminhos/`href` (use placeholders).
5. [ ] Após o `push`, confira o CI verde (`gh run list`) — o Pages publica sozinho.

> 💡 **Dica de diagnóstico:** se um link "quebra" online mas funciona localmente,
> quase sempre é **caminho relativo errado** (muito `../` ou falta de subpasta).
> Confira a árvore do `_site` e a posição real do arquivo de destino.

---

## 6. Verificação de segurança antes de publicar

Sempre que for dar `push`/publicar, rode uma varredura de dados sensíveis:

```bash
# caminhos pessoais, projetos privados, tokens
grep -rniE "Users.Admin|projeto-secreto|ghp_|sk-[a-z0-9]{20,}" --include="*.md" --include="*.py" --include="*.html" .
# confirme que artefatos gerados (_site/, out/, zips) estão no .gitignore
git check-ignore _site/
```

> O `.gitignore` do MimePy já blinda: `.env`, `index.html` (raiz, gerado),
> `examples/*/out/`, `_site/`, `*.zip`, `HANDOFF_CONVERSA.md`,
> `SESSION_CHECKPOINT.md`.

---

## 7. Referências

- Docs oficiais do GitHub Pages: https://docs.github.com/pt/pages
- MimePy (este projeto): `site/SITE.md` (landing), `examples/blog/` (exemplo),
  `docs/TECNICO.md` (arquitetura do motor), `scripts/deploy_pages.py` (monta o
  `_site` multi-página).
