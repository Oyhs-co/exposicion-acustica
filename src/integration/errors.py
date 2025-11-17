"""Cálculo de errores relativos y porcentuales."""

import numpy as np

def calcular_errores(resultados: dict, referencia: float, N: int) -> dict:
    """
    Calcula errores relativos y porcentuales respecto a un valor de referencia.

    Parameters
    ----------
    resultados : dict
        Diccionario con los valores de integración.
    referencia : float
        Valor de referencia (normalmente trapecios).

    Returns
    -------
    dict
        Diccionario con errores relativos y porcentuales.
    """
    errores = {}
    I_0 = 1e-12
    referencia = N * I_0 * 10**(referencia / 10)  # Ajuste de escala
    for metodo, valor in resultados.items():
        err_rel = abs(valor - referencia) / abs(referencia)
        err_pct = err_rel * 100
        errores[metodo] = err_rel
        errores[metodo + "_pct"] = err_pct
    return errores


def error_en_metodo(metodo: str, errores: dict) -> tuple[float | None, float | None]:
    """
    Obtiene el error relativo y porcentual de un método específico.

    Parameters
    ----------
    metodo : str
        Nombre del método de integración.
    errores : dict
        Diccionario con los errores calculados.

    Returns
    -------
    tuple
        Error relativo y porcentual del método, o None si no está disponible.
    """
    err_rel = errores.get(metodo, None)
    err_pct = errores.get(metodo + "_pct", None)
    return err_rel, err_pct

def mejor_metodo(errores: dict) -> str:
    """
    Determina el método con el menor error relativo.

    Parameters
    ----------
    errores : dict
        Diccionario con los errores calculados.

    Returns
    -------
    str | None
        Nombre del método con el menor error relativo, o None si no hay métodos disponibles.
    """
    min_error = float('inf')
    mejor_metodo = None
    for metodo in errores:
        if not metodo.endswith("_pct"):
            err_rel = errores[metodo]
            if err_rel is not None and err_rel < min_error:
                min_error = err_rel
                mejor_metodo = metodo
    return mejor_metodo