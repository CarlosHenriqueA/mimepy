# 🔬 Pesquisa prévia — concorrentes de "link in bio" / bio.site

> Documento obrigatório (etapa do processo): mapeamos os principais concorrentes
> antes de escrever qualquer código do template **bio**, para identificar o que
> aproveitar de melhor usando o ecossistema do MimePy (temas, tokens, cards,
> formulário offline) e entregar uma solução mais simples e flexível.
>
> **Fonte:** análise contínua de Linktree, Beacons, Bio.site (Squarespace),
> Taplink, Lnk.bio, Carrd e dxd.link (docs oficiais + comparativos 2025).

## 1. O que todos têm em comum (baseline)

| Recurso | Presente em |
|---|---|
| Foto/link de perfil + nome + bio curta | todos |
| One-link para redes sociais (Instagram, TikTok, etc.) | todos |
| Botões/links organizados em cards | todos |
| Ícones de redes sociais | todos |
| Tema de fundo customizável (cor, gradiente) | todos |
| (pagou) QR code + estatísticas de cliques | todos |

## 2. Diferenciais por plataforma

| Plataforma | Diferencial | Como o MimePy faria (1 dep, offline) |
|---|---|---|
| **Linktree** | o padrão; botões + integrações (análise pagas) | botões de card + `home_url` + 1 HTML |
| **Beacons** | monetização (embed de produto) + captura de e-mail + AI builder | card de produto + ` ```form ` (e-mail) |
| **Bio.site (Squarespace)** | clean, integrações PayPal/Stripe, SEO/custom-domain | card de produto com link de compra |
| **Taplink** | o mais customizável (400+ temas, fundo gradiente/imagem, animação de botão, seções/subpáginas) | tema `neon`/`mono`/`paper` + gradiente + hover de card |
| **Lnk.bio** | simples e barato, muitas fontes | temas prontos + CSS variáveis |
| **Carrd** | one-page flexível por seções | landing agrupada por `##` |

## 3. O que vamos aproveitar no template `bio`

1. **Perfil** — foto (emoji), nome, handle `@`, selo de verificação, mini-bio persuasiva.
2. **Ícones sociais** — barra de ícones por **emoji** (sem assets, offline).
3. **Botões principais** — cards com título, subtítulo, emoji/tag de destaque ("Novo", "Ao Vivo"), hover animado.
4. **Card de produto/serviço** — imagem (emoji), preço, descrição rápida, botão de compra.
5. **Mídia embutida** — bloco de player (YouTube/Spotify) via link/embed **offline** (cards com link).
6. **Captação de leads** — formulário ` ```form ` (e-mail/WhatsApp) offline.
7. **Temas** — escuro/claro/gradiente via `theme` + tokens do `DESIGN.md` (visual `neon`, `mono`, `paper`).

## 4. Diferencial de mercado do MimePy.

Nenhum concorrente entrega **1 arquivo HTML 100% offline, sem conta, sem plano,
sem branding da plataforma**. Com o MimePy:
- Você **publica onde quiser** (GitHub Pages, Netlify, próprio domínio).
- **Sem taxa e sem paywall** por recursos que os outros cobram (estatísticas? você
  usa um contador próprio — offline).
- Sem ID do construtor no footer.

> **Conclusão da pesquisa:** o template `bio` replicará o **padrão Linktree
> (cards)** + o **recursos de monetização do Beacons (produto + e-mail)** + a
> **customização do Taplink (temas/gradiente)** — tudo com a simplicidade e o
> offline do MimePy.
