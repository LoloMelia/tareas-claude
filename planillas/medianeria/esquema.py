# -*- coding: utf-8 -*-
"""Esquema del simulacro de medianera: planta y corte del muro medianero del patio."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

LARGO, ALTO, VECINO_ALTO = 16.25, 2.50, 5.80
fig = plt.figure(figsize=(16, 11), dpi=160)
fig.patch.set_facecolor("white")
NEGRO = "#111111"; GRIS = "#d9d9d9"; GRIS2 = "#9a9a9a"; ROJO = "#c0392b"

# ======================= PLANTA =======================
ax = fig.add_axes([0.03, 0.55, 0.94, 0.40]); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("PLANTA  (esquemática)", fontsize=14, fontweight="bold", loc="left")
ax.add_patch(Rectangle((-1, 0.0), LARGO + 3, 4.2, fc="#f4f4f4", ec=NEGRO, lw=1, ls=(0, (2, 2))))
ax.text(LARGO / 2, 5.0, 'VECINO  "1"  (construye pegado al muro: 2 pisos, 5,80 m)', ha="center", fontsize=12, color="#444444")
ax.add_patch(Rectangle((-1, -4.6), LARGO + 3, 4.6, fc="#e8e8e8", ec="none"))
ax.text(LARGO / 2 + 3.5, -5.2, 'NUESTRO LOTE  "A"  (patio)', ha="center", fontsize=12)
ax.add_patch(Rectangle((0, -0.12), LARGO, 0.24, fc=ROJO, ec=NEGRO, lw=0.8))
ax.annotate("MURO MEDIANERO DEL PATIO  (lado SO)\nladrillo Brimax 20 cm · zapata corrida · 2,50 m de alto", xy=(10.5, 0.1),
            xytext=(8.5, 7.0), fontsize=11, color=ROJO, arrowprops=dict(arrowstyle="->", color=ROJO, lw=1.5))
ax.add_patch(Rectangle((5, -4.4), 9.5, 4.0, fc="#cfcfcf", ec=NEGRO, lw=0.8))
ax.text(9.75, -2.2, "casa", ha="center", fontsize=12)
for x, txt in ((0, "línea municipal"), (5, "línea de edificación\n(5 m)")):
    ax.plot([x, x], [-4.8, 0.8], color="#1f4e9e", lw=1.5, ls=(0, (5, 3)))
    ax.text(x, -5.9, txt, ha="center", fontsize=10.5, color="#1f4e9e")
ax.annotate("", xy=(0, 1.4), xytext=(LARGO, 1.4), arrowprops=dict(arrowstyle="<->", lw=1))
ax.text(LARGO / 2, 1.8, "16,25 m", ha="center", fontsize=12)
ax.annotate("", xy=(0, -4.35), xytext=(5, -4.35), arrowprops=dict(arrowstyle="<->", lw=1))
ax.plot([3.0, 3.0], [-1.0, 1.0], color="#1f4e9e", lw=2.2)
ax.text(3.2, 1.0, "A", color="#1f4e9e", fontsize=13, fontweight="bold")
ax.text(3.2, -1.0, "corte A-A'", color="#1f4e9e", fontsize=11)
ax.set_xlim(-1.5, LARGO + 2.5); ax.set_ylim(-6.6, 8.2)

# ======================= CORTE =======================
bx = fig.add_axes([0.03, 0.03, 0.94, 0.47]); bx.set_aspect("equal"); bx.axis("off")
bx.set_title("CORTE A-A'  por el muro medianero  (cotas en m; ancho del muro ampliado 3 veces)", fontsize=14, fontweight="bold", loc="left")
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
R(-0.10, zc, 0.20, ALTO, fc="#d9a58b", ec=NEGRO, lw=0.8, hatch="///")
R(-0.12, zc, 0.02, ALTO, fc="#f2f2f2", ec=NEGRO, lw=0.6)
R(0.10, zc, 0.02, ALTO, fc="#f2f2f2", ec=NEGRO, lw=0.6)
# edificio del vecino: llega a 5,80, pero el muro liquidado termina en 2,50
R(-2.4, zc, 2.28, VECINO_ALTO, fc="#f4f4f4", ec=NEGRO, lw=0.8, ls=(0, (4, 3)))
R(-2.4, zc + ALTO - 0.0, 2.28, 0.0001, fc="none", ec="#c0392b", lw=1.6)
bx.plot([-0.12 * SX, -2.4 * SX], [zc + ALTO, zc + ALTO], color=ROJO, lw=1.6, ls=(0, (5, 3)))
bx.text(-1.3 * SX, zc + VECINO_ALTO - 1.1, 'VECINO "1"\n(2 pisos, 5,80 m)', ha="center", fontsize=12, color="#444444")
bx.text(-1.3 * SX, zc + ALTO + 0.12, "la parte sobre los 2,50 m la construye el vecino\ny no entra en la liquidación", ha="center", fontsize=9.5, color=ROJO)
bx.text(1.3 * SX, 1.6, 'NUESTRO PATIO "A"', ha="center", fontsize=13, color="#444444")
bx.text(-2.35 * SX, NT - 0.22, "terreno", fontsize=10, color="#6b5a3c")
XT = 3.0 * SX
def ref(texto, y_obj, x_obj, y_txt):
    bx.annotate(texto, xy=(x_obj * SX, y_obj), xytext=(XT, y_txt), fontsize=10.5, va="center",
                arrowprops=dict(arrowstyle="-", color="#888888", lw=0.8))
ref("Revoque exterior (I+J+E) y revoque interior (J+E): 16,25 × 2,50 cada uno", zc + 2.0, 0.12, 4.6)
ref("Mampostería de elevación: 16,25 × 2,50 × 0,20", zc + 1.0, 0.10, 3.7)
ref("Doble capa aisladora, horizontal y vertical", zc, 0.13, 2.8)
ref("Mampostería de cimientos 20 cm: 0,70 de alto × 0,20", Z0 + 1.15, 0.10, 1.9)
ref("Encadenado de cimientos H°A°: 0,20 × 0,30", Z0 + 0.70, 0.15, 1.0)
ref("Mampostería de cimientos 45 cm: 0,30 × 0,45", Z0 + 0.45, 0.225, 0.1)
ref("Banquina de hormigón sin armar: 0,30 × 0,45", Z0 + 0.15, 0.225, -0.8)
ref("Excavación de cimientos: 1,20 de profundidad × 0,45", Z0 + 0.03, 0.225, -1.7)
bx.annotate("", xy=(-2.6 * SX, zc), xytext=(-2.6 * SX, zc + ALTO), arrowprops=dict(arrowstyle="<->", lw=1))
bx.text(-2.78 * SX, zc + ALTO / 2, "2,50", rotation=90, ha="center", va="center", fontsize=11)
bx.annotate("", xy=(-2.6 * SX, Z0), xytext=(-2.6 * SX, NT), arrowprops=dict(arrowstyle="<->", lw=1))
bx.text(-2.78 * SX, Z0 / 2, "1,20", rotation=90, ha="center", va="center", fontsize=11)
bx.set_xlim(-3.0 * SX, 10.5); bx.set_ylim(-2.1, 6.9)
fig.text(0.03, 0.012, "Esquema del simulacro: lote exento (barrio privado), sin medianera real. Se toma el muro del patio sobre el lado SO como medianero; "
         "los ítems y medidas son los de la hoja \"Medianeria (simulacro)\".", fontsize=10.5, color="#444444")
fig.savefig("/home/user/tareas-claude/planillas/medianeria/esquema_medianera.png", bbox_inches="tight")
print("ok")
