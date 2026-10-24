# 🏗️ MimePy — Framework de Documentação & Landing Pages

<!-- Badges (offline): pills inline, sem CDN. Versão/versão/licença como
     credibilidade. Se publicar no GitHub, pode trocar por shields.io. -->
<p>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#0d9488;border:1px solid #0f766e;">📦 v0.3</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#0f766e;border:1px solid #15803d;">⚖️ GPL-2.0</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#2dd4bf;border:1px solid #5eead4;color:#064e3b;">🐍 Python 3.9+</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#f59e0b;border:1px solid #d97706;">📝 Markdown</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#111827;border:1px solid #374151;">📴 100% offline</span>
</p>

**O que é:** um framework **próprio e reutilizável** que gera, a partir de **Markdown** simples, tanto **documentação** (estilo GitBook/ReadTheDocs) quanto **landing pages** (site de 1 página).

> **Versão 0.2** — documentação (busca, dark mode, prev/next, copiar, impressão/PDF) **+ modo landing page premium** (navbar fixa, hero com gradiente, cards) para sites de 1 página.

> **🟢 Compatibilidade:** MimePy requer **Python 3.9 ou superior** (validado por análise estática/`ast` — sem recursos de 3.10+/3.11+). Única dependência: `markdown` (≥3.6).

## 🎨 Design system autoral

O MimePy tem um **design system próprio** (`DESIGN.md` — tokens em formato padronizado para devs e agentes consumirem):

- **Paleta:** esmeralda/teal (marca) + **âmbar** reservado ao CTA único
- **Fuga do "vibe coding"**: sem gradiente índigo/roxo genérico; composição anti-slop (cards variados, hierarquia por tipografia/espaço)
- **Tipografia:** stack de sistema (legível, offline, sem webfont)
- **Tokens:** cores, tipografia, espaçamento, raios, elevação — tudo em `src/assets/style.css` (docs) e `LANDING_CSS` (landing), centralizados via CSS variables

## Dois modos

| Modo | Para quê | Saída |
|---|---|---|
| **`docs`** (padrão) | Documentação multi-seção com sidebar + TOC | 1 página com navegação |
| **`landing`** | Site de 1 página premium (hero + seções + cards) | 1 página estilo landing |

> Ambos partem de Markdown e produzem **HTML autocontido, responsivo e offline**. Como escolher: veja `config.example.py` (campo `mode`).

## Características

| Recurso | Docs | Landing |
|---|---|---|
| 📄 Entrada em Markdown | ✅ | ✅ (1 arquivo) |
| 🌐 HTML autocontido (offline) | ✅ | ✅ |
| 📱 Responsivo (celular) | ✅ | ✅ |
| 🧭 Sidebar + TOC | ✅ | — |
| 🔍 Busca | ✅ | — |
| 🌙 Dark mode | ✅ | — |
| 🧭 Prev/Next | ✅ | — |
| 📋 Copiar código | ✅ | ✅ |
| 🖨️ Impressão/PDF | ✅ | ✅ |
| 🧭 **Navbar fixa** com links às seções | — | ✅ |
| 🎨 **Hero com gradiente** (fallback seguro) | — | ✅ |
| 🗂️ **Cards automáticos** (`###` → grade) | — | ✅ |
| 🏷️ **Badge de ícone** em cards (emoji destacado) | — | ✅ |
| 🔘 **Links de card** viram botões CTA | — | ✅ |
| 📱 **Responsivo** (3 breakpoints: <360 / <600 / <900) | ✅ | ✅ |
| 🖤 **Tema escuro automático** (pref. do sistema) | ✅ | — |
| 🎨 **Highlight de sintaxe** (offline) | ✅ | — |
| 🖼️ **Logo configurável** | ✅ | — |
| 🔍 **Busca no conteúdo** (não só título) | ✅ | — |
| 🔗 **Âncoras por seção** (copiar link) | ✅ | — |
| 📑 **TOC recolhível** (docs longas) | ✅ | — |
| 🔗 **Compartilhar** (copiar link) | ✅ | — |
| 🎛️ **Temas** (light/dark/neon/paper/mono) | ✅ | — |
| 📑 **TOC recolhível + sticky** (docs longas) | ✅ | — |
| ⌨️ **Atalho `/`** p/ focar a busca | ✅ | — |
| 🎨 **Templates** de landing (startup/produto/evento/docs/contato) | — | ✅ |
| 🧑‍💻 **Documentação técnica** (dev/IA) | ✅ | — |
| 🌐 **Idiomas** (toggle pt/en) | ✅ | — |
| 📄 **Gerar PDF** (script) | ✅ | — |
| 📝 **Formulário** (landing, via Markdown) | — | ✅ |

## Como usar (passo a passo rápido)

### Documentação (`mode: docs`)
```bash
pip install markdown
# coloque seus .md em docs/ + edite config.py (mode: docs)
python src/build.py        # -> index.html
```

### Landing page (`mode: landing`)
```bash
pip install markdown
# crie um LANDING.md + aponte config.py (mode: landing, landing_md: LANDING.md)
python src/build.py        # -> index.html
```

> Veja **`examples/`** para exemplos prontos.

## 📦 Saídas geradas (onde está cada index.html)

Cada comando `build.py` gera **um** `index.html`. Não são duplicados — são saídas de modos/configs diferentes:

| Arquivo | Origem | Conteúdo |
|---|---|---|
| `index.html` (raiz) | `build.py config.py` | **Doc do framework** (modo docs, 4 arquivos) |
| `site/index.html` | manual | **Landing oficial p/ GitHub Pages** |
| `examples/landing/out/index.html` | `build.py examples/landing/config.landing.py` | Exemplo de **landing de negócio** (Café Aurora) |
| `examples/recursos/out/index.html` | `build.py examples/recursos/config.recursos.py` | Exemplo de **showcase de recursos** |

> Para usar em outro projeto: rode o `build.py` apontando para um config — ele gera o `index.html` do `out_file` conforme o `out_dir` do config. Não precisa copiar/renomear manualmente.

## Estrutura da pasta

```
mimepy/
├── config.py / config.example.py
├── LICENSE              ← GPL-2.0
├── INDEX.md             ← guia p/ o Hermes "acionar"
├── SESSION_CHECKPOINT.md
├── docs/                ← docs do framework (este conteúdo)
├── src/
│   ├── build.py         ← motor (docs + landing)
│   └── assets/style.css ← tema
├── site/                ← landing oficial p/ GitHub Pages
└── examples/
    ├── landing/         ← landing de negócio fictício (Café Aurora)
    ├── recursos/        ← landing de "recursos do framework"
    └── demo/           ← exemplo de reuso (fictício, docs de demonstração)
```

## Para usar em OUTRO projeto

1. Copie a pasta do framework (ou só o `src/` + `config.py`).
2. Escolha o modo (`docs` ou `landing`) e ajuste o `config.py`.
3. Coloque seus `.md` (em `docs/` ou como `landing_md`).
4. Rode `python src/build.py`.

## Licença

**GPL-2.0** — licença de código aberto com copyleft forte: use, modifique e distribua livremente, desde que obras derivadas também sejam GPL-2.0.

---

*Veja `TUTORIAL.md` (passo a passo) e `REGRAS_DE_ESTILO.md` (formatação).*
