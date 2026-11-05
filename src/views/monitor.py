"""Vista 2: Monitor interactivo de datos con filtros data-driven y expanders modulares."""
from collections.abc import Callable
from dataclasses import dataclass

import pandas as pd
import streamlit as st

from src import texts
from src.config import (
    AVAILABLE_YEARS,
    AnalysisUnit,
    DEFAULT_YEAR,
    get_dimensiones_ipm,
)
from src.config_monitor import (
    FILTER_LAYOUT,
    MONITOR_FILTER_CONFIG,
    UNIDADES_ANALISIS,
)
from src.data import apply_analysis_unit, filter_ipm_dataset, get_ipm_data
from src.formatting import format_integer, format_percentage
from src.ipm import calculate_ipm_metrics
from src.tables import (
    build_deprivation_dist_table,
    build_dimension_contributions_table,
    build_excluded_indicators_table,
    build_flexible_poverty_table,
    build_flexible_sample_table,
    build_habitat_table,
    build_indicator_rates_table,
    build_overlap_table,
)
from src.views.shared import render_metric_cards, render_table, select_modo_matriz


@dataclass(frozen=True)
class MonitorSelection:
    """Selección activa de datos, año, filtros, variable de desagregación y unidad en el Monitor."""

    df: pd.DataFrame
    year: int
    filters: dict[str, list[int]]
    group_col: str
    unidad: AnalysisUnit


def _reset_monitor_filters() -> None:
    """Limpia en session_state todas las selecciones de filtros del monitor y restaura año y unidad por defecto."""
    for col in MONITOR_FILTER_CONFIG:
        key = f"monitor_filter_{col}"
        if key in st.session_state:
            st.session_state[key] = []
    st.session_state["monitor_year_sel"] = DEFAULT_YEAR
    st.session_state["monitor_unidad_analisis"] = next(iter(UNIDADES_ANALISIS.keys()))


def _render_multiselect(
    col_name: str,
    df: pd.DataFrame,
    filters: dict[str, list[int]],
) -> None:
    """Renderiza un selector múltiple para una variable del diseño de registro y guarda su selección."""
    if col_name not in df.columns:
        return
    cfg = MONITOR_FILTER_CONFIG[col_name]
    val_map: dict[int, str] = cfg["values"]
    present_codes = sorted(c for c in val_map if c in df[col_name].dropna().unique())
    filters[col_name] = st.multiselect(
        label=cfg["label"],
        options=present_codes,
        format_func=lambda code, m=val_map: f"{code} - {m.get(code, str(code))}",
        placeholder="Todos",
        key=f"monitor_filter_{col_name}",
    )


def _render_year_unit_selectors() -> tuple[int, AnalysisUnit]:
    """Renderiza los selectores de año de relevamiento y unidad de análisis (hogares / personas)."""
    unit_options = list(UNIDADES_ANALISIS.keys())
    if st.session_state.get("monitor_year_sel") not in AVAILABLE_YEARS:
        st.session_state["monitor_year_sel"] = DEFAULT_YEAR
    if st.session_state.get("monitor_unidad_analisis") not in unit_options:
        st.session_state["monitor_unidad_analisis"] = unit_options[0]

    col_year, col_unit = st.columns([0.35, 0.65])
    with col_year:
        year = st.segmented_control(
            label=texts.MONITOR_YEAR_LABEL,
            options=AVAILABLE_YEARS,
            default=DEFAULT_YEAR,
            selection_mode="single",
            key="monitor_year_sel",
        )
        if year is None:
            year = DEFAULT_YEAR
    with col_unit:
        unidad_sel = st.segmented_control(
            label=texts.MONITOR_UNIT_LABEL,
            options=unit_options,
            default=unit_options[0],
            selection_mode="single",
            key="monitor_unidad_analisis",
        )
        unidad = UNIDADES_ANALISIS.get(unidad_sel or unit_options[0], "hogares")
    return year, unidad


def _render_filter_grid(df: pd.DataFrame) -> dict[str, list[int]]:
    """Renderiza la grilla de filtros de vivienda/hogar y del jefe/a definida en FILTER_LAYOUT."""
    filters: dict[str, list[int]] = {}
    for section_title, rows in FILTER_LAYOUT:
        st.markdown(f"##### {section_title}")
        for row_cols in rows:
            for col_ui, col_name in zip(st.columns(len(row_cols)), row_cols):
                with col_ui:
                    _render_multiselect(col_name, df, filters)
    return filters


def _render_group_selector(df: pd.DataFrame) -> str:
    """Renderiza el selector de variable de cruce/desagregación de las tablas."""
    group_options = [k for k in MONITOR_FILTER_CONFIG if k in df.columns]
    return st.selectbox(
        label=texts.MONITOR_GROUP_LABEL,
        options=group_options,
        index=0,
        format_func=lambda k: MONITOR_FILTER_CONFIG[k]["label"],
        key="monitor_group_col",
    )


def render_monitor_filters(
    df_by_year_fn: Callable[[int], pd.DataFrame],
) -> MonitorSelection:
    """Renderiza el expander de año, unidad de análisis, filtros interactivos y variable de desagregación."""
    with st.expander(texts.MONITOR_FILTERS_EXPANDER_TITLE, expanded=True):
        col_caption, col_reset = st.columns([0.8, 0.2], vertical_alignment="center")
        with col_caption:
            st.caption(texts.MONITOR_INTRO_MD)
        with col_reset:
            st.button(
                texts.MONITOR_RESET_BUTTON,
                on_click=_reset_monitor_filters,
                width="stretch",
            )

        year, unidad = _render_year_unit_selectors()

        with st.spinner(texts.LOADING_SPINNER):
            df = df_by_year_fn(year)

        filters = _render_filter_grid(df)
        st.markdown("---")
        group_col = _render_group_selector(df)

    return MonitorSelection(
        df=df,
        year=year,
        filters=filters,
        group_col=group_col,
        unidad=unidad,
    )


def render_monitor_sample_banner(
    df_total: pd.DataFrame,
    df_filtered: pd.DataFrame,
    unidad: AnalysisUnit = "hogares",
) -> None:
    """Muestra un resumen compacto del tamaño muestral y población expandida tras aplicar los filtros."""
    tot_n = int(df_total["n_muestra"].sum()) if "n_muestra" in df_total.columns else len(df_total)
    tot_w = df_total["fexp"].sum()
    sub_n = (
        int(df_filtered["n_muestra"].sum())
        if (not df_filtered.empty and "n_muestra" in df_filtered.columns)
        else len(df_filtered)
    )
    sub_w = df_filtered["fexp"].sum() if not df_filtered.empty else 0.0

    pct_n = format_percentage(sub_n / tot_n * 100 if tot_n else 0)
    pct_w = format_percentage(sub_w / tot_w * 100 if tot_w else 0)
    unidad_str = "personas" if unidad == "personas" else "hogares"
    exp_str = "personas expandidas" if unidad == "personas" else "hogares expandidos"

    st.caption(
        f"**Subuniverso seleccionado ({unidad_str}):** `{format_integer(sub_n)}` de `{format_integer(tot_n)}` {unidad_str} en muestra "
        f"({pct_n}) · `{format_integer(sub_w)}` de `{format_integer(tot_w)}` {exp_str} ({pct_w} del total CABA)."
    )


# =============================================================================
# EXPANDERS INDIVIDUALES DEL MONITOR INTERACTIVO
# =============================================================================


def _expander_pobreza(
    df: pd.DataFrame,
    group_col: str,
    group_label: str,
    unidad: AnalysisUnit,
    caption: str,
) -> None:
    with st.expander(texts.MONITOR_EXPANDER_1, expanded=True):
        render_table(
            build_flexible_poverty_table(df, group_col=group_col, unidad=unidad),
            title=texts.monitor_poverty_title(group_label),
            hide_index=True,
            caption=caption,
            static=True,
        )
        st.markdown("---")
        render_table(
            build_flexible_sample_table(df, group_col=group_col, unidad=unidad),
            title=texts.monitor_sample_title(group_label),
            hide_index=True,
            caption=caption,
            static=True,
        )


def _expander_estructural(
    df: pd.DataFrame,
    group_col: str,
    group_label: str,
    caption: str,
) -> None:
    with st.expander(texts.MONITOR_EXPANDER_2, expanded=False):
        render_table(
            build_overlap_table(df, group_col=group_col, total_label="Total selección"),
            title=texts.monitor_overlap_title(group_label),
            hide_index=False,
            caption=caption,
            static=True,
        )


def _expander_intensidad(
    df: pd.DataFrame,
    group_col: str,
    group_label: str,
    caption: str,
) -> None:
    with st.expander(texts.MONITOR_EXPANDER_3, expanded=False):
        render_table(
            build_deprivation_dist_table(df, group_col=group_col, total_label="Total selección"),
            title=texts.monitor_deprivation_title(group_label),
            hide_index=False,
            caption=caption,
            static=True,
        )


def _expander_contribuciones(
    df: pd.DataFrame,
    group_col: str,
    group_label: str,
    caption: str,
) -> None:
    with st.expander(texts.MONITOR_EXPANDER_4, expanded=False):
        render_table(
            build_dimension_contributions_table(df, group_col=group_col, total_label="Total selección"),
            title=texts.monitor_contributions_title(group_label),
            hide_index=False,
            caption=caption,
        )


def _expander_habitat(
    df: pd.DataFrame,
    group_col: str,
    group_label: str,
    caption: str,
) -> None:
    with st.expander(texts.MONITOR_EXPANDER_5, expanded=False):
        render_table(
            build_habitat_table(df, group_col=group_col, total_label="Total selección"),
            title=texts.monitor_habitat_title(group_label),
            hide_index=False,
            note=texts.TABLA_9_NOTA_CLOACA,
            caption=caption,
        )


def _expander_excluidos(
    df: pd.DataFrame,
    group_col: str,
    group_label: str,
    caption: str,
) -> None:
    with st.expander(texts.MONITOR_EXPANDER_6, expanded=False):
        col_m, col_u = st.columns([0.65, 0.35], vertical_alignment="center")
        with col_m:
            modo_exc = select_modo_matriz(key="monitor_exc_modo")
        with col_u:
            respetar_univ = st.checkbox(
                texts.MONITOR_EXC_CHECKBOX_LABEL,
                value=False,
                key="monitor_exc_univ",
                help=texts.MONITOR_EXC_CHECKBOX_HELP,
            )
        render_table(
            build_excluded_indicators_table(
                df,
                group_col=group_col,
                modo=modo_exc,
                respetar_universo_excluido=respetar_univ,
                include_discussion=False,
                total_label="Total selección (%)",
            ),
            title=texts.monitor_excluded_title(group_label),
            hide_index=True,
            caption=caption,
        )


def _expander_indicadores(
    df: pd.DataFrame,
    group_col: str,
    group_label: str,
    year: int,
    caption: str,
) -> None:
    dims_year = get_dimensiones_ipm(year)
    n_sin = sum(len(d["sin_nnya"]) for d in dims_year.values())
    n_con = sum(len(d["con_nnya"]) for d in dims_year.values())

    with st.expander(texts.MONITOR_EXPANDER_7, expanded=False):
        modo_ind = select_modo_matriz(key="monitor_ind_modo")
        vista_nnya = st.radio(
            texts.MONITOR_NNYA_RADIO_LABEL,
            options=[
                f"Separar según presencia de NNyA ({n_con} ind. con NNyA / {n_sin} ind. sin NNyA)",
                f"Unificado sobre todos los hogares seleccionados ({n_con} indicadores)",
            ],
            horizontal=True,
            key="monitor_ind_vista_nnya",
        )

        if vista_nnya.startswith("Unificado"):
            render_table(
                build_indicator_rates_table(
                    df,
                    tiene_nnya=None,
                    modo=modo_ind,
                    group_col=group_col,
                    total_label="Total selección (%)",
                    year=year,
                ),
                title=texts.monitor_indicators_unified_title(n_con, group_label, year),
                hide_index=True,
                caption=caption,
            )
        else:
            titulos_nnya = [
                (1, texts.monitor_tabla_11_title(n_con, year)),
                (0, texts.monitor_tabla_12_title(n_sin, year)),
            ]
            for tiene_nnya, titulo in titulos_nnya:
                if (df["tiene_nnya"] == tiene_nnya).any():
                    st.markdown(f"##### {titulo}")
                    df_ind = build_indicator_rates_table(
                        df,
                        tiene_nnya=tiene_nnya,
                        modo=modo_ind,
                        group_col=group_col,
                        total_label="Total selección (%)",
                        year=year,
                    )
                    render_table(df_ind, hide_index=True, caption=caption)


def render_monitor_expanders(
    df: pd.DataFrame,
    group_col: str = "dominio",
    unidad: AnalysisUnit = "hogares",
    year: int = DEFAULT_YEAR,
) -> None:
    """Renderiza los 7 expanders del Monitor Interactivo."""
    group_label = MONITOR_FILTER_CONFIG[group_col]["short_label"]
    caption = texts.source_caption(year)

    _expander_pobreza(df, group_col, group_label, unidad, caption)
    _expander_estructural(df, group_col, group_label, caption)
    _expander_intensidad(df, group_col, group_label, caption)
    _expander_contribuciones(df, group_col, group_label, caption)
    _expander_habitat(df, group_col, group_label, caption)
    _expander_excluidos(df, group_col, group_label, caption)
    _expander_indicadores(df, group_col, group_label, year, caption)


def page_monitor_interactivo() -> None:
    """Vista 2: Monitor interactivo de datos con métricas arriba, filtros en expander y expanders de tablas."""
    st.title(texts.MONITOR_HEADER_TITLE)
    st.subheader(texts.MONITOR_SUBTITLE)
    st.warning(texts.MONITOR_BETA_WARNING_MD, icon="⚠️")

    metrics_container = st.container()

    sel = render_monitor_filters(get_ipm_data)
    df_unit = apply_analysis_unit(sel.df, unidad=sel.unidad)
    df_filtered = filter_ipm_dataset(df_unit, sel.filters)

    with metrics_container:
        metrics = calculate_ipm_metrics(df_filtered)
        render_metric_cards(metrics, unidad=sel.unidad)
        render_monitor_sample_banner(df_total=df_unit, df_filtered=df_filtered, unidad=sel.unidad)
        st.caption(texts.source_caption(sel.year))

    if df_filtered.empty:
        st.warning(texts.MONITOR_EMPTY_WARNING)
        return

    st.divider()
    render_monitor_expanders(df_filtered, group_col=sel.group_col, unidad=sel.unidad, year=sel.year)
