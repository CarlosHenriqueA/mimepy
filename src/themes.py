#!/usr/bin/env python3
"""
MimePy v0.4 — themes.py (temas CSS y lógica de selección)
================================================================
Contiene los temas del framework (light / dark / neon / paper / mono) como
bloques CSS variables, y la función que decide qué tema aplica según el config.

Separado del motor (build.py) para:
- testing unitario aislado (temas son datos puros + 1 función).
- reutilización: `export_tokens.py` y futura tooling consumen los tokens.
- mantenibilidad: agregar un tema = 1 bloque CSS + 1 rama aquí.

Uso:
    from themes import get_theme_css
    css_extra, default_theme = get_theme_css(cfg)
    # -> css_extra = CSS del tema elegido ('' para light)
    # -> default_theme = 'light'|'dark'|'neon'|'paper'|'mono'
"""

# ---------------------------------------------------------------- temas (CSS variables)
# Cada tema redirige las variables que el style.css de la doc consume.
# dark/neon modifican la base OSCURA (alternativas a light).
# paper/mono son temas de fondo propios (claro/oscuro en la sidebar).
THEMES_CSS = {
    "dark": """
[data-theme="dark"]{
  --bg:#0f172a; --fg:#e2e8f0; --muted:#94a3b8;
  --accent:#2dd4bf; --accent2:#5eead4; --cta:#fbbf24; --cta-strong:#f59e0b;
  --border:#1e293b; --code-bg:#1e293b; --note-bg:#134e4a; --note-border:#2dd4bf;
  --sidebar-bg:#020617; --sidebar-fg:#cbd5e1; --pre-bg:#0b1220; --pre-fg:#e2e8f0;
  --tool-bg:#0f172a; --input-bg:#0f172a;
}
""",
    "neon": """
[data-theme="neon"]{
  --bg:#0a0a0f; --fg:#f0f0ff; --muted:#a5a5c0;
  --accent:#00ffd5; --accent2:#00e0ff; --cta:#ff2e88; --cta-strong:#ff1177;
  --border:#2a2a4a; --code-bg:#12122a; --note-bg:#0f0f24; --note-border:#ff2e88;
  --sidebar-bg:#05050a; --sidebar-fg:#d5d5ff; --pre-bg:#0a0a1e; --pre-fg:#e0e0ff;
  --tool-bg:#12122a; --input-bg:#0a0a1e;
}
a{color:#7df9ff;}
""",
    # "paper": tema claro estilo impreso (marca esverdeada suave). Base CLARA.
    "paper": """
html[data-theme="paper"]{
  --bg:#fdfcf7; --fg:#2b2b2b; --muted:#6b7280;
  --accent:#15803d; --accent2:#166534; --cta:#b45309; --cta-strong:#92400e;
  --border:#e5e4db; --code-bg:#f4f3ec; --note-bg:#eef7ee; --note-border:#86c79a;
  --sidebar-bg:#f4f3ec; --sidebar-fg:#333; --pre-bg:#f4f3ec; --pre-fg:#2b2b2b;
  --tool-bg:#eceae0; --input-bg:#fff;
}
[data-theme="paper"] .sidebar{color:#333;}
[data-theme="paper"] .brand{color:#166534;}
""",
    # "mono": monocromático (tonos de gris/negro), visual técnico/minimalista. Base CLARA.
    "mono": """
html[data-theme="mono"]{
  --bg:#fafafa; --fg:#111; --muted:#525252;
  --accent:#111; --accent2:#333; --cta:#111; --cta-strong:#000;
  --border:#d4d4d4; --code-bg:#f2f2f2; --note-bg:#f2f2f2; --note-border:#a3a3a3;
  --sidebar-bg:#111; --sidebar-fg:#e5e5e5; --pre-bg:#111; --pre-fg:#e5e5e5;
  --tool-bg:#262626; --input-bg:#e5e5e5;
}
[data-theme="mono"] .sidebar nav a{color:#a3a3a3;}
[data-theme="mono"] h1{border-bottom-color:#111;}
""",
}

# Temas de fondo propio (oscuros o paper/mono) que sobreescriben el :root;
# la base LIGHT usa el CSS del style.css sin extras.
_BASE_LIGHT = "light"


def get_theme_css(cfg):
    """Retorna (css_extra, default_theme) según el config.

    - theme='light'  -> ('', 'light')
    - theme='dark'   -> (css dark, 'dark')
    - theme='neon'   -> (css dark + neon, 'dark')  (neon fuerza base oscura)
    - theme='paper'  -> (css paper, 'paper')
    - theme='mono'   -> (css mono, 'mono')
    - valor inválido -> ('', 'light')  (normaliza, no rompe el build)
    """
    theme = (cfg.get("theme") or _BASE_LIGHT).lower()
    extra = []
    if theme == "dark":
        extra.append(THEMES_CSS["dark"])
        default_theme = "dark"
    elif theme == "neon":
        extra.append(THEMES_CSS["dark"])     # neon también fuerza base oscura
        extra.append(THEMES_CSS["neon"])
        default_theme = "dark"
    elif theme == "paper":
        extra.append(THEMES_CSS["paper"])
        default_theme = "paper"
    elif theme == "mono":
        extra.append(THEMES_CSS["mono"])
        default_theme = "mono"
    else:
        default_theme = _BASE_LIGHT          # light (padrão) o inválido
    return "\n".join(extra), default_theme


def available_themes():
    """Lista de temas disponibles (para docs/CLI)."""
    return sorted(THEMES_CSS.keys()) + [_BASE_LIGHT]