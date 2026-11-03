"""Modelos de datos y estructuras tipadas del dominio."""
from dataclasses import dataclass


@dataclass(frozen=True)
class IPMMetrics:
    """Métricas agregadas del Índice de Pobreza Multidimensional."""
    h: float                     # Incidencia (Headcount ratio)
    a: float                     # Intensidad (Intensity of deprivation)
    m0: float                    # Tasa M0 ajustada (H * A)
    hogares_expandidos: int      # Total ponderado de hogares
    pobres_expandidos: int       # Total ponderado de hogares pobres


@dataclass(frozen=True)
class FilterParams:
    """Parámetros y filtros seleccionados por el usuario."""
    anio: int
    k_intra: float
    k_inter: float
    dominios: list[str]
    tipos_hogar: list[str]
