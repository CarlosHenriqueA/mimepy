# MimePy — O que você pode criar ✨

> Transforme **Markdown simples** em **documentação**, **landing pages**, **blog** e
> **páginas de vendas** — bonitas, responsivas e 100% offline.

---

## 🔍 Recursos prontos

| Recurso | Docs | Landing |
|---|---|---|
| 📄 A partir de Markdown | ✅ | ✅ |
| 📱 Responsivo (celular) | ✅ | ✅ |
| 🌙 Temas (light/dark/neon/paper/mono) | ✅ | ✅ |
| 🔍 Busca na sidebar | ✅ | — |
| 🧭 Navegação prev/next | ✅ | — |
| 🖨️ Impressão/PDF nítida | ✅ | ✅ |
| 🧩 Página conectada (ex.: thank-you) | ✅ | ✅ |
| 🎨 Cards, tabelas, depoimentos | ✅ | ✅ |
| 📬 Formulário de contato (offline) | — | ✅ |
| ✍️ Modo blog (posts por data) | ✅ | ✅ |

---

## 🎨 Templates prontos (8)

**🚀 Startup** · **🛠️ Produto** · **🎟️ Evento** · **📚 Docs** · **📬 Contato** ·
**✍️ Blog** · **🧞 Bio** · **💰 Vendas** — cada um já vem com conteúdo de exemplo:
copie, troque os textos e publique.

---

## 💡 Ideias de uso

### Para negócios
- Landing de produto/serviço
- Página institucional
- Página de vendas + página de obrigado
- Bio/link-in-bio para redes sociais (estilo Linktree)

### Para projetos
- Documentação técnica (README expandido)
- Guias e tutoriais
- Wiki de um repo
- Site de um framework/OSS
- Blog de posts por data

---

## 🧪 Exemplo rápido (só Markdown)

```markdown
# Minha Empresa
> Tagline cativante aqui.

## O que fazemos
Descreva seu produto de forma simples.

## Contato
Fale com a gente: **ola@empresa.com**
```

Agora rode:
```bash
python src/build.py examples/landing/config.landing.py
```

E gere um `index.html` lindo, pronto para publicar.

---

## ⚙️ Como funciona

1. Escreva seu conteúdo em um arquivo `.md` (com `##` separando as seções).
2. No `config.py`, escolha o modo: `"mode": "docs"` · `"landing"` · `"blog"`.
3. Rode `python src/build.py`.
4. Pronto — 1 arquivo HTML, responsivo, offline. Para mais páginas, monte o
   `_site` com `python scripts/deploy_pages.py` e publique no GitHub Pages.

> **Zero framework pesado.** Só Python + `markdown`. Acessível (WCAG 2.2 AA) e
> com contraste AA garantido no claro e no escuro.

---

*© 2026 MimePy · v0.5 · GPL-2.0 · Feito com o próprio MimePy.*
