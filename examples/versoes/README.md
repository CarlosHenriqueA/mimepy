# 📚 MimePy — Exemplo de Multi-versão de Docs (`/v1/`, `/v2/`)

Como publicar **várias versões da mesma documentação** (ex.: v1 estável e v2 em
desenvolvimento), tudo a partir de **Markdown puro** — sem nenhuma dependência
nova.

## Como funciona (só Markdown)

- Os arquivos `.md` ficam em `docs_versao/` (**compartilhados** entre as versões).
- Cada versão tem seu **próprio `config.py`** que diz **para onde** gerar o HTML
  via `out_dir` (e o título via `page_title`).
- O MimePy gera **um HTML por execução** do build — rodar o config de cada
  versão produz uma pasta separada.

## Gerar

```bash
# v1 (estável)  -> examples/versoes/out_v1/index.html
python src/build.py examples/versoes/v1/config.py

# v2 (preview)  -> examples/versoes/out_v2/index.html
python src/build.py examples/versoes/v2/config.py
```

## No GitHub Pages

Para servir `/v1/` e `/v2/`, publique cada `out_*` numa subpasta do site:

```
_site/
  index.html        <- home (v-stável / seletor)
  v1/index.html     <- out_v1/index.html
  v2/index.html     <- out_v2/index.html
```

(Dica: um pequeno `index.html` de home com links para `/v1/` e `/v2/`.)

## Filosofia mantida

- **1 dependência** (`markdown`) · **1 arquivo HTML por versão** · **offline**.
- Mudar um texto em `docs_versao/*.md` atualiza as duas versões ao rodar cada
  build — você escreve uma vez, publica em muitas versões.