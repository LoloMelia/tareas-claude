# -*- coding: utf-8 -*-
"""Genera, para cada local, una imagen de la planta con ese local sombreado.

El plano trae una polilinea roja cerrada por local y el rotulo en rojo adentro.
Se rellena desde el rotulo hacia afuera hasta chocar con el rojo, que hace de
borde, y se apaga el rojo de los demas locales.
"""
import collections, sys
import numpy as np
import pdfplumber
from PIL import Image
from scipy import ndimage

DPI = 200
GRIS = (120, 120, 120)      # color del sombreado
ALFA = 0.33                 # transparencia
BLANCO = (255, 255, 255)    # las marcas rojas de los demas locales desaparecen
BORDE = (110, 110, 110)     # el contorno del local sombreado, gris y fino
ROTULO = (40, 40, 40)       # el nombre del local
NEGRO = (0, 0, 0)           # mesadas, bachas y demas dibujos de color

def rotulos(pdf):
    """Agrupa las palabras del plano en un rotulo por local.

    El texto esta rotado, asi que un rotulo de dos renglones son dos columnas
    de palabras juntas. Se agrupan por cercania en las dos direcciones y se
    identifica cada local por su numero, o por el texto si no lo tiene.
    """
    pg = pdfplumber.open(pdf).pages[0]
    cajas = []
    for w in pg.extract_words():
        if w["text"] == "·":
            continue
        cajas.append([w["x0"], w["x1"], w["top"], w["bottom"], w["text"]])
    grupos = []
    for c in cajas:
        for g in grupos:
            if any(abs(c[0] - o[0]) < 12 and
                   c[2] < o[3] + 15 and o[2] < c[3] + 15 for o in g):
                g.append(c); break
        else:
            grupos.append([c])
    salida = {}
    for g in grupos:
        g.sort(key=lambda c: (c[0], c[2]))
        palabras = [c[4] for c in g]
        numeros = [p for p in palabras if p.isdigit()]
        clave = numeros[0] if numeros else " ".join(palabras)
        salida[clave] = (sum(c[0] + c[1] for c in g) / (2 * len(g)),
                         sum(c[2] + c[3] for c in g) / (2 * len(g)))
    return salida, pg.width, pg.height

def mascara_roja(a, umbral=45):
    """umbral alto: el trazo rojo. umbral bajo: tambien su halo antialias."""
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (r - np.maximum(g, b)) > umbral

def region(libre, semilla):
    """Rellena desde la semilla sobre los pixeles libres."""
    etiquetas, _ = ndimage.label(libre)
    e = etiquetas[semilla[1], semilla[0]]
    if e == 0:
        return None
    return etiquetas == e

def buscar_semilla(libre, px, py, radio=60):
    if libre[py, px]:
        return px, py
    for d in range(2, radio, 2):
        for dx, dy in ((d,0),(-d,0),(0,d),(0,-d),(d,d),(-d,-d),(d,-d),(-d,d)):
            x, y = px + dx, py + dy
            if 0 <= y < libre.shape[0] and 0 <= x < libre.shape[1] and libre[y, x]:
                return x, y
    return None

def generar(pdf, png, destino, locales, margen=0.07):
    """Una imagen por local, todas con el mismo encuadre."""
    rot, ancho_pt, _ = rotulos(pdf)
    base = Image.open(png).convert("RGB")
    a = np.array(base)
    f = base.width / ancho_pt
    roja = mascara_roja(a)
    halo = mascara_roja(a, 12)
    libre = ~halo
    comp, n = ndimage.label(roja, structure=np.ones((3, 3), int))

    # primera pasada: las regiones de cada local
    regiones = {}
    for clave, nombre in locales.items():
        if clave not in rot:
            print("  FALTA el rotulo", clave); continue
        cx, cy = rot[clave]
        s = buscar_semilla(libre, int(cx * f), int(cy * f))
        if s is None:
            print("  sin semilla libre para", clave); continue
        reg = region(libre, s)
        if reg is None or reg.sum() > 0.35 * reg.size:
            print("  el relleno se escapo en", clave); continue
        regiones[nombre] = reg

    # encuadre comun: la union de todos los locales mas un margen
    union = np.zeros_like(roja)
    for reg in regiones.values():
        union |= reg
    ys, xs = np.where(union)
    mx = int(margen * base.width)
    caja = (max(0, xs.min() - mx), max(0, ys.min() - mx),
            min(base.width, xs.max() + mx), min(base.height, ys.max() + mx))

    # todo lo que esta dibujado en color y no es rojo (mesadas, bachas) va a negro
    sat = (a.max(axis=2).astype(int) - a.min(axis=2).astype(int)) > 40
    color_ajeno = sat & ~roja

    resultados = {}
    for nombre, reg in regiones.items():
        conservar = np.zeros(n + 1, bool)
        for e in np.unique(comp[ndimage.binary_dilation(reg, iterations=3)]):
            if e: conservar[e] = True
        quedan = conservar[comp] & roja
        ys, xs = np.where(reg)
        alto_reg, ancho_reg = np.ptp(ys) + 1, np.ptp(xs) + 1

        salida = a.copy()
        cerca = ndimage.binary_dilation(quedan, iterations=2)
        salida[halo & ~cerca] = BLANCO           # el resto de las marcas, fuera
        salida[color_ajeno] = NEGRO              # mesadas y bachas en negro
        for e in np.unique(comp[quedan]):
            if not e: continue
            pieza = comp == e
            py, px = np.where(pieza)
            es_contorno = ((np.ptp(py) + 1) > 0.8 * alto_reg and
                           (np.ptp(px) + 1) > 0.8 * ancho_reg)
            salida[pieza] = BORDE if es_contorno else ROTULO
        for i in range(3):
            canal = salida[..., i].astype(float)
            canal[reg] = canal[reg] * (1 - ALFA) + GRIS[i] * ALFA
            salida[..., i] = canal.astype(np.uint8)
        Image.fromarray(salida).crop(caja).save("%s/%s.png" % (destino, nombre))
        resultados[nombre] = reg.sum() / f / f
        print("  %-22s ok" % nombre)
    return resultados


# superficie real de cada local, de la planilla de balance termico
SUPERFICIE = {"01-cocina": 27.16, "06-living": 35.16, "07-hall": 7.57,
              "08-vestidor": 7.23, "09-suite": 12.25, "10-bano-suite": 5.81,
              "11-bano-visitas": 3.12, "escalera": 7.02,
              "13-dormitorio-norte": 17.00, "14-play-room": 16.85,
              "15-dormitorio-sur": 14.18, "17-bano": 3.52}

PB = {"01": "01-cocina", "06": "06-living", "07": "07-hall", "08": "08-vestidor",
      "09": "09-suite", "10": "10-bano-suite", "11": "11-bano-visitas"}
PA = {"13": "13-dormitorio-norte", "14": "14-play-room", "ESCALERA": "escalera",
      "15": "15-dormitorio-sur", "17": "17-bano"}

if __name__ == "__main__":
    import os
    os.makedirs("pintadas", exist_ok=True)
    px = {}
    px.update(generar("plantas/pb.pdf", "plantas/pb200-1.png", "pintadas", PB))
    px.update(generar("plantas/pa.pdf", "plantas/pa200-1.png", "pintadas", PA))
    # control: la escala sale de la cocina y con ella se miden los demas
    if "01-cocina" in px:
        k = SUPERFICIE["01-cocina"] / px["01-cocina"]
        print("\n%-22s %8s %8s %7s" % ("local", "medido", "planilla", "dif"))
        for n, v in sorted(px.items()):
            m, p = v * k, SUPERFICIE.get(n)
            if p: print("%-22s %8.2f %8.2f %6.1f%%" % (n, m, p, 100 * (m - p) / p))
