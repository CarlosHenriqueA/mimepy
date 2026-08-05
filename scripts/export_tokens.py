#!/usr/bin/env python3
"""
MimePy — Exportar design tokens (N28).

Lê as CSS variables do `:root` em `src/assets/style.css` e gera arquivos de
tokens consumíveis em outros projetos:
  - tokens.json   (formato DTCG — Design Tokens Community Group)
  - token.css     (como :root com as vars, fácil de copiar)

Uso:
    python scripts/export_tokens.py [-o DIR]

Filosofia: o design system do MimePy vive nas CSS variables (`style.css`);
este script as "materializa" para reuso (adota o DESIGN.md em outros apps).
"""
import argparse
import re
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STYLE = REPO / "src" / "assets" / "style.css"


def extract_tokens():
    """Extrai `--nome: valor` do bloco `:root{...}` do style.css."""
    src = STYLE.read_text(encoding="utf-8")
    # captura o bloco :root até o FECHAMENTO — usamos re.S e buscamos do
    # primeiro '{' ao '}' correspondente (o :root é um único par de chaves).
    start = src.find(":root")
    if start == -1:
        return {}
    block = src[src.find("{", start):]
    # acha o fecha par: conta chaves a partir do bloco (simples, um par para :root)
    depth = 0
    end = 0
    for i, ch in enumerate(block):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    block = block[:end]
    tokens = {}
    # vários tokens podem estar na mesma linha (--bg:#fff; --fg:#000;) → findall
    for mm in re.finditer(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;]+);", block):
        tokens[mm.group(1)] = mm.group(2).strip()
    return tokens


def to_dtcg(tokens):
    """Converte {--bg:#fff} -> {"bg":{"value":"#fff","type":"color"}} DTCG."""
    out = {}
    for k, v in tokens.items():
        name = k[2:]                       # remove --
        # infere tipo DTCG a partir do valor
        if re.match(r"^#", v):
            t = "color"
        elif re.match(r"^\d+(px|rem|em|%|\s|$)", v):
            t = "dimension"
        else:
            t = "string"
        out[name] = {"value": v, "type": t}
    return out


def main():
    ap = argparse.ArgumentParser(description="Exporta tokens do DESIGN.md/style.css")
    ap.add_argument("-o", "--out", default=str(REPO / "tokens"),
                    help="diretório de saída (padrão: ./tokens)")
    args = ap.parse_args()

    tokens = extract_tokens()
    if not tokens:
        print("⚠️ Nenhum token encontrado em", STYLE)
        raise SystemExit(1)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) tokens.json (DTCG)
    dtcg = to_dtcg(tokens)
    (outdir / "tokens.json").write_text(
        json.dumps(dtcg, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2) token.css (pronto p/ copiar/importar)
    lines = [":root{"]
    lines += ["  %s: %s;" % (k, v) for k, v in sorted(tokens.items())]
    lines.append("}")
    (outdir / "token.css").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("[export] %d tokens -> %s (tokens.json DTCG + token.css)" % (len(tokens), outdir))


if __name__ == "__main__":
    main()
