"""Funciones de formateo numérico con convención local argentina (coma decimal y punto de miles)."""
from typing import Any

import pandas as pd


def format_decimal(valor: Any, decimales: int = 1) -> str:
    """Formatea un número flotante con coma decimal y punto separador de miles."""
    if valor is None or pd.isna(valor):
        return "—"
    try:
        val = float(valor)
        return f"{val:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(valor)


def format_integer(valor: Any) -> str:
    """Formatea un número entero con punto separador de miles."""
    if valor is None or pd.isna(valor):
        return "—"
    try:
        val = int(round(float(valor)))
        return f"{val:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)


def format_percentage(valor: Any, decimales: int = 1) -> str:
    """Formatea un valor porcentual (0 a 100) con sufijo %."""
    if valor is None or pd.isna(valor):
        return "—"
    return f"{format_decimal(valor, decimales)}%"


def format_df_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """Formatea todas las celdas de un DataFrame como porcentajes."""
    return df.map(format_percentage)
