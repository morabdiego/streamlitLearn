"""Punto de entrada principal de la aplicación de Pobreza Multidimensional en CABA."""
import pandas as pd
import streamlit as st

from src import texts
from src.components import (
    render_analysis_tabs,
    render_expander,
    render_header,
    render_metric_cards,
    render_monitor_expanders,
    render_monitor_filters,
    render_monitor_sample_banner,
)
from src.config import DEFAULT_K_INTER, DEFAULT_K_INTRA, DEFAULT_YEAR
from src.logic import (
    apply_analysis_unit,
    calculate_ipm_dataset,
    calculate_ipm_metrics,
    filter_ipm_dataset,
    load_hogares_data,
    load_individuos_data,
)

st.set_page_config(
    page_title=texts.PAGE_TITLE,
    page_icon=texts.PAGE_ICON,
    layout="centered",
)


@st.cache_data(show_spinner=False)
def get_ipm_data(year: int = DEFAULT_YEAR) -> pd.DataFrame:
    """Carga los microdatos de hogares e individuos y calcula las matrices del IPM según el año."""
    raw_hog = load_hogares_data(year)
    raw_ind = load_individuos_data(year)
    return calculate_ipm_dataset(
        raw_hog,
        k_intra=DEFAULT_K_INTRA,
        k_inter=DEFAULT_K_INTER,
        df_individuos=raw_ind,
        year=year,
    )


def page_analisis_pobreza() -> None:
    """Vista 1: Artículo y análisis de la pobreza multidimensional (sin filtros en sidebar)."""
    with st.spinner(texts.LOADING_SPINNER):
        df = get_ipm_data()
    metrics = calculate_ipm_metrics(df)
    render_header()
    render_metric_cards(metrics)
    st.caption(texts.SOURCE_CAPTION)

    render_expander()

    st.divider()
    render_analysis_tabs(df)


def page_monitor_interactivo() -> None:
    """Vista 2: Monitor interactivo de datos con métricas arriba, filtros en expander y expanders de tablas."""
    st.title(texts.MONITOR_HEADER_TITLE)
    st.subheader(texts.MONITOR_SUBTITLE)
    st.warning(texts.MONITOR_BETA_WARNING_MD, icon="⚠️")

    # Contenedor superior para que las métricas se visualicen antes del expander de filtros
    metrics_container = st.container()

    df_base, year, filters, group_col, unidad = render_monitor_filters(get_ipm_data)
    df_unit = apply_analysis_unit(df_base, unidad=unidad)
    df_filtered = filter_ipm_dataset(df_unit, filters)

    with metrics_container:
        metrics = calculate_ipm_metrics(df_filtered)
        render_metric_cards(metrics, unidad=unidad)
        render_monitor_sample_banner(df_total=df_unit, df_filtered=df_filtered, unidad=unidad)
        st.caption(
            f"Fuente: Elaboración propia en base a IDECBA, Encuesta Anual de Hogares (EAH) {year}. Base de usuarios."
        )

    if df_filtered.empty:
        st.warning("No se encontraron hogares en la muestra que cumplan simultáneamente con los filtros seleccionados.")
        return

    st.divider()
    render_monitor_expanders(df_filtered, group_col=group_col, unidad=unidad, year=year)


def main() -> None:
    pg = st.navigation([
        st.Page(
            page_analisis_pobreza,
            title=texts.NAV_ANALISIS_TITLE,
            # icon=texts.NAV_ANALISIS_ICON,
            url_path="analisis",
            default=True,
        ),
        st.Page(
            page_monitor_interactivo,
            title=texts.NAV_MONITOR_TITLE,
            # icon=texts.NAV_MONITOR_ICON,
            url_path="monitor",
        )],
        position="top")
    pg.run()


if __name__ == "__main__":
    main()
