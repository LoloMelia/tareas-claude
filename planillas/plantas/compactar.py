# -*- coding: utf-8 -*-
"""Version para pegar en AutoCAD: sin formulas, sin filas vacias, mas baja.

Se reconstruye hoja por hoja copiando solo las filas con contenido, porque
borrar filas en el lugar descoloca las celdas combinadas y las imagenes.
"""
import copy, io, sys, math, openpyxl
import bordes
from openpyxl.drawing.image import Image as XLImage
from openpyxl.worksheet.pagebreak import Break
from openpyxl.utils import get_column_letter

ALTO = 19.8        # 0,7 cm en puntos
ALTO_TITULO = 28.4  # 1 cm: filas de titulo (las que llevan relleno gris)


def _rotulo_croquis(c):
    return isinstance(c.value, str) and c.value.startswith("Ubicacion en planta")

TOPE = 160.0      # salvo que el texto no entre

# columnas de carga manual, que no tienen sentido una vez congelado el libro
AUXILIARES = {"Balance termico": (8, 9)}

origen, destino = sys.argv[1:3]
wb = openpyxl.load_workbook(origen)
nuevo = openpyxl.Workbook(); nuevo.remove(nuevo.active)

for hoja in wb.sheetnames:
    o = wb[hoja]
    aux = AUXILIARES.get(hoja, ())
    d = nuevo.create_sheet(hoja)
    d.sheet_view.showGridLines = o.sheet_view.showGridLines

    # filas con algo escrito (una combinada cuenta por su celda de arriba)
    llenas = set()
    for fila in o.iter_rows():
        if any(c.value not in (None, "") for c in fila
               if c.column not in aux and not _rotulo_croquis(c)):
            llenas.add(fila[0].row)
    for m in o.merged_cells.ranges:
        if m.min_row in llenas:
            llenas.update(range(m.min_row, m.max_row + 1))
    orden = sorted(llenas)
    # en el balance se deja una fila en blanco entre un bloque y el siguiente
    mapa = {}; n_fila = 0; primero = True
    for v in orden:
        n_fila += 1
        a = o.cell(row=v, column=1).value
        if hoja == "Balance termico" and isinstance(a, str) and a.startswith("LOCAL"):
            if not primero:
                n_fila += 1
            primero = False
        mapa[v] = n_fila

    anchos = {}
    for letra, dim in o.column_dimensions.items():
        for i in range(dim.min or 1, (dim.max or dim.min or 1) + 1):
            if i in aux:
                continue
            l = get_column_letter(i)
            nd = d.column_dimensions[l]
            nd.width = dim.width; nd.hidden = dim.hidden
            anchos[l] = dim.width or 10

    for vieja in orden:
        for c in o[vieja]:
            if c.column in aux or _rotulo_croquis(c):
                continue
            n = d.cell(row=mapa[vieja], column=c.column, value=c.value)
            n.font = copy.copy(c.font); n.fill = copy.copy(c.fill)
            n.border = copy.copy(c.border); n.alignment = copy.copy(c.alignment)
            n.number_format = c.number_format

    for m in o.merged_cells.ranges:
        if m.min_row in mapa and m.max_row in mapa:
            d.merge_cells(start_row=mapa[m.min_row], end_row=mapa[m.max_row],
                          start_column=m.min_col, end_column=m.max_col)

    # alto: 0,7 cm, y solo crece si el texto no entra en el ancho de la celda
    combinadas = {}
    for m in d.merged_cells.ranges:
        ancho = sum(anchos.get(get_column_letter(i), 10)
                    for i in range(m.min_col, m.max_col + 1))
        combinadas[(m.min_row, m.min_col)] = ancho
    for fila in d.iter_rows():
        alto = ALTO
        for c in fila:
            if not isinstance(c.value, str) or not c.value.strip():
                continue
            if not (c.alignment and c.alignment.wrap_text):
                continue
            ancho = combinadas.get((c.row, c.column), anchos.get(c.column_letter, 10))
            tam = c.font.size or 11
            # la negrita ocupa mas, asi que se estima con menos caracteres
            caracteres = max(1, int(ancho * (9.0 if c.font.bold else 10.8) / tam))
            renglones = sum(max(1, math.ceil(len(t) / caracteres))
                            for t in c.value.split("\n"))
            alto = max(alto, renglones * (tam * 1.25) + 2)
        titulo = any(c.fill is not None and c.fill.patternType == "solid"
                     and (c.fill.fgColor.rgb or "")[-6:].upper() not in ("FFFFFF", "")
                     for c in fila)
        if titulo:
            # 1 cm, salvo que el texto pida tres renglones o mas
            alto = ALTO_TITULO if alto < 45 else alto
        d.row_dimensions[fila[0].row].height = round(min(alto, TOPE), 1)

    # los esquemas (imagenes sueltas sobre las celdas) se llevan a su fila nueva;
    # la fila crece lo justo para que la imagen entre sin pisar a la vecina
    if hoja != "Balance termico":
        for im in o._images:
            fila0 = im.anchor._from.row + 1
            if fila0 not in mapa:
                continue
            nueva = mapa[fila0]
            img = XLImage(io.BytesIO(im._data()))
            img.width, img.height = im.width, im.height
            img.anchor = "%s%d" % (get_column_letter(im.anchor._from.col + 1), nueva)
            d.add_image(img)
            necesario = round(im.height * 0.75 + 3, 1)
            actual = d.row_dimensions[nueva].height or ALTO
            if necesario > actual:
                d.row_dimensions[nueva].height = necesario

    # en el balance, cada local empieza en una pagina nueva
    if hoja == "Balance termico":
        for v in orden:
            a1 = o.cell(row=v, column=1).value
            if isinstance(a1, str) and a1.startswith("LOCAL") and mapa[v] > 3:
                d.row_breaks.append(Break(id=mapa[v] - 2))
    d.page_setup.orientation = o.page_setup.orientation
    d.page_setup.fitToWidth = o.page_setup.fitToWidth
    d.page_setup.fitToHeight = 0
    d.sheet_properties.pageSetUpPr.fitToPage = True
    bordes.aplicar(d)
    print("%-28s %4d filas -> %4d" % (hoja, o.max_row, len(orden)))

nuevo.save(destino)
