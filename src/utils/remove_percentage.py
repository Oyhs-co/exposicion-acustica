"""
Script para eliminar un porcentaje variable de filas de forma homogénea.

Guarda el resultado en:
- data/reducido_<porcentaje>%.csv
"""

import polars as pl
import os
import logging
from utils import max_filas_validas

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def quitar_porcentaje_homogeneo(csv_path: str, columna_y: str, porcentaje: float, output_path: str = None):
    """
    Elimina un porcentaje de filas de forma homogénea.

    Parameters
    ----------
    csv_path : str
        Ruta al archivo CSV original.
    columna_y : str
        Columna a conservar (por si se quiere validar integridad).
    porcentaje : float
        Porcentaje a eliminar (entre 0 y 100).
    output_path : str, optional
        Ruta de salida. Si no se indica, se genera automáticamente.
    """
    if not (0 <= porcentaje <= 100):
        raise ValueError("El porcentaje debe estar entre 0 y 100.")

    logging.info(f"Leyendo archivo: {csv_path}")
    df = pl.read_csv(csv_path)

    n_original = df.height
    step = 100 / (100 - porcentaje)
    indices = [int(i * step) for i in range(int(n_original / step)) if int(i * step) < n_original]

    df_reducido = df[indices]
    n_necesario = max_filas_validas(df_reducido.height)
    df_reducido = df_reducido.head(n_necesario)
    os.makedirs("data", exist_ok=True)

    if output_path == '' or output_path is None:
        output_path = f"data/reducido_{porcentaje:.0f}%.csv"

    df_reducido.write_csv(output_path)
    logging.info(f"Archivo reducido aproximadamente al {100 - porcentaje:.0f}% ({df_reducido.height} filas). Guardado en: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Reduce un CSV eliminando un porcentaje de filas homogéneamente.")
    parser.add_argument("csv", help="Archivo CSV de entrada")
    parser.add_argument("columna", help="Columna a conservar")
    parser.add_argument("porcentaje", type=float, help="Porcentaje a eliminar (0-100)")

    args = parser.parse_args()
    quitar_porcentaje_homogeneo(args.csv, args.columna, args.porcentaje)
