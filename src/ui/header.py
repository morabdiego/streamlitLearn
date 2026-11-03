"""Componente de encabezado, contextualización teórica e histórica de la tesis."""
import pandas as pd
import streamlit as st


def render_header(anio: int) -> None:
    """Renderiza el título principal, autoría y el marco teórico-histórico del estudio."""
    st.title("🏙️ Pobreza Multidimensional en las Villas de la Ciudad Autónoma de Buenos Aires")
    st.markdown(
        f"**Actualización empírica y discusión metodológica con microdatos de la EAH ({anio})**  \n"
        "*Basado en la tesis de Licenciatura en Economía de **Diego J. Mora Benitez** "
        "(Facultad de Ciencias Económicas, Universidad de Buenos Aires • Tutora: Mg. Andrea Zaidel)*"
    )

    with st.expander(
        "📖 Capítulo 1: Marco Teórico, Enfoques de Pobreza, Villas y Trampas de Pobreza Estructural",
        expanded=False,
    ):
        col_teo1, col_teo2 = st.columns(2)

        with col_teo1:
            st.markdown("""
#### 1.1. Conceptualizaciones y el debate Absoluto vs. Relativo
Desde el retorno a la democracia en 1983, la pobreza por ingresos en la Argentina mantiene un piso estructural difícil de perforar aún en etapas de crecimiento económico (**Gasparini et al., 2019**). Como señalan **Clemente (2013)**, **Capuano (2015)** y **Giménez Mercado y Valente Adarme (2016)**, abordar este fenómeno exige superar el minimalismo del enfoque monetario o biológico de subsistencia (**Rowntree, 1901**) y resolver dos problemas metodológicos: la **identificación** de quiénes son pobres y la **agregación** en un índice sintético (**Domínguez Domínguez y Martín Caraballo, 2006; Barneche et al., 2010; Feres y Mancero, 2001**).

En la literatura destacan dos grandes tradiciones que dieron origen a las mediciones actuales (**Boltvinik, 2009**):
* **El enfoque de privación relativa (Peter Townsend, 1979, 2003)**: Critica la arbitrariedad de las canastas de subsistencia y define la pobreza como la carencia de recursos para obtener los tipos de alimentación, participar en las actividades y tener las condiciones de vida que son habituales o socialmente aprobadas en la sociedad a la que se pertenece. Es la génesis del **Método Consensual** (**Mack y Lansley, 1985; Gordon, 2006**).
* **El enfoque de capacidades y realizaciones (Amartya Sen, 1983, 1999)**: Evalúa el bienestar en términos de *funcionamientos* (lo que una persona valora ser o hacer) y *capacidades* (la libertad real para lograrlo; **León, 2016; PNUD, 1997**). En respuesta al relativismo de Townsend, **Sen (1983)** advierte que no debe confundirse pobreza con desigualdad: **existe un núcleo irreductible de pobreza absoluta** en el espacio de las capacidades básicas. Este enfoque —junto al enfoque de derechos (**Florio y Labrunée, 2021**) y antecedentes como NBI (**Beccaria y Minujín, 1985**)— fundamenta la metodología de **Alkire y Foster (2007)** derivada de la familia FGT (**Foster, Greer y Thorbecke, 1984**).
            """)

        with col_teo2:
            st.markdown("""
#### 1.2. Villas, Segregación Urbana y Trampas de Pobreza
Las definiciones convencionales suelen omitir la escala, naturaleza y localización espacial de la pobreza, subestimándola en asentamientos informales (**Mitlin y Satterthwaite, 2013**). En la CABA, las villas constituyen verdaderos **"enclaves urbanos de la pobreza"** (**Ziccardi, 1977**) marcados por la segregación residencial (**Sabatini et al., 2001**), la ocupación de tierras públicas, trama urbana irregular, alta densidad y verticalización (**UN-Habitat, 2002, 2003, 2020; Fernandes, 2011; Massidda, 2018; Suárez y Lépore, 2014**).

La permanencia intergeneracional en estos territorios configura lo que las ciencias sociales denominan **pobreza persistente o estructural** (**Rofman, 2015**) y la literatura económica modela como **trampas de pobreza**:
1. **Trampa de capital humano y salud (Marx, Stoker y Suri, 2013)**: La alimentación inadecuada, el déficit de agua y saneamiento y el hacinamiento deterioran tempranamente la salud infantil y condicionan los ingresos futuros.
2. **Trampa de baja acumulación de capital físico (Marx, Stoker y Suri, 2013)**: La inseguridad en la tenencia del suelo y el riesgo de desalojo desincentivan la inversión familiar y bloquean la inversión pública en infraestructura.
3. **Trampa de la política pública (*Policy Trap*)**: La distorsión estadística del peso asignado a las villas y su no elegibilidad para proyectos urbanos formales perpetúan la exclusión.
4. **Trampas sociales de pobreza (Durlauf y Shaorshadze, 2015)**: Factores institucionales (menor calidad educativa y acceso a bienes públicos), geográficos (movilidad e infraestructura) y de entorno. De este modo, la informalidad del hábitat no es sólo el *efecto*, sino también la *causa* que reproduce la pobreza (**Smolka, 2003; Del Castillo, 2011**).
            """)

        st.markdown("---")
        col_t1, col_t2 = st.columns([1.2, 1])

        with col_t1:
            st.markdown("**Tabla 1.1. Definiciones conceptuales y operativas del RENABAP para barrios populares**")
            df_renabap_def = pd.DataFrame([
                {
                    "Tipo de definición": "Conceptual",
                    "Definición": (
                        "Aquellos barrios comúnmente denominados villas, asentamientos y urbanizaciones informales, "
                        "que se constituyeron mediante diversas estrategias de ocupación del suelo, que presentan "
                        "diferentes grados de precariedad y hacinamiento, un déficit en el acceso formal a los "
                        "servicios básicos y una situación dominial irregular en la tenencia del suelo."
                    ),
                },
                {
                    "Tipo de definición": "Operativa",
                    "Definición": (
                        "Un conjunto de un mínimo de ocho familias agrupadas o contiguas, en donde más de la mitad "
                        "de la población no cuenta con título de propiedad del suelo, ni acceso formal a al menos "
                        "dos de los servicios básicos: agua corriente, energía eléctrica con medidor domiciliario "
                        "y/o sistema de eliminación de excretas a través de la red cloacal formal."
                    ),
                },
            ])
            st.dataframe(df_renabap_def, width="stretch", hide_index=True)
            st.caption("Fuente: RENABAP (2022).")

        with col_t2:
            st.markdown("**Tabla 1.2. Evolución de la población en villas, asentamientos y NHT en CABA (1962–2022)**")
            df_hist_villas = pd.DataFrame([
                {"Año": "1962", "Población en villas": "42.462", "% sobre total CABA": "1,4%"},
                {"Año": "1976", "Población en villas": "213.823", "% sobre total CABA": "7,4%"},
                {"Año": "1980", "Población en villas": "37.010", "% sobre total CABA": "1,3%"},
                {"Año": "1991", "Población en villas": "52.608", "% sobre total CABA": "1,8%"},
                {"Año": "2001", "Población en villas": "107.422", "% sobre total CABA": "3,9%"},
                {"Año": "2010", "Población en villas": "170.054", "% sobre total CABA": "5,9%"},
                {"Año": "2022", "Población en villas": "324.000", "% sobre total CABA": "10,4%"},
            ])
            st.dataframe(df_hist_villas, width="stretch", hide_index=True)
            st.caption(
                "Fuente: Elaboración propia en la tesis a partir de DGEyC, INDEC (2013) y RENABAP (2022). "
                "Nota: Macció y Lépore (2012) advierten el consenso sobre el subregistro oficial en estos territorios."
            )
