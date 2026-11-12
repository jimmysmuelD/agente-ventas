# Informe de ventas 2025 – Distribuidora Pacífico S.A.

Generado por `scripts/analisis.py` el 2026-11-12. Todas las cifras salen de ese script (también en `informes/resultados.json`). Montos en USD con 2 decimales (separador de miles «,», decimal «.»).

## 1. Resumen ejecutivo

- Qué pasó: ventas netas de USD 79,717.57 con margen bruto de USD 27,714.57 (34.77 %), 2962 pedidos y 380 clientes; S2 creció 7.05 % sobre S1. Picos en Dic (USD 10,033.50) y May (USD 9,371.87).
- Cambio de canal: Online creció 152.15 % en S2 mientras Tienda física cayó 23.63 %; Online ya pesa 15.93 % de las ventas del año.
- Qué preocupa: «Gaseosa cola 3L» cayó 74.66 % en S2 frente a S1, y 89 clientes en riesgo concentran USD 11,689.87 (14.66 %).
- Dependencia: 87 clientes Campeones generan 60.08 % de las ventas; las líneas con descuento > 15 % dejan solo 23.42 % de margen.
- Qué hacer: invertir en el canal Online y en la región Amazonía, investigar la caída de Gaseosa cola 3L, reactivar a los clientes en riesgo y pilotear un tope de descuento de 15 % en Mayorista.

## 2. Calidad de datos

- Filas en `datos/ventas_2025.csv`: **3000** (archivo original sin modificar).
- Duplicados exactos (las 12 columnas idénticas): **15**.
- Celdas vacías por columna: unidades = 10, precio_unitario = 10 (resto de columnas: 0; ninguna fila tiene ambas vacías).
- Unidades negativas o cero (tras quitar duplicados): **3**.
- Fechas que no cumplen AAAA-MM-DD: **2** (2025.08.21, 28/09/2025).

**Reglas de limpieza exactas (aplicadas en este orden):**

1. Duplicados exactos: se compara la fila completa (12 columnas, texto tal cual); se conserva la primera aparición.
2. Se elimina la fila si `unidades` o `precio_unitario` está vacío (no se imputa).
3. Se elimina la fila si `unidades` ≤ 0 (no hay columna que identifique devoluciones ni el pedido original, así que no se tratan como devolución).
4. Fechas que no cumplen AAAA-MM-DD se corrigen solo si el formato es inequívoco: `AAAA.MM.DD` o `AAAA/MM/DD` → AAAA-MM-DD; `DD/MM/AAAA` → AAAA-MM-DD solo si el día es > 12. Si fuera ambigua o inválida se eliminaría (no hubo casos). Fechas corregidas:
   - PED-01769: «2025.08.21» → 2025-08-21
   - PED-02058: «28/09/2025» → 2025-09-28
5. No se modifican precios, descuentos ni costos (se revisaron los rangos por producto y no hay valores atípicos).

| Motivo | Filas eliminadas |
|---|---|
| duplicado exacto (se conserva 1 copia) | 15 |
| unidades o precio_unitario vacío | 20 |
| unidades negativas o cero | 3 |
| **Total eliminadas** | **38** |

Filas antes: **3000** → filas después: **2962** (`datos/ventas_limpias.csv`). Tras la limpieza cada fila tiene un `id_pedido` único (2962), por eso nº de pedidos = nº de filas.

## 3. KPIs

| KPI | Valor |
|---|---|
| Ventas netas | USD 79,717.57 |
| Costo total | USD 52,003.00 |
| Margen bruto | USD 27,714.57 |
| Margen % | 34.77 % |
| Pedidos (id_pedido únicos) | 2962 |
| Ticket promedio (ventas / pedidos) | USD 26.91 |
| Clientes activos | 380 |
| Unidades vendidas | 24236 |
| Descuento medio ponderado por venta bruta | 8.96 % |

Fórmulas: ventas netas = unidades × precio_unitario × (1 − descuento_pct/100); costo = unidades × costo_unitario; margen = ventas − costo; margen % = margen / ventas. El crecimiento mes a mes está en 4.1.

## 4. Análisis por dimensión

### 4.1 Por mes

| Mes | Ventas netas | Margen % | Pedidos | Crecimiento vs mes anterior |
|---|---|---|---|---|
| Ene | USD 5,977.50 | 34.70 % | 207 | – |
| Feb | USD 5,117.67 | 35.16 % | 185 | -14.38 % |
| Mar | USD 6,312.51 | 34.72 % | 209 | 23.35 % |
| Abr | USD 5,572.76 | 35.69 % | 204 | -11.72 % |
| May | USD 9,371.87 | 35.44 % | 324 | 68.17 % |
| Jun | USD 6,149.56 | 34.83 % | 233 | -34.38 % |
| Jul | USD 6,038.12 | 34.16 % | 232 | -1.81 % |
| Ago | USD 6,056.22 | 35.44 % | 231 | 0.30 % |
| Sep | USD 6,559.76 | 34.02 % | 233 | 8.31 % |
| Oct | USD 6,274.72 | 34.40 % | 244 | -4.35 % |
| Nov | USD 6,253.38 | 34.11 % | 267 | -0.34 % |
| Dic | USD 10,033.50 | 34.54 % | 393 | 60.45 % |

Mes con más ventas: **Dic** (USD 10,033.50); mes con menos: **Feb** (USD 5,117.67). Profundización de los picos: en mayo Cuidado personal vendió USD 3,170.61 y Hogar USD 2,403.33 (frente a USD 997.92 y USD 949.15 en abril); en diciembre suben casi todas las categorías, sobre todo Hogar (USD 2,733.53), Bebidas (USD 2,518.07) y Snacks (USD 1,924.61). Hipótesis (no verificable con estos datos): Día de la Madre en mayo y temporada navideña en diciembre.

S1 vs S2 total: USD 38,501.88 → USD 41,215.69 (7.05 %).

### 4.2 Por región

| Valor | Ventas netas | Margen USD | Margen % | Participación % | Pedidos |
|---|---|---|---|---|---|
| Costa | USD 37,394.03 | USD 12,981.12 | 34.71 % | 46.91 % | 1379 |
| Sierra | USD 31,871.46 | USD 11,207.36 | 35.16 % | 39.98 % | 1214 |
| Amazonía | USD 7,465.31 | USD 2,583.96 | 34.61 % | 9.36 % | 272 |
| Insular | USD 2,986.78 | USD 942.13 | 31.54 % | 3.75 % | 97 |

S1 vs S2:

| Valor | S1 | S2 | Variación |
|---|---|---|---|
| Insular | USD 1,156.45 | USD 1,830.33 | 58.27 % |
| Amazonía | USD 3,120.97 | USD 4,344.34 | 39.20 % |
| Sierra | USD 15,613.44 | USD 16,258.02 | 4.13 % |
| Costa | USD 18,611.02 | USD 18,783.00 | 0.92 % |

Ventas por ciudad:

| Valor | Ventas netas | Margen USD | Margen % | Participación % | Pedidos |
|---|---|---|---|---|---|
| Manta | USD 16,008.63 | USD 5,550.98 | 34.67 % | 20.08 % | 567 |
| Quito | USD 14,975.57 | USD 5,188.87 | 34.65 % | 18.79 % | 548 |
| Machala | USD 12,934.92 | USD 4,460.27 | 34.48 % | 16.23 % | 483 |
| Cuenca | USD 8,597.37 | USD 3,029.92 | 35.24 % | 10.78 % | 370 |
| Guayaquil | USD 8,450.48 | USD 2,969.88 | 35.14 % | 10.60 % | 329 |
| Ambato | USD 8,298.52 | USD 2,988.57 | 36.01 % | 10.41 % | 296 |
| Tena | USD 3,866.54 | USD 1,290.34 | 33.37 % | 4.85 % | 139 |
| Puyo | USD 3,598.77 | USD 1,293.62 | 35.95 % | 4.51 % | 133 |
| Puerto Ayora | USD 2,986.78 | USD 942.13 | 31.54 % | 3.75 % | 97 |

Insular tiene el margen más bajo porque 52.63 % de sus ventas va por Mayorista (margen 25.66 %) y su descuento medio es 12.72 % (global 8.96 %).

### 4.3 Por canal

| Valor | Ventas netas | Margen USD | Margen % | Participación % | Pedidos |
|---|---|---|---|---|---|
| Tienda física | USD 36,563.56 | USD 14,230.71 | 38.92 % | 45.87 % | 1664 |
| Mayorista | USD 30,458.40 | USD 8,898.70 | 29.22 % | 38.21 % | 437 |
| Online | USD 12,695.61 | USD 4,585.16 | 36.12 % | 15.93 % | 861 |

S1 vs S2:

| Valor | S1 | S2 | Variación |
|---|---|---|---|
| Online | USD 3,605.18 | USD 9,090.43 | 152.15 % |
| Mayorista | USD 14,165.07 | USD 16,293.33 | 15.02 % |
| Tienda física | USD 20,731.62 | USD 15,831.94 | -23.63 % |

Ventas mensuales por canal (USD):

| Canal | Ene | Feb | Mar | Abr | May | Jun | Jul | Ago | Sep | Oct | Nov | Dic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tienda física | 3,485.17 | 3,284.49 | 3,101.53 | 3,566.22 | 4,554.34 | 2,739.87 | 2,124.63 | 3,015.70 | 2,644.35 | 2,526.72 | 2,093.75 | 3,426.78 |
| Mayorista | 2,273.86 | 1,562.37 | 2,776.51 | 1,441.95 | 3,613.56 | 2,496.84 | 2,822.06 | 2,055.81 | 2,576.90 | 2,207.08 | 2,629.71 | 4,001.77 |
| Online | 218.48 | 270.81 | 434.47 | 564.59 | 1,203.97 | 912.85 | 1,091.43 | 984.71 | 1,338.50 | 1,540.91 | 1,529.92 | 2,604.95 |

Online crece en todas las regiones; Tienda física cae en todas salvo Amazonía (variación S1 → S2):

| Región | Online | Tienda física | Mayorista |
|---|---|---|---|
| Amazonía | 420.89 % | 19.99 % | -14.84 % |
| Costa | 97.73 % | -25.26 % | 14.52 % |
| Insular | 278.79 % | -21.89 % | 110.95 % |
| Sierra | 157.86 % | -29.15 % | 14.38 % |

Descuento medio ponderado por canal: Tienda física 2.75 %, Mayorista 16.21 %, Online 6.77 %. Esto explica por qué Mayorista tiene el margen más bajo.

### 4.4 Por categoría

| Valor | Ventas netas | Margen USD | Margen % | Participación % | Pedidos |
|---|---|---|---|---|---|
| Limpieza | USD 17,668.24 | USD 5,735.04 | 32.46 % | 22.16 % | 591 |
| Bebidas | USD 17,580.88 | USD 5,963.28 | 33.92 % | 22.05 % | 755 |
| Hogar | USD 17,448.46 | USD 5,498.46 | 31.51 % | 21.89 % | 226 |
| Cuidado personal | USD 15,843.67 | USD 5,995.27 | 37.84 % | 19.87 % | 634 |
| Snacks | USD 11,176.32 | USD 4,522.52 | 40.47 % | 14.02 % | 756 |

S1 vs S2:

| Valor | S1 | S2 | Variación |
|---|---|---|---|
| Hogar | USD 7,247.60 | USD 10,200.87 | 40.75 % |
| Snacks | USD 4,958.61 | USD 6,217.70 | 25.39 % |
| Bebidas | USD 9,028.08 | USD 8,552.80 | -5.26 % |
| Limpieza | USD 9,074.70 | USD 8,593.54 | -5.30 % |
| Cuidado personal | USD 8,192.88 | USD 7,650.79 | -6.62 % |

### 4.5 Por producto

**Top 5 por ventas netas**

| Producto | Ventas netas | Margen % | Participación % |
|---|---|---|---|
| Detergente 2kg | USD 11,605.11 | 30.19 % | 14.56 % |
| Agua mineral 6x1L | USD 8,402.94 | 33.25 % | 10.54 % |
| Shampoo 400ml | USD 7,856.46 | 37.38 % | 9.86 % |
| Set de ollas | USD 7,654.05 | 28.04 % | 9.60 % |
| Juego de toallas | USD 5,174.24 | 35.87 % | 6.49 % |

**Bottom 5 por ventas netas** (de menor a mayor)

| Producto | Ventas netas | Margen % | Participación % |
|---|---|---|---|
| Cloro 1L | USD 2,360.92 | 37.82 % | 2.96 % |
| Chocolate 100g | USD 3,240.55 | 39.70 % | 4.07 % |
| Galletas integrales | USD 3,622.04 | 42.35 % | 4.54 % |
| Crema dental 150g | USD 3,675.54 | 37.96 % | 4.61 % |
| Desinfectante multiuso | USD 3,702.21 | 36.16 % | 4.64 % |

S1 vs S2 por producto:

| Producto | S1 | S2 | Variación |
|---|---|---|---|
| Vajilla 12 piezas | USD 1,826.29 | USD 2,793.88 | 52.98 % |
| Chocolate 100g | USD 1,311.03 | USD 1,929.52 | 47.18 % |
| Juego de toallas | USD 2,135.98 | USD 3,038.27 | 42.24 % |
| Agua mineral 6x1L | USD 3,507.73 | USD 4,895.21 | 39.56 % |
| Jugo de naranja 1L | USD 2,094.95 | USD 2,789.75 | 33.17 % |
| Set de ollas | USD 3,285.33 | USD 4,368.72 | 32.98 % |
| Crema dental 150g | USD 1,619.54 | USD 2,055.99 | 26.95 % |
| Papas fritas 200g | USD 1,948.26 | USD 2,365.46 | 21.41 % |
| Galletas integrales | USD 1,699.32 | USD 1,922.72 | 13.15 % |
| Desinfectante multiuso | USD 1,826.65 | USD 1,875.56 | 2.68 % |
| Cloro 1L | USD 1,213.78 | USD 1,147.14 | -5.49 % |
| Detergente 2kg | USD 6,034.27 | USD 5,570.84 | -7.68 % |
| Shampoo 400ml | USD 4,235.29 | USD 3,621.17 | -14.50 % |
| Jabón de tocador x3 | USD 2,338.04 | USD 1,973.63 | -15.59 % |
| Gaseosa cola 3L | USD 3,425.40 | USD 867.84 | -74.66 % |

Profundización Gaseosa cola 3L – ventas por mes: Ene USD 584.01, Feb USD 434.28, Mar USD 530.13, Abr USD 399.05, May USD 655.19, Jun USD 822.74, Jul USD 96.57, Ago USD 122.46, Sep USD 190.98, Oct USD 77.99, Nov USD 57.89, Dic USD 321.95. Variación S1→S2 por canal: Online -4.51 %, Tienda física -79.08 %, Mayorista -81.62 %; por región: Amazonía -20.66 %, Sierra -76.30 %, Costa -77.71 %, Insular -100.00 %.

## 5. Segmentación RFM

- Fecha de referencia: 2025-12-31. Recencia = días desde la última compra; Frecuencia = nº de `id_pedido` distintos; Monto = ventas netas del cliente.
- Puntajes 1-5 por quintiles de rango: puntaje = min(5, 1 + ⌊5·k / n⌋), con n = 380 clientes y k = nº de clientes con valor estrictamente peor (en R, peor = más días; en F y M, peor = menor valor). **Empates**: los clientes con el mismo valor reciben siempre el mismo puntaje (por eso los grupos de F no tienen el mismo tamaño).
- Segmentos en orden (gana la primera regla que se cumple): Campeones R≥4 y F≥4; Leales R≥3 y F≥3; Potenciales R≥3 y F≤2; En riesgo R=2, o R=1 y F≥3; Perdidos R=1 y F≤2. M se calcula pero no interviene.

Clientes por puntaje:

| Puntaje | R | F | M |
|---|---|---|---|
| 1 | 76 | 86 | 76 |
| 2 | 78 | 99 | 76 |
| 3 | 78 | 50 | 76 |
| 4 | 72 | 83 | 76 |
| 5 | 76 | 62 | 76 |

| Segmento | Clientes | Ventas netas | % ventas | Recencia media (días) | Frecuencia media | Acción comercial |
|---|---|---|---|---|---|---|
| Campeones | 87 | USD 47,893.56 | 60.08 % | 9.60 | 20.85 | Programa VIP: acceso anticipado, beneficios por volumen y pedirles referidos. |
| Leales | 62 | USD 10,265.53 | 12.88 % | 32.26 | 6.21 | Venta cruzada de categorías que aún no compran y puntos de fidelidad. |
| Potenciales | 77 | USD 6,547.32 | 8.21 % | 24.09 | 3.14 | Incentivar la segunda/tercera compra con cupón de recompra a 30 días. |
| En riesgo | 89 | USD 11,689.87 | 14.66 % | 101.28 | 4.38 | Contacto proactivo del vendedor y oferta personalizada de reactivación. |
| Perdidos | 65 | USD 3,321.28 | 4.17 % | 236.49 | 2.02 | Campaña de bajo costo (correo/WhatsApp); no invertir descuentos altos. |

Comprobación: 87 + 62 + 77 + 89 + 65 = 380 clientes = clientes activos (380). Detalle por cliente en `informes/rfm_clientes.csv`.

## 6. Preguntas de negocio

**1. ¿Qué región merece más inversión el próximo año y por qué?**

Amazonía. Es la región con mayor crecimiento S2 vs S1 (39.20 %: USD 3,120.97 a USD 4,344.34) entre las que mantienen un margen cercano al promedio (34.61 % frente a 34.77 % global). Tiene solo 37 clientes y 9.36 % de las ventas, así que hay espacio para crecer; su canal Online pasó de USD 270.54 a USD 1,409.20. Insular crece más (58.27 %) pero sobre una base pequeña (USD 2,986.78) y con el margen más bajo (31.54 %, descuento medio 12.72 % y 52.63 % de sus ventas por Mayorista): no conviene invertir ahí sin antes corregir precios y descuentos. Costa sigue siendo la mayor (46.91 %) pero casi no crece (0.92 %); Sierra tiene el mejor margen (35.16 %) y debe protegerse.

**2. ¿Qué producto conviene revisar o descontinuar?**

Revisar «Gaseosa cola 3L»: sus ventas cayeron 74.66 % entre S1 (USD 3,425.40) y S2 (USD 867.84). La caída es abrupta desde julio (líneas de pedido por mes ene-jun: 26, 15, 21, 19, 28, 28; jul-dic: 9, 8, 5, 4, 4, 14) y ocurre en Tienda física (-79.08 %) y Mayorista (-81.62 %), no en Online (-4.51 %). Un corte tan brusco sugiere un problema de abastecimiento o de listado más que de demanda: hay que verificarlo antes de decidir descontinuarlo. Además, «Set de ollas» tiene el margen más bajo (28.04 % frente a 34.77 %); conviene revisar su precio o costo. No se recomienda descontinuar el producto con menos ventas («Cloro 1L», USD 2,360.92) porque su margen es 37.82 %.

**3. ¿Qué canal potenciar?**

Potenciar Online: creció 152.15 % (de USD 3,605.18 en S1 a USD 9,090.43 en S2), crece en las cuatro regiones y tiene buen margen (36.12 %). En paralelo, Tienda física cayó 23.63 % y sigue siendo el canal más grande (45.87 %) y de mayor margen (38.92 %): hay que entender si sus clientes se están pasando a Online (canibalización) o se están perdiendo. Mayorista tiene el margen más bajo (29.22 %) por su descuento medio de 16.21 %.

**4. ¿Qué hacer con los clientes en riesgo?**

Son 89 clientes que suman USD 11,689.87 (14.66 % de las ventas) y llevan en promedio 101.28 días sin comprar. Los 20 de mayor monto concentran USD 5,819.60: priorizarlos con llamada del vendedor y oferta personalizada (listado en informes/rfm_clientes.csv). Por región, Costa concentra 54.63 % de sus compras; por canal, compraban sobre todo en Tienda física (46.23 %), el canal que más cae en S2. Usar descuentos de hasta 15 % (no mayores, ver pregunta 5) y medir reactivación a 60 días.

**5. ¿Qué pasaría con el margen si se eliminan los descuentos mayores al 15 %?**

Hay 211 líneas con descuento mayor a 15 % (USD 11,402.35 en ventas, margen 23.42 %; por canal: Mayorista 151, Online 60). Escenario A (supuesto: esas ventas se mantienen con descuento de 15 %): ventas USD 80,783.97, margen USD 28,780.97 (35.63 %), es decir USD 1,066.40 más de margen que hoy (USD 27,714.57, 34.77 %). Escenario B (supuesto: esas ventas se pierden): ventas USD 68,315.22, margen USD 25,043.87 (36.66 %); el margen % sube pero el margen en dólares cae USD 2,670.70. Conclusión: limitar a 15 % solo conviene si la mayoría de esos clientes (sobre todo mayoristas) sigue comprando; probarlo primero con un grupo piloto.

## 7. Limitaciones

- Datos ficticios de un solo año (2025): no hay base para comparar con 2024 ni estacionalidad de años previos.
- No hay datos de inventario, marketing, competencia ni devoluciones: las causas propuestas (quiebre de stock de Gaseosa, Día de la Madre, Navidad, canibalización de canales) son hipótesis.
- Se eliminaron 38 filas (1.27 % del original); las 3 con unidades negativas podrían ser devoluciones no registradas como tales.
- Los escenarios de descuento son extremos (todo se mantiene o todo se pierde); la realidad estará entre ambos y no considera efectos en otros productos.
- RFM por quintiles de rango: con muchos empates en Frecuencia los grupos no son exactamente iguales.
- Cada fila es un pedido de un solo producto, así que el ticket promedio es por línea de pedido.
