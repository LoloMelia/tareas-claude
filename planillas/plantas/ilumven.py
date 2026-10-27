# -*- coding: utf-8 -*-
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

# (local, a, b, area proyectada ilum, proyectada vent, exigible)
PB=[("01 - Cocina / comedor",7.63,3.56,16.95,8.48,True),
    ("02 - Deposito",3.8,3.1,None,None,False),
    ("03 - Lavadero",3.5,1.7,10.5,1.6,True),
    ("06 - Living / comedor",8.66,4.06,34.05,15.0,True),
    ("07 - Hall / ingreso",4.0,2.15,10.5,1.6,True),
    ("09 - Dormitorio suite",3.5,3.5,6.0,3.0,True),
    ("10 - Bano suite",3.38,1.72,"COND","COND",True),
    ("11 - Bano visita",2.4,1.3,"COND","COND",True),
    ("12 - Bano exterior",1.9,0.95,"COND","COND",True)]
PA=[("13 - Dormitorio 1",4.25,4.0,8.75,4.38,True),
    ("14 - Estar / Playroom",4.13,4.08,5.0,5.0,True),
    ("15 - Dormitorio 2",3.5,4.05,3.75,1.88,True),
    ("17 - Bano",2.2,1.6,1.875,0.94,True)]

def agregar(wb, nombre="Iluminacion y ventilacion"):
    thin=Side(style="thin",color="000000"); med=Side(style="medium",color="000000")
    BOX=Border(left=thin,right=thin,top=thin,bottom=thin)
    G1=PatternFill("solid",fgColor="D9D9D9"); G2=PatternFill("solid",fgColor="EDEDED")
    NIV=PatternFill("solid",fgColor="DDEBF7"); INP=PatternFill("solid",fgColor="E2EFDA")
    CALC=PatternFill("solid",fgColor="FFF2CC"); WARN=PatternFill("solid",fgColor="FCE4D6")
    C=Alignment(horizontal="center",vertical="center",wrap_text=True)
    ws=wb.create_sheet(nombre); ws.sheet_view.showGridLines=False
    cols=[("","Local",26),("","(a)\nMedidas",9),("","(b)\nMedidas",9),("","(Area)\nMedidas",10),
     ("Iluminacion","Coef.",8),("Iluminacion","Area requerida",12),("Iluminacion","Area proyectada",12),
     ("Ventilacion","Coef.",8),("Ventilacion","Area requerida",12),("Ventilacion","Area proyectada",12),
     ("","VERIFICACION",14),("","OBSERVACIONES",40)]
    N=len(cols)
    ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=N)
    t=ws.cell(row=1,column=1,value="PLANILLA DE ILUMINACION Y VENTILACION")
    t.font=Font(bold=True,size=12); t.alignment=C
    ws.row_dimensions[1].height=22; ws.row_dimensions[2].height=16; ws.row_dimensions[3].height=28
    c=1
    while c<=N:
        g=cols[c-1][0]
        if g=="":
            ws.merge_cells(start_row=2,start_column=c,end_row=3,end_column=c)
            x=ws.cell(row=2,column=c,value=cols[c-1][1]); x.font=Font(bold=True,size=9)
            x.alignment=C; x.fill=G1; x.border=BOX; ws.cell(row=3,column=c).border=BOX; c+=1
        else:
            e=c
            while e<N and cols[e][0]==g: e+=1
            ws.merge_cells(start_row=2,start_column=c,end_row=2,end_column=e)
            gc=ws.cell(row=2,column=c,value=g); gc.font=Font(bold=True,size=9)
            gc.alignment=C; gc.fill=G1; gc.border=BOX
            for k in range(c,e+1):
                sc=ws.cell(row=3,column=k,value=cols[k-1][1]); sc.font=Font(bold=True,size=8)
                sc.alignment=C; sc.fill=G2; sc.border=BOX; ws.cell(row=2,column=k).border=BOX
            c=e+1
    for i,(_,_,w) in enumerate(cols,start=1): ws.column_dimensions[get_column_letter(i)].width=w
    r=4
    for eti,lst in (("PB",PB),("PA",PA)):
        ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=N)
        nc=ws.cell(row=r,column=1,value=eti); nc.font=Font(bold=True,size=10); nc.fill=NIV
        nc.alignment=Alignment(horizontal="left",vertical="center")
        for k in range(1,N+1): ws.cell(row=r,column=k).border=BOX
        r+=1
        for local,a,b,pi,pv,exig in lst:
            ws.row_dimensions[r].height=17
            v=lambda col,val: ws.cell(row=r,column=col,value=val)
            v(1,local); v(2,a); v(3,b)
            v(4,f"=B{r}*C{r}")
            if exig:
                v(5,9); v(6,f"=D{r}/E{r}")
                v(8,"i/3"); v(9,f"=F{r}/3")
                v(7,pi); v(10,pv)
                v(11,f'=IF(OR(G{r}="COND",J{r}="COND"),"COND",'
                      f'IF(AND(G{r}>=F{r},J{r}>=I{r}),"CUMPLE","NO CUMPLE"))')
            else:
                for k in (5,6,7,8,9,10): v(k,"-")
                v(11,"NO EXIGIBLE")
            obs=[]
            if local.startswith("07"): obs.append("CORREGIDO: la planilla original repetia los valores del local 03 (0,66 y 0,22). Con 4,00 x 2,15 = 8,60 m2 corresponden 0,96 y 0,32. Cumple igual.")
            if local.startswith("02"): obs.append("Local no habitable: el codigo no le exige iluminacion ni ventilacion natural. Si se lo considera habitable, hay que preverle conducto.")
            if local.startswith("14"): obs.append("La superficie abrible declarada iguala a la vidriada: supondria una carpinteria 100% abrible. En el resto de los locales la relacion es del 50%. Verificar.")
            if local.startswith("10") or local.startswith("11") or local.startswith("12"):
                obs.append("Sin ventana al exterior: se ventila por conducto o extraccion mecanica.")
            if obs: v(12," ".join(obs))
            for k in range(1,N+1):
                cc=ws.cell(row=r,column=k); cc.border=BOX; cc.alignment=C; cc.font=Font(size=9)
                if k in (2,3,5,7,10): cc.fill=INP
                elif k in (4,6,9,11): cc.fill=CALC
                if k in (2,3,4,6,7,9,10): cc.number_format="0.00"
            ws.cell(row=r,column=1).alignment=Alignment(horizontal="left",vertical="center")
            if obs:
                o=ws.cell(row=r,column=12); o.fill=WARN; o.font=Font(size=8)
                o.alignment=Alignment(horizontal="left",vertical="center",wrap_text=True)
            r+=1
        for k in range(1,N+1):
            ws.cell(row=r-1,column=k).border=Border(left=thin,right=thin,top=thin,bottom=med)
    last=r-1
    for bueno,color,letra in (("CUMPLE","C6EFCE","006100"),):
        ws.conditional_formatting.add(f"K4:K{last}",CellIsRule(operator="equal",formula=[f'"{bueno}"'],
            fill=PatternFill("solid",fgColor=color),font=Font(color=letra,bold=True,size=9)))
    ws.conditional_formatting.add(f"K4:K{last}",CellIsRule(operator="equal",formula=['"NO CUMPLE"'],
        fill=PatternFill("solid",fgColor="FFC7CE"),font=Font(color="9C0006",bold=True,size=9)))
    ws.freeze_panes="B4"; ws.print_title_rows="1:3"
    ws.page_setup.orientation="landscape"; ws.page_setup.fitToWidth=1
    ws.sheet_properties.pageSetUpPr.fitToPage=True
    # memoria
    ms=wb.create_sheet("Memoria ilum. y vent.")
    ms.sheet_view.showGridLines=False
    ms.column_dimensions["A"].width=22; ms.column_dimensions["B"].width=96
    M=[("MEMORIA - ILUMINACION Y VENTILACION",""),("",""),
    ("CRITERIO","Area de iluminacion requerida = superficie del local / 9"),
    ("","Area de ventilacion requerida = un tercio de la de iluminacion = superficie / 27"),
    ("","Area proyectada: la vidriada de la carpinteria para iluminacion, y la parte que"),
    ("","realmente abre para ventilacion."),
    ("",""),
    ("RESULTADO","Los trece locales cumplen holgadamente iluminacion y ventilacion."),
    ("",""),
    ("CORRECCION","Local 07, Hall / ingreso: la planilla original traia 0,66 y 0,22, que son los"),
    ("","valores del local 03 (Lavadero, 6,0 m2). Con sus 4,00 x 2,15 = 8,60 m2 corresponden"),
    ("","0,96 y 0,32. No cambia el resultado, pero el numero no cerraba con la superficie"),
    ("","declarada y un verificador lo puede observar."),
    ("",""),
    ("A REVISAR","Local 14, Estar / Playroom: declara 5,00 m2 de ventilacion sobre 5,00 m2 de"),
    ("","iluminacion, es decir una carpinteria enteramente abrible. En los demas locales"),
    ("","la relacion es del 50 por ciento. Conviene verificar la carpinteria real."),
    ("",""),
    ("","Local 02, Deposito: figura sin exigencia por no ser habitable. Son 11,8 m2"),
    ("","cerrados: si se lo considera habitable hay que preverle conducto."),
    ("",""),
    ("REDONDEOS","Diferencias menores que no afectan: local 03 da 5,95 m2 y figura 6,0;"),
    ("","local 09 da 12,25 y figura 12,3."),
    ]
    for i,(a,b) in enumerate(M,start=1):
        ca=ms.cell(row=i,column=1,value=a); cb=ms.cell(row=i,column=2,value=b)
        ca.alignment=Alignment(vertical="top",wrap_text=True)
        cb.alignment=Alignment(vertical="top",wrap_text=True)
        hd=(i==1) or a in ("CRITERIO","RESULTADO","CORRECCION","A REVISAR","REDONDEOS")
        ca.font=Font(bold=True,size=11 if i==1 else 9); cb.font=Font(bold=hd,size=9)
    return nombre
