#!/usr/bin/env python3
"""
MimePy — Gerador de CHANGELOG.md (N15).

Deriva as mudanças do ROADMAP.md (itens marcados [x]) e gera/atualiza a
seção "não liberada" do CHANGELOG.md. Uso:
    python scripts/gen_changelog.py
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROADMAP = REPO / "docs" / "ROADMAP.md"
CHANGELOG = REPO / "CHANGELOG.md"


def collect_done():
    txt = ROADMAP.read_text(encoding="utf-8") if ROADMAP.exists() else ""
    items = []
    for m in re.finditer(r"- \[x\] (.+)", txt):
        items.append(m.group(1).strip())
    return items


def main():
    if CHANGELOG.exists() and ROADMAP.exists():
        done = collect_done()
        # Reinsere os itens concluídos na seção [Unreleased] (simples append se ausente)
        txt = CHANGELOG.read_text(encoding="utf-8")
        if "Unreleased" not in txt:
            txt = txt.replace("# Changelog — MimePy\n",
                              "# Changelog — MimePy\n\n## [Unreleased]\n\n"
                              + "\n".join("- " + d for d in done) + "\n")
            CHANGELOG.write_text(txt, encoding="utf-8")
            print("CHANGELOG atualizado com %d itens do ROADMAP." % len(done))
        else:
            print("CHANGELOG já tem seção Unreleased. (adicione manualmente se necessário)")
    else:
        print("ROADMAP/CHANGELOG ausente.")


if __name__ == "__main__":
    main()
