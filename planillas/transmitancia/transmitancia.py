# -*- coding: utf-8 -*-
"""Verificacion de transmitancia termica, norma IRAM 11601 (cuatro cerramientos).

Genera dos libros:
  Verificacion transmitancia IRAM 11601.xlsx                 (con formulas)
  Verificacion transmitancia IRAM 11601 (para AutoCAD).xlsx  (valores fijos)

R de cada capa = e / lambda; R total = suma (incluye Rse y Rsi); K = 1 / R total;
cumple si K <= K maxima admisible (Nivel B).
Formato de las planillas del proyecto: ver CLAUDE.md.
"""
import sys
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
TITULO = "VERIFICACIÓN DE TRANSMITANCIA TÉRMICA NORMA IRAM 11601"
BRIMAX = "Ladrillo Brimax portante 18"
LAMBDA_BRIMAX = 0.120     # la misma conductividad que ya se usa para el Brimax 20x60x5 (a confirmar con la ficha)

# capa: (nombre, densidad, espesor, lambda)
def mur(mortero):
    return [("Material de frente acrílico", None, 0.0, None),
            ("Mortero de cemento, cal y arena", None, mortero, 0.930),
            ("Azotado hidráulico cemento arena e hidrófugo", None, 0.005, 1.130),
            (BRIMAX, None, 0.180, LAMBDA_BRIMAX),
            ("Mortero de yeso monocapa", None, 0.020, 0.570),
            ("Latex Interior", None, 0.0, None)]

ELEMENTOS = [
 dict(nombre="Pared Exterior", flujo="Horizontal", rse=0.040, rsi=0.130, kmax=0.740, capas=mur(0.020)),
 dict(nombre="Pared Exterior B", flujo="Horizontal", rse=0.040, rsi=0.130, kmax=0.740, capas=mur(0.015)),
 dict(nombre="Pared Exterior doble en vigas perimetrales", flujo="Horizontal", rse=0.040, rsi=0.130, kmax=0.740, capas=[
    ("Hidrorepelente transparente", None, 0.0, None),
    ("Hormigón armado de piedra H21 c/ armadura", 2400, 0.120, 0.930),
    ("Pintura asfáltica ormiflex profesional", None, 0.0, None),
    ("Poliestireno expandido de alta densidad", 30, 0.025, 0.035),
    ("Ladrillo brimax 20x60x5", None, 0.050, 0.120),
    ("Malla fibra de vidrio", None, 0.0, None),
    ("Mortero de yeso monocapa", None, 0.020, 0.570)]),
 dict(nombre="Techo sobre planta alta", flujo="Vertical", rse=0.040, rsi=0.100, kmax=0.380, capas=[
    ("Pintura acrílica impermeable", None, 0.0, None),
    ("Membrana", 2000, 0.005, 0.700),
    ("Carpeta", 2000, 0.020, 1.130),
    ("Hormigón de pendiente c/ espumígeno", 300, 0.140, 0.090),
    ("Poliestireno expandido de alta densidad", 30, 0.030, 0.032),
    ("Barrera de vapor polietileno 200 micrones", None, 0.0, None),
    ("Hormigón armado de piedra H21 c/ armadura", 2400, 0.120, 1.630)]),
]

def calcular(el):
    r = sum(e / l for _, _, e, l in el["capas"] if l) + el["rse"] + el["rsi"]
    esp = sum(e for _, _, e, _ in el["capas"])
    return r, 1 / r, esp, (1 / r) <= el["kmax"]

def construir(ws, formulas):
    ws.sheet_view.showGridLines = False
    def f(c, b=False, color=None): c.font = Font(name=FUENTE, size=12, bold=b, color=color)
    for col, w in zip("ABCDE", (62, 17, 14, 14, 16)): ws.column_dimensions[col].width = w
    r = 1
    for el in ELEMENTOS:
        R0 = r
        def fila(h=ALTO):
            nonlocal r
            ws.row_dimensions[r].height = h; r += 1; return r - 1
        def mer(rr, c1, c2, valor, negrita=False, gris=False, alin=C):
            ws.merge_cells(start_row=rr, start_column=c1, end_row=rr, end_column=c2)
            c = ws.cell(row=rr, column=c1, value=valor); f(c, negrita); c.alignment = alin
            for k in range(c1, c2 + 1):
                x = ws.cell(row=rr, column=k)
                if gris: x.fill = GRIS
                x.border = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
            return c
        rr = fila(ALTO_TITULO); mer(rr, 1, 5, TITULO, True, True)
        rr = fila(); c = ws.cell(row=rr, column=1, value="Elemento"); f(c, True); c.fill = GRIS; c.alignment = L
        mer(rr, 2, 3, "Época del año", True, True); mer(rr, 4, 5, "Flujo del calor", True, True)
        rr = fila(); c = ws.cell(row=rr, column=1, value=el["nombre"]); f(c); c.alignment = L
        mer(rr, 2, 3, "Invierno-Verano"); mer(rr, 4, 5, el["flujo"])
        rr = fila(); c = ws.cell(row=rr, column=1, value="Zona Bioambiental"); f(c, True); c.alignment = L
        mer(rr, 2, 5, "III Ciudad de Rosario / Pcia de Santa Fe")
        rr = fila(ALTO_TITULO)
        for k, t in enumerate(["Capa del elemento constructivo", "Densidad (Kg/m³)", "e (m)", "λ (W/mK)", "R (m²K/W)"], 1):
            c = ws.cell(row=rr, column=k, value=t); f(c, True); c.fill = GRIS; c.alignment = C if k > 1 else L
        # Rse
        rr = fila(); mer(rr, 1, 4, "Resistencia superficial exterior Rse", alin=L)
        rse = rr; ws.cell(row=rr, column=5, value=el["rse"])
        primera = r
        for nom, dens, e, lam in el["capas"]:
            rr = fila()
            ws.cell(row=rr, column=1, value=nom)
            if dens: ws.cell(row=rr, column=2, value=dens)
            ws.cell(row=rr, column=3, value=e)
            if lam:
                ws.cell(row=rr, column=4, value=lam)
                ws.cell(row=rr, column=5, value=("=C%d/D%d" % (rr, rr)) if formulas else e / lam)
            for k in range(1, 6):
                c = ws.cell(row=rr, column=k); f(c); c.alignment = L if k == 1 else C
                c.border = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
        ultima = r - 1
        rr = fila(); mer(rr, 1, 4, "Resistencia superficial interior Rsi", alin=L); rsi = rr
        ws.cell(row=rr, column=5, value=el["rsi"])
        rr = fila(); mer(rr, 1, 2, "Espesor total aproximado", alin=L); esp = rr
        ws.cell(row=rr, column=3, value=("=SUM(C%d:C%d)" % (primera, ultima)) if formulas else calcular(el)[2])
        mer(rr, 4, 5, None)
        rr = fila(); mer(rr, 1, 4, "Resistencias térmicas totales R", True, alin=L); rt = rr
        ws.cell(row=rr, column=5, value=("=E%d+SUM(E%d:E%d)+E%d" % (rse, primera, ultima, rsi)) if formulas else calcular(el)[0])
        rr = fila(); mer(rr, 1, 4, "Transmitancia térmica del componente K (W/m²K) = 1/R", alin=L); kk = rr
        ws.cell(row=rr, column=5, value=("=1/E%d" % rt) if formulas else calcular(el)[1])
        rr = fila(); mer(rr, 1, 4, "Transmitancia máxima admisible s/reglamento edificación Nivel B (W/m²K)", True, alin=L); km = rr
        ws.cell(row=rr, column=5, value=el["kmax"])
        rr = fila(ALTO_TITULO); mer(rr, 1, 4, "Cumple con el reglamento de edificación de Rosario", True, True, L); cu = rr
        cumple = calcular(el)[3]
        ws.cell(row=rr, column=5, value=('=IF(E%d<=E%d,"SI","NO")' % (kk, km)) if formulas else ("SI" if cumple else "NO"))
        # formatos
        for rrr in [rse, rsi] + list(range(primera, ultima + 1)) + [rt, kk, km, cu, esp]:
            for k in range(1, 6):
                c = ws.cell(row=rrr, column=k)
                if c.font.name != FUENTE: f(c, rrr in (rt, km, cu))
                if k > 1 and c.alignment.horizontal is None: c.alignment = C
        for rrr in list(range(primera, ultima + 1)) + [rse, rsi, rt, kk]:
            ws.cell(row=rrr, column=5).number_format = "0.000"
        for rrr in range(primera, ultima + 1):
            ws.cell(row=rrr, column=3).number_format = "0.000"; ws.cell(row=rrr, column=4).number_format = "0.000"
        ws.cell(row=esp, column=3).number_format = "0.000"; ws.cell(row=km, column=5).number_format = "0.000"
        for rrr, b in ((kk, True), (cu, True)):
            f(ws.cell(row=rrr, column=5), b, VERDE if (cumple) else ROJO)
        ws.cell(row=cu, column=5).fill = GRIS
        if formulas:
            ws.conditional_formatting.add("E%d:E%d" % (kk, cu), CellIsRule(operator="equal", formula=['"NO"'], font=Font(name=FUENTE, bold=True, color=ROJO)))
            ws.conditional_formatting.add("E%d" % cu, CellIsRule(operator="equal", formula=['"SI"'], font=Font(name=FUENTE, bold=True, color=VERDE)))
        # bordes de todas las celdas del bloque y convencion del proyecto
        for rrr in range(R0, r):
            for k in range(1, 6):
                ws.cell(row=rrr, column=k).border = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
        r += 1    # fila en blanco entre una planilla y la siguiente
    bordes.aplicar(ws)
    ws.page_setup.orientation = "portrait"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

for nombre, formulas in (("Verificacion transmitancia IRAM 11601.xlsx", True),
                         ("Verificacion transmitancia IRAM 11601 (para AutoCAD).xlsx", False)):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Transmitancia"
    construir(ws, formulas)
    wb.save(nombre)
for el in ELEMENTOS:
    r, k, esp, ok = calcular(el)
    print("%-45s R=%.3f  K=%.3f  max=%.3f  %s" % (el["nombre"], r, k, el["kmax"], "SI" if ok else "NO"))
