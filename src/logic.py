"""Lógica de carga de datos, cálculo Alkire-Foster y construcción de tablas analíticas."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd

from src.config import (
    CODIGOS_NS_NC,
    DATA_DIR,
    DEFAULT_K_INTER,
    DEFAULT_K_INTRA,
    DEFAULT_YEAR,
    DIMENSIONES_IPM,
    DOMINIO_LABELS_MUESTRA,
    EPS,
    MAP_DOMINIO,
)
from src.texts import ESTRUCTURA_2025_MATRIZ, INDICADORES_EXCLUIDOS_MODULO_PM

IndicatorRateMode = Literal["no_censurada", "censurada", "entre_pobres"]


@dataclass(frozen=True)
class IPMMetrics:
    """Métricas agregadas del Índice de Pobreza Multidimensional (Alkire-Foster)."""

    h: float                   # Incidencia (proporción de hogares pobres, 0 a 1)
    a: float                   # Intensidad (privación media entre los pobres, 0 a 1)
    m0: float                  # Tasa de recuento ajustada (H * A = media de c_censurado)
    hogares_expandidos: int    # Total ponderado de hogares
    pobres_expandidos: int     # Total ponderado de hogares pobres IPM


# =============================================================================
# 1. CARGA DE DATOS Y FORMATEO NUMÉRICO
# =============================================================================


def load_hogares_data(year: int | str = DEFAULT_YEAR, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Carga la base de hogares de la EAH para el año indicado."""
    year_str = str(year)
    file_path = data_dir / year_str / f"eah{year_str}_bu_ampliada_hog.txt"
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de microdatos: {file_path}")
    return pd.read_csv(file_path, sep=";")


def format_decimal(valor: Any, decimales: int = 1) -> str:
    """Formatea un número flotante con coma decimal y punto separador de miles."""
    if valor is None or pd.isna(valor):
        return "—"
    try:
        val = float(valor)
        return f"{val:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(valor)


def format_integer(valor: Any) -> str:
    """Formatea un número entero con punto separador de miles."""
    if valor is None or pd.isna(valor):
        return "—"
    try:
        val = int(round(float(valor)))
        return f"{val:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)


def format_percentage(valor: Any, decimales: int = 1) -> str:
    """Formatea un valor porcentual (0 a 100) con sufijo %."""
    if valor is None or pd.isna(valor):
        return "—"
    return f"{format_decimal(valor, decimales)}%"


def format_df_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """Formatea todas las celdas de un DataFrame como porcentajes."""
    return df.map(format_percentage)


# =============================================================================
# 2. CÁLCULO METODOLÓGICO ALKIRE-FOSTER (MATRIZ NO CENSURADA Y CENSURADA)
# =============================================================================


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

    return df


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
    # Los hogares no pobres reciben 0 en todas las dimensiones pero permanecen en la matriz (n filas).
    for dim_key in dimensiones:
        df[f"{dim_key}_censurada"] = df[f"{dim_key}_privada"] * df["pobre_ipm"]
    df["c_censurado"] = df["c_vector"] * df["pobre_ipm"]

    return df


def calculate_ipm_dataset(
    df_hogares: pd.DataFrame,
    k_intra: float = DEFAULT_K_INTRA,
    k_inter: float = DEFAULT_K_INTER,
    dimensiones: dict = DIMENSIONES_IPM,
) -> pd.DataFrame:
    """Ejecuta el pipeline completo de preparación y cortes del IPM."""
    return apply_ipm_cutoffs(prepare_base_scores(df_hogares, dimensiones), k_intra, k_inter, dimensiones)


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
    """Calcula la tasa ponderada de privación en un indicador según el modo de matriz elegido:

    - 'no_censurada': % de hogares privados sobre el total de hogares válidos (h_j).
    - 'censurada': % de hogares privados Y pobres IPM sobre el total de hogares válidos (h_j(k)).
    - 'entre_pobres': % de hogares privados dentro del universo exclusivo de hogares pobres IPM (h_j(k) / H).
    """
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


# =============================================================================
# 3. CONSTRUCTORES DE TABLAS LISTAS PARA RENDERIZAR
# =============================================================================


def _dominios_presentes(df: pd.DataFrame) -> list[str]:
    return [d for d in MAP_DOMINIO.values() if d in df["dominio_desc"].unique()]


def build_sample_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 2: Distribución muestral y expandida de hogares con respuesta al módulo PM."""
    tot_n = len(df)
    tot_w = df["fexp"].sum()
    rows = []

    for dom_code, dom_label in DOMINIO_LABELS_MUESTRA.items():
        sub = df[df["dominio"] == dom_code]
        rows.append({
            "Marco muestral (hogares con módulo PM)": dom_label,
            "Muestra": format_integer(len(sub)),
            "% Muestra": format_percentage(len(sub) / tot_n * 100 if tot_n else 0),
            "Población": format_integer(sub["fexp"].sum()),
            "% Población": format_percentage(sub["fexp"].sum() / tot_w * 100 if tot_w else 0),
        })

    rows.append({
        "Marco muestral (hogares con módulo PM)": "Total de hogares",
        "Muestra": format_integer(tot_n),
        "% Muestra": "100,0%",
        "Población": format_integer(tot_w),
        "% Población": "100,0%",
    })
    return pd.DataFrame(rows)


def build_domain_poverty_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 3: Métricas Alkire-Foster y pobreza por ingresos según dominio muestral."""
    grupos = [(d, df[df["dominio_desc"] == d]) for d in _dominios_presentes(df)]
    if not df.empty:
        grupos.append(("Total de hogares", df))

    rows = []
    for label, sub in grupos:
        if sub.empty:
            continue
        m = calculate_ipm_metrics(sub)
        rows.append({
            "Marco muestral (hogares con módulo PM)": label,
            "Pobreza multidimensional (H)": format_percentage(m.h * 100),
            "Intensidad (A)": format_percentage(m.a * 100),
            "IPM (M0)": format_decimal(m.m0, decimales=3),
            "Pobreza por ingresos": format_percentage(calculate_income_poverty_rate(sub)),
        })
    return pd.DataFrame(rows)


def build_overlap_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 4: Matriz de pobreza estructural (IPM × ingresos) por dominio."""
    cols = {d: calculate_poverty_overlap(df[df["dominio_desc"] == d]) for d in _dominios_presentes(df)}
    if not df.empty:
        cols["Total CABA"] = calculate_poverty_overlap(df)
    return format_df_percentages(pd.DataFrame(cols))


def build_deprivation_dist_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 5: Cantidad de dimensiones privadas simultáneas entre los hogares pobres."""
    cols = {}
    for d in _dominios_presentes(df):
        dist = calculate_deprivation_distribution(df[df["dominio_desc"] == d])
        cols[d] = {f"{k} dimensiones privadas": dist[k] for k in range(2, 6)}
    return format_df_percentages(pd.DataFrame(cols))


def build_structure_2025_table() -> pd.DataFrame:
    """Tabla 6: Matriz de dimensiones e indicadores finales EAH 2025 (27 filas)."""
    return pd.DataFrame([
        {
            "Dimensión": dim,
            "Indicador": ind,
            "Sin menores de 18": en_sin,
            "Con menores de 18": en_con,
        }
        for dim, indicadores in ESTRUCTURA_2025_MATRIZ.items()
        for ind, (en_sin, en_con) in indicadores.items()
    ])


def build_dimension_contributions_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 7: Contribución porcentual de cada dimensión al índice M0."""
    cols = {}
    if not df.empty:
        cols["Total CABA"] = calculate_dimension_contributions(df)
    for d in _dominios_presentes(df):
        cols[d] = calculate_dimension_contributions(df[df["dominio_desc"] == d])
    return format_df_percentages(pd.DataFrame(cols))


def build_excluded_indicators_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 8: Tasas de privación en villas vs. resto para indicadores descartados del IPM."""
    villas = df[df["dominio"] == 3]
    resto = df[df["dominio"] == 4]

    filtro_grupo = {
        "Hogares sin NNyA": lambda sub: sub[sub["tiene_nnya"] == 0],
        "Hogares con NNyA": lambda sub: sub[sub["tiene_nnya"] == 1],
    }

    rows = []
    for item in INDICADORES_EXCLUIDOS_MODULO_PM:
        var = item["variable"]
        univ = item["universo_excluido"]
        filtrar = filtro_grupo.get(univ, lambda sub: sub)

        t_v = calculate_indicator_rate(filtrar(villas), var, modo="no_censurada")
        t_r = calculate_indicator_rate(filtrar(resto), var, modo="no_censurada")

        rows.append({
            "Variable": var,
            "Indicador": item["etiqueta"],
            "Dimensión": item["dimension"],
            "Grupo donde se excluye": univ,
            "Incidencia en villas": format_percentage(t_v),
            "Incidencia resto de la ciudad": format_percentage(t_r),
            "Discusión metodológica": item["motivo_exclusion"],
        })
    return pd.DataFrame(rows)


def build_habitat_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 9: Indicadores estructurales de hábitat y vivienda omitidos del IPM oficial."""
    cols = {d: calculate_structural_habitat_rates(df[df["dominio_desc"] == d]) for d in _dominios_presentes(df)}
    if not df.empty:
        cols["Total CABA"] = calculate_structural_habitat_rates(df)
    return format_df_percentages(pd.DataFrame(cols))


def build_nnya_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla 10: Resumen de métricas según presencia de menores de 18 años en el hogar."""
    rows = []
    for codigo, nombre in [(1, "Hogares con NNyA"), (0, "Hogares sin NNyA")]:
        sub = df[df["tiene_nnya"] == codigo]
        if sub.empty:
            continue
        m = calculate_ipm_metrics(sub)
        rows.append({
            "Tipo de hogar": nombre,
            "Pobreza multidimensional (H)": format_percentage(m.h * 100),
            "Intensidad (A)": format_percentage(m.a * 100),
            "IPM (M0)": format_decimal(m.m0, decimales=3),
            "Pobreza por ingresos": format_percentage(calculate_income_poverty_rate(sub)),
            "Muestra (N)": format_integer(len(sub)),
            "Hogares expandidos": format_integer(m.hogares_expandidos),
        })
    return pd.DataFrame(rows)


def build_indicator_rates_table(
    df: pd.DataFrame,
    tiene_nnya: int,
    modo: IndicatorRateMode = "no_censurada",
    dimensiones: dict = DIMENSIONES_IPM,
) -> pd.DataFrame:
    """Tablas 11 y 12: Tasas de privación por indicador según tipo de hogar, dominio y modo."""
    grupo_key = "con_nnya" if tiene_nnya == 1 else "sin_nnya"
    df_grupo = df[df["tiene_nnya"] == tiene_nnya]
    dominios = _dominios_presentes(df)

    rows = []
    for dim_cfg in dimensiones.values():
        for variable, etiqueta in dim_cfg[grupo_key].items():
            rec: dict[str, str] = {
                "Dimensión": dim_cfg["label"],
                "Indicador": etiqueta,
            }
            for d in dominios:
                t_dom = calculate_indicator_rate(df_grupo[df_grupo["dominio_desc"] == d], variable, modo=modo)
                rec[f"{d} (%)"] = format_percentage(t_dom)
            rec["Total CABA (%)"] = format_percentage(
                calculate_indicator_rate(df_grupo, variable, modo=modo)
            )
            rows.append(rec)
    return pd.DataFrame(rows)
