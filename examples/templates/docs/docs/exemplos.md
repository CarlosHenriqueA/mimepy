# Exemplos

Casos reais para copiar e adaptar.

## Documentação (modo docs)

```python
PROJECT = {
    "mode": "docs",
    "name": "MeuProjeto",
    "docs_dir": "docs",
    "sidebar": [
        ("inicio.md", "🚀 Início"),
        ("guia.md",   "📖 Guia"),
    ],
}
```

## Landing page (modo landing)

```python
PROJECT = {
    "mode": "landing",
    "name": "MeuProjeto",
    "landing_md": "LANDING.md",
    "hero": {"emoji": "🚀", "tagline": "Bem-vindo!"},
}
```

## Blog (modo blog)

Cada post tem `date:` no topo; o build ordena do mais recente ao mais antigo.

> Explore `examples/` do framework para ver todos os exemplos rodando.