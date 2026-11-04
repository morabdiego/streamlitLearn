"""Punto de entrada principal de la aplicación de Pobreza Multidimensional en CABA."""
import pandas as pd
import streamlit as st

from src import texts
from src.components import render_analysis_tabs, render_header, render_metric_cards
from src.config import DEFAULT_K_INTER, DEFAULT_K_INTRA, DEFAULT_YEAR
from src.logic import calculate_ipm_dataset, calculate_ipm_metrics, load_hogares_data

st.set_page_config(
    page_title=texts.PAGE_TITLE,
    page_icon=texts.PAGE_ICON,
    layout="centered",
)


@st.cache_data(show_spinner=False)
def get_ipm_data(year: int = DEFAULT_YEAR) -> pd.DataFrame:
    """Carga los microdatos de hogares y calcula las matrices del IPM."""
    raw_df = load_hogares_data(year)
    return calculate_ipm_dataset(raw_df, k_intra=DEFAULT_K_INTRA, k_inter=DEFAULT_K_INTER)


def main() -> None:
    with st.spinner(texts.LOADING_SPINNER):
        df = get_ipm_data()

    render_header()

    metrics = calculate_ipm_metrics(df)
    render_metric_cards(metrics)
    st.caption(texts.SOURCE_CAPTION)

    st.divider()
    render_analysis_tabs(df)


if __name__ == "__main__":
    main()
