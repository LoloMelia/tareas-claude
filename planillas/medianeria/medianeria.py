# -*- coding: utf-8 -*-
"""Planilla para la liquidacion de derechos de medianeria.

Reproduce la planilla de ejemplo (captura) con sus datos. Las columnas
calculadas llevan formulas; las de entrada (medidas, costos, antiguedad, estado,
vida util y coeficiente de Ross-Heidecke) son valores.
"""
import sys
sys.path.insert(0, "/home/user/tareas-claude/planillas/plantas")
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import bordes

FUENTE = "Bahnschrift Light Condensed"
GRIS = PatternFill("solid", fgColor="D9D9D9")
C = Alignment(horizontal="center", vertical="center", wrap_text=True)
L = Alignment(horizontal="left", vertical="center", wrap_text=True)
R90 = Alignment(horizontal="center", vertical="center", text_rotation=90, wrap_text=True)
ALTO = 19.8          # 0,7 cm
ALTO_TITULO = 28.4   # 1 cm
MONEDA = '_("$"* #,##0.00_);_("$"* \\(#,##0.00\\);_("$"* "-"??_);_(@_)'

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Medianeria"
ws.sheet_view.showGridLines = False

def f(c, b=False):
    c.font = Font(name=FUENTE, size=12, bold=b)

# --- cabecera de la hoja
ws["A1"] = "LIQUIDACIÓN DE LOS DERECHOS DE MEDIANERÍA."; f(ws["A1"])
ws["I1"] = "PRECIOS MES DE DICIEMBRE 2022"; f(ws["I1"])

ENC = 4  # fila del banner
ws.merge_cells(start_row=ENC, start_column=1, end_row=ENC + 1, end_column=1)
ws.cell(row=ENC, column=1, value="ITEMS DEL MURO")
ws.merge_cells(start_row=ENC, start_column=2, end_row=ENC, end_column=17)
ws.cell(row=ENC, column=2, value="PLANILLA PARA LA LIQUIDACIÓN DE DERECHOS DE MEDIANERÍA")
ws.merge_cells(start_row=ENC, start_column=18, end_row=ENC + 1, end_column=18)
ws.cell(row=ENC, column=18, value="Observaciones")

titulos = ["Largo (m)", "Alto (m)", "Ancho (m)", "Cómputo Métrico", "Coste unitario",
           "Impuesto al Valor Agregado ( IVA )", "Precio unitario", "Valor de Reposición",
           "Antigüedad en años del muro", "Estado del muro", "Vida útil del muro",
           "Porcentual de la edad respecto a la vida útil", "Valor residual",
           "Depreciación (Coeficiente de Ross-Heidecke)", "Valor actual del muro en pesos",
           "Total a liquidar en pesos"]
for i, t in enumerate(titulos):
    ws.cell(row=ENC + 1, column=2 + i, value=t)
for col in range(1, 19):
    for r in (ENC, ENC + 1):
        c = ws.cell(row=r, column=col); c.fill = GRIS; f(c, False)
        c.alignment = R90 if (r == ENC + 1 and 2 <= col <= 17) else C

# --- items: (nombre, largo, alto, ancho, formula_computo, coste, antig, estado, vida, residual?, dep)
IVA = 0.21
items = [
 ("Excavación de cimientos",              9.81, 1.2, 0.45, "=B{r}*C{r}*D{r}", 4207.13, 17, None, None, False, None),
 ("Banquina de hormigón sin armar",       9.81, 0.3, 0.45, "=B{r}*C{r}*D{r}", 51585.77, 17, 2, 90, False, 13.54),
 ("Mampostería de cimientos de 45cm",     9.81, 0.3, 0.45, "=B{r}*C{r}*D{r}", 37585.31, 17, 2, 90, False, 13.54),
 ("Encadenado de cimientos (H°A°)",       9.74, 0.2, 0.3,  "=B{r}*C{r}*D{r}", 5184.10, 17, 2, 90, False, 13.54),
 ("Mampostería de cimientos de 30m",      9.74, 0.7, 0.3,  "=B{r}*C{r}*D{r}", 37585.31, 17, 2, 50, False, 24.73),
 ("Doble capa aisladora horizontal y vertical", 9.74, 0.3, 0.24, "=B{r}*2*(C{r}+D{r})", 1743.65, 17, 2, 90, False, 13.54),
 ("Mampostería de elevación",              49.0, None, 0.3, "=B{r}*D{r}", 37585.31, 17, 2, 90, True, 13.54),
 ("Revoque exterior (I+J+E)",             49.0, None, None, "=B{r}", 4160.39, 17, 2, 40, False, 32.49),
 ("Revoque interior  (J+E)",              49.0, None, None, "=B{r}", 3194.01, 17, 2, 60, False, 19.99),
]
R0 = ENC + 2
for k, (nom, lg, al, an, fc, coste, ant, est, vida, resid, dep) in enumerate(items):
    r = R0 + k
    ws.cell(row=r, column=1, value=nom)
    ws.cell(row=r, column=2, value=lg)
    if al is not None: ws.cell(row=r, column=3, value=al)
    if an is not None: ws.cell(row=r, column=4, value=an)
    else: ws.cell(row=r, column=4, value="-")
    ws.cell(row=r, column=5, value=fc.format(r=r))
    ws.cell(row=r, column=6, value=coste)
    ws.cell(row=r, column=7, value="=ROUND(F%d*%s,2)" % (r, IVA))
    ws.cell(row=r, column=8, value="=F%d+G%d" % (r, r))
    ws.cell(row=r, column=9, value="=E%d*H%d" % (r, r))
    ws.cell(row=r, column=10, value=ant)
    ws.cell(row=r, column=11, value=est if est is not None else "-")
    ws.cell(row=r, column=12, value=vida if vida is not None else "-")
    ws.cell(row=r, column=13, value=("=J%d/L%d" % (r, r)) if vida else "-")
    ws.cell(row=r, column=14, value=("=ROUND(I%d*0.05,2)" % r) if resid else "-")
    ws.cell(row=r, column=15, value=dep if dep is not None else "-")
    # el ejemplo resuelve el valor actual como (reposicion - residual) x (coef - 1) - residual
    if dep is None:
        ws.cell(row=r, column=16, value="=I%d" % r)
    else:
        ws.cell(row=r, column=16, value=("=(I%d-N%d)*(O%d-1)-N%d" % (r, r, r, r)) if resid
                else "=I%d*(O%d-1)" % (r, r))
    ws.cell(row=r, column=17, value="=P%d/2" % r)
    # formatos
    for col in (2, 3, 4): ws.cell(row=r, column=col).number_format = "0.00"
    ws.cell(row=r, column=5).number_format = "0.0####"
    for col in (6, 7, 8, 9, 16, 17): ws.cell(row=r, column=col).number_format = MONEDA
    ws.cell(row=r, column=14).number_format = MONEDA
    ws.cell(row=r, column=13).number_format = "0%"
    ws.cell(row=r, column=15).number_format = "0.00"
    for col in range(1, 19):
        c = ws.cell(row=r, column=col); f(c)
        c.alignment = L if col in (1, 18) else C
        if col == 18: c.value = None
    if lg == 49.0 and al is None:           # largo y alto combinados en una sola celda
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)

RN = R0 + len(items) - 1
RT = RN + 1
ws.merge_cells(start_row=RT, start_column=1, end_row=RT, end_column=16)
ws.cell(row=RT, column=1, value="TOTAL A LIQUIDAR POR DERECHOS DE MEDIANERÍA")
ws.cell(row=RT, column=17, value="=SUM(Q%d:Q%d)" % (R0, RN)).number_format = MONEDA
for col in range(1, 18):
    c = ws.cell(row=RT, column=col); c.fill = GRIS; f(c, False)
    c.alignment = C

# --- totales de reposicion y honorarios
RV = RT + 2
ws.merge_cells(start_row=RV, start_column=5, end_row=RV, end_column=8)
ws.cell(row=RV, column=5, value="Valor de Reposición total")
ws.cell(row=RV, column=9, value="=SUM(I%d:I%d)" % (R0, RN)).number_format = MONEDA
ws.merge_cells(start_row=RV + 1, start_column=5, end_row=RV + 1, end_column=8)
ws.cell(row=RV + 1, column=5, value="Honorarios (10%)")
ws.cell(row=RV + 1, column=9, value="=ROUND(I%d*0.1,2)" % RV).number_format = MONEDA
for r in (RV, RV + 1):
    for col in range(5, 10):
        c = ws.cell(row=r, column=col); f(c); c.alignment = C

# --- notas al pie
RNOTA = RV + 4
ws.merge_cells(start_row=RNOTA, start_column=1, end_row=RNOTA, end_column=17)
ws.cell(row=RNOTA, column=1, value="NOTA: En el monto definido está incluido el IVA correspondiente. "
        "Los honorarios profesionales, un 10% (Diez por ciento) del valor de reposición del muro, se liquidan por separado.")
ws.cell(row=RNOTA, column=1).alignment = C
f(ws.cell(row=RNOTA, column=1))
textos = [
 'Por lo tanto el Sr. "A" abonará al Sr. "1" la mitad del valor actual del muro depreciado según lo indicado en la Planilla superior, o sea la suma de '
 'Once millones, ochocientos veintidós mil quinientos cincuenta y un pesos con sesenta y dos centavos para lo cual se extiende el siguiente recibo de pago.',
 'En prueba de conformidad se firman 3 (tres) ejemplares de un mismo tenor y a un solo efecto, en la ciudad de Rosario, (Pcia. De Santa Fe) a los 10 días '
 'del mes de Enero del año 2023, quedando el original en poder del Sr. "A", el duplicado en poder del Sr. "1", y el triplicado en poder del Arquitecto Liquidador.',
]
for i, t in enumerate(textos):
    r = RNOTA + 2 + i
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=17)
    ws.cell(row=r, column=1, value=t).alignment = L
    f(ws.cell(row=r, column=1))
    ws.row_dimensions[r].height = 54

# --- medidas
anchos = {1: 46, 2: 10, 3: 10, 4: 10, 5: 14, 6: 18, 7: 18, 8: 18, 9: 20, 10: 12, 11: 10,
          12: 10, 13: 14, 14: 18, 15: 18, 16: 22, 17: 22, 18: 26}
from openpyxl.utils import get_column_letter
for col, w in anchos.items():
    ws.column_dimensions[get_column_letter(col)].width = w
for r in range(1, ws.max_row + 1):
    ws.row_dimensions[r].height = ALTO
ws.row_dimensions[ENC].height = ALTO_TITULO
ws.row_dimensions[ENC + 1].height = 175
ws.row_dimensions[RT].height = ALTO_TITULO
for r in (RNOTA + 2, RNOTA + 3): ws.row_dimensions[r].height = 54
ws.row_dimensions[RNOTA].height = ALTO

# --- bordes: tabla principal, fila de total, cuadro de totales y nota
FINA = Side(style="thin", color="000000")
def marco(r1, r2, c1, c2):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ws.cell(row=r, column=c).border = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
marco(ENC, RT, 1, 18)
marco(RV, RV + 1, 5, 9)
marco(RNOTA, RNOTA, 1, 17)
bordes.aplicar(ws)

ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(sys.argv[1] if len(sys.argv) > 1 else "Planilla medianeria.xlsx")
print("filas", ws.max_row, "datos", R0, "-", RN, "total", RT)
