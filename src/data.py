"""Carga de microdatos de hogares e individuos, enriquecimiento, caché y filtrado."""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import AnalysisUnit, DATA_DIR, DEFAULT_K_INTER, DEFAULT_K_INTRA, DEFAULT_YEAR
from src.ipm import calculate_ipm_dataset


def load_hogares_data(year: int | str = DEFAULT_YEAR, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Carga la base de hogares de la EAH para el año indicado."""
    year_str = str(year)
    file_path = data_dir / year_str / f"eah{year_str}_bu_ampliada_hog.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de microdatos: {file_path}")
    return pd.read_csv(file_path, sep=";")


def load_individuos_data(year: int | str = DEFAULT_YEAR, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Carga la base de individuos (personas) de la EAH para el año indicado."""
    year_str = str(year)
    file_path = data_dir / year_str / f"eah{year_str}_bu_ampliada_ind.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de microdatos de individuos: {file_path}")
    return pd.read_csv(file_path, sep=";")


def enrich_hogares_with_individuos(
    df_hogares: pd.DataFrame,
    df_individuos: pd.DataFrame,
) -> pd.DataFrame:
    """Cruza la base de hogares con la de individuos (por id + nhogar) para incorporar:
    - cant_miembros: cantidad de integrantes del hogar
    - fexp_hogares y fexp_personas (fexp * cant_miembros)
    - Variables del jefe/a de hogar (parentes_5 == 1 en 2025, parentes_2 == 1 en 2021): sexo, estado, dh2, dh3.
    - Armonización de tipoho (2021) a tipoho_3 (2025).
    """
    df = df_hogares.copy()
    if "tipoho_3" not in df.columns and "tipoho" in df.columns:
        df["tipoho_3"] = df["tipoho"]

    conteo = (
        df_individuos.groupby(["id", "nhogar"], as_index=False)
        .agg(cant_miembros=("miembro", "count"))
    )

    col_parentes = "parentes_5" if "parentes_5" in df_individuos.columns else "parentes_2"
    cols_jefe = [c for c in ("sexo", "estado", "dh2", "dh3") if c in df_individuos.columns]
    jefe = (
        df_individuos[df_individuos[col_parentes] == 1][["id", "nhogar", *cols_jefe]]
        .drop_duplicates(subset=["id", "nhogar"])
    )

    df = df.merge(conteo, on=["id", "nhogar"], how="left")
    df = df.merge(jefe, on=["id", "nhogar"], how="left")

    df["cant_miembros"] = df["cant_miembros"].fillna(1).astype(int)
    df["fexp_hogares"] = df["fexp"]
    df["fexp_personas"] = df["fexp_hogares"] * df["cant_miembros"]
    df["n_muestra"] = 1
    return df.copy()


def apply_analysis_unit(df: pd.DataFrame, unidad: AnalysisUnit = "hogares") -> pd.DataFrame:
    """Ajusta el factor de expansión (fexp) y el conteo muestral según la unidad de análisis ('hogares' o 'personas')."""
    out = df.copy()
    if unidad == "personas":
        if "fexp_personas" in out.columns:
            out["fexp"] = out["fexp_personas"]
        elif "cant_miembros" in out.columns:
            out["fexp"] = out["fexp"] * out["cant_miembros"]
        out["n_muestra"] = out["cant_miembros"] if "cant_miembros" in out.columns else 1
    else:
        if "fexp_hogares" in out.columns:
            out["fexp"] = out["fexp_hogares"]
        out["n_muestra"] = 1
    return out


def filter_ipm_dataset(df: pd.DataFrame, filters: dict[str, list[int]]) -> pd.DataFrame:
    """Filtra el DataFrame de hogares según los valores seleccionados en cada variable."""
    out = df
    for col, selected_codes in filters.items():
        if selected_codes and col in out.columns:
            out = out[out[col].isin(selected_codes)]
    return out


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
