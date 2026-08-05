# 🎨 MimePy — Regras de Estilo

Como escrever os Markdown para sempre obter uma documentação bonita e consistente.

## Estrutura de títulos

- Use **um `#` por arquivo** (o título principal de cada doc).
- Use `##` para seções e `###` para subseções.
- Não pule níveis (não vá de `##` direto para `####`).

```markdown
# Título do Documento
## Seção principal
### Subseção
```

## Listas e priorização

Use listas para sempre que houver mais de 2 itens. Para prioridade, padronize:

| Símbolo | Significado |
|---|---|
| 🔴 **Alta** | Crítico / Fase 0 |
| 🟡 **Média** | Importante / Fase 1 |
| 🟢 **Baixa** | Nice to have / Fase 2+ |

## Tabelas

- Use tabelas para **comparações** e **dados tabulares** (ficam ótimas no tema).
- Cabeçalho com `|---|`.
- Tabelas largas **rolam horizontalmente** no celular automaticamente (wrapper `.table-scroll`).

```markdown
| Item | Valor | Status |
|---|---|---|
| Exemplo | R$ 10 | ✅ OK |
```

## Caixas de destaque (citações)

Use `>` para criar caixas de nota com borda azul — bom para **avisos, conclusões e chamadas**.

```markdown
> **Importante:** não substitui aconselhamento jurídico profissional.
```

## Código

- Código em linha: use crase `` ` ``.
- Blocos de código: use três crases ```` ``` ```` (ganham fundo escuro + rolagem no mobile).

```python
def exemplo():
    return "ok"
```

## Modelo de arquivo (bom padrão)

```
# 📌 Título (com emoji temático)

> **O que é:** breve resumo.
> **Status:** ✅ / ⚠️ / 🚧

---

## 1. ... (seções numeradas ajudam a navegar)

---

*Rodapé opcional com referências.*
```

## Checklist de qualidade

- [ ] Um `#` por arquivo (título principal)
- [ ] Seções numeradas (`1.`, `2.`...) quando longas
- [ ] Itens de prioridade com 🔴🟡🟢
- [ ] Tabelas para comparações
- [ ] `>` para notas/conclusões
- [ ] Blocos de código com destaque de linguagem
