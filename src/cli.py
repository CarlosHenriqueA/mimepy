#!/usr/bin/env python3
"""
MimePy — CLI (interface de linha de comando).

Comandos:
  python src/cli.py build [config.py]   Gera o HTML a partir de um config
                                        (padrão: config.py na raiz do framework)
  python src/cli.py init <nome> [-d DIR] [--template docs|landing]
                                        Cria um novo projeto MimePy (config +
                                        pasta docs) a partir de um modelo.

Objetivo (N3): democratizar o uso — não-devs criam e constroem sem tocar
no motor. Mantém a única dependência (markdown) e o HTML 1-arquivo offline.

Uso típico:
  $ python src/cli.py init meu-projeto
  $ cd meu-projeto && python <caminho>/src/cli.py build config.py
"""
import shutil
import sys
import argparse
import time
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parent.parent
BUILD = FRAMEWORK / "src" / "build.py"
EXAMPLES = FRAMEWORK / "examples" / "templates"


def cmd_build(config_path, watch=False):
    """Comando `build`: gera o HTML de um config.

    - `watch=False` (padrão): roda o build.py uma vez e encerra.
    - `watch=True` (N21): fica observando mudanças nos `.md`/`.py` do diretório
      do config e rebuilda automaticamente (modo dev).
    """
    import subprocess
    cfg = Path(config_path).resolve()
    if not cfg.exists():
        print("❌ config não encontrado:", cfg)
        sys.exit(1)

    # _run: executa o motor build.py apontando para o config (subprocess limpo).
    def _run():
        subprocess.run([sys.executable, str(BUILD), str(cfg)])

    if not watch:
        _run()
        sys.exit(0)

    # N21: --watch — rebuild automático ao salvar .md/.py no projeto do config.
    print("👀 Observando mudanças (Ctrl+C para sair)...")
    _run()
    # watch_dir = pasta do config (onde estão os .md do projeto).
    watch_dir = cfg.parent.resolve()
    # _snapshot: mapeia arquivo -> mtime (p/ detectar mudanças por polling).
    def _snapshot():
        import os
        snap = {}
        for root, _dirs, files in os.walk(watch_dir):
            if "__pycache__" in root or "out" in root:
                continue
            for f in files:
                if f.endswith((".md", ".py")):
                    p = os.path.join(root, f)
                    snap[p] = os.path.getmtime(p)
        return snap
    base_snap = _snapshot()
    while True:
        time.sleep(1.0)
        cur = _snapshot()
        changed = [k for k in cur if cur.get(k) != base_snap.get(k)]
        # detecta novos arquivos também
        if cur != base_snap:
            print("🔄 Mudança detectada, rebuildando...")
            _run()
            base_snap = cur


def cmd_init(name, dest, template):
    """Cria um novo projeto: pasta + config.py + docs/ (mode docs) ou LANDING.md."""
    if not name or name.strip() in ("", "."):
        print("nome do projeto obrigatório: mimepy init <nome>")
        sys.exit(1)
    target = (Path(dest) / name).resolve() if dest else (Path(dest or ".") / name).resolve()
    target = target if target.suffix == "" else target
    if target.exists() and any(target.iterdir()):
        print("❌ pasta já existe e não está vazia:", target)
        sys.exit(1)
    target.mkdir(parents=True, exist_ok=True)

    template = (template or "docs").lower()
    if template == "landing":
        # cópia do template "produto" como base landing
        base = EXAMPLES / "produto"
        if base.exists():
            (base / "config.py").read_text(encoding="utf-8")
            # reescreve config com nome novo
            cfg_txt = (base / "config.py").read_text(encoding="utf-8")
            cfg_txt = cfg_txt.replace("NomeDoProduto", name)
            (target / "config.py").write_text(cfg_txt, encoding="utf-8")
            (base / "LANDING.md").read_text(encoding="utf-8")
            shutil.copy2(base / "LANDING.md", target / "LANDING.md")
            print("✅ landing criada em", target)
        else:
            print("⚠️ template landing não encontrado; criar apenas config.")
            (target / "config.py").write_text(
                'PROJECT = {"mode":"landing","name":"%s","docs_dir":".",'
                '"out_dir":"out","out_file":"index.html","landing_md":"LANDING.md"}' % name,
                encoding="utf-8")
    else:
        # mode docs: cria docs/ com um README de exemplo
        docs = target / "docs"
        docs.mkdir(exist_ok=True)
        (docs / "README.md").write_text(
            "# %s\n\nBem-vindo à documentação de **%s**, gerada com MimePy.\n\n"
            "Edite este e outros arquivos `.md` e rode o build.\n" % (name, name),
            encoding="utf-8")
        (target / "config.py").write_text(
            '# MimePy — config de "%s"\n'
            'PROJECT = {\n'
            '    "name": "%s",\n'
            '    "brand": "📘",\n'
            '    "page_title": "📚 Documentação — %s",\n'
            '    "docs_dir": "docs",\n'
            '    "out_dir": "out",\n'
            '    "out_file": "index.html",\n'
            '    "sidebar": [("README.md", "Visão geral")],\n'
            '}\n' % (name, name, name),
            encoding="utf-8")
        print("✅ projeto docs criado em", target)
    print("🔗 rode:  python <caminho>/src/cli.py build %s/config.py" % target)


def main():
    p = argparse.ArgumentParser(prog="mimepy", description="MimePy CLI (build/init)")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="gera HTML a partir de um config")
    b.add_argument("config", nargs="?", default=str(FRAMEWORK / "config.py"),
                   help="caminho do config.py (padrão: config.py do framework)")
    b.add_argument("--watch", action="store_true",
                   help="rebuild automático ao salvar .md/.py (modo dev)")

    i = sub.add_parser("init", help="cria um novo projeto MimePy")
    i.add_argument("name", help="nome do projeto")
    i.add_argument("-d", "--dir", default=".", help="diretório destino (padrão: atual)")
    i.add_argument("--template", default="docs", choices=["docs", "landing"],
                   help="modelo inicial (docs ou landing)")

    args = p.parse_args()
    if args.cmd == "build":
        cmd_build(args.config, watch=args.watch)
    elif args.cmd == "init":
        cmd_init(args.name, args.dir, args.template)


if __name__ == "__main__":
    main()
