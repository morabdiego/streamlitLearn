"""Configuración, parámetros metodológicos y estructura de dimensiones del IPM."""
from pathlib import Path

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

# Mapeos de dominio muestral y presencia de menores de 18 años (NNyA)
MAP_DOMINIO = {
    3: "Villas y barrios populares",
    4: "Resto de la ciudad",
}

DOMINIO_LABELS_MUESTRA = {
    3: "Villas, asentamientos y NHT",
    4: "Resto de la ciudad",
}

MAP_TIPO_HOGAR = {
    "Hogares con NNyA": 1,
    "Hogares sin NNyA": 0,
}

# =============================================================================
# DISEÑO DE REGISTRO EAH 2025: VARIABLES DE FILTRO Y CRUCE DEL MONITOR
# =============================================================================
MAP_COMUNA: dict[int, str] = {i: f"Comuna {i}" for i in range(1, 16)}

MAP_H2: dict[int, str] = {
    0: "Sin dato",
    1: "Propietario de la vivienda y el terreno",
    2: "Inquilino o arrendatario",
    3: "Otro (prop. solo vivienda, ocupante por préstamo/trabajo/de hecho)",
    9: "Ns/Nc",
}

MAP_HACINAM_2: dict[int, str] = {
    0: "Sin habitaciones de uso exclusivo",
    1: "Sin hacinamiento (menos de 2 personas por cuarto)",
    2: "Con hacinamiento no crítico (2 a 3 personas por cuarto)",
    3: "Con hacinamiento crítico (más de 3 personas por cuarto)",
    9: "Ns/Nc habitaciones de uso exclusivo",
}

MAP_TIPOHO_3: dict[int, str] = {
    1: "Unipersonal",
    2: "Multipersonal no familiar",
    3: "Nuclear con núcleo completo",
    4: "Nuclear con núcleo incompleto",
    5: "Extendido o compuesto con núcleo completo",
    6: "Extendido o compuesto con núcleo incompleto",
    7: "Multipersonal familiar",
}

MAP_I_POBREZA: dict[int, str] = {
    1: "En situación de indigencia",
    2: "En situación de pobreza no indigente",
    3: "No pobres",
}

MAP_HOG_PER_0A17: dict[int, str] = {
    1: "Hogares con personas de 17 años o menos",
    2: "Hogares sin personas de 17 años o menos",
}

MAP_SEXO_JEFE: dict[int, str] = {
    1: "Varón",
    2: "Mujer",
}

MAP_ESTADO_JEFE: dict[int, str] = {
    1: "Ocupado",
    2: "Desocupado",
    3: "Inactivo",
}

MAP_DH2_JEFE: dict[int, str] = {
    1: "Varón",
    2: "Mujer",
    3: "Varón trans (trans de mujer a varón)",
    4: "Mujer trans (trans de varón a mujer)",
    5: "Travesti",
    6: "Otro",
    7: "No sabe / no contesta",
}

MAP_DH3_JEFE: dict[int, str] = {
    0: "No corresponde",
    1: "Lesbiana",
    2: "Gay",
    3: "Bisexual",
    4: "Heterosexual",
    5: "Otra orientación sexual",
    6: "No sabe / no contesta",
}

UNIDADES_ANALISIS: dict[str, str] = {
    "Hogares": "hogares",
    "Personas": "personas",
}

MONITOR_FILTER_CONFIG: dict[str, dict] = {
    "dominio": {
        "label": "Dominio muestral (dominio)",
        "short_label": "Dominio muestral",
        "values": MAP_DOMINIO,
    },
    "comuna": {
        "label": "Comuna (comuna)",
        "short_label": "Comuna",
        "values": MAP_COMUNA,
    },
    "h2": {
        "label": "Régimen de tenencia de la vivienda (h2)",
        "short_label": "Régimen de tenencia",
        "values": MAP_H2,
    },
    "hacinam_2": {
        "label": "Condición de hacinamiento (hacinam_2)",
        "short_label": "Condición de hacinamiento",
        "values": MAP_HACINAM_2,
    },
    "tipoho_3": {
        "label": "Tipo de hogar (tipoho_3)",
        "short_label": "Tipo de hogar",
        "values": MAP_TIPOHO_3,
    },
    "i_pobreza": {
        "label": "Situación de pobreza por ingresos (i_pobreza)",
        "short_label": "Situación de pobreza por ingresos",
        "values": MAP_I_POBREZA,
    },
    "hog_per_0a17": {
        "label": "Hogares con personas de 17 años o menos (hog_per_0a17)",
        "short_label": "Presencia de menores (0 a 17)",
        "values": MAP_HOG_PER_0A17,
    },
    "sexo": {
        "label": "Sexo del jefe/a de hogar - respondiente (sexo)",
        "short_label": "Sexo del jefe/a",
        "values": MAP_SEXO_JEFE,
    },
    "estado": {
        "label": "Condición de ocupación del jefe/a de hogar (estado)",
        "short_label": "Condición de ocupación del jefe/a",
        "values": MAP_ESTADO_JEFE,
    },
    "dh2": {
        "label": "Identidad de género del jefe/a de hogar (dh2)",
        "short_label": "Identidad de género del jefe/a",
        "values": MAP_DH2_JEFE,
    },
    "dh3": {
        "label": "Orientación sexual del jefe/a de hogar (dh3)",
        "short_label": "Orientación sexual del jefe/a",
        "values": MAP_DH3_JEFE,
    },
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
MODOS_MATRIZ_INDICADORES = {
    "Matriz no censurada (% sobre total de hogares)": "no_censurada",
    "Matriz censurada (% sobre total de hogares)": "censurada",
    "Entre hogares pobres (% sobre total de hogares pobres)": "entre_pobres",
}
