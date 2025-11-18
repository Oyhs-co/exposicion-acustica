"""
Pipeline principal para el procesamiento de datos acústicos.

Este módulo orquesta el flujo de trabajo de extremo a extremo:
- Lectura y transformación de datos (truncado al formato 25 + 6k, reducción porcentual).
- Conversión dB a intensidad.
- Cálculo de integrales numéricas, errores y estadísticos.
- Exportación de resultados y generación de gráficos.
- Cálculo de LAeq y dosis.

Incluye registro estructurado (logging) y manejo básico de errores para una
mejor trazabilidad del proceso.
"""
from __future__ import annotations

import logging
from typing import Dict, Any

import polars as pl

# Configuración de logging global
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    filename='data/pipeline.log',
)
logger = logging.getLogger(__name__)

from src.graphics import plot_and_save
from src.io import leer_csv, exportar_resultados, exportar_estadisticos
from src.integration import (
    db_a_intensidad,
    calcular_laeq_y_dosis,
    calcular_errores,
    calcular_estadisticos,
    calcular_metodos_integracion,
    mejor_metodo,
)
from src.utils import quitar_porcentaje_homogeneo, truncar_a_25_6k


def _log_dataframe_info(nombre: str, df: pl.DataFrame) -> None:
    """Registra información básica de un DataFrame para trazabilidad.

    Parámetros:
        nombre: Alias del DataFrame para el log.
        df: DataFrame de polars.
    """
    logger.info("DF %s -> filas=%d, columnas=%d", nombre, df.height, df.width)
    logger.debug("DF %s columnas: %s", nombre, df.columns)


def _exportar_y_graficar(
    df: pl.DataFrame,
    resultados: Dict[str, Any],
    ruta_prefix: str,
    objetivo_w_m2: float,
    ruta_export_resultados: str,
    ruta_export_estadisticos: str,
    ruta_export_laeq_dosis: str,
) -> None:
    """Exporta resultados, estadísticos, grafica series y calcula LAeq/dosis.

    Parámetros:
        df: DataFrame con columnas ["Tiempo (s)", "intensidad"].
        resultados: Diccionario de resultados de métodos de integración.
        ruta_prefix: Prefijo para nombres de gráficos.
        objetivo_w_m2: Valor objetivo para cálculo de errores.
        ruta_export_resultados: Ruta CSV para resultados completos.
        ruta_export_estadisticos: Ruta CSV para estadísticos completos.
        ruta_export_laeq_dosis: Ruta CSV para LAeq y dosis.
    """
    logger.info("Exportando resultados a %s", ruta_export_resultados)
    errores = calcular_errores(resultados, objetivo_w_m2, df.height)
    estadisticos = calcular_estadisticos(df["intensidad"].to_numpy())

    exportar_resultados(resultados, errores, ruta_export_resultados)
    exportar_estadisticos(estadisticos, ruta_export_estadisticos)

    logger.info("Generando gráficos con prefijo '%s'", ruta_prefix)
    plot_and_save(
        df["Tiempo (s)"].to_numpy(),
        df["intensidad"].to_numpy(),
        resultados,
        prefix=ruta_prefix,
    )

    logger.info("Calculando LAeq y dosis -> %s", ruta_export_laeq_dosis)
    # Persistimos primero la serie de intensidad requerida por la función
    df_intensidad_path = (
        ruta_export_laeq_dosis.replace("laeq_dosis", "intensidad")
    )
    df.write_csv(df_intensidad_path)

    energia = resultados[mejor_metodo(errores)]

    calcular_laeq_y_dosis(
        csv_path=df_intensidad_path,
        columna_intensidad="intensidad",
        dt=1.0,
        energia_total=energia,
        output_path=ruta_export_laeq_dosis,
    )


def main() -> None:
    """Ejecuta el pipeline principal de procesamiento de datos acústicos.

    Flujo resumido:
    1) Truncado 25 + 6k del archivo de entrada.
    2) Cálculo de intensidad y resultados completos.
    3) Reducción homogénea al 80% y resultados reducidos.

    Manejo de errores:
    - Cualquier excepción es registrada y relanzada con contexto adicional.
    """
    try:
        logger.info("Iniciando el pipeline de procesamiento de datos acústicos.")

        # 1) Truncado 25 + 6k
        logger.info("Truncando datos al formato 25 + 6k.")
        ruta_entrada = "data/datos.csv"
        ruta_truncado = "data/resultados/truncado_25_6k.csv"
        if not truncar_a_25_6k(
            ruta_entrada,
            columna_y="leq_mean",
            output_path=ruta_truncado,
        ):  # No se truncó
            logger.info("No se realizó truncado; usando archivo original.")
            ruta_truncado = ruta_entrada

        df_trunc = leer_csv(ruta_truncado)  # Evitar fila vacía final si existe
        _log_dataframe_info("truncado_25_6k", df_trunc)

        # 2) Serie completa
        logger.info("Convirtiendo dB a intensidad (serie completa)")
        intensidad = db_a_intensidad(df_trunc["leq_mean"].to_numpy())
        df_completo = pl.DataFrame(
            {
                "Tiempo (s)": pl.Series(range(1, df_trunc.height + 1)),
                "intensidad": intensidad,
            }
        )
        ruta_intensidad_completa = "data/resultados/intensidad_completa.csv"
        df_completo.write_csv(ruta_intensidad_completa)
        _log_dataframe_info("intensidad_completa", df_completo)

        logger.info("Calculando métodos de integración (serie completa)")
        res_completo = calcular_metodos_integracion(
            df_completo["Tiempo (s)"].to_numpy(),
            df_completo["intensidad"].to_numpy(),
        )

        _exportar_y_graficar(
            df=df_completo,
            resultados=res_completo,
            ruta_prefix="grafico_completo",
            objetivo_w_m2=90.4,
            ruta_export_resultados="data/resultados/resultados_completos.csv",
            ruta_export_estadisticos="data/resultados/estadisticos_completos.csv",
            ruta_export_laeq_dosis="data/resultados/laeq_dosis_completo.csv",
        )

        logger.info("Datos procesados y resultados guardados (serie completa)")

        # 3) Reducción homogénea al 80%
        logger.info("Generando conjunto de datos reducido al 80%.")
        ruta_reducido = "data/resultados/reducido_80.csv"
        quitar_porcentaje_homogeneo(
            ruta_truncado,
            columna_y="leq_mean",
            porcentaje=20.0,
            output_path=ruta_reducido,
        )

        df_red = leer_csv(ruta_reducido)
        _log_dataframe_info("reducido_80", df_red)

        logger.info("Convirtiendo dB a intensidad (reducido 80%%)")
        df_red_int = pl.DataFrame(
            {
                "Tiempo (s)": pl.Series(range(1, df_red.height + 1)),
                "intensidad": db_a_intensidad(df_red["leq_mean"].to_numpy()),
            }
        )
        ruta_int_reducido = "data/resultados/intensidad_reducido_80.csv"
        df_red_int.write_csv(ruta_int_reducido)
        _log_dataframe_info("intensidad_reducido_80", df_red_int)

        logger.info("Calculando métodos de integración (reducido 80%%)")
        res_red = calcular_metodos_integracion(
            df_red_int["Tiempo (s)"].to_numpy(),
            df_red_int["intensidad"].to_numpy(),
        )

        _exportar_y_graficar(
            df=df_red_int,
            resultados=res_red,
            ruta_prefix="grafico_reducido_80",
            objetivo_w_m2=90.4,
            ruta_export_resultados="data/resultados/resultados_reducido_80.csv",
            ruta_export_estadisticos="data/resultados/estadisticos_reducido_80.csv",
            ruta_export_laeq_dosis="data/resultados/laeq_dosis_reducido_80.csv",
        )

        logger.info("Pipeline completado.")

    except Exception as exc:
        logger.exception("Fallo en el pipeline: %s", exc)
        raise


if __name__ == "__main__":
    main()
