# MimePy — testes automáticos (pytest).
# Substituem os scripts ad-hoc por uma suíte real e reprodutível (N12).
# Rode com:  python -m pytest -q  (na raiz do framework)
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))          # raiz (gera import de build)
sys.path.insert(0, str(REPO / "src"))  # onde está o módulo build/cli
