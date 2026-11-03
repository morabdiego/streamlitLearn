"""Componente de encabezado, contextualización teórica e histórica de la tesis."""
import pandas as pd
import streamlit as st


def render_header(anio: int) -> None:
    """Renderiza el título principal, autoría y el marco teórico-histórico del estudio."""
    st.title("Pobreza multidimensional y segregación territorial. Análisis de la EAH 2025")
    st.markdown(
        "*Autor: **Mora Benitez, Diego J.** "
    )

    with st.expander(
        "Pobreza estructural en las villas de la Ciudad de Buenos Aires",
        expanded=False,
    ):
        col_teo2 = st.markdown("""
##### Villas, segregación urbana y trampas de pobreza
Las definiciones convencionales suelen omitir la escala, naturaleza y localización espacial de la pobreza, subestimándola en asentamientos informales (**Mitlin y Satterthwaite, 2013**). En la CABA, las villas constituyen verdaderos **"enclaves urbanos de la pobreza"** (**Ziccardi, 1977**) marcados por la segregación residencial (**Sabatini et al., 2001**), la ocupación de tierras públicas, trama urbana irregular, alta densidad y verticalización (**UN-Habitat, 2002, 2003, 2020; Fernandes, 2011; Massidda, 2018; Suárez y Lépore, 2014**).

La permanencia intergeneracional en estos territorios configura lo que las ciencias sociales denominan **pobreza persistente o estructural** (**Rofman, 2015**) y la literatura económica modela como **trampas de pobreza**:
1. **Trampa de capital humano y salud (Marx, Stoker y Suri, 2013)**: La alimentación inadecuada, el déficit de agua y saneamiento y el hacinamiento deterioran tempranamente la salud infantil y condicionan los ingresos futuros.
2. **Trampa de baja acumulación de capital físico (Marx, Stoker y Suri, 2013)**: La inseguridad en la tenencia del suelo y el riesgo de desalojo desincentivan la inversión familiar y bloquean la inversión pública en infraestructura.
3. **Trampa de la política pública (*Policy Trap*)**: La distorsión estadística del peso asignado a las villas y su no elegibilidad para proyectos urbanos formales perpetúan la exclusión.
4. **Trampas sociales de pobreza (Durlauf y Shaorshadze, 2015)**: Factores institucionales (menor calidad educativa y acceso a bienes públicos), geográficos (movilidad e infraestructura) y de entorno. De este modo, la informalidad del hábitat no es sólo el *efecto*, sino también la *causa* que reproduce la pobreza (**Smolka, 2003; Del Castillo, 2011**).
            """)

        st.markdown("---")
        st.markdown("**Tabla 1. Evolución de la población en villas, asentamientos y NHT en CABA (1962–2022)**")
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
