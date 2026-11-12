---
name: manual-analisis-ventas
description: Manual paso a paso para analizar las ventas de Distribuidora Pacífico (datos/ventas_2025.csv) que cubre calidad de datos, KPIs, análisis por dimensión, segmentación RFM, preguntas de negocio, informe y dashboard HTML. Úsalo para cualquier análisis de ventas, informe, segmentación de clientes o dashboard.
---

# Manual de análisis de ventas

Sigue los pasos en orden. Toda cifra sale de `scripts/analisis.py` (Python, solo librería
estándar). El script debe imprimir los resultados y guardarlos también en un JSON
(`informes/resultados.json`) que alimenta el informe y el dashboard.

## Paso 1 – Calidad de datos
- Cuenta y reporta: filas duplicadas exactas, celdas vacías (por columna), unidades
  negativas o cero, fechas que no cumplen AAAA-MM-DD.
- Crea `datos/ventas_limpias.csv` (nunca toques el original) y explica cada decisión, por
  ejemplo: duplicados → se conserva una copia; vacíos en unidades/precio → se eliminan;
  negativos → se eliminan (o se tratan como devolución, justificándolo); fechas mal escritas
  → se corrigen si el formato es inequívoco.
- Reporta filas antes, filas eliminadas por motivo y filas después.

## Paso 2 – KPIs
- Ventas netas = unidades × precio_unitario × (1 − descuento_pct/100)
- Costo total = unidades × costo_unitario
- Margen bruto USD = ventas netas − costo total; margen % = margen / ventas netas
- Número de pedidos, ticket promedio (ventas netas / pedidos), clientes activos
- Crecimiento mes a mes (%) de las ventas netas

## Paso 3 – Análisis por dimensión
- Por mes, región, canal y categoría: ventas, margen %, participación %.
- Por producto: top 5 y bottom 5 por ventas netas.
- Compara primer y segundo semestre (S1 vs S2) para detectar qué crece y qué cae.

## Paso 4 – Segmentación RFM
- Fecha de referencia: 31-12-2025. Recencia = días desde la última compra; Frecuencia =
  número de pedidos; Monto = ventas netas del cliente.
- Puntajes 1-5 por quintiles (en Recencia, menos días = 5).
- Segmentos (se aplican en este orden; el primero que cumple gana; documenta la regla y
  cómo trataste los empates de quintiles en el informe):
  1. Campeones: R ≥ 4 y F ≥ 4
  2. Leales: R ≥ 3 y F ≥ 3
  3. Potenciales: R ≥ 3 y F ≤ 2
  4. En riesgo: R = 2, o R = 1 y F ≥ 3
  5. Perdidos: R = 1 y F ≤ 2
  Cada cliente cae en exactamente un segmento; comprueba que los tamaños sumen el total.
- Para cada segmento: número de clientes, ventas netas, % de ventas y una acción comercial.

## Paso 5 – Preguntas de negocio (responder con datos)
1. ¿Qué región merece más inversión el próximo año y por qué?
2. ¿Qué producto conviene revisar o descontinuar?
3. ¿Qué canal potenciar?
4. ¿Qué hacer con los clientes en riesgo?
5. ¿Qué pasaría con el margen si se eliminan los descuentos mayores al 15 %?
   (Supuesto a declarar: esas ventas se mantienen con descuento 15 %, o se pierden; calcula
   al menos un escenario y explica el supuesto.)

## Paso 6 – Resumen ejecutivo
Máximo 5 viñetas para un gerente: qué pasó, qué preocupa, qué hacer.

## Paso 7 – Informe `informes/informe_ventas.md`
Orden: 1) Resumen ejecutivo, 2) Calidad de datos (con reglas de limpieza exactas),
3) KPIs, 4) Análisis por dimensión, 5) Segmentación RFM, 6) Preguntas de negocio,
7) Limitaciones. USD con 2 decimales.

## Paso 8 – Dashboard `docs/index.html`
- Un solo archivo HTML en español, diseño limpio y profesional, sin servidor.
- Gráficos con Chart.js desde CDN (versión fija, p. ej.
  `https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js`).
- Datos incrustados en el HTML (generados por script desde `informes/resultados.json`).
- Incluir: tarjetas de KPIs, ventas por mes, por región, por canal, top productos, segmentos
  RFM, resumen ejecutivo, sección "Preguntas al agente" con las respuestas (indicando que
  fueron generadas por el agente) y un filtro por región que actualice gráficos y KPIs.
- Pie de página: "Generado por el Agente Analista de Ventas (Claude Code) – datos ficticios
  con fines académicos".
- Comprueba que el HTML esté bien formado y que el JSON incrustado sea válido.

## Checklist final (responder sí/no a cada punto)
- [ ] ¿Cada cifra salió de un script?
- [ ] ¿Se reportó la calidad de datos?
- [ ] ¿Están respondidas las 5 preguntas de negocio?
- [ ] ¿El resumen ejecutivo tiene 5 viñetas o menos?
- [ ] ¿El dashboard abre sin errores?
- [ ] ¿Se mencionan las limitaciones?
- [ ] ¿Pasó la verificación? (la confirma la sesión principal tras el verificador)
