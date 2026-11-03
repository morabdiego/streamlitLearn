"""Configuración, constantes y metadatos para el cálculo y análisis del IPM."""
from pathlib import Path

# Rutas base
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "eah"

# Leyenda de fuente oficial requerida para gráficos y cuadros EAH 2025
SOURCE_CAPTION = (
    "Fuente: Elaboración propia en base a IDECBA (2026), "
    "Encuesta Anual de Hogares (EAH) 2025. Base de usuarios."
)

# Dimensiones e Indicadores del IPM (Diseño Oficial Consensual IDECBA / DGEyC)
# Nota metodológica: 27 indicadores para hogares con NNyA y 16 para hogares sin NNyA
DIMENSIONES_INDICADORES_IPM = {
    "dimension_1": {
        "hogares_con_nnya": {
            "hpm1": "Saltearse comidas",
            "hpm2": "Comer menos variado",
            "hpm3": "Reducir porciones",
        },
        "hogares_sin_nnya": {
            "hpm1": "Saltearse comidas",
            "hpm2": "Comer menos variado",
            "hpm3": "Reducir porciones",
        },
        "meta": {"label": "1. Alimentación"},
    },
    "dimension_2": {
        "hogares_con_nnya": {
            "pm54": "Atención médica",
            "pm57": "Acceso de remedios recetados",
            "pm60": "Realización de estudios médicos",
            "pm63": "Tratamientos dentales",
            "pm66": "Acceso a anticonceptivos",
            "pm69": "Controles médicos a menores",
            "pm51": "Asistencia para cuidados",
        },
        "hogares_sin_nnya": {
            "pm54": "Atención médica",
            "pm57": "Acceso de remedios recetados",
            "pm60": "Realización de estudios médicos",
            "pm63": "Tratamientos dentales",
        },
        "meta": {"label": "2. Salud y cuidados"},
    },
    "dimension_3": {
        "hogares_con_nnya": {
            "pm9": "Reparar goteras",
            "pm15": "Acceso a agua caliente",
            "pm21": "Tener electricidad con medidor formal",
            "pm24": "Conexión a internet",
            "pm27": "Ambientes separados para dormir",
            "pm30": "Camas para cada NNyA",
            "pm33": "Lugar adecuado para hacer los deberes",
        },
        "hogares_sin_nnya": {
            "pm9": "Reparar goteras",
            "pm15": "Acceso a agua caliente",
            "pm24": "Conexión a internet",
        },
        "meta": {"label": "3. Vivienda y servicios"},
    },
    "dimension_4": {
        "hogares_con_nnya": {
            "pm36": "Tener heladera",
            "pm39": "Tener frazadas suficientes",
            "pm42": "Tener ropa adecuada",
            "pm45": "Reemplazar calzado y ropa",
        },
        "hogares_sin_nnya": {
            "pm39": "Tener frazadas suficientes",
            "pm42": "Tener ropa adecuada",
            "pm45": "Reemplazar calzado y ropa",
        },
        "meta": {"label": "4. Equipamiento del hogar"},
    },
    "dimension_5": {
        "hogares_con_nnya": {
            "pm48": "Utilizar transporte público",
            "pm78": "Útiles escolares requeridos",
            "pm81": "Dispositivo electrónico para estudiar",
            "pm84": "Gastos personales semanales",
            "pm87": "Irse de vacaciones al menos una semana",
            "pm90": "Invitar familiares o amigos a comer",
        },
        "hogares_sin_nnya": {
            "pm48": "Utilizar transporte público",
            "pm84": "Gastos personales semanales",
            "pm87": "Irse de vacaciones al menos una semana",
            "pm90": "Invitar familiares o amigos a comer",
        },
        "meta": {"label": "5. Privación social y educación"},
    },
}

# Los 16 indicadores comunes a ambos tipos de hogar (Tabla A.4 de la tesis)
INDICADORES_COMUNES = {
    "hpm2": ("1. Alimentación", "Comer menos variado"),
    "hpm1": ("1. Alimentación", "Saltearse comidas"),
    "hpm3": ("1. Alimentación", "Reducir porciones"),
    "pm54": ("2. Salud y cuidados", "Atención médica"),
    "pm57": ("2. Salud y cuidados", "Acceso de remedios recetados"),
    "pm60": ("2. Salud y cuidados", "Realización de estudios médicos"),
    "pm63": ("2. Salud y cuidados", "Tratamientos dentales"),
    "pm9": ("3. Vivienda y servicios", "Reparar goteras"),
    "pm15": ("3. Vivienda y servicios", "Acceso a agua caliente"),
    "pm24": ("3. Vivienda y servicios", "Conexión a internet"),
    "pm39": ("4. Equipamiento del hogar", "Tener frazadas suficientes"),
    "pm42": ("4. Equipamiento del hogar", "Tener ropa adecuada"),
    "pm45": ("4. Equipamiento del hogar", "Reemplazar calzado y ropa"),
    "pm48": ("5. Privación social y educación", "Utilizar transporte público"),
    "pm84": ("5. Privación social y educación", "Gastos personales semanales"),
    "pm87": ("5. Privación social y educación", "Irse de vacaciones al menos una semana"),
    "pm90": ("5. Privación social y educación", "Invitar familiares o amigos a comer"),
}

# Indicadores relevados en el módulo PM pero excluidos total o parcialmente del índice oficial
INDICADORES_EXCLUIDOS_MODULO_PM = [
    {
        "variable": "pm21",
        "etiqueta": "Sin luz por conexión formal con medidor (en hogares sin NNyA)",
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
        "etiqueta": "Sin asistencia/apoyo para tareas de cuidado (en hogares sin NNyA)",
        "dimension": "2. Salud y cuidados",
        "universo_excluido": "Hogares sin NNyA",
        "motivo_exclusion": (
            "Se excluye en hogares sin menores de 18 años, invisibilizando la carga de cuidado de adultos mayores "
            "o personas con discapacidad en hogares adultos de villas (12,1% vs. 2,3% en el resto)."
        ),
    },
    {
        "variable": "pm36",
        "etiqueta": "No disponer de heladera por falta de recursos (en hogares sin NNyA)",
        "dimension": "4. Equipamiento del hogar",
        "universo_excluido": "Hogares sin NNyA",
        "motivo_exclusion": (
            "Excluido en hogares sin menores por baja incidencia promedio en la ciudad formal (0,6%), "
            "pero presente en el 5,1% de los hogares sin menores en villas."
        ),
    },
    {
        "variable": "pm66",
        "etiqueta": "Sin acceso a métodos anticonceptivos (en hogares sin NNyA)",
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

# Mapeos de dominio y clasificaciones
MAP_DOMINIO = {
    3: "Villas y barrios populares",
    4: "Resto de la ciudad",
}

MAP_TIPO_HOGAR = {
    "Hogares con NNyA": 1,
    "Hogares sin NNyA": 0,
}

# Tolerancia numérica para punto flotante
EPS = 1e-9

# Códigos de 'no aplica / no sabe / no responde' a tratar como NaN en pm*/hpm*
CODIGOS_NO_APLICA: list[int] = []

# Parámetros metodológicos por defecto (Metodología IDECBA)
DEFAULT_K_INTRA = 0.33
DEFAULT_K_INTER = 0.40  # 2/5
DEFAULT_YEAR = 2025
AVAILABLE_YEARS = [2025]
