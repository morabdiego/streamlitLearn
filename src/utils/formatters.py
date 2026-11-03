"""Funciones utilitarias para formateo de números en español (Argentina)."""
from typing import Any


def format_decimal(valor: Any, decimales: int = 1) -> str:
    """Formatea un número flotante con coma decimal y punto de miles."""
    if valor is None:
        return "—"
    try:
        val = float(valor)
        return f"{val:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(valor)


def format_integer(valor: Any) -> str:
    """Formatea un número entero con punto separador de miles."""
    if valor is None:
        return "—"
    try:
        val = int(round(float(valor)))
        return f"{val:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)


def format_percentage(valor: Any, decimales: int = 1) -> str:
    """Formatea una proporción (0 a 1 ó 0 a 100 si es ya porcentaje) con sufijo %."""
    if valor is None:
        return "—"
    return f"{format_decimal(valor, decimales)}%"
