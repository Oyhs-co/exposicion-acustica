"""Transformaciones de datos acústicos."""


import numpy as np


def db_a_intensidad(db: np.ndarray, I_ref: float = 1e-12) -> np.ndarray:
    """
    Convierte valores de presión sonora en dB a intensidad relativa.

    Parameters
    ----------
    db : np.ndarray
        Valores en dB.

    Returns
    -------
    np.ndarray
        Valores de intensidad relativa I(t) = 10^(L(t)/10).
    """
    return I_ref * 10 ** (db / 10)
