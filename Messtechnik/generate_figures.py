"""Erzeugt die Diagramme für die 2.-Jahrgang-Kapitel des MTRS-Skripts.

Läuft mit: uv run --frozen python Messtechnik/generate_figures.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = Path(__file__).parent
IMG = HERE / "images"
IMG.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.size": 10,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 150,
})


def downscale(name: str, max_width: int = 1400, max_height: int = 1400) -> None:
    """Skaliert große Commons-Dateien auf Repo-freundliche Größe."""
    path = IMG / name
    img = Image.open(path)
    if img.mode in ("RGBA", "P") and name.lower().endswith(("jpg", "jpeg")):
        img = img.convert("RGB")
    scale = min(max_width / img.width, max_height / img.height, 1.0)
    if scale < 1.0:
        img = img.resize((round(img.width * scale), round(img.height * scale)),
                         Image.LANCZOS)
    if name.lower().endswith(("jpg", "jpeg")):
        img.save(path, quality=85)
    else:
        img.save(path)
    img.close()


def messunsicherheit_typA() -> None:
    """Typ-A-Auswertung: Streuung der Messwerte, Referenzwert, Mittelwert."""
    rng = np.random.default_rng(42)
    x_ref = 10.0
    bias = 0.08
    samples = rng.normal(x_ref + bias, 0.05, 400)
    u_a = samples.std(ddof=1) / np.sqrt(len(samples))

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.hist(samples, bins=24, color="#5a8fd6", edgecolor="white",
            label="Messwerte $x_i$")
    ax.axvline(x_ref, color="#2e7d32", lw=2,
               label="Referenzwert $x_{ref}$")
    ax.axvline(samples.mean(), color="#d62728", lw=2, ls="--",
               label="Mittelwert $\\bar{x}$")
    ax.annotate("", xy=(samples.mean(), ax.get_ylim()[1] * 0.6),
                xytext=(samples.mean() - 3 * u_a, ax.get_ylim()[1] * 0.6),
                arrowprops=dict(arrowstyle="<->", color="#444444"))
    ax.text(samples.mean() - 2.5 * u_a, ax.get_ylim()[1] * 0.62,
            "$u_A = s/\\sqrt{n}$", fontsize=9, color="#444444")
    ax.set_xlabel("Messwert $x$")
    ax.set_ylabel("Häufigkeit")
    ax.legend(framealpha=0.9, fontsize=9)
    fig.tight_layout()
    fig.savefig(IMG / "messunsicherheit_typA.png", bbox_inches="tight")
    plt.close(fig)


def rueckwirkungsabweichung() -> None:
    """Relative Messabweichung durch Rückwirkung bei Spannungs- und Strommessung."""
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ratio = np.logspace(-3, 2, 300)

    # Spannungsmessung: R_Quelle / R_Voltmeter
    delta_u = -ratio / (1 + ratio) * 100
    ax.loglog(ratio, -delta_u, label="Spannungsmessung: $R_q/R_V$")

    # Strommessung: R_Amperemeter / R_Quelle
    ratio_a = 1 / ratio
    delta_i = -ratio_a / (1 + ratio_a) * 100
    ax.loglog(ratio, -delta_i, ls="--", label="Strommessung: $R_A/R_q$")

    ax.axhline(1.0, color="gray", lw=1, ls=":")
    ax.text(0.0012, 1.05, "1 %", fontsize=9, color="gray")
    ax.set_xlabel("Widerstandsverhältnis")
    ax.set_ylabel("relative Abweichung $|\\delta|$ in %")
    ax.legend(fontsize=9)
    ax.set_xlim(1e-3, 1e2)
    fig.tight_layout()
    fig.savefig(IMG / "rueckwirkungsabweichung.png", bbox_inches="tight")
    plt.close(fig)


def dmm_blockschaltbild() -> None:
    """Blockschaltbild eines digitalen Multimeters."""
    blocks = [
        "Eingangs-\nschutz",
        "Eingangs-\nteiler",
        "Verstärker\n(impedanzwandler)",
        "ADW\n(Zweiflanken-\\nverfahren)",
        "Zähler &\nLogik",
        "LCD-/LED-\nAnzeige",
    ]
    fig, ax = plt.subplots(figsize=(9, 1.9))
    ax.set_xlim(0, len(blocks) + 0.4)
    ax.set_ylim(0, 1.6)
    ax.axis("off")
    for i, b in enumerate(blocks):
        ax.add_patch(plt.Rectangle((i + 0.1, 0.5), 0.85, 0.6,
                                   fill=True, facecolor="#dce8f5",
                                   edgecolor="#365a80"))
        ax.text(i + 0.525, 0.8, b, ha="center", va="center", fontsize=9)
        if i < len(blocks) - 1:
            ax.annotate("", xy=(i + 1.0, 0.8), xytext=(i + 0.95, 0.8),
                        arrowprops=dict(arrowstyle="->", lw=1.4))
    fig.tight_layout()
    fig.savefig(IMG / "dmm_blockschaltbild.png", bbox_inches="tight")
    plt.close(fig)


def kennwerte_signale() -> None:
    """Sinussignal mit Kennwerten sowie gleichgerichteter Verlauf."""
    t = np.linspace(0, 2, 1000)
    u = np.sin(2 * np.pi * t)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3))
    ax1.plot(t, u, color="#5a8fd6", lw=1.6)
    ax1.axhline(0, color="gray", lw=0.8)
    ax1.axhline(1, color="#2e7d32", ls="--", lw=1)
    ax1.axhline(1 / np.sqrt(2), color="#d62728", ls="--", lw=1)
    ax1.axhline(2 / np.pi, color="#9467bd", ls="--", lw=1)
    ax1.text(2.02, 1.0, "$\\hat{u}$", fontsize=10, va="center", color="#2e7d32")
    ax1.text(2.02, 1 / np.sqrt(2), "$U_{eff}$", fontsize=10, va="center", color="#d62728")
    ax1.text(2.02, 2 / np.pi, "$\\overline{|u|}$", fontsize=10, va="center", color="#9467bd")
    ax1.set_title("Sinusschwingung", fontsize=10)
    ax1.set_xlabel("$t$ in Perioden")
    ax1.set_ylabel("$u(t)$")

    ax2.plot(t, np.abs(u), color="#5a8fd6", lw=1.6)
    ax2.axhline(2 / np.pi, color="#9467bd", ls="--", lw=1)
    ax2.text(2.02, 2 / np.pi, "$\\overline{|u|}$", fontsize=10, va="center", color="#9467bd")
    ax2.set_title("gleichgerichtete Schwingung", fontsize=10)
    ax2.set_xlabel("$t$ in Perioden")
    ax2.set_ylabel("$|u(t)|$")
    fig.tight_layout()
    fig.savefig(IMG / "kennwerte_signale.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    for name in (
        "Analog_multimeter_HARTIG_HELLING_VM-10K.jpg",
        "Electric_circuit_with_voltmeter_and_ammeter.JPG",
        "Moving_coil_instrument_principle.png",
    ):
        downscale(name)
    messunsicherheit_typA()
    rueckwirkungsabweichung()
    dmm_blockschaltbild()
    kennwerte_signale()
    print("Figuren erzeugt in", IMG)
