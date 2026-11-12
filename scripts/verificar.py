# -*- coding: utf-8 -*-
"""Verificador independiente de cifras – Distribuidora Pacífico S.A.

Parte del CSV original datos/ventas_2025.csv (solo lectura), aplica las reglas de
limpieza de la sección 2 de informes/informe_ventas.md, recalcula las cifras del
informe y las compara (tolerancia relativa 0,5 %). También compara los datos
embebidos en docs/index.html con los valores recalculados.
Escribe informes/verificacion.md. Solo librería estándar.
"""
import csv
import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_ORIG = os.path.join(BASE, "datos", "ventas_2025.csv")
DASH = os.path.join(BASE, "docs", "index.html")
SALIDA = os.path.join(BASE, "informes", "verificacion.md")
TOL = 0.005
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
FECHA_REF = date(2025, 12, 31)

# ----------------------------------------------------------------- limpieza
with open(CSV_ORIG, encoding="utf-8", newline="") as f:
    lector = csv.reader(f)
    cab = next(lector)
    crudas = [r for r in lector]

n_orig = len(crudas)
vistos, sin_dup = set(), []
for r in crudas:
    t = tuple(r)
    if t in vistos:
        continue
    vistos.add(t)
    sin_dup.append(r)
elim_dup = n_orig - len(sin_dup)

I = {c: i for i, c in enumerate(cab)}
paso2 = [r for r in sin_dup if r[I["unidades"]].strip() != "" and r[I["precio_unitario"]].strip() != ""]
elim_vacias = len(sin_dup) - len(paso2)
paso3 = [r for r in paso2 if float(r[I["unidades"]]) > 0]
elim_neg = len(paso2) - len(paso3)

fechas_corregidas, elim_fecha, limpias = [], 0, []
for r in paso3:
    fs = r[I["fecha"]].strip()
    d = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fs):
        y, m, dd = map(int, fs.split("-"))
    elif re.fullmatch(r"\d{4}[./]\d{2}[./]\d{2}", fs):
        y, m, dd = map(int, re.split(r"[./]", fs))
        fechas_corregidas.append((r[I["id_pedido"]], fs))
    elif re.fullmatch(r"\d{2}/\d{2}/\d{4}", fs):
        a, b, c = map(int, fs.split("/"))
        if a > 12:
            y, m, dd = c, b, a
            fechas_corregidas.append((r[I["id_pedido"]], fs))
        else:
            y = None
    else:
        y = None
    try:
        d = date(y, m, dd) if y else None
    except ValueError:
        d = None
    if d is None:
        elim_fecha += 1
        continue
    unid = int(float(r[I["unidades"]]))
    pu = float(r[I["precio_unitario"]])
    desc = float(r[I["descuento_pct"]])
    cu = float(r[I["costo_unitario"]])
    limpias.append({
        "id": r[I["id_pedido"]], "fecha": d, "mes": d.month, "cli": r[I["id_cliente"]],
        "region": r[I["region"]], "ciudad": r[I["ciudad"]], "canal": r[I["canal"]],
        "cat": r[I["categoria"]], "prod": r[I["producto"]], "unid": unid, "desc": desc,
        "bruto": unid * pu, "venta": unid * pu * (1 - desc / 100), "costo": unid * cu, "pu": pu, "cu": cu,
    })
total_elim = n_orig - len(limpias)

# ----------------------------------------------------------------- helpers
def agg(filas):
    v = sum(x["venta"] for x in filas)
    c = sum(x["costo"] for x in filas)
    return {"ventas": v, "costo": c, "margen": v - c, "mpct": (v - c) / v * 100 if v else 0.0,
            "pedidos": len({x["id"] for x in filas}), "unid": sum(x["unid"] for x in filas),
            "clientes": len({x["cli"] for x in filas})}

def por(filas, clave):
    g = defaultdict(list)
    for x in filas:
        g[x[clave]].append(x)
    return g

def s1(filas):
    return [x for x in filas if x["mes"] <= 6]

def s2(filas):
    return [x for x in filas if x["mes"] >= 7]

def var(filas):
    a = sum(x["venta"] for x in s1(filas))
    b = sum(x["venta"] for x in s2(filas))
    return a, b, (b - a) / a * 100 if a else float("nan")

def desc_pond(filas):
    br = sum(x["bruto"] for x in filas)
    return sum(x["bruto"] * x["desc"] / 100 for x in filas) / br * 100

L = limpias
T = agg(L)
VT = T["ventas"]

# ----------------------------------------------------------------- comprobaciones
checks = []  # (seccion, cifra, valor_informe, valor_recalculado)

def chk(sec, nombre, inf, rec):
    checks.append((sec, nombre, inf, rec))

S = "2. Calidad"
chk(S, "Filas originales", 3000, n_orig)
chk(S, "Duplicados exactos eliminados", 15, elim_dup)
chk(S, "Filas con unidades o precio vacío eliminadas", 20, elim_vacias)
chk(S, "Filas con unidades <= 0 eliminadas", 3, elim_neg)
chk(S, "Fechas corregidas (nº)", 2, len(fechas_corregidas))
chk(S, "Fechas corregidas (ids)", "PED-01769, PED-02058", ", ".join(sorted(i for i, _ in fechas_corregidas)))
chk(S, "Filas eliminadas por fecha inválida", 0, elim_fecha)
chk(S, "Total filas eliminadas", 38, total_elim)
chk(S, "Filas tras limpieza", 2962, len(L))
chk(S, "id_pedido únicos tras limpieza", 2962, T["pedidos"])
chk(S, "% filas eliminadas", 1.27, total_elim / n_orig * 100)

S = "3. KPIs"
chk(S, "Ventas netas (USD)", 79717.57, VT)
chk(S, "Costo total (USD)", 52003.00, T["costo"])
chk(S, "Margen bruto (USD)", 27714.57, T["margen"])
chk(S, "Margen %", 34.77, T["mpct"])
chk(S, "Pedidos", 2962, T["pedidos"])
chk(S, "Ticket promedio (USD)", 26.91, VT / T["pedidos"])
chk(S, "Clientes activos", 380, T["clientes"])
chk(S, "Unidades vendidas", 24236, T["unid"])
chk(S, "Descuento medio ponderado %", 8.96, desc_pond(L))

S = "4.1 Mes"
inf_mes = [(5977.50, 34.70, 207, None), (5117.67, 35.16, 185, -14.38), (6312.51, 34.72, 209, 23.35),
           (5572.76, 35.69, 204, -11.72), (9371.87, 35.44, 324, 68.17), (6149.56, 34.83, 233, -34.38),
           (6038.12, 34.16, 232, -1.81), (6056.22, 35.44, 231, 0.30), (6559.76, 34.02, 233, 8.31),
           (6274.72, 34.40, 244, -4.35), (6253.38, 34.11, 267, -0.34), (10033.50, 34.54, 393, 60.45)]
gm = por(L, "mes")
am = {m: agg(gm[m]) for m in range(1, 13)}
for m in range(1, 13):
    v, mp, pe, cr = inf_mes[m - 1]
    n = MESES[m - 1]
    chk(S, f"{n} ventas", v, am[m]["ventas"])
    chk(S, f"{n} margen %", mp, am[m]["mpct"])
    chk(S, f"{n} pedidos", pe, am[m]["pedidos"])
    if cr is not None:
        chk(S, f"{n} crecimiento vs mes anterior %", cr, (am[m]["ventas"] / am[m - 1]["ventas"] - 1) * 100)
mmax = max(am, key=lambda m: am[m]["ventas"])
mmin = min(am, key=lambda m: am[m]["ventas"])
chk(S, "Mes con más ventas", "Dic", MESES[mmax - 1])
chk(S, "Mes con menos ventas", "Feb", MESES[mmin - 1])
def cat_mes(cat, m):
    return sum(x["venta"] for x in L if x["cat"] == cat and x["mes"] == m)
chk(S, "May Cuidado personal", 3170.61, cat_mes("Cuidado personal", 5))
chk(S, "May Hogar", 2403.33, cat_mes("Hogar", 5))
chk(S, "Abr Cuidado personal", 997.92, cat_mes("Cuidado personal", 4))
chk(S, "Abr Hogar", 949.15, cat_mes("Hogar", 4))
chk(S, "Dic Hogar", 2733.53, cat_mes("Hogar", 12))
chk(S, "Dic Bebidas", 2518.07, cat_mes("Bebidas", 12))
chk(S, "Dic Snacks", 1924.61, cat_mes("Snacks", 12))
a, b, c = var(L)
chk(S, "S1 total", 38501.88, a)
chk(S, "S2 total", 41215.69, b)
chk(S, "Crecimiento S2 vs S1 %", 7.05, c)

def tabla_dim(S, clave, filas_inf):
    g = por(L, clave)
    for nom, v, mg, mp, part, pe in filas_inf:
        a_ = agg(g.get(nom, []))
        chk(S, f"{nom} ventas", v, a_["ventas"])
        chk(S, f"{nom} margen USD", mg, a_["margen"])
        chk(S, f"{nom} margen %", mp, a_["mpct"])
        chk(S, f"{nom} participación %", part, a_["ventas"] / VT * 100)
        chk(S, f"{nom} pedidos", pe, a_["pedidos"])

def tabla_var(S, clave, filas_inf):
    g = por(L, clave)
    for nom, v1, v2, vr in filas_inf:
        a_, b_, c_ = var(g.get(nom, []))
        chk(S, f"{nom} S1", v1, a_)
        chk(S, f"{nom} S2", v2, b_)
        chk(S, f"{nom} variación S1→S2 %", vr, c_)

S = "4.2 Región"
tabla_dim(S, "region", [("Costa", 37394.03, 12981.12, 34.71, 46.91, 1379), ("Sierra", 31871.46, 11207.36, 35.16, 39.98, 1214),
                        ("Amazonía", 7465.31, 2583.96, 34.61, 9.36, 272), ("Insular", 2986.78, 942.13, 31.54, 3.75, 97)])
tabla_var(S, "region", [("Insular", 1156.45, 1830.33, 58.27), ("Amazonía", 3120.97, 4344.34, 39.20),
                        ("Sierra", 15613.44, 16258.02, 4.13), ("Costa", 18611.02, 18783.00, 0.92)])
gr = por(L, "region")
crec_reg = {r: var(gr[r])[2] for r in gr}
chk(S, "Región que más crece (S2 vs S1)", "Insular", max(crec_reg, key=crec_reg.get))
S = "4.2 Ciudad"
tabla_dim(S, "ciudad", [("Manta", 16008.63, 5550.98, 34.67, 20.08, 567), ("Quito", 14975.57, 5188.87, 34.65, 18.79, 548),
                        ("Machala", 12934.92, 4460.27, 34.48, 16.23, 483), ("Cuenca", 8597.37, 3029.92, 35.24, 10.78, 370),
                        ("Guayaquil", 8450.48, 2969.88, 35.14, 10.60, 329), ("Ambato", 8298.52, 2988.57, 36.01, 10.41, 296),
                        ("Tena", 3866.54, 1290.34, 33.37, 4.85, 139), ("Puyo", 3598.77, 1293.62, 35.95, 4.51, 133),
                        ("Puerto Ayora", 2986.78, 942.13, 31.54, 3.75, 97)])
ins = gr["Insular"]
ins_may = [x for x in ins if x["canal"] == "Mayorista"]
chk(S, "Insular: % ventas por Mayorista", 52.63, sum(x["venta"] for x in ins_may) / sum(x["venta"] for x in ins) * 100)
chk(S, "Insular: margen % Mayorista", 25.66, agg(ins_may)["mpct"])
chk(S, "Insular: descuento medio ponderado %", 12.72, desc_pond(ins))

S = "4.3 Canal"
tabla_dim(S, "canal", [("Tienda física", 36563.56, 14230.71, 38.92, 45.87, 1664), ("Mayorista", 30458.40, 8898.70, 29.22, 38.21, 437),
                       ("Online", 12695.61, 4585.16, 36.12, 15.93, 861)])
tabla_var(S, "canal", [("Online", 3605.18, 9090.43, 152.15), ("Mayorista", 14165.07, 16293.33, 15.02),
                       ("Tienda física", 20731.62, 15831.94, -23.63)])
gc = por(L, "canal")
crec_can = {k: var(gc[k])[2] for k in gc}
chk(S, "Canal que más crece (S2 vs S1)", "Online", max(crec_can, key=crec_can.get))
canal_mes = {
    "Tienda física": [3485.17, 3284.49, 3101.53, 3566.22, 4554.34, 2739.87, 2124.63, 3015.70, 2644.35, 2526.72, 2093.75, 3426.78],
    "Mayorista": [2273.86, 1562.37, 2776.51, 1441.95, 3613.56, 2496.84, 2822.06, 2055.81, 2576.90, 2207.08, 2629.71, 4001.77],
    "Online": [218.48, 270.81, 434.47, 564.59, 1203.97, 912.85, 1091.43, 984.71, 1338.50, 1540.91, 1529.92, 2604.95],
}
for k, vals in canal_mes.items():
    for m, v in enumerate(vals, 1):
        chk(S, f"{k} {MESES[m - 1]} ventas", v, sum(x["venta"] for x in gc[k] if x["mes"] == m))
reg_can = {"Amazonía": (420.89, 19.99, -14.84), "Costa": (97.73, -25.26, 14.52),
           "Insular": (278.79, -21.89, 110.95), "Sierra": (157.86, -29.15, 14.38)}
for r, vals in reg_can.items():
    for k, v in zip(["Online", "Tienda física", "Mayorista"], vals):
        chk(S, f"{r} / {k} variación S1→S2 %", v, var([x for x in gr[r] if x["canal"] == k])[2])
for k, v in [("Tienda física", 2.75), ("Mayorista", 16.21), ("Online", 6.77)]:
    chk(S, f"{k} descuento medio ponderado %", v, desc_pond(gc[k]))

S = "4.4 Categoría"
tabla_dim(S, "cat", [("Limpieza", 17668.24, 5735.04, 32.46, 22.16, 591), ("Bebidas", 17580.88, 5963.28, 33.92, 22.05, 755),
                     ("Hogar", 17448.46, 5498.46, 31.51, 21.89, 226), ("Cuidado personal", 15843.67, 5995.27, 37.84, 19.87, 634),
                     ("Snacks", 11176.32, 4522.52, 40.47, 14.02, 756)])
tabla_var(S, "cat", [("Hogar", 7247.60, 10200.87, 40.75), ("Snacks", 4958.61, 6217.70, 25.39), ("Bebidas", 9028.08, 8552.80, -5.26),
                     ("Limpieza", 9074.70, 8593.54, -5.30), ("Cuidado personal", 8192.88, 7650.79, -6.62)])

S = "4.5 Producto"
gp = por(L, "prod")
ap = {p: agg(gp[p]) for p in gp}
orden = sorted(ap, key=lambda p: ap[p]["ventas"], reverse=True)
chk(S, "Nº de productos", 15, len(ap))
chk(S, "Top producto por ventas", "Detergente 2kg", orden[0])
chk(S, "Top 5 (orden)", "Detergente 2kg, Agua mineral 6x1L, Shampoo 400ml, Set de ollas, Juego de toallas", ", ".join(orden[:5]))
chk(S, "Bottom 5 (de menor a mayor)", "Cloro 1L, Chocolate 100g, Galletas integrales, Crema dental 150g, Desinfectante multiuso",
    ", ".join(list(reversed(orden))[:5]))
for p, v, mp, part in [("Detergente 2kg", 11605.11, 30.19, 14.56), ("Agua mineral 6x1L", 8402.94, 33.25, 10.54),
                       ("Shampoo 400ml", 7856.46, 37.38, 9.86), ("Set de ollas", 7654.05, 28.04, 9.60),
                       ("Juego de toallas", 5174.24, 35.87, 6.49), ("Cloro 1L", 2360.92, 37.82, 2.96),
                       ("Chocolate 100g", 3240.55, 39.70, 4.07), ("Galletas integrales", 3622.04, 42.35, 4.54),
                       ("Crema dental 150g", 3675.54, 37.96, 4.61), ("Desinfectante multiuso", 3702.21, 36.16, 4.64)]:
    chk(S, f"{p} ventas", v, ap[p]["ventas"])
    chk(S, f"{p} margen %", mp, ap[p]["mpct"])
    chk(S, f"{p} participación %", part, ap[p]["ventas"] / VT * 100)
chk(S, "Producto con menor margen %", "Set de ollas", min(ap, key=lambda p: ap[p]["mpct"]))
tabla_var(S, "prod", [("Vajilla 12 piezas", 1826.29, 2793.88, 52.98), ("Chocolate 100g", 1311.03, 1929.52, 47.18),
                      ("Juego de toallas", 2135.98, 3038.27, 42.24), ("Agua mineral 6x1L", 3507.73, 4895.21, 39.56),
                      ("Jugo de naranja 1L", 2094.95, 2789.75, 33.17), ("Set de ollas", 3285.33, 4368.72, 32.98),
                      ("Crema dental 150g", 1619.54, 2055.99, 26.95), ("Papas fritas 200g", 1948.26, 2365.46, 21.41),
                      ("Galletas integrales", 1699.32, 1922.72, 13.15), ("Desinfectante multiuso", 1826.65, 1875.56, 2.68),
                      ("Cloro 1L", 1213.78, 1147.14, -5.49), ("Detergente 2kg", 6034.27, 5570.84, -7.68),
                      ("Shampoo 400ml", 4235.29, 3621.17, -14.50), ("Jabón de tocador x3", 2338.04, 1973.63, -15.59),
                      ("Gaseosa cola 3L", 3425.40, 867.84, -74.66)])
crec_p = {p: var(gp[p])[2] for p in gp}
chk(S, "Producto que más cae S2 vs S1", "Gaseosa cola 3L", min(crec_p, key=crec_p.get))
gas = gp["Gaseosa cola 3L"]
for m, v in enumerate([584.01, 434.28, 530.13, 399.05, 655.19, 822.74, 96.57, 122.46, 190.98, 77.99, 57.89, 321.95], 1):
    chk(S, f"Gaseosa {MESES[m - 1]} ventas", v, sum(x["venta"] for x in gas if x["mes"] == m))
for m, v in enumerate([26, 15, 21, 19, 28, 28, 9, 8, 5, 4, 4, 14], 1):
    chk(S, f"Gaseosa {MESES[m - 1]} líneas", v, sum(1 for x in gas if x["mes"] == m))
for k, v in [("Online", -4.51), ("Tienda física", -79.08), ("Mayorista", -81.62)]:
    chk(S, f"Gaseosa {k} variación %", v, var([x for x in gas if x["canal"] == k])[2])
for r, v in [("Amazonía", -20.66), ("Sierra", -76.30), ("Costa", -77.71), ("Insular", -100.00)]:
    chk(S, f"Gaseosa {r} variación %", v, var([x for x in gas if x["region"] == r])[2])

# ----------------------------------------------------------------- RFM
S = "5. RFM"
gcli = por(L, "cli")
cli = {}
for c, fs in gcli.items():
    cli[c] = {"R": (FECHA_REF - max(x["fecha"] for x in fs)).days,
              "F": len({x["id"] for x in fs}), "M": sum(x["venta"] for x in fs)}
n = len(cli)
def puntaje(dim, peor_mayor):
    vals = [cli[c][dim] for c in cli]
    for c in cli:
        v = cli[c][dim]
        k = sum(1 for w in vals if (w > v if peor_mayor else w < v))
        cli[c]["s" + dim] = min(5, 1 + math.floor(5 * k / n))
puntaje("R", True)
puntaje("F", False)
puntaje("M", False)
def segmento(R, F):
    if R >= 4 and F >= 4: return "Campeones"
    if R >= 3 and F >= 3: return "Leales"
    if R >= 3 and F <= 2: return "Potenciales"
    if R == 2 or (R == 1 and F >= 3): return "En riesgo"
    return "Perdidos"
for c in cli:
    cli[c]["seg"] = segmento(cli[c]["sR"], cli[c]["sF"])
dist_inf = {"R": [76, 78, 78, 72, 76], "F": [86, 99, 50, 83, 62], "M": [76, 76, 76, 76, 76]}
for d, lst in dist_inf.items():
    for p, v in enumerate(lst, 1):
        chk(S, f"Clientes con puntaje {d}={p}", v, sum(1 for c in cli if cli[c]["s" + d] == p))
for sg, nc, v, pv, rm, fm in [("Campeones", 87, 47893.56, 60.08, 9.60, 20.85), ("Leales", 62, 10265.53, 12.88, 32.26, 6.21),
                              ("Potenciales", 77, 6547.32, 8.21, 24.09, 3.14), ("En riesgo", 89, 11689.87, 14.66, 101.28, 4.38),
                              ("Perdidos", 65, 3321.28, 4.17, 236.49, 2.02)]:
    cs = [c for c in cli if cli[c]["seg"] == sg]
    vv = sum(cli[c]["M"] for c in cs)
    chk(S, f"{sg} clientes", nc, len(cs))
    chk(S, f"{sg} ventas", v, vv)
    chk(S, f"{sg} % ventas", pv, vv / VT * 100)
    chk(S, f"{sg} recencia media", rm, sum(cli[c]["R"] for c in cs) / len(cs) if cs else float("nan"))
    chk(S, f"{sg} frecuencia media", fm, sum(cli[c]["F"] for c in cs) / len(cs) if cs else float("nan"))
chk(S, "Suma de segmentos", 380, sum(1 for c in cli))

# ----------------------------------------------------------------- Preguntas
S = "6. Preguntas"
ama = gr["Amazonía"]
chk(S, "Amazonía clientes", 37, len({x["cli"] for x in ama}))
a_, b_, _ = var([x for x in ama if x["canal"] == "Online"])
chk(S, "Amazonía Online S1", 270.54, a_)
chk(S, "Amazonía Online S2", 1409.20, b_)
riesgo = [c for c in cli if cli[c]["seg"] == "En riesgo"]
top20 = sorted(riesgo, key=lambda c: cli[c]["M"], reverse=True)[:20]
chk(S, "Top 20 en riesgo: monto", 5819.60, sum(cli[c]["M"] for c in top20))
lr = [x for x in L if x["cli"] in set(riesgo)]
vr = sum(x["venta"] for x in lr)
chk(S, "En riesgo: % compras en Costa", 54.63, sum(x["venta"] for x in lr if x["region"] == "Costa") / vr * 100)
chk(S, "En riesgo: % compras en Tienda física", 46.23, sum(x["venta"] for x in lr if x["canal"] == "Tienda física") / vr * 100)
alto = [x for x in L if x["desc"] > 15]
resto = [x for x in L if x["desc"] <= 15]
aa = agg(alto)
chk(S, "Líneas con descuento > 15 %", 211, len(alto))
chk(S, "Ventas con descuento > 15 %", 11402.35, aa["ventas"])
chk(S, "Margen % con descuento > 15 %", 23.42, aa["mpct"])
chk(S, "Líneas > 15 % en Mayorista", 151, sum(1 for x in alto if x["canal"] == "Mayorista"))
chk(S, "Líneas > 15 % en Online", 60, sum(1 for x in alto if x["canal"] == "Online"))
vA = sum(x["venta"] for x in resto) + sum(x["bruto"] * 0.85 for x in alto)
mA = vA - T["costo"]
chk(S, "Escenario A ventas", 80783.97, vA)
chk(S, "Escenario A margen USD", 28780.97, mA)
chk(S, "Escenario A margen %", 35.63, mA / vA * 100)
chk(S, "Escenario A margen adicional", 1066.40, mA - T["margen"])
ar = agg(resto)
chk(S, "Escenario B ventas", 68315.22, ar["ventas"])
chk(S, "Escenario B margen USD", 25043.87, ar["margen"])
chk(S, "Escenario B margen %", 36.66, ar["mpct"])
chk(S, "Escenario B caída de margen USD", 2670.70, T["margen"] - ar["margen"])

# ----------------------------------------------------------------- comparación
def comparar(inf, rec):
    if isinstance(inf, str) or isinstance(rec, str):
        return str(inf) == str(rec)
    if isinstance(rec, float) and math.isnan(rec):
        return False
    if round(rec, 2) == round(inf, 2):
        return True
    if inf == 0:
        return abs(rec) < 0.005
    return abs(rec - inf) / abs(inf) <= TOL

def fmt(v):
    if isinstance(v, str):
        return v
    if isinstance(v, int):
        return str(v)
    return f"{v:,.2f}"

res = [(s, n_, inf, rec, comparar(inf, rec)) for s, n_, inf, rec in checks]

# ----------------------------------------------------------------- dashboard
dash_res = []
with open(DASH, encoding="utf-8") as f:
    html = f.read()
mt = re.search(r'<script id="datos" type="application/json">(.*?)</script>', html, re.S)
if not mt:
    dash_res.append(("JSON embebido", "no encontrado", "", False))
else:
    D = json.loads(mt.group(1))
    def dchk(nombre, val, rec):
        dash_res.append((nombre, val, rec, comparar(val, rec)))
    for reg in D["porRegion"]:
        fs = L if reg == "Todas" else gr.get(reg, [])
        B = D["porRegion"][reg]
        a_ = agg(fs)
        k = B["kpis"]
        dchk(f"[{reg}] ventas_netas", k["ventas_netas"], a_["ventas"])
        dchk(f"[{reg}] costo_total", k["costo_total"], a_["costo"])
        dchk(f"[{reg}] margen_bruto", k["margen_bruto"], a_["margen"])
        dchk(f"[{reg}] margen_pct", k["margen_pct"], a_["mpct"])
        dchk(f"[{reg}] pedidos", k["pedidos"], a_["pedidos"])
        dchk(f"[{reg}] ticket_promedio", k["ticket_promedio"], a_["ventas"] / a_["pedidos"])
        dchk(f"[{reg}] clientes_activos", k["clientes_activos"], a_["clientes"])
        dchk(f"[{reg}] unidades", k["unidades"], a_["unid"])
        gmm = por(fs, "mes")
        prev = None
        for e in B["mensual"]:
            am_ = agg(gmm.get(e["mes"], []))
            dchk(f"[{reg}] {e['nombre']} ventas", e["ventas"], am_["ventas"])
            dchk(f"[{reg}] {e['nombre']} margen_pct", e["margen_pct"], am_["mpct"])
            dchk(f"[{reg}] {e['nombre']} pedidos", e["pedidos"], am_["pedidos"])
            if e["crecimiento_pct"] is not None:
                dchk(f"[{reg}] {e['nombre']} crecimiento_pct", e["crecimiento_pct"], (am_["ventas"] / prev - 1) * 100)
            prev = am_["ventas"]
        tot = a_["ventas"]
        for bloque, clave in [("canal", "canal"), ("categoria", "cat"), ("top_productos", "prod")]:
            gg = por(fs, clave)
            for nom, e in B[bloque].items():
                ag = agg(gg.get(nom, []))
                dchk(f"[{reg}] {bloque}/{nom} ventas", e["ventas"], ag["ventas"])
                dchk(f"[{reg}] {bloque}/{nom} margen", e["margen"], ag["margen"])
                dchk(f"[{reg}] {bloque}/{nom} margen_pct", e["margen_pct"], ag["mpct"])
                dchk(f"[{reg}] {bloque}/{nom} participacion_pct", e["participacion_pct"], ag["ventas"] / tot * 100)
                dchk(f"[{reg}] {bloque}/{nom} pedidos", e["pedidos"], ag["pedidos"])
                dchk(f"[{reg}] {bloque}/{nom} unidades", e["unidades"], ag["unid"])
        gpp = por(fs, "prod")
        top5 = sorted(gpp, key=lambda p: sum(x["venta"] for x in gpp[p]), reverse=True)[:5]
        dchk(f"[{reg}] top 5 productos (orden)", ", ".join(B["top_productos"].keys()), ", ".join(top5))
        clis = {x["cli"] for x in fs}
        for sg in ["Campeones", "Leales", "Potenciales", "En riesgo", "Perdidos"]:
            dchk(f"[{reg}] rfm {sg}", B["rfm"].get(sg, 0), sum(1 for c in clis if cli[c]["seg"] == sg))
    for sg, e in D["segmentos"].items():
        cs = [c for c in cli if cli[c]["seg"] == sg]
        vv = sum(cli[c]["M"] for c in cs)
        dchk(f"segmentos/{sg} clientes", e["clientes"], len(cs))
        dchk(f"segmentos/{sg} ventas", e["ventas"], vv)
        dchk(f"segmentos/{sg} participacion_pct", e["participacion_pct"], vv / VT * 100)
        dchk(f"segmentos/{sg} recencia_media", e["recencia_media"], sum(cli[c]["R"] for c in cs) / len(cs))
        dchk(f"segmentos/{sg} frecuencia_media", e["frecuencia_media"], sum(cli[c]["F"] for c in cs) / len(cs))
    for r, e in D["regiones"].items():
        ag = agg(gr.get(r, []))
        dchk(f"regiones/{r} ventas", e["ventas"], ag["ventas"])
        dchk(f"regiones/{r} margen_pct", e["margen_pct"], ag["mpct"])
    dchk("calidad/antes", D["calidad"]["antes"], n_orig)
    dchk("calidad/despues", D["calidad"]["despues"], len(L))
    mot = D["calidad"]["motivos"]
    dchk("calidad/duplicados", mot.get("duplicado exacto (se conserva 1 copia)"), elim_dup)
    dchk("calidad/vacías", mot.get("unidades o precio_unitario vacío"), elim_vacias)
    dchk("calidad/negativas", mot.get("unidades negativas o cero"), elim_neg)
    # textos del dashboard idénticos al informe
    with open(os.path.join(BASE, "informes", "informe_ventas.md"), encoding="utf-8") as f:
        inf_txt = f.read()
    for i, t in enumerate(D["resumen"], 1):
        dchk(f"resumen[{i}] idéntico al informe", "sí", "sí" if t in inf_txt else "no")
    for i, q in enumerate(D["preguntas"], 1):
        dchk(f"pregunta {i}: respuesta idéntica al informe", "sí", "sí" if q["r"] in inf_txt else "no")

# ----------------------------------------------------------------- salida
ok = sum(1 for r in res if r[4])
err = [r for r in res if not r[4]]
dok = sum(1 for r in dash_res if r[3])
derr = [r for r in dash_res if not r[3]]

out = []
out.append("# Verificación independiente de cifras – Informe de ventas 2025\n")
out.append(f"- Fecha de verificación: {date.today().isoformat()}")
out.append("- Script: `scripts/verificar.py` (solo librería estándar; no reutiliza `scripts/analisis.py` ni lee `datos/ventas_limpias.csv`).")
out.append("- Fuente: `datos/ventas_2025.csv` (original, solo lectura).")
out.append("- Tolerancia: diferencia relativa ≤ 0,5 % (o igualdad al redondear a 2 decimales). Textos: coincidencia exacta.\n")
out.append("## Reglas de limpieza aplicadas (sección 2 del informe)\n")
out.append(f"1. Duplicados exactos (12 columnas, texto tal cual), se conserva la primera aparición: {elim_dup} filas eliminadas.")
out.append(f"2. `unidades` o `precio_unitario` vacío: {elim_vacias} filas eliminadas.")
out.append(f"3. `unidades` ≤ 0: {elim_neg} filas eliminadas.")
out.append("4. Fechas: `AAAA.MM.DD`/`AAAA/MM/DD` → AAAA-MM-DD; `DD/MM/AAAA` solo si día > 12; ambigua o inválida → se elimina. "
           f"Corregidas: {', '.join(f'{i} («{s}»)' for i, s in fechas_corregidas)}; eliminadas: {elim_fecha}.")
out.append("5. Precios, descuentos y costos sin cambios.")
out.append(f"\nFilas: {n_orig} → {len(L)} ({total_elim} eliminadas).\n")
out.append("Fórmulas: ventas netas = unidades × precio_unitario × (1 − descuento_pct/100); costo = unidades × costo_unitario; "
           "S1 = ene-jun, S2 = jul-dic. RFM: fecha de referencia 2025-12-31, puntaje = min(5, 1 + ⌊5·k/n⌋) con k = nº de clientes "
           "estrictamente peores, segmentos según la sección 5 del informe.\n")
out.append("## Resumen\n")
out.append(f"- **Informe (`informes/informe_ventas.md`): {ok} OK, {len(err)} ERROR** de {len(res)} cifras comprobadas.")
out.append(f"- **Dashboard (`docs/index.html`, datos embebidos): {dok} OK, {len(derr)} ERROR** de {len(dash_res)} valores comprobados.\n")
if err or derr:
    out.append("### Errores\n")
    for s, n_, inf, rec, _ in err:
        out.append(f"- Informe – {s} – {n_}: informe {fmt(inf)}, recalculado {fmt(rec)}.")
    for n_, inf, rec, _ in derr:
        out.append(f"- Dashboard – {n_}: dashboard {fmt(inf)}, recalculado {fmt(rec)}.")
    out.append("")
else:
    out.append("No se encontraron errores.\n")
out.append("## Detalle – informe\n")
out.append("| Sección | Cifra | Valor en informe | Valor recalculado | Estado |")
out.append("|---|---|---|---|---|")
for s, n_, inf, rec, e in res:
    out.append(f"| {s} | {n_} | {fmt(inf)} | {fmt(rec)} | {'OK' if e else 'ERROR'} |")
out.append("\n## Detalle – dashboard (`docs/index.html`)\n")
out.append("| Cifra | Valor en dashboard | Valor recalculado | Estado |")
out.append("|---|---|---|---|")
for n_, inf, rec, e in dash_res:
    out.append(f"| {n_} | {fmt(inf)} | {fmt(rec)} | {'OK' if e else 'ERROR'} |")
with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

sys.stdout.reconfigure(encoding="utf-8")
print(f"Informe: {ok} OK, {len(err)} ERROR de {len(res)}")
print(f"Dashboard: {dok} OK, {len(derr)} ERROR de {len(dash_res)}")
for s, n_, inf, rec, _ in err:
    print("ERROR informe:", s, "|", n_, "|", fmt(inf), "vs", fmt(rec))
for n_, inf, rec, _ in derr:
    print("ERROR dashboard:", n_, "|", fmt(inf), "vs", fmt(rec))
