# Primeiros passos

Crie sua **primeira página** em minutos.

## 1. Estrutura

```
meu-projeto/
├── config.py      → identidade + navbar da documentação
└── docs/          → seus arquivos .md (1 por página)
```

## 2. Crie um arquivo de exemplo

`docs/hello.md`:

```markdown
# Olá, mundo!

Esta é a **primeira página** do meu projeto.
```

## 3. Aponte no config

```python
PROJECT = {
    "mode": "docs",
    "name": "MeuProjeto",
    "sidebar": [("hello.md", "👋 Olá, mundo")],
}
```

## 4. Gere e abra

```bash
python src/build.py
# → index.html — abra no navegador
```

> Você já tem uma documentação com **barra lateral** (esquerda) e conteúdo à
> direita, pronta. Basta adicionar mais `.md` e listá-los no `sidebar`.