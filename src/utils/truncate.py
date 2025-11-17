"""
Script para truncar un archivo CSV al máximo tamaño válido según la regla 25 + 6k.

Guarda el resultado en:
- data/truncado_25_6k.csv
"""

import polars as pl
import os
import logging
from .validations import max_filas_validas

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def truncar_a_25_6k(csv_path: str, columna_y: str, output_path: str = "data/truncado_25_6k.csv") -> bool:
    """
    Trunca un CSV al máximo tamaño válido según 25 + 6k.

    Parameters
    ----------
    csv_path : str
        Ruta al archivo CSV original.
    columna_y : str
        Columna a conservar (por si se quiere validar integridad).
    output_path : str, optional
        Ruta de salida del archivo truncado.
    """
    logging.info(f"Leyendo archivo: {csv_path}")
    df = pl.read_csv(csv_path)

    n_original = df.height
    n_valido = max_filas_validas(n_original)

    if n_valido >= n_original:
        logging.info("No es necesario truncar.")
        return False

    df_truncado = df.head(n_valido)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_truncado.write_csv(output_path)

    logging.info(f"Archivo truncado a {n_valido} filas. Guardado en: {output_path}")

    return True

if __name__ == "__main__":
    truncar_a_25_6k("datos.csv", columna_y="leq_mean")
