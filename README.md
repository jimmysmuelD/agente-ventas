# Agente Analista de Ventas con Claude Code

Proyecto universitario de **Analítica de Negocios**: un agente de IA, construido con Claude Code,
que analiza las ventas de una empresa, verifica sus propias cifras con un segundo agente y
entrega un informe y un dashboard web.

> ⚠️ **Los datos son ficticios.** "Distribuidora Pacífico S.A." no existe; las ventas se generan con
> `scripts/generar_datos.py` (semilla fija 42) con fines académicos.

## Problema de negocio
Distribuidora Pacífico S.A. (Ecuador, consumo masivo y hogar, USD) tiene un año de ventas (2025)
en un CSV con errores de calidad. La gerencia necesita saber qué pasó, qué preocupa y qué hacer:
qué región merece inversión, qué producto revisar, qué canal potenciar, qué hacer con los
clientes en riesgo y cómo afectan los descuentos al margen. Hacerlo a mano toma días y es
propenso a errores; el agente lo hace en minutos y cada cifra se verifica de forma independiente.

## Qué hace el agente
1. Revisa la calidad de los datos (duplicados, vacíos, negativos, fechas mal escritas) y crea una copia limpia.
2. Calcula KPIs: ventas netas, costo, margen bruto, pedidos, ticket promedio, clientes activos, crecimiento.
3. Analiza por mes, región, canal, categoría y producto (top 5 / bottom 5).
4. Segmenta clientes con RFM (Campeones, Leales, Potenciales, En riesgo, Perdidos).
5. Responde 5 preguntas de negocio con datos.
6. Escribe `informes/informe_ventas.md` y el dashboard `docs/index.html`.
7. Un segundo agente recalcula las cifras y escribe `informes/verificacion.md`.

## Arquitectura

```
Usuario
  │  "Analiza las ventas de datos/ventas_2025.csv"
  ▼
Sesión principal de Claude Code  (coordina según CLAUDE.md)
  │
  ├──► Subagente analista-ventas
  │       ├─ skill: manual-analisis-ventas (pasos + checklist)
  │       ├─ memoria: memoria/aprendizajes.md
  │       └─ scripts/analisis.py → informe_ventas.md + docs/index.html
  │
  ├──► Subagente verificador-cifras
  │       └─ scripts/verificar.py (recalcula desde el CSV original) → verificacion.md
  │
  │   ¿hay ERROR? → vuelve al analista (máximo 2 rondas)
  ▼
Informe + dashboard verificados → resumen al usuario
```

En Claude Code un subagente no puede llamar a otro; por eso la sesión principal hace de
orquestador siguiendo el flujo escrito en `CLAUDE.md`.

## Estructura de carpetas

```
.
├── CLAUDE.md                     # guía del proyecto y flujo multiagente
├── README.md
├── .gitignore
├── .claude/
│   ├── agents/
│   │   ├── analista-ventas.md    # subagente que analiza
│   │   └── verificador-cifras.md # subagente que verifica
│   └── skills/
│       └── manual-analisis-ventas/
│           └── SKILL.md          # manual (playbook) de análisis
├── datos/
│   └── ventas_2025.csv           # datos ficticios con errores intencionales
├── scripts/
│   └── generar_datos.py          # genera el CSV (solo librería estándar)
├── memoria/
│   └── aprendizajes.md           # memoria del agente entre sesiones
├── informes/                     # informe_ventas.md y verificacion.md
└── docs/                         # index.html (dashboard, GitHub Pages)
```

## Cómo reproducirlo paso a paso
1. Instala **Visual Studio Code**: https://code.visualstudio.com
2. Instala **Git**: https://git-scm.com (en Windows también: `winget install -e --id Git.Git`).
3. Instala **Python 3** desde https://www.python.org marcando **"Add Python to PATH"**.
   No hace falta instalar librerías: el proyecto usa solo la librería estándar.
4. En VS Code, abre Extensiones (Ctrl+Shift+X), busca **Claude Code** (de Anthropic) e instálala.
5. Abre el panel de Claude Code e **inicia sesión con tu cuenta de Claude**.
6. Clona o descarga este repositorio y ábrelo con **Archivo → Abrir carpeta**.
7. (Opcional) Regenera los datos: `python scripts/generar_datos.py`
8. En una **sesión nueva** de Claude Code escribe:

   ```
   Analiza las ventas de datos/ventas_2025.csv
   ```

9. Revisa `informes/informe_ventas.md`, `informes/verificacion.md` y abre `docs/index.html`
   en el navegador.

## 5 preguntas de ejemplo para probar el agente
1. ¿Qué región merece más inversión el próximo año y por qué?
2. ¿Qué producto conviene revisar o descontinuar?
3. Segmenta a los clientes con RFM y dime qué hacer con los que están en riesgo.
4. ¿Cómo evolucionó el canal Online durante 2025 comparado con la Tienda física?
5. ¿Qué pasaría con el margen si eliminamos los descuentos mayores al 15 %?

## Dashboard
Dashboard publicado: [ENLACE_DASHBOARD]

(Se publica con GitHub Pages desde la carpeta `docs/`.)

## Relación con los niveles de un agente

| Nivel | Qué es | Dónde está en el proyecto |
|---|---|---|
| Espacio de trabajo | Contexto y reglas que Claude lee siempre | `CLAUDE.md` |
| Agente | Especialista con rol, herramientas e instrucciones propias | `.claude/agents/analista-ventas.md` |
| Skill | Procedimiento reutilizable paso a paso con checklist | `.claude/skills/manual-analisis-ventas/SKILL.md` |
| Memoria | Lecciones que persisten entre sesiones | `memoria/aprendizajes.md` |
| Multiagente | Un segundo agente verifica de forma independiente al primero | `.claude/agents/verificador-cifras.md` + flujo en `CLAUDE.md` |
