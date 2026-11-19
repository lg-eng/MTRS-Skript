"""Testharness: fuehrt alle Python-Chunks der Messtechnik-Kapitel offline aus.

Simuliert den Jupyter-Kernel ATOM-fuer-Chunk pro Datei und faengt Fehler ab,
ohne einen Quarto-Render zu brauchen. Ausfuehren mit:
uv run --frozen python Messtechnik/test_chunks.py
"""

import os
import re
import sys
import traceback
from IPython.display import Markdown
from unittest.mock import MagicMock

import matplotlib
matplotlib.use("Agg")

BASE = __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0]
HELPER = os.path.join(BASE, "..", "..", "..", "..",
                      "Common", "QuartoBookHelpers", "QuartoBookHelpers.qmd")

FILES = [
    "01.01_Einfuehrung.qmd",
    "01.02_Strom_Spannung_Widerstand.qmd",
    "01.03_Digitales_Multimeter.qmd",
    "01.04_Kennwerte.qmd",
    "01.05_Frequenz_und_Periode.qmd",
    "01.06_ADW_DAW.qmd",
    "../Anhang/xx_Weiterfuehrende_Themen.qmd",
]

CHUNK_RE = re.compile(r"```{python(?P<opts>[^\n]*)\n(?P<body>.*?)```", re.DOTALL)


def extract_chunks(path):
    text = open(path, encoding="utf-8").read()
    chunks = []
    for m in CHUNK_RE.finditer(text):
        body = "\n".join(
            line for line in m.group("body").splitlines()
            if not line.strip().startswith("#|")
        )
        chunks.append(body)
    return chunks


def helper_code():
    m = CHUNK_RE.search(open(HELPER, encoding="utf-8").read())
    body = "\n".join(
        line for line in m.group("body").splitlines()
        if not line.strip().startswith("#|")
        and not line.strip().startswith("#")
    )
    return body


class SilentDisplay:
    def __call__(self, obj, *a, **k):
        try:
            data = getattr(obj, "data", None)
            marker = "[display]"
            text = str(data if data is not None else obj)
            for line in text.splitlines():
                if line.strip():
                    print(marker, line.strip()[:120])
        except Exception:
            print("[display]", repr(obj)[:100])


def main():
    failures = 0
    for fname in FILES:
        print(f"\n===== {fname}")
        ns = {}
        ns["display"] = SilentDisplay()
        ns["plt"] = __import__("matplotlib.pyplot", fromlist=["pyplot"])
        # plt.show() unter Agg stillabschalten
        ns["plt"].show = lambda *a, **k: None
        helper = helper_code()
        try:
            exec(compile(helper, "QuartoBookHelpers.qmd", "exec"), ns)
        except Exception:
            print("HELPER FEHLGESCHLAGEN:")
            traceback.print_exc()
            return 1
        for i, code in enumerate(extract_chunks(f"{BASE}\\{fname}"), 1):
            try:
                exec(compile(code, f"{fname}#chunk{i}", "exec"), ns)
            except Exception as e:
                failures += 1
                print(f"  FEHLER in Chunk {i}: {e}")
                traceback.print_exc(limit=3)
                print("  --- Code:")
                for line in code.splitlines()[:12]:
                    print("   ", line)
                return 1
    print("\nALLES OK" if failures == 0 else f"\n{failures} FEHLER")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
