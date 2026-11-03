"""Componentes para las pestañas de análisis, discusión metodológica, indicadores y bibliografía."""
import numpy as np
import pandas as pd
import streamlit as st

from src.config.constants import (
    DIMENSIONES_INDICADORES_IPM,
    INDICADORES_COMUNES,
    INDICADORES_EXCLUIDOS_MODULO_PM,
    MAP_DOMINIO,
    SOURCE_CAPTION,
)
from src.domain.alkire_foster import (
    calculate_deprivation_distribution,
    calculate_dimension_contributions,
    calculate_indicator_rate,
    calculate_ipm_metrics,
    calculate_poverty_overlap,
    calculate_structural_habitat_rates,
)
from src.utils.formatters import format_decimal, format_integer, format_percentage


def _format_df_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """Formatea todas las celdas numéricas de un DataFrame como porcentajes (compatible con Pandas 3+)."""
    return df.map(lambda v: format_percentage(v))


def render_tab_brecha_territorial(df_view: pd.DataFrame, raw_df: pd.DataFrame | None = None) -> None:
    """Pestaña 1: Marco muestral, brecha territorial Villas vs. Resto y acumulación de desventajas."""
    st.subheader("Pobreza multidimensional: Análisis por dominio geográfico de la muestra")
    st.markdown("""
> **La falacia del promedio urbano y la segregación residencial**: La CABA se caracteriza por poseer indicadores promedio de calidad de vida, salud, educación e ingresos altos respecto al resto del país (**INDEC, 2023a, 2023b**). Sin embargo, detrás del promedio general se oculta una profunda fractura socioespacial concentrada en las comunas del sur (**Sabatini et al., 2001**), donde una décima parte de la población habita en villas y asentamientos populares conviviendo con una acumulación sistemática de desventajas.
    """)

    # 1. Análisis del Marco Muestral (Tabla 3.1 actualizada)
    st.markdown("##### 1. Brecha de representación de las villas")
    st.markdown("""
A partir de 2019 la Encuesta Anual de Hogares (EAH) incorpora el módulo ampliado de pobreza multidimensional sobre dos marcos muestrales: **Marco 4 ("Viviendas particulares generales" / Resto de la ciudad)** y **Marco 3 ("Villas, asentamientos y NHT")**.

Al observar los factores de expansión muestral (`fexp`), el marco en villas obtiene una representación cercana al **3,8% – 4,0% de los hogares**, mientras que los relevamientos del **RENABAP (2022)** indican que al menos el **10,4% de la población porteña** reside en los 50 barrios populares de la Ciudad. Como advierten **Macció y Lépore (2012)** y **Marx, Stoker y Suri (2013)**, esta distorsión en el peso estadístico asignado a las villas **subestima las tasas globales de pobreza** de toda la CABA.
    """)

    if raw_df is not None and "dominio" in raw_df.columns:
        df_pm_resp = (
            raw_df[raw_df["ent_rea_pm"] == 1]
            if "ent_rea_pm" in raw_df.columns
            else raw_df
        )
        tot_n_pm = len(df_pm_resp)
        tot_w_pm = df_pm_resp["fexp"].sum()
        tot_n_all = len(raw_df)
        tot_w_all = raw_df["fexp"].sum()

        muestra_rows = []
        for dom_code, dom_label in [(3, "Villas, asentamientos y NHT"), (4, "Resto de la ciudad")]:
            sub_pm = df_pm_resp[df_pm_resp["dominio"] == dom_code]
            sub_all = raw_df[raw_df["dominio"] == dom_code]
            muestra_rows.append({
                "Marco muestral (hogares con módulo PM)": dom_label,
                "Muestra": format_integer(len(sub_pm)),
                "% Muestra": format_percentage(len(sub_pm) / tot_n_pm * 100 if tot_n_pm else 0),
                "Población": format_integer(sub_pm["fexp"].sum()),
                "% Población": format_percentage(sub_pm["fexp"].sum() / tot_w_pm * 100 if tot_w_pm else 0),
                # "Total Hogares EAH (N)": format_integer(len(sub_all)),
                # "Total Expandido EAH": format_integer(sub_all["fexp"].sum()),
            })
        muestra_rows.append({
            "Marco muestral (hogares con módulo PM)": "Total de hogares",
            "Muestra": format_integer(tot_n_pm),
            "% Muestra": "100,0%",
            "Población": format_integer(tot_w_pm),
            "% Población": "100,0%",
            # "Total Hogares EAH (N)": format_integer(tot_n_all),
            # "Total Expandido EAH": format_integer(tot_w_all),
        })
        st.dataframe(pd.DataFrame(muestra_rows), width="stretch", hide_index=True)
        st.caption(SOURCE_CAPTION)

    st.markdown("---")

    # 2. Tabla comparativa consolidada Alkire-Foster + Pobreza por Ingresos
    st.markdown("##### 2. Brecha de pobreza multidimensional y por ingresos")

    rows_dom = []
    dominios_presentes = [d for d in MAP_DOMINIO.values() if d in df_view["dominio_desc"].unique()]

    for d_nombre in dominios_presentes:
        sub_df = df_view[df_view["dominio_desc"] == d_nombre]
        if len(sub_df) > 0:
            metrics = calculate_ipm_metrics(sub_df)
            pobre_ing = (
                float(np.average(sub_df["pobre_ingreso"], weights=sub_df["fexp"]) * 100)
                if "pobre_ingreso" in sub_df.columns
                else 0.0
            )
            rows_dom.append({
                "Marco muestral (hogares con módulo PM)": d_nombre,
                "Pobreza multidimensional (H)": format_percentage(metrics.h * 100),
                "Intensidad (A)": format_percentage(metrics.a * 100),
                "IPM (M0)": format_decimal(metrics.m0, decimales=3),
                "Pobreza por ingresos": format_percentage(pobre_ing),
                # "Hogares Pobres IPM (exp)": format_integer(metrics.pobres_expandidos),
                # "Total Hogares (exp)": format_integer(metrics.hogares_expandidos),
                # "Muestra (N)": format_integer(len(sub_df)),
            })

    if len(df_view) > 0:
        m_tot = calculate_ipm_metrics(df_view)
        p_ing_tot = (
            float(np.average(df_view["pobre_ingreso"], weights=df_view["fexp"]) * 100)
            if "pobre_ingreso" in df_view.columns
            else 0.0
        )
        rows_dom.append({
            "Marco muestral (hogares con módulo PM)": "Total de hogares",
            "Pobreza multidimensional (H)": format_percentage(m_tot.h * 100),
            "Intensidad (A)": format_percentage(m_tot.a * 100),
            "IPM (M0)": format_decimal(m_tot.m0, decimales=3),
            "Pobreza por ingresos": format_percentage(p_ing_tot),
            # "Hogares Pobres IPM (exp)": format_integer(m_tot.pobres_expandidos),
            # "Total Hogares (exp)": format_integer(m_tot.hogares_expandidos),
            # "Muestra (N)": format_integer(len(df_view)),
        })

    if rows_dom:
        st.dataframe(pd.DataFrame(rows_dom), width="stretch", hide_index=True)
        st.caption(SOURCE_CAPTION)

    st.markdown("""
En los informes oficiales se publica únicamente la tasa de incidencia ($H = q/n$) global o por zonas geográficas (Norte, Centro y Sur), sin desagregar específicamente el marco muestral de villas ni informar la intensidad de las privaciones. Al reconstruir el cálculo mediante los índices de **Alkire y Foster (2007)** por marco muestral:
* La **Incidencia ($H$)** y la **Pobreza por Ingresos** en las villas cuadruplican y quintuplican los registros del resto de la ciudad.
* La **Intensidad ($A$)** revela que los hogares pobres en villas sufren un porcentaje promedio de privaciones simultáneas significativamente mayor.
* La **Tasa de Recuento Ajustada ($M_0 = H \\times A$)** arroja una brecha de **casi 5 veces** entre ambos territorios.
    """)

    with st.expander("📌 Comparación con los resultados originales de la Tesis (EAH 2021 vs. Actualización EAH 2025)"):
        st.markdown("""
En la tesis original sobre la **EAH 2021** (Tablas 3.3, 3.4 y 3.6), con los umbrales oficiales ($k_{\\text{intra}}=33,3\\%, k_{\\text{inter}}=40\\%$):
* **Villas (2021)**: $H = 70,6\\%$, $A = 61,0\\%$, $M_0 = 0,428$ y Pobreza por Ingresos $= 71,7\\%$.
* **Resto de la ciudad (2021)**: $H = 15,3\\%$, $A = 57,0\\%$, $M_0 = 0,087$ y Pobreza por Ingresos $= 13,8\\%$.
* **Total CABA (2021)**: $H = 17,5\\%$, $A = 57,5\\%$, $M_0 = 0,101$ y Pobreza por Ingresos $= 16,1\\%$.

La comparación intertemporal con los microdatos de **2025** ratifica la hipótesis central de la investigación: **la brecha estructural entre las villas y la ciudad formal no es un fenómeno coyuntural post-pandemia, sino una configuración persistente** donde el índice ajustado $M_0$ en las villas se sostiene entre 4 y 5 veces por encima del resto de la ciudad.
        """)

    st.markdown("---")

    # 3. Acumulación de Desventajas: Matriz de Doble Pobreza (Tabla 3.7)
    st.markdown("##### 3. Pobreza estructural")
    st.markdown("""
**David Gordon (2006)** ilustra la dinámica de la pobreza distinguiendo las trayectorias de ingresos —altamente sensibles al ciclo económico y shocks de empleo— frente a las condiciones materiales de vida, vinculadas a la provisión de bienes públicos, infraestructura y activos del hogar. Cuando ambas carencias se superponen (**pobreza multidimensional + pobreza monetaria**), se consolida un núcleo duro de exclusión donde la informalidad del hábitat opera simultáneamente como efecto y causa reproductora de la pobreza (**Smolka, 2003; Del Castillo, 2011**).
    """)

    overlap_dict = {}
    for d in dominios_presentes:
        sub = df_view[df_view["dominio_desc"] == d]
        overlap_dict[d] = calculate_poverty_overlap(sub)
    if len(df_view) > 0:
        overlap_dict["Total CABA"] = calculate_poverty_overlap(df_view)

    if overlap_dict:
        overlap_df = pd.DataFrame(overlap_dict)

        st.markdown("**Cuadro comparativo de superposición de pobrezas (%)**")
        table_overlap = _format_df_percentages(overlap_df)
        st.dataframe(table_overlap, width="stretch")
        st.caption(SOURCE_CAPTION)

    st.markdown("---")

    # 4. Profundidad e Intensidad de la Privación (Figura 3.2)
    st.markdown("### 4. Proporción de Hogares Pobres según Cantidad de Privaciones Acumuladas (Figura 3.2)")
    st.markdown("""
Al observar la distribución interna de los hogares identificados como pobres multidimensionales:
* En el **Resto de la ciudad**, más de la mitad de los hogares pobres se concentran exactamente sobre el umbral mínimo de corte ($2$ dimensiones privadas).
* En las **Villas y barrios populares**, cerca de **dos tercios de los hogares pobres acumulan entre 3, 4 y 5 dimensiones privadas simultáneamente**, demostrando que la pobreza en el hábitat informal es mucho más intensa y severa.
    """)

    dist_dict = {}
    for d in dominios_presentes:
        sub = df_view[df_view["dominio_desc"] == d]
        dist = calculate_deprivation_distribution(sub)
        dist_dict[d] = {
            "2 dimensiones privadas": dist.get(2, 0.0),
            "3 dimensiones privadas": dist.get(3, 0.0),
            "4 dimensiones privadas": dist.get(4, 0.0),
            "5 dimensiones privadas": dist.get(5, 0.0),
        }

    if dist_dict:
        dist_df = pd.DataFrame(dist_dict)
        col_d1, col_d2 = st.columns([1.2, 1])
        with col_d1:
            st.bar_chart(dist_df)
            st.caption(SOURCE_CAPTION)
        with col_d2:
            st.dataframe(_format_df_percentages(dist_df), width="stretch")
            st.caption(SOURCE_CAPTION)


def render_tab_discusion_metodologica(df_view: pd.DataFrame) -> None:
    """Pestaña 2: Capítulo 2 de la tesis - Debate entre Método Consensual y Alkire-Foster."""
    st.subheader("⚖️ Capítulo 2: Medición de la Pobreza Multidimensional (Alkire-Foster vs. Método Consensual)")
    st.markdown("""
El avance de las conceptualizaciones sobre el bienestar llevó a que la **CEPAL (2013)** y los institutos de estadística de la región impulsaran mediciones multidimensionales complementarias al ingreso. Mientras casi toda América Latina adoptó adaptaciones del método de **Alkire y Foster (2007)** de la *Oxford Poverty and Human Development Initiative* (**OPHI**) —con el caso singular de **México (CONEVAL, 2019)** que combina ingreso, privación social de Gordon y medidas de Alkire-Foster—, la CABA optó a contramano de la región por el **Método Consensual** europeo (**DGEyC, 2021b, 2022**).
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
#### 2.1. La Metodología Alkire – Foster (2007)
* **Fundamento**: Basada en el enfoque de capacidades de **Sen (1983, 1999)**, derechos humanos (**Florio y Labrunée, 2021**) y la familia de medidas FGT (**Foster, Greer y Thorbecke, 1984**). Adoptada oficialmente en Colombia (**DANE, 2023**), Costa Rica (**INEC, 2015**) y República Dominicana (**SIUBEN, 2017**).
* **Doble umbral (*Dual Cut-off*)**:
  1. *Primer corte ($z_j$ / $k_{\\text{intra}}$)*: Identifica si el hogar está privado en cada dimensión según sus indicadores aplicables.
  2. *Segundo corte ($k$ / $k_{\\text{inter}}$)*: Define la suma mínima de privaciones simultáneas ($c_i \\ge k$) para identificar al hogar como pobre multidimensional.
* **Medidas agregadas y propiedades (**Hernández Téllez y Macció, 2020; Santos, 2019**)**:
  - **Incidencia ($H = q/n$)**: Proporción de hogares pobres.
  - **Intensidad ($A$)**: Promedio de privaciones entre los pobres (censurando a los no pobres).
  - **Tasa de recuento ajustada ($M_0 = H \\times A$)**: Satisface **monotonicidad dimensional** (si un hogar pobre sufre una privación adicional, $M_0$ aumenta, mientras que $H$ es insensible) y **descomponibilidad aditiva** por subgrupos y dimensiones.
* **Desafío**: La selección de dimensiones, ponderaciones y umbrales requiere criterios normativos explícitos (**Macció y Mitchell, 2019; Santos, 2019**).
        """)

    with col2:
        st.warning("""
#### 2.2. El Método Consensual (Gordon, 2006; Mack y Lansley, 1985)
* **Fundamento**: Basada en la privación relativa de **Townsend (1979, 2003)** y **Guio et al. (2017)** en el Reino Unido y la Unión Europea. Busca sustraer la definición de pobreza del juicio arbitrario de expertos para someterla a una representación "democrática" de la sociedad.
* **Etapas de cálculo en CABA (**DGEyC, 2021b**)**:
  1. *Consenso social*: Se consulta qué ítems son necesarios para vivir dignamente en CABA (umbral de acuerdo social) y se contabilizan sólo las carencias ocurridas *por falta de recursos económicos*.
  2. *Filtros estadísticos*: Los ítems se someten cada año a pruebas de **validez** (ANOVA y regresiones logísticas contra ingresos) y **confiabilidad** estadística.
  3. *Agregación*: Reporta únicamente la tasa de incidencia ($H = q/n$).
* **Críticas y límites en sociedades desiguales**:
  - Dependencia del cuestionario (**Walker, 1987**), prácticas presupuestarias intrahogar (**Piachaud, 1987**) y preferencias adaptativas (**McKay, 2004**).
  - **El choque con la desigualdad latinoamericana (**Cecchini, 2019; De la Mata y Berniell, 2022; Macció y Mitchell, 2023**)**: En sociedades altamente desiguales y segregadas, presuponer que existe un consenso homogéneo entre la ciudad formal (96% ponderado) y las villas (4% ponderado) **oculta el núcleo irreductible de pobreza (Sen, 1983)** y descarta estadísticamente privaciones graves que sufren las minorías segregadas.
        """)

    st.markdown("---")

    # Contribución relativa de cada dimensión a M0 (Tabla A.3)
    st.markdown("### 🧩 Contribución Porcentual de cada Dimensión al Índice Ajustado $M_0$ (Tabla A.3)")
    st.markdown("""
Gracias a la propiedad de descomponibilidad de **Alkire y Foster (2007)** sobre la matriz censurada, podemos descomponer qué peso relativo tiene cada dimensión en la conformación de la pobreza multidimensional ($M_0$) de cada territorio. Se observa cómo en las **Villas** crece sustancialmente el peso relativo de **Vivienda y servicios**, mientras que **Alimentación** y **Privación social y educación** explican conjuntamente cerca del 60% del índice.
    """)

    dominios_presentes = [d for d in MAP_DOMINIO.values() if d in df_view["dominio_desc"].unique()]
    contrib_dict = {}

    if len(df_view) > 0:
        contrib_dict["Total CABA"] = calculate_dimension_contributions(df_view)

    for d in dominios_presentes:
        sub = df_view[df_view["dominio_desc"] == d]
        contrib_dict[d] = calculate_dimension_contributions(sub)

    if contrib_dict:
        contrib_df = pd.DataFrame(contrib_dict)
        col_c1, col_c2 = st.columns([1.2, 1])
        with col_c1:
            st.bar_chart(contrib_df)
            st.caption(SOURCE_CAPTION)
        with col_c2:
            table_contrib = _format_df_percentages(contrib_df)
            st.dataframe(table_contrib, width="stretch")
            st.caption(SOURCE_CAPTION)


def render_tab_discusion_indicadores(df_view: pd.DataFrame, k_intra: float) -> None:
    """Pestaña 3: Discusión profunda sobre la inclusión y exclusión de indicadores."""
    st.subheader("🧩 Discusión de Indicadores: ¿Por qué se Incluyen o Excluyen y Qué Falta Medir?")
    st.markdown("""
En el diseño oficial de la CABA se utilizan **5 dimensiones**: *(1) Alimentación, (2) Salud y cuidados, (3) Vivienda y servicios, (4) Equipamiento del hogar y (5) Privación social y educación*. Sin embargo, al someter cada indicador anualmente a consenso y pruebas psicométricas de validez y confiabilidad por subgrupo, quedaron **16 indicadores para hogares sin menores de 18 años** y **27 indicadores para hogares con menores de 18 años** (Tabla 3.2 de la tesis).

Este procedimiento estadístico genera **tres grandes problemas metodológicos y de diagnóstico** cuando se analiza la realidad de las villas:
    """)

    # Problema 1: Indicadores relevados en el módulo PM pero excluidos del cálculo oficial
    st.markdown("### 1. Indicadores relevados en el módulo de PM pero excluidos por filtros estadísticos")
    st.markdown("""
En la propia base de datos del módulo de Pobreza Multidimensional de la EAH existen preguntas que fueron relevadas en campo, pero **fueron descartadas total o parcialmente del cálculo del índice** por no superar las pruebas estadísticas de validez/confiabilidad en el promedio de la ciudad:
* **La exclusión de la conexión eléctrica formal (`pm21`) en hogares sin NNyA**: En el *Resto de la ciudad*, sólo el **0,1%** de los hogares sin menores carece de medidor eléctrico formal, por lo que el test estadístico global descarta la variable para ese grupo. ¡Pero en las **Villas**, el **47,0%** de los hogares sin menores sufre esta carencia (y el **69,8%** en hogares con menores)! Al excluirla, un hogar adulto en una villa sin medidor eléctrico no suma privación en *Vivienda y servicios*.
* **La exclusión de los indicadores de asistencia escolar (`pm72` Jardín 3-5 años y `pm75` Secundaria 15-17 años)**: Ambos se relevan en la EAH, pero como preguntan únicamente si la inasistencia escolar ocurre *"por falta de recursos económicos"*, la tasa declarada es menor al 0,8% y quedan fuera del índice. Como resultado, la dimensión llamada **"Privación social y educación"** no mide educación ni escolaridad alguna: sólo mide tener útiles (`pm78`) o computadora (`pm81`), y queda dominada por **vacaciones (`pm87`)** y **gastos personales (`pm84`)**, que son simples proxies de ingreso monetario.
* **La exclusión de la asistencia a comedores comunitarios (`hpm4`)**: Aunque más de **1 de cada 4 hogares en villas (26,8%)** recurre a comedores o merenderos comunitarios para alimentarse (frente a sólo 2,2% en el resto de la ciudad), este indicador no se computa en la dimensión *Alimentación*.
    """)

    excl_rows = []
    df_villas = df_view[df_view["dominio"] == 3] if "dominio" in df_view.columns else pd.DataFrame()
    df_resto = df_view[df_view["dominio"] == 4] if "dominio" in df_view.columns else pd.DataFrame()

    for item in INDICADORES_EXCLUIDOS_MODULO_PM:
        var = item["variable"]
        univ = item["universo_excluido"]
        if univ == "Hogares sin NNyA":
            sub_v = df_villas[df_villas["tiene_nnya"] == 0] if len(df_villas) else pd.DataFrame()
            sub_r = df_resto[df_resto["tiene_nnya"] == 0] if len(df_resto) else pd.DataFrame()
        elif univ == "Hogares con NNyA":
            sub_v = df_villas[df_villas["tiene_nnya"] == 1] if len(df_villas) else pd.DataFrame()
            sub_r = df_resto[df_resto["tiene_nnya"] == 1] if len(df_resto) else pd.DataFrame()
        else:
            sub_v = df_villas
            sub_r = df_resto

        t_v = calculate_indicator_rate(sub_v, var) if len(sub_v) else None
        t_r = calculate_indicator_rate(sub_r, var) if len(sub_r) else None

        excl_rows.append({
            "Variable": var,
            "Indicador relevado en EAH": item["etiqueta"],
            "Dimensión": item["dimension"],
            "Grupo donde se excluye": univ,
            "Privación en Villas (%)": format_percentage(t_v) if t_v is not None else "—",
            "Privación en Resto (%)": format_percentage(t_r) if t_r is not None else "—",
            "Discusión metodológica": item["motivo_exclusion"],
        })

    if excl_rows:
        st.dataframe(pd.DataFrame(excl_rows), width="stretch", hide_index=True)
        st.caption(SOURCE_CAPTION)

    st.markdown("---")

    # Problema 2: Indicadores estructurales de hábitat y vivienda presentes en la EAH pero omitidos del IPM
    st.markdown("### 2. El gran ausente: Hábitat, Saneamiento Básico, Hacinamiento y Tenencia del Suelo")
    st.markdown("""
Como advierten **Macció y Mitchell (2023)**, la segregación residencial oculta las Necesidades Básicas Insatisfechas (NBI) bajo un enfoque relativo diseñado para las clases medias urbanas. La definición operativa del **RENABAP (2022)** identifica a un barrio popular por tres carencias estructurales: **irregularidad en la tenencia del suelo, falta de red cloacal formal y falta de agua corriente o energía eléctrica con medidor**.

Al cruzar los microdatos generales de vivienda de la propia EAH 2025, comprobamos que estas privaciones estructurales —que **no forman parte del IPM oficial**— exhiben brechas extremas en las villas y constituyen la base material de las *trampas de pobreza* (**Marx, Stoker y Suri, 2013; Rofman, 2015**):
    """)

    dominios_presentes = [d for d in MAP_DOMINIO.values() if d in df_view["dominio_desc"].unique()]
    hab_dict = {}
    for d in dominios_presentes:
        sub = df_view[df_view["dominio_desc"] == d]
        hab_dict[d] = calculate_structural_habitat_rates(sub)
    if len(df_view) > 0:
        hab_dict["Total CABA"] = calculate_structural_habitat_rates(df_view)

    if hab_dict:
        hab_df = pd.DataFrame(hab_dict)
        col_h1, col_h2 = st.columns([1.2, 1])
        with col_h1:
            st.bar_chart(hab_df)
            st.caption(SOURCE_CAPTION)
        with col_h2:
            st.dataframe(_format_df_percentages(hab_df), width="stretch")
            st.caption(SOURCE_CAPTION)

    st.markdown("---")

    # Problema 3: Análisis dimensión por dimensión (No Censuradas y Censuradas)
    st.markdown("### 3. Tasas de Privación por Dimensión: Matriz No Censurada (Tabla 3.5) vs. Matriz Censurada (Tabla A.2)")
    st.markdown("""
* **Alimentación (el daño biológico e intergeneracional)**: Más del **60%** de los hogares en villas sufre privación alimentaria. No acceder a una nutrición adecuada en la niñez produce secuelas irreversibles en las capacidades cognitivas y laborales futuras.
* **Privación social y educación**: Es la dimensión con mayor privación en villas (>70%), traccionada por la imposibilidad de tomar vacaciones y realizar gastos personales, sumada a la brecha digital (falta de computadora para estudiar en hogares con NNyA).
* **Vivienda y servicios**: Afecta a más de la mitad de los hogares en villas (frente a menos del 10% en el resto de la ciudad), impulsada por la falta de conexión eléctrica con medidor, falta de agua caliente, goteras y falta de ambientes separados para dormir.
    """)

    tipo_matriz_dim = st.radio(
        "Seleccione el tipo de matriz dimensional a visualizar:",
        options=[
            "Matriz No Censurada (Tabla 3.5: Todos los hogares privados en la dimensión)",
            "Matriz Censurada (Tabla A.2: Hogares privados en la dimensión que además son pobres IPM)",
        ],
        horizontal=True,
    )
    es_censurada_dim = "Censurada (Tabla A.2" in tipo_matriz_dim

    dim_chart_dict = {d: {} for d in dominios_presentes}
    dim_rows = []

    for d_k, d_v in DIMENSIONES_INDICADORES_IPM.items():
        col_priv = f"{d_k}_privada"
        if col_priv not in df_view.columns:
            continue

        label_dim = d_v["meta"]["label"]
        serie_tot = df_view[col_priv] * df_view["pobre_ipm"] if es_censurada_dim else df_view[col_priv]
        tasa_total = float(np.average(serie_tot, weights=df_view["fexp"]) * 100) if len(df_view) > 0 else 0.0

        row = {
            "Dimensión": label_dim,
            "Total CABA (%)": format_percentage(tasa_total),
        }

        for d in dominios_presentes:
            sub = df_view[df_view["dominio_desc"] == d]
            if len(sub) > 0:
                serie_sub = sub[col_priv] * sub["pobre_ipm"] if es_censurada_dim else sub[col_priv]
                tasa_dom = float(np.average(serie_sub, weights=sub["fexp"]) * 100)
            else:
                tasa_dom = 0.0
            row[f"{d} (%)"] = format_percentage(tasa_dom)
            dim_chart_dict[d][label_dim] = tasa_dom

        dim_rows.append(row)

    if dim_rows:
        col_dim1, col_dim2 = st.columns([1.2, 1])
        with col_dim1:
            st.bar_chart(pd.DataFrame(dim_chart_dict))
            st.caption(SOURCE_CAPTION)
        with col_dim2:
            st.dataframe(pd.DataFrame(dim_rows), width="stretch", hide_index=True)
            st.caption(SOURCE_CAPTION)


def render_tab_indicadores_detalle(df_view: pd.DataFrame, tipos_hogar_seleccionados: list[str]) -> None:
    """Pestaña 4: Detalle por presencia de NNyA e indicadores individuales (Tablas A.4, A.5 y A.6)."""
    st.subheader("📋 Desagregación por Presencia de NNyA y Tasas por Indicador (Tablas A.4, A.5 y A.6)")

    # 1. Resumen de IPM según presencia de NNyA
    st.markdown("### 1. Pobreza Multidimensional según Presencia de Niños, Niñas y Adolescentes (NNyA)")
    st.markdown("""
Los hogares con presencia de menores de 18 años enfrentan mayores exigencias de cuidado, espacio habitacional, equipamiento educativo y nutrición, registrando una incidencia de pobreza multidimensional significativamente más elevada que los hogares sin menores.
    """)

    rows_nnya = []
    for tiene_nnya, nombre in [(1, "Hogares con NNyA (menores de 18 años)"), (0, "Hogares sin NNyA")]:
        sub_df = df_view[df_view["tiene_nnya"] == tiene_nnya]
        if len(sub_df) > 0:
            m = calculate_ipm_metrics(sub_df)
            p_ing = (
                float(np.average(sub_df["pobre_ingreso"], weights=sub_df["fexp"]) * 100)
                if "pobre_ingreso" in sub_df.columns
                else 0.0
            )
            rows_nnya.append({
                "Tipo de hogar": nombre,
                "Incidencia IPM (H)": format_percentage(m.h * 100),
                "Intensidad (A)": format_percentage(m.a * 100),
                "IPM Ajustado (M0)": format_decimal(m.m0, decimales=3),
                "Pobreza por Ingresos": format_percentage(p_ing),
                "Muestra (N)": format_integer(len(sub_df)),
                "Hogares expandidos": format_integer(m.hogares_expandidos),
                "Hogares pobres IPM (exp)": format_integer(m.pobres_expandidos),
            })

    if rows_nnya:
        st.dataframe(pd.DataFrame(rows_nnya), width="stretch", hide_index=True)
        st.caption(SOURCE_CAPTION)

    st.markdown("---")

    # Selector Censurado vs No Censurado
    st.markdown("### 2. Tasas de Privación por Indicador Individual según Marco Muestral")
    modo_ind = st.radio(
        "Modo de cálculo de las tasas por indicador:",
        options=[
            "Tasas No Censuradas (% sobre el total de hogares a los que aplica el indicador)",
            "Tasas Censuradas — Criterio Tablas A.4, A.5 y A.6 de la Tesis (% de hogares con carencia y pobres IPM)",
        ],
        horizontal=True,
    )
    es_censurado = "Censuradas — Criterio Tablas" in modo_ind

    dominios_presentes = [d for d in MAP_DOMINIO.values() if d in df_view["dominio_desc"].unique()]

    # 2.a Tabla A.4: Indicadores comunes a todos los hogares
    st.markdown("#### 🔹 Indicadores comunes a hogares con y sin menores de 18 años (Tabla A.4)")
    comunes_records = []
    for var, (dim_label, ind_label) in INDICADORES_COMUNES.items():
        t_tot = calculate_indicator_rate(df_view, var, censurado=es_censurado)
        rec = {
            "Dimensión": dim_label,
            "Indicador": ind_label,
        }
        for d in dominios_presentes:
            sub_d = df_view[df_view["dominio_desc"] == d]
            t_d = calculate_indicator_rate(sub_d, var, censurado=es_censurado)
            rec[f"{d} (%)"] = format_percentage(t_d) if t_d is not None else "—"
        rec["Total CABA (%)"] = format_percentage(t_tot) if t_tot is not None else "—"
        comunes_records.append(rec)

    if comunes_records:
        st.dataframe(pd.DataFrame(comunes_records), width="stretch", hide_index=True)
        st.caption(SOURCE_CAPTION)

    # 2.b Tablas A.6 y A.5: Desglose por tipo de hogar
    grupos = [
        (1, "Hogares con NNyA", "hogares_con_nnya", "Tabla A.6: 27 indicadores para hogares con menores de 18 años"),
        (0, "Hogares sin NNyA", "hogares_sin_nnya", "Tabla A.5: 16 indicadores para hogares sin menores de 18 años"),
    ]

    for tiene_nnya, nombre, grupo, titulo_tabla in grupos:
        if nombre not in tipos_hogar_seleccionados:
            continue

        st.markdown(f"#### 🔹 {titulo_tabla}")
        df_grupo = df_view[df_view["tiene_nnya"] == tiene_nnya]
        if len(df_grupo) == 0:
            st.info(f"No hay datos para {nombre} con los filtros seleccionados.")
            continue

        indicador_records = []
        for d_v in DIMENSIONES_INDICADORES_IPM.values():
            for variable, etiqueta in d_v[grupo].items():
                tasa_total = calculate_indicator_rate(df_grupo, variable, censurado=es_censurado)
                rec = {
                    "Dimensión": d_v["meta"]["label"],
                    "Variable": variable,
                    "Indicador": etiqueta,
                }
                for d in dominios_presentes:
                    sub_d = df_grupo[df_grupo["dominio_desc"] == d]
                    t_dom = calculate_indicator_rate(sub_d, variable, censurado=es_censurado)
                    rec[f"{d} (%)"] = format_percentage(t_dom) if t_dom is not None else "—"

                rec["Total CABA (%)"] = format_percentage(tasa_total) if tasa_total is not None else "—"
                indicador_records.append(rec)

        st.dataframe(pd.DataFrame(indicador_records), width="stretch", hide_index=True)
        st.caption(SOURCE_CAPTION)


def render_tab_conclusiones() -> None:
    """Pestaña 5: Capítulo 4 (Conclusiones), Anexo RENABAP (Tabla A.1) y Bibliografía Completa."""
    st.subheader("📜 Capítulo 4: Conclusiones, Barrios Populares (RENABAP) y Bibliografía")

    st.markdown("""
### Síntesis de Conclusiones y Recomendaciones para la Política Pública

La iniciativa de elaborar estadísticas oficiales sobre pobreza multidimensional en la CABA constituye un avance valioso frente a la ausencia de un IPM oficial a nivel nacional en la Argentina. Sin embargo, al incorporar la dimensión territorial e indagar en las brechas entre las villas y la ciudad "formal", emergen **cuatro conclusiones centrales**:

1. **Subestimación poblacional y estadística**:
   La subrepresentación del marco muestral de villas en la EAH (~3,8%–4,0% expandido frente a más del 10,4% real relevado por el RENABAP) conlleva una subestimación sistemática de los niveles globales de pobreza por ingresos y multidimensional de la Ciudad de Buenos Aires.
2. **Omisión de indicadores de pobreza estructural y reproducción intergeneracional**:
   El diseño del índice excluye variables estrechamente vinculadas con las *trampas de pobreza* en las villas: el acceso formal al agua potable y saneamiento básico (red cloacal), el hacinamiento crítico, la seguridad en la tenencia del suelo y los indicadores efectivos de asistencia, terminalidad y calidad educativa.
3. **Límites del enfoque consensual relativo en ciudades segregadas**:
   La utilización de enfoques relativos de privación en sociedades con altos niveles de desigualdad —visibles incluso geográficamente— tiende a ocultar la segmentación en la provisión de servicios públicos. Al exigir consenso y varianza estadística sobre el promedio de la ciudad formal, se descartan carencias agudas (como la falta de medidor eléctrico formal en hogares sin niños) que golpean casi exclusivamente a los asentamientos informales.
4. **Mayor incidencia, mayor intensidad y doble pobreza**:
   La pobreza multidimensional en las villas no sólo es cerca de **4,5 veces superior** en incidencia ($H$) a la del resto de la ciudad, sino que es en promedio **más intensa ($A$)** al evaluarse con la metodología de **Alkire y Foster (2007)**, quintuplicando la tasa ajustada ($M_0$) y concentrando un núcleo duro donde cerca de la mitad de los hogares sufre simultáneamente pobreza monetaria y multidimensional.

> **Horizonte de política pública**: En la Argentina existen más de **1,17 millones de familias en 5.687 barrios populares** según el RENABAP. Constituir una medición multidimensional oficial y nacional requiere superar las políticas meramente asistenciales de ingresos —que aunque indispensables para las economías domésticas vulneradas no logran por sí solas perforar el piso estructural— hacia políticas focalizadas de **integración urbana, infraestructura sanitaria, vivienda y educación** que igualen las condiciones básicas de vida y permitan quebrar la persistencia intergeneracional de la pobreza.
    """)

    st.markdown("---")

    with st.expander("🗺️ Anexo Tabla A.1: Las 50 villas, NHT y asentamientos contabilizados por el RENABAP en la CABA"):
        st.markdown("""
La mayor concentración de barrios populares se ubica en las comunas del sur de la CABA (**Comunas 4, 8, 7 y 9**), en estrecha correspondencia con los patrones históricos de segregación residencial.
        """)
        barrios_caba = [
            {"ID RENABAP": 2552, "Barrio popular": "Rodrigo Bueno", "Comuna": "Comuna 1"},
            {"ID RENABAP": 4637, "Barrio popular": "Padre Mugica (Ex Villa 31 y 31 Bis)", "Comuna": "Comuna 1"},
            {"ID RENABAP": 2553, "Barrio popular": "Saldías", "Comuna": "Comuna 2"},
            {"ID RENABAP": 2554, "Barrio popular": "Zavaleta", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2557, "Barrio popular": "El Pueblito", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2558, "Barrio popular": "Villa 26", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2559, "Barrio popular": "El Campito", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2560, "Barrio popular": "19 de Octubre (Lamadrid)", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2562, "Barrio popular": "Puente Barracas", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2563, "Barrio popular": "Luján 2364", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2564, "Barrio popular": "Lamadrid", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2565, "Barrio popular": "Agustín de Vedia", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2566, "Barrio popular": "Agustín Magaldi", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2568, "Barrio popular": "Pedro de Mendoza", "Comuna": "Comuna 4"},
            {"ID RENABAP": 2570, "Barrio popular": "Villa 21-24", "Comuna": "Comuna 4"},
            {"ID RENABAP": 4251, "Barrio popular": "La Rotonda", "Comuna": "Comuna 4"},
            {"ID RENABAP": 4470, "Barrio popular": "Pedro de Mendoza y Villarino", "Comuna": "Comuna 4"},
            {"ID RENABAP": 4471, "Barrio popular": "Matanza y Ferre", "Comuna": "Comuna 4"},
            {"ID RENABAP": 4472, "Barrio popular": "La Esquina", "Comuna": "Comuna 4"},
            {"ID RENABAP": 4941, "Barrio popular": "Zanchetti", "Comuna": "Comuna 4"},
            {"ID RENABAP": 4942, "Barrio popular": "El Pescadito", "Comuna": "Comuna 4"},
            {"ID RENABAP": 4634, "Barrio popular": "Playón de Caballito", "Comuna": "Comuna 6"},
            {"ID RENABAP": 2576, "Barrio popular": "Villa 13 Bis", "Comuna": "Comuna 7"},
            {"ID RENABAP": 2577, "Barrio popular": "Padre Rodolfo Ricciardelli (Ex Villa 1-11-14)", "Comuna": "Comuna 7"},
            {"ID RENABAP": 2578, "Barrio popular": "Barrio Obrero", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2579, "Barrio popular": "Barrio INTA", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2580, "Barrio popular": "Calacita", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2581, "Barrio popular": "Los Piletones", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2582, "Barrio popular": "La Esperanza", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2583, "Barrio popular": "Villa 15 (Ciudad Oculta)", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2584, "Barrio popular": "Pirelli", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2585, "Barrio popular": "Scapino", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2586, "Barrio popular": "Barrio Fátima", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2587, "Barrio popular": "Los Pinos", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2588, "Barrio popular": "María Auxiliadora", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2592, "Barrio popular": "Villa 20", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2593, "Barrio popular": "Bermejo", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2594, "Barrio popular": "Emaús", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2595, "Barrio popular": "NHT del Trabajo", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2597, "Barrio popular": "Ramón Carrillo", "Comuna": "Comuna 8"},
            {"ID RENABAP": 4294, "Barrio popular": "Santander", "Comuna": "Comuna 8"},
            {"ID RENABAP": 4636, "Barrio popular": "La Veredita", "Comuna": "Comuna 8"},
            {"ID RENABAP": 2598, "Barrio popular": "Lacarra", "Comuna": "Comuna 9"},
            {"ID RENABAP": 2599, "Barrio popular": "Cildáñez", "Comuna": "Comuna 9"},
            {"ID RENABAP": 2600, "Barrio popular": "Nuestro Barrio", "Comuna": "Comuna 9"},
            {"ID RENABAP": 4382, "Barrio popular": "El Ombú", "Comuna": "Comuna 14"},
            {"ID RENABAP": 4635, "Barrio popular": "Sin Nombre", "Comuna": "Comuna 14"},
            {"ID RENABAP": 2602, "Barrio popular": "Playón de Chacarita", "Comuna": "Comuna 15"},
            {"ID RENABAP": 2603, "Barrio popular": "La Carbonilla", "Comuna": "Comuna 15"},
            {"ID RENABAP": 2604, "Barrio popular": "Jorge Newbery", "Comuna": "Comuna 15"},
        ]
        st.dataframe(pd.DataFrame(barrios_caba), width="stretch", hide_index=True)
        st.caption("Fuente: Elaboración propia en base a RENABAP (2022).")

    st.markdown("---")

    st.markdown("### 📚 Bibliografía Citada")
    st.markdown("""
* **Alkire, S. & Foster, J. (2007).** *Counting and Multidimensional Poverty Measurement*. (OPHI Working Paper, 7). Oxford Poverty and Human Development Initiative.
* **Barneche, P., Bugallo, A., Ferrea, H., Ilarregui, M., Monteverde, C., Pérez, V. & Santa María, T. (2010).** Métodos de Medición de la Pobreza. Conceptos y aplicaciones en América Latina. *Entrelíneas de la Política Económica*, 26(4), 31-41. Dirección Provincial de Estadística de la Provincia de Buenos Aires.
* **Beccaria, L. A. & Minujín, A. (1985).** *Métodos alternativos para medir la evolución del tamaño de la pobreza*. (Documentos de trabajo N° 6). Instituto Nacional de Estadística y Censos (INDEC).
* **Boltvinik, J. (2009).** Peter Townsend y el rumbo de la investigación sobre pobreza en Gran Bretaña (Fundamentos y Debate). *Mundo Siglo XXI*, 19, 45-62.
* **Capuano, A. (2015).** *Consideraciones conceptuales y metodológicas sobre la medición de la pobreza infantil*. (Documentos de Trabajo, Red de Posgrados, 47). Buenos Aires: CLACSO.
* **Cecchini, S. (2019).** *Matriz de desigualdad social, enfoque de derechos y Objetivos de Desarrollo Sostenible*. División de Desarrollo Social, CEPAL.
* **CEPAL (2013).** *La medición de la pobreza multidimensional*. (Conferencia Estadística de las Américas XII). Santiago de Chile: CEPAL.
* **Clemente, A. (2013).** La pobreza como categoría de análisis e intervención. En Clemente, A. (coord.), *Territorios Urbanos y Pobreza Persistente*. Buenos Aires: Espacio Editorial.
* **CONEVAL (2019).** *Metodología para la medición multidimensional de la pobreza en México* (3.ª ed.). Ciudad de México: CONEVAL.
* **CONEVAL (s/f).** *Medir la pobreza con varias dimensiones: el aporte metodológico de México al mundo*. México: CONEVAL.
* **DANE (2023).** *Pobreza Multidimensional en Colombia. Año 2022*. Boletín Técnico. Colombia: Departamento Administrativo Nacional de Estadística.
* **De la Mata, D. & Berniell, L. (2022).** *Desigualdad y baja movilidad social en América Latina y el Caribe*. CAF: Banco de Desarrollo de América Latina y el Caribe.
* **Del Castillo, A. C. (2011).** Manifestaciones de la pobreza en tres barrios periféricos de San Miguel de Tucumán (1991-2010). *Plaza Pública*, 4(6), 40-56.
* **Dirección General de Estadísticas y Censos [DGEyC] (2021a).** *Base Usuarios 2021 Encuesta Anual de Hogares Ciudad de Buenos Aires*. Gobierno de la Ciudad de Buenos Aires.
* **Dirección General de Estadísticas y Censos [DGEyC] (2021b).** *La pobreza multidimensional en la Ciudad de Buenos Aires. Año 2019*. (Informe de Resultados, 1531). GCBA.
* **Dirección General de Estadísticas y Censos [DGEyC] (2022).** *La pobreza multidimensional en la Ciudad de Buenos Aires, antes y después de la pandemia. Años 2019 y 2021*. (Informe de Resultados, 1715). GCBA.
* **Domínguez Domínguez, J. & Martín Caraballo, A. M. (2006).** Medición de la pobreza: una revisión de los principales indicadores. *Revista de Métodos Cuantitativos para la Economía y la Empresa*, 2, 27-66.
* **Durlauf, S. & Shaorshadze, I. (2015).** Poverty Traps. En Odekon, M. (ed.), *The SAGE Encyclopedia of World Poverty* (2.ª ed.). SAGE Publications.
* **Feres, J. C. & Mancero, X. (2001).** *Enfoques para la medición de la pobreza. Breve revisión de la literatura*. (Serie Estudios Estadísticos y Prospectivos). CEPAL.
* **Fernandes, E. (2011).** *Regularización de asentamientos informales en América Latina*. Cambridge: Lincoln Institute of Land Policy.
* **Florio, E. M. & Labrunée, M. E. (2021).** Pobreza multidimensional, aproximaciones conceptuales y metodológicas para la evaluación de hogares con niños, niñas y adolescentes en el ámbito del Partido de General Pueyrredón. *FACES*, 27(57), 9-23.
* **Foster, J., Greer, J. & Thorbecke, E. (1984).** A Class of Decomposable Poverty Measures. *Econometrica*, 52(3), 761-766.
* **Gasparini, L., Tornarolli, L. & Gluzmann, P. (2019).** *El desafío de la pobreza en Argentina. Diagnóstico y perspectivas*. Buenos Aires: CEDLAS, CIPPEC, PNUD.
* **Giménez Mercado, C. & Valente Adarme, X. (2016).** Una aproximación a la pobreza desde el enfoque de capacidades de Amartya Sen. *Provincia*, (35), 99-149.
* **Gordon, D. (2006).** The concept and measurement of poverty. En Pantazis, C., Gordon, D. & Levitas, R. (eds.), *Poverty and Social Exclusion in Britain* (pp. 29-70). Bristol: The Policy Press.
* **Guio, A. C., Gordon, D., Najera, H. & Pomati, M. (2017).** *Revising the EU material deprivation variables*. Luxembourg: European Union.
* **Hernández Téllez, G. & Macció, J. (2020).** Condiciones de vida y pobreza multidimensional en las villas del Conurbano Bonaerense: el barrio Puerta de Hierro. *Ensayos de Política Económica*, 3(2), 37-75.
* **IDECBA (2026).** *Encuesta Anual de Hogares (EAH) 2025. Base de usuarios ampliada*. Instituto de Estadística y Censos de la Ciudad Autónoma de Buenos Aires.
* **INDEC (2013).** *Proyecciones provinciales de población por sexo y grupo de edad 2010-2040*. Buenos Aires: INDEC.
* **INDEC (2023a).** *Incidencia de la pobreza y la indigencia en 31 aglomerados urbanos. Segundo semestre de 2022*. Condiciones de vida, 7(4).
* **INDEC (2023b).** *Indicadores de calidad de vida por jurisdicción del Sistema Integrado de Estadísticas Sociales (SIES)*.
* **INEC (2015).** *Índice de pobreza multidimensional: metodología*. Costa Rica: Instituto Nacional de Estadística y Censos.
* **León, D. (2016).** *Enfoque de capacidades en Amartya Sen: Aproximaciones y reflexiones*. MPRA Paper N° 77532.
* **Macció, J. & Lépore, E. (2012).** Las villas en la ciudad de Buenos Aires: fragmentación espacial y segmentación de las condiciones sociales de vida. En Lépore, E. (coord.), *Capacidades de desarrollo y sociedad civil en las villas de la ciudad*. Buenos Aires: Educa.
* **Macció, J. & Mitchell, A. (2019).** *Análisis microeconométrico con la familia de medidas de pobreza multidimensional de Alkire-Foster: una discusión abierta*. (Documento de trabajo, 63). UCA.
* **Macció, J. & Mitchell, A. (2023).** Medición Multidimensional de Pobreza en Ciudades Segregadas: Evidencia de la Ciudad de Buenos Aires. *Revista Desarrollo y Sociedad*, (93), 101-137.
* **Mack, J. & Lansley, S. (1985).** *Poor Britain*. London: Allen and Unwin.
* **Marx, B., Stoker, T. & Suri, T. (2013).** The Economics of Slums in the Developing World. *Journal of Economic Perspectives*, 27(4), 187-210.
* **Massidda, A. L. (2018).** Cómo nombrar a la informalidad: Una revisión de las definiciones de villas en uso, sus implicaciones analíticas y su alcance. *Quid 16*, (10), 2-14.
* **McKay, S. (2004).** Poverty or preference: what do ‘consensual deprivation indicators’ really mean? *Fiscal Studies*, 25, 201-223.
* **Mitlin, D. & Satterthwaite, D. (2013).** *Urban Poverty in the Global South: Scale and Nature*. Routledge.
* **Mora Benitez, D. J. (2023).** *Pobreza multidimensional en las villas de la Ciudad Autónoma de Buenos Aires en el año 2021*. (Tesis de Licenciatura en Economía). Facultad de Ciencias Económicas, Universidad de Buenos Aires.
* **Oxford Poverty and Human Development Initiative [OPHI] (s.f.).** *Multidimensional Poverty*. https://ophi.org.uk/research/multidimensional-poverty
* **Piachaud, D. (1987).** Problems in the Definition and Measurement of Poverty. *Journal of Social Policy*, 16(2), 147-164.
* **PNUD (1990, 1997).** *Informe sobre Desarrollo Humano*. Nueva York: Oxford University Press.
* **RENABAP (2022).** *Manual para la conformación y actualización del Registro Nacional de Barrios Populares*. Secretaría de Integración Socio Urbana, Ministerio de Desarrollo Social de la Nación.
* **Rofman, A. (2015).** Hacia un nuevo enfoque sobre la cuestión de la pobreza estructural. *Debate Público*, 9, 49-55. Facultad de Ciencias Sociales, UBA.
* **Sabatini, F., Cáceres, G. & Cerda, J. (2001).** Segregación residencial en las principales ciudades chilenas: Tendencias de las tres últimas décadas y posibles cursos de acción. *EURE (Santiago)*, 27(82), 21-42.
* **Santos, M. E. (2019).** *Desafíos en el diseño de medidas de pobreza multidimensional*. (Serie Estudios Estadísticos, 100). Santiago: CEPAL.
* **Sen, A. (1983).** Poor, Relatively Speaking. *Oxford Economic Papers*, 35(2), 153-169.
* **Sen, A. (1999).** *Development as Freedom*. New York: First Anchor Books.
* **SIUBEN (2017).** *Índice de Pobreza Multidimensional de la República Dominicana*. Santo Domingo: Sistema Único de Beneficiarios.
* **Smolka, M. (2003).** Informalidad, pobreza urbana y precio de la tierra. *Land Lines*, 15(1). Cambridge: Lincoln Institute of Land Policy.
* **Suárez, A. L. & Lépore, E. (2014).** Las villas de emergencia de la ciudad de Buenos Aires. En Suárez, A. L., Mitchell, A. & Lépore, E. (eds.), *Las villas de la ciudad de Buenos Aires: territorios frágiles de inclusión social*. Buenos Aires: Educa.
* **Townsend, P. (1979).** *Poverty in the United Kingdom*. London: Allen Lane and Penguin Books.
* **Townsend, P. (2003).** La Conceptualización de la Pobreza. *Revista Comercio Exterior*, 53(5).
* **UN-Habitat (2002).** *Expert group meeting on slum indicators*. Nairobi: UN-Habitat.
* **UN-Habitat (2003).** *The Challenge of Slums: Global Report on Human Settlements 2003*. London: Earthscan Publications.
* **UN-Habitat (2020).** *Proportion of Urban Population Living in Slum Households by Country or area 2000-2020*. Global Urban Indicators Database.
* **Walker, R. (1987).** Consensual Approaches to the Definition of Poverty: Towards an Alternative Methodology. *Journal of Social Policy*, 16(2), 213-226.
* **Ziccardi, A. (1977).** *Políticas de vivienda y movimientos urbanos: El caso de Buenos Aires (1963-1973)*. Buenos Aires: CEUR, Instituto Torcuato Di Tella.
    """)

    with st.expander("📋 Cita académica en formato BibTeX"):
        st.code("""@mastersthesis{mora2023pobreza,
  author       = {Diego J. Mora Benitez},
  title        = {Pobreza multidimensional en las villas de la Ciudad Autónoma de Buenos Aires en el año 2021},
  school       = {Facultad de Ciencias Económicas, Universidad de Buenos Aires},
  year         = {2023},
  type         = {Tesis de Licenciatura en Economía},
  note         = {Tutora: Mg. Andrea Zaidel. Seminario de Integración y Aplicación (Cát. Lic. César Hernán Ruggeri)}
}""", language="bibtex")


def render_analysis_tabs(
    df_view: pd.DataFrame,
    k_intra: float,
    tipos_hogar_seleccionados: list[str],
    raw_df: pd.DataFrame | None = None,
) -> None:
    """Renderiza el conjunto completo de pestañas del dashboard con storytelling estructurado."""
    tab_brecha, tab_metodologia, tab_indicadores_disc, tab_detalle, tab_conclusiones = st.tabs([
        "🏙️ 1. Brecha Territorial y Muestra",
        "⚖️ 2. Debate Metodológico",
        "🧩 3. Discusión de Indicadores",
        "📋 4. Detalle por Indicador y NNyA",
        "📜 5. Conclusiones y Bibliografía",
    ])

    with tab_brecha:
        render_tab_brecha_territorial(df_view, raw_df=raw_df)

    with tab_metodologia:
        render_tab_discusion_metodologica(df_view)

    with tab_indicadores_disc:
        render_tab_discusion_indicadores(df_view, k_intra)

    with tab_detalle:
        render_tab_indicadores_detalle(df_view, tipos_hogar_seleccionados)

    with tab_conclusiones:
        render_tab_conclusiones()
