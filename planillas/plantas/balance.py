# -*- coding: utf-8 -*-
"""Formulario de balance termico para calefaccion, un bloque por local.

Mismo formulario que la planilla modelo. Lo que se puede sacar de las otras
planillas viene cargado: superficie del local, volumen y las aberturas con su
medida. Las longitudes de pared se cargan a mano, en las columnas H e I.
"""
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
import os

ALTURA = 3.00   # piso a cielorraso, de los cortes de la planilla de carpinterias
# el cielorraso suspendido de yeso va a 2,80 en varios locales, pero los muros
# llegan a 3,00 y el espacio sobre el cielorraso esta dentro de la envolvente:
# la pared pierde calor en toda su altura, asi que se computa 3,00 en todos.
ALTURA_LOCAL = {}

# local -> (nombre, a, b, planta, aberturas [(nombre, alto, ancho)], paredes_ext)
LOCALES = [
 ("01 - Cocina / comedor", 7.63, 3.56, "PB",
   [("VA01",3.00,0.75),("PF03",3.00,2.88),("PF04",0.60,2.70),("PV02",3.00,2.48)], 2),
 ("06 - Living / comedor", 8.66, 4.06, "PB",
   [("PF02",3.00,3.75),("PV01",3.00,7.70)], 2),
 ("07 - Hall / ingreso",   4.00, 2.15, "PB", [("PF01",3.00,3.55),("H01",3.00,1.50)], 2),
 ("08 - Vestidor",         3.38, 1.66, "PB", [], 1),
 ("Escalera",              4.06, 1.73, "PB", [("PF05",2.52,0.75)], 1),
 ("09 - Dormitorio suite", 3.50, 3.50, "PB",
   [("VA01",3.00,0.75),("PV03",3.00,1.76)], 2),
 ("10 - Bano suite",       3.38, 1.72, "PB", [("VA02",2.15,0.75)], 1),
 ("11 - Bano visitas",     2.40, 1.30, "PB", [], 1),
 ("13 - Dormitorio Norte", 4.25, 4.00, "PA",
   [("VA04",2.52,2.00),("VA05",2.52,1.40)], 2),
 ("14 - Play room",        4.13, 4.08, "PA", [("VA04",2.52,2.00)], 2),
 ("15 - Dormitorio Sur",   3.50, 4.05, "PA",
   [("PV04",3.00,2.06)], 2),
 ("17 - Bano",             2.20, 1.60, "PA", [("VA03",2.52,0.75)], 1),
]
# locales en L: segundo rectangulo que se suma al principal
EXTRA = {"08 - Vestidor": (1.09, 1.49)}   # el vestidor es en L: 1,66 de ancho,
                                          # que se angosta a 1,09 en el ingreso
# muros cargados por el autor del proyecto: (largo, "ext"/"int", orientacion, a que da)
MUROS = {
 # La orientacion sale del plano de fachadas: cada muro hereda la fachada de la
 # abertura que lleva. Donde el muro es ciego, o donde la abertura entra en mas
 # de un muro del mismo local, queda sin rotular.
 "01 - Cocina / comedor": [(7.63,"ext","NO","PF03 y PV02"),(3.56,"ext","SO","PF04 y VA01"),
                           (7.63,"int","SE","galeria y living"),(3.56,"int","NE","deposito y lavadero")],
 "06 - Living / comedor": [(8.66,"ext","SE","PF02"),(4.06,"int","NE","cocina"),
                           (8.66,"int","NO","galeria, con la PV01"),(4.06,"int","SO","escalera")],
 "07 - Hall / ingreso":   [(4.00,"ext","SO","PF01, patio interior"),(2.15,"ext","SE","puerta de ingreso"),
                           (4.00,"int","NE","vestidor"),(2.15,"int","NO","living comedor")],
 "08 - Vestidor":          [(1.70,"ext","","tramo exterior del lado largo, ciego"),
                           (3.17,"int","","resto del lado largo"),
                           (3.38,"int","",""),(1.66,"int","",""),
                           (1.49,"int","",""),(1.09,"int","",""),(0.57,"int","","")],
 "09 - Dormitorio suite": [(3.50,"ext","NE","PV03"),(3.50,"ext","SO","VA01"),
                           (3.50,"ext","","muro ciego"),(3.50,"int","","")],
 "10 - Bano suite":       [(3.38,"ext","NE","VA02"),(1.72,"int","",""),
                           (3.38,"int","SO",""),(1.72,"int","","")],
 "11 - Bano visitas":     [(1.30,"ext","","muro ciego"),(2.40,"int","",""),
                           (2.40,"int","",""),(1.30,"int","","")],
 "Escalera":              [(4.06,"ext","NE","PF05"),
                           (1.73,"ext","",""),(4.06,"int","SO",""),(1.73,"int","","")],
 "13 - Dormitorio Norte": [(4.25,"ext","NO","VA04"),(4.25,"ext","SE","VA05"),
                           (4.00,"ext","","muro ciego"),(4.00,"int","","")],
 "14 - Play room":        [(4.13,"ext","NO","VA04"),(4.08,"int","NE",""),
                           (4.13,"int","SE","")],   # el otro 4,08 no es muro: es la baranda de la escalera
 "15 - Dormitorio Sur":   [(4.05,"ext","SE","PV04"),(3.50,"ext","","muro ciego"),
                           (4.05,"int","NO",""),(3.50,"int","","")],
 "17 - Bano":             [(2.20,"ext","NE","VA03"),
                           (1.60,"ext","",""),(2.20,"int","SO",""),(1.60,"int","","")],
}
PAREDES = {"08 - Vestidor": [4.87, 1.66, 3.38, 0.57, 1.49, 1.09]}
# locales sin emisor propio: su carga la cubre el radiador del local al que se abren
SIN_EMISOR = {"07 - Hall / ingreso": "06 - Living / comedor",
              "Escalera":            "14 - Play room"}
# croquis de planta con el local sombreado, uno por bloque
CROQUIS_DIR = "/home/user/tareas-claude/planillas/plantas"
CROQUIS = {"01 - Cocina / comedor": "01-cocina", "06 - Living / comedor": "06-living",
           "07 - Hall / ingreso": "07-hall", "08 - Vestidor": "08-vestidor",
           "09 - Dormitorio suite": "09-suite", "10 - Bano suite": "10-bano-suite",
           "11 - Bano visitas": "11-bano-visitas", "Escalera": "escalera",
           "13 - Dormitorio Norte": "13-dormitorio-norte", "14 - Play room": "14-play-room",
           "15 - Dormitorio Sur": "15-dormitorio-sur", "17 - Bano": "17-bano"}
ANCHO_CROQUIS = 460   # pixeles; el alto sale de la proporcion de la imagen
ALTO_FILA_PT = 39.7   # la altura de fila que aplica el libro, en puntos
TOALLERO = {"10 - Bano suite", "11 - Bano visitas", "17 - Bano"}
MUROS_EXT = 4   # renglones en blanco: los muros que dan al exterior
MUROS_INT = 4   # vienen precargados con los cuatro lados del local

def agregar(wb):
    thin=Side(style="thin",color="000000"); med=Side(style="medium",color="000000")
    BOX=Border(left=thin,right=thin,top=thin,bottom=thin)
    G1=PatternFill("solid",fgColor="D9D9D9"); G2=PatternFill("solid",fgColor="EDEDED")
    PEND=PatternFill("solid",fgColor="FCE4D6")
    C=Alignment(horizontal="center",vertical="center",wrap_text=True)
    L=Alignment(horizontal="left",vertical="center",wrap_text=True)

    ws=wb.create_sheet("Balance termico"); ws.sheet_view.showGridLines=False
    for col,w in zip("ABCDEFGHI",(6,34,20,12,10,20,3,10,10)):
        ws.column_dimensions[col].width=w

    def celda(r,c,v=None,b=False,al=C,fill=None,fmt=None,borde=True):
        x=ws.cell(row=r,column=c,value=v)
        x.font=Font(bold=b); x.alignment=al
        if borde: x.border=BOX
        if fill: x.fill=fill
        if fmt: x.number_format=fmt
        return x

    def croquis(ws, nombre, r):
        """Pega la planta con el local sombreado y devuelve la fila siguiente."""
        archivo = os.path.join(CROQUIS_DIR, CROQUIS.get(nombre, "") + ".png")
        if not CROQUIS.get(nombre) or not os.path.exists(archivo):
            return r
        img = XLImage(archivo)
        alto = int(ANCHO_CROQUIS * img.height / img.width)
        img.width, img.height = ANCHO_CROQUIS, alto
        celda(r,2,"Ubicacion en planta de %s" % nombre,al=L,borde=False,b=True)
        img.anchor = "B%d" % (r + 1)
        ws.add_image(img)
        # alto en pixeles (96 ppp) -> puntos; reparto ese alto en filas propias
        puntos = alto * 72.0 / 96.0
        filas = int(puntos / ALTO_FILA_PT) + 1
        for i in range(filas):
            ws.row_dimensions[r + 1 + i].height = ALTO_FILA_PT
        return r + 1 + filas + 1

    def entrada(r):
        """las dos celdas donde se carga largo y alto de un muro"""
        for c in (8,9):
            x=ws.cell(row=r,column=c); x.fill=PEND; x.border=BOX; x.alignment=C
            x.number_format="0.00"

    r=1
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=6)
    celda(r,1,"FORMULARIO DE BALANCE TERMICO PARA CALEFACCION",b=True)
    celda(r,8,"largo",b=True,fill=G1); celda(r,9,"alto",b=True,fill=G1)
    r+=2

    FILAS_LOCAL={}; bloques=[]
    for nombre,a,b_,planta,aberturas,n_ext in LOCALES:
        ex=EXTRA.get(nombre)
        if nombre in MUROS:
            n_ext=min(3,sum(1 for m in MUROS[nombre] if m[1]=='ext')) or 1
        H=ALTURA_LOCAL.get(nombre, ALTURA)
        area=round(a*b_+(ex[0]*ex[1] if ex else 0),2); vol=round(area*H,2)
        ini_local=r
        ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=6)
        celda(r,1,"LOCAL  %s   (%s)   -   altura %.2f m"%(nombre,planta,H),b=True,fill=G2); r+=1
        for i,t in enumerate(["Nro","DESCRIPCION","DIMENSIONES (m)","AREA (m2)",
                              "FACTOR","PERDIDA CALOR (Kcal/h)"],start=1):
            celda(r,i,t,b=True,fill=G1)
        r+=1
        perdidas=[]

        def renglon(desc, factor, largo=None, alto=None, dim=None, area_fija=None, sangria=True):
            nonlocal r
            celda(r,1); celda(r,2,desc,al=L if not sangria else
                              Alignment(horizontal="left",vertical="center",indent=2,wrap_text=True))
            if largo is not None:
                ws.cell(row=r,column=8,value=largo); ws.cell(row=r,column=9,value=alto)
            entrada(r)
            celda(r,3,f'=IF(COUNT(H{r},I{r})<2,"",TEXT(H{r},"0.00")&" x "&TEXT(I{r},"0.00"))'
                      if dim is None else dim)
            if area_fija is not None:
                celda(r,4,area_fija,fmt="0.00")
            else:
                celda(r,4,f'=IF(COUNT(H{r},I{r})<2,"",ROUND(H{r}*I{r},2))',fmt="0.00")
            celda(r,5,factor,fmt="0")
            celda(r,6,f'=IF(D{r}="","",ROUND(D{r}*E{r},1))',fmt="0.0")
            perdidas.append(r); r+=1

        celda(r,1,"1",b=True); celda(r,2,"VENTANA",b=True,al=L)
        celda(r,3); celda(r,4); celda(r,5); celda(r,6); r+=1
        for nom,alt,anc in aberturas:
            renglon(nom, 60, largo=anc, alto=alt)
        if not aberturas:
            renglon("(sin aberturas)", 60)

        celda(r,1,"2",b=True); celda(r,2,"PAREDES EXTERIORES",b=True,al=L)
        celda(r,3); celda(r,4); celda(r,5); celda(r,6); r+=1
        datos = MUROS.get(nombre)
        if datos:
            ext=[m for m in datos if m[1]=="ext"]; inte=[m for m in datos if m[1]=="int"]
            for m in ext:
                renglon("AISLADAS (%s)"%m[2] if m[2] else "AISLADAS", 20, largo=m[0], alto=H)
            for _ in range(max(0, 2-len(ext))): renglon("AISLADAS", 20)
            for m in inte:
                renglon("INTERIORES (%s)"%", ".join(x for x in (m[2], m[3]) if x) if (m[2] or m[3]) else "INTERIORES", 25, largo=m[0], alto=H)
            for _ in range(max(0, 2-len(inte))): renglon("INTERIORES", 25)
        else:
            for _ in range(MUROS_EXT): renglon("AISLADAS", 20)
            lados = PAREDES.get(nombre) or ([a, b_, a, b_] + ([ex[0], ex[1]] if ex else []))
            for largo in lados:
                renglon("INTERIORES", 25, largo=largo, alto=H)

        celda(r,1,"3",b=True); celda(r,2,"TECHOS O CIELORRASOS",b=True,al=L)
        celda(r,3); celda(r,4); celda(r,5); celda(r,6); r+=1
        techo = "TECHO ENTREPISO" if planta=="PB" else "TECHO AISLADO"
        for desc,f in (("TECHO NO AISLADO",30),("TECHO AISLADO",20),("TECHO ENTREPISO",15)):
            if desc==techo: renglon(desc,f,dim="por croquis",area_fija=area)
            else:           renglon(desc,f,dim="",area_fija=None)

        celda(r,1,"4",b=True); celda(r,2,"PISO",b=True,al=L)
        celda(r,3); celda(r,4); celda(r,5); celda(r,6); r+=1
        piso = "SOBRE TIERRA" if planta=="PB" else "SOBRE LOCAL OCUPADO"
        for desc,f in (("SOBRE TIERRA",10),("SOBRE LOCAL OCUPADO",15)):
            if desc==piso: renglon(desc,f,dim="por croquis",area_fija=area)
            else:          renglon(desc,f,dim="",area_fija=None)

        celda(r,1,"5",b=True); celda(r,2,"INFILTRACION",b=True,al=L)
        celda(r,3); celda(r,4,"VOLUMEN (m3)",b=True); celda(r,5); celda(r,6); r+=1
        for desc,f,n in (("UNA PARED EXTERIOR",6,1),("DOS PAREDES EXTERIORES",9,2),
                         ("TRES O MAS PAREDES EXTERIORES",12,3)):
            if n==n_ext: renglon(desc,f,dim="%.2f m2 x %.2f"%(area,H),area_fija=vol)
            else:        renglon(desc,f,dim="",area_fija=None)

        fila_sub=r
        celda(r,1,"6",b=True); celda(r,2,"SUBTOTAL",b=True,al=L)
        celda(r,3); celda(r,4); celda(r,5)
        celda(r,6,"="+"+".join(f"IF(F{x}=\"\",0,F{x})" for x in perdidas),b=True,fmt="0.0")
        r+=1
        fila_tot=r
        celda(r,1,"7",b=True); celda(r,2,"PERDIDA TOTAL",b=True,al=L)
        ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=5)
        celda(r,3,f'=TEXT(F{fila_sub},"0.00")&"  X  "&Datos_balance!$B$4&" (FI)  X  "'
                  f'&Datos_balance!$B$5&" (FO)  X  "&Datos_balance!$B$6&" (FZ)"')
        celda(r,6,f"=ROUND(F{fila_sub}*Datos_balance!$B$4*Datos_balance!$B$5*Datos_balance!$B$6,1)",
              b=True,fmt="0.0")
        r+=1
        fila_suma=r; fila_cubrir=r+1
        celda(r,1); celda(r,2,"Carga de locales sin emisor",al=L)
        ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=5); celda(r,3)
        celda(r,6,None,fmt="0.0"); r+=1
        celda(r,1); celda(r,2,"CARGA TOTAL A CUBRIR",b=True,al=L)
        ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=5); celda(r,3)
        celda(r,6,f"=F{fila_tot}+IF(F{fila_suma}=\"\",0,F{fila_suma})",b=True,fmt="0.0")
        r+=2
        FILAS_LOCAL[nombre]=dict(total=fila_tot, suma=fila_suma, cubrir=fila_cubrir)
        if nombre in SIN_EMISOR:
            celda(r,1); celda(r,2,"SIN EMISOR",b=True,al=L)
            ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=5)
            celda(r,3,"la cubre el radiador de %s"%SIN_EMISOR[nombre]); celda(r,6)
            for k in range(1,7):
                ws.cell(row=r,column=k).border=Border(left=thin,right=thin,top=thin,bottom=med)
            r+=2
            r=croquis(ws,nombre,r)
            r+=2
            continue

        # emisor: radiador de elementos, o toallero en los banos
        if nombre in TOALLERO:
            bloque = [
              ("Salto termico:  dt = (te+ts)/2 - ti",
               '=TEXT((Datos_balance!$B$9+Datos_balance!$B$10)/2,"0")&" - "'
               '&TEXT(Datos_balance!$B$11,"0")&" = "'
               '&TEXT((Datos_balance!$B$9+Datos_balance!$B$10)/2-Datos_balance!$B$11,"0")&" C"',None),
              ("Kcal/h del toallero Scala/Domino 80",
               "=ROUND(Datos_balance!$B$18*Datos_balance!$B$15,0)","0"),
              ("Kcal/h del toallero Scala/Domino 150",
               "=ROUND(Datos_balance!$B$19*Datos_balance!$B$15,0)","0"),
              ("Toalleros necesarios",
               f"=IF(F{fila_cubrir}<=Datos_balance!$B$18*Datos_balance!$B$15,1,"
               f"ROUNDUP(F{fila_cubrir}/(Datos_balance!$B$19*Datos_balance!$B$15),0))","0"),
            ]
            adoptado = (f'=IF(F{fila_cubrir}<=Datos_balance!$B$18*Datos_balance!$B$15,'
                        '"Peisa Scala / Domino 80  (500 x 800 mm)",'
                        '"Peisa Scala / Domino 150  (500 x 1500 mm)")')
            etiqueta = "Toallero adoptado"
        else:
            bloque = [
              ("Salto termico:  dt = (te+ts)/2 - ti",
               '=TEXT((Datos_balance!$B$9+Datos_balance!$B$10)/2,"0")&" - "'
               '&TEXT(Datos_balance!$B$11,"0")&" = "'
               '&TEXT((Datos_balance!$B$9+Datos_balance!$B$10)/2-Datos_balance!$B$11,"0")&" C"',None),
              ("Kcal/h por elemento",
               "=ROUND(Datos_balance!$B$14*Datos_balance!$B$15,2)","0.00"),
              ("Elementos necesarios",
               f"=ROUNDUP(F{fila_cubrir}/(Datos_balance!$B$14*Datos_balance!$B$15),0)","0"),
              ("Ancho del radiador (cm)",
               f"=ROUNDUP(F{fila_cubrir}/(Datos_balance!$B$14*Datos_balance!$B$15),0)"
               "*Datos_balance!$B$16","0"),
            ]
            adoptado = "=Datos_balance!$B$13"
            etiqueta = "Radiador adoptado"
        for desc,form,fmt in bloque:
            celda(r,2,desc,al=L)
            ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=5)
            celda(r,3,form,fmt=fmt)
            celda(r,1); celda(r,6)
            r+=1
        celda(r,2,etiqueta,al=L)
        ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=5)
        celda(r,3,adoptado); celda(r,1); celda(r,6)
        r+=1
        for k in range(1,7):
            ws.cell(row=r-1,column=k).border=Border(left=thin,right=thin,top=thin,bottom=med)
        r+=1
        r=croquis(ws,nombre,r)
        r+=2

    for origen,destino in SIN_EMISOR.items():
        if origen in FILAS_LOCAL and destino in FILAS_LOCAL:
            d=FILAS_LOCAL[destino]
            partes=[f"F{FILAS_LOCAL[o]['total']}" for o,x in SIN_EMISOR.items()
                    if x==destino and o in FILAS_LOCAL]
            c=ws.cell(row=d["suma"],column=6); c.value="="+"+".join(partes)
            ws.cell(row=d["suma"],column=3).value=", ".join(
                o for o,x in SIN_EMISOR.items() if x==destino)
    ws.print_area=f"A1:F{r}"
    ws.page_setup.orientation="portrait"; ws.page_setup.fitToWidth=1
    ws.sheet_properties.pageSetUpPr.fitToPage=True

    # ---------- datos ----------
    dz=wb.create_sheet("Datos_balance"); dz.sheet_view.showGridLines=False
    for col,w in zip("ABCD",(42,14,12,52)): dz.column_dimensions[col].width=w
    def P(r,c,v,b=False,sz=10,fill=None,bd=False,al=None):
        x=dz.cell(row=r,column=c,value=v); x.font=Font(bold=b,size=sz)
        if fill:x.fill=fill
        if bd:x.border=BOX
        if al:x.alignment=Alignment(horizontal=al,vertical="center",wrap_text=True)
    P(1,1,"DATOS DE PARTIDA - BALANCE TERMICO",b=True,sz=13)
    P(3,1,"PARAMETRO",b=True,fill=G1,bd=True); P(3,2,"valor",b=True,fill=G1,bd=True,al="center")
    P(3,3,"unidad",b=True,fill=G1,bd=True,al="center"); P(3,4,"origen",b=True,fill=G1,bd=True)
    filas=[(4,"FI - factor de interrupcion",1.07,"-","Del formulario modelo."),
           (5,"FO - factor de orientacion",1.00,"-","FALTA la tabla de la catedra. Se adopta 1,00."),
           (6,"FZ - factor de zona",1.00,"-","FALTA la tabla de la catedra. Se adopta 1,00."),
           (9,"te - temperatura de ida del agua",90,"C","Del formulario modelo."),
           (10,"ts - temperatura de retorno",82,"C","Del formulario modelo."),
           (11,"ti - temperatura interior de diseno",20,"C","Del formulario modelo."),
           (14,"Kcal/h por elemento del radiador",245,"Kcal/h","Peisa Tropical 80-500, valor de catalogo a salto termico 60 C."),
           (15,"Factor de correccion por salto termico",1.12,"-","Pasa del salto de catalogo (60 C) al de la instalacion (66 C). (66/60)^1,3 = 1,13."),
           (16,"Ancho de cada elemento",8,"cm","Peisa Tropical: 80 mm por elemento.")]
    for r_,n,v,u,o in filas:
        P(r_,1,n,bd=True); P(r_,2,v,bd=True,al="center",fill=PEND)
        P(r_,3,u,bd=True,al="center",sz=9); P(r_,4,o,bd=True,sz=8)
    P(13,1,"RADIADOR",b=True); P(13,2,"Peisa Tropical 80-500",bd=True,al="center",fill=PEND)
    P(8,1,"TEMPERATURAS",b=True)
    P(17,1,"TOALLEROS (banos)",b=True)
    for r_,n,v,u,o in [(18,"Toallero Scala / Domino 80",632,"Kcal/h","500 x 800 mm. Valor de catalogo a 60 C."),
                       (19,"Toallero Scala / Domino 150",1174,"Kcal/h","500 x 1500 mm. Valor de catalogo a 60 C.")]:
        P(r_,1,n,bd=True); P(r_,2,v,bd=True,al="center",fill=PEND)
        P(r_,3,u,bd=True,al="center",sz=9); P(r_,4,o,bd=True,sz=8)
    P(21,1,"FACTORES DE PERDIDA (Kcal/h por m2, o por m3 en infiltracion)",b=True)
    P(22,1,"elemento",b=True,fill=G1,bd=True); P(22,2,"factor",b=True,fill=G1,bd=True,al="center")
    for i,(n,v) in enumerate([("Ventana",60),("Pared exterior aislada",20),
        ("Pared interior",25),("Techo no aislado",30),("Techo aislado",20),
        ("Techo entrepiso",15),("Piso sobre tierra",10),("Piso sobre local ocupado",15),
        ("Infiltracion, una pared exterior",6),("Infiltracion, dos paredes exteriores",9),
        ("Infiltracion, tres o mas paredes exteriores",12)],start=23):
        P(i,1,n,bd=True); P(i,2,v,bd=True,al="center")
    P(35,1,"Los factores estan escritos en cada renglon del formulario, no se leen de aca: "
            "esta tabla es solo de referencia.",sz=9,b=True)
    P(37,1,"QUE FALTA CARGAR",b=True,sz=12)
    for i,t in enumerate([
      "1. Las longitudes de pared de cada local, en las columnas H (largo) e I (alto) del formulario.",
      "   Las celdas estan en naranja. Al cargarlas se completan solas la dimension, el area y la perdida.",
      "2. Si el muro es aislado o no: el formulario trae tres renglones de cada tipo, borrar los que sobren.",
      "3. Las tablas de FO y FZ de la catedra. Por ahora los dos valen 1,00.",
      "4. Nada: el radiador ya esta cargado (Peisa Tropical 80-500, aluminio inyectado en blanco,",
      "   245 kcal/h por elemento, 80 mm de ancho, 575 mm de alto, 0,375 l por elemento).",
      "   En los tres banos va toallero Peisa Scala o Domino en vez de radiador de elementos.",
      "",
      "LO QUE YA VIENE CARGADO",
      "- Superficie y volumen de cada local, de la planilla de iluminacion y ventilacion.",
      "- Las aberturas de cada local con su medida real, del campo UBICACION de la planilla de",
      "  carpinterias. Son 17 aberturas repartidas en 13 locales.",
      "- Techo y piso segun la planta: en PB entrepiso arriba y piso sobre tierra; en PA techo",
      "  aislado arriba y piso sobre local ocupado. Si algun local no es asi, mover el area de renglon.",
      "- Infiltracion segun la cantidad de paredes exteriores que se estimo para cada local.",
      "",
      "Altura de local 3,00 m en todos. Varios tienen cielorraso suspendido de yeso a 2,80, "
      "pero el muro llega a la losa y el espacio sobre el cielorraso esta dentro de la "
      "envolvente, asi que la pared pierde calor en los 3,00."],
      start=38):
        P(i,1,t,sz=9,b=(t.isupper() and len(t)<30))
