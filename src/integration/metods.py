"""Métodos de integración numérica: trapecios, Simpson 1/3 y 3/8."""

import numpy as np
import logging

logger = logging.getLogger(__name__)


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
    if len(x) != len(y):
        raise ValueError("Los arrays x e y deben tener la misma longitud.")
    if len(x) < 2:
        raise ValueError("Se requieren al menos 2 puntos para la regla del trapecio.")

    result = np.trapz(y, x)
    logger.info(f"Integral Trapecios: {result:.6f}")
    return result


def simpson_1_3_rule(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calcula la integral usando Simpson 1/3.

    Parameters
    ----------
    x : np.ndarray
        Valores del eje independiente (deben ser equiespaciados).
    y : np.ndarray
        Valores del eje dependiente.

    Returns
    -------
    float
        Valor de la integral.

    Raises
    ------
    ValueError
        Si el número de puntos no es impar, menor que 3, o los puntos no son equiespaciados.
    """
    if len(x) != len(y):
        raise ValueError("Los arrays x e y deben tener la misma longitud.")
    n = len(x)
    if n < 3:
        raise ValueError("Se requieren al menos 3 puntos para Simpson 1/3.")
    if n % 2 == 0:
        raise ValueError("Simpson 1/3 requiere un número impar de puntos (n_puntos >= 3).")

    # Verificar que los puntos estén equiespaciados
    dx = np.diff(x)
    if not np.allclose(dx, dx[0]):
        raise ValueError("Simpson 1/3 requiere puntos equiespaciados.")

    h = dx[0]
    result = (h / 3) * (y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]))
    logger.info(f"Integral Simpson 1/3: {result:.6f}")
    return result


def simpson_3_8_rule(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calcula la integral usando Simpson 3/8.

    Parameters
    ----------
    x : np.ndarray
        Valores del eje independiente (deben ser equiespaciados).
    y : np.ndarray
        Valores del eje dependiente.

    Returns
    -------
    float
        Valor de la integral.

    Raises
    ------
    ValueError
        Si (n_puntos - 1) no es múltiplo de 3, o los puntos no son equiespaciados.
    """
    if len(x) != len(y):
        raise ValueError("Los arrays x e y deben tener la misma longitud.")
    n = len(x)
    if n < 4:
        raise ValueError("Se requieren al menos 4 puntos para Simpson 3/8.")
    if (n - 1) % 3 != 0:
        raise ValueError("Simpson 3/8 requiere que el número de subintervalos sea múltiplo de 3 "
                         "(es decir, n_puntos ≡ 1 mod 3).")

    # Verificar que los puntos estén equiespaciados
    dx = np.diff(x)
    if not np.allclose(dx, dx[0]):
        raise ValueError("Simpson 3/8 requiere puntos equiespaciados.")

    h = dx[0]
    # Construir coeficientes: 1, 3, 3, 2, 3, 3, 2, ..., 3, 3, 1
    coef = np.ones(n)
    coef[1:-1] = 3  # Todos los internos empiezan con 3
    coef[3:-1:3] = 2  # Cada tercer índice interno (3, 6, 9, ...) se corrige a 2

    result = (3 * h / 8) * np.dot(coef, y)
    logger.info(f"Integral Simpson 3/8: {result:.6f}")
    return result
