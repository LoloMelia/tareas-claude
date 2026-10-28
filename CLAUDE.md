
## Convenciones de las planillas (pedidas por el autor)

- **Bordes**: el perímetro de cada tabla va en línea llena; las líneas
  interiores, en línea de puntos, salvo las que tocan un encabezado, que van
  llenas. Implementado en `planillas/plantas/bordes.py`.
- **Alto de fila**: 0,7 cm (19,8 pt), y sólo crece si el texto no entra. Las
  filas de **título** (las de relleno gris) miden 1 cm (28,4 pt).
- **Bordes (precisión)**: título = celda con relleno gris; la negrita sola no es
  título. Las líneas interiores, en puntos; las del título y el perímetro, llenas.
- **Balance térmico**: una fila en blanco entre un bloque de local y el siguiente.
- **Versión para AutoCAD**: las planillas se pegan en AutoCAD, donde se
  pierden las referencias entre hojas. Por eso se entrega además una copia
  sin una sola fórmula (todo valor fijo), sin filas vacías y sin las columnas
  auxiliares de carga. Se genera con:
  `python3 desvincular.py <original> <recalculado por LibreOffice> <salida>`
  y después `python3 compactar.py <salida> <final>`.
- **Rótulos de paredes en el balance térmico**: sólo la orientación, por
  ejemplo `AISLADAS (NO)` o `INTERIORES (NE)`. Nunca el local con el que linda
  ni la abertura. La orientación es hacia donde mira la pared parada adentro
  del local; aislada = exterior.
