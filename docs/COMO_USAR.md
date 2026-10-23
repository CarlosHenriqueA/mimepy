# 👶 MimePy — Como usar, passo a passo (para leigos)

Este guia é para quem **nunca usou o MimePy** (nem precisa saber programar).
Aqui você aprende o básico para criar **documentação**, **landing page** e
**blog** a partir de textos simples em Markdown.

> **O que é o MimePy?** Uma ferramenta que pega arquivos de texto (Markdown) e
> vira um **site bonito** (HTML) — com menu lateral, busca, claro/escuro e
> acessibilidade — **sem precisar escrever código**.

---

## 1. O que você precisa (5 minutos)

| Item | O que é | Precisa? |
|---|---|---|
| **Python** (3.9+) | "motor" que roda a ferramenta | ✅ sim |
| **`markdown`** (pacote) | único componente extra | ✅ sim |
| Um **editor de texto** | para escrever os `.md` | ✅ sim (Bloco de Notas serve) |
| Saber Markdown | formato de texto simples (`#` título, `**negrito**`) | aprender em 2 min |

---

## 2. Instalar (só o essencial)

```bash
# 1) tenha o Python instalado (no Windows: python.org)
# 2) instale o único componente extra
pip install markdown
```

Pronto. A ferramenta MimePy não precisa de instalação além disso — você a usa a
partir da pasta onde a baixou.

---

## 3. Primeiro contato: crie seu primeiro site

O MimePy tem um **comando de inicialização** que cria tudo para você:

```bash
# cria uma pasta "meu-site" com tudo pronto
python src/cli.py init meu-site

# entra na pasta e gera o site
cd meu-site
python <caminho>/src/cli.py build config.py
```

Um HTML foi criado. Abra-o no navegador (duplo clique). Você já tem um site com
menu e aparência profissional, partindo de um único texto.

---

## 4. O Markdown: a "linguagem" que você usa para escrever

Markdown é texto puro com alguns símbolos. Veja o essencial:

```markdown
# Título grande (h1)

## Título de seção (h2)

### Subtítulo (h3)

Texto normal. **isto fica em negrito**, *isto em itálico*.

- item de lista
- outro item

1. item numerado
2. outro

```python
código aparece com destaque
```

> uma observação importante (fica em caixa destacada)

[Título do link](https://exemplo.com)
```

**Regra de ouro:** abra um parêntese com `#` e escreva; feche com `#` esse
trecho de código. Use **Enter** para cada parágrafo e deixe uma **linha em
branco** entre parágrafos.

---

## 5. Os três tipos de site que o MimePy cria

O MimePy tem três "modos". Você escolhe no arquivo `config.py` (uma linha).

| Modo | Para quê | Analogia |
|---|---|---|
| **`docs`** | Documentação com **menu lateral** e busca | estilo GitBook / Wikipedia técnica |
| **`landing`** | **Site de 1 página** de apresentação | "vitrine" de um produto/serviço |
| **`blog`** | **Lista de posts** ordenados por data | diário/notícias/artigos |

### 5.1 Modo **docs** (documentação)
- Pasta com vários arquivos `.md` + um `config.py` que ordena o **menu lateral**.
- Ideal para: manual, ajuda, Wiki, README de projeto.

**Como usar:**
1. Coloque seus textos em `docs/` (ex.: `docs/README.md`, `docs/guia.md`).
2. No `config.py`, liste os arquivos na ordem do menu:
   ```python
   "sidebar": [
       ("README.md", "Visão geral"),
       ("guia.md",     "Guia completo"),
   ],
   ```
3. Rode o build. O menu lateral aparece com busca e navegação anterior/próxima.

### 5.2 Modo **landing** (site de 1 página)
- Escreva TUDO num único arquivo (chamado `LANDING.md`).
- O `#` vira o título grande do topo; cada `##` vira uma seção da página;
  blocos `###` consecutivos vêm como **cards** (colunas com ícone).

**Como usar:**
1. Crie o `config.py` com `"mode": "landing"`.
2. Escreva seu `LANDING.md` (ex.: "🐱 Meu Produto" no `#`; `## Por que usar`,
   `### Rápido`, `### Simples`, `### Grátis`).
3. Rode o build → site de apresentação com navbar fixa e hero no topo.

### 5.3 Modo **blog**
- Tenha uma pasta `blog/` com vários posts `.md`.
- Cada post começa com um *frontmatter* (título, data, resumo):
  ```markdown
  ---
  title: Meu primeiro post
  date: 2026-10-23
  description: Um resumo do post.
  ---

  Conteúdo do post em Markdown...
  ```
- O build monta uma **página com a lista** (mais recente primeiro). Cada post
  abre ao clicar no título.

**Como usar:**
1. Crie `blog/` e coloque seus posts.
2. No `config.py`: `"mode": "blog"`.
3. Rode o build → página com a lista de posts.

---

## 6. Onde usar o MimePy na prática

- **No seu PC:** rode o build e abra o HTML — funciona offline, sem internet.
- **No GitHub Pages (grátis):** publique o HTML gerado e ganhe um endereço
  público: `https://voce.github.io/meu-site/`. Detalhes no arquivo
  `GUIA_GITHUB_PAGES.md` da raiz do projeto.

---

## 7. Resumo rápido (cola)

```bash
pip install markdown                       # única dependência
python src/cli.py init meu-site            # cria projeto
cd meu-site
python <caminho>/src/cli.py build config.py   # gera o HTML
```

- Modo docs → `"mode": "docs"`, arquivos em `docs/`
- Modo landing → `"mode": "landing"`, arquivo `LANDING.md`
- Modo blog → `"mode": "blog"`, arquivos em `blog/` (com `date:` no topo)

---

> **Dúvida?** O bom é que o MimePy não quebra nada: mude um título, rode o
> build de novo, e o site atualiza. Comece simples e vá adicionando seções.