"""Lógica metodológica Alkire-Foster: scores dimensionales, cortes, matrices y métricas agregadas."""
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.config import (
    CODIGOS_NS_NC,
    DEFAULT_K_INTER,
    DEFAULT_K_INTRA,
    DEFAULT_YEAR,
    DIMENSIONES_IPM,
    EPS,
    IndicatorRateMode,
    MAP_DOMINIO,
    get_dimensiones_ipm,
)


@dataclass(frozen=True)
class IPMMetrics:
    """Métricas agregadas del Índice de Pobreza Multidimensional (Alkire-Foster)."""

    h: float                   # Incidencia (proporción de hogares pobres, 0 a 1)
    a: float                   # Intensidad (privación media entre los pobres, 0 a 1)
    m0: float                  # Tasa de recuento ajustada (H * A = media de c_censurado)
    hogares_expandidos: int    # Total ponderado de hogares (o personas según fexp activo)
    pobres_expandidos: int     # Total ponderado de hogares (o personas) pobres IPM


def score_dimension(df: pd.DataFrame, variables: list[str]) -> pd.Series:
    """Calcula la proporción de indicadores privados (== 1) sobre los válidos (no NaN)."""
    cols = [v for v in variables if v in df.columns]
    if not cols:
        return pd.Series(np.nan, index=df.index)
    sub = df[cols]
    validos = sub.notna().sum(axis=1)
    return (sub == 1).sum(axis=1) / validos.where(validos > 0)


def prepare_base_scores(
    df_hogares: pd.DataFrame,
    dimensiones: dict = DIMENSIONES_IPM,
    codigos_ns_nc: list[int] = CODIGOS_NS_NC,
) -> pd.DataFrame:
    """Filtra el universo con respuesta al módulo PM y calcula los scores continuos por dimensión."""
    df = df_hogares.copy()

    if "ent_rea_pm" in df.columns:
        df = df[df["ent_rea_pm"] == 1].copy()
    elif "enr_rea_pm" in df.columns:
        df = df[df["enr_rea_pm"] == 1].copy()

    if "tipoho_3" not in df.columns and "tipoho" in df.columns:
        df["tipoho_3"] = df["tipoho"]

    df["tiene_nnya"] = (df["hog_per_0a17"] == 1).astype(int)
    df["pobre_ingreso"] = df["i_pobreza"].isin([1, 2]).astype(int) if "i_pobreza" in df.columns else 0
    df["dominio_desc"] = df["dominio"].map(MAP_DOMINIO).fillna("Otro") if "dominio" in df.columns else "Sin especificar"

    if codigos_ns_nc:
        vars_pm = {
            v
            for d in dimensiones.values()
            for grupo in ("con_nnya", "sin_nnya")
            for v in d[grupo]
            if v in df.columns
        }
        if vars_pm:
            df[list(vars_pm)] = df[list(vars_pm)].replace(codigos_ns_nc, np.nan)

    for dim_key, dim_cfg in dimensiones.items():
        score_con = score_dimension(df, list(dim_cfg["con_nnya"]))
        score_sin = score_dimension(df, list(dim_cfg["sin_nnya"]))
        df[f"{dim_key}_score"] = np.where(df["tiene_nnya"] == 1, score_con, score_sin)

    return df.copy()


def apply_ipm_cutoffs(
    df_scores: pd.DataFrame,
    k_intra: float = DEFAULT_K_INTRA,
    k_inter: float = DEFAULT_K_INTER,
    dimensiones: dict = DIMENSIONES_IPM,
) -> pd.DataFrame:
    """Aplica el doble corte (k_intra, k_inter) construyendo las matrices no censurada y censurada."""
    df = df_scores.copy()
    total_dims = len(dimensiones)
    priv_cols: list[str] = []

    # 1. Matriz de privaciones dimensionales NO censurada g0 (n x d)
    for dim_key in dimensiones:
        col_priv = f"{dim_key}_privada"
        df[col_priv] = (df[f"{dim_key}_score"] >= k_intra - EPS).astype(int)
        priv_cols.append(col_priv)

    # 2. Vector de conteo NO censurado c_i e identificación de pobreza multidimensional
    df["cant_dim_privadas"] = df[priv_cols].sum(axis=1)
    df["c_vector"] = df["cant_dim_privadas"] / total_dims
    df["pobre_ipm"] = (df["c_vector"] >= k_inter - EPS).astype(int)

    # 3. Matriz de privaciones dimensionales CENSURADA g0(k) y vector censurado c_i(k)
    for dim_key in dimensiones:
        df[f"{dim_key}_censurada"] = df[f"{dim_key}_privada"] * df["pobre_ipm"]
    df["c_censurado"] = df["c_vector"] * df["pobre_ipm"]

    return df.copy()


def calculate_ipm_dataset(
    df_hogares: pd.DataFrame,
    k_intra: float = DEFAULT_K_INTRA,
    k_inter: float = DEFAULT_K_INTER,
    dimensiones: dict | None = None,
    df_individuos: pd.DataFrame | None = None,
    year: int = DEFAULT_YEAR,
) -> pd.DataFrame:
    """Ejecuta el pipeline completo de preparación, enriquecimiento con individuos (opcional) y cortes del IPM."""
    from src.data import enrich_hogares_with_individuos

    dims = dimensiones if dimensiones is not None else get_dimensiones_ipm(year)
    base_hog = (
        enrich_hogares_with_individuos(df_hogares, df_individuos)
        if df_individuos is not None
        else df_hogares
    )
    return apply_ipm_cutoffs(prepare_base_scores(base_hog, dims), k_intra, k_inter, dims)


def calculate_ipm_metrics(data: pd.DataFrame) -> IPMMetrics:
    """Calcula H, A, M0 y totales de hogares ponderados por fexp."""
    if data.empty or data["fexp"].sum() == 0:
        return IPMMetrics(h=0.0, a=0.0, m0=0.0, hogares_expandidos=0, pobres_expandidos=0)

    w = data["fexp"]
    pobres = data[data["pobre_ipm"] == 1]

    h = float(np.average(data["pobre_ipm"], weights=w))
    a = float(np.average(pobres["c_vector"], weights=pobres["fexp"])) if not pobres.empty else 0.0
    m0 = float(h * a)

    return IPMMetrics(
        h=h,
        a=a,
        m0=m0,
        hogares_expandidos=int(round(w.sum())),
        pobres_expandidos=int(round((data["pobre_ipm"] * w).sum())),
    )


def calculate_income_poverty_rate(data: pd.DataFrame) -> float:
    """Calcula el porcentaje ponderado de hogares pobres por ingresos."""
    if data.empty or "pobre_ingreso" not in data.columns or data["fexp"].sum() == 0:
        return 0.0
    return float(np.average(data["pobre_ingreso"], weights=data["fexp"]) * 100)


def calculate_indicator_rate(
    data: pd.DataFrame,
    variable: str,
    modo: IndicatorRateMode = "no_censurada",
) -> float | None:
    """Calcula la tasa ponderada de privación en un indicador según el modo de matriz elegido."""
    if variable not in data.columns or data.empty:
        return None

    universo = data[data["pobre_ipm"] == 1] if modo == "entre_pobres" else data
    validos = universo[variable].notna() & (universo[variable] != 9)
    peso_base = universo.loc[validos, "fexp"].sum()
    if peso_base == 0:
        return None

    privados = validos & (universo[variable] == 1)
    if modo == "censurada":
        privados = privados & (universo["pobre_ipm"] == 1)

    peso_privado = universo.loc[privados, "fexp"].sum()
    return float(peso_privado / peso_base * 100)


def calculate_poverty_overlap(data: pd.DataFrame) -> dict[str, float]:
    """Calcula la matriz de superposición entre pobreza multidimensional y por ingresos (%)."""
    empty = {
        "Pobreza estructural": 0.0,
        "Solo pobreza multidimensional": 0.0,
        "Solo pobreza por ingresos": 0.0,
        "No pobre": 0.0,
    }
    if data.empty or "pobre_ingreso" not in data.columns or data["fexp"].sum() == 0:
        return empty

    w = data["fexp"]
    total_w = w.sum()
    ipm = data["pobre_ipm"] == 1
    ing = data["pobre_ingreso"] == 1

    return {
        "Pobreza estructural": float(w[ipm & ing].sum() / total_w * 100),
        "Solo pobreza multidimensional": float(w[ipm & ~ing].sum() / total_w * 100),
        "Solo pobreza por ingresos": float(w[~ipm & ing].sum() / total_w * 100),
        "No pobre": float(w[~ipm & ~ing].sum() / total_w * 100),
    }


def calculate_deprivation_distribution(data: pd.DataFrame) -> dict[int, float]:
    """Distribución porcentual de dimensiones privadas simultáneas (2 a 5) entre los hogares pobres."""
    pobres = data[data["pobre_ipm"] == 1]
    if pobres.empty or pobres["fexp"].sum() == 0:
        return {k: 0.0 for k in range(2, 6)}

    total_pobres_w = pobres["fexp"].sum()
    return {
        k: float(pobres.loc[pobres["cant_dim_privadas"] == k, "fexp"].sum() / total_pobres_w * 100)
        for k in range(2, 6)
    }


def calculate_dimension_contributions(
    data: pd.DataFrame,
    dimensiones: dict = DIMENSIONES_IPM,
) -> dict[str, float]:
    """Contribución porcentual de cada dimensión al índice M0 sobre la matriz censurada."""
    if data.empty:
        return {d["label"]: 0.0 for d in dimensiones.values()}

    w = data["fexp"]
    pesos_censurados = {
        d["label"]: float(((data[f"{k}_privada"] * data["pobre_ipm"]) * w).sum())
        for k, d in dimensiones.items()
        if f"{k}_privada" in data.columns
    }
    total_censurado = sum(pesos_censurados.values())
    if total_censurado == 0:
        return {d["label"]: 0.0 for d in dimensiones.values()}

    return {label: val / total_censurado * 100 for label, val in pesos_censurados.items()}


def _weighted_valid_rate(data: pd.DataFrame, cond: pd.Series, valid: pd.Series) -> float:
    peso_valido = data.loc[valid, "fexp"].sum()
    if peso_valido == 0:
        return 0.0
    return float(data.loc[valid & cond, "fexp"].sum() / peso_valido * 100)


def calculate_structural_habitat_rates(data: pd.DataFrame) -> dict[str, float]:
    """Tasas ponderadas de privaciones estructurales de hábitat y vivienda en la EAH."""
    if data.empty:
        return {}

    res: dict[str, float] = {}
    if "h2" in data.columns:
        res["Tenencia irregular"] = _weighted_valid_rate(
            data, data["h2"] == 3, ~data["h2"].isin([0, 9])
        )
    if "hacinam_2" in data.columns:
        valid_hac = data["hacinam_2"] != 9
        res["Hacinamiento general (2 o más personas por cuarto)"] = _weighted_valid_rate(
            data, data["hacinam_2"].isin([2, 3]), valid_hac
        )
        res["Hacinamiento crítico (más de 3 personas por cuarto)"] = _weighted_valid_rate(
            data, data["hacinam_2"] == 3, valid_hac
        )
    if "v12" in data.columns:
        res["Sin desagüe a red cloacal(*)"] = _weighted_valid_rate(
            data, data["v12"].isin([2, 3, 4]), ~data["v12"].isin([0, 9])
        )
    if "h1" in data.columns:
        res["Baño compartido con otro hogar"] = _weighted_valid_rate(
            data, data["h1"] == 2, data["h1"] != 9
        )
    if "hpm4" in data.columns:
        res["Asistencia a comedor o merendero comunitario"] = _weighted_valid_rate(
            data, data["hpm4"] == 1, ~data["hpm4"].isin([0, 9])
        )
    return res
