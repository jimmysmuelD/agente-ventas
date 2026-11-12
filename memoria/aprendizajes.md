# Aprendizajes del Agente Analista de Ventas

Regla: guardar aquí solo lecciones que sirvan para análisis futuros (no correcciones de una
sola vez). Cada lección con fecha (AAAA-MM-DD) y una línea de por qué importa.

<!-- Formato: - AAAA-MM-DD – Lección. Por qué: ... -->
- 2026-11-12 – Aplicar la limpieza en orden fijo (duplicados exactos → vacíos en unidades/precio → unidades ≤ 0 → fechas) y reportar cada conteo en ese orden. Por qué: el verificador recalcula desde el CSV original y un orden distinto cambia los conteos por motivo.
- 2026-11-12 – Fechas: aceptar solo correcciones inequívocas (AAAA.MM.DD, AAAA/MM/DD, DD/MM/AAAA con día > 12) y listar cada id_pedido corregido. Por qué: deja la regla recalculable y evita inventar fechas ambiguas.
- 2026-11-12 – Antes de concluir, desglosar S1 vs S2 por producto y por canal × mes: los totales anuales ocultaron una caída de ~75 % de un producto y el traspaso Tienda física → Online. Por qué: las alertas importantes aparecen en el desglose, no en el total.
- 2026-11-12 – Si el informe se genera desde resultados.json, recordar que json convierte claves numéricas en texto (usar str(k) al leer). Por qué: provocó una tabla RFM con ceros silenciosos.
- 2026-11-12 – En textos con verbos de caída ("cayó", "bajó") usar el valor absoluto del %. Por qué: evita frases como "cayó -23 %" que confunden al gerente.
