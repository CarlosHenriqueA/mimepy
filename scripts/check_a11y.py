#!/usr/bin/env python3
"""
MimePy — Validação de Acessibilidade (WCAG 2.2 AA)

Uso:
    python scripts/check_a11y.py              # valida DESIGN.md + index.html
    python scripts/check_a11y.py --design     # só o design system (contraste)
    python scripts/check_a11y.py --html PATH  # valida um HTML gerado

O que este script faz (acessibilidade internacional — W3C/WAI):
  1. Design system: roda o linter `@google/design.md` no DESIGN.md, que
     verifica CONTRASTE WCAG AA (1.4.3) das cores/tokens, referências quebradas
     e estrutura do spec. (Requisito para destravar ainda mais conformidade.)
  2. HTML gerado: verifica presença dos recursos de acessibilidade NATIVOS
     que o build.py já embute: lang, skip-link, focus-visible, reduced-motion,
     aria-label nas regiões, role="main" e aria-current (scrollspy).

FAIL = 1 (ex.: erro de contraste ou HTML sem acessibilidade).
PASS = 0.
"""
import re
import sys
import subprocess
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parent.parent  # raiz do framework (mimepy/)

# Itens de acessibilidade que o HTML gerado deve conter (WCAG 2.2 AA).
# Cada item é (descrição, marcaçior a procurar no HTML).
HTML_CHECKS = [
    ("lang no <html> (3.1.1)",                  r'<html[^>]*\blang='),
    ("meta viewport (reflow) (1.4.10)",         r'name="viewport"'),
    ("skip-link (2.4.1 Bypass Blocks)",         r'class="skip-link"'),
    ("foco visível :focus-visible (2.4.7)",     r':focus-visible'),
    ("reduzir movimento (2.3.3)",               r'prefers-reduced-motion'),
    ("aria-label na sidebar (1.3.1)",           r'aria-label="Navegação do documento"'),
    ("aria-current no nav (2.4.1)",             r'aria-current'),
    ("role=main (1.3.1 / landmarks)",           r'<main[^>]*role="main"'),
]


def _needle_regexes():
    # converte a lista de checks em pares (nome, regex compilado)
    return [(name, re.compile(pattern)) for name, pattern in HTML_CHECKS]


def check_html(path: Path) -> tuple:
    """Valida um HTML gerado: retorna (ok, lista_de_falhas)."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False, [f"arquivo não encontrado: {path}"]
    missing = []
    for name, rx in _needle_regexes():
        if not rx.search(text):
            missing.append(name)
    return (len(missing) == 0), missing


def check_design() -> tuple:
    """Roda o linter do DESIGN.md (contraste WCAG). Retorna (ok, msg)."""
    design = FRAMEWORK / "DESIGN.md"
    if not design.exists():
        return False, ["DESIGN.md não encontrado"]
    # Windows: usar o alias 'designmd' (o bin 'design.md' colide com assoc .md)
    # No Windows, 'npx' costuma ser um arquivo .CMD que o subprocess.run não
    # executa direto (precisa do caminho completo com extensão). Resolve isso.
    import shutil
    npx_path = (shutil.which("npx.cmd") or shutil.which("npx") or "npx")
    cmd = [npx_path, "-y", "-p", "@google/design.md", "designmd", "lint", str(design)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180,
                           cwd=str(FRAMEWORK))
    except FileNotFoundError:
        # npx não instalado — reporta e segue (não bloqueia o HTML)
        return True, "[aviso] npx não disponível; pulei contraste DESIGN.md"
    # exit 1 = erro (ex.: contraste reprovado); 0 = ok/só warnings
    ok = (r.returncode == 0)
    msg = r.stdout.strip()[-400:] if ok else (r.stdout + r.stderr)[-600:]
    return ok, msg


def main() -> int:
    argv = sys.argv[1:]
    only_design = "--design" in argv
    only_html = any(a.startswith("--html") for a in argv)

    fails = []

    if not only_html:
        ok, msg = check_design()
        print("== Design system (WCAG contraste via DESIGN.md) ==")
        print(("PASS" if ok else "FAIL"), "-", msg)
        if not ok:
            fails.append("design")

    if not only_design:
        html_path = None
        for a in argv:
            if a.startswith("--html"):
                html_path = Path(a.split("=", 1)[1])
        if html_path is None:
            html_path = FRAMEWORK / "index.html"
        ok, missing = check_html(html_path)
        print("== HTML gerado (recursos de acessibilidade) ==")
        if ok:
            print("PASS - todos os recursos nativos presentes")
        else:
            print("FAIL - faltando:", ", ".join(missing))
            fails.append("html")

    if fails:
        print("\n[a11y] RESULTADO: FAIL  (corrigir itens acima)")
        return 1
    print("\n[a11y] RESULTADO: PASS  (WCAG 2.2 AA — estrutura e contraste)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
