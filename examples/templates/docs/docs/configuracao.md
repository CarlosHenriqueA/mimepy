# Configuração

Cada opção do `config.py` explicada.

## Identidade

```python
PROJECT = {
    "name": "MeuProjeto",     # nome exibido na barra lateral
    "brand": "📚",            # emoji/logotipo
    "page_title": "MeuProjeto",
    "lang": "pt-BR",
    "theme": "dark",          # light | dark | neon | paper | mono
}
```

## Estrutura

| Chave | O que faz |
|---|---|
| `docs_dir` | pasta com os arquivos `.md` |
| `out_dir` | pasta de saída do HTML |
| `out_file` | nome do arquivo gerado |
| `sidebar` | lista `(arquivo, título)` — vira a **barra lateral** |

## Recursos

```python
"features": {
    "search": True,    # busca na barra lateral
    "dark": True,      # toggle claro/escuro
    "prev_next": True, # navegação anterior/próxima
    "copy": True,      # botão copiar código
}
```

## Home

```python
"home_url": "../../../../index.html",  # link do logotipo → página principal
```

> Qualquer chave omissa usa o padrão seguro — seu template continua funcionando.