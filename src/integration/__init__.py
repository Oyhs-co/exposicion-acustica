"""Paquete de métodos de integración numérica."""

from .metods import trapezoidal_rule, simpson_1_3_rule, simpson_3_8_rule
from .dB_to_intensity import db_a_intensidad
from .analize import calcular_laeq_y_dosis
from .errors import calcular_errores
from .statisticists import calcular_estadisticos

__all__ = [
    "trapezoidal_rule",
    "simpson_1_3_rule",
    "simpson_3_8_rule",
    "db_a_intensidad",
    "calcular_laeq_y_dosis",
    "calcular_errores",
    "calcular_estadisticos",
]
