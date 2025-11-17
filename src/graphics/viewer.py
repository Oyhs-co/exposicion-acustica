"""Generación y guardado de gráficos."""

import matplotlib.pyplot as plt
import numpy as np
import logging

logging.getLogger(__name__)


def plot_and_save(
    x: np.ndarray,
    y: np.ndarray,
    results: dict[str, float],
    prefix: str | None = None,
) -> None:
    """
    Genera y guarda:
    - Gráfico de serie temporal mejorado (más claro y descriptivo).
    - Gráfico de barras de comparación de métodos (sin cambios).
    """
    plt.figure(figsize=(14, 6))

    # ---------- Serie temporal MEJORADA ----------
    plt.subplot(1, 2, 1)

    # Línea principal
    plt.plot(x, y, color='teal', linewidth=2, label='Datos observados (y)')

    # Sombra suave
    plt.fill_between(x, y, alpha=0.2, color='teal')

    # Estadísticas para la leyenda
    y_mean = np.mean(y)
    y_std = np.std(y)

    plt.axhline(y_mean, color='crimson', linestyle='--', linewidth=1.2, label=f'Media: {y_mean:.2f}')
    plt.axhline(y_mean + y_std, color='gray', linestyle=':', alpha=0.7, label=f'+1 desv. estándar: {y_mean + y_std:.2f}')
    plt.axhline(y_mean - y_std, color='gray', linestyle=':', alpha=0.7, label=f'-1 desv. estándar: {y_mean - y_std:.2f}')

    plt.title("Serie temporal de los datos observados")
    plt.xlabel("Índice o variable independiente (x)")
    plt.ylabel("Valor observado (y)")
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend(loc='best', fontsize=9)
    plt.tight_layout()

    # Guardar serie temporal
    serie_path = f"IMG/{prefix}_serie.png"
    plt.savefig(serie_path)
    logging.info(f"Gráfica de serie guardada en {serie_path}")

    # ---------- Comparación de métodos (SIN CAMBIOS) ----------
    plt.subplot(1, 2, 2)
    methods = list(results.keys())
    values = list(results.values())
    plt.bar(methods, values, color=['orange', 'green', 'red'])
    plt.title("Comparación de métodos de integración")
    plt.ylabel("Valor de la integral")
    plt.grid(axis='y')
    comparacion_path = f"IMG/{prefix}_comparacion.png"
    plt.savefig(comparacion_path)
    logging.info(f"Gráfica de comparación guardada en {comparacion_path}")

    plt.tight_layout()
    plt.close()