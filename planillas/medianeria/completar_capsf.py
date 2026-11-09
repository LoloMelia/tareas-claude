# -*- coding: utf-8 -*-
"""Completa la planilla del CAPSF (Informe modelo medianeria, jun-2025) con el simulacro.

Usa LibreOffice por UNO (soffice --accept=socket,host=localhost,port=2002;urp;) para
conservar las imagenes, formatos y formulas del modelo. Uso:
    python3 completar_capsf.py <modelo.xls> <salida.xlsx>
"""
import sys, uno, os
from com.sun.star.beans import PropertyValue
from com.sun.star.awt import Point, Size

modelo, salida = [os.path.abspath(a) for a in sys.argv[1:3]]
AQUI = os.path.dirname(os.path.abspath(__file__))

def pv(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p

local = uno.getComponentContext()
resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
doc = desktop.loadComponentFromURL("file://" + modelo, "_blank", 0, (pv("Hidden", True),))
S = doc.Sheets

def num(sh, ref, v): S.getByName(sh).getCellRangeByName(ref).setValue(v)
def txt(sh, ref, v): S.getByName(sh).getCellRangeByName(ref).String = v
def frm(sh, ref, v): S.getByName(sh).getCellRangeByName(ref).Formula = v
def limpiar(sh, rng): S.getByName(sh).getCellRangeByName(rng).clearContents(1 | 2 | 4 | 16)

# ---------------- 1-caratula ----------------
txt("1-caratula", "D13", "")                      # comitente: a completar
txt("1-caratula", "D14", "Casa I+B - SIMULACRO de medianería")
txt("1-caratula", "D15", "Lote 230, Barrio Vida, Funes, Santa Fe")
txt("1-caratula", "D51", "FUNES, NOVIEMBRE DE 2026")

# ---------------- 3-computo: muro del patio, 16,25 x 0,30 x 3,00 (15 cm de cada lado del eje medianero)
C = "3-computo"
L = 16.25
txt(C, "C16", "sector A.B"); num(C, "E16", L); num(C, "F16", 0.45); num(C, "G16", 1.0)          # excavacion
txt(C, "C20", "sector A.B"); num(C, "E20", L); num(C, "F20", 0.45); num(C, "G20", 0.30)         # zapata corrida
num(C, "E22", L); num(C, "F22", 0.45); num(C, "G22", 0.30)                                      # mamposteria de fundacion
sh = S.getByName(C)
sh.copyRange(sh.getCellRangeByName("C23").CellAddress, sh.getCellRangeByName("C22:K22").RangeAddress)
num(C, "E23", L); num(C, "F23", 0.30); num(C, "G23", 0.40)
frm(C, "J21", "=+I22+I23")
txt(C, "C26", "sector A.B.F.G"); num(C, "E26", L); num(C, "F26", 0.30); num(C, "G26", 3.00)     # elevacion (un solo sector)
limpiar(C, "C28:K29")
num(C, "D33", 2); num(C, "E33", L); num(C, "F33", 0.30)                                         # capa horizontal
num(C, "D35", 2); num(C, "E35", L); num(C, "F35", 0.20)                                         # capa vertical
txt(C, "C39", "sector A.B.F.G"); num(C, "E39", L); num(C, "G39", 3.00)                          # revoque interior
limpiar(C, "C40:K40")
txt(C, "C42", "sector A.B.F.G"); num(C, "E42", L); num(C, "G42", 3.00)                          # revoque exterior
limpiar(C, "C43:K43")

# ---------------- 5-val.reposicion: antiguedad 13 anios, estado 2,5 (como la clase), residual 5 % solo en la mamposteria de elevacion
V = "5-val.reposicion"
sv = S.getByName(V)
sv.getColumns().getByName("G").IsVisible = True
for col in "GHIJKL": sv.getColumns().getByName(col).IsVisible = True
# coeficientes de la tabla de Ross-Heidecke, estado 1, segun la edad en % de cada rubro
KT = {20: 15.42, 21: 15.42, 22: 15.42,   # 13/90 = 14 %
      23: 28.26,                          # horizontal 13/40 = 33 %
      24: 23.14,                          # vertical 13/50 = 26 %
      25: 28.26,                          # revoque exterior 13/40 = 33 %
      26: 20.42}                          # revoque interior 13/60 = 22 %
for r in range(19, 27):
    num(V, "H%d" % r, 13); num(V, "I%d" % r, 2.5)
for r, k in KT.items(): num(V, "K%d" % r, k)
num(V, "G22", 5)                      # valor residual 5 % en la mamposteria de elevacion, como en la clase

# ---------------- 2-croquis: se reemplazan los dibujos del ejemplo por los del simulacro
Q = S.getByName("2-croquis"); dp = Q.DrawPage
for k in range(dp.Count - 1, -1, -1):
    s = dp.getByIndex(k)
    if s.Position.Y > 4000 and s.Position.Y < 20000:   # los dos croquis del ejemplo (no la cabecera ni el pie)
        dp.remove(s)
def imagen(archivo, x, y, w, h):
    g = doc.createInstance("com.sun.star.drawing.GraphicObjectShape")
    g.GraphicURL = "file://" + os.path.join(AQUI, archivo)
    dp.add(g); g.Position = Point(x, y); g.Size = Size(w, h)
imagen("esquema_planta.png", 600, 4800, 8674, 6490)
imagen("esquema_corte.png", 400, 12400, 15800, 4900)
txt("2-croquis", "D10", "Lote 230, Barrio Vida, Funes (muro del patio, lado SO)")
txt("2-croquis", "G27", "Sr. A: en condominio")
txt("2-croquis", "H27", "sobre 3,00 m: Sr. B")
limpiar("2-croquis", "Q27")

doc.storeToURL("file://" + salida, (pv("FilterName", "Calc MS Excel 2007 XML"),))
doc.close(True)
print("guardado", salida)
