# -*- coding: utf-8 -*-
"""Esquema del simulacro de medianera: planta y corte."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch

fig = plt.figure(figsize=(16, 11), dpi=160)
fig.patch.set_facecolor("white")
NEGRO = "#111111"; GRIS = "#d9d9d9"; GRIS2 = "#9a9a9a"

# ======================= PLANTA =======================
ax = fig.add_axes([0.03, 0.52, 0.60, 0.44]); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("PLANTA  (arriba = NO, derecha = NE)", fontsize=14, fontweight="bold", loc="left")
ax.add_patch(Rectangle((-9, -1.2), 8.8, 5.96, fc="#f4f4f4", ec=NEGRO, lw=1, ls=(0, (2, 2))))
ax.text(-5.0, 3.5, 'VECINO  "1"\n(construcción a adosar)', ha="center", va="center", fontsize=12, color="#444444")
ax.add_patch(Rectangle((0.0, 0), 7.63, 3.56, fc=GRIS, ec="none"))
ax.text(4.2, 2.6, 'NUESTRA COCINA  "A"\n7,63 × 3,56 m', ha="center", va="center", fontsize=12)
e = 0.2
ax.add_patch(Rectangle((-e, -e), 7.63 + 2 * e, e, fc=GRIS2, ec=NEGRO, lw=0.8))
ax.add_patch(Rectangle((-e, 3.56), 7.63 + 2 * e, e, fc=GRIS2, ec=NEGRO, lw=0.8))
ax.add_patch(Rectangle((7.63, 0), e, 3.56, fc=GRIS2, ec=NEGRO, lw=0.8))
ax.add_patch(Rectangle((-e, 0), e, 3.56, fc="#c0392b", ec=NEGRO, lw=0.8))
ax.annotate("MEDIANERA\n(pared SO de la cocina; PF04 y VA01\ntomadas como ciegas)",
            xy=(-0.1, 3.3), xytext=(-6.6, 6.1), fontsize=11, color="#c0392b", ha="left",
            arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.5))
ax.annotate("", xy=(-1.5, 0), xytext=(-1.5, 3.56), arrowprops=dict(arrowstyle="<->", lw=1))
ax.text(-1.85, 1.78, "3,56 m", rotation=90, ha="center", va="center", fontsize=11)
ax.annotate("", xy=(0, -1.0), xytext=(7.63, -1.0), arrowprops=dict(arrowstyle="<->", lw=1))
ax.text(3.8, -1.55, "7,63 m", ha="center", fontsize=11)
ax.plot([-3.4, 1.8], [0.8, 0.8], color="#1f4e9e", lw=2, ls=(0, (6, 3)))
ax.text(-3.4, 1.15, "A", color="#1f4e9e", fontsize=13, fontweight="bold")
ax.text(1.8, 1.15, "A'", color="#1f4e9e", fontsize=13, fontweight="bold")
ax.text(-3.4, 0.2, "corte A-A'", color="#1f4e9e", fontsize=11)
ax.annotate("", xy=(7.0, 6.3), xytext=(7.0, 5.0), arrowprops=dict(arrowstyle="-|>", lw=2))
ax.text(7.0, 6.55, "NO", ha="center", fontsize=12, fontweight="bold")
ax.annotate("", xy=(8.6, 5.65), xytext=(7.0, 5.65), arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#555555"))
ax.text(8.75, 5.65, "NE", va="center", fontsize=11, color="#555555")
ax.set_xlim(-9.2, 9.6); ax.set_ylim(-2.2, 7.2)

# ======================= CORTE =======================
bx = fig.add_axes([0.03, 0.06, 0.94, 0.42]); bx.set_aspect("equal"); bx.axis("off")
bx.set_title("CORTE A-A'  por la medianera  (cotas en m; ancho de la pared ampliado 3 veces)", fontsize=14, fontweight="bold", loc="left")
SX = 3.0
def R(x, z, w, h, **kw): bx.add_patch(Rectangle((x * SX, z), w * SX, h, **kw))
Z0 = -1.2; NT = 0.0
R(-2.4, Z0, 2.4 - 0.225, 1.2, fc="#efe6d6", ec="none")
R(0.225, Z0, 2.4 - 0.225, 1.2, fc="#efe6d6", ec="none")
bx.plot([-2.4 * SX, -0.225 * SX], [NT, NT], color="#6b5a3c", lw=1.5)
bx.plot([0.225 * SX, 2.4 * SX], [NT, NT], color="#6b5a3c", lw=1.5)
R(-0.225, Z0, 0.45, 1.2, fc="white", ec="#777777", lw=0.8, ls=(0, (3, 2)))
R(-0.225, Z0, 0.45, 0.30, fc="#c9c9c9", ec=NEGRO, lw=0.8, hatch="...")
R(-0.225, Z0 + 0.30, 0.45, 0.30, fc="#d9a58b", ec=NEGRO, lw=0.8, hatch="///")
R(-0.15, Z0 + 0.60, 0.30, 0.20, fc="#8e8e8e", ec=NEGRO, lw=0.8, hatch="xx")
R(-0.10, Z0 + 0.80, 0.20, 0.70, fc="#d9a58b", ec=NEGRO, lw=0.8, hatch="///")
zc = Z0 + 1.50
bx.plot([-0.13 * SX, 0.13 * SX], [zc, zc], color=NEGRO, lw=3)
R(-0.10, zc, 0.20, 3.00, fc="#d9a58b", ec=NEGRO, lw=0.8, hatch="///")
R(-0.12, zc, 0.02, 3.00, fc="#f2f2f2", ec=NEGRO, lw=0.6)
R(0.10, zc, 0.02, 3.00, fc="#f2f2f2", ec=NEGRO, lw=0.6)
R(-2.4, zc + 3.0 - 0.12, 2.28, 0.12, fc="#bdbdbd", ec=NEGRO, lw=0.8)
R(0.12, zc + 3.0 - 0.12, 2.28, 0.12, fc="#bdbdbd", ec=NEGRO, lw=0.8)
bx.text(-1.3 * SX, 1.6, 'VECINO "1"', ha="center", fontsize=13, color="#444444")
bx.text(1.3 * SX, 1.6, 'NUESTRA CASA "A"', ha="center", fontsize=13, color="#444444")
bx.text(-2.35 * SX, NT - 0.22, "terreno", fontsize=10, color="#6b5a3c")
XT = 3.0 * SX
def ref(texto, y_obj, x_obj, y_txt):
    bx.annotate(texto, xy=(x_obj * SX, y_obj), xytext=(XT, y_txt), fontsize=10.5, va="center",
                arrowprops=dict(arrowstyle="-", color="#888888", lw=0.8))
ref("Revoque exterior (I+J+E) y revoque interior (J+E): 3,56 × 3,00 cada uno", zc + 2.6, 0.12, 3.35)
ref("Mampostería de elevación: 3,56 × 3,00 × 0,20", zc + 1.8, 0.10, 2.65)
ref("Doble capa aisladora, horizontal y vertical", zc, 0.13, 1.95)
ref("Mampostería de cimientos 20 cm: 0,70 de alto × 0,20", Z0 + 1.15, 0.10, 1.25)
ref("Encadenado de cimientos H°A°: 0,20 × 0,30", Z0 + 0.70, 0.15, 0.55)
ref("Mampostería de cimientos 45 cm: 0,30 × 0,45", Z0 + 0.45, 0.225, -0.15)
ref("Banquina de hormigón sin armar: 0,30 × 0,45", Z0 + 0.15, 0.225, -0.85)
ref("Excavación de cimientos: 1,20 de profundidad × 0,45", Z0 + 0.03, 0.225, -1.55)
bx.annotate("", xy=(-2.6 * SX, zc), xytext=(-2.6 * SX, zc + 3.0), arrowprops=dict(arrowstyle="<->", lw=1))
bx.text(-2.78 * SX, zc + 1.5, "3,00", rotation=90, ha="center", va="center", fontsize=11)
bx.annotate("", xy=(-2.6 * SX, Z0), xytext=(-2.6 * SX, NT), arrowprops=dict(arrowstyle="<->", lw=1))
bx.text(-2.78 * SX, Z0 / 2, "1,20", rotation=90, ha="center", va="center", fontsize=11)
bx.set_xlim(-3.0 * SX, 17.0 * SX / 1.0 * 0.62); bx.set_ylim(-1.9, 3.7)

fig.text(0.03, 0.015, "Esquema del simulacro: lote exento, sin medianera real. La pared SO de la cocina se toma como medianera; "
         "los ítems y medidas son los de la hoja \"Medianeria (simulacro)\".", fontsize=10.5, color="#444444")
fig.savefig("/home/user/tareas-claude/planillas/medianeria/esquema_medianera.png", bbox_inches="tight")
print("ok")
