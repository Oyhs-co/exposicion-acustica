"""Lectura de archivos CSV con Polars."""

import polars as pl
import logging

logging.getLogger(__name__)


def leer_csv(ruta: str) -> pl.DataFrame:
    """
    Lee un archivo CSV y devuelve un DataFrame de Polars.

    Parameters
    ----------
    ruta : str
        Ruta al archivo CSV.

    Returns
    -------
    pl.DataFrame
        Datos leídos.
    """
    logging.info(f"Leyendo archivo: {ruta}")
    return pl.read_csv(ruta)
