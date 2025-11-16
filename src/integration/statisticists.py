"""Cálculo de estadísticos descriptivos."""


import numpy as np


def calcular_estadisticos(y: np.ndarray) -> dict:
    """
    Calcula estadísticos descriptivos de un array.

    Parameters
    ----------
    y : np.ndarray
        Array de valores.

    Returns
    -------
    dict
        Diccionario con media, desviación estándar, min, max y mediana.
    """
    return {
        "media": float(np.mean(y)),
        "desv_std": float(np.std(y)),
        "min": float(np.min(y)),
        "max": float(np.max(y)),
        "mediana": float(np.median(y)),
    }