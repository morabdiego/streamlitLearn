"""Módulo de carga y lectura de microdatos de la EAH."""
from pathlib import Path
import pandas as pd
import streamlit as st

from src.config.constants import DATA_DIR


@st.cache_data(show_spinner=False)
def load_hogares_data(year: int | str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Carga la base de hogares para un año determinado desde el directorio de datos."""
    year_str = str(year)
    file_path = data_dir / year_str / f"eah{year_str}_bu_ampliada_hog.txt"

    if not file_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de microdatos de hogares en: {file_path}"
        )

    return pd.read_csv(file_path, sep=";")


@st.cache_data(show_spinner=False)
def load_individuos_data(year: int | str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Carga la base de individuos para un año determinado desde el directorio de datos."""
    year_str = str(year)
    file_path = data_dir / year_str / f"eah{year_str}_bu_ampliada_ind.txt"

    if not file_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de microdatos de individuos en: {file_path}"
        )

    return pd.read_csv(file_path, sep=";")


def load_data(year: int | str, load_ind: bool = False, data_dir: Path = DATA_DIR):
    """Función de conveniencia para cargar hogares y (opcionalmente) individuos."""
    base_hogares = load_hogares_data(year, data_dir)
    base_individuos = load_individuos_data(year, data_dir) if load_ind else None
    return base_hogares, base_individuos
