"""Exportación de resultados a CSV."""

import polars as pl
import logging

logging.getLogger(__name__)


def exportar_resultados(results: dict, errores: dict, ruta: str = "data/resultados_integracion.csv"):
    """
    Exporta resultados de integración y errores a CSV.

    Parameters
    ----------
    results : dict
        Valores de integración.
    errores : dict
        Errores relativos y porcentuales.
    ruta : str
        Ruta de salida.
    """
    df = pl.DataFrame({
        "metodo": list(results.keys()),
        "integral": list(results.values()),
        "error_relativo": [errores.get(m, None) for m in results.keys()],
        "error_porcentual": [errores.get(m + "_pct", None) for m in results.keys()]
    })
    df.write_csv(ruta)
    logging.info(f"Resultados exportados a {ruta}")


def exportar_estadisticos(stats: dict, ruta: str = "data/estadisticos.csv"):
    """
    Exporta estadísticos a CSV.

    Parameters
    ----------
    stats : dict
        Estadísticos calculados.
    ruta : str
        Ruta de salida.
    """
    df = pl.DataFrame(stats)
    df.write_csv(ruta)
    logging.info(f"Estadísticos exportados a {ruta}")