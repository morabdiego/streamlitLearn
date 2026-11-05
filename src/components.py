"""Componentes visuales de Streamlit para la presentación de textos, KPIs y tablas."""
import pandas as pd
import streamlit as st

from src import texts
from src.config import (
    AVAILABLE_YEARS,
    DEFAULT_YEAR,
    MODOS_MATRIZ_INDICADORES,
    MONITOR_FILTER_CONFIG,
    UNIDADES_ANALISIS,
    get_dimensiones_ipm,
)
from src.logic import (
    AnalysisUnit,
    IPMMetrics,
    build_deprivation_dist_table,
    build_dimension_contributions_table,
    build_domain_poverty_table,
    build_excluded_indicators_table,
    build_flexible_deprivation_dist_table,
    build_flexible_dimension_contributions_table,
    build_flexible_excluded_indicators_table,
    build_flexible_habitat_table,
    build_flexible_indicator_rates_table,
    build_flexible_overlap_table,
    build_flexible_poverty_table,
    build_flexible_sample_table,
    build_habitat_table,
    build_indicator_rates_table,
    build_nnya_summary_table,
    build_overlap_table,
    build_sample_table,
    build_structure_2025_table,
    format_decimal,
    format_integer,
    format_percentage,
)


def _render_table(
    df: pd.DataFrame,
    title: str | None = None,
    hide_index: bool = True,
    note: str | None = None,
    caption: str = texts.SOURCE_CAPTION,
    table = False
) -> None:
    """Renderiza una tabla con su título, nota opcional y fuente oficial."""
    if title:
        st.markdown(title)
    if not df.empty:
        if table:
            st.table(df, height="content", hide_index=hide_index)
        else:
            st.dataframe(df, width="stretch", hide_index=hide_index)
        if note:
            st.caption(note)
        st.caption(caption)

def render_header() -> None:
    """Renderiza el encabezado principal, autoría y marco teórico introductorio."""
    st.title(texts.HEADER_TITLE)
    st.header(texts.HEADER_SUBTITLE)
    # st.markdown(texts.HEADER_AUTHOR)
    col1, col2 = st.columns([.7, .2])
    with col1:
        st.link_button(label="Autor: Mora Benitez, Diego J.", url="https://linktr.ee/morabdiego")
    with col2:
        st.link_button(label="Ver código en Github", url="https://github.com/morabdiego/streamlitlearn")

def render_expander() -> None:
    st.markdown(
        """
        <style>
        div[data-testid="stExpander"] summary p {
            font-size: 1.25rem !important;  /* Ajusta el tamaño deseado (ej. 1.2rem, 18px, 20px) */
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.expander(texts.HEADER_EXPANDER_TITLE, expanded=False):
        st.markdown(texts.HEADER_THEORY_MD)
        st.markdown("---")
        _render_table(
            pd.DataFrame(texts.TABLA_1_HISTORICO_VILLAS),
            title=texts.TABLA_1_TITULO,
            hide_index=True,
            caption=texts.TABLA_1_CAPTION,
            table=True,
        )

def render_metric_cards(metrics: IPMMetrics, unidad: AnalysisUnit = "hogares") -> None:
    """Renderiza las 4 tarjetas principales de métricas Alkire-Foster (a nivel hogares o personas)."""
    col1, col2, col3, col4 = st.columns(4)
    pobres_label = texts.KPI_POBRES_PERSONAS_LABEL if unidad == "personas" else texts.KPI_POBRES_LABEL

    col1.metric(
        label=texts.KPI_H_LABEL,
        value=format_percentage(metrics.h * 100),
        help=texts.KPI_H_HELP,
    )
    col2.metric(
        label=texts.KPI_A_LABEL,
        value=format_percentage(metrics.a * 100),
        help=texts.KPI_A_HELP,
    )
    col3.metric(
        label=texts.KPI_M0_LABEL,
        value=format_decimal(metrics.m0, decimales=3),
        help=texts.KPI_M0_HELP,
    )
    col4.metric(
        label=pobres_label,
        value=format_integer(metrics.pobres_expandidos),
        delta=f"de {format_integer(metrics.hogares_expandidos)} totales",
        delta_color="off",
    )


def render_tab_brecha_territorial(df: pd.DataFrame) -> None:
    """Pestaña 1: Marco muestral, brecha territorial, pobreza estructural e intensidad."""
    st.subheader(texts.TAB1_SUBHEADER)
    st.markdown(texts.TAB1_INTRO_MD)

    st.markdown(texts.TAB1_SEC1_TITULO)
    st.markdown(texts.TAB1_SEC1_MD)
    _render_table(build_sample_table(df), title=texts.TABLA_2_TITULO, hide_index=True, table=True)

    st.markdown("---")

    st.markdown(texts.TAB1_SEC2_TITULO)
    _render_table(build_domain_poverty_table(df), title=texts.TABLA_3_TITULO, hide_index=True, table=True)
    st.markdown(texts.TAB1_SEC2_OUTRO_MD)

    st.markdown("---")

    st.markdown(texts.TAB1_SEC3_TITULO)
    st.markdown(texts.TAB1_SEC3_MD)
    _render_table(build_overlap_table(df), title=texts.TABLA_4_TITULO, hide_index=False, table=True)

    st.markdown("---")

    st.markdown(texts.TAB1_SEC4_TITULO)
    st.markdown(texts.TAB1_SEC4_MD)
    _render_table(build_deprivation_dist_table(df), title=texts.TABLA_5_TITULO, hide_index=False, table=True)


def render_tab_discusion_metodologica(df: pd.DataFrame) -> None:
    """Pestaña 2: Debate Método Consensual vs. Alkire-Foster, estructura 2025 y contribución a M0."""
    st.subheader(texts.TAB2_SUBHEADER)
    st.markdown(texts.TAB2_INTRO_MD)
    st.warning(texts.TAB2_CONSENSUAL_WARNING_MD)
    st.info(texts.TAB2_AF_INFO_MD)

    st.markdown(texts.TAB2_SEC7_TITULO)
    df_matriz = build_structure_2025_table()
    st.markdown(texts.TABLA_6_TITULO)
    st.dataframe(
        df_matriz,
        # width="stretch",
        hide_index=True,
        # height=min(35 * len(df_matriz) + 38, 800),
        column_config={
            "Dimensión": st.column_config.TextColumn(width="medium"),
            "Indicador": st.column_config.TextColumn(width="medium"),
        },
    )
    st.caption(texts.SOURCE_CAPTION)

    st.markdown("---")

    st.markdown(texts.TAB2_SEC8_TITULO)
    st.markdown(texts.TAB2_SEC8_MD)
    _render_table(build_dimension_contributions_table(df), title=texts.TABLA_7_TITULO, hide_index=False)


def render_tab_discusion_indicadores(df: pd.DataFrame) -> None:
    """Pestaña 3: Indicadores descartados del módulo PM y variables estructurales de hábitat."""
    st.subheader(texts.TAB3_SUBHEADER)
    st.markdown(texts.TAB3_INTRO_MD)

    st.markdown(texts.TAB3_SEC9_TITULO)
    st.markdown(texts.TAB3_SEC9_MD)
    _render_table(build_excluded_indicators_table(df), title=texts.TABLA_8_TITULO, hide_index=True, table=True)

    st.markdown("---")

    st.markdown(texts.TAB3_SEC10_TITULO)
    st.markdown(texts.TAB3_SEC10_MD)
    _render_table(
        build_habitat_table(df),
        title=texts.TABLA_9_TITULO,
        hide_index=False,
        note=texts.TABLA_9_NOTA_CLOACA,
    )

    st.markdown("---")


def render_tab_indicadores_detalle(df: pd.DataFrame) -> None:
    """Pestaña 4: Resumen según presencia de NNyA y tasas por indicador (3 modos de matriz)."""
    st.subheader(texts.TAB4_SUBHEADER)

    st.markdown(texts.TAB4_SEC11_TITULO)
    st.markdown(texts.TAB4_SEC11_MD)
    _render_table(build_nnya_summary_table(df), title=texts.TABLA_10_TITULO, hide_index=True, table=True)

    st.markdown("---")

    st.markdown(texts.TAB4_SEC12_TITULO)
    opcion_sel = st.radio(
        texts.TAB4_RADIO_LABEL,
        options=list(MODOS_MATRIZ_INDICADORES.keys()),
        horizontal=True,
    )
    modo = MODOS_MATRIZ_INDICADORES[opcion_sel]

    for tiene_nnya, titulo in [(1, texts.TABLA_11_TITULO), (0, texts.TABLA_12_TITULO)]:
        st.markdown(f"##### {titulo}")
        df_ind = build_indicator_rates_table(df, tiene_nnya=tiene_nnya, modo=modo) # pyright: ignore[reportArgumentType]
        _render_table(df_ind, hide_index=True)


def render_tab_conclusiones() -> None:
    """Pestaña 5: Conclusiones, Anexo RENABAP y Bibliografía."""
    st.subheader(texts.TAB5_SUBHEADER)
    st.markdown(texts.TAB5_CONCLUSIONES_MD)

    st.markdown("---")

    with st.expander(texts.ANEXO_1_TITULO):
        st.markdown(texts.ANEXO_1_INTRO_MD)
        _render_table(
            pd.DataFrame(texts.BARRIOS_RENABAP_CABA),
            hide_index=True,
            caption=texts.ANEXO_1_CAPTION,
        )

    st.markdown("---")

    st.markdown(texts.BIBLIOGRAFIA_TITULO)
    st.markdown(texts.BIBLIOGRAFIA_MD)


def render_analysis_tabs(df: pd.DataFrame) -> None:
    """Renderiza las 5 pestañas temáticas de la aplicación."""
    tab1, tab2, tab3, tab4, tab5 = st.tabs(texts.TAB_LABELS)

    with tab1:
        render_tab_brecha_territorial(df)
    with tab2:
        render_tab_discusion_metodologica(df)
    with tab3:
        render_tab_discusion_indicadores(df)
    with tab4:
        render_tab_indicadores_detalle(df)
    with tab5:
        render_tab_conclusiones()


# =============================================================================
# COMPONENTES DEL MONITOR INTERACTIVO DE DATOS
# =============================================================================


def _reset_monitor_filters() -> None:
    """Limpia en session_state todas las selecciones de filtros del monitor y restaura año y unidad por defecto."""
    for col in MONITOR_FILTER_CONFIG:
        key = f"monitor_filter_{col}"
        if key in st.session_state:
            st.session_state[key] = []
    st.session_state["monitor_year_sel"] = DEFAULT_YEAR
    st.session_state["monitor_unidad_analisis"] = next(iter(UNIDADES_ANALISIS.keys()))


def render_monitor_filters(
    df_by_year_fn,
) -> tuple[pd.DataFrame, int, dict[str, list[int]], str, AnalysisUnit]:
    """Renderiza el expander de año, unidad de análisis, filtros interactivos y variable de desagregación."""
    with st.expander(texts.MONITOR_FILTERS_EXPANDER_TITLE, expanded=True):
        col_caption, col_reset = st.columns([0.8, 0.2], vertical_alignment="center")
        with col_caption:
            st.caption(texts.MONITOR_INTRO_MD)
        with col_reset:
            st.button(
                "Limpiar filtros",
                on_click=_reset_monitor_filters,
                width="stretch",
            )

        unit_options = list(UNIDADES_ANALISIS.keys())
        if st.session_state.get("monitor_year_sel") not in AVAILABLE_YEARS:
            st.session_state["monitor_year_sel"] = DEFAULT_YEAR
        if st.session_state.get("monitor_unidad_analisis") not in unit_options:
            st.session_state["monitor_unidad_analisis"] = unit_options[0]

        col_year, col_unit = st.columns([0.35, 0.65])
        with col_year:
            year = st.segmented_control(
                label="📅 Año de relevamiento (EAH):",
                options=AVAILABLE_YEARS,
                default=DEFAULT_YEAR,
                selection_mode="single",
                key="monitor_year_sel",
            )
            if year is None:
                year = DEFAULT_YEAR
        with col_unit:
            unidad_sel = st.segmented_control(
                label="👥 Unidad de análisis y factor de expansión (`fexp`):",
                options=unit_options,
                default=unit_options[0],
                selection_mode="single",
                key="monitor_unidad_analisis",
            )
            unidad: AnalysisUnit = UNIDADES_ANALISIS.get(unidad_sel or unit_options[0], "hogares")  # pyright: ignore[reportAssignmentType]

        with st.spinner(texts.LOADING_SPINNER):
            df: pd.DataFrame = df_by_year_fn(year)

        st.markdown("##### 🏠 Variables de vivienda y hogar")
        filters: dict[str, list[int]] = {}

        def _render_multiselect(col_name: str) -> None:
            if col_name not in df.columns:
                return
            cfg = MONITOR_FILTER_CONFIG[col_name]
            val_map: dict[int, str] = cfg["values"]
            present_codes = sorted(c for c in val_map if c in df[col_name].dropna().unique())
            selected = st.multiselect(
                label=cfg["label"],
                options=present_codes,
                format_func=lambda code, m=val_map: f"{code} - {m.get(code, str(code))}",
                placeholder="Todos",
                key=f"monitor_filter_{col_name}",
            )
            filters[col_name] = selected

        # Fila 1: Dominio, Comuna, Presencia de menores (0 a 17)
        r1_c1, r1_c2, r1_c3 = st.columns(3)
        with r1_c1:
            _render_multiselect("dominio")
        with r1_c2:
            _render_multiselect("comuna")
        with r1_c3:
            _render_multiselect("hog_per_0a17")

        # Fila 2: Régimen de tenencia (h2), Hacinamiento (hacinam_2)
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            _render_multiselect("h2")
        with r2_c2:
            _render_multiselect("hacinam_2")

        # Fila 3: Tipo de hogar (tipoho_3), Situación de pobreza por ingresos (i_pobreza)
        r3_c1, r3_c2 = st.columns(2)
        with r3_c1:
            _render_multiselect("tipoho_3")
        with r3_c2:
            _render_multiselect("i_pobreza")

        st.markdown("##### 👤 Características del jefe/a de hogar (respondiente)")
        # Fila 4: Sexo (sexo), Condición de ocupación (estado)
        r4_c1, r4_c2 = st.columns(2)
        with r4_c1:
            _render_multiselect("sexo")
        with r4_c2:
            _render_multiselect("estado")

        # Fila 5: Identidad de género (dh2), Orientación sexual (dh3)
        r5_c1, r5_c2 = st.columns(2)
        with r5_c1:
            _render_multiselect("dh2")
        with r5_c2:
            _render_multiselect("dh3")

        st.markdown("---")
        group_options = [k for k in MONITOR_FILTER_CONFIG if k in df.columns]
        group_col = st.selectbox(
            label="📊 Desagregar / cruzar las tablas por la variable:",
            options=group_options,
            index=0,
            format_func=lambda k: MONITOR_FILTER_CONFIG[k]["label"],
            key="monitor_group_col",
        )

    return df, year, filters, group_col, unidad


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


def render_monitor_expanders(
    df: pd.DataFrame,
    group_col: str = "dominio",
    unidad: AnalysisUnit = "hogares",
    year: int = DEFAULT_YEAR,
) -> None:
    """Renderiza los expanders con todas las tablas del informe adaptadas a los filtros, cruce, unidad y año."""
    group_label = MONITOR_FILTER_CONFIG[group_col]["short_label"]
    dims_year = get_dimensiones_ipm(year)
    n_sin = sum(len(d["sin_nnya"]) for d in dims_year.values())
    n_con = sum(len(d["con_nnya"]) for d in dims_year.values())

    # Expander 1: Condiciones de pobreza (H, A, M0, ingresos) y muestra (Tablas 2, 3 y 10)
    with st.expander(texts.MONITOR_EXPANDER_1, expanded=False):
        _render_table(
            build_flexible_poverty_table(df, group_col=group_col, unidad=unidad),
            title=f"**Métricas Alkire-Foster y pobreza por ingresos según {group_label}**",
            hide_index=True,
            table=True,
        )
        st.markdown("---")
        _render_table(
            build_flexible_sample_table(df, group_col=group_col, unidad=unidad),
            title=f"**Distribución de muestra y población expandida según {group_label}**",
            hide_index=True,
            table=True,
        )

    # Expander 2: Pobreza estructural (Tabla 4)
    with st.expander(texts.MONITOR_EXPANDER_2, expanded=False):
        _render_table(
            build_flexible_overlap_table(df, group_col=group_col),
            title=f"**Pobreza estructural (IPM × ingresos) según {group_label}**",
            hide_index=False,
            table=True,
        )

    # Expander 3: Intensidad de las privaciones - Cantidad de dimensiones privadas (Tabla 5)
    with st.expander(texts.MONITOR_EXPANDER_3, expanded=False):
        _render_table(
            build_flexible_deprivation_dist_table(df, group_col=group_col),
            title=f"**Cantidad de dimensiones privadas simultáneas (hogares pobres PM) según {group_label}**",
            hide_index=False,
            table=True,
        )

    # Expander 4: Contribución por dimensión a M0 (Tabla 7)
    with st.expander(texts.MONITOR_EXPANDER_4, expanded=False):
        _render_table(
            build_flexible_dimension_contributions_table(df, group_col=group_col),
            title=f"**Contribución porcentual de cada dimensión al índice $M_0$ según {group_label}**",
            hide_index=False,
        )

    # Expander 5: Indicadores estructurales de hábitat y vivienda (Tabla 9)
    with st.expander(texts.MONITOR_EXPANDER_5, expanded=False):
        _render_table(
            build_flexible_habitat_table(df, group_col=group_col),
            title=f"**Privaciones estructurales de hábitat y vivienda según {group_label}**",
            hide_index=False,
            note=texts.TABLA_9_NOTA_CLOACA,
        )

    # Expander 6: Indicadores descartados del módulo PM (Tabla 8)
    with st.expander(texts.MONITOR_EXPANDER_6, expanded=False):
        col_m, col_u = st.columns([0.65, 0.35], vertical_alignment="center")
        with col_m:
            opcion_exc = st.radio(
                texts.TAB4_RADIO_LABEL,
                options=list(MODOS_MATRIZ_INDICADORES.keys()),
                horizontal=True,
                key="monitor_exc_modo",
            )
        with col_u:
            respetar_univ = st.checkbox(
                "Evaluar sólo en el subgrupo excluido oficialmente",
                value=False,
                key="monitor_exc_univ",
                help="Si se activa, cada indicador se evalúa únicamente en el subgrupo (con o sin NNyA) donde fue descartado oficialmente.",
            )
        modo_exc = MODOS_MATRIZ_INDICADORES[opcion_exc]
        _render_table(
            build_flexible_excluded_indicators_table(
                df,
                group_col=group_col,
                modo=modo_exc,  # pyright: ignore[reportArgumentType]
                respetar_universo_excluido=respetar_univ,
            ),
            title=f"**Indicadores relevados en el módulo PM pero excluidos del índice oficial según {group_label}**",
            hide_index=True,
        )

    # Expander 7: Tasas por indicador de las 5 dimensiones (Tablas 11 y 12)
    with st.expander(texts.MONITOR_EXPANDER_7, expanded=False):
        opcion_ind = st.radio(
            texts.TAB4_RADIO_LABEL,
            options=list(MODOS_MATRIZ_INDICADORES.keys()),
            horizontal=True,
            key="monitor_ind_modo",
        )
        modo_ind = MODOS_MATRIZ_INDICADORES[opcion_ind]

        vista_nnya = st.radio(
            "Desglose según presencia de menores de 18 años (NNyA):",
            options=[
                f"Separar según presencia de NNyA ({n_con} ind. con NNyA / {n_sin} ind. sin NNyA)",
                f"Unificado sobre todos los hogares seleccionados ({n_con} indicadores)",
            ],
            horizontal=True,
            key="monitor_ind_vista_nnya",
        )

        if vista_nnya.startswith("Unificado"):
            _render_table(
                build_flexible_indicator_rates_table(
                    df,
                    group_col=group_col,
                    modo=modo_ind,  # pyright: ignore[reportArgumentType]
                    tiene_nnya=None,
                    year=year,
                ),
                title=f"**Tasas de privación de los {n_con} indicadores según {group_label} (EAH {year})**",
                hide_index=True,
            )
        else:
            titulos_nnya = [
                (1, f"Tabla 11: {n_con} indicadores para hogares con menores de 18 años (EAH {year})"),
                (0, f"Tabla 12: {n_sin} indicadores para hogares sin menores de 18 años (EAH {year})"),
            ]
            for tiene_nnya, titulo in titulos_nnya:
                if (df["tiene_nnya"] == tiene_nnya).any():
                    st.markdown(f"##### {titulo}")
                    df_ind = build_flexible_indicator_rates_table(
                        df,
                        group_col=group_col,
                        modo=modo_ind,  # pyright: ignore[reportArgumentType]
                        tiene_nnya=tiene_nnya,
                        year=year,
                    )
                    _render_table(df_ind, hide_index=True)
