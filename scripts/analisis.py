"""Análisis de ventas 2025 – Distribuidora Pacífico S.A.

Uso:  python scripts/analisis.py
Solo librería estándar. Lee datos/ventas_2025.csv (sin modificarlo), genera:
  - datos/ventas_limpias.csv
  - informes/resultados.json
  - informes/informe_ventas.md
  - docs/index.html
"""
import csv
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEN = RAIZ / "datos" / "ventas_2025.csv"
LIMPIO = RAIZ / "datos" / "ventas_limpias.csv"
RESULTADOS = RAIZ / "informes" / "resultados.json"
INFORME = RAIZ / "informes" / "informe_ventas.md"
DASHBOARD = RAIZ / "docs" / "index.html"
FECHA_REF = dt.date(2025, 12, 31)
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def r2(x):
    return round(x + 0.0, 2)


def pct(a, b):
    return r2(100.0 * a / b) if b else None


# --------------------------------------------------------------------------- Paso 1
def normalizar_fecha(texto):
    """Devuelve (fecha_iso, corregida?) o (None, None) si no es inequívoca."""
    t = texto.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t):
        try:
            return dt.date.fromisoformat(t).isoformat(), False
        except ValueError:
            return None, None
    m = re.fullmatch(r"(\d{4})[./](\d{2})[./](\d{2})", t)          # AAAA.MM.DD
    if m:
        a, mth, d = m.groups()
    else:
        m = re.fullmatch(r"(\d{2})[/.-](\d{2})[/.-](\d{4})", t)    # DD/MM/AAAA
        if not m:
            return None, None
        d, mth, a = m.groups()
        if int(d) <= 12:      # ambiguo DD/MM vs MM/DD -> no se corrige
            return None, None
    try:
        return dt.date(int(a), int(mth), int(d)).isoformat(), True
    except ValueError:
        return None, None


def limpiar():
    with open(ORIGEN, encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        columnas = lector.fieldnames
        filas = list(lector)
    calidad = {"filas_originales": len(filas)}

    calidad["vacios_por_columna"] = {c: sum(1 for x in filas if (x[c] or "").strip() == "")
                                     for c in columnas}
    vistos, sin_dup = set(), []
    for x in filas:
        clave = tuple(x[c] for c in columnas)
        if clave in vistos:
            continue
        vistos.add(clave)
        sin_dup.append(x)
    calidad["duplicados_exactos"] = len(filas) - len(sin_dup)

    def ent(v):
        try:
            return int(v.strip())
        except (ValueError, AttributeError):
            return None

    calidad["unidades_negativas_o_cero"] = sum(1 for x in sin_dup
                                               if ent(x["unidades"]) is not None and ent(x["unidades"]) <= 0)
    calidad["fechas_mal_formato"] = [x["fecha"] for x in sin_dup
                                     if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", x["fecha"].strip())]

    eliminadas = Counter()
    corregidas = []
    limpias = []
    for x in sin_dup:
        if x["unidades"].strip() == "" or x["precio_unitario"].strip() == "":
            eliminadas["unidades o precio_unitario vacío"] += 1
            continue
        if int(x["unidades"]) <= 0:
            eliminadas["unidades negativas o cero"] += 1
            continue
        fecha, fue_corregida = normalizar_fecha(x["fecha"])
        if fecha is None:
            eliminadas["fecha inválida o ambigua"] += 1
            continue
        if fue_corregida:
            corregidas.append({"id_pedido": x["id_pedido"], "original": x["fecha"], "corregida": fecha})
            x = dict(x, fecha=fecha)
        limpias.append(x)

    calidad["eliminadas_por_motivo"] = dict(eliminadas)
    calidad["eliminadas_por_motivo"] = {"duplicado exacto (se conserva 1 copia)": calidad["duplicados_exactos"],
                                        **dict(eliminadas)}
    calidad["fechas_corregidas"] = corregidas
    calidad["filas_finales"] = len(limpias)
    calidad["filas_eliminadas_total"] = len(filas) - len(limpias)
    calidad["ids_pedido_unicos_finales"] = len({x["id_pedido"] for x in limpias})

    LIMPIO.parent.mkdir(exist_ok=True)
    with open(LIMPIO, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columnas)
        w.writeheader()
        w.writerows(limpias)
    return limpias, calidad


# --------------------------------------------------------------------------- utilidades
def preparar(filas):
    out = []
    for x in filas:
        u = int(x["unidades"])
        p = float(x["precio_unitario"])
        d = float(x["descuento_pct"])
        c = float(x["costo_unitario"])
        venta = u * p * (1 - d / 100)
        costo = u * c
        fecha = dt.date.fromisoformat(x["fecha"])
        out.append({**x, "u": u, "p": p, "d": d, "c": c, "venta": venta, "costo": costo,
                    "margen": venta - costo, "fecha_d": fecha, "mes": fecha.month})
    return out


def kpis(filas):
    v = sum(x["venta"] for x in filas)
    c = sum(x["costo"] for x in filas)
    ped = len({x["id_pedido"] for x in filas})
    return {"ventas_netas": r2(v), "costo_total": r2(c), "margen_bruto": r2(v - c),
            "margen_pct": pct(v - c, v), "pedidos": ped, "ticket_promedio": r2(v / ped) if ped else 0,
            "clientes_activos": len({x["id_cliente"] for x in filas}),
            "unidades": sum(x["u"] for x in filas)}


def por(filas, clave, total=None):
    g = defaultdict(list)
    for x in filas:
        g[x[clave]].append(x)
    total = total if total is not None else sum(x["venta"] for x in filas)
    res = {}
    for k, xs in g.items():
        v = sum(x["venta"] for x in xs)
        m = sum(x["margen"] for x in xs)
        res[k] = {"ventas": r2(v), "margen": r2(m), "margen_pct": pct(m, v),
                  "participacion_pct": pct(v, total), "pedidos": len({x["id_pedido"] for x in xs}),
                  "unidades": sum(x["u"] for x in xs)}
    return dict(sorted(res.items(), key=lambda kv: -kv[1]["ventas"]))


def mensual(filas):
    res = []
    previo = None
    for m in range(1, 13):
        xs = [x for x in filas if x["mes"] == m]
        v = sum(x["venta"] for x in xs)
        mg = sum(x["margen"] for x in xs)
        res.append({"mes": m, "nombre": MESES[m - 1], "ventas": r2(v), "margen_pct": pct(mg, v),
                    "pedidos": len({x["id_pedido"] for x in xs}),
                    "crecimiento_pct": pct(v - previo, previo) if previo else None})
        previo = v
    return res


def semestres(filas, clave):
    g = defaultdict(lambda: [0.0, 0.0])
    for x in filas:
        g[x[clave]][0 if x["mes"] <= 6 else 1] += x["venta"]
    res = {k: {"S1": r2(a), "S2": r2(b), "variacion_pct": pct(b - a, a)} for k, (a, b) in g.items()}
    return dict(sorted(res.items(), key=lambda kv: -(kv[1]["variacion_pct"] or 0)))


# --------------------------------------------------------------------------- Paso 4 RFM
def puntaje(valor, todos, mayor_es_mejor=True):
    """Quintil por rango con empates: puntaje = 1 + floor(5 * k / n), tope 5, donde k = nº de
    clientes con valor estrictamente peor. Clientes empatados reciben el mismo puntaje."""
    n = len(todos)
    if mayor_es_mejor:
        k = sum(1 for t in todos if t < valor)
    else:
        k = sum(1 for t in todos if t > valor)
    return min(5, 1 + (5 * k) // n)


def segmento(r, f):
    if r >= 4 and f >= 4:
        return "Campeones"
    if r >= 3 and f >= 3:
        return "Leales"
    if r >= 3 and f <= 2:
        return "Potenciales"
    if r == 2 or (r == 1 and f >= 3):
        return "En riesgo"
    return "Perdidos"


ACCIONES = {
    "Campeones": "Programa VIP: acceso anticipado, beneficios por volumen y pedirles referidos.",
    "Leales": "Venta cruzada de categorías que aún no compran y puntos de fidelidad.",
    "Potenciales": "Incentivar la segunda/tercera compra con cupón de recompra a 30 días.",
    "En riesgo": "Contacto proactivo del vendedor y oferta personalizada de reactivación.",
    "Perdidos": "Campaña de bajo costo (correo/WhatsApp); no invertir descuentos altos.",
}
ORDEN_SEG = ["Campeones", "Leales", "Potenciales", "En riesgo", "Perdidos"]


def rfm(filas):
    cli = defaultdict(lambda: {"ultima": None, "pedidos": set(), "monto": 0.0, "region": None})
    for x in filas:
        c = cli[x["id_cliente"]]
        c["ultima"] = max(c["ultima"], x["fecha_d"]) if c["ultima"] else x["fecha_d"]
        c["pedidos"].add(x["id_pedido"])
        c["monto"] += x["venta"]
        c["region"] = x["region"]
    rec = {k: (FECHA_REF - v["ultima"]).days for k, v in cli.items()}
    fre = {k: len(v["pedidos"]) for k, v in cli.items()}
    mon = {k: v["monto"] for k, v in cli.items()}
    lr, lf, lm = list(rec.values()), list(fre.values()), list(mon.values())
    clientes = []
    for k in sorted(cli):
        R = puntaje(rec[k], lr, mayor_es_mejor=False)
        F = puntaje(fre[k], lf)
        M = puntaje(mon[k], lm)
        clientes.append({"id_cliente": k, "region": cli[k]["region"], "recencia": rec[k],
                         "frecuencia": fre[k], "monto": r2(mon[k]), "R": R, "F": F, "M": M,
                         "segmento": segmento(R, F)})
    total = sum(mon.values())
    seg = {}
    for s in ORDEN_SEG:
        cs = [c for c in clientes if c["segmento"] == s]
        v = sum(mon[c["id_cliente"]] for c in cs)
        seg[s] = {"clientes": len(cs), "ventas": r2(v), "participacion_pct": pct(v, total),
                  "recencia_media": r2(sum(c["recencia"] for c in cs) / len(cs)) if cs else None,
                  "frecuencia_media": r2(sum(c["frecuencia"] for c in cs) / len(cs)) if cs else None,
                  "accion": ACCIONES[s]}
    dist = {e: dict(sorted(Counter(c[e] for c in clientes).items())) for e in ("R", "F", "M")}
    return clientes, seg, dist


# --------------------------------------------------------------------------- Paso 5 descuentos
def escenarios_descuento(filas, tope=15):
    base_v = sum(x["venta"] for x in filas)
    base_m = sum(x["margen"] for x in filas)
    afect = [x for x in filas if x["d"] > tope]
    resto = [x for x in filas if x["d"] <= tope]
    # A: las ventas con descuento > tope se mantienen pero con descuento = tope
    va = sum(x["venta"] for x in resto) + sum(x["u"] * x["p"] * (1 - tope / 100) for x in afect)
    ma = va - sum(x["costo"] for x in filas)
    # B: las ventas con descuento > tope se pierden
    vb = sum(x["venta"] for x in resto)
    mb = sum(x["margen"] for x in resto)
    av = sum(x["venta"] for x in afect)
    am = sum(x["margen"] for x in afect)
    return {
        "lineas_afectadas": len(afect), "ventas_afectadas": r2(av), "margen_afectado": r2(am),
        "margen_pct_afectadas": pct(am, av),
        "base": {"ventas": r2(base_v), "margen": r2(base_m), "margen_pct": pct(base_m, base_v)},
        "A_tope_15": {"ventas": r2(va), "margen": r2(ma), "margen_pct": pct(ma, va),
                      "delta_margen": r2(ma - base_m)},
        "B_se_pierden": {"ventas": r2(vb), "margen": r2(mb), "margen_pct": pct(mb, vb),
                         "delta_margen": r2(mb - base_m)},
        "por_descuento": por(filas, "descuento_pct"),
    }


def matriz_mes(filas, clave):
    t = defaultdict(lambda: [0.0] * 12)
    for x in filas:
        t[x[clave]][x["mes"] - 1] += x["venta"]
    return {k: [r2(v) for v in vs] for k, vs in t.items()}


def investigar(filas):
    """Profundizaciones sobre lo que se sale de lo normal."""
    inv = {}
    inv["canal_por_mes"] = matriz_mes(filas, "canal")
    inv["categoria_por_mes"] = matriz_mes(filas, "categoria")
    g = [x for x in filas if x["producto"] == "Gaseosa cola 3L"]
    inv["gaseosa_por_mes"] = {"ventas": matriz_mes([{**x, "t": "t"} for x in g], "t")["t"],
                              "lineas": [sum(1 for x in g if x["mes"] == m) for m in range(1, 13)]}
    inv["gaseosa_semestre_canal"] = semestres(g, "canal")
    inv["gaseosa_semestre_region"] = semestres(g, "region")
    # descuento medio ponderado (por venta bruta)
    def desc_medio(xs):
        b = sum(x["u"] * x["p"] for x in xs)
        return r2(sum(x["d"] * x["u"] * x["p"] for x in xs) / b) if b else None
    inv["descuento_medio_total"] = desc_medio(filas)
    for dim in ("region", "canal", "producto"):
        g2 = defaultdict(list)
        for x in filas:
            g2[x[dim]].append(x)
        inv[f"descuento_medio_{dim}"] = {k: desc_medio(v) for k, v in g2.items()}
    inv["canal_semestre_por_region"] = {r: semestres([x for x in filas if x["region"] == r], "canal")
                                        for r in sorted({x["region"] for x in filas})}
    inv["clientes_por_region"] = dict(Counter(r for _, r in {(x["id_cliente"], x["region"]) for x in filas}))
    inv["desc_mayor15_por_canal"] = dict(Counter(x["canal"] for x in filas if x["d"] > 15))
    return inv


def bloque(filas):
    """Agregados que el dashboard recalcula por región."""
    prod = por(filas, "producto")
    return {"kpis": kpis(filas), "mensual": mensual(filas), "canal": por(filas, "canal"),
            "categoria": por(filas, "categoria"), "top_productos": dict(list(prod.items())[:5])}


def analizar():
    crudas, calidad = limpiar()
    filas = preparar(crudas)
    k = kpis(filas)
    mens = mensual(filas)
    prod = por(filas, "producto")
    clientes, seg, dist = rfm(filas)
    regiones = por(filas, "region")
    res = {
        "generado": dt.date.today().isoformat(),
        "calidad": calidad,
        "kpis": k,
        "mensual": mens,
        "region": regiones,
        "ciudad": por(filas, "ciudad"),
        "canal": por(filas, "canal"),
        "categoria": por(filas, "categoria"),
        "producto": prod,
        "top5": list(prod.items())[:5],
        "bottom5": list(prod.items())[-5:][::-1],
        "semestres": {d: semestres(filas, d) for d in ("region", "canal", "categoria", "producto")},
        "semestre_total": semestres([{**x, "t": "Total"} for x in filas], "t")["Total"],
        "canal_por_region": {r: por([x for x in filas if x["region"] == r], "canal") for r in regiones},
        "mensual_por_region": {r: mensual([x for x in filas if x["region"] == r]) for r in regiones},
        "rfm_segmentos": seg,
        "rfm_distribucion": dist,
        "rfm_total_clientes": len(clientes),
        "rfm_por_region": {r: dict(Counter(c["segmento"] for c in clientes if c["region"] == r))
                           for r in regiones},
        "descuentos": escenarios_descuento(filas),
        "dashboard": {"Todas": bloque(filas),
                      **{r: bloque([x for x in filas if x["region"] == r]) for r in regiones}},
    }
    for r in regiones:
        res["dashboard"][r]["rfm"] = res["rfm_por_region"][r]
    res["dashboard"]["Todas"]["rfm"] = {s: seg[s]["clientes"] for s in ORDEN_SEG}
    # Riesgo: clientes en riesgo, top por monto
    en_riesgo = sorted([c for c in clientes if c["segmento"] == "En riesgo"], key=lambda c: -c["monto"])
    res["en_riesgo_top10"] = en_riesgo[:10]
    ids_riesgo = {c["id_cliente"] for c in en_riesgo}
    fr = [x for x in filas if x["id_cliente"] in ids_riesgo]
    res["en_riesgo_por_canal"] = por(fr, "canal")
    res["en_riesgo_por_region"] = por(fr, "region")
    res["en_riesgo_top20_ventas"] = r2(sum(c["monto"] for c in en_riesgo[:20]))
    res["investigaciones"] = investigar(filas)
    with open(RAIZ / "informes" / "rfm_clientes.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(clientes[0].keys()))
        w.writeheader()
        w.writerows(clientes)
    return res, filas


def comprobaciones(res):
    k = res["kpis"]
    errores = []
    for dim in ("region", "canal", "categoria", "producto"):
        s = sum(v["ventas"] for v in res[dim].values())
        if abs(s - k["ventas_netas"]) > 0.05:
            errores.append(f"suma {dim} {s} != {k['ventas_netas']}")
        p = sum(v["participacion_pct"] for v in res[dim].values())
        if abs(p - 100) > 0.1:
            errores.append(f"participación {dim} suma {p}")
    if abs(sum(m["ventas"] for m in res["mensual"]) - k["ventas_netas"]) > 0.05:
        errores.append("suma mensual no cuadra")
    if sum(s["clientes"] for s in res["rfm_segmentos"].values()) != res["rfm_total_clientes"]:
        errores.append("segmentos RFM no suman el total")
    if res["rfm_total_clientes"] != k["clientes_activos"]:
        errores.append("clientes RFM != clientes activos")
    c = res["calidad"]
    if c["filas_originales"] - sum(c["eliminadas_por_motivo"].values()) != c["filas_finales"]:
        errores.append("conteo de limpieza no cuadra")
    return errores


# --------------------------------------------------------------------------- Pasos 5-7 texto
def usd(x):
    return f"USD {x:,.2f}"


def pc(x):
    return "n/d" if x is None else f"{x:.2f} %"


def region_recomendada(res):
    """Región con mayor crecimiento S2 vs S1 entre las que tienen margen >= margen global - 1 pp."""
    sem, reg, m = res["semestres"]["region"], res["region"], res["kpis"]["margen_pct"]
    cand = [r for r in sem if reg[r]["margen_pct"] >= m - 1]
    return max(cand, key=lambda r: sem[r]["variacion_pct"])


def respuestas(res):
    k = res["kpis"]
    sem = res["semestres"]
    inv = res["investigaciones"]
    reg = res["region"]
    # P1: región con mayor crecimiento S2 vs S1 entre las que tienen margen >= margen global - 1 pp
    r1 = region_recomendada(res)
    r_mas = max(sem["region"], key=lambda r: sem["region"][r]["variacion_pct"])
    r_grande = max(reg, key=lambda r: reg[r]["ventas"])
    r_margen = max(reg, key=lambda r: reg[r]["margen_pct"])
    p1 = (f"{r1}. Es la región con mayor crecimiento S2 vs S1 ({pc(sem['region'][r1]['variacion_pct'])}: "
          f"{usd(sem['region'][r1]['S1'])} a {usd(sem['region'][r1]['S2'])}) entre las que mantienen un margen "
          f"cercano al promedio ({pc(reg[r1]['margen_pct'])} frente a {pc(k['margen_pct'])} global). "
          f"Tiene solo {inv['clientes_por_region'][r1]} clientes y {pc(reg[r1]['participacion_pct'])} de las ventas, así que "
          f"hay espacio para crecer; su canal Online pasó de {usd(inv['canal_semestre_por_region'][r1]['Online']['S1'])} a "
          f"{usd(inv['canal_semestre_por_region'][r1]['Online']['S2'])}.")
    if r_mas != r1:
        p1 += (f" {r_mas} crece más ({pc(sem['region'][r_mas]['variacion_pct'])}) pero sobre una base pequeña "
               f"({usd(reg[r_mas]['ventas'])}) y con el margen más bajo ({pc(reg[r_mas]['margen_pct'])}, descuento medio "
               f"{pc(inv['descuento_medio_region'][r_mas])} y "
               f"{pc(res['canal_por_region'][r_mas]['Mayorista']['participacion_pct'])} de sus ventas por Mayorista): "
               f"no conviene invertir ahí sin antes corregir precios y descuentos.")
    p1 += (f" {r_grande} sigue siendo la mayor ({pc(reg[r_grande]['participacion_pct'])}) pero casi no crece "
           f"({pc(sem['region'][r_grande]['variacion_pct'])}); {r_margen} tiene el mejor margen "
           f"({pc(reg[r_margen]['margen_pct'])}) y debe protegerse.")
    # P2: producto que más cae y producto de menor margen
    pr = sem["producto"]
    pcae = min(pr, key=lambda x: pr[x]["variacion_pct"])
    pm = min(res["producto"], key=lambda x: res["producto"][x]["margen_pct"])
    p2 = (f"Revisar «{pcae}»: sus ventas cayeron {pc(abs(pr[pcae]['variacion_pct']))} entre S1 ({usd(pr[pcae]['S1'])}) y "
          f"S2 ({usd(pr[pcae]['S2'])}).")
    if pcae == "Gaseosa cola 3L":
        gm = inv["gaseosa_por_mes"]
        gc = inv["gaseosa_semestre_canal"]
        p2 += (f" La caída es abrupta desde julio (líneas de pedido por mes ene-jun: {', '.join(map(str, gm['lineas'][:6]))}; "
               f"jul-dic: {', '.join(map(str, gm['lineas'][6:]))}) y ocurre en Tienda física ({pc(gc['Tienda física']['variacion_pct'])}) "
               f"y Mayorista ({pc(gc['Mayorista']['variacion_pct'])}), no en Online ({pc(gc['Online']['variacion_pct'])}). "
               f"Un corte tan brusco sugiere un problema de abastecimiento o de listado más que de demanda: "
               f"hay que verificarlo antes de decidir descontinuarlo.")
    b0 = res["bottom5"][0]
    p2 += (f" Además, «{pm}» tiene el margen más bajo ({pc(res['producto'][pm]['margen_pct'])} frente a "
           f"{pc(k['margen_pct'])}); conviene revisar su precio o costo. No se recomienda descontinuar el producto con "
           f"menos ventas («{b0[0]}», {usd(b0[1]['ventas'])}) porque su margen es {pc(b0[1]['margen_pct'])}.")
    # P3 canal
    cs = sem["canal"]
    c1 = max(cs, key=lambda c: cs[c]["variacion_pct"])
    cc = min(cs, key=lambda c: cs[c]["variacion_pct"])
    p3 = (f"Potenciar {c1}: creció {pc(cs[c1]['variacion_pct'])} (de {usd(cs[c1]['S1'])} en S1 a {usd(cs[c1]['S2'])} "
          f"en S2), crece en las cuatro regiones y tiene buen margen ({pc(res['canal'][c1]['margen_pct'])}). "
          f"En paralelo, {cc} cayó {pc(abs(cs[cc]['variacion_pct']))} y sigue siendo el canal más grande "
          f"({pc(res['canal'][cc]['participacion_pct'])}) y de mayor margen ({pc(res['canal'][cc]['margen_pct'])}): hay que "
          f"entender si sus clientes se están pasando a {c1} (canibalización) o se están perdiendo. Mayorista tiene "
          f"el margen más bajo ({pc(res['canal']['Mayorista']['margen_pct'])}) por su descuento medio de "
          f"{pc(inv['descuento_medio_canal']['Mayorista'])}.")
    # P4 en riesgo
    sr = res["rfm_segmentos"]["En riesgo"]
    rc = res["en_riesgo_por_canal"]
    rr = res["en_riesgo_por_region"]
    rmax = max(rr, key=lambda r: rr[r]["ventas"])
    cmax = max(rc, key=lambda c: rc[c]["ventas"])
    p4 = (f"Son {sr['clientes']} clientes que suman {usd(sr['ventas'])} ({pc(sr['participacion_pct'])} de las ventas) y "
          f"llevan en promedio {sr['recencia_media']:.2f} días sin comprar. Los 20 de mayor monto concentran "
          f"{usd(res['en_riesgo_top20_ventas'])}: priorizarlos con llamada del vendedor y oferta personalizada "
          f"(listado en informes/rfm_clientes.csv). Por región, {rmax} concentra {pc(rr[rmax]['participacion_pct'])} de "
          f"sus compras; por canal, compraban sobre todo en {cmax} ({pc(rc[cmax]['participacion_pct'])}), el canal que "
          f"más cae en S2. Usar descuentos de hasta 15 % (no mayores, ver pregunta 5) y medir reactivación a 60 días.")
    d = res["descuentos"]
    dc = inv["desc_mayor15_por_canal"]
    p5 = (f"Hay {d['lineas_afectadas']} líneas con descuento mayor a 15 % ({usd(d['ventas_afectadas'])} en ventas, "
          f"margen {pc(d['margen_pct_afectadas'])}; por canal: " + ", ".join(f"{c} {n}" for c, n in dc.items()) + "). "
          f"Escenario A (supuesto: esas ventas se mantienen con descuento de 15 %): ventas "
          f"{usd(d['A_tope_15']['ventas'])}, margen {usd(d['A_tope_15']['margen'])} ({pc(d['A_tope_15']['margen_pct'])}), "
          f"es decir {usd(d['A_tope_15']['delta_margen'])} más de margen que hoy ({usd(d['base']['margen'])}, "
          f"{pc(d['base']['margen_pct'])}). Escenario B (supuesto: esas ventas se pierden): ventas "
          f"{usd(d['B_se_pierden']['ventas'])}, margen {usd(d['B_se_pierden']['margen'])} "
          f"({pc(d['B_se_pierden']['margen_pct'])}); el margen % sube pero el margen en dólares cae "
          f"{usd(-d['B_se_pierden']['delta_margen'])}. Conclusión: limitar a 15 % solo conviene si la mayoría de esos "
          f"clientes (sobre todo mayoristas) sigue comprando; probarlo primero con un grupo piloto.")
    return [("¿Qué región merece más inversión el próximo año y por qué?", p1),
            ("¿Qué producto conviene revisar o descontinuar?", p2),
            ("¿Qué canal potenciar?", p3),
            ("¿Qué hacer con los clientes en riesgo?", p4),
            ("¿Qué pasaría con el margen si se eliminan los descuentos mayores al 15 %?", p5)]


def resumen_ejecutivo(res):
    k = res["kpis"]
    st = res["semestre_total"]
    m = res["mensual"]
    orden = sorted(m, key=lambda x: -x["ventas"])
    cs = res["semestres"]["canal"]
    pr = res["semestres"]["producto"]
    pcae = min(pr, key=lambda x: pr[x]["variacion_pct"])
    seg = res["rfm_segmentos"]
    d = res["descuentos"]
    c1 = max(cs, key=lambda c: cs[c]["variacion_pct"])
    r1 = region_recomendada(res)
    return [
        f"Qué pasó: ventas netas de {usd(k['ventas_netas'])} con margen bruto de {usd(k['margen_bruto'])} "
        f"({pc(k['margen_pct'])}), {k['pedidos']} pedidos y {k['clientes_activos']} clientes; S2 creció "
        f"{pc(st['variacion_pct'])} sobre S1. Picos en {orden[0]['nombre']} ({usd(orden[0]['ventas'])}) y "
        f"{orden[1]['nombre']} ({usd(orden[1]['ventas'])}).",
        f"Cambio de canal: Online creció {pc(cs['Online']['variacion_pct'])} en S2 mientras Tienda física cayó "
        f"{pc(abs(cs['Tienda física']['variacion_pct']))}; Online ya pesa {pc(res['canal']['Online']['participacion_pct'])} "
        f"de las ventas del año.",
        f"Qué preocupa: «{pcae}» cayó {pc(abs(pr[pcae]['variacion_pct']))} en S2 frente a S1, y {seg['En riesgo']['clientes']} "
        f"clientes en riesgo concentran {usd(seg['En riesgo']['ventas'])} ({pc(seg['En riesgo']['participacion_pct'])}).",
        f"Dependencia: {seg['Campeones']['clientes']} clientes Campeones generan {pc(seg['Campeones']['participacion_pct'])} "
        f"de las ventas; las líneas con descuento > 15 % dejan solo {pc(d['margen_pct_afectadas'])} de margen.",
        f"Qué hacer: invertir en el canal {c1} y en la región {r1}, investigar la caída de {pcae}, "
        "reactivar a los clientes en riesgo y pilotear un tope de descuento de 15 % en Mayorista.",
    ]


def tabla(encabezado, filas):
    out = ["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
    out += ["| " + " | ".join(str(c) for c in f) + " |" for f in filas]
    return "\n".join(out)


def tabla_dim(d):
    return tabla(["Valor", "Ventas netas", "Margen USD", "Margen %", "Participación %", "Pedidos"],
                 [[k, usd(v["ventas"]), usd(v["margen"]), pc(v["margen_pct"]), pc(v["participacion_pct"]),
                   v["pedidos"]] for k, v in d.items()])


def generar_informe(res):
    k, c = res["kpis"], res["calidad"]
    inv = res["investigaciones"]
    L = []
    A = L.append
    A("# Informe de ventas 2025 – Distribuidora Pacífico S.A.\n")
    A(f"Generado por `scripts/analisis.py` el {res['generado']}. Todas las cifras salen de ese script "
      "(también en `informes/resultados.json`). Montos en USD con 2 decimales (separador de miles «,», decimal «.»).\n")
    A("## 1. Resumen ejecutivo\n")
    for b in resumen_ejecutivo(res):
        A(f"- {b}")
    A("\n## 2. Calidad de datos\n")
    A(f"- Filas en `datos/ventas_2025.csv`: **{c['filas_originales']}** (archivo original sin modificar).")
    A(f"- Duplicados exactos (las 12 columnas idénticas): **{c['duplicados_exactos']}**.")
    A("- Celdas vacías por columna: " + ", ".join(f"{col} = {n}" for col, n in c["vacios_por_columna"].items() if n)
      + " (resto de columnas: 0; ninguna fila tiene ambas vacías).")
    A(f"- Unidades negativas o cero (tras quitar duplicados): **{c['unidades_negativas_o_cero']}**.")
    A(f"- Fechas que no cumplen AAAA-MM-DD: **{len(c['fechas_mal_formato'])}** ({', '.join(c['fechas_mal_formato'])}).\n")
    A("**Reglas de limpieza exactas (aplicadas en este orden):**\n")
    A("1. Duplicados exactos: se compara la fila completa (12 columnas, texto tal cual); se conserva la primera aparición.")
    A("2. Se elimina la fila si `unidades` o `precio_unitario` está vacío (no se imputa).")
    A("3. Se elimina la fila si `unidades` ≤ 0 (no hay columna que identifique devoluciones ni el pedido original, "
      "así que no se tratan como devolución).")
    A("4. Fechas que no cumplen AAAA-MM-DD se corrigen solo si el formato es inequívoco: `AAAA.MM.DD` o `AAAA/MM/DD` → "
      "AAAA-MM-DD; `DD/MM/AAAA` → AAAA-MM-DD solo si el día es > 12. Si fuera ambigua o inválida se eliminaría "
      "(no hubo casos). Fechas corregidas:")
    for f in c["fechas_corregidas"]:
        A(f"   - {f['id_pedido']}: «{f['original']}» → {f['corregida']}")
    A("5. No se modifican precios, descuentos ni costos (se revisaron los rangos por producto y no hay valores atípicos).\n")
    A(tabla(["Motivo", "Filas eliminadas"], [[m, n] for m, n in c["eliminadas_por_motivo"].items()]
            + [["**Total eliminadas**", f"**{c['filas_eliminadas_total']}**"]]))
    A(f"\nFilas antes: **{c['filas_originales']}** → filas después: **{c['filas_finales']}** "
      f"(`datos/ventas_limpias.csv`). Tras la limpieza cada fila tiene un `id_pedido` único "
      f"({c['ids_pedido_unicos_finales']}), por eso nº de pedidos = nº de filas.\n")
    A("## 3. KPIs\n")
    A(tabla(["KPI", "Valor"], [
        ["Ventas netas", usd(k["ventas_netas"])], ["Costo total", usd(k["costo_total"])],
        ["Margen bruto", usd(k["margen_bruto"])], ["Margen %", pc(k["margen_pct"])],
        ["Pedidos (id_pedido únicos)", k["pedidos"]], ["Ticket promedio (ventas / pedidos)", usd(k["ticket_promedio"])],
        ["Clientes activos", k["clientes_activos"]], ["Unidades vendidas", k["unidades"]],
        ["Descuento medio ponderado por venta bruta", pc(inv["descuento_medio_total"])]]))
    A("\nFórmulas: ventas netas = unidades × precio_unitario × (1 − descuento_pct/100); costo = unidades × "
      "costo_unitario; margen = ventas − costo; margen % = margen / ventas. El crecimiento mes a mes está en 4.1.\n")
    A("## 4. Análisis por dimensión\n")
    A("### 4.1 Por mes\n")
    A(tabla(["Mes", "Ventas netas", "Margen %", "Pedidos", "Crecimiento vs mes anterior"],
            [[m["nombre"], usd(m["ventas"]), pc(m["margen_pct"]), m["pedidos"],
              pc(m["crecimiento_pct"]) if m["crecimiento_pct"] is not None else "–"] for m in res["mensual"]]))
    mmax = max(res["mensual"], key=lambda x: x["ventas"])
    mmin = min(res["mensual"], key=lambda x: x["ventas"])
    cm = inv["categoria_por_mes"]
    A(f"\nMes con más ventas: **{mmax['nombre']}** ({usd(mmax['ventas'])}); mes con menos: **{mmin['nombre']}** "
      f"({usd(mmin['ventas'])}). Profundización de los picos: en mayo Cuidado personal vendió "
      f"{usd(cm['Cuidado personal'][4])} y Hogar {usd(cm['Hogar'][4])} (frente a {usd(cm['Cuidado personal'][3])} y "
      f"{usd(cm['Hogar'][3])} en abril); en diciembre suben casi todas las categorías, sobre todo Hogar "
      f"({usd(cm['Hogar'][11])}), Bebidas ({usd(cm['Bebidas'][11])}) y Snacks ({usd(cm['Snacks'][11])}). "
      "Hipótesis (no verificable con estos datos): Día de la Madre en mayo y temporada navideña en diciembre.\n")
    A(f"S1 vs S2 total: {usd(res['semestre_total']['S1'])} → {usd(res['semestre_total']['S2'])} "
      f"({pc(res['semestre_total']['variacion_pct'])}).\n")
    for titulo, dim in (("4.2 Por región", "region"), ("4.3 Por canal", "canal"), ("4.4 Por categoría", "categoria")):
        A(f"### {titulo}\n")
        A(tabla_dim(res[dim]))
        A("\nS1 vs S2:\n")
        A(tabla(["Valor", "S1", "S2", "Variación"], [[n, usd(v["S1"]), usd(v["S2"]), pc(v["variacion_pct"])]
                                                     for n, v in res["semestres"][dim].items()]))
        A("")
        if dim == "region":
            A("Ventas por ciudad:\n")
            A(tabla_dim(res["ciudad"]))
            ci = res["canal_por_region"]["Insular"]["Mayorista"]
            A(f"\nInsular tiene el margen más bajo porque {pc(ci['participacion_pct'])} de sus ventas va por Mayorista "
              f"(margen {pc(ci['margen_pct'])}) y su descuento medio es {pc(inv['descuento_medio_region']['Insular'])} "
              f"(global {pc(inv['descuento_medio_total'])}).\n")
        if dim == "canal":
            A("Ventas mensuales por canal (USD):\n")
            A(tabla(["Canal"] + MESES, [[cn] + [f"{v:,.2f}" for v in vs] for cn, vs in inv["canal_por_mes"].items()]))
            A("\nOnline crece en todas las regiones; Tienda física cae en todas salvo Amazonía (variación S1 → S2):\n")
            A(tabla(["Región", "Online", "Tienda física", "Mayorista"],
                    [[r, pc(v["Online"]["variacion_pct"]), pc(v["Tienda física"]["variacion_pct"]),
                      pc(v["Mayorista"]["variacion_pct"])] for r, v in inv["canal_semestre_por_region"].items()]))
            A("\nDescuento medio ponderado por canal: " + ", ".join(
                f"{n} {pc(v)}" for n, v in inv["descuento_medio_canal"].items())
              + ". Esto explica por qué Mayorista tiene el margen más bajo.\n")
    A("### 4.5 Por producto\n")
    A("**Top 5 por ventas netas**\n")
    A(tabla(["Producto", "Ventas netas", "Margen %", "Participación %"],
            [[n, usd(v["ventas"]), pc(v["margen_pct"]), pc(v["participacion_pct"])] for n, v in res["top5"]]))
    A("\n**Bottom 5 por ventas netas** (de menor a mayor)\n")
    A(tabla(["Producto", "Ventas netas", "Margen %", "Participación %"],
            [[n, usd(v["ventas"]), pc(v["margen_pct"]), pc(v["participacion_pct"])] for n, v in res["bottom5"]]))
    A("\nS1 vs S2 por producto:\n")
    A(tabla(["Producto", "S1", "S2", "Variación"], [[n, usd(v["S1"]), usd(v["S2"]), pc(v["variacion_pct"])]
                                                    for n, v in res["semestres"]["producto"].items()]))
    g = inv["gaseosa_por_mes"]
    A("\nProfundización Gaseosa cola 3L – ventas por mes: " + ", ".join(
        f"{MESES[i]} {usd(g['ventas'][i])}" for i in range(12)) + ". Variación S1→S2 por canal: " + ", ".join(
        f"{n} {pc(v['variacion_pct'])}" for n, v in inv["gaseosa_semestre_canal"].items()) + "; por región: " + ", ".join(
        f"{n} {pc(v['variacion_pct'])}" for n, v in inv["gaseosa_semestre_region"].items()) + ".\n")
    A("## 5. Segmentación RFM\n")
    A("- Fecha de referencia: 2025-12-31. Recencia = días desde la última compra; Frecuencia = nº de `id_pedido` "
      "distintos; Monto = ventas netas del cliente.")
    A(f"- Puntajes 1-5 por quintiles de rango: puntaje = min(5, 1 + ⌊5·k / n⌋), con n = {res['rfm_total_clientes']} "
      "clientes y k = nº de clientes con valor estrictamente peor (en R, peor = más días; en F y M, peor = menor valor). "
      "**Empates**: los clientes con el mismo valor reciben siempre el mismo puntaje (por eso los grupos de F no "
      "tienen el mismo tamaño).")
    A("- Segmentos en orden (gana la primera regla que se cumple): Campeones R≥4 y F≥4; Leales R≥3 y F≥3; "
      "Potenciales R≥3 y F≤2; En riesgo R=2, o R=1 y F≥3; Perdidos R=1 y F≤2. M se calcula pero no interviene.\n")
    dist = res["rfm_distribucion"]
    A("Clientes por puntaje:\n")
    A(tabla(["Puntaje", "R", "F", "M"], [[s, dist["R"].get(str(s), 0), dist["F"].get(str(s), 0), dist["M"].get(str(s), 0)]
                                         for s in range(1, 6)]))
    A("")
    seg = res["rfm_segmentos"]
    A(tabla(["Segmento", "Clientes", "Ventas netas", "% ventas", "Recencia media (días)", "Frecuencia media",
             "Acción comercial"],
            [[s, v["clientes"], usd(v["ventas"]), pc(v["participacion_pct"]), f"{v['recencia_media']:.2f}",
              f"{v['frecuencia_media']:.2f}", v["accion"]] for s, v in seg.items()]))
    A(f"\nComprobación: {' + '.join(str(v['clientes']) for v in seg.values())} = "
      f"{sum(v['clientes'] for v in seg.values())} clientes = clientes activos ({k['clientes_activos']}). "
      "Detalle por cliente en `informes/rfm_clientes.csv`.\n")
    A("## 6. Preguntas de negocio\n")
    for i, (q, a) in enumerate(respuestas(res), 1):
        A(f"**{i}. {q}**\n\n{a}\n")
    A("## 7. Limitaciones\n")
    for t in ["Datos ficticios de un solo año (2025): no hay base para comparar con 2024 ni estacionalidad de años previos.",
              "No hay datos de inventario, marketing, competencia ni devoluciones: las causas propuestas "
              "(quiebre de stock de Gaseosa, Día de la Madre, Navidad, canibalización de canales) son hipótesis.",
              f"Se eliminaron {c['filas_eliminadas_total']} filas "
              f"({pc(100 * c['filas_eliminadas_total'] / c['filas_originales'])} del original); las "
              f"{c['unidades_negativas_o_cero']} con unidades negativas podrían ser devoluciones no registradas como tales.",
              "Los escenarios de descuento son extremos (todo se mantiene o todo se pierde); la realidad estará entre ambos "
              "y no considera efectos en otros productos.",
              "RFM por quintiles de rango: con muchos empates en Frecuencia los grupos no son exactamente iguales.",
              "Cada fila es un pedido de un solo producto, así que el ticket promedio es por línea de pedido."]:
        A(f"- {t}")
    A("")
    INFORME.write_text("\n".join(L), encoding="utf-8")


# --------------------------------------------------------------------------- Paso 8 dashboard
def generar_dashboard(res):
    datos = {
        "porRegion": res["dashboard"],
        "regiones": {r: {"ventas": v["ventas"], "margen_pct": v["margen_pct"]} for r, v in res["region"].items()},
        "segmentos": res["rfm_segmentos"],
        "resumen": resumen_ejecutivo(res),
        "preguntas": [{"p": q, "r": a} for q, a in respuestas(res)],
        "calidad": {"antes": res["calidad"]["filas_originales"], "despues": res["calidad"]["filas_finales"],
                    "motivos": res["calidad"]["eliminadas_por_motivo"]},
        "generado": res["generado"],
    }
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = (RAIZ / "scripts" / "plantilla_dashboard.html").read_text(encoding="utf-8").replace("__DATOS__", js)
    DASHBOARD.parent.mkdir(exist_ok=True)
    DASHBOARD.write_text(html, encoding="utf-8")
    return html


def validar_html(html):
    from html.parser import HTMLParser

    class P(HTMLParser):
        vacias = {"meta", "br", "img", "input", "link", "hr"}

        def __init__(self):
            super().__init__()
            self.pila, self.errores = [], []

        def handle_starttag(self, tag, attrs):
            if tag not in self.vacias:
                self.pila.append(tag)

        def handle_endtag(self, tag):
            if not self.pila or self.pila[-1] != tag:
                self.errores.append(f"cierre inesperado </{tag}>")
            else:
                self.pila.pop()

    p = P()
    p.feed(html)
    ini = html.index('type="application/json">') + len('type="application/json">')
    json.loads(html[ini:html.index("</script>", ini)])   # lanza error si el JSON incrustado no es válido
    return p.errores + ([f"etiquetas sin cerrar: {p.pila}"] if p.pila else [])


if __name__ == "__main__":
    res, filas = analizar()
    errs = comprobaciones(res)
    RESULTADOS.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    res = json.loads(RESULTADOS.read_text(encoding="utf-8"))     # el informe se alimenta del JSON
    generar_informe(res)
    errs += validar_html(generar_dashboard(res))
    k = res["kpis"]
    print("Filas:", res["calidad"]["filas_originales"], "->", res["calidad"]["filas_finales"],
          res["calidad"]["eliminadas_por_motivo"])
    print("KPIs:", json.dumps(k, ensure_ascii=False))
    print("Semestres canal:", res["semestres"]["canal"])
    print("Semestres región:", res["semestres"]["region"])
    print("Segmentos:", {s: v["clientes"] for s, v in res["rfm_segmentos"].items()})
    print("Descuentos:", {e: res["descuentos"][e] for e in ("base", "A_tope_15", "B_se_pierden")})
    print("Archivos:", LIMPIO, RESULTADOS, INFORME, DASHBOARD, sep="\n  ")
    print("COMPROBACIONES:", "OK" if not errs else errs)
