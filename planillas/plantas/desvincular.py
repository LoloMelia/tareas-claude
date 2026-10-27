# -*- coding: utf-8 -*-
"""Deja el libro sin una sola formula: cada celda queda con su valor fijo.

Hace falta porque al pegar las planillas en AutoCAD las referencias a las
hojas de Datos se pierden y los datos desaparecen.
"""
import sys, openpyxl

original, recalculado, destino = sys.argv[1:4]
fmt = openpyxl.load_workbook(original)              # trae formato y formulas
val = openpyxl.load_workbook(recalculado, data_only=True)   # trae los valores

cambiadas = faltantes = 0
for hoja in fmt.sheetnames:
    a, b = fmt[hoja], val[hoja]
    for fila in a.iter_rows():
        for c in fila:
            if not (isinstance(c.value, str) and c.value.startswith("=")):
                continue
            v = b.cell(row=c.row, column=c.column).value
            if v is None and c.value != "=":
                faltantes += 1
            c.value = v
            cambiadas += 1

# el formato condicional tambien apunta a otras celdas: se quita
for hoja in fmt.worksheets:
    hoja.conditional_formatting._cf_rules.clear()

fmt.save(destino)
print("formulas convertidas a valor:", cambiadas, "| sin valor:", faltantes)
