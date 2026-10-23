"""Testes de CLI (src/cli.py) + temas (src/themes.py) + modo blog (v0.4).

Cobre os recursos que antes não tinham teste: init/build do CLI, temas
papel/mono/neon, e o modo blog. Complementa test_build.py / test_security.py.
"""
import os
import subprocess
import sys
from pathlib import Path

import build
import themes

REPO = Path(__file__).resolve().parent.parent
CLI = REPO / "src" / "cli.py"
PY = sys.executable


# ---------------- temas ----------------
def test_themes_available():
    t = themes.available_themes()
    assert set(t) == {"light", "dark", "neon", "paper", "mono"}


def test_theme_paper_default():
    css, dt = themes.get_theme_css({"theme": "paper"})
    assert dt == "paper" and "data-theme=\"paper\"" in css


def test_theme_invalido_normaliza_light():
    css, dt = themes.get_theme_css({"theme": "roxo-vibecoding"})
    assert dt == "light" and css == ""


def test_theme_neon_forca_dark():
    css, dt = themes.get_theme_css({"theme": "neon"})
    assert dt == "dark" and "data-theme=\"neon\"" in css


# ---------------- CLI ----------------
def test_cli_help():
    r = subprocess.run([PY, str(CLI), "--help"], capture_output=True, text=True)
    assert r.returncode == 0
    assert "build" in r.stdout and "init" in r.stdout


def test_cli_build_mostra_watch():
    r = subprocess.run([PY, str(CLI), "build", "--help"],
                       capture_output=True, text=True)
    assert "--watch" in r.stdout


def test_cli_init_docs(tmp_path):
    dest = tmp_path / "novo"
    r = subprocess.run([PY, str(CLI), "init", "meuproj", "-d", str(dest)],
                       capture_output=True, text=True)
    assert r.returncode == 0
    cfg = dest / "meuproj" / "config.py"
    docs = dest / "meuproj" / "docs" / "README.md"
    assert cfg.exists() and docs.exists()
    assert "meuproj" in cfg.read_text(encoding="utf-8")


def test_cli_init_landing(tmp_path):
    dest = tmp_path / "n2"
    r = subprocess.run([PY, str(CLI), "init", "ap", "-d", str(dest),
                        "--template", "landing"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    cfg = dest / "ap" / "config.py"
    assert cfg.exists()
    assert "mode" in cfg.read_text(encoding="utf-8")


def test_cli_init_nome_invalido():
    r = subprocess.run([PY, str(CLI), "init", ""], capture_output=True, text=True)
    assert r.returncode != 0


# ---------------- modo blog ----------------
def test_build_blog_gera_posts(tmp_path):
    bdir = tmp_path / "blog"; bdir.mkdir()
    (bdir / "p1.md").write_text(
        "---\ntitle: Primeiro\ndate: 2026-08-04\n---\n\nConteudo 1.",
        encoding="utf-8")
    (bdir / "p2.md").write_text(
        "---\ntitle: Segundo\ndate: 2026-08-01\n---\n\nConteudo 2.",
        encoding="utf-8")
    cfg = {"mode": "blog", "blog_dir": "blog", "name": "B",
           "page_title": "Blog", "out_dir": ".", "out_file": "i.html"}
    out = build.build_blog(cfg, tmp_path)
    txt = out.read_text(encoding="utf-8")
    assert txt.count("class=\"post\"") == 2
    # mais recente primeiro (Primeiro=08-04 vem antes de Segundo=08-01)
    assert txt.find("Primeiro") < txt.find("Segundo")


def test_build_blog_vazio(tmp_path):
    cfg = {"mode": "blog", "blog_dir": "nao-Existe", "name": "B",
           "page_title": "B", "out_dir": ".", "out_file": "i.html"}
    out = build.build_blog(cfg, tmp_path)
    assert "Sem posts" in out.read_text(encoding="utf-8")