# 🌐 GitHub Pages com MimePy — Guia completo (incl. blog)

Este documento explica como o **MimePy** publica sites no **GitHub Pages** e
como criar um **blog** com GitHub + GitHub Pages. É um guia de referência para
quem for manter o projeto ou replicar a publicação.

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

## 5. Verificação de segurança antes de publicar

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

## 6. Referências

- Docs oficiais do GitHub Pages: https://docs.github.com/pt/pages
- MimePy (este projeto): `site/SITE.md` (landing), `examples/blog/` (exemplo),
  `docs/TECNICO.md` (arquitetura do motor).
