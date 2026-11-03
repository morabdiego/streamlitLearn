"""Punto de entrada principal para la aplicación de Streamlit del IPM."""
import streamlit as st

from src.config.constants import SOURCE_CAPTION
from src.data.loader import load_hogares_data
from src.domain.alkire_foster import (
    apply_ipm_cutoffs,
    calculate_ipm_metrics,
    filter_ipm_dataset,
    prepare_base_scores,
)
from src.ui.header import render_header
from src.ui.metrics import render_metric_cards
from src.ui.sidebar import render_sidebar
from src.ui.tabs import render_analysis_tabs


# 1. Configuración de página
st.set_page_config(
    page_title="Pobreza Multidimensional en CABA",
    page_icon="🏙️",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def get_cached_base_scores(anio: int):
    """Carga los microdatos de hogares y calcula los scores dimensionales continuos."""
    raw_df = load_hogares_data(anio)
    return prepare_base_scores(raw_df)


def main() -> None:
    # 2. Barra lateral con filtros y parámetros metodológicos
    params = render_sidebar()

    # 3. Procesamiento reactivo del IPM
    with st.spinner("Procesando microdatos y calculando cortes..."):
        raw_df = load_hogares_data(params.anio)
        df_base = get_cached_base_scores(params.anio)
        df_ipm = apply_ipm_cutoffs(
            df_base,
            k_intra=params.k_intra,
            k_inter=params.k_inter,
        )
        df_view = filter_ipm_dataset(
            df_ipm,
            dominios_seleccionados=params.dominios,
            tipos_hogar_seleccionados=params.tipos_hogar,
        )

    # 4. Título, autoría y contextualización teórica
    render_header(params.anio)

    # 5. Tarjetas de métricas principales (Alkire-Foster) para la selección actual
    metrics = calculate_ipm_metrics(df_view)
    render_metric_cards(metrics)
    st.caption(SOURCE_CAPTION)

    st.divider()

    # 6. Pestañas temáticas con storytelling, discusión metodológica y datos desagregados
    render_analysis_tabs(
        df_view=df_view,
        k_intra=params.k_intra,
        tipos_hogar_seleccionados=params.tipos_hogar,
        raw_df=raw_df,
    )


if __name__ == "__main__":
    main()
