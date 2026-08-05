# 🧑‍🏫 MimePy — Tutorial Passo a Passo

Como gerar uma documentação bonita com o MimePy, do zero, em poucos minutos.

> **Versão 0.2** — os exemplos abaixo incluem os recursos novos (busca, dark mode, navegação).

## Passo 1 — Instalar a dependência

O MimePy usa o pacote Python `markdown` (a única dependência).

```bash
pip install markdown
```

> Se usar `uv`/venv, rode no ambiente ativo. Verifique com `python -c "import markdown"`.

## Passo 2 — Colocar seus Markdown

Crie os arquivos `.md` na pasta **`docs/`**. Dicas de organização:

| Convenção | Exemplo |
|---|---|
| Começar por um índice/visão geral | `README.md` |
| Usar numeração para ordem (opcional) | `01_INTRO.md`, `02_GUIA.md` |
| Um tópico por arquivo | `MERCADO.md`, `PROJETO_TECNICO.md` |

Os arquivos seguem **Markdown puro** (títulos, listas, tabelas, código, citações). Nada de especial.

## Passo 3 — Editar o `config.py`

Ajuste o mínimo necessário:

```python
PROJECT = {
    "name": "NomeDoProjeto",
    "brand": "⚖️",
    "subtitle": "Uma descrição curta",
    "page_title": "📚 Documentação do Projeto X",
    "intro": "Um parágrafo de boas-vindas.",
    "footer": "NomeDoProjeto · 2026",

    # Ordem + títulos da sidebar
    "sidebar": [
        ("README.md", "Visão geral"),
        ("01_INTRO.md", "Introdução"),
        ("02_GUIA.md", "Guia técnico"),
    ],
}
```

### Recursos opcionais (v0.2)

Todos vêm ligados por padrão. Desligue pondo `False`:

```python
PROJECT["features"] = {
    "search": True,     # busca na sidebar
    "dark": True,       # toggle claro/escuro
    "prev_next": True,  # navegação anterior/próximo
    "copy": True,       # botão copiar nos blocos de código
    "back_top": True,   # voltar ao topo
    "print": True,      # impressão/PDF
}
```

## Passo 4 — Gerar o HTML

```bash
python src/build.py
```

Deve imprimir:
```
[MimePy 0.2] OK -> C:\...\index.html  (N docs, X bytes)
```

Abra o `index.html` no navegador. Pronto — com busca, dark mode e tudo.

## Passo 5 — (Opcional) Criar uma LANDING PAGE premium

Com o MimePy você pode gerar um **site de 1 página** (hero + seções) a partir de Markdown, com **visual premium**: navbar fixa, hero com gradiente e **cards** — ideal para landing de produto, institucional, captura etc.

### 5.1 Criar o Markdown da landing

Crie `LANDING.md` (ex.: junto do config). Use `#` para o título (hero), `##` para as seções e **`###` para os itens que viram cards**:

```markdown
# Minha Empresa
> Tagline cativante.

## Recursos
### 🚀 Recursos A
Descrição do recurso A.

### 🛠️ Recursos B
Descrição do recurso B.
```

> **Dica:** os blocos `###` consecutivos dentro de uma `##` viram automaticamente uma **grade de cards** com hover animado. As `##` viram seções com link na **navbar fixa** do topo.

### 5.2 Configurar o modo landing

No `config.py`, coloque `"mode": "landing"` e aponte o arquivo:

```python
PROJECT = {
    "mode": "landing",
    "name": "Minha Empresa",
    "page_title": "Minha Empresa — Site",
    "landing_md": "LANDING.md",
    "docs_dir": ".",                 # LANDING.md junto do config
    "out_dir": "out",
    "out_file": "index.html",

    # Hero (topo da página)
    "hero": {
        "emoji": "🚀",
        "tagline": "Uma manchete cativante.",
        "cta_text": "Começar",
        "cta_link": "#secoes",
    },
}
```

### 5.3 Gerar

```bash
python src/build.py
# [MimePy] LANDING OK -> out/index.html
```

> **Exemplos prontos:** `examples/landing/` (negócio fictício "Café Aurora") e `examples/recursos/` (showcase dos recursos) — ambos com o visual premium (navbar, hero e cards).

## Integrar ao fluxo (no Hermes)

Quando quiser **acionar o framework** para documentar um projeto ou criar uma landing, basta dizer algo como:

> "Use o MimePy (pasta `$MIMEPY`) para gerar a landing do projeto X" *(ou "a documentação")*

E o processo será: apontar o `config.py` para os `.md` do projeto → rodar `build.py` → entregar o `index.html`.

## Dicas rápidas

- **Tabela que estoura no celular** → já tem rolagem horizontal automática (wrapper `.table-scroll`).
- **Código longo** → blocos ```` ``` ```` ganham fundo escuro, rolagem e **botão copiar**.
- **Notas/citações** → `> texto` cria caixa de destaque azul.
- **Dark mode** → botão 🌙 no topo da sidebar; a escolha é lembrada no navegador.
- **Gerar PDF** → abra o `index.html` e use **Ctrl+P** → "Salvar como PDF" (o print CSS deixa limpo).
- **Exemplo de reuso** → veja `examples/demo/` (projeto fictício de demonstração).

---

*Tem dúvida sobre formatação? Veja `REGRAS_DE_ESTILO.md`.*
