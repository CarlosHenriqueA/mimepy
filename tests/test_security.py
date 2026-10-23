"""Testes de segurança (v0.4): sanitizador por parser real (src/security.py).

Valida o endurecimento contra os vetores XSS mais comuns e garante que o
sanitize não destrói conteúdo legítimo (sem falso-positivo).
"""
import sys
import subprocess
from pathlib import Path

import security  # via conftest (sys.path inclui src/)

REPO = Path(__file__).resolve().parent.parent


def _san(text):
    return security.sanitize_html(text)


# ---------------- vetores que DEVEM ser neutralizados ----------------
def test_remove_script_tag():
    assert _san("<script>alert(1)</script><p>ok</p>") == "<p>ok</p>"


def test_remove_script_malformado():
    # <SCRIPT com variantes de caixa e atributos
    r = _san("<SCRIPT SRC='x'></SCRIPT>ok")
    assert "SCRIPT" not in r and "ok" in r


def test_remove_style_tag():
    assert _san("<style>body{}</style>") == ""


def test_remove_iframe():
    assert _san("<iframe src='https://evil'></iframe>x") == "x"


def test_remove_form_input():
    assert _san("<form action='x'><input name='a'></form>t") == "t"


def test_remove_object_embed_link():
    for tag in ("object", "embed", "link", "base", "meta"):
        r = _san("<%s>corpo</%s>x" % (tag, tag))
        assert tag not in r.lower(), tag


def test_remove_onclick_attribute():
    assert _san("<p onclick=\"alert(1)\">texto</p>") == "<p>texto</p>"


def test_remove_onerror():
    assert _san('<img src="x.png" onerror="alert(1)">') == '<img src="x.png">'


def test_block_javascript_href():
    assert _san('<a href="javascript:alert(1)">x</a>') == "<a>x</a>"


def test_block_javascript_obfuscado():
    # java\tscript: com espaços inseridos no meio
    r = _san('<a href="java\\tscript:alert(1)">x</a>')
    assert "javascript" not in r.lower()


def test_block_data_img():
    assert _san('<img src="data:text/html;base64,xyz">x') == "x"


def test_block_style_url():
    assert _san('<div style="background:url(javascript:x)">a</div>') == "<div>a</div>"


def test_block_style_import():
    assert _san('<div style="@import url(x)">a</div>') == "<div>a</div>"


def test_remove_svg_math():
    for tag in ("svg", "math"):
        r = _san("<%s>onload=alert(1)</%s>ok" % (tag, tag))
        assert tag not in r.lower(), tag
        assert "ok" in r


# ---------------- conteúdo legítimo que DEVE sobreviver ----------------
def test_preserva_texto_formatado():
    r = _san("<h1>Oi</h1><p><strong>negrito</strong> e <em>italico</em>.</p>")
    assert "<h1>Oi</h1>" in r and "<strong>negrito</strong>" in r


def test_preserva_link_https():
    assert _san('<a href="https://ok.com" target="_blank">l</a>') == \
        '<a href="https://ok.com" target="_blank">l</a>'


def test_preserva_mailto():
    assert "mailto:" in _san('<a href="mailto:oi@x.com">mail</a>')


def test_preserva_ancora_interna():
    assert _san('<a href="#secao">ancora</a>') == '<a href="#secao">ancora</a>'


def test_preserva_code_com_linguagem():
    # a classe language-* é necessária para o highlight funcionar
    assert _san('<code class="language-python">x=1</code>') == \
        '<code class="language-python">x=1</code>'


def test_preserva_tabela():
    r = _san("<table><tr><td>a</td></tr></table>")
    assert "<table>" in r and "<td>a</td>" in r


def test_escapa_texto_com_especiais():
    assert _san("<p>a < b & c</p>") == "<p>a &lt; b &amp; c</p>"


# ---------------- integração com o motor ----------------
def test_build_com_sanitize_remove_xss(tmp_path):
    import build
    d = tmp_path / "p"; (d / "docs").mkdir(parents=True)
    (d / "docs" / "a.md").write_text(
        "# A\n\n<script>alert(1)</script>\n\n<p onclick=\"x()\">ok</p>",
        encoding="utf-8")
    cfg = {"name": "X", "page_title": "X", "docs_dir": "docs",
           "out_dir": ".", "out_file": "i.html",
           "sidebar": [("a.md", "A")], "sanitize": True}
    out = build.build(cfg, d)
    txt = out.read_text(encoding="utf-8")
    assert "alert(1)" not in txt
    assert "onclick" not in txt