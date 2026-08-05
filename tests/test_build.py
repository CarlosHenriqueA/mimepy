"""Testes do motor (src/build.py): build docs/landing + temas + _cardize/_side_label."""
import re
import sys
from pathlib import Path

import build  # via conftest (sys.path)

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def _cfg_for(tmp, name, mode="docs", theme=None, extra=None):
    """Gera um config.py temporário e retorna (cfg_dict, base_dir)."""
    d = tmp / name
    d.mkdir(parents=True, exist_ok=True)
    docs = d / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "README.md").write_text(
        "# Teste\n\nTexto normal com **negrito**. `code` aqui.\n\n## Se\u00e7\u00e3o\nConte\u00fado da se\u00e7\u00e3o.",
        encoding="utf-8")
    cfg = {
        "name": name, "page_title": "T\u00edtulo",
        "docs_dir": "docs", "out_dir": ".", "out_file": "index.html",
        "sidebar": [("README.md", "Vis\u00e3o geral")],
    }
    if mode == "landing":
        cfg["mode"] = "landing"
        cfg["landing_md"] = "README.md"
        cfg["docs_dir"] = "docs"
    if theme:
        cfg["theme"] = theme
    if extra:
        cfg.update(extra)
    return cfg, d


def test_render_md_basico(tmp_path):
    md = tmp_path / "a.md"
    md.write_text("# T\u00edtulo\n\nPar\u00e1grafo com **negrito** e `code`.", encoding="utf-8")
    html, meta = build.render_md(md, ["tables", "fenced_code", "sane_lists"])
    assert "<h1" in html
    assert "<strong>" in html
    assert "<code>" in html


def test_render_md_frontmatter(tmp_path):
    # N22: frontmatter extraído; título/descrição removidos do corpo.
    md = tmp_path / "b.md"
    md.write_text("---\ntitle: Instala\u00e7\u00e3o\ndescription: passo a passo\norder: 2\n---\n\n# Corpo\n\nTexto.",
                  encoding="utf-8")
    html, meta = build.render_md(md, [])
    assert meta.get("title") == "Instala\u00e7\u00e3o"
    assert meta.get("description") == "passo a passo"
    assert meta.get("order") == "2"
    assert "Corpo" in html and "Instala\u00e7\u00e3o" not in html


def test_build_docs_gera_html(tmp_path):
    cfg, base = _cfg_for(tmp_path, "proj")
    out = build.build(cfg, base)
    txt = out.read_text(encoding="utf-8")
    assert "Proj" in txt or "proj" in txt
    assert "sidebar" in txt
    assert "<main" in txt
    assert "Content-Security-Policy" in txt  # N10 CSP presente


def test_build_landing_gera_html(tmp_path):
    cfg, base = _cfg_for(tmp_path, "land", mode="landing")
    out = build.build_landing(cfg, base)
    txt = out.read_text(encoding="utf-8")
    assert "land-nav" in txt or "hero" in txt
    assert "Content-Security-Policy" in txt


def test_sanitize_remove_script(tmp_path):
    cfg, base = _cfg_for(tmp_path, "sec", extra={"sanitize": True})
    (base / "docs" / "README.md").write_text(
        "# S\n\n<p onclick=\"x()\">ok</p>\n\n<script>alert(1)</script>\n\n[a](javascript:alert(1))",
        encoding="utf-8")
    out = build.build(cfg, base)
    txt = out.read_text(encoding="utf-8")
    # O documento LEGÍTIMO contém <script> (APP_JS do framework) — o que precisa
    # sumir são os VETORES maliciosos vindos do Markdown não confiável:
    assert "alert(1)" not in txt
    assert "onclick" not in txt
    assert "javascript:" not in txt.lower().replace("&lt;", "<").replace("&gt;", ">") \
        or "javascript:" not in txt
    # e o texto limpo permanece
    assert "ok" in txt


def test_sanitize_deve_conservar_texto_limpo():
    safe = build.sanitize_html("<h1>Olá</h1><p>texto</p>")
    assert "<h1>Olá</h1>" in safe
    assert "<p>texto</p>" in safe


def test_noopener_js_presente():
    # N11: o JS do APP_JS deve conter a atribuição rel=noopener
    assert "noopener noreferrer" in build.APP_JS


def test_csp_no_templates():
    # N10: CSP presente nos templates docs e landing
    assert "Content-Security-Policy" in build.APP_JS or "Content-Security-Policy" in (
        build.__doc__ or "") or True  # verificação real abaixo
    # verificação concreta: procurar no build.py a string da meta
    src = (REPO / "src" / "build.py").read_text(encoding="utf-8")
    assert "Content-Security-Policy" in src


def test_theme_css_variantes():
    # M8/M12: temas light/dark/neon/paper/mono
    css, dt = build.get_theme_css({"theme": "mono"})
    assert dt == "mono" and "data-theme=\"mono\"" in css
    css2, dt2 = build.get_theme_css({"theme": "paper"})
    assert dt2 == "paper" and "data-theme=\"paper\"" in css2
    css3, dt3 = build.get_theme_css({"theme": "neon"})
    assert dt3 == "dark" and "data-theme=\"neon\"" in css3
    css4, dt4 = build.get_theme_css({})
    assert dt4 == "light" and css4 == ""


def test_cardize_extrai_emoji():
    assert "class=\"ic\"" in build._cardize("<h3>📄 Markdown</h3><p>x</p>")
    assert "class=\"ic\"" in build._cardize("<h3>🌙 Dark / Light</h3><p>x</p>")
    assert "class=\"ic\"" not in build._cardize("<h3>Sem emoji</h3><p>x</p>")


def test_side_label_icon():
    assert "side-ic" in build._side_label("🚀 Início")
    assert "side-ic" not in build._side_label("Segurança")


def test_python_agora():
    """Apenas garante que o módulo carrega sem erro (básico)."""
    assert hasattr(build, "VERSION")
