# ✨ MimePy — Novas Melhorias Ideadas (pesquisa de mercado/frontend)

> Registro das **novas** melhorias idealizadas além do roadmap, baseadas em
> boas práticas de frontend/UI/UX e no posicionamento de mercado (GitBook,
> ReadTheDocs, Docusaurus, Mintlify, MkDocs). **Ad-hoc — ideias a avaliar.**

---

## ✅ Concluído (deste ciclo)

- **Temas pré-prontos** `paper` e `mono` (além de dark/neon/light) → `THEMES_CSS`.
- **TOC sticky** em docs longas (`.df-toc` fica fixo ao rolar).
- **Atalho de teclado `/`** para focar a busca (padrão GitBook/Mintlify).
- **Badge de licença/versão** no README e no site (credibilidade).
- **Toolbar à direita** na doc (acessibilidade/dark/idioma/fonte).
- **Documentação técnica** `docs/TECNICO.md` (para dev/IA).
- **Compatibilidade Python 3.9+** validada e documentada.

---

## 📌 Anotado para melhorias futuras (novas)

24. **4 landing templates prontos** (startup, produto, evento, docs) em `examples/templates/` — copiar → editar → publicar (dar ao usuário um ponto de partida de download).
25. **`prefers-contrast` automático** — acionar o modo alto contraste via media query do SO (sem botão).
26. **CLI `mimepy init/build`** — criar projeto + rodar build com 1 comando (democratiza).
27. **Busca com snippet/destaque** — mostrar o trecho que casou no resultado.
28. **Exportação DTCG/Tailwind** do DESIGN.md (`tokens.json`/`theme.css`).
29. **Multi-versão de docs** (`/v1/`, `/v2/`) via `out_dir` por versão.
30. **GitHub Action** para build automático + deploy no Pages por PR.

---

## 🚀 De maior impacto (recomendado avaliar primeiro)

1. **Temas alternativos via DESIGN.md** — além do tema autoral, permitir `theme: "neon" | "paper" | "mono"` que troca apenas os tokens do `DESIGN.md`/CSS variables. Baixo custo (já temos tokens), alto valor de "sabor".
2. **Exportação DTCG/Tailwind do DESIGN.md** — usar o linter `@google/design.md export` para gerar `tokens.json`/`theme.css` consumíveis em outros projetos. Facilita adoção.
3. **CLI (`mimepy build/init`)** — `mimepy init <projeto>` cria pasta + config + sidebar a partir de um template; `mimepy build` roda. Democratiza o uso para não-devs.
4. **Busca com destaque (highlight)** — além de filtrar, mostrar o trecho do conteúdo que casou (snippet). Melhora muito a usabilidade de docs grandes.

## 🎨 Frontend/UI/UX (provenientes da auditoria anti-slop)

5. **`prefers-contrast` (alto contraste automático)** — usar a media query para acionar o modo HC sem botão, em usuários que já pedem no SO.
6. **Tema escuro em landing** — hoje a landing é sempre escura; permitir landing clara/escura por config.
7. **Imagens responsivas** — suporte a `width`/lazy-load de imagens no Markdown (melhora performance mobile).
8. **Sticky TOC** em docs longas — o TOC recolhível pode virar sticky ao rolar.
9. **Print aprimorado** — numeração de páginas e capa em `@media print`.

## 🔐 Segurança/a11y

10. **CSP (Content-Security-Policy)** — adicionar meta CSP (script-src, style-src) para endurecer o HTML gerado.
11. **`rel="noopener"`** em links externos (já é default moderno, mas garantir).
12. **Testes automáticos (pytest)** — criar `tests/` para build+security, substituindo os scripts ad-hoc.

## 🌍 Mercado/adoção

13. ✅ **Badge de licença/versão** no README e no site (pills inline offline).
14. ✅ **Templates de exemplo** — 4 landing templates prontos (startup, produto, evento, docs) em `examples/templates/`.
15. **Changelog automático** — derivado do ROADMAP/SESSION_CHECKPOINT.
16. **GitHub Actions** — workflow que roda `build.py` e publica no GitHub Pages (1-clique).

---

### Priorização sugerida (MoSCoW)
- **Must (próximo ciclo):** 4 (busca com destaque) · 1 (temas) 
- **Should:** 3 (CLI) · 7 (imagens responsivas) · 10 (CSP)
- **→ feitos:** 13 (badges) · 14 (templates) · 8 (toc sticky) · 17 (tecla /) · 1 (temas)
- **Could:** 2 (export tokens) · 5 (prefers-contrast)
- **Won't (agora):** 12 (pytest full) · 16 (CI) — após base estável

> **Filosofia:** manter **1 dependência (`markdown`), 1 arquivo HTML, offline**.
> Cada melhoria deve preservar simplicidade; se exigir dependência nova, avaliar
> se vale o trade-off (o MimePy se vende por "simples").

---

## 🆕 Novas melhorias — research de concorrentes (v0.3)

Benchmark contra **GitBook · Docusaurus · ReadTheDocs · Mintlify · MkDocs**.
Diferencias observados nos concorrentes e como o MimePy pode capturá-los
mantendo a simplicidade:

| Concorrente | Recurso que chama atenção | Como o MimePy faria (mantendo 1 dep) |
|---|---|---|
| MkDocs | **material design / ícones embutidos** | ✅ tema "paper" **feito** + ícones por emoji já têm |
| GitBook | **pesquisa global + atalhos de teclado (**`/`**)** | ✅ tecla `/` **feito** |
| Docusaurus | **multiversão de docs** (`/v1/`, `/v2/`) | `out_dir` por versão (já suporta) |
| ReadTheDocs | **build remoto + preview por PR** | GitHub Action que roda build (já planejado) |
| Mintlify | **hierarquia de sidebar em grupos** | sidebar por seções/agrupamento no config |
| GitBook/MkDocs | **dark/light nativo + código highlight** | ✅ já temos |
| Docusaurus | **blog/notas** via markdown | modo "blog" (lista de posts) |

### Novas melhorias priorizadas (etapas de adoção)

17. ✅ **Atalho de teclado `/`** para focar a busca (padrão GitBook/Mintlify) — 1 linha de JS.
18. **Ícones por emoji + símbolos** nos links da sidebar (visual rico sem assets).
19. **Sidebar agrupada por seções** (múltiplos grupos no config), como Mintlify.
20. **Modo "texto simples"** (sem highlight) para renderização determinística/de teste.
21. **`--watch`** no CLI: rebuild automático ao salvar `.md` (DX de dev).
22. **Metadados por página** (frontmatter `title`/`description`/`order`) no modo docs.
23. **Sitemap + 404** para o site GitHub Pages.

### Estratégia recomendada (próximos ciclos)
- **Maior ROI agora:** 17 (atalho `/`), 18 (ícones), 19 (sidebar agrupada) — custo baixo, apelo alto.
- **Médio:** 20 (modo texto), 21 (watch), 22 (frontmatter).
- **Baixo/indireto:** 23 (sitemap/404), blog, multiversão (dependem de uso real).

> **Consistência:** todas as novas ideias preservam o pilar "1 dependência,
> 1 arquivo HTML, offline". Ideias que exigiram build complexo (Node) foram
> descartadas até que valha o trade-off.
