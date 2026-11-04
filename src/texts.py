"""Textos editoriales, títulos, cuadros estáticos y bibliografía de la aplicación."""

PAGE_TITLE = "Pobreza Multidimensional en CABA"
PAGE_ICON = "🏙️"
LOADING_SPINNER = "Procesando microdatos y calculando cortes..."

SOURCE_CAPTION = (
    "Fuente: Elaboración propia en base a IDECBA (2026), "
    "Encuesta Anual de Hogares (EAH) 2025. Base de usuarios."
)

# =============================================================================
# ENCABEZADO E INTRODUCCIÓN
# =============================================================================
HEADER_TITLE = "Pobreza multidimensional y segregación territorial. Análisis de la EAH 2025"
HEADER_AUTHOR = "*Autor: **Mora Benitez, Diego J.** "
HEADER_EXPANDER_TITLE = "Pobreza estructural en las villas de la Ciudad de Buenos Aires"

HEADER_THEORY_MD = """
##### Villas, segregación urbana y trampas de pobreza
Las definiciones convencionales suelen omitir la escala, naturaleza y localización espacial de la pobreza, subestimándola en asentamientos informales (**Mitlin y Satterthwaite, 2013**). En la CABA, las villas constituyen verdaderos **"enclaves urbanos de la pobreza"** (**Ziccardi, 1977**) marcados por la segregación residencial (**Sabatini et al., 2001**), la ocupación de tierras públicas, trama urbana irregular, alta densidad y verticalización (**UN-Habitat, 2002, 2003, 2020; Fernandes, 2011; Massidda, 2018; Suárez y Lépore, 2014**).

La permanencia intergeneracional en estos territorios configura lo que las ciencias sociales denominan **pobreza persistente o estructural** (**Rofman, 2015**) y la literatura económica modela como **trampas de pobreza**:
1. **Trampa de capital humano y salud (Marx, Stoker y Suri, 2013)**: La alimentación inadecuada, el déficit de agua y saneamiento y el hacinamiento deterioran tempranamente la salud infantil y condicionan los ingresos futuros.
2. **Trampa de baja acumulación de capital físico (Marx, Stoker y Suri, 2013)**: La inseguridad en la tenencia del suelo y el riesgo de desalojo desincentivan la inversión familiar y bloquean la inversión pública en infraestructura.
3. **Trampa de la política pública (*Policy Trap*)**: La distorsión estadística del peso asignado a las villas y su no elegibilidad para proyectos urbanos formales perpetúan la exclusión.
4. **Trampas sociales de pobreza (Durlauf y Shaorshadze, 2015)**: Factores institucionales (menor calidad educativa y acceso a bienes públicos), geográficos (movilidad e infraestructura) y de entorno. De este modo, la informalidad del hábitat no es sólo el *efecto*, sino también la *causa* que reproduce la pobreza (**Smolka, 2003; Del Castillo, 2011**).
"""

TABLA_1_TITULO = "**Tabla 1. Evolución de la población en villas, asentamientos y NHT en CABA (1962–2022)**"
TABLA_1_HISTORICO_VILLAS = [
    {"Año": "1962", "Población en villas": "42.462", "% sobre total CABA": "1,4%"},
    {"Año": "1976", "Población en villas": "213.823", "% sobre total CABA": "7,4%"},
    {"Año": "1980", "Población en villas": "37.010", "% sobre total CABA": "1,3%"},
    {"Año": "1991", "Población en villas": "52.608", "% sobre total CABA": "1,8%"},
    {"Año": "2001", "Población en villas": "107.422", "% sobre total CABA": "3,9%"},
    {"Año": "2010", "Población en villas": "170.054", "% sobre total CABA": "5,9%"},
    {"Año": "2022", "Población en villas": "324.000", "% sobre total CABA": "10,4%"},
]
TABLA_1_CAPTION = (
    "Fuente: Elaboración propia en la tesis a partir de DGEyC, INDEC (2013) y RENABAP (2022). "
    "Nota: Macció y Lépore (2012) advierten el consenso sobre el subregistro oficial en estos territorios."
)

# =============================================================================
# TARJETAS DE MÉTRICAS PRINCIPALES (KPIs)
# =============================================================================
KPI_H_LABEL = "Incidencia (H)"
KPI_H_HELP = "Porcentaje de hogares pobres multidimensionales"

KPI_A_LABEL = "Intensidad (A)"
KPI_A_HELP = "Promedio de privaciones entre los hogares identificados como pobres"

KPI_M0_LABEL = "IPM (M0)"
KPI_M0_HELP = "Tasa M0 ajustada por intensidad (H × A)"

KPI_POBRES_LABEL = "Total de hogares pobres multidimensionales"

# =============================================================================
# PESTAÑAS DE NAVEGACIÓN
# =============================================================================
TAB_LABELS = [
    "1. Pobreza estructural",
    "2. ¿Cómo se calcula?",
    "3. ¿Qué no estamos viendo?",
    "4. Indicadores",
    "5. Conclusiones",
]

# =============================================================================
# PESTAÑA 1: POBREZA ESTRUCTURAL Y BRECHA TERRITORIAL
# =============================================================================
TAB1_SUBHEADER = "Pobreza multidimensional: Análisis por dominio geográfico de la muestra"
TAB1_INTRO_MD = """
> **La falacia del promedio urbano y la segregación residencial**: La CABA se caracteriza por poseer indicadores promedio de calidad de vida, salud, educación e ingresos altos respecto al resto del país (**INDEC, 2023a, 2023b**). Sin embargo, detrás del promedio general se oculta una profunda fractura socioespacial concentrada en las comunas del sur (**Sabatini et al., 2001**), donde una décima parte de la población habita en villas y asentamientos populares conviviendo con una acumulación sistemática de desventajas.
"""

TAB1_SEC1_TITULO = "##### 1. Brecha de representación de las villas"
TAB1_SEC1_MD = """
A partir de 2019 la Encuesta Anual de Hogares (EAH) incorpora el módulo ampliado de pobreza multidimensional sobre dos marcos muestrales: **Marco 4 ("Viviendas particulares generales" / Resto de la ciudad)** y **Marco 3 ("Villas, asentamientos y NHT")**.

Al observar los factores de expansión muestral (`fexp`), el marco en villas obtiene una representación cercana al **3,8% – 4,0% de los hogares**, mientras que los relevamientos del **RENABAP (2022)** indican que al menos el **10,4% de la población porteña** reside en los 50 barrios populares de la Ciudad. Como advierten **Macció y Lépore (2012)** y **Marx, Stoker y Suri (2013)**, esta distorsión en el peso estadístico asignado a las villas **subestima las tasas globales de pobreza** de toda la CABA.
"""
TABLA_2_TITULO = "**Tabla 2: Distribución de muestra y muestra expandida por dominio muestral**"

TAB1_SEC2_TITULO = "##### 2. Brecha de pobreza multidimensional y por ingresos"
TABLA_3_TITULO = "**Tabla 3: Dominio muestral por condiciones de pobreza**"
TAB1_SEC2_OUTRO_MD = """
En los informes oficiales se publica únicamente la tasa de incidencia ($H = q/n$) global o por zonas geográficas (Norte, Centro y Sur), sin desagregar específicamente el marco muestral de villas ni informar la intensidad de las privaciones. Al reconstruir el cálculo mediante los índices de **Alkire y Foster (2007)** por marco muestral:
* La **Incidencia ($H$)** y la **Pobreza por Ingresos** en las villas cuadruplican y quintuplican los registros del resto de la ciudad.
* La **Intensidad ($A$)** revela que los hogares pobres en villas sufren un porcentaje promedio de privaciones simultáneas significativamente mayor.
* La **Tasa de Recuento Ajustada ($M_0 = H \\times A$)** arroja una brecha de **casi 5 veces** entre ambos territorios.
"""

TAB1_SEC3_TITULO = "##### 3. Pobreza estructural"
TAB1_SEC3_MD = """
**David Gordon (2006)** ilustra la dinámica de la pobreza distinguiendo las trayectorias de ingresos —altamente sensibles al ciclo económico y shocks de empleo— frente a las condiciones materiales de vida, vinculadas a la provisión de bienes públicos, infraestructura y activos del hogar. Cuando ambas carencias se superponen (**pobreza multidimensional + pobreza monetaria**), se consolida un núcleo duro de exclusión donde la informalidad del hábitat opera simultáneamente como efecto y causa reproductora de la pobreza (**Smolka, 2003; Del Castillo, 2011**).
"""
TABLA_4_TITULO = "**Tabla 4: Pobreza estructural por dominio muestral**"

TAB1_SEC4_TITULO = "##### 4. Intensidad de las privaciones - Dimensiones"
TAB1_SEC4_MD = """
Al observar la distribución interna de los hogares identificados como pobres multidimensionales:
* En el **Resto de la ciudad**, más de la mitad de los hogares pobres se concentran exactamente sobre el umbral mínimo de corte ($2$ dimensiones privadas).
* En las **Villas y barrios populares**, cerca de **dos tercios de los hogares pobres acumulan entre 3, 4 y 5 dimensiones privadas simultáneamente**, demostrando que la pobreza en el hábitat informal es mucho más intensa y severa.
"""
TABLA_5_TITULO = "**Tabla 5: Cantidad de privaciones - Hogares pobres multidimensionales**"

# =============================================================================
# PESTAÑA 2: DISCUSIÓN METODOLÓGICA (¿CÓMO SE CALCULA?)
# =============================================================================
TAB2_SUBHEADER = "Métodos para medir pobreza multidimensional"
TAB2_INTRO_MD = """
La **CEPAL (2013)** y los institutos de estadística de la región impulsaron mediciones multidimensionales de bienestar complementarias al ingreso.
Mientras casi toda América Latina adoptó adaptaciones del método de **Alkire y Foster (2007)** de la *Oxford Poverty and Human Development Initiative* (**OPHI**) —con el caso singular de **México (CONEVAL, 2019)**
 que combina ingreso, privación social de Gordon y medidas de Alkire-Foster—. El **Instituto de Estadísticas de CABA** optó a contramano de la región por el **Método Consensual** europeo (**DGEyC, 2021b, 2022**).
"""

TAB2_CONSENSUAL_WARNING_MD = """
#### 5. Pobreza multidimensional en CABA: El método consensual (Gordon, 2006; Mack y Lansley, 1985)
* **Fundamento**: Basada en la concepción de pobreza relativa de **Townsend (1979, 2003)** y **Guio et al. (2017)** en el Reino Unido y la Unión Europea. Busca sustraer la definición de pobreza del juicio arbitrario de expertos para someterla a una representación "democrática" de la sociedad.
* **Etapas de cálculo en CABA (**DGEyC, 2021b**)**:
  1. *Consenso social*: Se consulta qué ítems son necesarios para vivir dignamente en CABA (umbral de acuerdo social) y se contabilizan sólo las carencias ocurridas *por falta de recursos económicos*.
  2. *Filtros estadísticos*: Los ítems se someten cada año a pruebas de **validez** (ANOVA y regresiones logísticas contra ingresos) y **confiabilidad** estadística.
  3. *Identificación*: Mediante doble umbral, primero se identifica si el hogar esta privado en alguna dimensión según sus indicadores aplicables ($z_j$),
  segundo define la suma mínima de privaciones simultáneas para identificar a un hogar como pobre $k$ , $c_i \\ge k$. En este caso se define una dimensión privada con al menos el 33% de sus indicadores, y un umbral de 2 de 5 dimensiones.
  4. *Agregación*: Reporta únicamente la tasa de incidencia ($H = q/n$).
* **Críticas y límites en sociedades desiguales**:
  - Dependencia del cuestionario (**Walker, 1987**), prácticas presupuestarias intrahogar (**Piachaud, 1987**) y preferencias adaptativas (**McKay, 2004**).
  - **El choque con la desigualdad latinoamericana (**Cecchini, 2019; De la Mata y Berniell, 2022; Macció y Mitchell, 2023**)**: En sociedades altamente desiguales y segregadas, presuponer que existe un consenso homogéneo entre la ciudad formal (96% ponderado) y las villas (4% ponderado) **oculta el núcleo irreductible de pobreza (Sen, 1983)** y descarta estadísticamente privaciones graves que sufren las minorías segregadas.
"""

TAB2_AF_INFO_MD = """
#### 6. Una metodología alternativa: El índice de pobreza multidimensional de Alkire-Foster
* **Fundamento**: Basada en el enfoque de capacidades de **Sen (1983, 1999)** y en la idea de núcleo irreductible de pobreza (pobreza absoluta), derechos humanos (**Florio y Labrunée, 2021**) y la familia de medidas FGT (**Foster, Greer y Thorbecke, 1984**). Adoptada oficialmente en Colombia (**DANE, 2023**), Costa Rica (**INEC, 2015**) y República Dominicana (**SIUBEN, 2017**).
* **Identificación**: Mediante dobrel umbral
* **Medidas agregadas y propiedades (**Hernández Téllez y Macció, 2020; Santos, 2019**)**:
  - **Incidencia ($H = q/n$)**: Proporción de hogares pobres.
  - **Intensidad ($A$)**: Promedio de privaciones entre los pobres (matriz censurada, es decir, excluyendo del cálculo a hogares no pobres).
  - **Tasa de recuento ajustada o Índice de Pobreza Multidimensional (IPM) ($M_0 = H \\times A$)**: Satisface **monotonicidad dimensional** (si un hogar pobre sufre una privación adicional, $M_0$ aumenta, mientras que $H$ es insensible) y **descomponibilidad aditiva** por subgrupos y dimensiones.
* **Desafío**: La selección de dimensiones, ponderaciones y umbrales requiere criterios normativos explícitos (**Macció y Mitchell, 2019; Santos, 2019**).
"""

TAB2_SEC7_TITULO = "#### 7. Indicadores y dimensiones de la medición IDECBA 2025"
TABLA_6_TITULO = "**Tabla 6: Dimensiones e indicadores finales. EAH 2025**"

_AMBOS, _SOLO_CON = (True, True), (False, True)
ESTRUCTURA_2025_MATRIZ = {
    "1. Alimentación": {
        "Saltearse comidas": _AMBOS,
        "Comer menos variado": _AMBOS,
        "Reducir porciones": _AMBOS,
    },
    "2. Salud y cuidados": {
        "Atención médica": _AMBOS,
        "Acceso a remedios recetados": _AMBOS,
        "Realización de estudios médicos": _AMBOS,
        "Tratamientos dentales": _AMBOS,
        "Asistencia para cuidados": _SOLO_CON,
        "Acceso a anticonceptivos": _SOLO_CON,
        "Controles médicos a menores": _SOLO_CON,
    },
    "3. Vivienda y servicios": {
        "Reparar goteras": _AMBOS,
        "Acceso a agua caliente": _AMBOS,
        "Tener electricidad": _SOLO_CON,
        "Conexión a internet": _AMBOS,
        "Ambientes separados": _SOLO_CON,
        "Camas para cada niño/a": _SOLO_CON,
        "Lugar para hacer los deberes": _SOLO_CON,
    },
    "4. Equipamiento del hogar": {
        "Tener heladera": _SOLO_CON,
        "Tener frazadas suficientes": _AMBOS,
        "Tener ropa adecuada": _AMBOS,
        "Reemplazar calzado y ropa": _AMBOS,
    },
    "5. Privación social y educación": {
        "Gastos personales": _AMBOS,
        "Irse de vacaciones": _AMBOS,
        "Invitar a la casa a comer": _AMBOS,
        "Utilizar transporte público": _AMBOS,
        "Útiles escolares requeridos": _SOLO_CON,
        "Dispositivo electrónico para estudiar": _SOLO_CON,
    },
}

TAB2_SEC8_TITULO = "#### 8. Análisis de contribución mediante IPM $M_0$"
TAB2_SEC8_MD = """
Gracias a la propiedad de descomponibilidad de **Alkire y Foster (2007)** sobre la matriz censurada, podemos descomponer qué peso relativo tiene cada dimensión en la conformación de la pobreza multidimensional ($M_0$) de cada territorio.
Las pobreza multidimensional en villas se explica en mayor medida que en el resto de la ciudad por las dimensiones 2, 3 y 5. La presencia de comedores comunitarios alivian el 1.
"""
TABLA_7_TITULO = "**Tabla 7: Contribución por dimensión según dominio muestral**"

# =============================================================================
# PESTAÑA 3: DISCUSIÓN DE INDICADORES (¿QUÉ NO ESTAMOS VIENDO?)
# =============================================================================
TAB3_SUBHEADER = "¿Que indicadores se estan considerando y cuáles faltan?"
TAB3_INTRO_MD = """
En el diseño oficial de la CABA se utilizan **5 dimensiones**: *(1) Alimentación, (2) Salud y cuidados, (3) Vivienda y servicios, (4) Equipamiento del hogar y (5) Privación social y educación*. Sin embargo, al someter cada indicador anualmente a consenso y pruebas estadísticas de validez y confiabilidad por subgrupo, quedaron **17 indicadores para hogares sin menores de 18 años** y **27 indicadores para hogares con menores de 18 años** (Tabla 3.2 de la tesis).

Este procedimiento estadístico genera **tres grandes problemas metodológicos y de diagnóstico** cuando se analiza la realidad de las villas:
"""

TAB3_SEC9_TITULO = "#### 9. Indicadores relevados en el módulo de PM pero excluidos por filtros estadísticos"
TAB3_SEC9_MD = """
En la propia base de datos del módulo de Pobreza Multidimensional de la EAH existen preguntas que fueron relevadas en campo, pero **fueron descartadas total o parcialmente del cálculo del índice** por no superar las pruebas estadísticas de validez/confiabilidad en el promedio de la ciudad:
* **La exclusión de la conexión eléctrica formal (`pm21`) en hogares sin NNyA**: En el *Resto de la ciudad*, sólo el **0,1%** de los hogares sin menores carece de medidor eléctrico formal, por lo que el test estadístico global descarta la variable para ese grupo. ¡Pero en las **Villas**, el **47,0%** de los hogares sin menores sufre esta carencia (y el **69,8%** en hogares con menores)! Al excluirla, un hogar adulto en una villa sin medidor eléctrico no suma privación en *Vivienda y servicios*.
* **La exclusión de los indicadores de asistencia escolar (`pm72` Jardín 3-5 años y `pm75` Secundaria 15-17 años)**: Ambos se relevan en la EAH, pero como preguntan únicamente si la inasistencia escolar ocurre *"por falta de recursos económicos"*, la tasa declarada es menor al 0,8% y quedan fuera del índice. Como resultado, la dimensión llamada **"Privación social y educación"** no mide educación ni escolaridad alguna: sólo mide tener útiles (`pm78`) o computadora (`pm81`), y queda dominada por **vacaciones (`pm87`)** y **gastos personales (`pm84`)**, que son simples proxies de ingreso monetario.
* **La exclusión de la asistencia a comedores comunitarios (`hpm4`)**: Aunque más de **1 de cada 4 hogares en villas (26,8%)** recurre a comedores o merenderos comunitarios para alimentarse (frente a sólo 2,2% en el resto de la ciudad), este indicador no se computa en la dimensión *Alimentación*.
"""
TABLA_8_TITULO = "**Tabla 8: Indicadores descartados**"

INDICADORES_EXCLUIDOS_MODULO_PM = [
    {
        "variable": "pm21",
        "etiqueta": "Sin luz por conexión formal con medidor",
        "dimension": "3. Vivienda y servicios",
        "universo_excluido": "Hogares sin NNyA",
        "motivo_exclusion": (
            "En el Resto de la ciudad casi ningún hogar sin menores carece de medidor eléctrico (0,1%), "
            "por lo que no supera los filtros estadísticos globales para ese subgrupo. Sin embargo, en las Villas "
            "afecta al 47,0% de los hogares sin menores."
        ),
    },
    {
        "variable": "pm51",
        "etiqueta": "Sin asistencia/apoyo para tareas de cuidado",
        "dimension": "2. Salud y cuidados",
        "universo_excluido": "Hogares sin NNyA",
        "motivo_exclusion": (
            "Se excluye en hogares sin menores de 18 años, invisibilizando la carga de cuidado de adultos mayores "
            "o personas con discapacidad en hogares adultos de villas (12,1% vs. 2,3% en el resto)."
        ),
    },
    {
        "variable": "pm36",
        "etiqueta": "No disponer de heladera por falta de recursos",
        "dimension": "4. Equipamiento del hogar",
        "universo_excluido": "Hogares sin NNyA",
        "motivo_exclusion": (
            "Excluido en hogares sin menores por baja incidencia promedio en la ciudad formal (0,6%), "
            "pero presente en el 5,1% de los hogares sin menores en villas."
        ),
    },
    {
        "variable": "pm66",
        "etiqueta": "Sin acceso a métodos anticonceptivos",
        "dimension": "2. Salud y cuidados",
        "universo_excluido": "Hogares sin NNyA",
        "motivo_exclusion": (
            "Excluido del subgrupo de hogares sin menores, pese a registrar una brecha de 20 veces "
            "entre villas (3,9%) y el resto de la ciudad (0,2%)."
        ),
    },
    {
        "variable": "pm72",
        "etiqueta": "Inasistencia al jardín de infantes (3 a 5 años) por falta de recursos",
        "dimension": "5. Privación social y educación",
        "universo_excluido": "Hogares con NNyA",
        "motivo_exclusion": (
            "Descartado en las pruebas de validez y confiabilidad estadística: al restringir la pregunta "
            "exclusivamente a la 'falta de dinero', la tasa declarada es casi nula (<0,5%), dejando fuera "
            "las barreras de vacantes e infraestructura escolar."
        ),
    },
    {
        "variable": "pm75",
        "etiqueta": "Inasistencia a escuela secundaria (15 a 17 años) por falta de recursos",
        "dimension": "5. Privación social y educación",
        "universo_excluido": "Hogares con NNyA",
        "motivo_exclusion": (
            "Descartado por los tests estadísticos del método consensual. Su exclusión deja a la dimensión "
            "'Educación' sin indicadores de asistencia o terminalidad escolar, midiendo únicamente tenencia "
            "de útiles y computadora."
        ),
    },
    {
        "variable": "hpm4",
        "etiqueta": "Asistencia a comedores o merenderos comunitarios en el último mes",
        "dimension": "1. Alimentación",
        "universo_excluido": "Todos los hogares",
        "motivo_exclusion": (
            "Relevado en el bloque alimentario pero no integrado al score dimensional. En las villas el 26,8% "
            "de los hogares asiste a comedores comunitarios (vs. 2,2% en el resto), estrategia colectiva que "
            "amortigua el hambre extrema."
        ),
    },
]

TAB3_SEC10_TITULO = "### 10. El gran ausente: hábitat, saneamiento básico, hacinamiento y régimen de tenencia"
TAB3_SEC10_MD = """
Como advierten **Macció y Mitchell (2023)**, la segregación residencial oculta las Necesidades Básicas Insatisfechas (NBI) bajo un enfoque relativo diseñado para las clases medias urbanas. La definición operativa del **RENABAP (2022)** identifica a un barrio popular por tres carencias estructurales: **irregularidad en la tenencia del suelo, falta de red cloacal formal y falta de agua corriente o energía eléctrica con medidor**.

Al cruzar los microdatos generales de vivienda de la propia EAH 2025, comprobamos que estas privaciones estructurales —que **no forman parte del IPM oficial**— exhiben brechas extremas en las villas y constituyen la base material de las *trampas de pobreza* (**Marx, Stoker y Suri, 2013; Rofman, 2015**):
"""
TABLA_9_TITULO = "**Tabla 9: Variables de la EAH que no fueron utilizadas para construir la medición de pobreza multidimensional**"
TABLA_9_NOTA_CLOACA = (
    "(*) Nota: Existe un conflicto en la contabilización esta variable al existir cloacas vecinales "
    "en las villas, en donde generalmente los hogares no identifican que tipo de desagüe poseen al preexistir cloacas informales."
)

# =============================================================================
# PESTAÑA 4: DETALLE DE INDICADORES
# =============================================================================
TAB4_SUBHEADER = "Detalle de indicadores"
TAB4_SEC11_TITULO = "#### 11. Menores a cargo dentro del hogar"
TAB4_SEC11_MD = """
Los hogares con presencia de menores de 18 años enfrentan mayores exigencias de cuidado, espacio habitacional, equipamiento educativo y nutrición, registrando una incidencia de pobreza multidimensional significativamente más elevada que los hogares sin menores.
"""
TABLA_10_TITULO = "**Tabla 10: Pobreza multidimensional según presencia de NNyA**"

TAB4_SEC12_TITULO = "### 12. Tasas de privación por indicador según dominio muestral"
TAB4_RADIO_LABEL = "Modo de cálculo de las tasas por indicador:"
TABLA_11_TITULO = "Tabla 11: 27 indicadores para hogares con menores de 18 años"
TABLA_12_TITULO = "Tabla 12: 17 indicadores para hogares sin menores de 18 años"

# =============================================================================
# PESTAÑA 5: CONCLUSIONES, ANEXO RENABAP Y BIBLIOGRAFÍA
# =============================================================================
TAB5_SUBHEADER = "Conclusiones, anexos y bibliografía consultada"
TAB5_CONCLUSIONES_MD = """
##### 13. ¿Por qué la ciudad no difunde estos resultados y como podriamos mejorar la medición?

La iniciativa de elaborar estadísticas oficiales sobre pobreza multidimensional en la CABA constituye un avance valioso frente a la ausencia de un IPM oficial a nivel nacional en la Argentina.
Pese al gran avance, no hay registros de que estas medidas sean utilizadas para objetivos de política pública, y tampoco hay difusión del desagregado entre villas y resto de la ciudad de las estadísticas oficiales, por más que existan los microdatos, no es de acceso masivo.
Finalmente, al incorporar la dimensión territorial e indagar en las brechas entre las villas y la ciudad "formal", emergen **cuatro conclusiones centrales**:

1. **Subestimación poblacional y estadística**:
   La subrepresentación del marco muestral de villas en la EAH (~3,8%–4,0% expandido frente a más del 10,4% real relevado por el RENABAP) conlleva una subestimación sistemática de los niveles globales de pobreza por ingresos y multidimensional de la Ciudad de Buenos Aires.
2. **Omisión de indicadores de pobreza estructural y reproducción intergeneracional**:
   El diseño del índice excluye variables estrechamente vinculadas con las *trampas de pobreza* en las villas: el acceso formal al agua potable y saneamiento básico (red cloacal), el hacinamiento crítico, la seguridad en la tenencia del suelo y los indicadores efectivos de asistencia, terminalidad y calidad educativa.
3. **Límites del enfoque consensual relativo en ciudades segregadas**:
   La utilización de enfoques relativos de privación en sociedades con altos niveles de desigualdad —visibles incluso geográficamente— tiende a ocultar la segmentación en la provisión de servicios públicos. Al exigir consenso y varianza estadística sobre el promedio de la ciudad formal, se descartan carencias agudas (como la falta de medidor eléctrico formal en hogares sin niños) que golpean casi exclusivamente a los asentamientos informales.
4. **Mayor incidencia, mayor intensidad y doble pobreza**:
   La pobreza multidimensional en las villas no sólo es cerca de **4,5 veces superior** en incidencia ($H$) a la del resto de la ciudad, sino que es en promedio **más intensa ($A$)** al evaluarse con la metodología de **Alkire y Foster (2007)**, quintuplicando la tasa ajustada ($M_0$) y concentrando un núcleo duro donde cerca de la mitad de los hogares sufre simultáneamente pobreza monetaria y multidimensional.

> **Horizonte de política pública**: En la Argentina existen más de **1,17 millones de familias en 5.687 barrios populares** según el RENABAP. Constituir una medición multidimensional oficial y nacional requiere superar las políticas meramente asistenciales de ingresos —que aunque indispensables para las economías domésticas vulneradas no logran por sí solas perforar el piso estructural— hacia políticas focalizadas de **integración urbana, infraestructura sanitaria, vivienda y educación** que igualen las condiciones básicas de vida y permitan quebrar la persistencia intergeneracional de la pobreza.
"""

ANEXO_1_TITULO = "Anexo 1: Las 50 villas, NHT y asentamientos contabilizados por el RENABAP en la CABA"
ANEXO_1_INTRO_MD = """
La mayor concentración de barrios populares se ubica en las comunas del sur de la CABA (**Comunas 4, 8, 7 y 9**), en estrecha correspondencia con los patrones históricos de segregación residencial.
"""
ANEXO_1_CAPTION = "Fuente: Elaboración propia en base a RENABAP (2022)."

BARRIOS_RENABAP_CABA = [
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

BIBLIOGRAFIA_TITULO = "##### Bibliografía"
BIBLIOGRAFIA_MD = """
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
"""
