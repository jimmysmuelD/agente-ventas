# Verificación independiente de cifras – Informe de ventas 2025

- Fecha de verificación: 2026-11-12
- Script: `scripts/verificar.py` (solo librería estándar; no reutiliza `scripts/analisis.py` ni lee `datos/ventas_limpias.csv`).
- Fuente: `datos/ventas_2025.csv` (original, solo lectura).
- Tolerancia: diferencia relativa ≤ 0,5 % (o igualdad al redondear a 2 decimales). Textos: coincidencia exacta.

## Reglas de limpieza aplicadas (sección 2 del informe)

1. Duplicados exactos (12 columnas, texto tal cual), se conserva la primera aparición: 15 filas eliminadas.
2. `unidades` o `precio_unitario` vacío: 20 filas eliminadas.
3. `unidades` ≤ 0: 3 filas eliminadas.
4. Fechas: `AAAA.MM.DD`/`AAAA/MM/DD` → AAAA-MM-DD; `DD/MM/AAAA` solo si día > 12; ambigua o inválida → se elimina. Corregidas: PED-01769 («2025.08.21»), PED-02058 («28/09/2025»); eliminadas: 0.
5. Precios, descuentos y costos sin cambios.

Filas: 3000 → 2962 (38 eliminadas).

Fórmulas: ventas netas = unidades × precio_unitario × (1 − descuento_pct/100); costo = unidades × costo_unitario; S1 = ene-jun, S2 = jul-dic. RFM: fecha de referencia 2025-12-31, puntaje = min(5, 1 + ⌊5·k/n⌋) con k = nº de clientes estrictamente peores, segmentos según la sección 5 del informe.

## Resumen

- **Informe (`informes/informe_ventas.md`): 448 OK, 0 ERROR** de 448 cifras comprobadas.
- **Dashboard (`docs/index.html`, datos embebidos): 743 OK, 0 ERROR** de 743 valores comprobados.

No se encontraron errores.

## Detalle – informe

| Sección | Cifra | Valor en informe | Valor recalculado | Estado |
|---|---|---|---|---|
| 2. Calidad | Filas originales | 3000 | 3000 | OK |
| 2. Calidad | Duplicados exactos eliminados | 15 | 15 | OK |
| 2. Calidad | Filas con unidades o precio vacío eliminadas | 20 | 20 | OK |
| 2. Calidad | Filas con unidades <= 0 eliminadas | 3 | 3 | OK |
| 2. Calidad | Fechas corregidas (nº) | 2 | 2 | OK |
| 2. Calidad | Fechas corregidas (ids) | PED-01769, PED-02058 | PED-01769, PED-02058 | OK |
| 2. Calidad | Filas eliminadas por fecha inválida | 0 | 0 | OK |
| 2. Calidad | Total filas eliminadas | 38 | 38 | OK |
| 2. Calidad | Filas tras limpieza | 2962 | 2962 | OK |
| 2. Calidad | id_pedido únicos tras limpieza | 2962 | 2962 | OK |
| 2. Calidad | % filas eliminadas | 1.27 | 1.27 | OK |
| 3. KPIs | Ventas netas (USD) | 79,717.57 | 79,717.57 | OK |
| 3. KPIs | Costo total (USD) | 52,003.00 | 52,003.00 | OK |
| 3. KPIs | Margen bruto (USD) | 27,714.57 | 27,714.57 | OK |
| 3. KPIs | Margen % | 34.77 | 34.77 | OK |
| 3. KPIs | Pedidos | 2962 | 2962 | OK |
| 3. KPIs | Ticket promedio (USD) | 26.91 | 26.91 | OK |
| 3. KPIs | Clientes activos | 380 | 380 | OK |
| 3. KPIs | Unidades vendidas | 24236 | 24236 | OK |
| 3. KPIs | Descuento medio ponderado % | 8.96 | 8.96 | OK |
| 4.1 Mes | Ene ventas | 5,977.50 | 5,977.50 | OK |
| 4.1 Mes | Ene margen % | 34.70 | 34.70 | OK |
| 4.1 Mes | Ene pedidos | 207 | 207 | OK |
| 4.1 Mes | Feb ventas | 5,117.67 | 5,117.67 | OK |
| 4.1 Mes | Feb margen % | 35.16 | 35.16 | OK |
| 4.1 Mes | Feb pedidos | 185 | 185 | OK |
| 4.1 Mes | Feb crecimiento vs mes anterior % | -14.38 | -14.38 | OK |
| 4.1 Mes | Mar ventas | 6,312.51 | 6,312.51 | OK |
| 4.1 Mes | Mar margen % | 34.72 | 34.72 | OK |
| 4.1 Mes | Mar pedidos | 209 | 209 | OK |
| 4.1 Mes | Mar crecimiento vs mes anterior % | 23.35 | 23.35 | OK |
| 4.1 Mes | Abr ventas | 5,572.76 | 5,572.76 | OK |
| 4.1 Mes | Abr margen % | 35.69 | 35.69 | OK |
| 4.1 Mes | Abr pedidos | 204 | 204 | OK |
| 4.1 Mes | Abr crecimiento vs mes anterior % | -11.72 | -11.72 | OK |
| 4.1 Mes | May ventas | 9,371.87 | 9,371.87 | OK |
| 4.1 Mes | May margen % | 35.44 | 35.44 | OK |
| 4.1 Mes | May pedidos | 324 | 324 | OK |
| 4.1 Mes | May crecimiento vs mes anterior % | 68.17 | 68.17 | OK |
| 4.1 Mes | Jun ventas | 6,149.56 | 6,149.56 | OK |
| 4.1 Mes | Jun margen % | 34.83 | 34.83 | OK |
| 4.1 Mes | Jun pedidos | 233 | 233 | OK |
| 4.1 Mes | Jun crecimiento vs mes anterior % | -34.38 | -34.38 | OK |
| 4.1 Mes | Jul ventas | 6,038.12 | 6,038.12 | OK |
| 4.1 Mes | Jul margen % | 34.16 | 34.16 | OK |
| 4.1 Mes | Jul pedidos | 232 | 232 | OK |
| 4.1 Mes | Jul crecimiento vs mes anterior % | -1.81 | -1.81 | OK |
| 4.1 Mes | Ago ventas | 6,056.22 | 6,056.22 | OK |
| 4.1 Mes | Ago margen % | 35.44 | 35.44 | OK |
| 4.1 Mes | Ago pedidos | 231 | 231 | OK |
| 4.1 Mes | Ago crecimiento vs mes anterior % | 0.30 | 0.30 | OK |
| 4.1 Mes | Sep ventas | 6,559.76 | 6,559.76 | OK |
| 4.1 Mes | Sep margen % | 34.02 | 34.02 | OK |
| 4.1 Mes | Sep pedidos | 233 | 233 | OK |
| 4.1 Mes | Sep crecimiento vs mes anterior % | 8.31 | 8.31 | OK |
| 4.1 Mes | Oct ventas | 6,274.72 | 6,274.72 | OK |
| 4.1 Mes | Oct margen % | 34.40 | 34.40 | OK |
| 4.1 Mes | Oct pedidos | 244 | 244 | OK |
| 4.1 Mes | Oct crecimiento vs mes anterior % | -4.35 | -4.35 | OK |
| 4.1 Mes | Nov ventas | 6,253.38 | 6,253.38 | OK |
| 4.1 Mes | Nov margen % | 34.11 | 34.11 | OK |
| 4.1 Mes | Nov pedidos | 267 | 267 | OK |
| 4.1 Mes | Nov crecimiento vs mes anterior % | -0.34 | -0.34 | OK |
| 4.1 Mes | Dic ventas | 10,033.50 | 10,033.50 | OK |
| 4.1 Mes | Dic margen % | 34.54 | 34.54 | OK |
| 4.1 Mes | Dic pedidos | 393 | 393 | OK |
| 4.1 Mes | Dic crecimiento vs mes anterior % | 60.45 | 60.45 | OK |
| 4.1 Mes | Mes con más ventas | Dic | Dic | OK |
| 4.1 Mes | Mes con menos ventas | Feb | Feb | OK |
| 4.1 Mes | May Cuidado personal | 3,170.61 | 3,170.61 | OK |
| 4.1 Mes | May Hogar | 2,403.33 | 2,403.33 | OK |
| 4.1 Mes | Abr Cuidado personal | 997.92 | 997.92 | OK |
| 4.1 Mes | Abr Hogar | 949.15 | 949.15 | OK |
| 4.1 Mes | Dic Hogar | 2,733.53 | 2,733.53 | OK |
| 4.1 Mes | Dic Bebidas | 2,518.07 | 2,518.07 | OK |
| 4.1 Mes | Dic Snacks | 1,924.61 | 1,924.61 | OK |
| 4.1 Mes | S1 total | 38,501.88 | 38,501.88 | OK |
| 4.1 Mes | S2 total | 41,215.69 | 41,215.69 | OK |
| 4.1 Mes | Crecimiento S2 vs S1 % | 7.05 | 7.05 | OK |
| 4.2 Región | Costa ventas | 37,394.03 | 37,394.03 | OK |
| 4.2 Región | Costa margen USD | 12,981.12 | 12,981.12 | OK |
| 4.2 Región | Costa margen % | 34.71 | 34.71 | OK |
| 4.2 Región | Costa participación % | 46.91 | 46.91 | OK |
| 4.2 Región | Costa pedidos | 1379 | 1379 | OK |
| 4.2 Región | Sierra ventas | 31,871.46 | 31,871.46 | OK |
| 4.2 Región | Sierra margen USD | 11,207.36 | 11,207.36 | OK |
| 4.2 Región | Sierra margen % | 35.16 | 35.16 | OK |
| 4.2 Región | Sierra participación % | 39.98 | 39.98 | OK |
| 4.2 Región | Sierra pedidos | 1214 | 1214 | OK |
| 4.2 Región | Amazonía ventas | 7,465.31 | 7,465.31 | OK |
| 4.2 Región | Amazonía margen USD | 2,583.96 | 2,583.96 | OK |
| 4.2 Región | Amazonía margen % | 34.61 | 34.61 | OK |
| 4.2 Región | Amazonía participación % | 9.36 | 9.36 | OK |
| 4.2 Región | Amazonía pedidos | 272 | 272 | OK |
| 4.2 Región | Insular ventas | 2,986.78 | 2,986.78 | OK |
| 4.2 Región | Insular margen USD | 942.13 | 942.13 | OK |
| 4.2 Región | Insular margen % | 31.54 | 31.54 | OK |
| 4.2 Región | Insular participación % | 3.75 | 3.75 | OK |
| 4.2 Región | Insular pedidos | 97 | 97 | OK |
| 4.2 Región | Insular S1 | 1,156.45 | 1,156.45 | OK |
| 4.2 Región | Insular S2 | 1,830.33 | 1,830.33 | OK |
| 4.2 Región | Insular variación S1→S2 % | 58.27 | 58.27 | OK |
| 4.2 Región | Amazonía S1 | 3,120.97 | 3,120.97 | OK |
| 4.2 Región | Amazonía S2 | 4,344.34 | 4,344.34 | OK |
| 4.2 Región | Amazonía variación S1→S2 % | 39.20 | 39.20 | OK |
| 4.2 Región | Sierra S1 | 15,613.44 | 15,613.44 | OK |
| 4.2 Región | Sierra S2 | 16,258.02 | 16,258.02 | OK |
| 4.2 Región | Sierra variación S1→S2 % | 4.13 | 4.13 | OK |
| 4.2 Región | Costa S1 | 18,611.02 | 18,611.02 | OK |
| 4.2 Región | Costa S2 | 18,783.00 | 18,783.00 | OK |
| 4.2 Región | Costa variación S1→S2 % | 0.92 | 0.92 | OK |
| 4.2 Región | Región que más crece (S2 vs S1) | Insular | Insular | OK |
| 4.2 Ciudad | Manta ventas | 16,008.63 | 16,008.63 | OK |
| 4.2 Ciudad | Manta margen USD | 5,550.98 | 5,550.98 | OK |
| 4.2 Ciudad | Manta margen % | 34.67 | 34.67 | OK |
| 4.2 Ciudad | Manta participación % | 20.08 | 20.08 | OK |
| 4.2 Ciudad | Manta pedidos | 567 | 567 | OK |
| 4.2 Ciudad | Quito ventas | 14,975.57 | 14,975.57 | OK |
| 4.2 Ciudad | Quito margen USD | 5,188.87 | 5,188.87 | OK |
| 4.2 Ciudad | Quito margen % | 34.65 | 34.65 | OK |
| 4.2 Ciudad | Quito participación % | 18.79 | 18.79 | OK |
| 4.2 Ciudad | Quito pedidos | 548 | 548 | OK |
| 4.2 Ciudad | Machala ventas | 12,934.92 | 12,934.92 | OK |
| 4.2 Ciudad | Machala margen USD | 4,460.27 | 4,460.27 | OK |
| 4.2 Ciudad | Machala margen % | 34.48 | 34.48 | OK |
| 4.2 Ciudad | Machala participación % | 16.23 | 16.23 | OK |
| 4.2 Ciudad | Machala pedidos | 483 | 483 | OK |
| 4.2 Ciudad | Cuenca ventas | 8,597.37 | 8,597.37 | OK |
| 4.2 Ciudad | Cuenca margen USD | 3,029.92 | 3,029.92 | OK |
| 4.2 Ciudad | Cuenca margen % | 35.24 | 35.24 | OK |
| 4.2 Ciudad | Cuenca participación % | 10.78 | 10.78 | OK |
| 4.2 Ciudad | Cuenca pedidos | 370 | 370 | OK |
| 4.2 Ciudad | Guayaquil ventas | 8,450.48 | 8,450.48 | OK |
| 4.2 Ciudad | Guayaquil margen USD | 2,969.88 | 2,969.88 | OK |
| 4.2 Ciudad | Guayaquil margen % | 35.14 | 35.14 | OK |
| 4.2 Ciudad | Guayaquil participación % | 10.60 | 10.60 | OK |
| 4.2 Ciudad | Guayaquil pedidos | 329 | 329 | OK |
| 4.2 Ciudad | Ambato ventas | 8,298.52 | 8,298.52 | OK |
| 4.2 Ciudad | Ambato margen USD | 2,988.57 | 2,988.57 | OK |
| 4.2 Ciudad | Ambato margen % | 36.01 | 36.01 | OK |
| 4.2 Ciudad | Ambato participación % | 10.41 | 10.41 | OK |
| 4.2 Ciudad | Ambato pedidos | 296 | 296 | OK |
| 4.2 Ciudad | Tena ventas | 3,866.54 | 3,866.54 | OK |
| 4.2 Ciudad | Tena margen USD | 1,290.34 | 1,290.34 | OK |
| 4.2 Ciudad | Tena margen % | 33.37 | 33.37 | OK |
| 4.2 Ciudad | Tena participación % | 4.85 | 4.85 | OK |
| 4.2 Ciudad | Tena pedidos | 139 | 139 | OK |
| 4.2 Ciudad | Puyo ventas | 3,598.77 | 3,598.77 | OK |
| 4.2 Ciudad | Puyo margen USD | 1,293.62 | 1,293.62 | OK |
| 4.2 Ciudad | Puyo margen % | 35.95 | 35.95 | OK |
| 4.2 Ciudad | Puyo participación % | 4.51 | 4.51 | OK |
| 4.2 Ciudad | Puyo pedidos | 133 | 133 | OK |
| 4.2 Ciudad | Puerto Ayora ventas | 2,986.78 | 2,986.78 | OK |
| 4.2 Ciudad | Puerto Ayora margen USD | 942.13 | 942.13 | OK |
| 4.2 Ciudad | Puerto Ayora margen % | 31.54 | 31.54 | OK |
| 4.2 Ciudad | Puerto Ayora participación % | 3.75 | 3.75 | OK |
| 4.2 Ciudad | Puerto Ayora pedidos | 97 | 97 | OK |
| 4.2 Ciudad | Insular: % ventas por Mayorista | 52.63 | 52.63 | OK |
| 4.2 Ciudad | Insular: margen % Mayorista | 25.66 | 25.66 | OK |
| 4.2 Ciudad | Insular: descuento medio ponderado % | 12.72 | 12.72 | OK |
| 4.3 Canal | Tienda física ventas | 36,563.56 | 36,563.56 | OK |
| 4.3 Canal | Tienda física margen USD | 14,230.71 | 14,230.71 | OK |
| 4.3 Canal | Tienda física margen % | 38.92 | 38.92 | OK |
| 4.3 Canal | Tienda física participación % | 45.87 | 45.87 | OK |
| 4.3 Canal | Tienda física pedidos | 1664 | 1664 | OK |
| 4.3 Canal | Mayorista ventas | 30,458.40 | 30,458.40 | OK |
| 4.3 Canal | Mayorista margen USD | 8,898.70 | 8,898.70 | OK |
| 4.3 Canal | Mayorista margen % | 29.22 | 29.22 | OK |
| 4.3 Canal | Mayorista participación % | 38.21 | 38.21 | OK |
| 4.3 Canal | Mayorista pedidos | 437 | 437 | OK |
| 4.3 Canal | Online ventas | 12,695.61 | 12,695.61 | OK |
| 4.3 Canal | Online margen USD | 4,585.16 | 4,585.16 | OK |
| 4.3 Canal | Online margen % | 36.12 | 36.12 | OK |
| 4.3 Canal | Online participación % | 15.93 | 15.93 | OK |
| 4.3 Canal | Online pedidos | 861 | 861 | OK |
| 4.3 Canal | Online S1 | 3,605.18 | 3,605.18 | OK |
| 4.3 Canal | Online S2 | 9,090.43 | 9,090.43 | OK |
| 4.3 Canal | Online variación S1→S2 % | 152.15 | 152.15 | OK |
| 4.3 Canal | Mayorista S1 | 14,165.07 | 14,165.07 | OK |
| 4.3 Canal | Mayorista S2 | 16,293.33 | 16,293.33 | OK |
| 4.3 Canal | Mayorista variación S1→S2 % | 15.02 | 15.02 | OK |
| 4.3 Canal | Tienda física S1 | 20,731.62 | 20,731.62 | OK |
| 4.3 Canal | Tienda física S2 | 15,831.94 | 15,831.94 | OK |
| 4.3 Canal | Tienda física variación S1→S2 % | -23.63 | -23.63 | OK |
| 4.3 Canal | Canal que más crece (S2 vs S1) | Online | Online | OK |
| 4.3 Canal | Tienda física Ene ventas | 3,485.17 | 3,485.17 | OK |
| 4.3 Canal | Tienda física Feb ventas | 3,284.49 | 3,284.49 | OK |
| 4.3 Canal | Tienda física Mar ventas | 3,101.53 | 3,101.53 | OK |
| 4.3 Canal | Tienda física Abr ventas | 3,566.22 | 3,566.22 | OK |
| 4.3 Canal | Tienda física May ventas | 4,554.34 | 4,554.34 | OK |
| 4.3 Canal | Tienda física Jun ventas | 2,739.87 | 2,739.86 | OK |
| 4.3 Canal | Tienda física Jul ventas | 2,124.63 | 2,124.63 | OK |
| 4.3 Canal | Tienda física Ago ventas | 3,015.70 | 3,015.70 | OK |
| 4.3 Canal | Tienda física Sep ventas | 2,644.35 | 2,644.35 | OK |
| 4.3 Canal | Tienda física Oct ventas | 2,526.72 | 2,526.72 | OK |
| 4.3 Canal | Tienda física Nov ventas | 2,093.75 | 2,093.75 | OK |
| 4.3 Canal | Tienda física Dic ventas | 3,426.78 | 3,426.78 | OK |
| 4.3 Canal | Mayorista Ene ventas | 2,273.86 | 2,273.86 | OK |
| 4.3 Canal | Mayorista Feb ventas | 1,562.37 | 1,562.37 | OK |
| 4.3 Canal | Mayorista Mar ventas | 2,776.51 | 2,776.51 | OK |
| 4.3 Canal | Mayorista Abr ventas | 1,441.95 | 1,441.95 | OK |
| 4.3 Canal | Mayorista May ventas | 3,613.56 | 3,613.56 | OK |
| 4.3 Canal | Mayorista Jun ventas | 2,496.84 | 2,496.84 | OK |
| 4.3 Canal | Mayorista Jul ventas | 2,822.06 | 2,822.06 | OK |
| 4.3 Canal | Mayorista Ago ventas | 2,055.81 | 2,055.81 | OK |
| 4.3 Canal | Mayorista Sep ventas | 2,576.90 | 2,576.90 | OK |
| 4.3 Canal | Mayorista Oct ventas | 2,207.08 | 2,207.08 | OK |
| 4.3 Canal | Mayorista Nov ventas | 2,629.71 | 2,629.71 | OK |
| 4.3 Canal | Mayorista Dic ventas | 4,001.77 | 4,001.77 | OK |
| 4.3 Canal | Online Ene ventas | 218.48 | 218.48 | OK |
| 4.3 Canal | Online Feb ventas | 270.81 | 270.81 | OK |
| 4.3 Canal | Online Mar ventas | 434.47 | 434.47 | OK |
| 4.3 Canal | Online Abr ventas | 564.59 | 564.59 | OK |
| 4.3 Canal | Online May ventas | 1,203.97 | 1,203.97 | OK |
| 4.3 Canal | Online Jun ventas | 912.85 | 912.85 | OK |
| 4.3 Canal | Online Jul ventas | 1,091.43 | 1,091.43 | OK |
| 4.3 Canal | Online Ago ventas | 984.71 | 984.71 | OK |
| 4.3 Canal | Online Sep ventas | 1,338.50 | 1,338.50 | OK |
| 4.3 Canal | Online Oct ventas | 1,540.91 | 1,540.91 | OK |
| 4.3 Canal | Online Nov ventas | 1,529.92 | 1,529.92 | OK |
| 4.3 Canal | Online Dic ventas | 2,604.95 | 2,604.95 | OK |
| 4.3 Canal | Amazonía / Online variación S1→S2 % | 420.89 | 420.89 | OK |
| 4.3 Canal | Amazonía / Tienda física variación S1→S2 % | 19.99 | 19.99 | OK |
| 4.3 Canal | Amazonía / Mayorista variación S1→S2 % | -14.84 | -14.84 | OK |
| 4.3 Canal | Costa / Online variación S1→S2 % | 97.73 | 97.73 | OK |
| 4.3 Canal | Costa / Tienda física variación S1→S2 % | -25.26 | -25.26 | OK |
| 4.3 Canal | Costa / Mayorista variación S1→S2 % | 14.52 | 14.52 | OK |
| 4.3 Canal | Insular / Online variación S1→S2 % | 278.79 | 278.79 | OK |
| 4.3 Canal | Insular / Tienda física variación S1→S2 % | -21.89 | -21.89 | OK |
| 4.3 Canal | Insular / Mayorista variación S1→S2 % | 110.95 | 110.95 | OK |
| 4.3 Canal | Sierra / Online variación S1→S2 % | 157.86 | 157.86 | OK |
| 4.3 Canal | Sierra / Tienda física variación S1→S2 % | -29.15 | -29.15 | OK |
| 4.3 Canal | Sierra / Mayorista variación S1→S2 % | 14.38 | 14.38 | OK |
| 4.3 Canal | Tienda física descuento medio ponderado % | 2.75 | 2.75 | OK |
| 4.3 Canal | Mayorista descuento medio ponderado % | 16.21 | 16.21 | OK |
| 4.3 Canal | Online descuento medio ponderado % | 6.77 | 6.77 | OK |
| 4.4 Categoría | Limpieza ventas | 17,668.24 | 17,668.24 | OK |
| 4.4 Categoría | Limpieza margen USD | 5,735.04 | 5,735.04 | OK |
| 4.4 Categoría | Limpieza margen % | 32.46 | 32.46 | OK |
| 4.4 Categoría | Limpieza participación % | 22.16 | 22.16 | OK |
| 4.4 Categoría | Limpieza pedidos | 591 | 591 | OK |
| 4.4 Categoría | Bebidas ventas | 17,580.88 | 17,580.88 | OK |
| 4.4 Categoría | Bebidas margen USD | 5,963.28 | 5,963.28 | OK |
| 4.4 Categoría | Bebidas margen % | 33.92 | 33.92 | OK |
| 4.4 Categoría | Bebidas participación % | 22.05 | 22.05 | OK |
| 4.4 Categoría | Bebidas pedidos | 755 | 755 | OK |
| 4.4 Categoría | Hogar ventas | 17,448.46 | 17,448.46 | OK |
| 4.4 Categoría | Hogar margen USD | 5,498.46 | 5,498.46 | OK |
| 4.4 Categoría | Hogar margen % | 31.51 | 31.51 | OK |
| 4.4 Categoría | Hogar participación % | 21.89 | 21.89 | OK |
| 4.4 Categoría | Hogar pedidos | 226 | 226 | OK |
| 4.4 Categoría | Cuidado personal ventas | 15,843.67 | 15,843.67 | OK |
| 4.4 Categoría | Cuidado personal margen USD | 5,995.27 | 5,995.27 | OK |
| 4.4 Categoría | Cuidado personal margen % | 37.84 | 37.84 | OK |
| 4.4 Categoría | Cuidado personal participación % | 19.87 | 19.87 | OK |
| 4.4 Categoría | Cuidado personal pedidos | 634 | 634 | OK |
| 4.4 Categoría | Snacks ventas | 11,176.32 | 11,176.32 | OK |
| 4.4 Categoría | Snacks margen USD | 4,522.52 | 4,522.52 | OK |
| 4.4 Categoría | Snacks margen % | 40.47 | 40.47 | OK |
| 4.4 Categoría | Snacks participación % | 14.02 | 14.02 | OK |
| 4.4 Categoría | Snacks pedidos | 756 | 756 | OK |
| 4.4 Categoría | Hogar S1 | 7,247.60 | 7,247.60 | OK |
| 4.4 Categoría | Hogar S2 | 10,200.87 | 10,200.87 | OK |
| 4.4 Categoría | Hogar variación S1→S2 % | 40.75 | 40.75 | OK |
| 4.4 Categoría | Snacks S1 | 4,958.61 | 4,958.61 | OK |
| 4.4 Categoría | Snacks S2 | 6,217.70 | 6,217.70 | OK |
| 4.4 Categoría | Snacks variación S1→S2 % | 25.39 | 25.39 | OK |
| 4.4 Categoría | Bebidas S1 | 9,028.08 | 9,028.08 | OK |
| 4.4 Categoría | Bebidas S2 | 8,552.80 | 8,552.80 | OK |
| 4.4 Categoría | Bebidas variación S1→S2 % | -5.26 | -5.26 | OK |
| 4.4 Categoría | Limpieza S1 | 9,074.70 | 9,074.70 | OK |
| 4.4 Categoría | Limpieza S2 | 8,593.54 | 8,593.54 | OK |
| 4.4 Categoría | Limpieza variación S1→S2 % | -5.30 | -5.30 | OK |
| 4.4 Categoría | Cuidado personal S1 | 8,192.88 | 8,192.88 | OK |
| 4.4 Categoría | Cuidado personal S2 | 7,650.79 | 7,650.79 | OK |
| 4.4 Categoría | Cuidado personal variación S1→S2 % | -6.62 | -6.62 | OK |
| 4.5 Producto | Nº de productos | 15 | 15 | OK |
| 4.5 Producto | Top producto por ventas | Detergente 2kg | Detergente 2kg | OK |
| 4.5 Producto | Top 5 (orden) | Detergente 2kg, Agua mineral 6x1L, Shampoo 400ml, Set de ollas, Juego de toallas | Detergente 2kg, Agua mineral 6x1L, Shampoo 400ml, Set de ollas, Juego de toallas | OK |
| 4.5 Producto | Bottom 5 (de menor a mayor) | Cloro 1L, Chocolate 100g, Galletas integrales, Crema dental 150g, Desinfectante multiuso | Cloro 1L, Chocolate 100g, Galletas integrales, Crema dental 150g, Desinfectante multiuso | OK |
| 4.5 Producto | Detergente 2kg ventas | 11,605.11 | 11,605.11 | OK |
| 4.5 Producto | Detergente 2kg margen % | 30.19 | 30.19 | OK |
| 4.5 Producto | Detergente 2kg participación % | 14.56 | 14.56 | OK |
| 4.5 Producto | Agua mineral 6x1L ventas | 8,402.94 | 8,402.94 | OK |
| 4.5 Producto | Agua mineral 6x1L margen % | 33.25 | 33.25 | OK |
| 4.5 Producto | Agua mineral 6x1L participación % | 10.54 | 10.54 | OK |
| 4.5 Producto | Shampoo 400ml ventas | 7,856.46 | 7,856.46 | OK |
| 4.5 Producto | Shampoo 400ml margen % | 37.38 | 37.38 | OK |
| 4.5 Producto | Shampoo 400ml participación % | 9.86 | 9.86 | OK |
| 4.5 Producto | Set de ollas ventas | 7,654.05 | 7,654.05 | OK |
| 4.5 Producto | Set de ollas margen % | 28.04 | 28.04 | OK |
| 4.5 Producto | Set de ollas participación % | 9.60 | 9.60 | OK |
| 4.5 Producto | Juego de toallas ventas | 5,174.24 | 5,174.24 | OK |
| 4.5 Producto | Juego de toallas margen % | 35.87 | 35.87 | OK |
| 4.5 Producto | Juego de toallas participación % | 6.49 | 6.49 | OK |
| 4.5 Producto | Cloro 1L ventas | 2,360.92 | 2,360.92 | OK |
| 4.5 Producto | Cloro 1L margen % | 37.82 | 37.82 | OK |
| 4.5 Producto | Cloro 1L participación % | 2.96 | 2.96 | OK |
| 4.5 Producto | Chocolate 100g ventas | 3,240.55 | 3,240.55 | OK |
| 4.5 Producto | Chocolate 100g margen % | 39.70 | 39.70 | OK |
| 4.5 Producto | Chocolate 100g participación % | 4.07 | 4.07 | OK |
| 4.5 Producto | Galletas integrales ventas | 3,622.04 | 3,622.04 | OK |
| 4.5 Producto | Galletas integrales margen % | 42.35 | 42.35 | OK |
| 4.5 Producto | Galletas integrales participación % | 4.54 | 4.54 | OK |
| 4.5 Producto | Crema dental 150g ventas | 3,675.54 | 3,675.54 | OK |
| 4.5 Producto | Crema dental 150g margen % | 37.96 | 37.96 | OK |
| 4.5 Producto | Crema dental 150g participación % | 4.61 | 4.61 | OK |
| 4.5 Producto | Desinfectante multiuso ventas | 3,702.21 | 3,702.21 | OK |
| 4.5 Producto | Desinfectante multiuso margen % | 36.16 | 36.16 | OK |
| 4.5 Producto | Desinfectante multiuso participación % | 4.64 | 4.64 | OK |
| 4.5 Producto | Producto con menor margen % | Set de ollas | Set de ollas | OK |
| 4.5 Producto | Vajilla 12 piezas S1 | 1,826.29 | 1,826.29 | OK |
| 4.5 Producto | Vajilla 12 piezas S2 | 2,793.88 | 2,793.88 | OK |
| 4.5 Producto | Vajilla 12 piezas variación S1→S2 % | 52.98 | 52.98 | OK |
| 4.5 Producto | Chocolate 100g S1 | 1,311.03 | 1,311.03 | OK |
| 4.5 Producto | Chocolate 100g S2 | 1,929.52 | 1,929.52 | OK |
| 4.5 Producto | Chocolate 100g variación S1→S2 % | 47.18 | 47.18 | OK |
| 4.5 Producto | Juego de toallas S1 | 2,135.98 | 2,135.98 | OK |
| 4.5 Producto | Juego de toallas S2 | 3,038.27 | 3,038.27 | OK |
| 4.5 Producto | Juego de toallas variación S1→S2 % | 42.24 | 42.24 | OK |
| 4.5 Producto | Agua mineral 6x1L S1 | 3,507.73 | 3,507.73 | OK |
| 4.5 Producto | Agua mineral 6x1L S2 | 4,895.21 | 4,895.21 | OK |
| 4.5 Producto | Agua mineral 6x1L variación S1→S2 % | 39.56 | 39.56 | OK |
| 4.5 Producto | Jugo de naranja 1L S1 | 2,094.95 | 2,094.95 | OK |
| 4.5 Producto | Jugo de naranja 1L S2 | 2,789.75 | 2,789.75 | OK |
| 4.5 Producto | Jugo de naranja 1L variación S1→S2 % | 33.17 | 33.17 | OK |
| 4.5 Producto | Set de ollas S1 | 3,285.33 | 3,285.33 | OK |
| 4.5 Producto | Set de ollas S2 | 4,368.72 | 4,368.72 | OK |
| 4.5 Producto | Set de ollas variación S1→S2 % | 32.98 | 32.98 | OK |
| 4.5 Producto | Crema dental 150g S1 | 1,619.54 | 1,619.55 | OK |
| 4.5 Producto | Crema dental 150g S2 | 2,055.99 | 2,055.99 | OK |
| 4.5 Producto | Crema dental 150g variación S1→S2 % | 26.95 | 26.95 | OK |
| 4.5 Producto | Papas fritas 200g S1 | 1,948.26 | 1,948.26 | OK |
| 4.5 Producto | Papas fritas 200g S2 | 2,365.46 | 2,365.46 | OK |
| 4.5 Producto | Papas fritas 200g variación S1→S2 % | 21.41 | 21.41 | OK |
| 4.5 Producto | Galletas integrales S1 | 1,699.32 | 1,699.32 | OK |
| 4.5 Producto | Galletas integrales S2 | 1,922.72 | 1,922.72 | OK |
| 4.5 Producto | Galletas integrales variación S1→S2 % | 13.15 | 13.15 | OK |
| 4.5 Producto | Desinfectante multiuso S1 | 1,826.65 | 1,826.65 | OK |
| 4.5 Producto | Desinfectante multiuso S2 | 1,875.56 | 1,875.56 | OK |
| 4.5 Producto | Desinfectante multiuso variación S1→S2 % | 2.68 | 2.68 | OK |
| 4.5 Producto | Cloro 1L S1 | 1,213.78 | 1,213.78 | OK |
| 4.5 Producto | Cloro 1L S2 | 1,147.14 | 1,147.14 | OK |
| 4.5 Producto | Cloro 1L variación S1→S2 % | -5.49 | -5.49 | OK |
| 4.5 Producto | Detergente 2kg S1 | 6,034.27 | 6,034.27 | OK |
| 4.5 Producto | Detergente 2kg S2 | 5,570.84 | 5,570.84 | OK |
| 4.5 Producto | Detergente 2kg variación S1→S2 % | -7.68 | -7.68 | OK |
| 4.5 Producto | Shampoo 400ml S1 | 4,235.29 | 4,235.29 | OK |
| 4.5 Producto | Shampoo 400ml S2 | 3,621.17 | 3,621.17 | OK |
| 4.5 Producto | Shampoo 400ml variación S1→S2 % | -14.50 | -14.50 | OK |
| 4.5 Producto | Jabón de tocador x3 S1 | 2,338.04 | 2,338.04 | OK |
| 4.5 Producto | Jabón de tocador x3 S2 | 1,973.63 | 1,973.63 | OK |
| 4.5 Producto | Jabón de tocador x3 variación S1→S2 % | -15.59 | -15.59 | OK |
| 4.5 Producto | Gaseosa cola 3L S1 | 3,425.40 | 3,425.40 | OK |
| 4.5 Producto | Gaseosa cola 3L S2 | 867.84 | 867.84 | OK |
| 4.5 Producto | Gaseosa cola 3L variación S1→S2 % | -74.66 | -74.66 | OK |
| 4.5 Producto | Producto que más cae S2 vs S1 | Gaseosa cola 3L | Gaseosa cola 3L | OK |
| 4.5 Producto | Gaseosa Ene ventas | 584.01 | 584.01 | OK |
| 4.5 Producto | Gaseosa Feb ventas | 434.28 | 434.28 | OK |
| 4.5 Producto | Gaseosa Mar ventas | 530.13 | 530.13 | OK |
| 4.5 Producto | Gaseosa Abr ventas | 399.05 | 399.05 | OK |
| 4.5 Producto | Gaseosa May ventas | 655.19 | 655.19 | OK |
| 4.5 Producto | Gaseosa Jun ventas | 822.74 | 822.74 | OK |
| 4.5 Producto | Gaseosa Jul ventas | 96.57 | 96.57 | OK |
| 4.5 Producto | Gaseosa Ago ventas | 122.46 | 122.46 | OK |
| 4.5 Producto | Gaseosa Sep ventas | 190.98 | 190.98 | OK |
| 4.5 Producto | Gaseosa Oct ventas | 77.99 | 77.99 | OK |
| 4.5 Producto | Gaseosa Nov ventas | 57.89 | 57.89 | OK |
| 4.5 Producto | Gaseosa Dic ventas | 321.95 | 321.95 | OK |
| 4.5 Producto | Gaseosa Ene líneas | 26 | 26 | OK |
| 4.5 Producto | Gaseosa Feb líneas | 15 | 15 | OK |
| 4.5 Producto | Gaseosa Mar líneas | 21 | 21 | OK |
| 4.5 Producto | Gaseosa Abr líneas | 19 | 19 | OK |
| 4.5 Producto | Gaseosa May líneas | 28 | 28 | OK |
| 4.5 Producto | Gaseosa Jun líneas | 28 | 28 | OK |
| 4.5 Producto | Gaseosa Jul líneas | 9 | 9 | OK |
| 4.5 Producto | Gaseosa Ago líneas | 8 | 8 | OK |
| 4.5 Producto | Gaseosa Sep líneas | 5 | 5 | OK |
| 4.5 Producto | Gaseosa Oct líneas | 4 | 4 | OK |
| 4.5 Producto | Gaseosa Nov líneas | 4 | 4 | OK |
| 4.5 Producto | Gaseosa Dic líneas | 14 | 14 | OK |
| 4.5 Producto | Gaseosa Online variación % | -4.51 | -4.51 | OK |
| 4.5 Producto | Gaseosa Tienda física variación % | -79.08 | -79.08 | OK |
| 4.5 Producto | Gaseosa Mayorista variación % | -81.62 | -81.62 | OK |
| 4.5 Producto | Gaseosa Amazonía variación % | -20.66 | -20.66 | OK |
| 4.5 Producto | Gaseosa Sierra variación % | -76.30 | -76.30 | OK |
| 4.5 Producto | Gaseosa Costa variación % | -77.71 | -77.71 | OK |
| 4.5 Producto | Gaseosa Insular variación % | -100.00 | -100.00 | OK |
| 5. RFM | Clientes con puntaje R=1 | 76 | 76 | OK |
| 5. RFM | Clientes con puntaje R=2 | 78 | 78 | OK |
| 5. RFM | Clientes con puntaje R=3 | 78 | 78 | OK |
| 5. RFM | Clientes con puntaje R=4 | 72 | 72 | OK |
| 5. RFM | Clientes con puntaje R=5 | 76 | 76 | OK |
| 5. RFM | Clientes con puntaje F=1 | 86 | 86 | OK |
| 5. RFM | Clientes con puntaje F=2 | 99 | 99 | OK |
| 5. RFM | Clientes con puntaje F=3 | 50 | 50 | OK |
| 5. RFM | Clientes con puntaje F=4 | 83 | 83 | OK |
| 5. RFM | Clientes con puntaje F=5 | 62 | 62 | OK |
| 5. RFM | Clientes con puntaje M=1 | 76 | 76 | OK |
| 5. RFM | Clientes con puntaje M=2 | 76 | 76 | OK |
| 5. RFM | Clientes con puntaje M=3 | 76 | 76 | OK |
| 5. RFM | Clientes con puntaje M=4 | 76 | 76 | OK |
| 5. RFM | Clientes con puntaje M=5 | 76 | 76 | OK |
| 5. RFM | Campeones clientes | 87 | 87 | OK |
| 5. RFM | Campeones ventas | 47,893.56 | 47,893.56 | OK |
| 5. RFM | Campeones % ventas | 60.08 | 60.08 | OK |
| 5. RFM | Campeones recencia media | 9.60 | 9.60 | OK |
| 5. RFM | Campeones frecuencia media | 20.85 | 20.85 | OK |
| 5. RFM | Leales clientes | 62 | 62 | OK |
| 5. RFM | Leales ventas | 10,265.53 | 10,265.53 | OK |
| 5. RFM | Leales % ventas | 12.88 | 12.88 | OK |
| 5. RFM | Leales recencia media | 32.26 | 32.26 | OK |
| 5. RFM | Leales frecuencia media | 6.21 | 6.21 | OK |
| 5. RFM | Potenciales clientes | 77 | 77 | OK |
| 5. RFM | Potenciales ventas | 6,547.32 | 6,547.32 | OK |
| 5. RFM | Potenciales % ventas | 8.21 | 8.21 | OK |
| 5. RFM | Potenciales recencia media | 24.09 | 24.09 | OK |
| 5. RFM | Potenciales frecuencia media | 3.14 | 3.14 | OK |
| 5. RFM | En riesgo clientes | 89 | 89 | OK |
| 5. RFM | En riesgo ventas | 11,689.87 | 11,689.87 | OK |
| 5. RFM | En riesgo % ventas | 14.66 | 14.66 | OK |
| 5. RFM | En riesgo recencia media | 101.28 | 101.28 | OK |
| 5. RFM | En riesgo frecuencia media | 4.38 | 4.38 | OK |
| 5. RFM | Perdidos clientes | 65 | 65 | OK |
| 5. RFM | Perdidos ventas | 3,321.28 | 3,321.28 | OK |
| 5. RFM | Perdidos % ventas | 4.17 | 4.17 | OK |
| 5. RFM | Perdidos recencia media | 236.49 | 236.49 | OK |
| 5. RFM | Perdidos frecuencia media | 2.02 | 2.02 | OK |
| 5. RFM | Suma de segmentos | 380 | 380 | OK |
| 6. Preguntas | Amazonía clientes | 37 | 37 | OK |
| 6. Preguntas | Amazonía Online S1 | 270.54 | 270.54 | OK |
| 6. Preguntas | Amazonía Online S2 | 1,409.20 | 1,409.20 | OK |
| 6. Preguntas | Top 20 en riesgo: monto | 5,819.60 | 5,819.58 | OK |
| 6. Preguntas | En riesgo: % compras en Costa | 54.63 | 54.63 | OK |
| 6. Preguntas | En riesgo: % compras en Tienda física | 46.23 | 46.23 | OK |
| 6. Preguntas | Líneas con descuento > 15 % | 211 | 211 | OK |
| 6. Preguntas | Ventas con descuento > 15 % | 11,402.35 | 11,402.35 | OK |
| 6. Preguntas | Margen % con descuento > 15 % | 23.42 | 23.42 | OK |
| 6. Preguntas | Líneas > 15 % en Mayorista | 151 | 151 | OK |
| 6. Preguntas | Líneas > 15 % en Online | 60 | 60 | OK |
| 6. Preguntas | Escenario A ventas | 80,783.97 | 80,783.97 | OK |
| 6. Preguntas | Escenario A margen USD | 28,780.97 | 28,780.97 | OK |
| 6. Preguntas | Escenario A margen % | 35.63 | 35.63 | OK |
| 6. Preguntas | Escenario A margen adicional | 1,066.40 | 1,066.40 | OK |
| 6. Preguntas | Escenario B ventas | 68,315.22 | 68,315.22 | OK |
| 6. Preguntas | Escenario B margen USD | 25,043.87 | 25,043.87 | OK |
| 6. Preguntas | Escenario B margen % | 36.66 | 36.66 | OK |
| 6. Preguntas | Escenario B caída de margen USD | 2,670.70 | 2,670.70 | OK |

## Detalle – dashboard (`docs/index.html`)

| Cifra | Valor en dashboard | Valor recalculado | Estado |
|---|---|---|---|
| [Todas] ventas_netas | 79,717.57 | 79,717.57 | OK |
| [Todas] costo_total | 52,003.00 | 52,003.00 | OK |
| [Todas] margen_bruto | 27,714.57 | 27,714.57 | OK |
| [Todas] margen_pct | 34.77 | 34.77 | OK |
| [Todas] pedidos | 2962 | 2962 | OK |
| [Todas] ticket_promedio | 26.91 | 26.91 | OK |
| [Todas] clientes_activos | 380 | 380 | OK |
| [Todas] unidades | 24236 | 24236 | OK |
| [Todas] Ene ventas | 5,977.50 | 5,977.50 | OK |
| [Todas] Ene margen_pct | 34.70 | 34.70 | OK |
| [Todas] Ene pedidos | 207 | 207 | OK |
| [Todas] Feb ventas | 5,117.67 | 5,117.67 | OK |
| [Todas] Feb margen_pct | 35.16 | 35.16 | OK |
| [Todas] Feb pedidos | 185 | 185 | OK |
| [Todas] Feb crecimiento_pct | -14.38 | -14.38 | OK |
| [Todas] Mar ventas | 6,312.51 | 6,312.51 | OK |
| [Todas] Mar margen_pct | 34.72 | 34.72 | OK |
| [Todas] Mar pedidos | 209 | 209 | OK |
| [Todas] Mar crecimiento_pct | 23.35 | 23.35 | OK |
| [Todas] Abr ventas | 5,572.76 | 5,572.76 | OK |
| [Todas] Abr margen_pct | 35.69 | 35.69 | OK |
| [Todas] Abr pedidos | 204 | 204 | OK |
| [Todas] Abr crecimiento_pct | -11.72 | -11.72 | OK |
| [Todas] May ventas | 9,371.87 | 9,371.87 | OK |
| [Todas] May margen_pct | 35.44 | 35.44 | OK |
| [Todas] May pedidos | 324 | 324 | OK |
| [Todas] May crecimiento_pct | 68.17 | 68.17 | OK |
| [Todas] Jun ventas | 6,149.56 | 6,149.56 | OK |
| [Todas] Jun margen_pct | 34.83 | 34.83 | OK |
| [Todas] Jun pedidos | 233 | 233 | OK |
| [Todas] Jun crecimiento_pct | -34.38 | -34.38 | OK |
| [Todas] Jul ventas | 6,038.12 | 6,038.12 | OK |
| [Todas] Jul margen_pct | 34.16 | 34.16 | OK |
| [Todas] Jul pedidos | 232 | 232 | OK |
| [Todas] Jul crecimiento_pct | -1.81 | -1.81 | OK |
| [Todas] Ago ventas | 6,056.22 | 6,056.22 | OK |
| [Todas] Ago margen_pct | 35.44 | 35.44 | OK |
| [Todas] Ago pedidos | 231 | 231 | OK |
| [Todas] Ago crecimiento_pct | 0.30 | 0.30 | OK |
| [Todas] Sep ventas | 6,559.76 | 6,559.76 | OK |
| [Todas] Sep margen_pct | 34.02 | 34.02 | OK |
| [Todas] Sep pedidos | 233 | 233 | OK |
| [Todas] Sep crecimiento_pct | 8.31 | 8.31 | OK |
| [Todas] Oct ventas | 6,274.72 | 6,274.72 | OK |
| [Todas] Oct margen_pct | 34.40 | 34.40 | OK |
| [Todas] Oct pedidos | 244 | 244 | OK |
| [Todas] Oct crecimiento_pct | -4.35 | -4.35 | OK |
| [Todas] Nov ventas | 6,253.38 | 6,253.38 | OK |
| [Todas] Nov margen_pct | 34.11 | 34.11 | OK |
| [Todas] Nov pedidos | 267 | 267 | OK |
| [Todas] Nov crecimiento_pct | -0.34 | -0.34 | OK |
| [Todas] Dic ventas | 10,033.50 | 10,033.50 | OK |
| [Todas] Dic margen_pct | 34.54 | 34.54 | OK |
| [Todas] Dic pedidos | 393 | 393 | OK |
| [Todas] Dic crecimiento_pct | 60.45 | 60.45 | OK |
| [Todas] canal/Tienda física ventas | 36,563.56 | 36,563.56 | OK |
| [Todas] canal/Tienda física margen | 14,230.71 | 14,230.71 | OK |
| [Todas] canal/Tienda física margen_pct | 38.92 | 38.92 | OK |
| [Todas] canal/Tienda física participacion_pct | 45.87 | 45.87 | OK |
| [Todas] canal/Tienda física pedidos | 1664 | 1664 | OK |
| [Todas] canal/Tienda física unidades | 10393 | 10393 | OK |
| [Todas] canal/Mayorista ventas | 30,458.40 | 30,458.40 | OK |
| [Todas] canal/Mayorista margen | 8,898.70 | 8,898.70 | OK |
| [Todas] canal/Mayorista margen_pct | 29.22 | 29.22 | OK |
| [Todas] canal/Mayorista participacion_pct | 38.21 | 38.21 | OK |
| [Todas] canal/Mayorista pedidos | 437 | 437 | OK |
| [Todas] canal/Mayorista unidades | 10271 | 10271 | OK |
| [Todas] canal/Online ventas | 12,695.61 | 12,695.61 | OK |
| [Todas] canal/Online margen | 4,585.16 | 4,585.16 | OK |
| [Todas] canal/Online margen_pct | 36.12 | 36.12 | OK |
| [Todas] canal/Online participacion_pct | 15.93 | 15.93 | OK |
| [Todas] canal/Online pedidos | 861 | 861 | OK |
| [Todas] canal/Online unidades | 3572 | 3572 | OK |
| [Todas] categoria/Limpieza ventas | 17,668.24 | 17,668.24 | OK |
| [Todas] categoria/Limpieza margen | 5,735.04 | 5,735.04 | OK |
| [Todas] categoria/Limpieza margen_pct | 32.46 | 32.46 | OK |
| [Todas] categoria/Limpieza participacion_pct | 22.16 | 22.16 | OK |
| [Todas] categoria/Limpieza pedidos | 591 | 591 | OK |
| [Todas] categoria/Limpieza unidades | 5055 | 5055 | OK |
| [Todas] categoria/Bebidas ventas | 17,580.88 | 17,580.88 | OK |
| [Todas] categoria/Bebidas margen | 5,963.28 | 5,963.28 | OK |
| [Todas] categoria/Bebidas margen_pct | 33.92 | 33.92 | OK |
| [Todas] categoria/Bebidas participacion_pct | 22.05 | 22.05 | OK |
| [Todas] categoria/Bebidas pedidos | 755 | 755 | OK |
| [Todas] categoria/Bebidas unidades | 6772 | 6772 | OK |
| [Todas] categoria/Hogar ventas | 17,448.46 | 17,448.46 | OK |
| [Todas] categoria/Hogar margen | 5,498.46 | 5,498.46 | OK |
| [Todas] categoria/Hogar margen_pct | 31.51 | 31.51 | OK |
| [Todas] categoria/Hogar participacion_pct | 21.89 | 21.89 | OK |
| [Todas] categoria/Hogar pedidos | 226 | 226 | OK |
| [Todas] categoria/Hogar unidades | 611 | 611 | OK |
| [Todas] categoria/Cuidado personal ventas | 15,843.67 | 15,843.67 | OK |
| [Todas] categoria/Cuidado personal margen | 5,995.27 | 5,995.27 | OK |
| [Todas] categoria/Cuidado personal margen_pct | 37.84 | 37.84 | OK |
| [Todas] categoria/Cuidado personal participacion_pct | 19.87 | 19.87 | OK |
| [Todas] categoria/Cuidado personal pedidos | 634 | 634 | OK |
| [Todas] categoria/Cuidado personal unidades | 5468 | 5468 | OK |
| [Todas] categoria/Snacks ventas | 11,176.32 | 11,176.32 | OK |
| [Todas] categoria/Snacks margen | 4,522.52 | 4,522.52 | OK |
| [Todas] categoria/Snacks margen_pct | 40.47 | 40.47 | OK |
| [Todas] categoria/Snacks participacion_pct | 14.02 | 14.02 | OK |
| [Todas] categoria/Snacks pedidos | 756 | 756 | OK |
| [Todas] categoria/Snacks unidades | 6330 | 6330 | OK |
| [Todas] top_productos/Detergente 2kg ventas | 11,605.11 | 11,605.11 | OK |
| [Todas] top_productos/Detergente 2kg margen | 3,503.51 | 3,503.51 | OK |
| [Todas] top_productos/Detergente 2kg margen_pct | 30.19 | 30.19 | OK |
| [Todas] top_productos/Detergente 2kg participacion_pct | 14.56 | 14.56 | OK |
| [Todas] top_productos/Detergente 2kg pedidos | 219 | 219 | OK |
| [Todas] top_productos/Detergente 2kg unidades | 1976 | 1976 | OK |
| [Todas] top_productos/Agua mineral 6x1L ventas | 8,402.94 | 8,402.94 | OK |
| [Todas] top_productos/Agua mineral 6x1L margen | 2,793.84 | 2,793.84 | OK |
| [Todas] top_productos/Agua mineral 6x1L margen_pct | 33.25 | 33.25 | OK |
| [Todas] top_productos/Agua mineral 6x1L participacion_pct | 10.54 | 10.54 | OK |
| [Todas] top_productos/Agua mineral 6x1L pedidos | 285 | 285 | OK |
| [Todas] top_productos/Agua mineral 6x1L unidades | 2671 | 2671 | OK |
| [Todas] top_productos/Shampoo 400ml ventas | 7,856.46 | 7,856.46 | OK |
| [Todas] top_productos/Shampoo 400ml margen | 2,937.06 | 2,937.06 | OK |
| [Todas] top_productos/Shampoo 400ml margen_pct | 37.38 | 37.38 | OK |
| [Todas] top_productos/Shampoo 400ml participacion_pct | 9.86 | 9.86 | OK |
| [Todas] top_productos/Shampoo 400ml pedidos | 187 | 187 | OK |
| [Todas] top_productos/Shampoo 400ml unidades | 1822 | 1822 | OK |
| [Todas] top_productos/Set de ollas ventas | 7,654.05 | 7,654.05 | OK |
| [Todas] top_productos/Set de ollas margen | 2,146.05 | 2,146.05 | OK |
| [Todas] top_productos/Set de ollas margen_pct | 28.04 | 28.04 | OK |
| [Todas] top_productos/Set de ollas participacion_pct | 9.60 | 9.60 | OK |
| [Todas] top_productos/Set de ollas pedidos | 58 | 58 | OK |
| [Todas] top_productos/Set de ollas unidades | 153 | 153 | OK |
| [Todas] top_productos/Juego de toallas ventas | 5,174.24 | 5,174.24 | OK |
| [Todas] top_productos/Juego de toallas margen | 1,856.24 | 1,856.24 | OK |
| [Todas] top_productos/Juego de toallas margen_pct | 35.87 | 35.87 | OK |
| [Todas] top_productos/Juego de toallas participacion_pct | 6.49 | 6.49 | OK |
| [Todas] top_productos/Juego de toallas pedidos | 111 | 111 | OK |
| [Todas] top_productos/Juego de toallas unidades | 316 | 316 | OK |
| [Todas] top 5 productos (orden) | Detergente 2kg, Agua mineral 6x1L, Shampoo 400ml, Set de ollas, Juego de toallas | Detergente 2kg, Agua mineral 6x1L, Shampoo 400ml, Set de ollas, Juego de toallas | OK |
| [Todas] rfm Campeones | 87 | 87 | OK |
| [Todas] rfm Leales | 62 | 62 | OK |
| [Todas] rfm Potenciales | 77 | 77 | OK |
| [Todas] rfm En riesgo | 89 | 89 | OK |
| [Todas] rfm Perdidos | 65 | 65 | OK |
| [Costa] ventas_netas | 37,394.03 | 37,394.03 | OK |
| [Costa] costo_total | 24,412.90 | 24,412.90 | OK |
| [Costa] margen_bruto | 12,981.12 | 12,981.12 | OK |
| [Costa] margen_pct | 34.71 | 34.71 | OK |
| [Costa] pedidos | 1379 | 1379 | OK |
| [Costa] ticket_promedio | 27.12 | 27.12 | OK |
| [Costa] clientes_activos | 165 | 165 | OK |
| [Costa] unidades | 11477 | 11477 | OK |
| [Costa] Ene ventas | 2,788.19 | 2,788.19 | OK |
| [Costa] Ene margen_pct | 34.84 | 34.84 | OK |
| [Costa] Ene pedidos | 97 | 97 | OK |
| [Costa] Feb ventas | 2,590.94 | 2,590.94 | OK |
| [Costa] Feb margen_pct | 35.91 | 35.91 | OK |
| [Costa] Feb pedidos | 96 | 96 | OK |
| [Costa] Feb crecimiento_pct | -7.07 | -7.07 | OK |
| [Costa] Mar ventas | 2,938.92 | 2,938.92 | OK |
| [Costa] Mar margen_pct | 34.08 | 34.08 | OK |
| [Costa] Mar pedidos | 96 | 96 | OK |
| [Costa] Mar crecimiento_pct | 13.43 | 13.43 | OK |
| [Costa] Abr ventas | 3,022.70 | 3,022.70 | OK |
| [Costa] Abr margen_pct | 35.72 | 35.72 | OK |
| [Costa] Abr pedidos | 104 | 104 | OK |
| [Costa] Abr crecimiento_pct | 2.85 | 2.85 | OK |
| [Costa] May ventas | 3,748.14 | 3,748.14 | OK |
| [Costa] May margen_pct | 36.68 | 36.68 | OK |
| [Costa] May pedidos | 147 | 147 | OK |
| [Costa] May crecimiento_pct | 24.00 | 24.00 | OK |
| [Costa] Jun ventas | 3,522.14 | 3,522.14 | OK |
| [Costa] Jun margen_pct | 34.32 | 34.32 | OK |
| [Costa] Jun pedidos | 119 | 119 | OK |
| [Costa] Jun crecimiento_pct | -6.03 | -6.03 | OK |
| [Costa] Jul ventas | 2,336.69 | 2,336.69 | OK |
| [Costa] Jul margen_pct | 36.05 | 36.05 | OK |
| [Costa] Jul pedidos | 110 | 110 | OK |
| [Costa] Jul crecimiento_pct | -33.66 | -33.66 | OK |
| [Costa] Ago ventas | 2,983.13 | 2,983.13 | OK |
| [Costa] Ago margen_pct | 35.30 | 35.30 | OK |
| [Costa] Ago pedidos | 114 | 114 | OK |
| [Costa] Ago crecimiento_pct | 27.66 | 27.66 | OK |
| [Costa] Sep ventas | 3,277.68 | 3,277.68 | OK |
| [Costa] Sep margen_pct | 34.57 | 34.57 | OK |
| [Costa] Sep pedidos | 117 | 117 | OK |
| [Costa] Sep crecimiento_pct | 9.87 | 9.87 | OK |
| [Costa] Oct ventas | 2,878.35 | 2,878.35 | OK |
| [Costa] Oct margen_pct | 34.68 | 34.68 | OK |
| [Costa] Oct pedidos | 106 | 106 | OK |
| [Costa] Oct crecimiento_pct | -12.18 | -12.18 | OK |
| [Costa] Nov ventas | 2,997.60 | 2,997.60 | OK |
| [Costa] Nov margen_pct | 32.35 | 32.35 | OK |
| [Costa] Nov pedidos | 109 | 109 | OK |
| [Costa] Nov crecimiento_pct | 4.14 | 4.14 | OK |
| [Costa] Dic ventas | 4,309.55 | 4,309.55 | OK |
| [Costa] Dic margen_pct | 32.90 | 32.90 | OK |
| [Costa] Dic pedidos | 164 | 164 | OK |
| [Costa] Dic crecimiento_pct | 43.77 | 43.77 | OK |
| [Costa] canal/Tienda física ventas | 17,319.33 | 17,319.33 | OK |
| [Costa] canal/Tienda física margen | 6,770.08 | 6,770.08 | OK |
| [Costa] canal/Tienda física margen_pct | 39.09 | 39.09 | OK |
| [Costa] canal/Tienda física participacion_pct | 46.32 | 46.32 | OK |
| [Costa] canal/Tienda física pedidos | 801 | 801 | OK |
| [Costa] canal/Tienda física unidades | 4995 | 4995 | OK |
| [Costa] canal/Mayorista ventas | 15,023.20 | 15,023.20 | OK |
| [Costa] canal/Mayorista margen | 4,377.50 | 4,377.50 | OK |
| [Costa] canal/Mayorista margen_pct | 29.14 | 29.14 | OK |
| [Costa] canal/Mayorista participacion_pct | 40.18 | 40.18 | OK |
| [Costa] canal/Mayorista pedidos | 208 | 208 | OK |
| [Costa] canal/Mayorista unidades | 4956 | 4956 | OK |
| [Costa] canal/Online ventas | 5,051.49 | 5,051.49 | OK |
| [Costa] canal/Online margen | 1,833.54 | 1,833.54 | OK |
| [Costa] canal/Online margen_pct | 36.30 | 36.30 | OK |
| [Costa] canal/Online participacion_pct | 13.51 | 13.51 | OK |
| [Costa] canal/Online pedidos | 370 | 370 | OK |
| [Costa] canal/Online unidades | 1526 | 1526 | OK |
| [Costa] categoria/Bebidas ventas | 8,431.59 | 8,431.59 | OK |
| [Costa] categoria/Bebidas margen | 2,841.69 | 2,841.69 | OK |
| [Costa] categoria/Bebidas margen_pct | 33.70 | 33.70 | OK |
| [Costa] categoria/Bebidas participacion_pct | 22.55 | 22.55 | OK |
| [Costa] categoria/Bebidas pedidos | 350 | 350 | OK |
| [Costa] categoria/Bebidas unidades | 3215 | 3215 | OK |
| [Costa] categoria/Limpieza ventas | 8,426.98 | 8,426.98 | OK |
| [Costa] categoria/Limpieza margen | 2,675.68 | 2,675.68 | OK |
| [Costa] categoria/Limpieza margen_pct | 31.75 | 31.75 | OK |
| [Costa] categoria/Limpieza participacion_pct | 22.54 | 22.54 | OK |
| [Costa] categoria/Limpieza pedidos | 268 | 268 | OK |
| [Costa] categoria/Limpieza unidades | 2444 | 2444 | OK |
| [Costa] categoria/Cuidado personal ventas | 8,259.89 | 8,259.89 | OK |
| [Costa] categoria/Cuidado personal margen | 3,144.69 | 3,144.69 | OK |
| [Costa] categoria/Cuidado personal margen_pct | 38.07 | 38.07 | OK |
| [Costa] categoria/Cuidado personal participacion_pct | 22.09 | 22.09 | OK |
| [Costa] categoria/Cuidado personal pedidos | 325 | 325 | OK |
| [Costa] categoria/Cuidado personal unidades | 2794 | 2794 | OK |
| [Costa] categoria/Hogar ventas | 7,385.75 | 7,385.75 | OK |
| [Costa] categoria/Hogar margen | 2,344.25 | 2,344.25 | OK |
| [Costa] categoria/Hogar margen_pct | 31.74 | 31.74 | OK |
| [Costa] categoria/Hogar participacion_pct | 19.75 | 19.75 | OK |
| [Costa] categoria/Hogar pedidos | 97 | 97 | OK |
| [Costa] categoria/Hogar unidades | 260 | 260 | OK |
| [Costa] categoria/Snacks ventas | 4,889.81 | 4,889.81 | OK |
| [Costa] categoria/Snacks margen | 1,974.82 | 1,974.81 | OK |
| [Costa] categoria/Snacks margen_pct | 40.39 | 40.39 | OK |
| [Costa] categoria/Snacks participacion_pct | 13.08 | 13.08 | OK |
| [Costa] categoria/Snacks pedidos | 339 | 339 | OK |
| [Costa] categoria/Snacks unidades | 2764 | 2764 | OK |
| [Costa] top_productos/Detergente 2kg ventas | 5,554.86 | 5,554.86 | OK |
| [Costa] top_productos/Detergente 2kg margen | 1,627.06 | 1,627.06 | OK |
| [Costa] top_productos/Detergente 2kg margen_pct | 29.29 | 29.29 | OK |
| [Costa] top_productos/Detergente 2kg participacion_pct | 14.85 | 14.85 | OK |
| [Costa] top_productos/Detergente 2kg pedidos | 90 | 90 | OK |
| [Costa] top_productos/Detergente 2kg unidades | 958 | 958 | OK |
| [Costa] top_productos/Shampoo 400ml ventas | 4,299.61 | 4,299.61 | OK |
| [Costa] top_productos/Shampoo 400ml margen | 1,623.91 | 1,623.91 | OK |
| [Costa] top_productos/Shampoo 400ml margen_pct | 37.77 | 37.77 | OK |
| [Costa] top_productos/Shampoo 400ml participacion_pct | 11.50 | 11.50 | OK |
| [Costa] top_productos/Shampoo 400ml pedidos | 102 | 102 | OK |
| [Costa] top_productos/Shampoo 400ml unidades | 991 | 991 | OK |
| [Costa] top_productos/Agua mineral 6x1L ventas | 4,271.46 | 4,271.46 | OK |
| [Costa] top_productos/Agua mineral 6x1L margen | 1,413.36 | 1,413.36 | OK |
| [Costa] top_productos/Agua mineral 6x1L margen_pct | 33.09 | 33.09 | OK |
| [Costa] top_productos/Agua mineral 6x1L participacion_pct | 11.42 | 11.42 | OK |
| [Costa] top_productos/Agua mineral 6x1L pedidos | 140 | 140 | OK |
| [Costa] top_productos/Agua mineral 6x1L unidades | 1361 | 1361 | OK |
| [Costa] top_productos/Set de ollas ventas | 3,466.38 | 3,466.38 | OK |
| [Costa] top_productos/Set de ollas margen | 982.38 | 982.38 | OK |
| [Costa] top_productos/Set de ollas margen_pct | 28.34 | 28.34 | OK |
| [Costa] top_productos/Set de ollas participacion_pct | 9.27 | 9.27 | OK |
| [Costa] top_productos/Set de ollas pedidos | 26 | 26 | OK |
| [Costa] top_productos/Set de ollas unidades | 69 | 69 | OK |
| [Costa] top_productos/Juego de toallas ventas | 2,341.06 | 2,341.06 | OK |
| [Costa] top_productos/Juego de toallas margen | 839.56 | 839.56 | OK |
| [Costa] top_productos/Juego de toallas margen_pct | 35.86 | 35.86 | OK |
| [Costa] top_productos/Juego de toallas participacion_pct | 6.26 | 6.26 | OK |
| [Costa] top_productos/Juego de toallas pedidos | 51 | 51 | OK |
| [Costa] top_productos/Juego de toallas unidades | 143 | 143 | OK |
| [Costa] top 5 productos (orden) | Detergente 2kg, Shampoo 400ml, Agua mineral 6x1L, Set de ollas, Juego de toallas | Detergente 2kg, Shampoo 400ml, Agua mineral 6x1L, Set de ollas, Juego de toallas | OK |
| [Costa] rfm Campeones | 41 | 41 | OK |
| [Costa] rfm Leales | 30 | 30 | OK |
| [Costa] rfm Potenciales | 23 | 23 | OK |
| [Costa] rfm En riesgo | 49 | 49 | OK |
| [Costa] rfm Perdidos | 22 | 22 | OK |
| [Sierra] ventas_netas | 31,871.46 | 31,871.46 | OK |
| [Sierra] costo_total | 20,664.10 | 20,664.10 | OK |
| [Sierra] margen_bruto | 11,207.36 | 11,207.36 | OK |
| [Sierra] margen_pct | 35.16 | 35.16 | OK |
| [Sierra] pedidos | 1214 | 1214 | OK |
| [Sierra] ticket_promedio | 26.25 | 26.25 | OK |
| [Sierra] clientes_activos | 155 | 155 | OK |
| [Sierra] unidades | 9679 | 9679 | OK |
| [Sierra] Ene ventas | 2,703.67 | 2,703.67 | OK |
| [Sierra] Ene margen_pct | 34.84 | 34.84 | OK |
| [Sierra] Ene pedidos | 99 | 99 | OK |
| [Sierra] Feb ventas | 1,955.49 | 1,955.49 | OK |
| [Sierra] Feb margen_pct | 35.39 | 35.39 | OK |
| [Sierra] Feb pedidos | 73 | 73 | OK |
| [Sierra] Feb crecimiento_pct | -27.67 | -27.67 | OK |
| [Sierra] Mar ventas | 2,789.53 | 2,789.53 | OK |
| [Sierra] Mar margen_pct | 35.49 | 35.49 | OK |
| [Sierra] Mar pedidos | 96 | 96 | OK |
| [Sierra] Mar crecimiento_pct | 42.65 | 42.65 | OK |
| [Sierra] Abr ventas | 1,960.87 | 1,960.87 | OK |
| [Sierra] Abr margen_pct | 36.18 | 36.18 | OK |
| [Sierra] Abr pedidos | 78 | 78 | OK |
| [Sierra] Abr crecimiento_pct | -29.71 | -29.71 | OK |
| [Sierra] May ventas | 4,511.72 | 4,511.72 | OK |
| [Sierra] May margen_pct | 34.73 | 34.73 | OK |
| [Sierra] May pedidos | 138 | 138 | OK |
| [Sierra] May crecimiento_pct | 130.09 | 130.09 | OK |
| [Sierra] Jun ventas | 1,692.15 | 1,692.15 | OK |
| [Sierra] Jun margen_pct | 35.71 | 35.71 | OK |
| [Sierra] Jun pedidos | 76 | 76 | OK |
| [Sierra] Jun crecimiento_pct | -62.49 | -62.49 | OK |
| [Sierra] Jul ventas | 2,541.06 | 2,541.06 | OK |
| [Sierra] Jul margen_pct | 34.34 | 34.34 | OK |
| [Sierra] Jul pedidos | 95 | 95 | OK |
| [Sierra] Jul crecimiento_pct | 50.17 | 50.17 | OK |
| [Sierra] Ago ventas | 2,270.02 | 2,270.02 | OK |
| [Sierra] Ago margen_pct | 35.77 | 35.77 | OK |
| [Sierra] Ago pedidos | 86 | 86 | OK |
| [Sierra] Ago crecimiento_pct | -10.67 | -10.67 | OK |
| [Sierra] Sep ventas | 2,507.03 | 2,507.03 | OK |
| [Sierra] Sep margen_pct | 33.16 | 33.16 | OK |
| [Sierra] Sep pedidos | 89 | 89 | OK |
| [Sierra] Sep crecimiento_pct | 10.44 | 10.44 | OK |
| [Sierra] Oct ventas | 2,168.93 | 2,168.93 | OK |
| [Sierra] Oct margen_pct | 36.80 | 36.80 | OK |
| [Sierra] Oct pedidos | 98 | 98 | OK |
| [Sierra] Oct crecimiento_pct | -13.49 | -13.49 | OK |
| [Sierra] Nov ventas | 2,485.56 | 2,485.56 | OK |
| [Sierra] Nov margen_pct | 35.13 | 35.13 | OK |
| [Sierra] Nov pedidos | 118 | 118 | OK |
| [Sierra] Nov crecimiento_pct | 14.60 | 14.60 | OK |
| [Sierra] Dic ventas | 4,285.42 | 4,285.42 | OK |
| [Sierra] Dic margen_pct | 35.37 | 35.37 | OK |
| [Sierra] Dic pedidos | 168 | 168 | OK |
| [Sierra] Dic crecimiento_pct | 72.41 | 72.41 | OK |
| [Sierra] canal/Tienda física ventas | 15,028.81 | 15,028.81 | OK |
| [Sierra] canal/Tienda física margen | 5,823.61 | 5,823.61 | OK |
| [Sierra] canal/Tienda física margen_pct | 38.75 | 38.75 | OK |
| [Sierra] canal/Tienda física participacion_pct | 47.15 | 47.15 | OK |
| [Sierra] canal/Tienda física pedidos | 675 | 675 | OK |
| [Sierra] canal/Tienda física unidades | 4197 | 4197 | OK |
| [Sierra] canal/Mayorista ventas | 11,285.03 | 11,285.03 | OK |
| [Sierra] canal/Mayorista margen | 3,378.68 | 3,378.68 | OK |
| [Sierra] canal/Mayorista margen_pct | 29.94 | 29.94 | OK |
| [Sierra] canal/Mayorista participacion_pct | 35.41 | 35.41 | OK |
| [Sierra] canal/Mayorista pedidos | 169 | 169 | OK |
| [Sierra] canal/Mayorista unidades | 3942 | 3942 | OK |
| [Sierra] canal/Online ventas | 5,557.62 | 5,557.62 | OK |
| [Sierra] canal/Online margen | 2,005.07 | 2,005.07 | OK |
| [Sierra] canal/Online margen_pct | 36.08 | 36.08 | OK |
| [Sierra] canal/Online participacion_pct | 17.44 | 17.44 | OK |
| [Sierra] canal/Online pedidos | 370 | 370 | OK |
| [Sierra] canal/Online unidades | 1540 | 1540 | OK |
| [Sierra] categoria/Limpieza ventas | 7,221.21 | 7,221.21 | OK |
| [Sierra] categoria/Limpieza margen | 2,383.31 | 2,383.31 | OK |
| [Sierra] categoria/Limpieza margen_pct | 33.00 | 33.00 | OK |
| [Sierra] categoria/Limpieza participacion_pct | 22.66 | 22.66 | OK |
| [Sierra] categoria/Limpieza pedidos | 253 | 253 | OK |
| [Sierra] categoria/Limpieza unidades | 2053 | 2053 | OK |
| [Sierra] categoria/Hogar ventas | 7,140.50 | 7,140.50 | OK |
| [Sierra] categoria/Hogar margen | 2,323.50 | 2,323.50 | OK |
| [Sierra] categoria/Hogar margen_pct | 32.54 | 32.54 | OK |
| [Sierra] categoria/Hogar participacion_pct | 22.40 | 22.40 | OK |
| [Sierra] categoria/Hogar pedidos | 90 | 90 | OK |
| [Sierra] categoria/Hogar unidades | 241 | 241 | OK |
| [Sierra] categoria/Bebidas ventas | 6,799.57 | 6,799.57 | OK |
| [Sierra] categoria/Bebidas margen | 2,349.17 | 2,349.17 | OK |
| [Sierra] categoria/Bebidas margen_pct | 34.55 | 34.55 | OK |
| [Sierra] categoria/Bebidas participacion_pct | 21.33 | 21.33 | OK |
| [Sierra] categoria/Bebidas pedidos | 304 | 304 | OK |
| [Sierra] categoria/Bebidas unidades | 2592 | 2592 | OK |
| [Sierra] categoria/Cuidado personal ventas | 5,928.12 | 5,928.12 | OK |
| [Sierra] categoria/Cuidado personal margen | 2,224.62 | 2,224.62 | OK |
| [Sierra] categoria/Cuidado personal margen_pct | 37.53 | 37.53 | OK |
| [Sierra] categoria/Cuidado personal participacion_pct | 18.60 | 18.60 | OK |
| [Sierra] categoria/Cuidado personal pedidos | 238 | 238 | OK |
| [Sierra] categoria/Cuidado personal unidades | 2069 | 2069 | OK |
| [Sierra] categoria/Snacks ventas | 4,782.06 | 4,782.06 | OK |
| [Sierra] categoria/Snacks margen | 1,926.76 | 1,926.76 | OK |
| [Sierra] categoria/Snacks margen_pct | 40.29 | 40.29 | OK |
| [Sierra] categoria/Snacks participacion_pct | 15.00 | 15.00 | OK |
| [Sierra] categoria/Snacks pedidos | 329 | 329 | OK |
| [Sierra] categoria/Snacks unidades | 2724 | 2724 | OK |
| [Sierra] top_productos/Detergente 2kg ventas | 4,650.04 | 4,650.04 | OK |
| [Sierra] top_productos/Detergente 2kg margen | 1,423.34 | 1,423.34 | OK |
| [Sierra] top_productos/Detergente 2kg margen_pct | 30.61 | 30.61 | OK |
| [Sierra] top_productos/Detergente 2kg participacion_pct | 14.59 | 14.59 | OK |
| [Sierra] top_productos/Detergente 2kg pedidos | 92 | 92 | OK |
| [Sierra] top_productos/Detergente 2kg unidades | 787 | 787 | OK |
| [Sierra] top_productos/Agua mineral 6x1L ventas | 3,239.61 | 3,239.61 | OK |
| [Sierra] top_productos/Agua mineral 6x1L margen | 1,091.31 | 1,091.31 | OK |
| [Sierra] top_productos/Agua mineral 6x1L margen_pct | 33.69 | 33.69 | OK |
| [Sierra] top_productos/Agua mineral 6x1L participacion_pct | 10.16 | 10.16 | OK |
| [Sierra] top_productos/Agua mineral 6x1L pedidos | 112 | 112 | OK |
| [Sierra] top_productos/Agua mineral 6x1L unidades | 1023 | 1023 | OK |
| [Sierra] top_productos/Set de ollas ventas | 3,042.25 | 3,042.25 | OK |
| [Sierra] top_productos/Set de ollas margen | 918.25 | 918.25 | OK |
| [Sierra] top_productos/Set de ollas margen_pct | 30.18 | 30.18 | OK |
| [Sierra] top_productos/Set de ollas participacion_pct | 9.55 | 9.55 | OK |
| [Sierra] top_productos/Set de ollas pedidos | 23 | 23 | OK |
| [Sierra] top_productos/Set de ollas unidades | 59 | 59 | OK |
| [Sierra] top_productos/Shampoo 400ml ventas | 2,892.38 | 2,892.38 | OK |
| [Sierra] top_productos/Shampoo 400ml margen | 1,064.48 | 1,064.48 | OK |
| [Sierra] top_productos/Shampoo 400ml margen_pct | 36.80 | 36.80 | OK |
| [Sierra] top_productos/Shampoo 400ml participacion_pct | 9.08 | 9.08 | OK |
| [Sierra] top_productos/Shampoo 400ml pedidos | 69 | 69 | OK |
| [Sierra] top_productos/Shampoo 400ml unidades | 677 | 677 | OK |
| [Sierra] top_productos/Vajilla 12 piezas ventas | 2,209.01 | 2,209.01 | OK |
| [Sierra] top_productos/Vajilla 12 piezas margen | 713.01 | 713.01 | OK |
| [Sierra] top_productos/Vajilla 12 piezas margen_pct | 32.28 | 32.28 | OK |
| [Sierra] top_productos/Vajilla 12 piezas participacion_pct | 6.93 | 6.93 | OK |
| [Sierra] top_productos/Vajilla 12 piezas pedidos | 27 | 27 | OK |
| [Sierra] top_productos/Vajilla 12 piezas unidades | 68 | 68 | OK |
| [Sierra] top 5 productos (orden) | Detergente 2kg, Agua mineral 6x1L, Set de ollas, Shampoo 400ml, Vajilla 12 piezas | Detergente 2kg, Agua mineral 6x1L, Set de ollas, Shampoo 400ml, Vajilla 12 piezas | OK |
| [Sierra] rfm Campeones | 37 | 37 | OK |
| [Sierra] rfm Leales | 29 | 29 | OK |
| [Sierra] rfm Potenciales | 32 | 32 | OK |
| [Sierra] rfm En riesgo | 26 | 26 | OK |
| [Sierra] rfm Perdidos | 31 | 31 | OK |
| [Amazonía] ventas_netas | 7,465.31 | 7,465.31 | OK |
| [Amazonía] costo_total | 4,881.35 | 4,881.35 | OK |
| [Amazonía] margen_bruto | 2,583.96 | 2,583.96 | OK |
| [Amazonía] margen_pct | 34.61 | 34.61 | OK |
| [Amazonía] pedidos | 272 | 272 | OK |
| [Amazonía] ticket_promedio | 27.45 | 27.45 | OK |
| [Amazonía] clientes_activos | 37 | 37 | OK |
| [Amazonía] unidades | 2254 | 2254 | OK |
| [Amazonía] Ene ventas | 365.87 | 365.87 | OK |
| [Amazonía] Ene margen_pct | 32.43 | 32.43 | OK |
| [Amazonía] Ene pedidos | 7 | 7 | OK |
| [Amazonía] Feb ventas | 328.22 | 328.22 | OK |
| [Amazonía] Feb margen_pct | 30.08 | 30.08 | OK |
| [Amazonía] Feb pedidos | 6 | 6 | OK |
| [Amazonía] Feb crecimiento_pct | -10.29 | -10.29 | OK |
| [Amazonía] Mar ventas | 527.48 | 527.48 | OK |
| [Amazonía] Mar margen_pct | 33.26 | 33.26 | OK |
| [Amazonía] Mar pedidos | 13 | 13 | OK |
| [Amazonía] Mar crecimiento_pct | 60.71 | 60.71 | OK |
| [Amazonía] Abr ventas | 372.50 | 372.50 | OK |
| [Amazonía] Abr margen_pct | 34.63 | 34.63 | OK |
| [Amazonía] Abr pedidos | 15 | 15 | OK |
| [Amazonía] Abr crecimiento_pct | -29.38 | -29.38 | OK |
| [Amazonía] May ventas | 693.51 | 693.51 | OK |
| [Amazonía] May margen_pct | 34.62 | 34.62 | OK |
| [Amazonía] May pedidos | 27 | 27 | OK |
| [Amazonía] May crecimiento_pct | 86.18 | 86.18 | OK |
| [Amazonía] Jun ventas | 833.40 | 833.40 | OK |
| [Amazonía] Jun margen_pct | 34.86 | 34.86 | OK |
| [Amazonía] Jun pedidos | 31 | 31 | OK |
| [Amazonía] Jun crecimiento_pct | 20.17 | 20.17 | OK |
| [Amazonía] Jul ventas | 807.74 | 807.74 | OK |
| [Amazonía] Jul margen_pct | 28.14 | 28.14 | OK |
| [Amazonía] Jul pedidos | 17 | 17 | OK |
| [Amazonía] Jul crecimiento_pct | -3.08 | -3.08 | OK |
| [Amazonía] Ago ventas | 594.12 | 594.12 | OK |
| [Amazonía] Ago margen_pct | 36.54 | 36.54 | OK |
| [Amazonía] Ago pedidos | 25 | 25 | OK |
| [Amazonía] Ago crecimiento_pct | -26.45 | -26.45 | OK |
| [Amazonía] Sep ventas | 651.78 | 651.78 | OK |
| [Amazonía] Sep margen_pct | 35.44 | 35.44 | OK |
| [Amazonía] Sep pedidos | 21 | 21 | OK |
| [Amazonía] Sep crecimiento_pct | 9.70 | 9.70 | OK |
| [Amazonía] Oct ventas | 661.84 | 661.84 | OK |
| [Amazonía] Oct margen_pct | 36.05 | 36.05 | OK |
| [Amazonía] Oct pedidos | 29 | 29 | OK |
| [Amazonía] Oct crecimiento_pct | 1.54 | 1.54 | OK |
| [Amazonía] Nov ventas | 626.06 | 626.06 | OK |
| [Amazonía] Nov margen_pct | 36.81 | 36.81 | OK |
| [Amazonía] Nov pedidos | 30 | 30 | OK |
| [Amazonía] Nov crecimiento_pct | -5.41 | -5.41 | OK |
| [Amazonía] Dic ventas | 1,002.81 | 1,002.81 | OK |
| [Amazonía] Dic margen_pct | 38.61 | 38.61 | OK |
| [Amazonía] Dic pedidos | 51 | 51 | OK |
| [Amazonía] Dic crecimiento_pct | 60.18 | 60.18 | OK |
| [Amazonía] canal/Tienda física ventas | 3,207.45 | 3,207.45 | OK |
| [Amazonía] canal/Tienda física margen | 1,250.80 | 1,250.80 | OK |
| [Amazonía] canal/Tienda física margen_pct | 39.00 | 39.00 | OK |
| [Amazonía] canal/Tienda física participacion_pct | 42.96 | 42.96 | OK |
| [Amazonía] canal/Tienda física pedidos | 142 | 142 | OK |
| [Amazonía] canal/Tienda física unidades | 919 | 919 | OK |
| [Amazonía] canal/Mayorista ventas | 2,578.12 | 2,578.12 | OK |
| [Amazonía] canal/Mayorista margen | 739.07 | 739.07 | OK |
| [Amazonía] canal/Mayorista margen_pct | 28.67 | 28.67 | OK |
| [Amazonía] canal/Mayorista participacion_pct | 34.53 | 34.53 | OK |
| [Amazonía] canal/Mayorista pedidos | 40 | 40 | OK |
| [Amazonía] canal/Mayorista unidades | 964 | 964 | OK |
| [Amazonía] canal/Online ventas | 1,679.74 | 1,679.74 | OK |
| [Amazonía] canal/Online margen | 594.09 | 594.09 | OK |
| [Amazonía] canal/Online margen_pct | 35.37 | 35.37 | OK |
| [Amazonía] canal/Online participacion_pct | 22.50 | 22.50 | OK |
| [Amazonía] canal/Online pedidos | 90 | 90 | OK |
| [Amazonía] canal/Online unidades | 371 | 371 | OK |
| [Amazonía] categoria/Hogar ventas | 1,807.62 | 1,807.62 | OK |
| [Amazonía] categoria/Hogar margen | 543.12 | 543.12 | OK |
| [Amazonía] categoria/Hogar margen_pct | 30.05 | 30.05 | OK |
| [Amazonía] categoria/Hogar participacion_pct | 24.21 | 24.21 | OK |
| [Amazonía] categoria/Hogar pedidos | 27 | 27 | OK |
| [Amazonía] categoria/Hogar unidades | 61 | 61 | OK |
| [Amazonía] categoria/Limpieza ventas | 1,646.80 | 1,646.80 | OK |
| [Amazonía] categoria/Limpieza margen | 551.00 | 551.00 | OK |
| [Amazonía] categoria/Limpieza margen_pct | 33.46 | 33.46 | OK |
| [Amazonía] categoria/Limpieza participacion_pct | 22.06 | 22.06 | OK |
| [Amazonía] categoria/Limpieza pedidos | 56 | 56 | OK |
| [Amazonía] categoria/Limpieza unidades | 432 | 432 | OK |
| [Amazonía] categoria/Bebidas ventas | 1,627.58 | 1,627.58 | OK |
| [Amazonía] categoria/Bebidas margen | 548.38 | 548.38 | OK |
| [Amazonía] categoria/Bebidas margen_pct | 33.69 | 33.69 | OK |
| [Amazonía] categoria/Bebidas participacion_pct | 21.80 | 21.80 | OK |
| [Amazonía] categoria/Bebidas pedidos | 73 | 73 | OK |
| [Amazonía] categoria/Bebidas unidades | 668 | 668 | OK |
| [Amazonía] categoria/Snacks ventas | 1,196.26 | 1,196.26 | OK |
| [Amazonía] categoria/Snacks margen | 495.91 | 495.91 | OK |
| [Amazonía] categoria/Snacks margen_pct | 41.46 | 41.46 | OK |
| [Amazonía] categoria/Snacks participacion_pct | 16.02 | 16.02 | OK |
| [Amazonía] categoria/Snacks pedidos | 68 | 68 | OK |
| [Amazonía] categoria/Snacks unidades | 667 | 667 | OK |
| [Amazonía] categoria/Cuidado personal ventas | 1,187.05 | 1,187.05 | OK |
| [Amazonía] categoria/Cuidado personal margen | 445.55 | 445.55 | OK |
| [Amazonía] categoria/Cuidado personal margen_pct | 37.53 | 37.53 | OK |
| [Amazonía] categoria/Cuidado personal participacion_pct | 15.90 | 15.90 | OK |
| [Amazonía] categoria/Cuidado personal pedidos | 48 | 48 | OK |
| [Amazonía] categoria/Cuidado personal unidades | 426 | 426 | OK |
| [Amazonía] top_productos/Detergente 2kg ventas | 1,153.26 | 1,153.26 | OK |
| [Amazonía] top_productos/Detergente 2kg margen | 370.16 | 370.16 | OK |
| [Amazonía] top_productos/Detergente 2kg margen_pct | 32.10 | 32.10 | OK |
| [Amazonía] top_productos/Detergente 2kg participacion_pct | 15.45 | 15.45 | OK |
| [Amazonía] top_productos/Detergente 2kg pedidos | 30 | 30 | OK |
| [Amazonía] top_productos/Detergente 2kg unidades | 191 | 191 | OK |
| [Amazonía] top_productos/Set de ollas ventas | 704.32 | 704.32 | OK |
| [Amazonía] top_productos/Set de ollas margen | 164.32 | 164.32 | OK |
| [Amazonía] top_productos/Set de ollas margen_pct | 23.33 | 23.33 | OK |
| [Amazonía] top_productos/Set de ollas participacion_pct | 9.43 | 9.43 | OK |
| [Amazonía] top_productos/Set de ollas pedidos | 7 | 7 | OK |
| [Amazonía] top_productos/Set de ollas unidades | 15 | 15 | OK |
| [Amazonía] top_productos/Vajilla 12 piezas ventas | 675.46 | 675.46 | OK |
| [Amazonía] top_productos/Vajilla 12 piezas margen | 213.46 | 213.46 | OK |
| [Amazonía] top_productos/Vajilla 12 piezas margen_pct | 31.60 | 31.60 | OK |
| [Amazonía] top_productos/Vajilla 12 piezas participacion_pct | 9.05 | 9.05 | OK |
| [Amazonía] top_productos/Vajilla 12 piezas pedidos | 8 | 8 | OK |
| [Amazonía] top_productos/Vajilla 12 piezas unidades | 21 | 21 | OK |
| [Amazonía] top_productos/Jugo de naranja 1L ventas | 653.92 | 653.92 | OK |
| [Amazonía] top_productos/Jugo de naranja 1L margen | 232.72 | 232.72 | OK |
| [Amazonía] top_productos/Jugo de naranja 1L margen_pct | 35.59 | 35.59 | OK |
| [Amazonía] top_productos/Jugo de naranja 1L participacion_pct | 8.76 | 8.76 | OK |
| [Amazonía] top_productos/Jugo de naranja 1L pedidos | 36 | 36 | OK |
| [Amazonía] top_productos/Jugo de naranja 1L unidades | 324 | 324 | OK |
| [Amazonía] top_productos/Agua mineral 6x1L ventas | 583.43 | 583.43 | OK |
| [Amazonía] top_productos/Agua mineral 6x1L margen | 199.13 | 199.13 | OK |
| [Amazonía] top_productos/Agua mineral 6x1L margen_pct | 34.13 | 34.13 | OK |
| [Amazonía] top_productos/Agua mineral 6x1L participacion_pct | 7.82 | 7.82 | OK |
| [Amazonía] top_productos/Agua mineral 6x1L pedidos | 24 | 24 | OK |
| [Amazonía] top_productos/Agua mineral 6x1L unidades | 183 | 183 | OK |
| [Amazonía] top 5 productos (orden) | Detergente 2kg, Set de ollas, Vajilla 12 piezas, Jugo de naranja 1L, Agua mineral 6x1L | Detergente 2kg, Set de ollas, Vajilla 12 piezas, Jugo de naranja 1L, Agua mineral 6x1L | OK |
| [Amazonía] rfm Campeones | 6 | 6 | OK |
| [Amazonía] rfm Leales | 3 | 3 | OK |
| [Amazonía] rfm Potenciales | 16 | 16 | OK |
| [Amazonía] rfm En riesgo | 11 | 11 | OK |
| [Amazonía] rfm Perdidos | 1 | 1 | OK |
| [Insular] ventas_netas | 2,986.78 | 2,986.78 | OK |
| [Insular] costo_total | 2,044.65 | 2,044.65 | OK |
| [Insular] margen_bruto | 942.13 | 942.13 | OK |
| [Insular] margen_pct | 31.54 | 31.54 | OK |
| [Insular] pedidos | 97 | 97 | OK |
| [Insular] ticket_promedio | 30.79 | 30.79 | OK |
| [Insular] clientes_activos | 23 | 23 | OK |
| [Insular] unidades | 826 | 826 | OK |
| [Insular] Ene ventas | 119.78 | 119.78 | OK |
| [Insular] Ene margen_pct | 35.38 | 35.38 | OK |
| [Insular] Ene pedidos | 4 | 4 | OK |
| [Insular] Feb ventas | 243.03 | 243.03 | OK |
| [Insular] Feb margen_pct | 32.13 | 32.13 | OK |
| [Insular] Feb pedidos | 10 | 10 | OK |
| [Insular] Feb crecimiento_pct | 102.90 | 102.90 | OK |
| [Insular] Mar ventas | 56.59 | 56.59 | OK |
| [Insular] Mar margen_pct | 42.92 | 42.92 | OK |
| [Insular] Mar pedidos | 4 | 4 | OK |
| [Insular] Mar crecimiento_pct | -76.72 | -76.72 | OK |
| [Insular] Abr ventas | 216.69 | 216.69 | OK |
| [Insular] Abr margen_pct | 32.69 | 32.69 | OK |
| [Insular] Abr pedidos | 7 | 7 | OK |
| [Insular] Abr crecimiento_pct | 282.94 | 282.94 | OK |
| [Insular] May ventas | 418.50 | 418.50 | OK |
| [Insular] May margen_pct | 33.36 | 33.36 | OK |
| [Insular] May pedidos | 12 | 12 | OK |
| [Insular] May crecimiento_pct | 93.13 | 93.13 | OK |
| [Insular] Jun ventas | 101.87 | 101.87 | OK |
| [Insular] Jun margen_pct | 37.37 | 37.37 | OK |
| [Insular] Jun pedidos | 7 | 7 | OK |
| [Insular] Jun crecimiento_pct | -75.66 | -75.66 | OK |
| [Insular] Jul ventas | 352.64 | 352.64 | OK |
| [Insular] Jul margen_pct | 34.20 | 34.20 | OK |
| [Insular] Jul pedidos | 10 | 10 | OK |
| [Insular] Jul crecimiento_pct | 246.18 | 246.18 | OK |
| [Insular] Ago ventas | 208.95 | 208.95 | OK |
| [Insular] Ago margen_pct | 30.56 | 30.56 | OK |
| [Insular] Ago pedidos | 6 | 6 | OK |
| [Insular] Ago crecimiento_pct | -40.75 | -40.75 | OK |
| [Insular] Sep ventas | 123.26 | 123.26 | OK |
| [Insular] Sep margen_pct | 29.74 | 29.74 | OK |
| [Insular] Sep pedidos | 6 | 6 | OK |
| [Insular] Sep crecimiento_pct | -41.01 | -41.01 | OK |
| [Insular] Oct ventas | 565.59 | 565.59 | OK |
| [Insular] Oct margen_pct | 21.88 | 21.88 | OK |
| [Insular] Oct pedidos | 11 | 11 | OK |
| [Insular] Oct crecimiento_pct | 358.84 | 358.84 | OK |
| [Insular] Nov ventas | 144.16 | 144.16 | OK |
| [Insular] Nov margen_pct | 41.35 | 41.35 | OK |
| [Insular] Nov pedidos | 10 | 10 | OK |
| [Insular] Nov crecimiento_pct | -74.51 | -74.51 | OK |
| [Insular] Dic ventas | 435.72 | 435.72 | OK |
| [Insular] Dic margen_pct | 33.15 | 33.15 | OK |
| [Insular] Dic pedidos | 10 | 10 | OK |
| [Insular] Dic crecimiento_pct | 202.24 | 202.24 | OK |
| [Insular] canal/Mayorista ventas | 1,572.05 | 1,572.05 | OK |
| [Insular] canal/Mayorista margen | 403.45 | 403.45 | OK |
| [Insular] canal/Mayorista margen_pct | 25.66 | 25.66 | OK |
| [Insular] canal/Mayorista participacion_pct | 52.63 | 52.63 | OK |
| [Insular] canal/Mayorista pedidos | 20 | 20 | OK |
| [Insular] canal/Mayorista unidades | 409 | 409 | OK |
| [Insular] canal/Tienda física ventas | 1,007.96 | 1,007.96 | OK |
| [Insular] canal/Tienda física margen | 386.21 | 386.21 | OK |
| [Insular] canal/Tienda física margen_pct | 38.32 | 38.32 | OK |
| [Insular] canal/Tienda física participacion_pct | 33.75 | 33.75 | OK |
| [Insular] canal/Tienda física pedidos | 46 | 46 | OK |
| [Insular] canal/Tienda física unidades | 282 | 282 | OK |
| [Insular] canal/Online ventas | 406.76 | 406.76 | OK |
| [Insular] canal/Online margen | 152.47 | 152.47 | OK |
| [Insular] canal/Online margen_pct | 37.48 | 37.48 | OK |
| [Insular] canal/Online participacion_pct | 13.62 | 13.62 | OK |
| [Insular] canal/Online pedidos | 31 | 31 | OK |
| [Insular] canal/Online unidades | 135 | 135 | OK |
| [Insular] categoria/Hogar ventas | 1,114.59 | 1,114.59 | OK |
| [Insular] categoria/Hogar margen | 287.59 | 287.59 | OK |
| [Insular] categoria/Hogar margen_pct | 25.80 | 25.80 | OK |
| [Insular] categoria/Hogar participacion_pct | 37.32 | 37.32 | OK |
| [Insular] categoria/Hogar pedidos | 12 | 12 | OK |
| [Insular] categoria/Hogar unidades | 49 | 49 | OK |
| [Insular] categoria/Bebidas ventas | 722.14 | 722.14 | OK |
| [Insular] categoria/Bebidas margen | 224.04 | 224.04 | OK |
| [Insular] categoria/Bebidas margen_pct | 31.02 | 31.02 | OK |
| [Insular] categoria/Bebidas participacion_pct | 24.18 | 24.18 | OK |
| [Insular] categoria/Bebidas pedidos | 28 | 28 | OK |
| [Insular] categoria/Bebidas unidades | 297 | 297 | OK |
| [Insular] categoria/Cuidado personal ventas | 468.61 | 468.61 | OK |
| [Insular] categoria/Cuidado personal margen | 180.41 | 180.41 | OK |
| [Insular] categoria/Cuidado personal margen_pct | 38.50 | 38.50 | OK |
| [Insular] categoria/Cuidado personal participacion_pct | 15.69 | 15.69 | OK |
| [Insular] categoria/Cuidado personal pedidos | 23 | 23 | OK |
| [Insular] categoria/Cuidado personal unidades | 179 | 179 | OK |
| [Insular] categoria/Limpieza ventas | 373.26 | 373.26 | OK |
| [Insular] categoria/Limpieza margen | 125.06 | 125.06 | OK |
| [Insular] categoria/Limpieza margen_pct | 33.50 | 33.50 | OK |
| [Insular] categoria/Limpieza participacion_pct | 12.50 | 12.50 | OK |
| [Insular] categoria/Limpieza pedidos | 14 | 14 | OK |
| [Insular] categoria/Limpieza unidades | 126 | 126 | OK |
| [Insular] categoria/Snacks ventas | 308.18 | 308.18 | OK |
| [Insular] categoria/Snacks margen | 125.03 | 125.03 | OK |
| [Insular] categoria/Snacks margen_pct | 40.57 | 40.57 | OK |
| [Insular] categoria/Snacks participacion_pct | 10.32 | 10.32 | OK |
| [Insular] categoria/Snacks pedidos | 20 | 20 | OK |
| [Insular] categoria/Snacks unidades | 175 | 175 | OK |
| [Insular] top_productos/Juego de toallas ventas | 516.11 | 516.11 | OK |
| [Insular] top_productos/Juego de toallas margen | 159.11 | 159.11 | OK |
| [Insular] top_productos/Juego de toallas margen_pct | 30.83 | 30.83 | OK |
| [Insular] top_productos/Juego de toallas participacion_pct | 17.28 | 17.28 | OK |
| [Insular] top_productos/Juego de toallas pedidos | 8 | 8 | OK |
| [Insular] top_productos/Juego de toallas unidades | 34 | 34 | OK |
| [Insular] top_productos/Set de ollas ventas | 441.10 | 441.10 | OK |
| [Insular] top_productos/Set de ollas margen | 81.10 | 81.10 | OK |
| [Insular] top_productos/Set de ollas margen_pct | 18.39 | 18.39 | OK |
| [Insular] top_productos/Set de ollas participacion_pct | 14.77 | 14.77 | OK |
| [Insular] top_productos/Set de ollas pedidos | 2 | 2 | OK |
| [Insular] top_productos/Set de ollas unidades | 10 | 10 | OK |
| [Insular] top_productos/Agua mineral 6x1L ventas | 308.44 | 308.44 | OK |
| [Insular] top_productos/Agua mineral 6x1L margen | 90.04 | 90.04 | OK |
| [Insular] top_productos/Agua mineral 6x1L margen_pct | 29.19 | 29.19 | OK |
| [Insular] top_productos/Agua mineral 6x1L participacion_pct | 10.33 | 10.33 | OK |
| [Insular] top_productos/Agua mineral 6x1L pedidos | 9 | 9 | OK |
| [Insular] top_productos/Agua mineral 6x1L unidades | 104 | 104 | OK |
| [Insular] top_productos/Detergente 2kg ventas | 246.96 | 246.96 | OK |
| [Insular] top_productos/Detergente 2kg margen | 82.96 | 82.96 | OK |
| [Insular] top_productos/Detergente 2kg margen_pct | 33.59 | 33.59 | OK |
| [Insular] top_productos/Detergente 2kg participacion_pct | 8.27 | 8.27 | OK |
| [Insular] top_productos/Detergente 2kg pedidos | 7 | 7 | OK |
| [Insular] top_productos/Detergente 2kg unidades | 40 | 40 | OK |
| [Insular] top_productos/Jugo de naranja 1L ventas | 238.50 | 238.50 | OK |
| [Insular] top_productos/Jugo de naranja 1L margen | 81.20 | 81.20 | OK |
| [Insular] top_productos/Jugo de naranja 1L margen_pct | 34.05 | 34.05 | OK |
| [Insular] top_productos/Jugo de naranja 1L participacion_pct | 7.99 | 7.99 | OK |
| [Insular] top_productos/Jugo de naranja 1L pedidos | 14 | 14 | OK |
| [Insular] top_productos/Jugo de naranja 1L unidades | 121 | 121 | OK |
| [Insular] top 5 productos (orden) | Juego de toallas, Set de ollas, Agua mineral 6x1L, Detergente 2kg, Jugo de naranja 1L | Juego de toallas, Set de ollas, Agua mineral 6x1L, Detergente 2kg, Jugo de naranja 1L | OK |
| [Insular] rfm Campeones | 3 | 3 | OK |
| [Insular] rfm Leales | 0 | 0 | OK |
| [Insular] rfm Potenciales | 6 | 6 | OK |
| [Insular] rfm En riesgo | 3 | 3 | OK |
| [Insular] rfm Perdidos | 11 | 11 | OK |
| segmentos/Campeones clientes | 87 | 87 | OK |
| segmentos/Campeones ventas | 47,893.56 | 47,893.56 | OK |
| segmentos/Campeones participacion_pct | 60.08 | 60.08 | OK |
| segmentos/Campeones recencia_media | 9.60 | 9.60 | OK |
| segmentos/Campeones frecuencia_media | 20.85 | 20.85 | OK |
| segmentos/Leales clientes | 62 | 62 | OK |
| segmentos/Leales ventas | 10,265.53 | 10,265.53 | OK |
| segmentos/Leales participacion_pct | 12.88 | 12.88 | OK |
| segmentos/Leales recencia_media | 32.26 | 32.26 | OK |
| segmentos/Leales frecuencia_media | 6.21 | 6.21 | OK |
| segmentos/Potenciales clientes | 77 | 77 | OK |
| segmentos/Potenciales ventas | 6,547.32 | 6,547.32 | OK |
| segmentos/Potenciales participacion_pct | 8.21 | 8.21 | OK |
| segmentos/Potenciales recencia_media | 24.09 | 24.09 | OK |
| segmentos/Potenciales frecuencia_media | 3.14 | 3.14 | OK |
| segmentos/En riesgo clientes | 89 | 89 | OK |
| segmentos/En riesgo ventas | 11,689.87 | 11,689.87 | OK |
| segmentos/En riesgo participacion_pct | 14.66 | 14.66 | OK |
| segmentos/En riesgo recencia_media | 101.28 | 101.28 | OK |
| segmentos/En riesgo frecuencia_media | 4.38 | 4.38 | OK |
| segmentos/Perdidos clientes | 65 | 65 | OK |
| segmentos/Perdidos ventas | 3,321.28 | 3,321.28 | OK |
| segmentos/Perdidos participacion_pct | 4.17 | 4.17 | OK |
| segmentos/Perdidos recencia_media | 236.49 | 236.49 | OK |
| segmentos/Perdidos frecuencia_media | 2.02 | 2.02 | OK |
| regiones/Costa ventas | 37,394.03 | 37,394.03 | OK |
| regiones/Costa margen_pct | 34.71 | 34.71 | OK |
| regiones/Sierra ventas | 31,871.46 | 31,871.46 | OK |
| regiones/Sierra margen_pct | 35.16 | 35.16 | OK |
| regiones/Amazonía ventas | 7,465.31 | 7,465.31 | OK |
| regiones/Amazonía margen_pct | 34.61 | 34.61 | OK |
| regiones/Insular ventas | 2,986.78 | 2,986.78 | OK |
| regiones/Insular margen_pct | 31.54 | 31.54 | OK |
| calidad/antes | 3000 | 3000 | OK |
| calidad/despues | 2962 | 2962 | OK |
| calidad/duplicados | 15 | 15 | OK |
| calidad/vacías | 20 | 20 | OK |
| calidad/negativas | 3 | 3 | OK |
| resumen[1] idéntico al informe | sí | sí | OK |
| resumen[2] idéntico al informe | sí | sí | OK |
| resumen[3] idéntico al informe | sí | sí | OK |
| resumen[4] idéntico al informe | sí | sí | OK |
| resumen[5] idéntico al informe | sí | sí | OK |
| pregunta 1: respuesta idéntica al informe | sí | sí | OK |
| pregunta 2: respuesta idéntica al informe | sí | sí | OK |
| pregunta 3: respuesta idéntica al informe | sí | sí | OK |
| pregunta 4: respuesta idéntica al informe | sí | sí | OK |
| pregunta 5: respuesta idéntica al informe | sí | sí | OK |
