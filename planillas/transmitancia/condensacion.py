# -*- coding: utf-8 -*-
"""Calculo de condensacion superficial, muro y cubierta, lado a lado (formato de la planilla de la autora).

theta_si = t_int - tau,  tau = Rsi x (t_int - TDMN) / RT;  VERIFICA si theta_si > punto de rocio.
El punto de rocio del aire interior se calcula con la formula de Magnus (en lugar del grafico psicrometrico).
Libros: con formulas y (para AutoCAD) con valores fijos. Convenciones de formato: ver CLAUDE.md.
"""
import sys, math
sys.path.insert(0, "/home/user/tareas-claude/planillas/plantas")
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter as CL
import bordes

FUENTE = "Bahnschrift Light Condensed"
GRIS = PatternFill("solid", fgColor="D9D9D9")
GRIS_K = PatternFill("solid", fgColor="EDEDED")
AZUL = PatternFill("solid", fgColor="D9E2F3")
VERDE_F = PatternFill("solid", fgColor="C6E0B4")
C = Alignment(horizontal="center", vertical="center", wrap_text=True)
L = Alignment(horizontal="left", vertical="center", wrap_text=True)
RGT = Alignment(horizontal="right", vertical="center")
ALTO, ALTO_TITULO = 19.8, 28.4
FINA = Side(style="thin", color="000000")
BOX = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
VERDE, ROJO = "1E7A3C", "C00000"
TINT, TDMN, HR = 18.0, -4.0, 65.0
BRIMAX = "Ladrillo Brimax portante 18"

ELEMENTOS = [
 dict(titulo="CALCULO DE CONDENSACION SUPERFICIAL MURO", nombre="Muro exterior", rse=0.040, rsi=0.130, col0=1, capas=[
   ("Material de frente acrílico", None, 0.0, None),
   ("Mortero de cemento, cal y arena", None, 0.020, 0.930),
   ("Azotado hidráulico cemento arena e hidrófugo", None, 0.005, 1.130),
   (BRIMAX, None, 0.180, 0.120),
   ("Mortero de yeso monocapa", None, 0.020, 0.570),
   ("Latex Interior", None, 0.0, None)]),
 dict(titulo="CALCULO DE CONDENSACION SUPERFICIAL CUBIERTA", nombre="Cubierta", rse=0.040, rsi=0.100, col0=8, capas=[
   ("Pintura acrílica impermeable", None, 0.0, None),
   ("Membrana", 2000, 0.005, 0.700),
   ("Carpeta", 2000, 0.020, 1.130),
   ("Hormigón de pendiente c/ vermiculita", 600, 0.120, 0.160),
   ("Poliestireno expandido de alta densidad", 30, 0.060, 0.032),
   ("Barrera de vapor", None, 0.0, None),
   ("Hormigón armado de piedra H21 c/ armadura", 2400, 0.120, 1.630)]),
]

def ps(t): return 610.5 * math.exp(17.269 * t / (237.3 + t))
def rocio(t, hr):
    x = math.log(hr / 100.0 * ps(t) / 610.5)
    return 237.3 * x / (17.269 - x)

def calcular(el):
    rt = el["rse"] + el["rsi"] + sum(e / l for _, _, e, l in el["capas"] if l)
    dt = TINT - TDMN; tau = el["rsi"] * dt / rt; th = TINT - tau
    return dict(rt=rt, k=1 / rt, esp=sum(e for _, _, e, _ in el["capas"]), dt=dt, tau=tau, th=th, roc=rocio(TINT, HR), ok=th > rocio(TINT, HR))

def construir(ws, formulas):
    ws.sheet_view.showGridLines = False
    def f(c, b=False, color=None, size=12): c.font = Font(name=FUENTE, size=size, bold=b, color=color)
    anchos = {1: 7, 2: 52, 3: 15, 4: 15, 5: 15, 6: 15, 7: 4, 8: 7, 9: 52, 10: 15, 11: 15, 12: 15, 13: 15}
    for col, w in anchos.items(): ws.column_dimensions[CL(col)].width = w
    alt = {}                                    # altura de cada fila: la maxima pedida por cualquier bloque
    bloques = []
    for el in ELEMENTOS:
        d = calcular(el); o = el["col0"] - 1    # desplazamiento de columnas
        c_ = lambda k: CL(o + k)                # letra de la columna k (1..6) del bloque
        r = 1
        def fila(h=ALTO):
            nonlocal r
            alt[r] = max(alt.get(r, 0), h); r += 1; return r - 1
        def cel(rr, k, valor=None, negrita=False, alin=C, fmt=None, fill=None, color=None, caja=False, size=12):
            c = ws.cell(row=rr, column=o + k, value=valor); f(c, negrita, color, size); c.alignment = alin
            if fmt: c.number_format = fmt
            if fill: c.fill = fill
            if caja: c.border = BOX
            return c
        def mer(rr, k1, k2, valor=None, negrita=False, gris=False, alin=C, caja=True, fill=None):
            ws.merge_cells(start_row=rr, start_column=o + k1, end_row=rr, end_column=o + k2)
            c = cel(rr, k1, valor, negrita, alin)
            for k in range(k1, k2 + 1):
                x = ws.cell(row=rr, column=o + k)
                if caja: x.border = BOX
                if gris: x.fill = GRIS
                if fill: x.fill = fill
            return c
        rr = fila(ALTO_TITULO); mer(rr, 1, 6, el["titulo"], True, True)
        T0 = rr
        fila()
        rr = fila(); cel(rr, 2, el["nombre"], True, L, caja=True); mer(rr, 3, 6, "III Ciudad de Rosario / Pcia de Santa Fe")
        fila()
        rr = fila(ALTO_TITULO)
        for k, t in enumerate(["Capa", "Capa del elemento constructivo", "Densidad (Kg/m³)", "e (m)", "λ (W/mK)", "R (m²K/W)"], 1):
            cel(rr, k, t, True, L if k == 2 else C, fill=GRIS, caja=True)
        rr = fila(ALTO_TITULO); mer(rr, 1, 5, "Resistencia superficial exterior Rse", alin=L, gris=True); rse = rr
        cel(rr, 6, el["rse"], False, C, "0.000", GRIS, caja=True)
        primera = r
        for i, (nom, dens, e, lam) in enumerate(el["capas"], 1):
            rr = fila()
            cel(rr, 1, i, caja=True); cel(rr, 2, nom, alin=L, caja=True)
            cel(rr, 3, dens, fmt="0", caja=True); cel(rr, 4, e, fmt="0.000", caja=True); cel(rr, 5, lam, fmt="0.000", caja=True)
            cel(rr, 6, (("=%s%d/%s%d" % (c_(4), rr, c_(5), rr)) if formulas else e / lam) if lam else None, fmt="0.000", caja=True)
        ultima = r - 1
        rr = fila(ALTO_TITULO); mer(rr, 1, 5, "Resistencia superficial interior Rsi", alin=L, gris=True); rsi = rr
        cel(rr, 6, el["rsi"], False, C, "0.000", GRIS, caja=True)
        rr = fila(); mer(rr, 1, 3, "Espesor total aproximado", alin=L)
        cel(rr, 4, ("=SUM(%s%d:%s%d)" % (c_(4), primera, c_(4), ultima)) if formulas else d["esp"], fmt="0.000", caja=True); mer(rr, 5, 6, None)
        rr = fila(); mer(rr, 1, 5, "Resistencias térmicas totales R", alin=L); rt = rr
        cel(rr, 6, ("=%s%d+SUM(%s%d:%s%d)+%s%d" % (c_(6), rse, c_(6), primera, c_(6), ultima, c_(6), rsi)) if formulas else d["rt"], True, fmt="0.000", caja=True)
        fila()
        rr = fila(ALTO_TITULO); mer(rr, 1, 5, "Transmitancia térmica del componente K (W/m²K) = 1/R", alin=L); kk = rr
        cel(rr, 6, ("=1/%s%d" % (c_(6), rt)) if formulas else d["k"], False, C, "0.000", GRIS_K, VERDE, True)
        # ---- datos y calculo
        fila()
        ti = fila(); cel(ti, 1, "Temperatura interior del local", alin=L); ws.merge_cells(start_row=ti, start_column=o + 1, end_row=ti, end_column=o + 2)
        cel(ti, 3, "t int=", True, RGT); cel(ti, 4, TINT, fmt="0", caja=True); cel(ti, 5, "°C", alin=L)
        fila()
        tm = fila(); cel(tm, 1, "Temperatura mínima de diseño de invierno", alin=L); ws.merge_cells(start_row=tm, start_column=o + 1, end_row=tm, end_column=o + 2)
        cel(tm, 3, "TDMN=", True, RGT); cel(tm, 4, TDMN, fmt="0", caja=True); cel(tm, 5, "°C", alin=L)
        fila()
        dt = fila(); cel(dt, 3, "Δt = tint − TDMN =", True, RGT); ws.merge_cells(start_row=dt, start_column=o + 3, end_row=dt, end_column=o + 4)
        cel(dt, 5, ("=%s%d-%s%d" % (c_(4), ti, c_(4), tm)) if formulas else d["dt"], fmt="0", caja=True); cel(dt, 6, "°C", alin=L)
        fila()
        ta = fila(); cel(ta, 1, "Disminución de la temp. en la sup. int. del cerramiento", alin=L); ws.merge_cells(start_row=ta, start_column=o + 1, end_row=ta, end_column=o + 2)
        cel(ta, 3, "τ = (Rsi × Δt) / Rt =", True, RGT); ws.merge_cells(start_row=ta, start_column=o + 3, end_row=ta, end_column=o + 4)
        cel(ta, 5, ("=%s%d*%s%d/%s%d" % (c_(6), rsi, c_(5), dt, c_(6), rt)) if formulas else d["tau"], fmt="0.0", caja=True); cel(ta, 6, "°C", alin=L)
        th = fila(); cel(th, 1, "Temperatura de la cara interior del muro", alin=L); ws.merge_cells(start_row=th, start_column=o + 1, end_row=th, end_column=o + 2)
        cel(th, 3, "H = tint − τ", True, RGT); ws.merge_cells(start_row=th, start_column=o + 3, end_row=th, end_column=o + 4)
        cel(th, 5, ("=%s%d-%s%d" % (c_(4), ti, c_(5), ta)) if formulas else d["th"], fmt="0.0", fill=AZUL, caja=True); cel(th, 6, "°C (a)", alin=L)
        fila()
        ro0 = fila(); cel(ro0, 1, "Temperatura de rocío del aire int. (fórmula de Magnus)", alin=L); ws.merge_cells(start_row=ro0, start_column=o + 1, end_row=ro0 + 1, end_column=o + 2)
        ws.cell(row=ro0, column=o + 1).alignment = L
        cel(ro0, 3, "°C", True, caja=True); cel(ro0, 4, "%HR", True, caja=True)
        ro = ro0 + 1; fila()
        cel(ro, 3, ("=%s%d" % (c_(4), ti)) if formulas else TINT, fmt="0", caja=True); cel(ro, 4, HR, fmt="0", caja=True)
        ws.merge_cells(start_row=ro0, start_column=o + 5, end_row=ro, end_column=o + 5)
        mg = "{h}/100*610.5*EXP(17.269*{t}/(237.3+{t}))/610.5"
        inner = mg.format(h="%s%d" % (c_(4), ro), t="%s%d" % (c_(3), ro))
        magnus = "=237.3*LN(%s)/(17.269-LN(%s))" % (inner, inner)
        cel(ro0, 5, magnus if formulas else d["roc"], fmt="0.0", fill=VERDE_F, caja=True); ws.cell(row=ro, column=o + 5).border = BOX
        cel(ro0, 6, "°C (b)", alin=L); ws.merge_cells(start_row=ro0, start_column=o + 6, end_row=ro, end_column=o + 6)
        fila()
        h2 = fila(); cel(h2, 4, "°C (a)", True, caja=True); cel(h2, 6, "°C (b)", True, caja=True)
        rel = fila(); cel(rel, 1, "Relación entre las temperaturas de cálculo", alin=L); ws.merge_cells(start_row=rel, start_column=o + 1, end_row=rel, end_column=o + 3)
        cel(rel, 4, ("=%s%d" % (c_(5), th)) if formulas else d["th"], fmt="0.0", fill=AZUL, caja=True); cel(rel, 5, ">")
        cel(rel, 6, ("=%s%d" % (c_(5), ro0)) if formulas else d["roc"], fmt="0.0", fill=VERDE_F, caja=True)
        rc = fila(ALTO_TITULO)
        mer(rc, 1, 3, "CONDICIÓN VÁLIDA e/ LAS TEMPERATURAS", True, True, L, caja=False)
        cel(rc, 4, "t. interior del muro", True, fill=GRIS); cel(rc, 5, ">", True, fill=GRIS); cel(rc, 6, "t. punto de rocío", True, fill=GRIS)
        fila()
        rv_ = fila(ALTO_TITULO)
        cel(rv_, 5, ('=IF(%s%d>%s%d,"VERIFICA","NO VERIFICA")' % (c_(5), th, c_(5), ro0)) if formulas else ("VERIFICA" if d["ok"] else "NO VERIFICA"),
            False, C, fill=VERDE_F if d["ok"] else PatternFill("solid", fgColor="F4B6B6"), color=VERDE if d["ok"] else ROJO, caja=True)
        if formulas:
            ws.conditional_formatting.add("%s%d" % (c_(5), rv_), CellIsRule(operator="equal", formula=['"NO VERIFICA"'], font=Font(name=FUENTE, bold=True, color=ROJO), fill=PatternFill("solid", bgColor="F4B6B6")))
        fila()
        a0 = fila(); mer(a0, 1, 6, "Cálculos auxiliares:", alin=L)
        pv = HR / 100 * ps(TINT)
        aux = ["ps(%g °C) = 610,5 × e^(17,269 × %g / (237,3 + %g)) = %.0f Pa" % (TINT, TINT, TINT, ps(TINT)),
               "p = HR × ps = %g %% × %.0f = %.0f Pa" % (HR, ps(TINT), pv),
               "θr = 237,3 × ln(p / 610,5) / (17,269 − ln(p / 610,5)) = %.1f °C" % d["roc"]]
        for t in aux:
            rr = fila(); mer(rr, 1, 6, t, alin=L)
        bloques.append((T0, r - 1, o, kk, rv_))
    for rr, h in alt.items(): ws.row_dimensions[rr].height = h
    bordes.aplicar(ws)
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

for nombre, formulas in (("Condensacion superficial.xlsx", True), ("Condensacion superficial (para AutoCAD).xlsx", False)):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Condensacion superficial"
    construir(ws, formulas); wb.save(nombre)
for el in ELEMENTOS:
    d = calcular(el)
    print("%-45s RT=%.3f K=%.3f tau=%.2f theta_si=%.1f rocio=%.1f %s" % (el["titulo"], d["rt"], d["k"], d["tau"], d["th"], d["roc"], "VERIFICA" if d["ok"] else "NO"))
