"""Configuración, parámetros metodológicos y estructura de dimensiones del IPM."""
from pathlib import Path
from typing import Literal

IndicatorRateMode = Literal["no_censurada", "censurada", "entre_pobres"]
AnalysisUnit = Literal["hogares", "personas"]

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "eah"

# Parámetros metodológicos por defecto (IDECBA / Alkire-Foster)
DEFAULT_YEAR = 2025
AVAILABLE_YEARS: list[int] = [2025, 2021]
DEFAULT_K_INTRA = 0.33  # Al menos 33% de indicadores privados dentro de la dimensión
DEFAULT_K_INTER = 0.40  # Al menos 2 de 5 dimensiones privadas (40%)
EPS = 1e-9

# Códigos de "No sabe / No contesta" en variables del módulo PM
CODIGOS_NS_NC = [9]

# Mapeos de dominio muestral
MAP_DOMINIO: dict[int, str] = {
    3: "Villas y barrios populares",
    4: "Resto de la ciudad",
}

DOMINIO_LABELS_MUESTRA: dict[int, str] = {
    3: "Villas, asentamientos y NHT",
    4: "Resto de la ciudad",
}

# Estructura oficial EAH 2025: 5 dimensiones (27 indicadores con NNyA / 17 indicadores sin NNyA)
DIMENSIONES_IPM = {
    "dimension_1": {
        "label": "1. Alimentación",
        "con_nnya": {
            "hpm1": "Saltearse comidas",
            "hpm2": "Comer menos variado",
            "hpm3": "Reducir porciones",
        },
        "sin_nnya": {
            "hpm1": "Saltearse comidas",
            "hpm2": "Comer menos variado",
            "hpm3": "Reducir porciones",
        },
    },
    "dimension_2": {
        "label": "2. Salud y cuidados",
        "con_nnya": {
            "pm54": "Atención médica",
            "pm57": "Acceso de remedios recetados",
            "pm60": "Realización de estudios médicos",
            "pm63": "Tratamientos dentales",
            "pm66": "Acceso a anticonceptivos",
            "pm69": "Controles médicos a menores",
            "pm51": "Asistencia para cuidados",
        },
        "sin_nnya": {
            "pm54": "Atención médica",
            "pm57": "Acceso de remedios recetados",
            "pm60": "Realización de estudios médicos",
            "pm63": "Tratamientos dentales",
        },
    },
    "dimension_3": {
        "label": "3. Vivienda y servicios",
        "con_nnya": {
            "pm9": "Reparar goteras",
            "pm15": "Acceso a agua caliente",
            "pm21": "Tener electricidad con medidor formal",
            "pm24": "Conexión a internet",
            "pm27": "Ambientes separados para dormir",
            "pm30": "Camas para cada NNyA",
            "pm33": "Lugar adecuado para hacer los deberes",
        },
        "sin_nnya": {
            "pm9": "Reparar goteras",
            "pm15": "Acceso a agua caliente",
            "pm24": "Conexión a internet",
        },
    },
    "dimension_4": {
        "label": "4. Equipamiento del hogar",
        "con_nnya": {
            "pm36": "Tener heladera",
            "pm39": "Tener frazadas suficientes",
            "pm42": "Tener ropa adecuada",
            "pm45": "Reemplazar calzado y ropa",
        },
        "sin_nnya": {
            "pm39": "Tener frazadas suficientes",
            "pm42": "Tener ropa adecuada",
            "pm45": "Reemplazar calzado y ropa",
        },
    },
    "dimension_5": {
        "label": "5. Privación social y educación",
        "con_nnya": {
            "pm48": "Utilizar transporte público",
            "pm78": "Útiles escolares requeridos",
            "pm81": "Dispositivo electrónico para estudiar",
            "pm84": "Gastos personales semanales",
            "pm87": "Irse de vacaciones al menos una semana",
            "pm90": "Invitar familiares o amigos a comer",
        },
        "sin_nnya": {
            "pm48": "Utilizar transporte público",
            "pm84": "Gastos personales semanales",
            "pm87": "Irse de vacaciones al menos una semana",
            "pm90": "Invitar familiares o amigos a comer",
        },
    },
}

# Estructura oficial EAH 2021: 5 dimensiones (27 indicadores con NNyA / 16 indicadores sin NNyA)
# Según Tabla T.4 (IDECBA), en 2021 la Dimensión 3 para hogares sin menores de 18 años
# incluye únicamente 2 indicadores (Reparar goteras y Conexión a internet, sin Agua caliente).
DIMENSIONES_IPM_2025 = DIMENSIONES_IPM

DIMENSIONES_IPM_2021 = {
    **DIMENSIONES_IPM_2025,
    "dimension_3": {
        "label": "3. Vivienda y servicios",
        "con_nnya": DIMENSIONES_IPM_2025["dimension_3"]["con_nnya"],
        "sin_nnya": {
            "pm9": "Reparar goteras",
            "pm24": "Conexión a internet",
        },
    },
}

DIMENSIONES_IPM_POR_ANIO: dict[int, dict] = {
    2021: DIMENSIONES_IPM_2021,
    2025: DIMENSIONES_IPM_2025,
}


def get_dimensiones_ipm(year: int = DEFAULT_YEAR) -> dict:
    """Devuelve la estructura oficial de dimensiones e indicadores del IPM según el año de la EAH."""
    return DIMENSIONES_IPM_POR_ANIO.get(int(year), DIMENSIONES_IPM_2025)


# Modos disponibles para el cálculo de tasas por indicador (Tablas 11 y 12)
MODOS_MATRIZ_INDICADORES: dict[str, IndicatorRateMode] = {
    "Matriz no censurada (% sobre total de hogares)": "no_censurada",
    "Matriz censurada (% sobre total de hogares)": "censurada",
    "Entre hogares pobres (% sobre total de hogares pobres)": "entre_pobres",
}
