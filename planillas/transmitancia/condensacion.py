# -*- coding: utf-8 -*-
"""Calculo de condensacion superficial (muro y cubierta), IRAM 11625.

theta_si = t_int - tau,  tau = Rsi x (t_int - TDMN) / RT;  verifica si theta_si > punto de rocio.
Punto de rocio del aire interior con la formula de Magnus (en lugar del grafico psicrometrico).
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
TINT, TDMN, HR = 18.0, -4.0, 65.0
BRIMAX = "Ladrillo Brimax portante 18"

ELEMENTOS = [
 dict(titulo="CALCULO DE CONDENSACION SUPERFICIAL MURO", nombre="Muro exterior", rse=0.040, rsi=0.130, capas=[
   ("Material de frente acrílico", None, 0.0, None),
   ("Mortero de cemento, cal y arena", None, 0.015, 0.930),
   ("Azotado hidráulico cemento arena e hidrófugo", None, 0.005, 1.130),
   (BRIMAX, None, 0.180, 0.120),
   ("Mortero de yeso monocapa", None, 0.020, 0.570),
   ("Latex Interior", None, 0.0, None)]),
 dict(titulo="CALCULO DE CONDENSACION SUPERFICIAL CUBIERTA", nombre="Cubierta", rse=0.040, rsi=0.100, capas=[
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
    def f(c, b=False, color=None): c.font = Font(name=FUENTE, size=12, bold=b, color=color)
    for col, w in zip("ABCDEF", (8, 56, 17, 13, 13, 16)): ws.column_dimensions[col].width = w
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
        rr = fila(ALTO_TITULO); mer(rr, 1, 6, el["titulo"], True, True)
        rr = fila(); c = ws.cell(row=rr, column=2, value=el["nombre"]); f(c, True); c.alignment = L
        mer(rr, 3, 6, "III Ciudad de Rosario / Pcia de Santa Fe")
        rr = fila(ALTO_TITULO)
        for k, t in enumerate(["Capa", "Capa del elemento constructivo", "Densidad (Kg/m³)", "e (m)", "λ (W/mK)", "R (m²K/W)"], 1):
            c = ws.cell(row=rr, column=k, value=t); f(c, True); c.fill = GRIS; c.alignment = L if k == 2 else C
        rr = fila(); mer(rr, 1, 5, "Resistencia superficial exterior Rse", alin=L); rse = rr; ws.cell(row=rr, column=6, value=el["rse"])
        primera = r
        for i, (nom, dens, e, lam) in enumerate(el["capas"], 1):
            rr = fila()
            ws.cell(row=rr, column=1, value=i); ws.cell(row=rr, column=2, value=nom)
            if dens: ws.cell(row=rr, column=3, value=dens)
            ws.cell(row=rr, column=4, value=e)
            if lam:
                ws.cell(row=rr, column=5, value=lam)
                ws.cell(row=rr, column=6, value=("=D%d/E%d" % (rr, rr)) if formulas else e / lam)
        ultima = r - 1
        rr = fila(); mer(rr, 1, 5, "Resistencia superficial interior Rsi", alin=L); rsi = rr; ws.cell(row=rr, column=6, value=el["rsi"])
        rr = fila(); mer(rr, 1, 3, "Espesor total aproximado", alin=L); esp = rr
        ws.cell(row=rr, column=4, value=("=SUM(D%d:D%d)" % (primera, ultima)) if formulas else d["esp"]); mer(rr, 5, 6)
        rr = fila(); mer(rr, 1, 5, "Resistencias térmicas totales R", True, alin=L); rt = rr
        ws.cell(row=rr, column=6, value=("=F%d+SUM(F%d:F%d)+F%d" % (rse, primera, ultima, rsi)) if formulas else d["rt"])
        rr = fila(); mer(rr, 1, 5, "Transmitancia térmica del componente K (W/m²K) = 1/R", alin=L); kk = rr
        ws.cell(row=rr, column=6, value=("=1/F%d" % rt) if formulas else d["k"])
        # ---- datos y calculo
        def calc(lbl, simbolo, valor, unidad, fmt="0.0", negrita=False):
            rr = fila(); mer(rr, 1, 3, lbl, alin=L)
            c = ws.cell(row=rr, column=4, value=simbolo); c.alignment = C; f(c)
            c = ws.cell(row=rr, column=5, value=valor); c.alignment = C; f(c, negrita); c.number_format = fmt
            c = ws.cell(row=rr, column=6, value=unidad); c.alignment = C; f(c)
            return rr
        ti = calc("Temperatura interior del local", "t int =", TINT, "°C", "0")
        tm = calc("Temperatura mínima de diseño de invierno", "TDMN =", TDMN, "°C", "0")
        dt = calc("Δt = tint − TDMN", "Δt =", ("=E%d-E%d" % (ti, tm)) if formulas else d["dt"], "°C", "0")
        ta = calc("Disminución de la temp. en la sup. int. del cerramiento: τ = (Rsi × Δt) / Rt", "τ =", ("=F%d*E%d/F%d" % (rsi, dt, rt)) if formulas else d["tau"], "°C")
        th = calc("Temperatura de la cara interior (a): θsi = tint − τ", "θsi =", ("=E%d-E%d" % (ti, ta)) if formulas else d["th"], "°C (a)", "0.0", True)
        hr = calc("Humedad relativa interior", "HR =", HR, "%", "0")
        ro = calc("Temperatura de rocío del aire interior (b), con la fórmula de Magnus", "θr =",
                  ("=237.3*LN(E{h}/100*610.5*EXP(17.269*E{t}/(237.3+E{t}))/610.5)/(17.269-LN(E{h}/100*610.5*EXP(17.269*E{t}/(237.3+E{t}))/610.5))".format(h=hr, t=ti)) if formulas else d["roc"],
                  "°C (b)", "0.0", True)
        rr = fila(); mer(rr, 1, 3, "Relación entre las temperaturas de cálculo", alin=L)
        c = ws.cell(row=rr, column=4, value=("=E%d" % th) if formulas else d["th"]); c.alignment = C; f(c); c.number_format = "0.0"
        c = ws.cell(row=rr, column=5, value=">"); c.alignment = C; f(c)
        c = ws.cell(row=rr, column=6, value=("=E%d" % ro) if formulas else d["roc"]); c.alignment = C; f(c); c.number_format = "0.0"
        rel = rr
        rr = fila(ALTO_TITULO); mer(rr, 1, 3, "CONDICIÓN VÁLIDA e/ LAS TEMPERATURAS: t interior del muro > t punto de rocío", True, True, L)
        for k in (4, 5, 6): ws.cell(row=rr, column=k).fill = GRIS; ws.cell(row=rr, column=k).border = box
        mer(rr, 4, 6, ('=IF(E%d>E%d,"VERIFICA","NO VERIFICA")' % (th, ro)) if formulas else ("VERIFICA" if d["ok"] else "NO VERIFICA"), True, True)
        res = rr; f(ws.cell(row=res, column=4), True, VERDE if d["ok"] else ROJO)
        if formulas:
            ws.conditional_formatting.add("D%d" % res, CellIsRule(operator="equal", formula=['"NO VERIFICA"'], font=Font(name=FUENTE, bold=True, color=ROJO)))
            ws.conditional_formatting.add("D%d" % res, CellIsRule(operator="equal", formula=['"VERIFICA"'], font=Font(name=FUENTE, bold=True, color=VERDE)))
        # calculos auxiliares
        rr = fila(); mer(rr, 1, 6, "Cálculos auxiliares:", True, alin=L)
        pv = HR / 100 * ps(TINT)
        aux = ["ps(%g °C) = 610,5 × e^(17,269 × %g / (237,3 + %g)) = %.0f Pa" % (TINT, TINT, TINT, ps(TINT)),
               "p = HR × ps = %g %% × %.0f = %.0f Pa" % (HR, ps(TINT), pv),
               "θr = 237,3 × ln(p / 610,5) / (17,269 − ln(p / 610,5)) = %.1f °C" % d["roc"]]
        for t in aux:
            rr = fila(); mer(rr, 1, 6, t, alin=L)
        # formatos de las capas
        for rrr in range(primera, ultima + 1):
            for k in range(1, 7):
                c = ws.cell(row=rrr, column=k); f(c); c.alignment = L if k == 2 else C
            for k in (4, 5, 6): ws.cell(row=rrr, column=k).number_format = "0.000"
        for rrr in (rse, rsi, rt, kk):
            f(ws.cell(row=rrr, column=6), rrr in (rt,)); ws.cell(row=rrr, column=6).alignment = C; ws.cell(row=rrr, column=6).number_format = "0.000"
        f(ws.cell(row=kk, column=6), True, VERDE); f(ws.cell(row=esp, column=4)); ws.cell(row=esp, column=4).alignment = C; ws.cell(row=esp, column=4).number_format = "0.000"
        for rrr in range(R0, r):
            for k in range(1, 7): ws.cell(row=rrr, column=k).border = box
        r += 1
    bordes.aplicar(ws)
    ws.page_setup.orientation = "portrait"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

for nombre, formulas in (("Condensacion superficial.xlsx", True), ("Condensacion superficial (para AutoCAD).xlsx", False)):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Condensacion superficial"
    construir(ws, formulas); wb.save(nombre)
for el in ELEMENTOS:
    d = calcular(el)
    print("%-45s RT=%.3f K=%.3f tau=%.2f theta_si=%.1f rocio=%.1f %s" % (el["titulo"], d["rt"], d["k"], d["tau"], d["th"], d["roc"], "VERIFICA" if d["ok"] else "NO"))
