"""Utilidades de validación."""


def max_filas_validas(n: int) -> int:
    """
    Calcula el máximo número de filas válido según 25 + 6k.

    Parameters
    ----------
    n : int
        Número actual de filas.

    Returns
    -------
    int
        Máximo número de filas válido.
    """
    k_max = (n - 25) // 6
    return 25 + 6 * k_max
