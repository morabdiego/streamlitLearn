"""Componente de barra lateral con controles y filtros."""
import streamlit as st

from src.config.constants import (
    AVAILABLE_YEARS,
    DEFAULT_K_INTER,
    DEFAULT_K_INTRA,
    DEFAULT_YEAR,
    MAP_DOMINIO,
    MAP_TIPO_HOGAR,
)
from src.domain.models import FilterParams


def render_sidebar() -> FilterParams:
    """Renderiza los controles de la barra lateral y devuelve los parámetros seleccionados."""
    with st.sidebar:
        st.header("⚙️ Parámetros del IPM")

        anio_sel = st.selectbox(
            "Año de relevamiento:",
            options=AVAILABLE_YEARS,
            index=AVAILABLE_YEARS.index(DEFAULT_YEAR) if DEFAULT_YEAR in AVAILABLE_YEARS else 0,
        )

        st.markdown("---")
        st.markdown("**Umbrales metodológicos:**")

        u_intra = st.slider(
            "Corte intra-dimensión (k-intra):",
            min_value=0.10,
            max_value=0.60,
            value=DEFAULT_K_INTRA,
            step=0.01,
            format="%.2f",
            help="Metodología IDECBA: 33%",
        )

        u_inter = st.slider(
            "Corte inter-dimensión (k-inter):",
            min_value=0.20,
            max_value=0.80,
            value=DEFAULT_K_INTER,
            step=0.05,
            format="%.2f",
            help="Metodología IDECBA: 40%",
        )

        st.markdown("---")
        st.markdown("**Filtros poblacionales:**")

        filtro_dom = st.multiselect(
            "Dominio geográfico:",
            options=list(MAP_DOMINIO.values()),
            default=list(MAP_DOMINIO.values()),
        )

        filtro_tipo_hogar = st.multiselect(
            "Presencia de NNyA:",
            options=list(MAP_TIPO_HOGAR.keys()),
            default=list(MAP_TIPO_HOGAR.keys()),
        )

    return FilterParams(
        anio=anio_sel,
        k_intra=u_intra,
        k_inter=u_inter,
        dominios=filtro_dom,
        tipos_hogar=filtro_tipo_hogar,
    )
