# Exposición Acústica – Pipeline de Procesamiento

Evaluación de la exposición acústica diaria en un dormitorio mediante integración numérica del nivel equivalente continuo de ruido (LAeq) y análisis complementario. Este proyecto implementa un pipeline reproducible para transformar señales en dB a intensidad, aplicar métodos de integración, estimar errores y exportar resultados y gráficos.

---

## Tabla de contenidos
- Descripción general
- Estructura del proyecto
- Requisitos e instalación
- Datos de entrada y formatos
- Pipeline: etapas y salidas
- Uso (CLI / script principal)
- Módulos y funciones principales
- Resultados, gráficos y artefactos
- Registro (logging) y trazabilidad
- Manejo de errores
- Desarrollo y pruebas
- Licencia

---

## Descripción general
El pipeline lee datos de ruido (dB) muestreados en el tiempo, aplica transformaciones y cálculos para:
1. Truncar la serie al formato 25 + 6k (estandarización de duraciones/segmentos).
2. Convertir dB a intensidad (W/m²).
3. Integrar numéricamente la señal con varios métodos.
4. Calcular errores respecto a un objetivo, métricas estadísticas y LAeq/dosis.
5. Exportar resultados a CSV y generar gráficos.
6. Repetir el flujo sobre un subconjunto reducido (80%).

La trazabilidad se asegura mediante logging estructurado y docstrings que describen entradas, salidas y supuestos.

---

## Estructura del proyecto
```
exposicion-acustica/
├─ data/
│  ├─ datos.csv                 # Entrada principal con la serie en dB
│  └─ resultados/               # Artefactos generados por el pipeline
├─ src/
│  ├─ graphics/
│  │  ├─ __init__.py
│  │  └─ viewer.py             # plot_and_save: visualización y guardado de gráficos
│  ├─ integration/
│  │  ├─ __init__.py
│  │  ├─ analize.py            # Análisis adicionales (si aplica)
│  │  ├─ calculations.py       # Métodos de integración numérica
│  │  ├─ dB_to_intensity.py    # Conversión dB -> intensidad
│  │  ├─ errors.py             # Cálculo de errores
│  │  ├─ metods.py             # Orquestación/definiciones de métodos
│  │  └─ statisticists.py      # Estadísticos descriptivos
│  ├─ io/
│  │  ├─ __init__.py
│  │  ├─ exportCSV.py          # Exportación de CSV
│  │  └─ read.py               # Lectura robusta de CSV
│  └─ utils/
│     ├─ __init__.py
│     ├─ acustic.py            # Utilidades acústicas
│     ├─ geojson_to_csv.py     # Conversión auxiliar (GIS -> CSV)
│     ├─ remove_percentage.py  # Reducción homogénea por porcentaje
│     ├─ transforms.py         # Transformaciones varias
│     ├─ truncate.py           # Truncado 25 + 6k
│     └─ validations.py        # Validaciones de entradas
├─ main.py                      # Pipeline orquestado con logging y manejo de errores
├─ pyproject.toml               # Configuración del proyecto/paquetes
├─ README.md                    # Este documento
└─ LICENSE
```

---

## Requisitos e instalación
- Python 3.10+
- Dependencias principales:
  - polars
  - numpy
  - matplotlib (o librería de visualización utilizada por `viewer.py`)

Instalación recomendada (entorno virtual):
```
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install -e .
```
O bien:
```
pip install polars numpy matplotlib
```

Las dependencias exactas pueden consultarse en `pyproject.toml`.

---

## Datos de entrada y formatos
Archivo esperado: `data/datos.csv`
- Debe contener al menos la columna: `leq_mean` (nivel en dB por muestra).
- Se asume un paso de muestreo constante (dt = 1.0 s por defecto, ajustable en funciones que lo acepten).

El pipeline genera múltiples artefactos bajo `data/resultados/`.

---

## Pipeline: etapas y salidas
Flujo orquestado en `main.py`:
1) Truncado 25 + 6k
- Entrada: `data/datos.csv` (columna `leq_mean`).
- Salida: `data/resultados/truncado_25_6k.csv`.

2) Serie completa
- Conversión dB -> intensidad.
- Salidas:
  - `intensidad_completa.csv`
  - Resultados de integración: `resultados_completos.csv`
  - Estadísticos: `estadisticos_completos.csv`
  - Gráficos: `grafico_completo_*.png` (según implementación)
  - LAeq y dosis: `laeq_dosis_completo.csv`

3) Reducción al 80%
- Reducción homogénea desde el truncado 25 + 6k.
- Conversión y análisis análogo a la serie completa.
- Salidas:
  - `intensidad_reducido_80.csv`
  - `resultados_reducido_80.csv`
  - `estadisticos_reducido_80.csv`
  - `grafico_reducido_80_*.png`
  - `laeq_dosis_reducido_80.csv`

---

## Uso (CLI / script principal)
Desde la raíz del proyecto:
```
python main.py
```
Parámetros como rutas, nombre de columna o dt se encuentran dentro de `main.py` y/o en las funciones llamadas. Para personalizarlos, editar el script o exponer nuevos argumentos.

---

## Módulos y funciones principales
A continuación se listan los puntos de entrada más relevantes utilizados por el pipeline:

- src/io
  - read.py: `leer_csv(path: str) -> polars.DataFrame`
  - exportCSV.py: `exportar_resultados(resultados: dict, errores: dict, path: str)`, `exportar_estadisticos(estadisticos: dict, path: str)`

- src/utils
  - truncate.py: `truncar_a_25_6k(path: str, columna_y: str, output_path: str)`
  - remove_percentage.py: `quitar_porcentaje_homogeneo(path: str, columna_y: str, porcentaje: float, output_path: str)`
  - acustic.py / transforms.py: utilidades auxiliares

- src/integration
  - dB_to_intensity.py: `db_a_intensidad(y_db: np.ndarray) -> np.ndarray`
  - calculations.py / metods.py: `calcular_metodos_integracion(t: np.ndarray, y: np.ndarray) -> dict`
  - errors.py: `calcular_errores(resultados: dict, objetivo_w_m2: float) -> dict`
  - statisticists.py: `calcular_estadisticos(y: np.ndarray) -> dict`
  - analize.py: utilidades de análisis
  - `calcular_laeq_y_dosis(path_csv: str, columna_intensidad: str, dt: float, output_path: str)`

- src/graphics
  - viewer.py: `plot_and_save(t: np.ndarray, y: np.ndarray, resultados: dict, prefix: str)`

- main.py
  - `main()`: orquesta todo el flujo; incluye logging y manejo de errores.

Cada función debe contar con docstrings que indiquen parámetros, retornos y posibles excepciones.

---

## Resultados, gráficos y artefactos
Los CSV y gráficos se generan en `data/resultados/`. Nombres típicos:
- Intensidad: `intensidad_completa.csv`, `intensidad_reducido_80.csv`
- Integración: `resultados_completos.csv`, `resultados_reducido_80.csv`
- Estadísticos: `estadisticos_completos.csv`, `estadisticos_reducido_80.csv`
- LAeq/dosis: `laeq_dosis_completo.csv`, `laeq_dosis_reducido_80.csv`
- Gráficos: `grafico_completo_*`, `grafico_reducido_80_*`

Ajuste de nombres y rutas puede realizarse modificando `main.py` o las funciones de exportación.

---

## Registro (logging) y trazabilidad
El pipeline emplea `logging` con formato:
```
%(asctime)s - %(levelname)s - %(name)s - %(message)s
```
Niveles:
- INFO: etapas del flujo, rutas de salida y operaciones clave.
- DEBUG: metadatos detallados (p. ej., columnas y tamaño de DataFrames).
- ERROR/EXCEPTION: fallo del pipeline con traza.

Para activar DEBUG global:
```
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

---

## Manejo de errores
- `main()` encapsula el flujo en un bloque try/except y registra cualquier excepción con `logger.exception`, re-lanzándola para visibilidad en ejecución por lotes o CI.
- Funciones de E/S y cálculo deberían validar precondiciones (columnas requeridas, arrays no vacíos, tipos) y emitir errores descriptivos.

Recomendaciones:
- Validar que `data/datos.csv` existe y contiene `leq_mean`.
- Confirmar permisos de escritura en `data/resultados/`.
- Verificar que las dependencias están instaladas y versiones compatibles.

---

## Desarrollo y pruebas
Sugerencias para ampliar la calidad del proyecto:
- Añadir pruebas unitarias (pytest) para funciones de integración, errores y utilidades.
- Añadir validaciones de esquema (pydantic o pandera) para archivos de entrada.
- Integración continua (GitHub Actions) para ejecutar linting (ruff/flake8) y tests.
- Tipado estático (mypy/pyright) para mejorar mantenibilidad.

---

## Licencia
Este proyecto se distribuye bajo la licencia incluida en `LICENSE`.
