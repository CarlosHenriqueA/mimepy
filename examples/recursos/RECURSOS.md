# MimePy — O que você pode criar ✨

> Transforme **Markdown simples** em **sites de 1 página** (landing) ou **documentação** bonita e responsiva.

---

## 🔍 Recursos prontos

| Recurso | Landing | Docs |
|---|---|---|
| 📄 A partir de Markdown | ✅ | ✅ |
| 📱 Responsivo (celular) | ✅ | ✅ |
| 🌙 Dark mode | — | ✅ |
| 🔍 Busca na sidebar | — | ✅ |
| 🧭 Navegação prev/next | — | ✅ |
| 🖨️ Impressão/PDF | ✅ | ✅ |
| 🎨 Tema escuro | ✅ | — |

---

## 💡 Ideias de uso

### Para negócios
- Landing de produto/serviço
- Página institucional
- Página de captura (newsletter)
- Portfólio simples

### Para projetos
- Documentação técnica (README expandido)
- Guias e tutoriais
- Wiki de um repo
- Site de um framework/OSS

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
2. No `config.py`, coloque `"mode": "landing"`.
3. Rode `python src/build.py`.
4. Pronto — 1 arquivo HTML, responsivo, offline.

> **Zero framework pesado.** Só Python + `markdown`.

---

*© 2026 MimePy · GPL-2.0 · Feito com o próprio MimePy.*
