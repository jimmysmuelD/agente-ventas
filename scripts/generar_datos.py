"""Genera datos/ventas_2025.csv para Distribuidora Pacífico S.A. (datos ficticios).

Solo usa la librería estándar. Semilla fija 42: siempre produce el mismo archivo.
Uso:  python scripts/generar_datos.py
"""
import calendar
import csv
import datetime as dt
import random
from pathlib import Path

SEMILLA = 42
FILAS_BASE = 2985          # + 15 duplicados = 3000 filas
N_CLIENTES = 400
RUTA_SALIDA = Path(__file__).resolve().parent.parent / "datos" / "ventas_2025.csv"

COLUMNAS = ["id_pedido", "fecha", "id_cliente", "region", "ciudad", "canal", "categoria",
            "producto", "unidades", "precio_unitario", "descuento_pct", "costo_unitario"]

CIUDADES = {
    "Costa": ["Guayaquil", "Manta", "Machala"],
    "Sierra": ["Quito", "Cuenca", "Ambato"],
    "Amazonía": ["Tena", "Puyo"],
    "Insular": ["Puerto Ayora"],
}
CLIENTES_POR_REGION = {"Costa": 170, "Sierra": 160, "Amazonía": 40, "Insular": 30}

# categoria, producto, precio de lista, costo unitario, peso de popularidad
PRODUCTOS = [
    ("Bebidas", "Agua mineral 6x1L", 3.50, 2.10, 10),
    ("Bebidas", "Jugo de naranja 1L", 2.20, 1.30, 9),
    ("Bebidas", "Gaseosa cola 3L", 2.80, 1.70, 11),
    ("Snacks", "Galletas integrales", 1.80, 0.95, 9),
    ("Snacks", "Papas fritas 200g", 2.10, 1.15, 9),
    ("Snacks", "Chocolate 100g", 1.90, 1.05, 7),
    ("Limpieza", "Detergente 2kg", 6.50, 4.10, 8),
    ("Limpieza", "Cloro 1L", 1.40, 0.80, 8),
    ("Limpieza", "Desinfectante multiuso", 3.20, 1.90, 6),
    ("Cuidado personal", "Shampoo 400ml", 4.80, 2.70, 6),
    ("Cuidado personal", "Jabón de tocador x3", 2.50, 1.40, 7),
    ("Cuidado personal", "Crema dental 150g", 2.30, 1.30, 7),
    ("Hogar", "Juego de toallas", 18.00, 10.50, 3),
    ("Hogar", "Vajilla 12 piezas", 35.00, 22.00, 2),
    ("Hogar", "Set de ollas", 55.00, 36.00, 2),
]
PRODUCTO_EN_CAIDA = "Gaseosa cola 3L"

# Estacionalidad: pico en mayo (Día de la Madre) y diciembre
PESO_MES = [0.90, 0.80, 0.90, 0.90, 1.40, 1.00, 1.00, 1.00, 1.00, 1.05, 1.15, 1.70]


def pesos_region(mes):
    """Amazonía es pequeña pero crece mes a mes."""
    return {"Costa": 46, "Sierra": 42, "Amazonía": 2 + 1.2 * (mes - 1), "Insular": 3}


def pesos_canal(mes):
    """Online crece mes a mes; Mayorista estable."""
    online = 8 + 3.5 * (mes - 1)
    return {"Tienda física": 100 - 15 - online, "Online": online, "Mayorista": 15}


def peso_producto(prod, mes):
    categoria, nombre, _, _, peso = prod
    if nombre == PRODUCTO_EN_CAIDA and mes >= 7:
        peso *= 0.25
    if mes == 5 and categoria in ("Hogar", "Cuidado personal"):
        peso *= 2.5
    if mes == 12 and categoria in ("Hogar", "Snacks", "Bebidas"):
        peso *= 1.8
    return peso


def crear_clientes(rng):
    clientes = []
    n = 1
    for region, cantidad in CLIENTES_POR_REGION.items():
        for _ in range(cantidad):
            clientes.append({
                "id": f"CLI-{n:04d}",
                "region": region,
                "ciudad": rng.choice(CIUDADES[region]),
                "peso": 1.0,
                "ultimo_mes": 12,
            })
            n += 1
    rng.shuffle(clientes)
    for c in clientes[:20]:            # clientes VIP: compran mucho más
        c["peso"] = 15.0
    for c in clientes[20:70]:          # clientes que dejaron de comprar a mitad de año
        c["ultimo_mes"] = rng.choice([4, 5, 6])
    return clientes


def unidades_para(canal, categoria, rng):
    if categoria == "Hogar":
        return rng.randint(3, 10) if canal == "Mayorista" else rng.randint(1, 3)
    if canal == "Mayorista":
        return rng.randint(10, 40)
    if canal == "Online":
        return rng.randint(1, 8)
    return rng.randint(1, 12)


def descuento_para(canal, rng):
    opciones = {
        "Tienda física": ([0, 5, 10], [60, 25, 15]),
        "Online": ([0, 5, 10, 15, 20], [35, 25, 20, 12, 8]),
        "Mayorista": ([10, 15, 20, 25], [35, 30, 22, 13]),
    }
    valores, pesos = opciones[canal]
    return rng.choices(valores, pesos)[0]


def elegir(rng, pesos):
    claves = list(pesos)
    return rng.choices(claves, [pesos[k] for k in claves])[0]


def generar_filas(rng, clientes):
    total_peso = sum(PESO_MES)
    pedidos_mes = [round(FILAS_BASE * p / total_peso) for p in PESO_MES]
    pedidos_mes[-1] += FILAS_BASE - sum(pedidos_mes)

    filas = []
    for mes, cantidad in enumerate(pedidos_mes, start=1):
        dias_mes = calendar.monthrange(2025, mes)[1]
        for _ in range(cantidad):
            region = elegir(rng, pesos_region(mes))
            candidatos = [c for c in clientes if c["region"] == region and c["ultimo_mes"] >= mes]
            cliente = rng.choices(candidatos, [c["peso"] for c in candidatos])[0]
            canal = elegir(rng, pesos_canal(mes))
            prod = rng.choices(PRODUCTOS, [peso_producto(p, mes) for p in PRODUCTOS])[0]
            categoria, nombre, precio_lista, costo, _ = prod
            fecha = dt.date(2025, mes, rng.randint(1, dias_mes))
            filas.append({
                "fecha": fecha.isoformat(),
                "id_cliente": cliente["id"],
                "region": region,
                "ciudad": cliente["ciudad"],
                "canal": canal,
                "categoria": categoria,
                "producto": nombre,
                "unidades": unidades_para(canal, categoria, rng),
                "precio_unitario": f"{precio_lista * rng.uniform(0.97, 1.03):.2f}",
                "descuento_pct": descuento_para(canal, rng),
                "costo_unitario": f"{costo:.2f}",
            })

    filas.sort(key=lambda f: f["fecha"])
    for i, fila in enumerate(filas, start=1):
        fila["id_pedido"] = f"PED-{i:05d}"
    return filas


def introducir_errores(rng, filas):
    """Errores de calidad intencionales, en filas distintas entre sí."""
    indices = rng.sample(range(len(filas)), 15 + 20 + 3 + 2)
    i_dup, i_vacio = indices[:15], indices[15:35]
    i_neg, i_fecha = indices[35:38], indices[38:40]

    for k, i in enumerate(i_vacio):                     # 20 celdas vacías
        filas[i]["unidades" if k % 2 == 0 else "precio_unitario"] = ""
    for i in i_neg:                                     # 3 unidades negativas
        filas[i]["unidades"] = -abs(int(filas[i]["unidades"]))
    año, mes, dia = filas[i_fecha[0]]["fecha"].split("-")
    filas[i_fecha[0]]["fecha"] = f"{dia}/{mes}/{año}"   # formato DD/MM/AAAA
    año, mes, dia = filas[i_fecha[1]]["fecha"].split("-")
    filas[i_fecha[1]]["fecha"] = f"{año}.{mes}.{dia}"   # formato AAAA.MM.DD

    # 15 duplicados exactos, insertados justo después de la fila original
    originales = [filas[i] for i in i_dup]
    resultado = []
    for fila in filas:
        resultado.append(fila)
        if any(fila is o for o in originales):
            resultado.append(dict(fila))
    return resultado


def main():
    rng = random.Random(SEMILLA)
    clientes = crear_clientes(rng)
    filas = introducir_errores(rng, generar_filas(rng, clientes))
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_SALIDA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"Archivo creado: {RUTA_SALIDA} ({len(filas)} filas)")


if __name__ == "__main__":
    main()
