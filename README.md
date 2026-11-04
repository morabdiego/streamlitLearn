# Pobreza Multidimensional y Segregación Urbana en la CABA

Plataforma interactiva en **Streamlit** para el cálculo, discusión metodológica y visualización de la pobreza multidimensional en la Ciudad Autónoma de Buenos Aires, basada en la investigación de grado de **Diego J. Mora Benitez** (*"Pobreza multidimensional en las villas de la Ciudad Autónoma de Buenos Aires en el año 2021"*, Facultad de Ciencias Económicas, UBA).

---

## 🎯 Enfoque Teórico y Storytelling

El tablero no es un simple visor de datos numéricos, sino una herramienta de discusión metodológica y de políticas públicas que integra:

1. **La Brecha Territorial (Villas vs. Resto de la Ciudad)**: Visibiliza cómo el promedio de la CABA oculta que en villas la pobreza multidimensional y por ingresos multiplica por 4 a 5 veces la de la ciudad formal.
2. **Acumulación de Desventajas y Doble Pobreza**: Cruce entre pobreza monetaria y multidimensional (pobreza crónica) según Gordon (2006) y Clemente (2013).
3. **El Debate Metodológico**: Comparación crítica entre el **Método Consensual** (Townsend / Gordon / DGEyC) y la **Metodología Alkire-Foster** (Sen / OPHI), analizando la propiedad de *monotonicidad dimensional* y la intensidad ($A$).
4. **Discusión Crítica de Indicadores**:
   - *Alimentación*: Más del 60% en villas con privación alimentaria (daño biológico y trampas de pobreza de capital humano).
   - *Privación Social y Educación*: Por qué está inflada por proxies de ingreso (vacaciones) y la ausencia de indicadores de deserción y calidad educativa.
   - *Vivienda y Servicios*: La omisión de los indicadores estructurales del RENABAP (red cloacal formal, agua potable formal y regularización dominial).
5. **Corrección de Sesgo Muestral**: Advertencia sobre la subestimación en la EAH (~4% muestral vs. >10% real de población en barrios populares).

---

## 🏗️ Estructura del Proyecto

```text
streamlitLearn/
├── eah/                           # Microdatos oficiales de la EAH (IDECBA)
├── src/
│   ├── config.py                  # Parámetros metodológicos, rutas, dimensiones y mapeos
│   ├── texts.py                   # Textos, títulos, notas, cuadros estáticos y bibliografía
│   ├── logic.py                   # Carga de datos, cálculos Alkire-Foster y armado de tablas
│   └── components.py              # Componentes visuales de Streamlit (encabezado, KPIs y pestañas)
├── tests/
│   └── test_logic.py              # Pruebas unitarias de cálculos, matrices y benchmarks EAH 2025
├── main.py                        # Punto de entrada principal
└── pyproject.toml
```

---

## 🚀 Cómo ejecutar la aplicación

```bash
uv run streamlit run main.py
```

La aplicación no muestra la barra lateral: usa por defecto el año y los cortes metodológicos configurados, e incluye todos los dominios y tipos de hogar.

Para correr las pruebas unitarias:

```bash
uv run python -m unittest discover tests
```
