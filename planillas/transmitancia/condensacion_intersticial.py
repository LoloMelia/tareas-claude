# -*- coding: utf-8 -*-
"""Condensacion intersticial (Glaser, IRAM 11625), con el diseno de la planilla de la autora.

En cada interfaz entre capas: temperatura T, presion de vapor real rho (cae en proporcion al Rv acumulado),
temperatura de rocio Tr de esa presion y diferencia T - Tr. Hay condensacion donde T < Tr (diferencia negativa).
Libros: con formulas y (para AutoCAD) con valores fijos. Convenciones de formato: ver CLAUDE.md.
"""
import sys, math
sys.path.insert(0, "/home/user/tareas-claude/planillas/plantas")
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
import bordes

FUENTE = "Bahnschrift Light Condensed"
GRIS = PatternFill("solid", fgColor="D9D9D9")
C = Alignment(horizontal="center", vertical="center", wrap_text=True)
L = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALTO, ALTO_TITULO = 19.8, 28.4
FINA = Side(style="thin", color="000000")
BOX = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
ROJO = "C00000"
TI, HRI, TDMN, HRE = 18.0, 65.0, -4.0, 80.0
TITULO = "VERIFICACIÓN DE TRANSMITANCIA TÉRMICA\nNORMA IRAM 11601"      # titulo de la planilla de la autora
BRIMAX = "Ladrillo HCCA Brimax 18 portante"

def ps(t): return 0.6105 * math.exp(17.269 * t / (237.3 + t)) if t >= 0 else 0.6105 * math.exp(21.875 * t / (265.5 + t))
def tr(p):
    x = math.log(p / 0.6105)
    return 237.3 * x / (17.269 - x) if p >= 0.6105 else 265.5 * x / (21.875 - x)

# capa: (nombre, densidad, e, lambda, delta (g/m.h.kPa), Delta permeancia (g/m2.h.kPa))
MURO = [("Latex Interior", None, 0.0, None, None, 1.13),
        ("Mortero de yeso monocapa", 1000, 0.020, 0.570, 0.07, None),
        (BRIMAX, None, 0.180, 0.120, 0.13, None),
        ("Azotado hidráulico cemento arena e hidrófugo", 2000, 0.005, 1.130, 0.022, None),
        ("Mortero de cemento, cal y arena", 1800, 0.020, 0.930, 0.044, None),
        ("Material de frente acrílico", None, 0.0, None, None, 5.0)]
MURO_B = MURO[:2] + [("Barrera de vapor polietileno 200 micrones", None, 0.0, None, None, 0.008)] + MURO[2:]
CUBIERTA = [("Hormigón armado de piedra H21 c/ armadura", 2400, 0.120, 1.630, 0.02, None),
            ("Barrera de vapor polietileno 200 micrones", None, 0.0, None, None, 0.008),
            ("Poliestireno expandido de alta densidad", 30, 0.060, 0.032, 0.0075, None),
            ("Hormigón de pendiente c/ vermiculita", 600, 0.120, 0.160, 0.15, None),
            ("Carpeta", 2000, 0.020, 1.130, 0.022, None),
            ("Membrana geotextil", 2000, 0.005, 0.700, None, 0.67),
            ("Pintura acrílica impermeable blanca", None, 0.0, None, None, 5.0)]
ELEMENTOS = [
 dict(nombre="MURO EXTERIOR", flujo="HORIZONTAL", rsi=0.130, rse=0.040, capas=MURO),
 dict(nombre="MURO EXTERIOR con PINTURA ASFALTICA", flujo="HORIZONTAL", rsi=0.130, rse=0.040, capas=MURO_B),
 dict(nombre="CUBIERTA", flujo="ASCENDENTE", rsi=0.100, rse=0.040, capas=CUBIERTA),
]

def rv(e, d, D):
    if D: return 1.0 / D
    if d and e: return e / d
    return 0.0

def calcular(el):
    rt = el["rsi"] + el["rse"] + sum(e / l for _, _, e, l, _, _ in el["capas"] if l)
    rvt = sum(rv(e, d, D) for _, _, e, _, d, D in el["capas"])
    pi, pe = HRI / 100 * ps(TI), HRE / 100 * ps(TDMN)
    dt, dp = TI - TDMN, pi - pe
    filas = []; acr = el["rsi"]; acv = 0.0
    t = TI - acr / rt * dt; filas.append((t, pi, tr(pi), t - tr(pi)))
    for _, _, e, l, d, D in el["capas"]:
        acr += e / l if l else 0.0; acv += rv(e, d, D)
        t = TI - acr / rt * dt; p = pi - dp * acv / rvt
        filas.append((t, p, tr(p), t - tr(p)))
    return dict(rt=rt, k=1 / rt, rvt=rvt, pi=pi, pe=pe, dt=dt, dp=dp, filas=filas,
                esp=sum(e for _, _, e, _, _, _ in el["capas"]), cond=[i for i, x in enumerate(filas) if x[3] < 0])

def construir(ws, formulas):
    ws.sheet_view.showGridLines = False
    def f(c, b=False, color=None, size=12): c.font = Font(name=FUENTE, size=size, bold=b, color=color)
    for col, w in zip("ABCDEFGHIJKLM", (50, 10, 9, 9, 10, 9, 15, 15, 15, 8, 9, 9, 10)): ws.column_dimensions[col].width = w
    r = 1
    for el in ELEMENTOS:
        R0 = r; d = calcular(el)
        def fila(h=ALTO):
            nonlocal r
            ws.row_dimensions[r].height = h; r += 1; return r - 1
        def mer(rr, c1, c2, valor=None, negrita=False, gris=False, alin=C):
            ws.merge_cells(start_row=rr, start_column=c1, end_row=rr, end_column=c2)
            c = ws.cell(row=rr, column=c1, value=valor); f(c, negrita); c.alignment = alin
            for k in range(c1, c2 + 1):
                x = ws.cell(row=rr, column=k); x.border = BOX
                if gris: x.fill = GRIS
            return c
        def num(rr, col, v, fmt="0.00", negrita=False):
            c = ws.cell(row=rr, column=col, value=v); f(c, negrita); c.alignment = C; c.number_format = fmt; return c
        rr = fila(ALTO_TITULO + 8); mer(rr, 1, 13, TITULO, False, True)
        rr = fila(ALTO_TITULO); mer(rr, 1, 5, "ELEMENTO", True, True); mer(rr, 6, 9, "EPOCA DEL AÑO", True, True); mer(rr, 10, 13, "FLUJO DE CALOR", True, True)
        rr = fila(); mer(rr, 1, 5, el["nombre"], True); mer(rr, 6, 9, "INVIERNO"); mer(rr, 10, 13, el["flujo"])
        rr = fila(); mer(rr, 1, 5, "ZONA BIOAMBIENTAL"); mer(rr, 6, 13, "IIIa - Ciudad de Rosario (Pcia. de Santa Fe)", True)
        fila()
        rr = fila(46)
        enc = ["Capa del elemento constructivo", "Dens. (Kg/m³)", "e (m)", "λ (W/mK)", "R (m²K/W)", "T (°C)", "Permeab δ (g/m.h.kPa)",
               "Permean Δ (g/m.h.kPa)", "Rv (m².h.kPa/g)", "HR (%)", "ρ (kPa)", "Tr (°C)", "Dif.(Δt)"]
        for k, t in enumerate(enc, 1):
            c = ws.cell(row=rr, column=k, value=t); f(c, False); c.fill = GRIS; c.alignment = L if k == 1 else C
        n = len(el["capas"])
        r_air = r; r_rsi = r + 1; r_int0 = r + 2
        r_capa = [r + 3 + 2 * i for i in range(n)]
        r_if = [r + 4 + 2 * i for i in range(n)]
        r_rse = r + 3 + 2 * n; r_esp = r_rse + 1; r_tdmn = r_esp + 1; r_zona = r_tdmn + 1
        r_lab = r_zona + 1; r_val = r_lab + 1; r_klab = r_val + 1; r_kval = r_klab + 1
        RT = "$E$%d" % r_val; RVT = "$I$%d" % r_val
        # aire interior
        fila(); mer(r_air, 1, 5, "Temperatura interior del aire", alin=L)
        num(r_air, 6, TI, "0", True); num(r_air, 10, HRI, "0", True)
        def trf(rr): return "=IF(K{r}>=0.6105,237.3*LN(K{r}/0.6105)/(17.269-LN(K{r}/0.6105)),265.5*LN(K{r}/0.6105)/(21.875-LN(K{r}/0.6105)))".format(r=rr)
        num(r_air, 11, ("=J%d/100*0.6105*EXP(17.269*F%d/(237.3+F%d))" % (r_air, r_air, r_air)) if formulas else d["pi"])
        num(r_air, 12, trf(r_air) if formulas else tr(d["pi"]), "0.00"); num(r_air, 13, ("=F%d-L%d" % (r_air, r_air)) if formulas else TI - tr(d["pi"]), "0.0")
        fila(ALTO_TITULO); mer(r_rsi, 1, 4, "Resistencia superficial interior Rsi", alin=L, gris=True); num(r_rsi, 5, el["rsi"], "0.000")
        ws.cell(row=r_rsi, column=5).fill = GRIS
        def interfaz(rr, idx, hasta):
            fila()
            t, p, trr, dif = d["filas"][idx]
            if formulas:
                num(rr, 6, "=$F$%d-($F$%d-$F$%d)*SUM($E$%d:E%d)/%s" % (r_air, r_air, r_tdmn, r_rsi, hasta, RT))
                num(rr, 11, ("=$K$%d-($K$%d-$K$%d)*SUM($I$%d:I%d)/%s" % (r_air, r_air, r_zona, r_capa[0], hasta, RVT)) if idx > 0 else "=$K$%d" % r_air)
                num(rr, 12, trf(rr)); num(rr, 13, "=F%d-L%d" % (rr, rr))
            else:
                num(rr, 6, t); num(rr, 11, p); num(rr, 12, trr); num(rr, 13, dif)
        interfaz(r_int0, 0, r_rsi)
        for i, (nom, dens, e, lam, dl, DD) in enumerate(el["capas"]):
            rr = r_capa[i]; fila()
            ws.cell(row=rr, column=1, value=nom); f(ws.cell(row=rr, column=1)); ws.cell(row=rr, column=1).alignment = L
            if dens: num(rr, 2, dens, "0")
            num(rr, 3, e, "0.000")
            if lam: num(rr, 4, lam, "0.000"); num(rr, 5, ("=C%d/D%d" % (rr, rr)) if formulas else e / lam, "0.000")
            if dl: num(rr, 7, dl, "0.0000")
            if DD: num(rr, 8, DD, "0.000")
            num(rr, 9, ("=IF(H{r}>0,1/H{r},IF(AND(G{r}>0,C{r}>0),C{r}/G{r},0))".format(r=rr)) if formulas else rv(e, dl, DD), "0.00")
            interfaz(r_if[i], i + 1, rr)
        fila(ALTO_TITULO); mer(r_rse, 1, 4, "Resistencia superficial exterior Rse", alin=L, gris=True); num(r_rse, 5, el["rse"], "0.000")
        ws.cell(row=r_rse, column=5).fill = GRIS
        fila(); mer(r_esp, 1, 2, "Espesor total aproximado", alin=L)
        num(r_esp, 3, ("=SUM(C%d:C%d)" % (r_capa[0], r_capa[-1])) if formulas else d["esp"], "0.000")
        fila(); mer(r_tdmn, 1, 5, "Temperatura de diseño mínima TDMN para Rosario", alin=L); num(r_tdmn, 6, TDMN, "0", True)
        fila(); c = ws.cell(row=r_zona, column=1, value="(Zona Bioclimática)"); f(c); c.alignment = L
        mer(r_zona, 2, 5, "IIIa", True); num(r_zona, 10, HRE, "0", True)
        num(r_zona, 11, ("=J%d/100*IF(F%d>=0,0.6105*EXP(17.269*F%d/(237.3+F%d)),0.6105*EXP(21.875*F%d/(265.5+F%d)))" % ((r_zona, r_tdmn) + (r_tdmn,) * 4)) if formulas else d["pe"])
        # resistencias totales
        fila(); c = ws.cell(row=r_lab, column=1, value="Resistencias totales"); f(c, True); c.alignment = L
        mer(r_lab, 2, 4, "TERMICA", True)
        for col, t in ((5, "Rt"), (6, "(Δt)"), (11, "(Δρ)"), (9, "RVt")):
            num(r_lab, col, t, "@")
        mer(r_lab, 7, 8, "AL VAPOR", True)
        fila()
        num(r_val, 5, ("=E%d+E%d+SUM(E%d:E%d)" % (r_rsi, r_rse, r_capa[0], r_capa[-1])) if formulas else d["rt"], "0.000", True)
        num(r_val, 6, ("=F%d-F%d" % (r_air, r_tdmn)) if formulas else d["dt"], "0", True)
        num(r_val, 9, ("=SUM(I%d:I%d)" % (r_capa[0], r_capa[-1])) if formulas else d["rvt"], "0.00", True)
        num(r_val, 11, ("=K%d-K%d" % (r_air, r_zona)) if formulas else d["dp"], "0.00", True)
        fila(); num(r_klab, 5, "K", "@")
        fila(); num(r_kval, 5, ("=1/E%d" % r_val) if formulas else d["k"], "0.000", True)
        if formulas:
            ws.conditional_formatting.add("M%d:M%d" % (r_int0, r_if[-1]), CellIsRule(operator="lessThan", formula=["0"], font=Font(name=FUENTE, bold=True, color=ROJO)))
        else:
            for rrr in [r_int0] + r_if:
                if ws.cell(row=rrr, column=13).value < 0: f(ws.cell(row=rrr, column=13), True, ROJO)
        for rrr in range(R0, r):
            for k in range(1, 14):
                x = ws.cell(row=rrr, column=k)
                if x.font.name != FUENTE: f(x)
                x.border = BOX
        for rrr in (r_lab, r_val, r_klab, r_kval):       # los cuadros de resumen: solo las celdas con contenido
            for k in range(1, 14):
                if ws.cell(row=rrr, column=k).value in (None, "") and not any(rrr == m.min_row and m.min_col <= k <= m.max_col for m in ws.merged_cells.ranges):
                    ws.cell(row=rrr, column=k).border = Border(left=Side(), right=Side(), top=Side(), bottom=Side())
        r += 1
    bordes.aplicar(ws)
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

for nombre, formulas in (("Condensacion intersticial.xlsx", True), ("Condensacion intersticial (para AutoCAD).xlsx", False)):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Condensacion intersticial"
    construir(ws, formulas); wb.save(nombre)
for el in ELEMENTOS:
    d = calcular(el)
    print("%-38s Rt=%.3f K=%.3f RVt=%.2f  condensa en %s" % (el["nombre"], d["rt"], d["k"], d["rvt"],
          [("superficie" if i == 0 else el["capas"][i - 1][0][:26], round(d["filas"][i][3], 2)) for i in d["cond"]] or "ninguna"))
