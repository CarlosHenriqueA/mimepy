# MimePy — Documentação bonita, em 30 segundos

## ✅ Por que usar o MimePy?

### 📄 Markdown simples
Escreva em Markdown puro. **Nada de sintaxe proprietária** — o que você já sabe continua igual.

### 🔍 Busca no conteúdo
O leitor filtra por título **e** conteúdo, com atalho e resultados instantâneos.

### 🌙 Dark / Light / Neon
Tema claro/escuro com um clique — e **segue a preferência do sistema** automaticamente.

### ♿ Acessível (WCAG 2.2 AA)
Skip-link, foco visível, alto contraste e tamanho de fonte nativos de fábrica.

### 📱 100% Responsivo
Abre perfeitamente em **celular, tablet e desktop**, com menu hambúrguer no mobile.

### 🖨️ PDF de graça
Ctrl+P vira um **PDF limpo** — ou use o script dedicado de PDF.

### 🚀 Pronto para publicar
Um único arquivo HTML autocontido, perfeito para **GitHub Pages** e hospedagem estática.

### 🧩 Um arquivo só, offline
Saída leve e portátil. **Sem CDN, sem build complexo, sem Node, sem dor.**

## 💻 Como usar (3 passos)

| Passo | Ação |
|---|---|
| **1. Instalar** | `pip install markdown` (única dependência) |
| **2. Escrever** | coloque seus `.md` + edite o `config.py` |
| **3. Gerar** | `python src/build.py` → `index.html` |

```python
PROJECT = {
    "name": "MeuProjeto",
    "brand": "⚖️",
    "page_title": "📚 Documentação",
    "sidebar": [
        ("README.md",  "Visão geral"),
        ("02_GUIA.md", "Guia técnico"),
    ],
    "features": {"search": True, "dark": True, "share": True},
}
```

## 🗂️ Explore — veja o MimePy em ação

Cada item abre a respectiva página gerada pelo framework.

### 📚 Documentação
Documentação **geral do framework** (mode docs): sidebar com ícones, busca no
conteúdo, temas, âncoras, TOC e mais — 8 guias completos.

[📘 Abrir a documentação geral →](../index.html)

### 🎯 Exemplos prontos

**☕ Landing de negócio** — Café Aurora: hero com gradiente, cards de produto, navbar fixa.
[Ver a landing →](../examples/landing/out/index.html)

**🏗️ Showcase de recursos** — todo o potencial visual num único Markdown.
[Ver o showcase →](../examples/recursos/out/index.html)

**☀️ Demo (Solaris Kit)** — reuso em outro projeto (docs fictícias de produto).
[Ver o demo →](../examples/demo/out/solaris-kit.html)

**📰 Blog de exemplo** — modo `blog` com posts ordenados por data.
[Ver o blog →](../examples/blog/out/index.html)

### 🎨 Templates de landing (copie e edite)

**🚀 Startup** — proposta de valor + planos + FAQ.
[Ver template →](../examples/templates/startup/out/index.html)

**🛠️ Produto** — destaques + como funciona.
[Ver template →](../examples/templates/produto/out/index.html)

**🎟️ Evento** — agenda + palestrantes + inscrição.
[Ver template →](../examples/templates/evento/out/index.html)

**📚 Docs** — página inicial de documentação de projeto.
[Ver template →](../examples/templates/docs/out/index.html)


## 🎨 Design system & acessibilidade

- **Paleta autoral** esmeralda/teal + âmbar (CTA único) — distante do "vibe coding" roxo genérico.
- **Acessibilidade nativa (WCAG 2.2 AA)**: skip-link, foco visível, alto contraste, tamanho de fonte, `prefers-reduced-motion`.
- **Temas**: light / dark / neon.

## ⚖️ Licença

**GNU GPL v2** — código aberto com copyleft. Use, modifique e distribua livremente; obras derivadas também devem ser GPL-2.0.

<p>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#0d9488;border:1px solid #0f766e;">📦 v0.3</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#0f766e;border:1px solid #15803d;">⚖️ GPL-2.0</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#2dd4bf;border:1px solid #5eead4;color:#064e3b;">🐍 Python 3.9+</span>
  <span style="display:inline-block;padding:.15em .7em;margin:.1em;font-size:.8em;border-radius:10px;color:#fff;background:#15803d;border:1px solid #166534;">♿ WCAG 2.2 AA</span>
</p>
