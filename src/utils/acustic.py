"""Cálculos acústicos: LAeq,T y dosis de ruido."""


import numpy as np


def calcular_laeq_t(intensidades: np.ndarray, dt: float, energia_total: float) -> float:
    """
    Calcula el nivel equivalente continuo LAeq,T.

    Parameters
    ----------
    intensidades : np.ndarray
        Valores de intensidad I(t).
    dt : float
        Intervalo de tiempo entre muestras (en segundos).

    Returns
    -------
    float
        LAeq,T en dB(A).
    """
    I_ref = 1e-12
    energia_total = np.sum(intensidades) * dt
    T = len(intensidades) * dt
    laeq = 10 * np.log10((energia_total / T) / I_ref)
    return laeq


def calcular_dosis(laeq: float, T_horas: float) -> float:
    """
    Calcula la dosis de ruido en % según RD 286/2006.

    Parameters
    ----------
    laeq : float
        LAeq,T en dB(A).
    T_horas : float
        Tiempo total de medición en horas.

    Returns
    -------
    float
        Dosis de ruido en porcentaje.
    """
    lex8h = laeq + 10 * np.log10(T_horas / 8)
    dosis = 100 * (2 ** ((lex8h - 85) / 3))
    return dosis
