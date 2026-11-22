# -*- coding: utf-8 -*-
"""Verificacion de condensacion intersticial (Glaser), IRAM 11625: muro, muro con barrera de vapor y cubierta.

Para cada interfaz entre capas se calculan la temperatura T, la presion de vapor real rho, la temperatura
de rocio Tr de esa presion y la diferencia T - Tr. Hay condensacion donde T < Tr (diferencia negativa).
Libros: con formulas y (para AutoCAD) con valores fijos. Formato del proyecto: ver CLAUDE.md.
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
VERDE, ROJO = "1E7A3C", "C00000"
TI, HRI, TDMN, HRE = 18.0, 65.0, -4.0, 80.0
TITULO = "VERIFICACIÓN DE CONDENSACIÓN INTERSTICIAL NORMA IRAM 11625"
BRIMAX = "Ladrillo Brimax portante 18"

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
                esp=sum(e for _, _, e, _, _, _ in el["capas"]), cond=[i for i, f in enumerate(filas) if f[3] < 0])

def construir(ws, formulas):
    ws.sheet_view.showGridLines = False
    def f(c, b=False, color=None): c.font = Font(name=FUENTE, size=12, bold=b, color=color)
    for col, w in zip("ABCDEFGHIJKLMN", (50, 10, 9, 9, 10, 9, 15, 15, 15, 8, 9, 9, 10, 14)): ws.column_dimensions[col].width = w
    box = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
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
                x = ws.cell(row=rr, column=k); x.border = box
                if gris: x.fill = GRIS
            return c
        def num(rr, col, v, fmt="0.00", negrita=False):
            c = ws.cell(row=rr, column=col, value=v); f(c, negrita); c.alignment = C; c.number_format = fmt; return c
        rr = fila(ALTO_TITULO); mer(rr, 1, 14, TITULO, True, True)
        rr = fila(); mer(rr, 1, 5, "ELEMENTO", True, True); mer(rr, 6, 9, "ÉPOCA DEL AÑO", True, True); mer(rr, 10, 14, "FLUJO DE CALOR", True, True)
        rr = fila(); mer(rr, 1, 5, el["nombre"], True); mer(rr, 6, 9, "INVIERNO"); mer(rr, 10, 14, el["flujo"])
        rr = fila(); mer(rr, 1, 5, "ZONA BIOAMBIENTAL", alin=L); mer(rr, 6, 14, "IIIa - Ciudad de Rosario (Pcia. de Santa Fe)", True)
        rr = fila(ALTO_TITULO)
        enc = ["Capa del elemento constructivo", "Dens. (Kg/m³)", "e (m)", "λ (W/mK)", "R (m²K/W)", "T (°C)",
               "Permeab δ (g/m.h.kPa)", "Permean Δ (g/m².h.kPa)", "Rv (m².h.kPa/g)", "HR (%)", "ρ (kPa)", "Tr (°C)", "Dif. (Δt)", "¿Condensa?"]
        for k, t in enumerate(enc, 1):
            c = ws.cell(row=rr, column=k, value=t); f(c, True); c.fill = GRIS; c.alignment = L if k == 1 else C
        ws.row_dimensions[rr].height = 58
        # filas: se reservan los numeros de fila para poder referenciar hacia adelante
        n = len(el["capas"])
        r_air = r; r_rsi = r + 1; r_int0 = r + 2
        r_capa = [r + 3 + 2 * i for i in range(n)]          # fila de cada capa
        r_if = [r + 4 + 2 * i for i in range(n)]            # interfaz posterior a cada capa
        r_rse = r + 3 + 2 * n; r_ext = r_rse + 1; r_esp = r_ext + 1; r_res = r_esp + 1; r_k = r_res + 1
        r_vap = r_k + 1; r_fin = r_vap + 1
        RT = "$E$%d" % r_res; RVT = "$E$%d" % r_vap
        # aire interior
        fila(); mer(r_air, 1, 5, "Temperatura interior del aire", alin=L)
        num(r_air, 6, TI, "0"); num(r_air, 10, HRI, "0")
        pi_f = "=J%d/100*0.6105*EXP(17.269*F%d/(237.3+F%d))" % (r_air, r_air, r_air)
        num(r_air, 11, pi_f if formulas else d["pi"])
        def trf(rr): return "=IF(K{r}>=0.6105,237.3*LN(K{r}/0.6105)/(17.269-LN(K{r}/0.6105)),265.5*LN(K{r}/0.6105)/(21.875-LN(K{r}/0.6105)))".format(r=rr)
        def ifila(rr, idx):
            t, p, trr, dif = d["filas"][idx]
            return t, p, trr, dif
        num(r_air, 12, trf(r_air) if formulas else tr(d["pi"])); num(r_air, 13, ("=F%d-L%d" % (r_air, r_air)) if formulas else TI - tr(d["pi"]))
        # Rsi + interfaz de la superficie interior
        fila(); mer(r_rsi, 1, 4, "Resistencia superficial interior Rsi", alin=L); num(r_rsi, 5, el["rsi"], "0.000")
        def interfaz(rr, idx, etiqueta, hasta_capa_row):
            fila(ALTO)
            c = ws.cell(row=rr, column=1, value=etiqueta); f(c); c.alignment = L; c.font = Font(name=FUENTE, size=10, italic=True)
            t, p, trr, dif = d["filas"][idx]
            if formulas:
                num(rr, 6, "=$F$%d-($F$%d-$F$%d)*SUM($E$%d:E%d)/%s" % (r_air, r_air, r_ext, r_rsi, hasta_capa_row, RT))
                first = r_capa[0]
                num(rr, 11, ("=$K$%d-($K$%d-$K$%d)*SUM($I$%d:I%d)/%s" % (r_air, r_air, r_ext, first, hasta_capa_row, RVT)) if idx > 0 else "=$K$%d" % r_air)
                num(rr, 12, trf(rr)); num(rr, 13, "=F%d-L%d" % (rr, rr))
                num(rr, 14, '=IF(M%d<0,"CONDENSA","")' % rr, "@", True)
            else:
                num(rr, 6, t); num(rr, 11, p); num(rr, 12, trr); num(rr, 13, dif)
                num(rr, 14, "CONDENSA" if dif < 0 else "", "@", True)
            f(ws.cell(row=rr, column=14), True, ROJO)
        interfaz(r_int0, 0, "  Superficie interior del cerramiento", r_rsi)
        for i, (nom, dens, e, lam, dl, DD) in enumerate(el["capas"]):
            rr = r_capa[i]; fila()
            ws.cell(row=rr, column=1, value=nom)
            if dens: num(rr, 2, dens, "0")
            num(rr, 3, e, "0.000")
            if lam:
                num(rr, 4, lam, "0.000"); num(rr, 5, ("=C%d/D%d" % (rr, rr)) if formulas else e / lam, "0.000")
            if dl: num(rr, 7, dl, "0.0000")
            if DD: num(rr, 8, DD, "0.000")
            v = rv(e, dl, DD)
            num(rr, 9, ("=IF(H{r}>0,1/H{r},IF(AND(G{r}>0,C{r}>0),C{r}/G{r},0))".format(r=rr)) if formulas else v, "0.00")
            c = ws.cell(row=rr, column=1); f(c); c.alignment = L
            interfaz(r_if[i], i + 1, "  Cara exterior de: " + nom, rr)
        fila(); mer(r_rse, 1, 4, "Resistencia superficial exterior Rse", alin=L); num(r_rse, 5, el["rse"], "0.000")
        fila(); mer(r_ext, 1, 5, "Temperatura de diseño mínima TDMN para Rosario (Zona bioclimática IIIa)", alin=L)
        num(r_ext, 6, TDMN, "0"); num(r_ext, 10, HRE, "0")
        pe_f = "=J%d/100*IF(F%d>=0,0.6105*EXP(17.269*F%d/(237.3+F%d)),0.6105*EXP(21.875*F%d/(265.5+F%d)))" % ((r_ext,) * 6)
        num(r_ext, 11, pe_f if formulas else d["pe"]); num(r_ext, 12, trf(r_ext) if formulas else tr(d["pe"])); num(r_ext, 13, ("=F%d-L%d" % (r_ext, r_ext)) if formulas else TDMN - tr(d["pe"]))
        fila(); mer(r_esp, 1, 2, "Espesor total aproximado", alin=L)
        num(r_esp, 3, ("=SUM(C%d:C%d)" % (r_capa[0], r_capa[-1])) if formulas else d["esp"], "0.000")
        mer(r_esp, 4, 14, None)
        # sumas de resistencias
        fila(); mer(r_res, 1, 4, "Resistencias totales   TÉRMICA   Rt (m²K/W)", True, alin=L)
        num(r_res, 5, ("=E%d+E%d+SUM(E%d:E%d)" % (r_rsi, r_rse, r_capa[0], r_capa[-1])) if formulas else d["rt"], "0.000", True)
        mer(r_res, 6, 8, "Δt = tint − TDMN (°C)", alin=L); num(r_res, 9, ("=F%d-F%d" % (r_air, r_ext)) if formulas else d["dt"], "0", True)
        mer(r_res, 10, 14, None)
        fila(); mer(r_k, 1, 4, "K (W/m²K) = 1 / Rt", alin=L); num(r_k, 5, ("=1/E%d" % r_res) if formulas else d["k"], "0.000", True)
        mer(r_k, 6, 14, None)
        fila(); mer(r_vap, 1, 4, "Resistencias totales   AL VAPOR   RVt (m².h.kPa/g)", True, alin=L)
        num(r_vap, 5, ("=SUM(I%d:I%d)" % (r_capa[0], r_capa[-1])) if formulas else d["rvt"], "0.00", True)
        mer(r_vap, 6, 8, "Δρ = ρi − ρe (kPa)", alin=L)
        num(r_vap, 9, ("=K%d-K%d" % (r_air, r_ext)) if formulas else d["dp"], "0.00", True)
        mer(r_vap, 10, 14, None)
        fila(ALTO_TITULO); mer(r_fin, 1, 5, "CONDENSACIÓN INTERSTICIAL (hay condensación donde T < Tr, es decir, diferencia negativa)", True, True, L)
        rng = "N%d:N%d" % (r_int0, r_if[-1])
        resultado = '=IF(COUNTIF(%s,"CONDENSA")>0,"HAY CONDENSACIÓN","NO HAY CONDENSACIÓN")' % rng
        mer(r_fin, 6, 14, resultado if formulas else ("HAY CONDENSACIÓN" if d["cond"] else "NO HAY CONDENSACIÓN"), True, True)
        f(ws.cell(row=r_fin, column=6), True, ROJO if d["cond"] else VERDE)
        if formulas:
            ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"CONDENSA"'], font=Font(name=FUENTE, bold=True, color=ROJO)))
            ws.conditional_formatting.add("F%d" % r_fin, CellIsRule(operator="equal", formula=['"HAY CONDENSACIÓN"'], font=Font(name=FUENTE, bold=True, color=ROJO)))
            ws.conditional_formatting.add("F%d" % r_fin, CellIsRule(operator="equal", formula=['"NO HAY CONDENSACIÓN"'], font=Font(name=FUENTE, bold=True, color=VERDE)))
        for rrr in range(R0, r):
            for k in range(1, 15):
                x = ws.cell(row=rrr, column=k)
                if x.font.name != FUENTE: f(x)
                x.border = box
        r += 1
    bordes.aplicar(ws)
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

for nombre, formulas in (("Condensacion intersticial.xlsx", True), ("Condensacion intersticial (para AutoCAD).xlsx", False)):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Condensacion intersticial"
    construir(ws, formulas); wb.save(nombre)
for el in ELEMENTOS:
    d = calcular(el)
    print("%-38s Rt=%.3f K=%.3f RVt=%.2f dp=%.2f  condensa en %s" % (el["nombre"], d["rt"], d["k"], d["rvt"], d["dp"],
          [("interior" if i == 0 else el["capas"][i - 1][0][:28], round(d["filas"][i][3], 2)) for i in d["cond"]] or "ninguna"))
