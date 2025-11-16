"""Cálculo de errores relativos y porcentuales."""


def calcular_errores(resultados: dict, referencia: float) -> dict:
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
    for metodo, valor in resultados.items():
        if metodo != "Trapecios":
            err_rel = abs(valor - referencia) / abs(referencia)
            err_pct = err_rel * 100
            errores[metodo] = err_rel
            errores[metodo + "_pct"] = err_pct
    return errores
