"""
Script para transformar columna de dB a intensidad relativa I(t) = 10^(L(t)/10).

Guarda el resultado en:
- data/intensidad.csv
"""

import polars as pl
import os
import logging
from ..utils import db_a_intensidad

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def transformar_intensidad(csv_path: str, columna_db: str, output_path: str = "data/intensidad.csv"):
    """
    Transforma columna de dB a intensidad relativa.

    Parameters
    ----------
    csv_path : str
        Ruta al archivo CSV original.
    columna_db : str
        Nombre de la columna en dB.
    output_path : str, optional
        Ruta de salida.
    """
    logging.info(f"Leyendo archivo: {csv_path}")
    df = pl.read_csv(csv_path)

    if columna_db not in df.columns:
        raise ValueError(f"Columna '{columna_db}' no encontrada.")

    db_vals = df[columna_db].to_numpy()
    intensidad = db_a_intensidad(db_vals)

    df_resultado = df.with_columns(pl.Series(intensidad).alias("intensidad"))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_resultado.write_csv(output_path)

    logging.info(f"Intensidad calculada y guardada en: {output_path}")


if __name__ == "__main__":
    transformar_intensidad("data/truncado_25_6k.csv", columna_db="leq_mean")