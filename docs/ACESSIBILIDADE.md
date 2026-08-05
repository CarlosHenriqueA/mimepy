# ♿ MimePy — Acessibilidade

Declaração de acessibilidade do framework, alinhada à **WCAG 2.2** (Web Content
Accessibility Guidelines, padrão internacional da W3C/WAI).

---

## Conformidade

O HTML gerado pelo MimePy (docs e landing) busca atender o **nível AA** da WCAG.
Itens implementados **de fábrica** (sem o autor precisar fazer nada):

| Critério | Recurso | Docs | Landing |
|---|---|---|---|
| **1.3.1** Informação/relações | `aria-label` em sidebar/nav, `role="main"`, headings | ✅ | ✅ |
| **1.4.3** Contraste (AA) | paleta com contraste válido (validado no DESIGN.md) | ✅ | ✅ |
| **1.4.10** Reflow | `viewport` + responsivo (sem scroll horizontal 2D) | ✅ | ✅ |
| **2.1.1** Teclado | todos os controles operáveis por teclado + `:focus-visible` | ✅ | ✅ |
| **2.3.3** Movimento reduzido | `prefers-reduced-motion` | ✅ | ✅ |
| **2.4.1** Bypass | **skip-link** ("Pular para o conteúdo") | ✅ | ✅ |
| **2.4.7** Foco visível | `:focus-visible` com contraste | ✅ | ✅ |
| **3.1.1** Idioma | `lang` no `<html>` | ✅ | ✅ |

## Recursos de acessibilidade do usuário (WAI)

- **Tamanho de fonte** — botões `A / A+ / A++` no topo (persistente).
- **Alto contraste** — botão `◐` ativa modo preto/amarelo (persistente).
- **Tema automático** — segue a preferência do sistema (`dark`/`light`).
- **Sem cores como única informação** — tabelas, títulos e ícones têm
  complemento textual (não só cor).

## Como validar

O MimePy inclui `scripts/check_a11y.py`, que verifica a presença dos recursos
de acessibilidade no HTML **e** roda o linter de contraste do `DESIGN.md`:

```bash
python scripts/check_a11y.py
# -> PASS (WCAG 2.2 AA — estrutura e contraste)
```

## Limitações honestas

- **Contraste por padrão**: cores padrão passam no linter; se você personalizar
  cores, rode o linter para conferir.
- **HTML bruto no Markdown**: se o conteúdo não for 100% confiável, ative
  `sanitize: true` (ver `docs/SEGURANCA.md`) — também protege a acessibilidade
  contra conteúdo inesperado.

---

*MimePy se compromete com docs/sites acessíveis por padrão, com controles de
fonte, contraste e movimento para o usuário final.*
