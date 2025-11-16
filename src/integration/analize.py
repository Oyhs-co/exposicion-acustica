"""
Script para calcular LAeq,T y dosis de ruido desde intensidad.

Guarda el resultado en:
- data/laeq_dosis.csv
"""

import polars as pl
import os
import logging
from ..utils import calcular_laeq_t, calcular_dosis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calcular_laeq_y_dosis(csv_path: str, columna_intensidad: str, dt: float, output_path: str = "data/laeq_dosis.csv"):
    """
    Calcula LAeq,T y dosis de ruido desde intensidad.

    Parameters
    ----------
    csv_path : str
        Ruta al CSV con columna de intensidad.
    columna_intensidad : str
        Nombre de la columna de intensidad.
    dt : float
        Intervalo entre muestras en segundos.
    output_path : str, optional
        Ruta de salida.
    """
    logging.info(f"Leyendo archivo: {csv_path}")
    df = pl.read_csv(csv_path)

    if columna_intensidad not in df.columns:
        raise ValueError(f"Columna '{columna_intensidad}' no encontrada.")

    intensidades = df[columna_intensidad].to_numpy()
    T_seg = len(intensidades) * dt
    T_horas = T_seg / 3600

    laeq = calcular_laeq_t(intensidades, dt)
    dosis = calcular_dosis(laeq, T_horas)

    df_resultado = pl.DataFrame({
        "LAeq_T_dB": [laeq],
        "dosis_%": [dosis],
        "T_horas": [T_horas]
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_resultado.write_csv(output_path)

    logging.info(f"LAeq,T = {laeq:.2f} dB(A)")
    logging.info(f"Dosis = {dosis:.2f}%")
    logging.info(f"Resultados guardados en: {output_path}")


if __name__ == "__main__":
    calcular_laeq_y_dosis("data/intensidad.csv", columna_intensidad="intensidad", dt=1.0)
