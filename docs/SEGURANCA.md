# 🛡️ MimePy — Segurança

Modelo de segurança do framework **para quem vai usá-lo** para documentar
projetos e criar sites. Foque no que protege **você** e **quem lê** sua doc.

---

## Resumo executivo

| Tópico | Status |
|---|---|
| Entrada | Markdown (arquivo local, do próprio autor) |
| Dependências | **1** (`python-markdown`) — cadeia pequena = menos superfície de ataque |
| Saída | HTML **estático, autocontido, offline** (sem JS de terceiros, sem CDN) |
| XSS via config | ❌ **mitigado** (escapa `brand`, `emoji`, textos; bloqueia `javascript:` em CTA) |
| XSS via Markdown | ⚠️ depende (Markdown permite HTML bruto) → use `sanitize: true` |
| Injeção de path | config local de confiança; sem input remoto |

---

## 1. Entrada confiável (config)

O MimePy roda **localmente** a partir de:
- um `config.py` (código Python que você escreve), e
- arquivos `.md` que você coloca na pasta.

Como o config é **código Python seu** (importado com `importlib`), ele tem o
mesmo poder que rodar `python`. **Não carregue configs de terceiros sem revisar.**

## 2. Saída estática e offline

A saída é **HTML estático**: sem JavaScript de CDN, sem analítica, sem
mensagens externas. Isso reduz drasticamente a superfície de ataque em
produção — não há código de terceiros executando no navegador de quem lê.

## 3. XSS (Cross-Site Scripting)

### a) Valores do config
Todos os textos vindos do config (`brand`, `name`, `page_title`, `intro`,
`footer`, `subtitle`, `tagline`, `cta_text`, `emoji`) são **escapados com
`html.escape`** ao serem inseridos no HTML → um valor com `<script>` vira
texto inofensivo.

**CTAs:** links de CTA que começam com `javascript:` ou `data:` são
**bloqueados** (revertidos para `#`). (Defesa contra `javascript:` XSS.)

### b) Conteúdo do Markdown (ATENÇÃO)
Por padrão, o MimePy usa `python-markdown` com extensões que **permitem HTML
bruto** no Markdown (flexibilidade: o autor pode embutir `<div>`, `<span>`,
etc.). Isso é ótimo, mas significa que **Markdown de fonte NÃO confiável**
(conteúdo comentado por terceiros, importado, etc.) poderia injetar script.

**Quando usar `sanitize: true`** no config:

```python
PROJECT["sanitize"] = True   # remove <script>, on* e javascript: do markdown
```

Isso liga um filtro que:
- remove tags `<script>`/`<style>` (e conteúdo),
- remove atributos `on*` (onclick, onerror, onload...),
- remove URLs `javascript:`/`data:` de `href`/`src`.

> **Regra de ouro:** se qualquer conteúdo da sua doc vem de fonte que você não
> controla 100%, **ative `sanitize: true`**.

## 4. Path / escrita de arquivos

`docs_dir`, `out_dir` e `out_file` vêm do config (seu, de confiança). O build
cria a pasta de saída se preciso e grava **um** HTML. Não há input remoto.

## 4b. Backend / scripts (verificação de segurança)

Os scripts (`scripts/gen_pdf.py`, `scripts/check_a11y.py`) usam `subprocess` para
chamar ferramentas externas (navegador headless, `npx`). **Revisão feita:**
- **Nenhum `shell=True`** → impossibilita *command injection* por argumento.
- `subprocess.run` recebe **lista de argumentos** (nunca concatenação de string).
- Paths de navegador são **fixos** no código (não vindos de input).
- `importlib.exec_module` carrega o `config.py` como código Python — **por design**
  (o config é do autor). Nunca carregar config de terceiros sem revisar.
- `check_a11y.py` faz `npx @google/design.md` — comando fixo, sem input de usuário
  no argumento.

## 5. .gitignore (não publique acidentais)

O `.gitignore` já protege:
- segredos: `.env`, `*.key`, `*.pem`, `auth.json`
- gerados: `index.html`, `examples/*/out/`
- pessoais/de contexto: `HANDOFF_CONVERSA.md`, `SESSION_CHECKPOINT.md`, `*.zip`, `backups/`

> **Antes de publicar** o framework no GitHub, revise o `.gitignore` e garanta
> que nenhum `.md`/config com dados reais do seu projeto ficou exposto.

---

## 4c. Endurecimento (defesa em profundidade — v0.3)

Além do básico, o HTML gerado agora inclui:

- **CSP (Content-Security-Policy)** — `meta` no head limita `default-src 'self'`;
  `script-src`/`style-src` permitem inline (necessário p/ o JS/CSS do framework),
  mas **bloqueiam recursos de origem externa** (reforça o offline e reduz exfiltração).
- **`rel="noopener noreferrer"`** — aplicado automaticamente a todo link externo
  (evita *tabnabbing* e vazamento de referrer).
- **prefers-contrast automático** — o modo alto contraste liga sozinho para
  usuários que já pedem no SO (`@media (prefers-contrast: more)`), além do botão.

## Checklist rápido (antes de publicar uma doc)

1. [ ] Ative `sanitize: true` se o Markdown não for 100% seu.
2. [ ] Revise o config — sem chaves/segredos dentro.
3. [ ] Confirme o `.gitignore` cobre `.env`, `out/`, zips.
4. [ ] Teste abrir o `index.html` direto do disco (`file://`) — funciona offline.

---

*Segurança por padrão: saída estática + escaping dos valores de config +
sanitização opcional de Markdown. Em caso de dúvida, ative `sanitize: true`.*
