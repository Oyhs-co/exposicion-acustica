"""Generación y guardado de gráficos."""

import matplotlib.pyplot as plt
import numpy as np
import logging

logging.getLogger(__name__)


def plot_and_save(x: np.ndarray, y: np.ndarray, results: dict, prefix: str = None) -> None:
    """
    Genera y guarda gráficas de serie temporal y comparación de métodos.

    Parameters
    ----------
    x : np.ndarray
        Eje x.
    y : np.ndarray
        Eje y.
    results : dict
        Resultados de integración.
    """
    plt.figure(figsize=(12, 5))

    # Serie temporal
    plt.subplot(1, 2, 1)
    plt.plot(x, y, label='Datos (y)', color='blue')
    plt.title("Serie temporal de los datos")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"IMG/{prefix}_serie.png")
    logging.info(f"Gráfica de serie guardada en IMG/{prefix}_serie.png")

    # Comparación de métodos
    plt.subplot(1, 2, 2)
    methods = list(results.keys())
    values = list(results.values())
    plt.bar(methods, values, color=['orange', 'green', 'red'])
    plt.title("Comparación de métodos de integración")
    plt.ylabel("Valor de la integral")
    plt.grid(axis='y')
    plt.savefig(f"IMG/{prefix}_comparacion.png")
    logging.info(f"Gráfica de comparación guardada en IMG/{prefix}_comparacion.png")

    plt.tight_layout()
    plt.close()
