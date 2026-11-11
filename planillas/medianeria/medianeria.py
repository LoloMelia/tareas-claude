# -*- coding: utf-8 -*-
"""Planilla para la liquidacion de derechos de medianeria, en el formato de la planilla de
ejemplo (la primera captura), cargada con el computo del grafico de la autora y los precios
unitarios del CAPSF (jun-2025, sin actualizar).

Coste unitario = precio CAPSF x 1,20 (10 % gastos generales + 10 % beneficio);
IVA 21 % sobre ese coste; precio unitario = coste + IVA (= precio CAPSF x 1,452).
Depreciacion: Ross-Heidecke, criterio del CAPSF, 13 anios y estado 2,5, residual 0 %.
"""
import sys
sys.path.insert(0, "/home/user/tareas-claude/planillas/plantas")
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import bordes

FUENTE = "Bahnschrift Light Condensed"
GRIS = PatternFill("solid", fgColor="D9D9D9")
C = Alignment(horizontal="center", vertical="center", wrap_text=True)
L_ = Alignment(horizontal="left", vertical="center", wrap_text=True)
R90 = Alignment(horizontal="center", vertical="center", text_rotation=90, wrap_text=True)
ALTO = 19.8; ALTO_TITULO = 28.4
MONEDA = '_("$"* #,##0.00_);_("$"* \\(#,##0.00\\);_("$"* "-"??_);_(@_)'
IVA = 0.21; GGB = 1.20
FINA = Side(style="thin", color="000000")
ANT, EST = 13, 2.5

TITULOS = ["Largo (m)", "Alto (m)", "Ancho (m)", "Cómputo Métrico", "Coste unitario",
           "Impuesto al Valor Agregado ( IVA )", "Precio unitario", "Valor de Reposición",
           "Antigüedad en años del muro", "Estado del muro", "Vida útil del muro",
           "Porcentual de la edad respecto a la vida útil", "Valor residual",
           "Depreciación (Coeficiente de Ross-Heidecke)", "Valor actual del muro en pesos",
           "Total a liquidar en pesos"]
ANCHOS = {1: 46, 2: 10, 3: 10, 4: 10, 5: 14, 6: 18, 7: 18, 8: 18, 9: 20, 10: 12, 11: 10,
          12: 10, 13: 14, 14: 18, 15: 18, 16: 22, 17: 22, 18: 36}

L = 15.98                                   # largo del cimiento (sector A'A - I'I)
SECT = [(3.63, 4.20), (6.33, 6.50), (6.00, 3.50)]    # (largo, alto) de los sectores de elevacion
AREA = "=3.63*4.2+6.33*6.5+6*3.5"           # area del perfil comun sobre el nivel +-0,00
OBS_SECT = "3,63x4,20 + 6,33x6,50 + 6,00x3,50"

# (nombre, largo, alto, ancho, formula, precio CAPSF jun-25, vida util, coef. Ross-Heidecke, observacion)
ITEMS = [
 ("Excavación de cimientos",                 L, 1.00, 0.45, "=B{r}*C{r}*D{r}", 30298.81246546,  None, None,  "sector A'A - I'I"),
 ("Zapata corrida hormigón de cascotes",     L, 0.30, 0.45, "=B{r}*C{r}*D{r}", 161870.029844038, 90, 15.42, "sector A'A - I'I"),
 ("Mampostería de fundación (0,45 x 0,30)",  L, 0.30, 0.45, "=B{r}*C{r}*D{r}", 229491.09209829,  90, 15.42, "sector A'A - I'I"),
 ("Mampostería de fundación (0,30 x 0,40)",  L, 0.40, 0.30, "=B{r}*C{r}*D{r}", 229491.09209829,  90, 15.42, "sector A'A - I'I"),
 ("Mampostería de elevación",                AREA, None, 0.30, "=B{r}*D{r}",    254069.47968799,  90, 15.42, OBS_SECT),
 ("Capa aisladora horizontal (doble)",       L, None, 0.30, "=B{r}*2*D{r}",    17211.6217668618, 50, 23.14, "2 capas x 15,98 x 0,30"),
 ("Capa aisladora vertical (doble)",         L, None, 0.20, "=B{r}*2*D{r}",    14957.6988685418, 40, 28.26, "2 capas x 15,98 x 0,20"),
 ("Revoque exterior (azotado+grueso+fino)",  AREA, None, None, "=B{r}",         24238.9833057592, 40, 28.26, OBS_SECT),
 ("Revoque interior (grueso+fino)",          AREA, None, None, "=B{r}",         17510.2560152792, 60, 20.42, OBS_SECT),
]

def palabras(n):
    u = ["cero","uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve","diez","once","doce",
         "trece","catorce","quince","dieciséis","diecisiete","dieciocho","diecinueve","veinte","veintiuno",
         "veintidós","veintitrés","veinticuatro","veinticinco","veintiséis","veintisiete","veintiocho","veintinueve"]
    d = ["","","","treinta","cuarenta","cincuenta","sesenta","setenta","ochenta","noventa"]
    c = ["","ciento","doscientos","trescientos","cuatrocientos","quinientos","seiscientos","setecientos","ochocientos","novecientos"]
    def menos_mil(n):
        if n == 0: return ""
        if n == 100: return "cien"
        s = []
        if n >= 100: s.append(c[n // 100]); n %= 100
        if n >= 30:
            t = d[n // 10]; s.append(t + (" y " + u[n % 10] if n % 10 else ""))
        elif n > 0: s.append(u[n])
        return " ".join(s)
    if n == 0: return "cero"
    mm, resto = divmod(n, 1000000); mil, uni = divmod(resto, 1000)
    out = []
    if mm: out.append("un millón" if mm == 1 else menos_mil(mm) + " millones")
    if mil: out.append("mil" if mil == 1 else menos_mil(mil) + " mil")
    if uni: out.append(menos_mil(uni))
    return " ".join(out).replace("uno mil", "un mil").replace("veintiuno mil", "veintiún mil")

def apocope(t):
    if t.endswith("veintiuno"): return t[:-9] + "veintiún"
    if t.endswith("uno"): return t[:-3] + "un"
    return t

def total_calculado():
    tot = 0.0
    for nom, lg, al, an, fc, capsf, vida, coef, obs in ITEMS:
        if isinstance(lg, str): lg = eval(lg[1:])
        if fc == "=B{r}*C{r}*D{r}": comp = lg * al * an
        elif fc == "=B{r}*D{r}": comp = lg * an
        elif fc == "=B{r}*2*D{r}": comp = lg * 2 * an
        else: comp = lg
        coste = capsf * GGB; iva = round(coste * IVA, 2); prec = coste + iva
        rep = comp * prec
        va = rep if coef is None else rep * (1 - coef / 100.0)
        tot += va / 2
    return tot

def construir(ws, monto):
    ws.sheet_view.showGridLines = False
    def f(c, b=False): c.font = Font(name=FUENTE, size=12, bold=b)
    ws["A1"] = "LIQUIDACIÓN DE LOS DERECHOS DE MEDIANERÍA."; f(ws["A1"])
    ws["I1"] = "VALORES CAPSF JUNIO 2025 (sin actualizar)"; f(ws["I1"])
    ws["A2"] = "SIMULACRO: muro medianero del patio (lado SO). Lote exento, sin medianera real."; f(ws["A2"])
    ENC = 4
    ws.merge_cells(start_row=ENC, start_column=1, end_row=ENC + 1, end_column=1)
    ws.cell(row=ENC, column=1, value="ITEMS DEL MURO")
    ws.merge_cells(start_row=ENC, start_column=2, end_row=ENC, end_column=17)
    ws.cell(row=ENC, column=2, value="PLANILLA PARA LA LIQUIDACIÓN DE DERECHOS DE MEDIANERÍA")
    ws.merge_cells(start_row=ENC, start_column=18, end_row=ENC + 1, end_column=18)
    ws.cell(row=ENC, column=18, value="Observaciones")
    for i, t in enumerate(TITULOS): ws.cell(row=ENC + 1, column=2 + i, value=t)
    for col in range(1, 19):
        for r in (ENC, ENC + 1):
            c = ws.cell(row=r, column=col); c.fill = GRIS; f(c)
            c.alignment = R90 if (r == ENC + 1 and 2 <= col <= 17) else C
    R0 = ENC + 2
    for k, (nom, lg, al, an, fc, capsf, vida, coef, obs) in enumerate(ITEMS):
        r = R0 + k
        ws.cell(row=r, column=1, value=nom)
        ws.cell(row=r, column=2, value=lg)
        if al is not None: ws.cell(row=r, column=3, value=al)
        ws.cell(row=r, column=4, value=an if an is not None else "-")
        ws.cell(row=r, column=5, value=fc.format(r=r))
        ws.cell(row=r, column=6, value="=%r*%s" % (capsf, GGB))
        ws.cell(row=r, column=7, value="=ROUND(F%d*%s,2)" % (r, IVA))
        ws.cell(row=r, column=8, value="=F%d+G%d" % (r, r))
        ws.cell(row=r, column=9, value="=E%d*H%d" % (r, r))
        ws.cell(row=r, column=10, value=ANT)
        ws.cell(row=r, column=11, value=EST if vida else "-")
        ws.cell(row=r, column=12, value=vida if vida else "-")
        ws.cell(row=r, column=13, value=("=J%d/L%d" % (r, r)) if vida else "-")
        ws.cell(row=r, column=14, value="-")
        ws.cell(row=r, column=15, value=coef if coef is not None else "-")
        ws.cell(row=r, column=16, value=("=I%d*(1-O%d/100)" % (r, r)) if coef is not None else "=I%d" % r)
        ws.cell(row=r, column=17, value="=P%d/2" % r)
        ws.cell(row=r, column=18, value=obs)
        for col in (2, 3, 4): ws.cell(row=r, column=col).number_format = "0.00"
        ws.cell(row=r, column=5).number_format = "0.0####"
        for col in (6, 7, 8, 9, 16, 17): ws.cell(row=r, column=col).number_format = MONEDA
        ws.cell(row=r, column=13).number_format = "0%"
        ws.cell(row=r, column=15).number_format = "0.00"
        for col in range(1, 19):
            c = ws.cell(row=r, column=col); f(c)
            c.alignment = L_ if col in (1, 18) else C
        if al is None:
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    RN = R0 + len(ITEMS) - 1; RT = RN + 1
    ws.merge_cells(start_row=RT, start_column=1, end_row=RT, end_column=16)
    ws.cell(row=RT, column=1, value="TOTAL A LIQUIDAR POR DERECHOS DE MEDIANERÍA")
    ws.cell(row=RT, column=17, value="=SUM(Q%d:Q%d)" % (R0, RN)).number_format = MONEDA
    for col in range(1, 18):
        c = ws.cell(row=RT, column=col); c.fill = GRIS; f(c); c.alignment = C
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
    RNOTA = RV + 4
    ws.merge_cells(start_row=RNOTA, start_column=1, end_row=RNOTA, end_column=17)
    ws.cell(row=RNOTA, column=1, value="NOTA: En el monto definido está incluido el IVA correspondiente. "
            "Los honorarios profesionales, un 10% (Diez por ciento) del valor de reposición del muro, se liquidan por separado.")
    ws.cell(row=RNOTA, column=1).alignment = C; f(ws.cell(row=RNOTA, column=1))
    textos = [
     "Coste unitario = precio unitario del CAPSF (junio de 2025, sin actualizar) por 1,20 (10% de gastos generales y 10% de beneficio). "
     "Precio unitario = coste unitario más 21% de IVA, es decir, precio del CAPSF por 1,452. Depreciación según la tabla de Ross-Heidecke, "
     "con " + str(ANT) + " años de antigüedad y estado " + str(EST).replace(".", ",") + "; valor residual 0%. Valor actual = valor de reposición x (1 - coeficiente / 100).",
     'Por lo tanto el Sr. "A" abonará al Sr. "1" la mitad del valor actual del muro depreciado según lo indicado en la Planilla superior, o sea la suma de '
     + monto + ", para lo cual se extiende el siguiente recibo de pago.",
     'En prueba de conformidad se firman 3 (tres) ejemplares de un mismo tenor y a un solo efecto, en la ciudad de Funes, (Pcia. De Santa Fe) a los ___ días '
     'del mes de __________ del año ______, quedando el original en poder del Sr. "A", el duplicado en poder del Sr. "1", y el triplicado en poder del Arquitecto Liquidador.',
    ]
    for i, t in enumerate(textos):
        r = RNOTA + 2 + i
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=17)
        ws.cell(row=r, column=1, value=t).alignment = L_; f(ws.cell(row=r, column=1))
    for col, w in ANCHOS.items(): ws.column_dimensions[get_column_letter(col)].width = w
    for r in range(1, ws.max_row + 1): ws.row_dimensions[r].height = ALTO
    ws.row_dimensions[ENC].height = ALTO_TITULO
    ws.row_dimensions[ENC + 1].height = 175
    ws.row_dimensions[RT].height = ALTO_TITULO
    for i in range(len(textos)): ws.row_dimensions[RNOTA + 2 + i].height = 54
    def marco(r1, r2, c1, c2):
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                ws.cell(row=r, column=c).border = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
    marco(ENC, RT, 1, 18); marco(RV, RV + 1, 5, 9); marco(RNOTA, RNOTA, 1, 17)
    bordes.aplicar(ws)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

tot = total_calculado()
entero = int(tot); cent = int(round((tot - entero) * 100))
monto = "%s pesos con %s centavos" % (apocope(palabras(entero)), apocope(palabras(cent)) if cent else "cero")
wb = openpyxl.Workbook()
ws = wb.active; ws.title = "Medianeria (simulacro)"
construir(ws, monto)
destino = sys.argv[1] if len(sys.argv) > 1 else "Planilla medianeria.xlsx"
wb.save(destino)
print("total a liquidar %.2f -> %s" % (tot, monto))
