"""Configuración de variables de filtro, etiquetas del diseño de registro y grilla del Monitor Interactivo."""
from src.config import AnalysisUnit, MAP_DOMINIO

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

UNIDADES_ANALISIS: dict[str, AnalysisUnit] = {
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

FILTER_LAYOUT: list[tuple[str, list[list[str]]]] = [
    (
        "🏠 Variables de vivienda y hogar",
        [
            ["dominio", "comuna", "hog_per_0a17"],
            ["h2", "hacinam_2"],
            ["tipoho_3", "i_pobreza"],
        ],
    ),
    (
        "👤 Características del jefe/a de hogar (respondiente)",
        [
            ["sexo", "estado"],
            ["dh2", "dh3"],
        ],
    ),
]
