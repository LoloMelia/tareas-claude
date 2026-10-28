# Guía para la defensa del TP

Casa I+B · Lote 230 · Barrio Vida, Funes · Santa Fe

Este archivo tiene tres partes: cómo se calcula la planilla de iluminación y
ventilación, cómo se hace el balance térmico, y los puntos del trabajo que
conviene tener preparados para explicar.

---

# 0. De dónde salió cada método

**Este trabajo se hizo sin tener a la vista el apunte de la cátedra.** Los
métodos se dedujeron de las **planillas de ejemplo**: mirando las filas ya
resueltas y probando qué fórmula reproduce esos números. Donde el ejemplo traía
una fila calculada, la fórmula está verificada contra ella; donde no, se adoptó
el criterio corriente.

| Procedencia | Qué se tomó de ahí |
|---|---|
| **Planillas de ejemplo de la cátedra** (verificado contra filas resueltas) | Los coeficientes 1/9 y 1/3 de iluminación y ventilación. Todos los factores del balance térmico (60, 25, 20, 30, 15, 10, 6, 9, 12) y el FI = 1,07. El cálculo del radiador, incluido el factor 1,12. El método de losas por tensiones admisibles (σ = 2400 kg/cm², z = 0,9 h, repartición As/5). La fórmula de corte τ = V / (b · 0,85 h), deducida probándola contra una fila resuelta. |
| **CIRSOC 201 y práctica corriente** (no de la cátedra) | El dimensionado de vigas y columnas por rotura y los coeficientes φ. La fórmula simplificada de muro portante usada en tabiques. |
| **Ordenanza 8757/11**, consultada en internet | Los valores de factor de exposición solar y los cuadrantes. Las transmitancias máximas. |
| **Documentación de obra** | Toda la geometría: planos de planta, despieces de locales, planilla de carpinterías, plano de fachadas, detalles constructivos y cómputo métrico. |

## Lo que conviene chequear contra el apunte, en orden de importancia

1. **Los factores del balance térmico.** Si la cátedra da una tabla distinta,
   cambian todos los números del balance.
2. **Si hay tabla de FO y FZ.** Acá valen 1,00 porque es lo que usa la planilla
   de ejemplo. Si el apunte trae tabla de corrección, hay que aplicarla.
3. **Los coeficientes 1/9 y 1/3.** Algunos reglamentos usan 1/8 o 1/10 según la
   clase de local.
4. **El método de tabiques.** Es el que más se adoptó por criterio propio: la
   planilla de la cátedra solo traía las cargas, no la fórmula de capacidad.

---

# 1. Planilla de iluminación y ventilación

## El criterio

El Reglamento de Edificación de Rosario no pide calcular nada complicado: pide
que la ventana sea **una fracción de la superficie del piso** del local. Todo
sale de tres números.

## Los tres pasos

**1. Superficie del local**

```
Área = a × b
```

**2. Iluminación — superficie vidriada mínima**

```
Área requerida = Área del local / 9
```

El 9 es el coeficiente para locales de primera clase: dormitorios, estar,
comedor, cocina. O sea que la ventana tiene que ser como mínimo **1/9 de la
superficie del piso**.

**3. Ventilación — superficie abrible mínima**

```
Área requerida = (área de iluminación requerida) / 3
```

Acá está la clave, y es lo que más se confunde: **la ventilación no se calcula
sobre el local, se calcula sobre la iluminación ya calculada**. Es 1/3 de la
ventana, o sea 1/27 de la superficie del piso.

La diferencia entre las dos columnas de "proyectada" es la misma idea:
*vidriada* es todo el paño; *abrible* es solo la parte que se puede abrir. En
una corrediza de dos hojas abrís la mitad — por eso en casi todos los locales
el área de ventilación proyectada es la mitad de la de iluminación.

## Ejemplo con la cocina de esta casa

| | |
|---|---|
| Local | 7,63 × 3,56 = **27,16 m²** |
| Iluminación requerida | 27,16 / 9 = **3,02 m²** |
| Iluminación proyectada | **16,95 m²** → cumple |
| Ventilación requerida | 3,02 / 3 = **1,01 m²** |
| Ventilación proyectada | **8,48 m²** → cumple |

## Los dos casos especiales de esta casa

**Baños sin ventana al exterior (10, 11 y 12).** Están marcados **COND** en vez
de un número. El código no les exige ventilación natural: se resuelven por
**conducto de ventilación o extracción mecánica**. No se les pone área
requerida, se declara el conducto.

**Depósito (02).** Marcado **NO EXIGIBLE**: es local no habitable, el código no
le pide ni iluminación ni ventilación natural.

## Dos observaciones que quedaron anotadas en la planilla

- **Local 07, Hall:** la planilla original repetía los valores del local 03
  (0,66 y 0,22). Con los 8,60 m² reales (4,00 × 2,15) corresponden 0,96 y 0,32. Cumple igual.
- **Local 14, Estar / Playroom:** declara 5,00 m² de ventilación sobre 5,00 m²
  de superficie vidriada, o sea una carpintería 100 % abrible. En el resto de
  los locales la relación es del 50 %. Conviene verificarlo.

> **Aviso honesto:** los coeficientes 1/9 y 1/3 son los de la planilla de la
> cátedra y los de uso corriente en Rosario, pero no están verificados contra el
> texto del Reglamento vigente. Si lo presentás en el municipio, chequealos.

---

# 2. Balance térmico para calefacción

## El criterio

Es el método simplificado por **factores**: cada elemento de la envolvente
(ventana, pared, techo, piso) pierde una cantidad fija de calor por metro
cuadrado, y la infiltración de aire por metro cúbico. No se calculan
transmitancias: los factores ya las tienen adentro.

El objetivo es llegar a los **kcal/h que pierde cada local**, para después
elegir el radiador que los repone.

## Los factores

| Elemento | Factor | Unidad |
|---|---|---|
| Ventana | **60** | kcal/h por m² |
| Pared exterior aislada | **20** | kcal/h por m² |
| Pared interior | **25** | kcal/h por m² |
| Techo no aislado | **30** | kcal/h por m² |
| Techo aislado | **20** | kcal/h por m² |
| Techo entrepiso | **15** | kcal/h por m² |
| Piso sobre tierra | **10** | kcal/h por m² |
| Piso sobre local ocupado | **15** | kcal/h por m² |
| Infiltración, 1 pared exterior | **6** | kcal/h por m³ |
| Infiltración, 2 paredes exteriores | **9** | kcal/h por m³ |
| Infiltración, 3 o más | **12** | kcal/h por m³ |

Dos cosas del método que conviene tener claras:

- **Las paredes se computan enteras**, sin descontarles la ventana, y la ventana
  se suma aparte. No es un error: el método está calibrado así.
- **La infiltración se calcula sobre el volumen del local**, y el factor depende
  de cuántas paredes exteriores tiene. Más paredes al exterior, más rendijas.

## El procedimiento, local por local

1. Listar cada **ventana** con su área, a factor 60.
2. Listar cada **pared**, separando las exteriores (20) de las interiores (25).
3. El **techo**: entrepiso si arriba hay otro local, aislado o no aislado si da
   al exterior.
4. El **piso**: sobre tierra en planta baja, sobre local ocupado en planta alta.
5. La **infiltración**: volumen del local por el factor que corresponda.
6. **Subtotal** = suma de todo lo anterior.
7. **Pérdida total** = Subtotal × FI × FO × FZ

## Los tres factores de corrección

| | Qué es | Valor usado |
|---|---|---|
| **FI** | Factor de interrupción. Compensa el enfriamiento del edificio cuando la calefacción no funciona de corrido (se apaga de noche): hay que recalentar la masa. | **1,07** |
| **FO** | Factor de orientación. Castiga los locales que dan a la orientación más desfavorable, con menos sol y más viento. | **1,00** |
| **FZ** | Factor de zona. Corrige según la zona bioambiental. Rosario es zona IIIb, templada cálida, de las benignas del país. | **1,00** |

FO y FZ valen 1 porque es lo que usa la planilla modelo de la cátedra. No se
aplica tabla de corrección.

## Ejemplo completo: la cocina

| Nro | Descripción | Dimensiones | Área | Factor | kcal/h |
|---|---|---|---|---|---|
| **1** | **VENTANA** | | | | |
| | VA01 | 0,75 × 3,00 | 2,25 | 60 | 135,0 |
| | PF03 | 2,88 × 3,00 | 8,64 | 60 | 518,4 |
| | PF04 | 2,70 × 0,60 | 1,62 | 60 | 97,2 |
| | PV02 | 2,48 × 3,00 | 7,44 | 60 | 446,4 |
| **2** | **PAREDES** | | | | |
| | Aislada (NO) | 7,63 × 3,00 | 22,89 | 20 | 457,8 |
| | Aislada (SO) | 3,56 × 3,00 | 10,68 | 20 | 213,6 |
| | Interior (galería y living) | 7,63 × 3,00 | 22,89 | 25 | 572,3 |
| | Interior (depósito y lavadero) | 3,56 × 3,00 | 10,68 | 25 | 267,0 |
| **3** | **TECHO** entrepiso | por croquis | 27,16 | 15 | 407,4 |
| **4** | **PISO** sobre tierra | por croquis | 27,16 | 10 | 271,6 |
| **5** | **INFILTRACIÓN** 2 paredes ext. | 27,16 × 3,00 | 81,48 | 9 | 733,3 |
| **6** | **SUBTOTAL** | | | | **4.120,0** |
| **7** | **PÉRDIDA TOTAL** | 4.120 × 1,07 × 1 × 1 | | | **4.408,4** |

## Del calor al radiador

Una vez que tenés los kcal/h, el radiador sale en cuatro cuentas.

**1. Salto térmico de la instalación**

```
Δt = (te + ts) / 2 − ti
Δt = (90 + 82) / 2 − 20 = 86 − 20 = 66 °C
```

donde `te` es la temperatura de ida del agua, `ts` la de retorno y `ti` la
temperatura interior de diseño.

**2. Rendimiento real de cada elemento**

El catálogo da el rendimiento a un salto de 60 °C. Como tu instalación trabaja a
66 °C, cada elemento rinde más, y el factor de corrección lo contempla:

```
245 kcal/h × 1,12 = 274,4 kcal/h por elemento
```

El 1,12 se puede comprobar: (66/60)^1,3 = 1,13.

**3. Cantidad de elementos**

```
Elementos = Pérdida total / kcal por elemento   (redondeando para arriba)
Cocina: 4.408,4 / 274,4 = 16,1 → 17 elementos
```

**4. Largo del radiador**

```
17 elementos × 8 cm = 136 cm
```

## Los emisores de esta casa

- **Radiadores: Peisa Tropical 80-500**, aluminio inyectado blanco. 245 kcal/h
  por elemento, 80 mm de ancho, 575 mm de alto, 0,375 l por elemento.
- **Toalleros (los tres baños): Peisa Scala / Domino**, 500 × 1500 mm,
  1.174 kcal/h.

## Resultado

| Local | Pérdida | A cubrir | Emisor |
|---|---|---|---|
| 01 Cocina / comedor | 4.408 | 4.408 | 17 elementos (2 radiadores) |
| 06 Living / comedor | 5.726 | 8.065 | 30 elementos (2 radiadores) |
| 07 Hall | 2.340 | *→ living* | — |
| 08 Vestidor | 1.266 | 1.266 | 5 elementos |
| Escalera | 1.348 | *→ play room* | — |
| 09 Dormitorio suite | 2.238 | 2.238 | 9 elementos |
| 10 Baño suite | 1.135 | 1.135 | toallero |
| 11 Baño visitas | 717 | 717 | toallero |
| 13 Dormitorio Norte | 2.965 | 2.965 | 11 elementos |
| 14 Play room | 2.203 | 3.552 | 13 elementos |
| 15 Dormitorio Sur | 2.428 | 2.428 | 9 elementos |
| 17 Baño | 904 | 904 | toallero |
| **TOTAL** | **27.677 kcal/h** | | **94 elementos + 3 toalleros** |

**27.677 kcal/h ≈ 32 kW** es el valor con el que se selecciona la caldera, que
va en el depósito.

## El detalle del hall y la escalera

El hall y la escalera **no tienen radiador** pero sí pierden calor: el hall
tiene 10,65 m² de vidrio y la puerta de ingreso H01 y la escalera el paño fijo PF05. Como están abiertos a
otros locales, el aire es el mismo, y sus pérdidas las tiene que reponer el
radiador del local vecino.

Por eso cada bloque de la planilla tiene dos renglones extra: **"Carga de
locales sin emisor"** y **"CARGA TOTAL A CUBRIR"**. El living absorbe el hall y
el play room absorbe la escalera, y el radiador se dimensiona con el total.

---

# 3. Puntos a explicar en la defensa

Son resultados que no cierran o criterios que se adoptaron. Ninguno es un error
a corregir: lo que se espera es que los sepas explicar.

## 3.1 VCH 03a — sección insuficiente

**Qué pasa:** viga chata de **40 × 13 cm** para una luz de **3,71 m**, con una
carga de 2.988 kg/m. La planilla devuelve **SECCIÓN INSUF.**: excede la cuantía
máxima de armadura y no llega a la altura mínima por flecha. Además la
separación de estribos da menos de 10 cm, que es difícil de construir.

**Cómo explicarlo:** es una viga chata, y su canto está limitado por el espesor
de la losa. No se puede engrosar sin bajar del cielorraso. El cálculo dice que
con 13 cm de altura total no alcanza — es el precio de mantener el cielorraso
parejo.

**Qué proponer si te preguntan:** revisar el ancho tributario real (puede estar
sobreestimado), o aceptar que la viga baje unos centímetros en ese tramo.

## 3.2 Columna C9 de planta baja — sobrecargada

**Qué pasa:** **55,94 t** de carga sobre una sección de **15 × 30 cm**, que da
450 cm². Queda por encima de su capacidad.

**Un dato que lo refuerza:** el detalle estructural de la escalera nombra
"Col 9 15x30", así que **la sección es la correcta** — no es un error de
dimensión en mi planilla.

**Cómo explicarlo:** es la columna más cargada del conjunto. 15 × 30 es una
sección esbelta para 56 t. Una columna de 20 × 30 resolvería el problema.

## 3.3 Tabique T07 — al 106 %

**Qué pasa:** **30,62 t** sobre **98 cm** de tabique de 12 cm de espesor. Da
**NO VERIFICA**, pero por poco: está al 106 % de su capacidad.

**De dónde viene la carga:** recibe VI 02 (21,12 t), VI 10b (6,60 t),
VI 10a (1,59 t) y VI 17 (1,31 t).

**Cómo explicarlo, que es lo importante:** la capacidad sale de la **fórmula
simplificada de muro portante**, cuya reducción por esbeltez se come dos tercios
de la resistencia. Con 12 cm de espesor y 3,15 m de altura el coeficiente vale
**0,327**. Esa fórmula supone el muro **sin arriostrar**, y en la realidad el
tabique está vinculado a losas y muros perpendiculares. **Un análisis más fino
del arriostramiento real daría más capacidad y el tabique verificaría.**

Y un dato concreto: **con 104 cm de largo en vez de 98, verifica.**

## 3.4 Capacidad de los pilotes — el punto más débil del trabajo

**Hay que decirlo de entrada, no esperar a que te lo pregunten.**

No hay estudio de suelos. La capacidad de 22 t por pilote **no está verificada**:
la deduje al revés, del propio diseño. El proyectista puso **un solo pilote bajo
una columna de 21 t**, así que la capacidad que él adoptó es por lo menos esa.

**Por qué es discutible:** 21 t en un pilote de Ø30 requiere una adherencia de
4,5 a 4,8 t/m², contra los **2 a 3 t/m² típicos del loess de la zona de
Rosario**. O sea que el valor adoptado está en el extremo optimista.

**Cómo plantearlo:** es una lectura inversa del diseño, no una verificación.
Sin estudio de suelos no se puede verificar, y eso es una limitación del trabajo,
no un resultado.

## 3.5 Factor de exposición solar — la casa no cumpliría

**Qué pasa:** los seis paños fijos no tienen protección solar, así que su factor
de exposición solar es **0,88**. El máximo que admite la Ordenanza 8757/11 para
el cuadrante Este/Oeste es **0,30**.

**Por qué caen todos en ese cuadrante:** la casa está **girada 45° respecto del
norte**. Sus cuatro fachadas son Noreste, Sudeste, Sudoeste y Noroeste, o sea
que **ninguna cae en el cuadrante Norte ni en el Sur** — las cuatro entran en el
Este/Oeste, que es el más exigente.

**Por qué la planilla igual da CUMPLE:** porque la planilla de la cátedra
verifica la transmitancia (2,80 ≤ 2,90), no el factor de exposición solar. Para
el TP está bien; para el municipio, no pasaría.

**Dato relacionado, bueno para la memoria:** la fachada **Noroeste concentra
59,91 m²**, más de la mitad del vidrio de la casa, con sol de tarde y sin
protección exterior. Es el punto más flojo de la envolvente.

**Las tres salidas posibles, si te preguntan:**

1. **Cambiar el vidrio** por uno de control solar. Baja el Fes sin tocar la obra.
2. Ver local por local si la abertura ocupa **menos del 20 % del lado expuesto**:
   en ese caso la ordenanza no exige verificar el Fes.
3. Agregar **protección exterior**. Ojo: el alero y el parasol horizontal solo
   computan al Norte; al Este y al Oeste la protección tiene que ser **vertical**.

Y una aclaración que conviene hacer: **las cortinas de la casa son blackout
interiores y no computan** como protección solar. La radiación ya atravesó el
vidrio cuando llega a la cortina.

## 3.6 Criterios adoptados que conviene poder defender

**Todas las vigas son invertidas.** Se deduce de las cotas N.F.L / N.S.V y se
confirma con el cielorraso de hormigón visto. La consecuencia de cálculo: la
losa trabaja como ala comprimida **en el apoyo** para una viga invertida, y
**en el tramo** para una colgante. Es al revés de lo habitual.

**Tabiques: dos criterios de carga mezclados.** T1 a T6 usan las cargas de la
planilla de la cátedra, que probablemente sean de servicio. T7 a T13 usan las
reacciones de mi bajada, que son **mayoradas**. Comparar cargas de servicio
contra φPn (resistencia última) queda del lado inseguro en torno a un 40 %. Con
utilizaciones del 10 al 20 % no cambia ningún veredicto, pero hay que saberlo.

**Losas: método de tensiones admisibles**, el mismo criterio de la planilla
modelo (σ = 2400 kg/cm², z = 0,9 h). Las vigas y columnas, en cambio, van por
**rotura (CIRSOC 201)**. Son dos criterios distintos en el mismo trabajo porque
así lo pide cada planilla de la cátedra.

**Muros exteriores: sí están aislados.** El paquete lleva **25 mm de
poliestireno expandido de alta densidad** entre el cierre de ladrillo Brimax y
la terminación de frente. Por eso van a factor 20 y no a uno más alto.

**Techo: también aislado.** La capa es el **hormigón de pendiente alivianado con
perlitas de poliestireno expandido**, que cumple doble función, pendiente y
aislación. Y la **barrera de vapor está del lado caliente**, debajo del
aislante, que es donde corresponde.

**Altura de muro 3,00 m.** Varios locales tienen cielorraso suspendido de yeso a
2,80, pero el muro llega a la losa y el espacio sobre el cielorraso está dentro
de la envolvente: la pared pierde calor en toda su altura. Las carpinterías de
3,00 entran porque el cielorraso sube a la losa antes de la abertura, por la
garganta de luz.

## 3.7 Un detalle del plano, no del cálculo

En el plano de carpinterías hay un **bloque suelto rotulado "PV04 1,50"** al
final de la fila de las PV, con un rótulo y una cota pero **sin ficha**: sin
tipo de abertura, sin ubicación, sin cantidad, sin forma de abrir. **No es una
abertura** y no está computada. La PV04 real es una sola, de 2,06, cantidad 1,
en el dormitorio sur. Conviene borrar ese bloque del plano.

## 3.8 Balance térmico: lo que conviene poder explicar

**Qué significa la orientación de una pared.** Es hacia dónde mira la pared
parada adentro del local: el punto cardinal del lado de afuera. En una pared
exterior coincide con la fachada. En una **interior**, la misma pared tiene dos
caras, una por local, con orientaciones opuestas: la pared que el hall ve al NE
es la que el vestidor ve al SO.

**Qué lleva el rótulo de cada pared.** Sólo la orientación, tanto en las
aisladas como en las interiores: `AISLADAS (NO)`, `INTERIORES (NE)`. No se
escribe con qué local linda ni qué abertura tiene.

**Por qué aparecen tres renglones de techo (y dos de piso).** Es el formulario de
la cátedra, que trae impresas todas las opciones y se completa sólo la que
corresponde. En planta baja corresponde **techo entrepiso** (factor 15, porque
arriba hay otro local calefaccionado) y **piso sobre tierra** (10). En planta alta,
**techo aislado** (20, cubierta con aislación) y **piso sobre local ocupado** (15).
La misma losa de 12 cm es techo entrepiso abajo y piso sobre local ocupado
arriba.

**Paredes enteras, sin descontar aberturas.** El método de la cátedra computa
cada pared completa y suma la abertura aparte (factor 60). Así lo hace el
formulario modelo y así se hizo en todos los locales.

**Aislada o interior.** Aislada es la que da al exterior (factor 20, paquete con
25 mm de EPS). Interior es la que da a otro local (factor 25). El factor de la
interior es mayor que el de la aislada porque se la supone sin aislación.

**Dos locales sin radiador.** El **hall** se suma al living y la **escalera** al
play room, porque están abiertos a ellos y el aire es el mismo. El radiador se
dimensiona con el total, que figura en cada bloque como "CARGA TOTAL A CUBRIR".

**Baranda de la escalera, play room.** Una de las paredes de 4,08 m del play room
es una baranda, no un muro. No se cuenta como pared: entre el play room y la
escalera hay un solo ambiente.

**Pared del living a la escalera.** Llega hasta la losa, sobre el baño exterior
(12) que está bajo la escalera. Se cuenta como muro completo.

**Hall: la puerta de ingreso H01 — a consultar.** Mide 1,50 × 3,00, es de
**hierro** y está en la planilla de herrería, no en la de carpintería. Se la
computó como abertura (renglón VENTANA, factor 60), igual que si fuera
vidriada. Es la opción conservadora, pero la puerta es opaca, y como las
paredes se cuentan enteras, el área de la puerta ya está dentro de la pared SE
de 2,15 × 3,00 (factor 20). **Consultar** cómo trata las puertas el método de
la cátedra. Si no las carga como ventana, el hall pasa de 2.340 a 2.051 kcal/h
y el living de 8.065 a 7.776 kcal/h (de 30 a 29 elementos).

**Vestidor.** Es en L: el lado largo de 4,87 se separa en 1,70 exterior y 3,17
interior (hacia el hall), y del lado opuesto hay tres tramos cortos (3,38, 0,57 y
1,49). El extremo de 1,09 **no tiene pared**: se entra sin puerta, así que no se
computa.

**Cosas para chequear antes de la defensa.**

- El hall comparte con el vestidor una pared de **4,00**, pero el tramo interior
  del vestidor que da al hall es de **3,17**. No coinciden: conviene mirar el plano.
- Las **superficies** de los croquis no cierran del todo con las de la planilla.
  La más dudosa es la escalera: la planilla usa 7,02 m² (del detalle
  estructural) y la polilínea da unos 4,6 m².
- **Consultar:** si la puerta de hierro H01 se carga como abertura (factor 60) o
  queda dentro de la pared. Hoy está cargada como vidriada.

---

# Resumen de verificaciones

| Planilla | Verifican |
|---|---|
| Iluminación y ventilación | 13 / 13 |
| Planilla 3 higrotérmica | 19 / 19 |
| Vigas | 30 / 31 — falla VCH 03a |
| Losas | 10 / 10 |
| Columnas | 12 / 13 — falla C9 |
| Vigas de fundación | 29 / 31 |
| Pilotes y cabezales | 9 / 9 |
| Tabiques | 12 / 13 — falla T07 |
| Balance térmico | 12 locales, 27.677 kcal/h |

Tres resultados que no verifican sobre unos 140 elementos calculados. En una
casa ya construida eso es esperable, y **saber explicar por qué aparecen suele
valer más que que no aparezcan**.
