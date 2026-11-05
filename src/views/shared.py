"""Componentes visuales compartidos entre páginas: tablas, tarjetas KPI y selectores comunes."""
import pandas as pd
import streamlit as st

from src import texts
from src.config import AnalysisUnit, IndicatorRateMode, MODOS_MATRIZ_INDICADORES
from src.formatting import format_decimal, format_integer, format_percentage
from src.ipm import IPMMetrics

_EXPANDER_CSS = """
<style>
div[data-testid="stExpander"] summary p {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
}
</style>
"""


def inject_expander_css() -> None:
    """Inyecta el estilo CSS para el encabezado de los expanders."""
    st.markdown(_EXPANDER_CSS, unsafe_allow_html=True)


def render_table(
    df: pd.DataFrame,
    title: str | None = None,
    hide_index: bool = True,
    note: str | None = None,
    caption: str = texts.SOURCE_CAPTION,
    static: bool = False,
) -> None:
    """Renderiza una tabla con su título, nota opcional y fuente oficial."""
    if title:
        st.markdown(title)
    if not df.empty:
        if static:
            st.table(df, height="content", hide_index=hide_index)
        else:
            st.dataframe(df, width="stretch", hide_index=hide_index)
        if note:
            st.caption(note)
        st.caption(caption)


def select_modo_matriz(key: str | None = None) -> IndicatorRateMode:
    """Renderiza el selector de modo de matriz (no censurada, censurada, entre pobres) y devuelve la clave tipada."""
    opcion_sel = st.radio(
        texts.TAB4_RADIO_LABEL,
        options=list(MODOS_MATRIZ_INDICADORES.keys()),
        horizontal=True,
        key=key,
    )
    return MODOS_MATRIZ_INDICADORES[opcion_sel]


def render_metric_cards(metrics: IPMMetrics, unidad: AnalysisUnit = "hogares") -> None:
    """Renderiza las 4 tarjetas principales de métricas Alkire-Foster (a nivel hogares o personas)."""
    col1, col2, col3, col4 = st.columns(4)
    pobres_label = texts.KPI_POBRES_PERSONAS_LABEL if unidad == "personas" else texts.KPI_POBRES_LABEL

    col1.metric(
        label=texts.KPI_H_LABEL,
        value=format_percentage(metrics.h * 100),
        help=texts.KPI_H_HELP,
    )
    col2.metric(
        label=texts.KPI_A_LABEL,
        value=format_percentage(metrics.a * 100),
        help=texts.KPI_A_HELP,
    )
    col3.metric(
        label=texts.KPI_M0_LABEL,
        value=format_decimal(metrics.m0, decimales=3),
        help=texts.KPI_M0_HELP,
    )
    col4.metric(
        label=pobres_label,
        value=format_integer(metrics.pobres_expandidos),
        delta=f"de {format_integer(metrics.hogares_expandidos)} totales",
        delta_color="off",
    )
