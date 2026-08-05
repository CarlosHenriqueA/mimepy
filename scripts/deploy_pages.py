#!/usr/bin/env python3
"""
MimePy — Prepara a saída para GitHub Pages (N23, deploy completo).

Monta o diretório `_site/` na RAIZ do repositório com a estrutura final que o
GitHub Pages serve, de forma que TODOS os links internos funcionem online:

    _site/
      index.html            <- pagina principal (landing: site/index.html)  [home]
      docs/index.html       <- documentacao geral (index.html da raiz)
      examples/...          <- exemplos e templates (de examples/*/out/*.html)
      sitemap.xml           <- p/ SEO
      robots.txt            <- autoriza rastreadores
      404.html              <- fallback amigavel

Uso:
    python scripts/deploy_pages.py site/config.site.py
    # -> monta _site/ com a landing na raiz + doc + exemplos + auxiliares.
    # Em CI (workflow pages), este script roda ANTES do upload-pages-artifact
    # (path: _site).

Por que montar o _site no deploy (e nao apenas copiar a landing)?
- O GitHub Pages serve a partir da raiz configurada. Se publicarmos apenas a
  landing, os links para as outras paginas (doc, exemplos, templates) QUEBRAM.
- Montando a arvore completa, cada link relativo (docs/, examples/, ...) resolve
  para o arquivo correspondente dentro do proprio site.
- Mantem offline/1-arquivo por pagina e 0 dependencia alem de `markdown`.
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUILD = REPO / "src" / "build.py"
SITE = "_site"


def _build(config_path):
    """Garante que o HTML do config esteja atual (roda o motor build.py)."""
    subprocess.run([sys.executable, str(BUILD), str(config_path)], check=True)


def go(config_path):
    cfg_path = Path(config_path).resolve()
    deploy = cfg_path.parent                      # pasta do config (ex.: site/)
    _build(cfg_path)                              # atualiza a landing em deploy/

    site_root = REPO / SITE
    if site_root.exists():
        shutil.rmtree(site_root)                  # limpa antes de reconstruir
    site_root.mkdir(parents=True)

    # 1) Home = landing principal (site/index.html)
    landing = deploy / "index.html"
    shutil.copy2(landing, site_root / "index.html")

    # 2) Documentacao geral = index.html da raiz do repo -> _site/docs/
    (site_root / "docs").mkdir()
    raiz_doc = REPO / "index.html"
    if raiz_doc.exists():
        shutil.copy2(raiz_doc, site_root / "docs" / "index.html")

    # 3) Exemplos e templates: examples/**/out/<arquivo>.html -> _site/examples/<X>/...
    ex_src = REPO / "examples"
    if ex_src.exists():
        for out in ex_src.rglob("out"):
            if not out.is_dir():
                continue
            rel_out = out.relative_to(ex_src)         # ex.: landing/out ou templates/startup/out
            for f in out.glob("*.html"):
                dst = site_root / "examples" / rel_out / f.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)

    # 4) sitemap.xml + robots.txt + 404.html (na raiz do _site)
    base_url = "/"
    (site_root / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{base_url}</loc><priority>1.0</priority></url>\n'
        '</urlset>\n', encoding="utf-8")
    (site_root / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: %s\n" % (base_url + "sitemap.xml"),
        encoding="utf-8")
    (site_root / "404.html").write_text(
        "<!DOCTYPE html>\n<html lang=\"pt-BR\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>404 - Pagina nao encontrada</title>"
        "<style>body{font-family:system-ui,sans-serif;background:#0b1220;color:#e2e8f0;"
        "display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center;}"
        "a{color:#2dd4bf;}</style></head>"
        "<body><div><h1>404</h1><p>Pagina nao encontrada.</p>"
        f"<p><a href=\"{base_url}\">Voltar ao inicio</a>.</p>"
        "</div></body></html>\n", encoding="utf-8")

    # Resumo
    n = len(list(site_root.rglob("*.html")))
    print(f"[deploy] _site montado com {n} paginas HTML em {site_root}")
    print("[deploy] home: /  · doc: /docs/  · exemplos: /examples/  "
          "· + sitemap/robots/404")


if __name__ == "__main__":
    go(sys.argv[1] if len(sys.argv) > 1 else str(REPO / "site/config.site.py"))
