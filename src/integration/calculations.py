"""Cálculos de integración numérica."""

from .metods import trapezoidal_rule, simpson_1_3_rule, simpson_3_8_rule
import numpy as np
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def calcular_metodos_integracion(x: np.ndarray,
                                 y: np.ndarray) -> dict[str, float | None]:
    """
    Calcula la integral de y respecto a x usando varios
    métodos de integración numérica.

    Parameters
    ----------
    x : np.ndarray
        Valores del eje independiente.
    y : np.ndarray
        Valores del eje dependiente.

    Returns
    -------
    dict
        Diccionario con los resultados de cada método de integración.
    """
    resultados = {}
    resultados['Trapecios'] = trapezoidal_rule(x, y)
    try:
        resultados['Simpson 1/3'] = simpson_1_3_rule(x, y)
    except ValueError as e:
        logging.warning(f"Simpson 1/3 no se pudo calcular: {e}")
        resultados['Simpson 1/3'] = None
    try:
        resultados['Simpson 3/8'] = simpson_3_8_rule(x, y)
    except ValueError as e:
        logging.warning(f"Simpson 3/8 no se pudo calcular: {e}")
        resultados['Simpson 3/8'] = None

    return resultados
