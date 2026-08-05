#!/usr/bin/env python3
"""
MimePy — Gera PDF a partir do MESMO config do HTML (M11).

Uso:
    python scripts/gen_pdf.py                     # usa config.py (raiz)
    python scripts/gen_pdf.py caminho/config.py   # usa outro config

Como funciona:
  1. Roda o build (src/build.py <config>) para gerar o HTML.
  2. Tenta converter para PDF com o motor disponível, em ordem:
       a) navegador headless (Chrome/Edge, via --headless --print-to-pdf)
          → melhor fidelidade (honra @media print do MimePy).
       b) WeasyPrint, se instalado (pip install weasyprint).
  3. Se nenhum motor existir, imprime instrução clara para salvar PDF via
     Ctrl+P no navegador (o @media print do MimePy já deixa tudo limpo).

Saída: <out_dir>/<out_file>.pdf (mesmo config).

Honestidade: o MimePy mantém 1 dependência (markdown). PDF é OPCIONAL e usa
um motor que já exista na máquina (headless Chrome/Edge ou weasyprint).
"""
import os
import re
import shutil
import subprocess
import sys
import importlib.util
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parent.parent
VERSION = "0.2"


def load_config(config_path):
    spec = importlib.util.spec_from_file_location("mimepy_cfg", config_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PROJECT


def find_local_html(html_path, config_path):
    """Gera o HTML via build e localiza o index.html do config."""
    r = subprocess.run([sys.executable,
                        str(FRAMEWORK / "src" / "build.py"),
                        str(config_path)],
                       capture_output=True, text=True, cwd=str(FRAMEWORK))
    if r.returncode != 0:
        print("Erro no build:", r.stderr[-500:]); sys.exit(1)
    m = re.search(r"OK ->\s*(.+)", r.stdout)
    if m:
        return m.group(1).strip()
    return str(html_path)


def find_browser():
    """Procura um navegador headless (Chrome/Edge) para exportar PDF."""
    for exe in [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ]:
        if os.path.exists(exe):
            return exe
    # fallback: procurar no PATH
    return shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("msedge")


def main():
    cfg_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (FRAMEWORK / "config.py")
    if not cfg_path.exists():
        print("config não encontrado:", cfg_path); sys.exit(1)

    cfg = load_config(cfg_path)
    out_dir = (cfg_path.parent / cfg["out_dir"]).resolve()
    out_html = out_dir / cfg["out_file"]
    out_pdf = out_dir / (cfg["out_file"] + ".pdf")

    print(f"[MimePy {VERSION}] Gerando HTML (config {cfg_path.name})...")
    html_file = Path(find_local_html(out_html, cfg_path))
    print("  HTML:", html_file)

    # (a) navegador headless
    browser = find_browser()
    if browser:
        print("  Motor: navegador headless")
        cmd = [browser, "--headless", "--disable-gpu",
               "--print-to-pdf=" + str(out_pdf),
               "file:///" + str(html_file).replace("\\", "/")]
        subprocess.run(cmd, capture_output=True)
        if out_pdf.exists() and out_pdf.stat().st_size > 0:
            print(f"  PDF OK -> {out_pdf} ({out_pdf.stat().st_size} bytes)")
            return
        print("  (headless não gerou; tentando weasyprint)")

    # (b) WeasyPrint (opcional)
    try:
        import weasyprint
        print("  Motor: weasyprint")
        weasyprint.HTML(filename=str(html_file)).write_pdf(str(out_pdf))
        print(f"  PDF OK -> {out_pdf} ({out_pdf.stat().st_size} bytes)")
    except ImportError:
        print("  Nenhum motor de PDF instalado (headless ou weasyprint).")
        print("  Dica: abra o HTML no navegador e use Ctrl+P -> 'Salvar como PDF'.")
        print("  (o @media print do MimePy já deixa a página limpa p/ isso)")
    except Exception as e:
        print("  Erro no weasyprint:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
