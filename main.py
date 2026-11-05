"""Punto de entrada principal de la aplicación de Pobreza Multidimensional en CABA."""
import streamlit as st

from src import texts
from src.views.analisis import page_analisis_pobreza
from src.views.monitor import page_monitor_interactivo

st.set_page_config(
    page_title=texts.PAGE_TITLE,
    page_icon=texts.PAGE_ICON,
    layout="centered",
)


def main() -> None:
    pg = st.navigation([
        st.Page(
            page_analisis_pobreza,
            title=texts.NAV_ANALISIS_TITLE,
            icon=texts.NAV_ANALISIS_ICON,
            url_path="analisis",
            default=True,
        ),
        st.Page(
            page_monitor_interactivo,
            title=texts.NAV_MONITOR_TITLE,
            icon=texts.NAV_MONITOR_ICON,
            url_path="monitor",
        )],
        position="top")
    pg.run()


if __name__ == "__main__":
    main()
