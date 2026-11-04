"""Componentes visuales de Streamlit para la presentación de textos, KPIs y tablas."""
import pandas as pd
import streamlit as st

from src import texts
from src.config import MODOS_MATRIZ_INDICADORES
from src.logic import (
    IPMMetrics,
    build_deprivation_dist_table,
    build_dimension_contributions_table,
    build_domain_poverty_table,
    build_excluded_indicators_table,
    build_habitat_table,
    build_indicator_rates_table,
    build_nnya_summary_table,
    build_overlap_table,
    build_sample_table,
    build_structure_2025_table,
    format_decimal,
    format_integer,
    format_percentage,
)


def _render_table(
    df: pd.DataFrame,
    title: str | None = None,
    hide_index: bool = True,
    note: str | None = None,
    caption: str = texts.SOURCE_CAPTION,
    table = False
) -> None:
    """Renderiza una tabla con su título, nota opcional y fuente oficial."""
    if title:
        st.markdown(title)
    if not df.empty:
        if table:
            st.table(df, height="content", hide_index=hide_index)
        else:
            st.dataframe(df, width="stretch", hide_index=hide_index)
        if note:
            st.caption(note)
        st.caption(caption)


def render_header() -> None:
    """Renderiza el encabezado principal, autoría y marco teórico introductorio."""
    st.title(texts.HEADER_TITLE)
    st.markdown(texts.HEADER_AUTHOR)

    with st.expander(texts.HEADER_EXPANDER_TITLE, expanded=False):
        st.markdown(texts.HEADER_THEORY_MD)
        st.markdown("---")
        _render_table(
            pd.DataFrame(texts.TABLA_1_HISTORICO_VILLAS),
            title=texts.TABLA_1_TITULO,
            hide_index=True,
            caption=texts.TABLA_1_CAPTION,
            table=True
        )


def render_metric_cards(metrics: IPMMetrics) -> None:
    """Renderiza las 4 tarjetas principales de métricas Alkire-Foster."""
    col1, col2, col3, col4 = st.columns(4)

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
        label=texts.KPI_POBRES_LABEL,
        value=format_integer(metrics.pobres_expandidos),
        delta=f"de {format_integer(metrics.hogares_expandidos)} totales",
        delta_color="off",
    )


def render_tab_brecha_territorial(df: pd.DataFrame) -> None:
    """Pestaña 1: Marco muestral, brecha territorial, pobreza estructural e intensidad."""
    st.subheader(texts.TAB1_SUBHEADER)
    st.markdown(texts.TAB1_INTRO_MD)

    st.markdown(texts.TAB1_SEC1_TITULO)
    st.markdown(texts.TAB1_SEC1_MD)
    _render_table(build_sample_table(df), title=texts.TABLA_2_TITULO, hide_index=True, table=True)

    st.markdown("---")

    st.markdown(texts.TAB1_SEC2_TITULO)
    _render_table(build_domain_poverty_table(df), title=texts.TABLA_3_TITULO, hide_index=True, table=True)
    st.markdown(texts.TAB1_SEC2_OUTRO_MD)

    st.markdown("---")

    st.markdown(texts.TAB1_SEC3_TITULO)
    st.markdown(texts.TAB1_SEC3_MD)
    _render_table(build_overlap_table(df), title=texts.TABLA_4_TITULO, hide_index=False, table=True)

    st.markdown("---")

    st.markdown(texts.TAB1_SEC4_TITULO)
    st.markdown(texts.TAB1_SEC4_MD)
    _render_table(build_deprivation_dist_table(df), title=texts.TABLA_5_TITULO, hide_index=False, table=True)


def render_tab_discusion_metodologica(df: pd.DataFrame) -> None:
    """Pestaña 2: Debate Método Consensual vs. Alkire-Foster, estructura 2025 y contribución a M0."""
    st.subheader(texts.TAB2_SUBHEADER)
    st.markdown(texts.TAB2_INTRO_MD)
    st.warning(texts.TAB2_CONSENSUAL_WARNING_MD)
    st.info(texts.TAB2_AF_INFO_MD)

    st.markdown(texts.TAB2_SEC7_TITULO)
    df_matriz = build_structure_2025_table()
    st.markdown(texts.TABLA_6_TITULO)
    st.dataframe(
        df_matriz,
        # width="stretch",
        hide_index=True,
        # height=min(35 * len(df_matriz) + 38, 800),
        column_config={
            "Dimensión": st.column_config.TextColumn(width="medium"),
            "Indicador": st.column_config.TextColumn(width="medium"),
        },
    )
    st.caption(texts.SOURCE_CAPTION)

    st.markdown("---")

    st.markdown(texts.TAB2_SEC8_TITULO)
    st.markdown(texts.TAB2_SEC8_MD)
    _render_table(build_dimension_contributions_table(df), title=texts.TABLA_7_TITULO, hide_index=False)


def render_tab_discusion_indicadores(df: pd.DataFrame) -> None:
    """Pestaña 3: Indicadores descartados del módulo PM y variables estructurales de hábitat."""
    st.subheader(texts.TAB3_SUBHEADER)
    st.markdown(texts.TAB3_INTRO_MD)

    st.markdown(texts.TAB3_SEC9_TITULO)
    st.markdown(texts.TAB3_SEC9_MD)
    _render_table(build_excluded_indicators_table(df), title=texts.TABLA_8_TITULO, hide_index=True, table=True)

    st.markdown("---")

    st.markdown(texts.TAB3_SEC10_TITULO)
    st.markdown(texts.TAB3_SEC10_MD)
    _render_table(
        build_habitat_table(df),
        title=texts.TABLA_9_TITULO,
        hide_index=False,
        note=texts.TABLA_9_NOTA_CLOACA,
    )

    st.markdown("---")


def render_tab_indicadores_detalle(df: pd.DataFrame) -> None:
    """Pestaña 4: Resumen según presencia de NNyA y tasas por indicador (3 modos de matriz)."""
    st.subheader(texts.TAB4_SUBHEADER)

    st.markdown(texts.TAB4_SEC11_TITULO)
    st.markdown(texts.TAB4_SEC11_MD)
    _render_table(build_nnya_summary_table(df), title=texts.TABLA_10_TITULO, hide_index=True, table=True)

    st.markdown("---")

    st.markdown(texts.TAB4_SEC12_TITULO)
    opcion_sel = st.radio(
        texts.TAB4_RADIO_LABEL,
        options=list(MODOS_MATRIZ_INDICADORES.keys()),
        horizontal=True,
    )
    modo = MODOS_MATRIZ_INDICADORES[opcion_sel]

    for tiene_nnya, titulo in [(1, texts.TABLA_11_TITULO), (0, texts.TABLA_12_TITULO)]:
        st.markdown(f"##### {titulo}")
        df_ind = build_indicator_rates_table(df, tiene_nnya=tiene_nnya, modo=modo) # pyright: ignore[reportArgumentType]
        _render_table(df_ind, hide_index=True)


def render_tab_conclusiones() -> None:
    """Pestaña 5: Conclusiones, Anexo RENABAP y Bibliografía."""
    st.subheader(texts.TAB5_SUBHEADER)
    st.markdown(texts.TAB5_CONCLUSIONES_MD)

    st.markdown("---")

    with st.expander(texts.ANEXO_1_TITULO):
        st.markdown(texts.ANEXO_1_INTRO_MD)
        _render_table(
            pd.DataFrame(texts.BARRIOS_RENABAP_CABA),
            hide_index=True,
            caption=texts.ANEXO_1_CAPTION,
        )

    st.markdown("---")

    st.markdown(texts.BIBLIOGRAFIA_TITULO)
    st.markdown(texts.BIBLIOGRAFIA_MD)


def render_analysis_tabs(df: pd.DataFrame) -> None:
    """Renderiza las 5 pestañas temáticas de la aplicación."""
    tab1, tab2, tab3, tab4, tab5 = st.tabs(texts.TAB_LABELS)

    with tab1:
        render_tab_brecha_territorial(df)
    with tab2:
        render_tab_discusion_metodologica(df)
    with tab3:
        render_tab_discusion_indicadores(df)
    with tab4:
        render_tab_indicadores_detalle(df)
    with tab5:
        render_tab_conclusiones()
