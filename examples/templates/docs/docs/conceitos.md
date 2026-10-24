# Conceitos

Entenda a base do MimePy antes de avançar.

## Markdown é a única fonte

Você escreve em Markdown; o MimePy cuida do **design, busca, temas e
acessibilidade** na camada de saída (HTML/CSS/JS gerada).

## Modos

| Modo | Para quê |
|---|---|
| `docs` | Documentação com **barra lateral** + conteúdo à direita |
| `landing` | Site de 1 página de apresentação |
| `blog` | Lista de posts ordenados por data |

## Um arquivo HTML, offline

Cada build gera **um arquivo HTML autocontido** (CSS+JS embutidos) — portátil,
sem servidor, perfeito para GitHub Pages.

> Regra de ouro: 1 dependência (`markdown`), 1 arquivo HTML, offline.