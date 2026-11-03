"""Componente para la visualización de tarjetas de métricas (KPIs)."""
import streamlit as st

from src.domain.models import IPMMetrics
from src.utils.formatters import format_decimal, format_integer, format_percentage


def render_metric_cards(metrics: IPMMetrics) -> None:
    """Renderiza las 4 tarjetas principales con las métricas de Alkire-Foster."""
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Incidencia (H)",
        value=format_percentage(metrics.h * 100),
        help="Porcentaje de hogares pobres multidimensionales",
    )

    col2.metric(
        label="Intensidad (A)",
        value=format_percentage(metrics.a * 100),
        help="Promedio de privaciones entre los hogares identificados como pobres",
    )

    col3.metric(
        label="IPM (M0)",
        value=format_decimal(metrics.m0, decimales=3),
        help="Tasa M0 ajustada por intensidad (H × A)",
    )

    col4.metric(
        label="Total de hogares pobres multidimensionales",
        value=format_integer(metrics.pobres_expandidos),
        delta=f"de {format_integer(metrics.hogares_expandidos)} totales",
        delta_color="off",
    )
