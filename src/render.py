#!/usr/bin/env python3
"""
MimePy v0.4 — render.py (conversión Markdown → HTML + frontmatter)
==================================================================
Aísla la transformación de Markdown (usando la única dependencia `markdown`)
y la extracción de frontmatter YAML (title/description/order).

Separado del motor para testing y para que otras tooling (blog, CLI) puedan
reutilizarlo. Compat: `render_md(path, extensions) -> (html, meta)`.
"""
import re

import markdown

# extensiones por defecto — cubren el Markdown "GitBook-like" del framework
_DEFAULT_EXT = ["tables", "fenced_code", "sane_lists", "md_in_html",
                "attr_list", "def_list"]


def parse_frontmatter(md):
    """Extrae un bloque `--- ... ---` inicial y devuelve (metadata, cuerpo).

    - metadata: dict con claves lower-case de title/description/order data.
    - cuerpo: el Markdown restante (sin el bloque).
    Soporta valores simples (`clave: valor`) con o sin comillas.
    """
    meta = {}
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", md, flags=re.S)
    if fm:
        for line in fm.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")
        md = md[fm.end():]                # descarta el bloque del cuerpo
    return meta, md


def _robust_tables(md):
    """Garantiza línea en blanco antes del separador de tabla cuando es necesario.

    Solo cuando una línea separador (|---|) viene tras un PARÁGRAFO suelto
    (sin '|') y no tras otro header de tabla. Mejora la fidelidad.
    """
    return re.sub(
        r"(?m)^(?P<prev>[^\n|][^\n]*)\n(?P<sep>\|[^\n]*\|[\s:|:-]*\|\s*)$",
        lambda m: m.group("prev") + "\n\n" + m.group("sep"),
        md,
    )


def render_md(path, extensions):
    """Convierte un archivo .md en (html, meta).

    - html: el Markdown renderizado (tablas robustas, code fences, etc.)
    - meta: frontmatter (title/description/order) si existía.
    """
    with open(path, encoding="utf-8") as f:
        md = f.read()

    meta, md = parse_frontmatter(md)
    md = _robust_tables(md)
    html = markdown.markdown(md, extensions=extensions or _DEFAULT_EXT)
    return html, meta


def render_md_text(text, extensions=None):
    """Variante sin archivo: convierte un string Markdown y devuelve solo html."""
    meta, md = parse_frontmatter(text or "")
    md = _robust_tables(md)
    return markdown.markdown(md, extensions=extensions or _DEFAULT_EXT)