# 📄 GitHub Pages — publicação do MimePy

Esta pasta contém a **página de apresentação** do MimePy para publicação no **GitHub Pages** (grátis e direto do repositório).

## Como publicar (passo a passo simples)

### Opção A — GitHub Pages a partir do branch (recomendada)
1. Crie um repositório no GitHub (ex.: `mimepy`).
2. Suba o projeto do framework (incluindo a pasta `site/`).
3. Vá em **Settings → Pages**.
4. Em **Source**, selecione: branch `main` + pasta `/site` (ou `/docs`).
5. Publique. Sua página ficará em: `https://<usuario>.github.io/mimepy/`

### Opção B — Publicar só a página (sem repositório do código)
- Pode subir apenas o conteúdo de `site/` num repositório e ativar GitHub Pages nesse repositório.

## O que está em `site/`
| Arquivo | O que é |
|---|---|
| `index.html` | Página de apresentação (hero, recursos, como usar, licença) — tudo num arquivo, offline |
| `LICENSE` (copiar da raiz) | Texto GPL-2.0 (vincular no rodapé) |

> **Dica:** aponte o botão/rodapé "Abrir a documentação" para o `index.html` da **raiz** (a doc gerada pelo framework), se quiser publicar as duas.

## Boas práticas ao publicar
- **Nome do repositório** = nome do projeto público (ex.: `mimepy`).
- **README.md** na raiz com "o que é", badge de licença (`GPL-2.0`) e exemplo de uso.
- **Licença real**: manter o arquivo `LICENSE` na raiz do repositório (obrigatório para o GitHub mostrar a licença).

---

*Veja também `ROADMAP.md` → seção "publicidade" para a ideia de CI que publica automaticamente o `index.html` nas pages.*
