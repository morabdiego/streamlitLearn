"""Lógica de negocio y cálculo metodológico de Alkire-Foster para el IPM.

Este módulo es completamente independiente de Streamlit y de la interfaz de usuario,
permitiendo pruebas unitarias y reutilización.
"""
import numpy as np
import pandas as pd

from src.config.constants import (
    CODIGOS_NO_APLICA,
    DIMENSIONES_INDICADORES_IPM,
    EPS,
    MAP_DOMINIO,
    MAP_TIPO_HOGAR,
)
from src.domain.models import IPMMetrics


def score_dimension(df: pd.DataFrame, variables: list[str]) -> pd.Series:
    """Calcula la proporción de indicadores privados sobre los aplicables (no NaN)."""
    existing_vars = [v for v in variables if v in df.columns]
    if not existing_vars:
        return pd.Series(np.nan, index=df.index)

    sub_df = df[existing_vars]
    privados = (sub_df == 1).sum(axis=1)
    validos = sub_df.notna().sum(axis=1)
    return privados / validos.where(validos > 0)


def prepare_base_scores(
    df_hogares: pd.DataFrame,
    dimensiones: dict = DIMENSIONES_INDICADORES_IPM,
    codigos_no_aplica: list[int] = CODIGOS_NO_APLICA,
) -> pd.DataFrame:
    """Prepara el DataFrame base calculando scores dimensionales continuos.

    Esta etapa es independiente de los umbrales k_intra y k_inter,
    por lo que puede ser calculada y cacheada eficientemente.
    """
    df = df_hogares.copy()

    # Filtro de respuesta del módulo de privaciones (ent_rea_pm == 1 en EAH)
    if "ent_rea_pm" in df.columns:
        df = df[df["ent_rea_pm"] == 1].copy()
    elif "enr_rea_pm" in df.columns:
        df = df[df["enr_rea_pm"] == 1].copy()

    # Presencia de NNyA (hog_per_0a17: 1 = hay, 2 = no hay)
    df["tiene_nnya"] = (df["hog_per_0a17"] == 1).astype(int)

    # Condición de pobreza por ingresos (i_pobreza 1: Indigente, 2: Pobre no indigente)
    if "i_pobreza" in df.columns:
        df["pobre_ingreso"] = df["i_pobreza"].isin([1, 2]).astype(int)
    else:
        df["pobre_ingreso"] = 0

    # Códigos de no aplica / no responde -> NaN
    if codigos_no_aplica:
        todas_vars = {
            v
            for d in dimensiones.values()
            for grupo in ("hogares_con_nnya", "hogares_sin_nnya")
            for v in d[grupo]
            if v in df.columns
        }
        df[list(todas_vars)] = df[list(todas_vars)].replace(codigos_no_aplica, np.nan)

    # Cálculo continuo del score por dimensión
    for dim_key, dim_val in dimensiones.items():
        col_dim_score = f"{dim_key}_score"
        vars_con = list(dim_val["hogares_con_nnya"].keys())
        vars_sin = list(dim_val["hogares_sin_nnya"].keys())

        score_con = score_dimension(df, vars_con)
        score_sin = score_dimension(df, vars_sin)

        df[col_dim_score] = np.where(df["tiene_nnya"] == 1, score_con, score_sin)

    # Mapeo descriptivo del dominio geográfico
    if "dominio" in df.columns:
        df["dominio_desc"] = df["dominio"].map(MAP_DOMINIO).fillna("Otro")
    else:
        df["dominio_desc"] = "Sin especificar"

    return df


def apply_ipm_cutoffs(
    df_scores: pd.DataFrame,
    k_intra: float,
    k_inter: float,
    dimensiones: dict = DIMENSIONES_INDICADORES_IPM,
    eps: float = EPS,
) -> pd.DataFrame:
    """Aplica los umbrales metodológicos k-intra y k-inter (Alkire-Foster dual-cutoff)."""
    df = df_scores.copy()
    dim_cols = []

    # 1. Corte intra-dimensional
    for dim_key in dimensiones.keys():
        col_dim_score = f"{dim_key}_score"
        col_dim_priv = f"{dim_key}_privada"
        dim_cols.append(col_dim_priv)
        df[col_dim_priv] = (df[col_dim_score] >= k_intra - eps).astype(int)

    # 2. Agregación inter-dimensional
    total_dimensiones = len(dimensiones)
    df["cant_dim_privadas"] = df[dim_cols].sum(axis=1)
    df["c_vector"] = df["cant_dim_privadas"] / total_dimensiones

    # 3. Identificación y vector censurado
    df["pobre_ipm"] = (df["c_vector"] >= k_inter - eps).astype(int)
    df["c_censurado"] = np.where(df["pobre_ipm"] == 1, df["c_vector"], 0.0)

    return df


def calculate_ipm_dataset(
    df_hogares: pd.DataFrame,
    k_intra: float,
    k_inter: float,
    dimensiones: dict = DIMENSIONES_INDICADORES_IPM,
    codigos_no_aplica: list[int] = CODIGOS_NO_APLICA,
) -> pd.DataFrame:
    """Pipeline completo de cálculo de IPM desde datos crudos."""
    df_base = prepare_base_scores(df_hogares, dimensiones, codigos_no_aplica)
    return apply_ipm_cutoffs(df_base, k_intra, k_inter, dimensiones)


def filter_ipm_dataset(
    df: pd.DataFrame,
    dominios_seleccionados: list[str],
    tipos_hogar_seleccionados: list[str],
) -> pd.DataFrame:
    """Filtra el DataFrame según dominio geográfico y presencia de NNyA."""
    filtered = df.copy()

    if dominios_seleccionados:
        filtered = filtered[filtered["dominio_desc"].isin(dominios_seleccionados)]

    if tipos_hogar_seleccionados:
        codigos_tipo = [
            MAP_TIPO_HOGAR[tipo]
            for tipo in tipos_hogar_seleccionados
            if tipo in MAP_TIPO_HOGAR
        ]
        filtered = filtered[filtered["tiene_nnya"].isin(codigos_tipo)]

    return filtered


def calculate_ipm_metrics(data: pd.DataFrame) -> IPMMetrics:
    """Calcula las métricas de pobreza multidimensional ponderadas por fexp."""
    if len(data) == 0:
        return IPMMetrics(h=0.0, a=0.0, m0=0.0, hogares_expandidos=0, pobres_expandidos=0)

    w = data["fexp"]
    sum_w = w.sum()

    # Incidencia (H)
    h = float(np.average(data["pobre_ipm"], weights=w))

    # Intensidad (A) entre los pobres
    pobres = data[data["pobre_ipm"] == 1]
    if len(pobres) > 0:
        a = float(np.average(pobres["c_vector"], weights=pobres["fexp"]))
    else:
        a = 0.0

    # Tasa M0 ajustada
    m0 = float(h * a)

    hogares_expandidos = int(round(sum_w))
    pobres_expandidos = int(round((data["pobre_ipm"] * w).sum()))

    return IPMMetrics(
        h=h,
        a=a,
        m0=m0,
        hogares_expandidos=hogares_expandidos,
        pobres_expandidos=pobres_expandidos,
    )


def calculate_indicator_rate(
    data: pd.DataFrame,
    variable: str,
    censurado: bool = False,
) -> float | None:
    """Calcula el porcentaje ponderado de privación en un indicador específico.

    Si censurado=True, contabiliza como privados únicamente a aquellos hogares que sufren la
    carencia en el indicador (variable == 1) Y además son identificados como pobres
    multidimensionales (pobre_ipm == 1), tal como en las Tablas A.4, A.5 y A.6 de la tesis.
    """
    if variable not in data.columns:
        return None

    validos = data[variable].notna()
    peso_aplicable = data.loc[validos, "fexp"].sum()
    if peso_aplicable == 0:
        return None

    cond_privado = validos & (data[variable] == 1)
    if censurado and "pobre_ipm" in data.columns:
        cond_privado = cond_privado & (data["pobre_ipm"] == 1)

    peso_privado = data.loc[cond_privado, "fexp"].sum()
    return float(peso_privado / peso_aplicable * 100)


def calculate_poverty_overlap(data: pd.DataFrame) -> dict[str, float]:
    """Calcula la matriz de superposición entre pobreza por ingresos y multidimensional."""
    if len(data) == 0 or "pobre_ingreso" not in data.columns:
        return {
            "Doble pobreza (Crónica)": 0.0,
            "Solo pobreza multidimensional": 0.0,
            "Solo pobreza por ingresos": 0.0,
            "No pobre en ninguna": 0.0,
        }

    total_w = data["fexp"].sum()
    if total_w == 0:
        return {
            "Doble pobreza (Crónica)": 0.0,
            "Solo pobreza multidimensional": 0.0,
            "Solo pobreza por ingresos": 0.0,
            "No pobre en ninguna": 0.0,
        }

    ambos = (data["pobre_ipm"] == 1) & (data["pobre_ingreso"] == 1)
    solo_ipm = (data["pobre_ipm"] == 1) & (data["pobre_ingreso"] == 0)
    solo_ing = (data["pobre_ipm"] == 0) & (data["pobre_ingreso"] == 1)
    ninguno = (data["pobre_ipm"] == 0) & (data["pobre_ingreso"] == 0)

    return {
        "Doble pobreza (Crónica)": float(data.loc[ambos, "fexp"].sum() / total_w * 100),
        "Solo pobreza multidimensional": float(data.loc[solo_ipm, "fexp"].sum() / total_w * 100),
        "Solo pobreza por ingresos": float(data.loc[solo_ing, "fexp"].sum() / total_w * 100),
        "No pobre en ninguna": float(data.loc[ninguno, "fexp"].sum() / total_w * 100),
    }


def calculate_deprivation_distribution(data: pd.DataFrame) -> dict[int, float]:
    """Calcula la distribución porcentual de privaciones simultáneas (2 a 5) entre los pobres."""
    pobres = data[data["pobre_ipm"] == 1]
    if len(pobres) == 0:
        return {2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0}

    total_pobres_w = pobres["fexp"].sum()
    dist = {}
    for k in range(2, 6):
        peso_k = pobres.loc[pobres["cant_dim_privadas"] == k, "fexp"].sum()
        dist[k] = float(peso_k / total_pobres_w * 100)
    return dist


def calculate_dimension_contributions(
    data: pd.DataFrame,
    dimensiones: dict = DIMENSIONES_INDICADORES_IPM,
) -> dict[str, float]:
    """Calcula la contribución porcentual de cada dimensión a la tasa M0 de Alkire-Foster."""
    metrics = calculate_ipm_metrics(data)
    if metrics.m0 == 0:
        return {d_val["meta"]["label"]: 0.0 for d_val in dimensiones.values()}

    total_w = data["fexp"].sum()
    d_count = len(dimensiones)
    denominador = total_w * d_count * metrics.m0

    contributions = {}
    for dim_key, dim_val in dimensiones.items():
        col_priv = f"{dim_key}_privada"
        if col_priv in data.columns:
            numerador = (data[col_priv] * data["pobre_ipm"] * data["fexp"]).sum()
            contributions[dim_val["meta"]["label"]] = float(numerador / denominador * 100)
        else:
            contributions[dim_val["meta"]["label"]] = 0.0

    return contributions


def calculate_structural_habitat_rates(data: pd.DataFrame) -> dict[str, float]:
    """Calcula tasas ponderadas de privaciones estructurales de hábitat y vivienda en la EAH."""
    if len(data) == 0:
        return {}

    w = data["fexp"]
    res = {}

    if "h2" in data.columns:
        res["Tenencia irregular / precaria de la vivienda (sin título de propiedad)"] = float(
            np.average(data["h2"] == 3, weights=w) * 100
        )
    if "hacinam_2" in data.columns:
        res["Hacinamiento general (2 o más personas por cuarto)"] = float(
            np.average(data["hacinam_2"].isin([2, 3]), weights=w) * 100
        )
        res["Hacinamiento crítico (más de 3 personas por cuarto)"] = float(
            np.average(data["hacinam_2"] == 3, weights=w) * 100
        )
    if "v12" in data.columns:
        res["Sin desagüe a red cloacal pública (pozo, cámara séptica o letrina)"] = float(
            np.average(data["v12"] != 1, weights=w) * 100
        )
    if "h1" in data.columns:
        res["Baño compartido con otro hogar"] = float(
            np.average(data["h1"] == 2, weights=w) * 100
        )
    if "hpm4" in data.columns:
        res["Asistencia a comedor o merendero comunitario (último mes)"] = float(
            np.average(data["hpm4"] == 1, weights=w) * 100
        )

    return res
