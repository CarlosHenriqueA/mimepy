---
title: Bem-vindo ao blog com MimePy
description: Como usar o modo blog para publicar posts a partir de Markdown.
date: 2026-08-05
---

O **MimePy** agora tem um modo `blog`: basta colocar arquivos `.md` numa pasta
e ele gera um HTML com a lista de posts. Cada post usa **frontmatter** com
`title`, `description` e `date`.

```python
PROJECT = {
    "mode": "blog",
    "blog_dir": "blog",   # pasta com os posts
}
```

> A ordem é pela `date` (mais recente primeiro).
