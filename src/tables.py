"""Constructores unificados de tablas analíticas para la vista de Análisis y el Monitor Interactivo."""
import pandas as pd

from src.config import (
    AnalysisUnit,
    DEFAULT_YEAR,
    DOMINIO_LABELS_MUESTRA,
    IndicatorRateMode,
    get_dimensiones_ipm,
)
from src.config_monitor import MONITOR_FILTER_CONFIG
from src.formatting import (
    format_decimal,
    format_df_percentages,
    format_integer,
    format_percentage,
)
from src.ipm import (
    calculate_deprivation_distribution,
    calculate_dimension_contributions,
    calculate_income_poverty_rate,
    calculate_indicator_rate,
    calculate_ipm_metrics,
    calculate_poverty_overlap,
    calculate_structural_habitat_rates,
)
from src.texts import ESTRUCTURA_2025_MATRIZ, INDICADORES_EXCLUIDOS_MODULO_PM


def _sample_count(df: pd.DataFrame) -> int:
    """Devuelve el tamaño muestral según la unidad activa (hogares o personas)."""
    if df.empty:
        return 0
    if "n_muestra" in df.columns:
        return int(df["n_muestra"].sum())
    return len(df)


def _group_subsets(df: pd.DataFrame, group_col: str = "dominio") -> tuple[str, list[tuple[str, pd.DataFrame]]]:
    """Devuelve la etiqueta de la variable de cruce y la lista de (etiqueta_categoría, sub_df) con datos."""
    cfg = MONITOR_FILTER_CONFIG.get(group_col, MONITOR_FILTER_CONFIG["dominio"])
    col_label = cfg["short_label"]
    val_map: dict[int, str] = cfg["values"]

    if group_col not in df.columns or df.empty:
        return col_label, []

    present_codes = set(df[group_col].dropna().unique())
    subsets: list[tuple[str, pd.DataFrame]] = []
    for code, label in val_map.items():
        if code in present_codes:
            sub = df[df[group_col] == code]
            if not sub.empty:
                subsets.append((label, sub))
    return col_label, subsets


# =============================================================================
# TABLAS CON COLUMNAS ESPECÍFICAS DEL ARTÍCULO (TABLAS 2, 3, 6 Y 10)
# =============================================================================


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
    _, subsets = _group_subsets(df, "dominio")
    grupos = list(subsets)
    if not df.empty:
        grupos.append(("Total de hogares", df))

    rows = []
    for label, sub in grupos:
        m = calculate_ipm_metrics(sub)
        rows.append({
            "Marco muestral (hogares con módulo PM)": label,
            "Pobreza multidimensional (H)": format_percentage(m.h * 100),
            "Intensidad (A)": format_percentage(m.a * 100),
            "IPM (M0)": format_decimal(m.m0, decimales=3),
            "Pobreza por ingresos": format_percentage(calculate_income_poverty_rate(sub)),
        })
    return pd.DataFrame(rows)


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


# =============================================================================
# TABLAS DE MUESTRA Y POBREZA DEL MONITOR INTERACTIVO
# =============================================================================


def build_flexible_sample_table(
    df: pd.DataFrame,
    group_col: str = "dominio",
    unidad: AnalysisUnit = "hogares",
) -> pd.DataFrame:
    """Tabla 2 flexible: Distribución muestral y expandida según la variable de cruce y unidad elegida."""
    col_label, subsets = _group_subsets(df, group_col)
    tot_n = _sample_count(df)
    tot_w = df["fexp"].sum() if not df.empty else 0.0
    col_exp = "Personas expandidas (N)" if unidad == "personas" else "Hogares expandidos (N)"
    rows = []

    for label, sub in subsets:
        sub_n = _sample_count(sub)
        sub_w = sub["fexp"].sum()
        rows.append({
            col_label: label,
            "Muestra (n)": format_integer(sub_n),
            "% Muestra": format_percentage(sub_n / tot_n * 100 if tot_n else 0),
            col_exp: format_integer(sub_w),
            "% Población": format_percentage(sub_w / tot_w * 100 if tot_w else 0),
        })

    if not df.empty:
        rows.append({
            col_label: "Total selección",
            "Muestra (n)": format_integer(tot_n),
            "% Muestra": "100,0%",
            col_exp: format_integer(tot_w),
            "% Población": "100,0%",
        })
    return pd.DataFrame(rows)


def build_flexible_poverty_table(
    df: pd.DataFrame,
    group_col: str = "dominio",
    unidad: AnalysisUnit = "hogares",
) -> pd.DataFrame:
    """Tablas 3 y 10 unificadas y flexibles: H, A, M0, pobreza por ingresos y muestra por variable de cruce."""
    col_label, subsets = _group_subsets(df, group_col)
    grupos = list(subsets)
    if not df.empty:
        grupos.append(("Total selección", df))

    col_exp = "Personas expandidas (N)" if unidad == "personas" else "Hogares expandidos (N)"
    rows = []
    for label, sub in grupos:
        m = calculate_ipm_metrics(sub)
        row: dict[str, str] = {
            col_label: label,
            "Pobreza multidimensional (H)": format_percentage(m.h * 100),
            "Intensidad (A)": format_percentage(m.a * 100),
            "IPM (M0)": format_decimal(m.m0, decimales=3),
        }
        if group_col != "i_pobreza":
            row["Pobreza por ingresos"] = format_percentage(calculate_income_poverty_rate(sub))
        row["Muestra (n)"] = format_integer(_sample_count(sub))
        row[col_exp] = format_integer(m.hogares_expandidos)
        rows.append(row)
    return pd.DataFrame(rows)


# =============================================================================
# TABLAS UNIFICADAS (ARTÍCULO + MONITOR INTERACTIVO: TABLAS 4, 5, 7, 8, 9, 11 Y 12)
# =============================================================================


def build_overlap_table(
    df: pd.DataFrame,
    group_col: str = "dominio",
    total_label: str = "Total CABA",
) -> pd.DataFrame:
    """Tabla 4 unificada: Matriz de pobreza estructural (IPM × ingresos) por variable de cruce."""
    _, subsets = _group_subsets(df, group_col)
    cols = {label: calculate_poverty_overlap(sub) for label, sub in subsets}
    if not df.empty:
        cols[total_label] = calculate_poverty_overlap(df)
    return format_df_percentages(pd.DataFrame(cols))


def build_deprivation_dist_table(
    df: pd.DataFrame,
    group_col: str = "dominio",
    total_label: str | None = None,
) -> pd.DataFrame:
    """Tabla 5 unificada: Cantidad de dimensiones privadas simultáneas (2 a 5) entre los hogares pobres."""
    _, subsets = _group_subsets(df, group_col)
    cols = {}
    for label, sub in subsets:
        dist = calculate_deprivation_distribution(sub)
        cols[label] = {f"{k} dimensiones privadas": dist[k] for k in range(2, 6)}
    if total_label is not None and not df.empty:
        dist_tot = calculate_deprivation_distribution(df)
        cols[total_label] = {f"{k} dimensiones privadas": dist_tot[k] for k in range(2, 6)}
    return format_df_percentages(pd.DataFrame(cols))


def build_dimension_contributions_table(
    df: pd.DataFrame,
    group_col: str = "dominio",
    total_label: str = "Total CABA",
) -> pd.DataFrame:
    """Tabla 7 unificada: Contribución porcentual de cada dimensión al índice M0."""
    _, subsets = _group_subsets(df, group_col)
    cols = {}
    if not df.empty:
        cols[total_label] = calculate_dimension_contributions(df)
    for label, sub in subsets:
        cols[label] = calculate_dimension_contributions(sub)
    return format_df_percentages(pd.DataFrame(cols))


def build_excluded_indicators_table(
    df: pd.DataFrame,
    group_col: str = "dominio",
    modo: IndicatorRateMode = "no_censurada",
    respetar_universo_excluido: bool = True,
    include_discussion: bool = True,
    total_label: str | None = None,
) -> pd.DataFrame:
    """Tabla 8 unificada: Indicadores descartados del módulo PM."""
    filtro_grupo = {
        "Hogares sin NNyA": lambda sub: sub[sub["tiene_nnya"] == 0],
        "Hogares con NNyA": lambda sub: sub[sub["tiene_nnya"] == 1],
    }

    if include_discussion and group_col == "dominio" and total_label is None:
        villas = df[df["dominio"] == 3]
        resto = df[df["dominio"] == 4]
        rows = []
        for item in INDICADORES_EXCLUIDOS_MODULO_PM:
            var = item["variable"]
            univ = item["universo_excluido"]
            filtrar = filtro_grupo.get(univ, lambda sub: sub) if respetar_universo_excluido else (lambda sub: sub)
            rows.append({
                "Variable": var,
                "Indicador": item["etiqueta"],
                "Dimensión": item["dimension"],
                "Grupo donde se excluye": univ,
                "Incidencia en villas": format_percentage(calculate_indicator_rate(filtrar(villas), var, modo=modo)),
                "Incidencia resto de la ciudad": format_percentage(calculate_indicator_rate(filtrar(resto), var, modo=modo)),
                "Discusión metodológica": item["motivo_exclusion"],
            })
        return pd.DataFrame(rows)

    _, subsets = _group_subsets(df, group_col)
    tot_col = total_label or "Total selección (%)"
    rows = []
    for item in INDICADORES_EXCLUIDOS_MODULO_PM:
        var = item["variable"]
        univ = item["universo_excluido"]
        filtrar = filtro_grupo.get(univ, lambda sub: sub) if respetar_universo_excluido else (lambda sub: sub)

        rec: dict[str, str] = {
            "Variable": var,
            "Indicador": item["etiqueta"],
            "Dimensión": item["dimension"],
            "Exclusión oficial": univ,
        }
        for label, sub in subsets:
            t_sub = calculate_indicator_rate(filtrar(sub), var, modo=modo)
            rec[f"{label} (%)"] = format_percentage(t_sub)
        rec[tot_col] = format_percentage(calculate_indicator_rate(filtrar(df), var, modo=modo))
        rows.append(rec)
    return pd.DataFrame(rows)


def build_habitat_table(
    df: pd.DataFrame,
    group_col: str = "dominio",
    total_label: str = "Total CABA",
) -> pd.DataFrame:
    """Tabla 9 unificada: Indicadores estructurales de hábitat y vivienda omitidos del IPM oficial."""
    _, subsets = _group_subsets(df, group_col)
    cols = {label: calculate_structural_habitat_rates(sub) for label, sub in subsets}
    if not df.empty:
        cols[total_label] = calculate_structural_habitat_rates(df)
    return format_df_percentages(pd.DataFrame(cols))


def build_indicator_rates_table(
    df: pd.DataFrame,
    tiene_nnya: int | None = 1,
    modo: IndicatorRateMode = "no_censurada",
    group_col: str = "dominio",
    total_label: str = "Total CABA (%)",
    dimensiones: dict | None = None,
    year: int = DEFAULT_YEAR,
) -> pd.DataFrame:
    """Tablas 11 y 12 unificadas: Tasas de privación por indicador según tipo de hogar, variable de cruce y modo."""
    dims = dimensiones if dimensiones is not None else get_dimensiones_ipm(year)
    df_base = df if tiene_nnya is None else df[df["tiene_nnya"] == tiene_nnya]
    grupo_key = "sin_nnya" if tiene_nnya == 0 else "con_nnya"
    _, subsets = _group_subsets(df_base, group_col)

    rows = []
    for dim_cfg in dims.values():
        for variable, etiqueta in dim_cfg[grupo_key].items():
            rec: dict[str, str] = {
                "Dimensión": dim_cfg["label"],
                "Indicador": etiqueta,
            }
            for label, sub in subsets:
                t_sub = calculate_indicator_rate(sub, variable, modo=modo)
                rec[f"{label} (%)"] = format_percentage(t_sub)
            rec[total_label] = format_percentage(
                calculate_indicator_rate(df_base, variable, modo=modo)
            )
            rows.append(rec)
    return pd.DataFrame(rows)
