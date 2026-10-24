# 🎨 MimePy — Templates de Landing Page

Templates prontos para você **copiar, editar e publicar** — cada um é uma
landing completa gerada pelo MimePy (modo landing), sem precisar partir do zero.

## Como usar

```bash
# 1. Copie o template desejado:  (de `examples/templates/<tipo>/`)
# 2. Edite o config.py (nome, emoji, textos) e o LANDING.md (conteúdo)
# 3. Gere o HTML:
python src/build.py examples/templates/<tipo>/config.py
#    -> examples/templates/<tipo>/out/index.html
```

## Templates disponíveis

| Template | Pasta | Ideal para |
|---|---|---|
| 🚀 **Startup** | `startup/` | App/SaaS: proposta de valor, planos, FAQ |
| 🛠️ **Produto** | `produto/` | Produto/serviço: destaques + como funciona |
| 🎟️ **Evento** | `evento/` | Conferência/workshop: agenda, palestrantes, inscrição |
| 📚 **Docs** | `docs/` | Página inicial de documentação de projeto |
| 📬 **Contato** | `contato/` | Captura de leads: formulário de contato + compromissos |

## O que vem em cada template

- `config.py` — identidade, tema (`dark`), hero (emoji, tagline, CTA)
- `LANDING.md` — conteúdo em Markdown: seções `##` viram seções; `###` viram **cards**

> Todos usam o **design system autoral** (esmeralda/teal + âmbar), são
> responsivos, acessíveis (WCAG 2.2 AA) e offline — como todo MimePy.
