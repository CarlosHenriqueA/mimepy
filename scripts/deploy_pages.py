#!/usr/bin/env python3
"""
MimePy — Prepara saída para GitHub Pages (N23).

Gera, dentro de <out_dir>, os arquivos extras que um site estático
publicável precisa além do index.html:
  - sitemap.xml        (lista de páginas p/ SEO)
  - 404.html           (fallback amigável p/ rotas inexistentes)
  - robots.txt         (autoriza rastreadores)

Uso:
    python scripts/deploy_pages.py site/config.site.py
    # -> gera site/out/sitemap.xml, 404.html, robots.txt + index.html (já existente)

Como funciona: roda o build do config dado (para garantir o index.html atual),
depois grava os arquivos auxiliares no mesmo out_dir.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUILD = REPO / "src" / "build.py"
sys.path.insert(0, str(REPO / "src"))


def go(config_path):
    import importlib.util
    import subprocess

    cfg_path = Path(config_path).resolve()
    # 1) garante o index.html atual (via build.py)
    subprocess.run([sys.executable, str(BUILD), str(cfg_path)], check=True)

    # 2) lê o config para saber o out_dir
    spec = importlib.util.spec_from_file_location("mimepy_cfg", cfg_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cfg = mod.PROJECT
    out = (cfg_path.parent / cfg["out_dir"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    site_name = cfg.get("name", "MimePy")
    base_url = cfg.get("base_url", "/")

    # 3) sitemap.xml — assume index.html como página principal
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{base_url}</loc><priority>1.0</priority></url>\n'
        '</urlset>\n', encoding="utf-8")

    # 4) robots.txt
    (out / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: %s\n" % (base_url + "sitemap.xml"),
        encoding="utf-8")

    # 5) 404.html — fallback amigável (estilo do framework)
    (out / "404.html").write_text(
        "<!DOCTYPE html>\n<html lang=\"pt-BR\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>404 — Página não encontrada</title>"
        "<style>body{font-family:system-ui,sans-serif;background:#0b1220;color:#e2e8f0;"
        "display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center;}"
        "a{color:#2dd4bf;}code{background:#1e293b;padding:2px 6px;border-radius:4px;}</style></head>"
        "<body><div><h1>404</h1><p>Página não encontrada.</p>"
        f"<p>Volte ao <a href=\"{base_url}\">início de {site_name}</a>.</p>"
        "<p><small>Gerado com MimePy · GPL-2.0</small></p></div></body></html>\n",
        encoding="utf-8")

    print("[deploy] sitemap.xml, robots.txt e 404.html gerados em", out)


if __name__ == "__main__":
    go(sys.argv[1] if len(sys.argv) > 1 else str(REPO / "site/config.site.py"))
