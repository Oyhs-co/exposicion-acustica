"""Métodos de integración numérica: trapecios, Simpson 1/3 y 3/8."""

import numpy as np
import logging

logging.getLogger(__name__)


def trapezoidal_rule(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calcula la integral usando la regla del trapecio.

    Parameters
    ----------
    x : np.ndarray
        Valores del eje independiente.
    y : np.ndarray
        Valores del eje dependiente.

    Returns
    -------
    float
        Valor de la integral.
    """
    result = np.trapz(y, x)
    logging.info(f"Integral Trapecios: {result:.6f}")
    return result


def simpson_1_3_rule(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calcula la integral usando Simpson 1/3.

    Parameters
    ----------
    x : np.ndarray
        Valores del eje independiente.
    y : np.ndarray
        Valores del eje dependiente.

    Returns
    -------
    float
        Valor de la integral.

    Raises
    ------
    ValueError
        Si el número de puntos no es impar.
    """
    n = len(x)
    if n % 2 == 0:
        raise ValueError("Simpson 1/3 requiere un número impar de puntos.")
    h = x[1] - x[0]
    result = (h / 3) * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]))
    logging.info(f"Integral Simpson 1/3: {result:.6f}")
    return result


def simpson_3_8_rule(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calcula la integral usando Simpson 3/8.

    Parameters
    ----------
    x : np.ndarray
        Valores del eje independiente.
    y : np.ndarray
        Valores del eje dependiente.

    Returns
    -------
    float
        Valor de la integral.

    Raises
    ------
    ValueError
        Si el número de puntos no es múltiplo de 3.
    """
    n = len(x)
    if n % 3 != 0:
        raise ValueError("Simpson 3/8 requiere un número de puntos múltiplo de 3.")
    h = x[1] - x[0]
    suma = y[0] + y[-1]
    for i in range(1, n - 1):
        suma += 3 * y[i] if i % 3 != 0 else 2 * y[i]
    result = (3 * h / 8) * suma
    logging.info(f"Integral Simpson 3/8: {result:.6f}")
    return result
