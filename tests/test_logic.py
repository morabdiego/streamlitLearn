"""Pruebas unitarias de los cálculos Alkire-Foster, matrices censurada/no censurada y validación EAH 2025."""
import unittest

import numpy as np
import pandas as pd

from src.config import DIMENSIONES_IPM
from src.logic import (
    apply_ipm_cutoffs,
    build_deprivation_dist_table,
    build_dimension_contributions_table,
    build_domain_poverty_table,
    build_excluded_indicators_table,
    build_habitat_table,
    build_indicator_rates_table,
    build_nnya_summary_table,
    build_overlap_table,
    build_sample_table,
    build_structure_2025_table,
    calculate_deprivation_distribution,
    calculate_dimension_contributions,
    calculate_indicator_rate,
    calculate_ipm_dataset,
    calculate_ipm_metrics,
    calculate_poverty_overlap,
    calculate_structural_habitat_rates,
    format_decimal,
    format_integer,
    format_percentage,
    load_hogares_data,
    score_dimension,
)


class TestFormatters(unittest.TestCase):
    def test_formatters_argentina_locale_and_nulls(self):
        self.assertEqual(format_decimal(0.1051, 3), "0,105")
        self.assertEqual(format_integer(1349888), "1.349.888")
        self.assertEqual(format_percentage(18.815), "18,8%")
        self.assertEqual(format_percentage(None), "—")
        self.assertEqual(format_percentage(np.nan), "—")


class TestAlkireFosterCalculations(unittest.TestCase):
    def test_score_dimension(self):
        df = pd.DataFrame({
            "v1": [1, 0, np.nan],
            "v2": [1, 1, 1],
            "v3": [np.nan, 0, np.nan],
        })
        scores = score_dimension(df, ["v1", "v2", "v3"])
        self.assertAlmostEqual(scores.iloc[0], 1.0)
        self.assertAlmostEqual(scores.iloc[1], 1 / 3)
        self.assertAlmostEqual(scores.iloc[2], 1.0)

    def test_uncensored_and_censored_matrices_and_metrics(self):
        dims = {"d1": {"label": "D1"}, "d2": {"label": "D2"}}
        df_scores = pd.DataFrame({
            "d1_score": [0.5, 0.5, 0.0],
            "d2_score": [0.5, 0.0, 0.0],
            "fexp": [100.0, 100.0, 200.0],
        })
        # k_intra=0.33, k_inter=1.0 (requiere las 2 dimensiones privadas)
        df = apply_ipm_cutoffs(df_scores, k_intra=0.33, k_inter=1.0, dimensiones=dims)

        # Matriz no censurada: hogar 1 está privado en d1 pero no es pobre IPM (c_vector=0.5 < 1.0)
        self.assertEqual(df["d1_privada"].tolist(), [1, 1, 0])
        self.assertEqual(df["pobre_ipm"].tolist(), [1, 0, 0])

        # Matriz censurada: hogar 1 pasa a 0 en d1_censurada y c_censurado
        self.assertEqual(df["d1_censurada"].tolist(), [1, 0, 0])
        self.assertEqual(df["c_censurado"].tolist(), [1.0, 0.0, 0.0])

        metrics = calculate_ipm_metrics(df)
        self.assertAlmostEqual(metrics.h, 0.25)
        self.assertAlmostEqual(metrics.a, 1.0)
        self.assertAlmostEqual(metrics.m0, 0.25)
        self.assertAlmostEqual(metrics.m0, np.average(df["c_censurado"], weights=df["fexp"]))

    def test_indicator_rate_three_modes_and_identity(self):
        df = pd.DataFrame({
            "ind1": [1, 0, 1, 9],       # fila 3 es Ns/Nc (9) -> excluida del universo válido
            "pobre_ipm": [1, 1, 0, 1],
            "fexp": [30.0, 10.0, 60.0, 50.0],
        })
        # Válidos (filas 0, 1, 2): peso total = 100; pobres válidos (filas 0, 1): peso = 40 (H = 0.40)
        # 1) No censurada: privados (filas 0 y 2 = 90) / 100 = 90%
        r_uncens = calculate_indicator_rate(df, "ind1", modo="no_censurada")
        self.assertAlmostEqual(r_uncens, 90.0)

        # 2) Censurada h_j(k): privado Y pobre (fila 0 = 30) / 100 = 30%
        r_cens = calculate_indicator_rate(df, "ind1", modo="censurada")
        self.assertAlmostEqual(r_cens, 30.0)

        # 3) Entre hogares pobres: privado dentro de pobres (30) / total pobres válidos (40) = 75%
        r_poor = calculate_indicator_rate(df, "ind1", modo="entre_pobres")
        self.assertAlmostEqual(r_poor, 75.0)

        # Identidad Alkire-Foster: h_j(k) == H_valido * tasa_entre_pobres
        h_valido = 40.0 / 100.0
        self.assertAlmostEqual(r_cens, h_valido * r_poor)

    def test_overlap_and_habitat_rates(self):
        df = pd.DataFrame({
            "pobre_ipm": [1, 1, 0, 0],
            "pobre_ingreso": [1, 0, 1, 0],
            "h2": [3, 1, 1, 9],
            "hacinam_2": [3, 2, 1, 9],
            "v12": [2, 1, 1, 9],
            "h1": [2, 1, 1, 9],
            "hpm4": [1, 2, 2, 9],
            "fexp": [25.0, 25.0, 25.0, 25.0],
        })
        overlap = calculate_poverty_overlap(df)
        self.assertAlmostEqual(sum(overlap.values()), 100.0)
        self.assertAlmostEqual(overlap["Pobreza estructural"], 25.0)

        # Con fila 3 como Ns/Nc (9), el peso válido en hábitat es 75.0
        hab = calculate_structural_habitat_rates(df)
        self.assertAlmostEqual(hab["Tenencia irregular"], 100 / 3)
        self.assertAlmostEqual(hab["Hacinamiento general (2 o más personas por cuarto)"], 200 / 3)
        self.assertAlmostEqual(hab["Hacinamiento crítico (más de 3 personas por cuarto)"], 100 / 3)


class TestEAH2025OfficialBenchmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw_df = load_hogares_data(2025)
        cls.df = calculate_ipm_dataset(cls.raw_df)

    def test_official_idecba_2025_rates(self):
        # Resultados oficiales publicados por IDECBA para EAH 2025
        m_total = calculate_ipm_metrics(self.df)
        m_con = calculate_ipm_metrics(self.df[self.df["tiene_nnya"] == 1])
        self.assertAlmostEqual(round(m_total.h * 100, 1), 18.8)
        self.assertAlmostEqual(round(m_con.h * 100, 1), 20.6)

        # Tasas oficiales por dimensión en CABA 2025: 25,6% | 4,1% | 12,1% | 7,3% | 20,9%
        expected_dims = {
            "dimension_1": 25.6,
            "dimension_2": 4.1,
            "dimension_3": 12.1,
            "dimension_4": 7.3,
            "dimension_5": 20.9,
        }
        w = self.df["fexp"]
        for dim_key, expected in expected_dims.items():
            rate = np.average(self.df[f"{dim_key}_privada"], weights=w) * 100
            self.assertAlmostEqual(round(rate, 1), expected)

    def test_alkire_foster_identities_and_tables_on_real_data(self):
        # 1. Contribuciones dimensionales suman 100%
        contribs = calculate_dimension_contributions(self.df)
        self.assertAlmostEqual(sum(contribs.values()), 100.0, places=6)

        # 2. Distribución de privaciones entre pobres suma 100% y su media ponderada / 5 == A
        dist = calculate_deprivation_distribution(self.df)
        self.assertAlmostEqual(sum(dist.values()), 100.0, places=6)
        mean_dims_share = sum(k * (pct / 100.0) for k, pct in dist.items()) / len(DIMENSIONES_IPM)
        m_total = calculate_ipm_metrics(self.df)
        self.assertAlmostEqual(mean_dims_share, m_total.a, places=6)

        # 3. En todos los indicadores: censurada == H_grupo * entre_pobres, y censurada <= no_censurada
        con_nnya = self.df[self.df["tiene_nnya"] == 1]
        h_con = calculate_ipm_metrics(con_nnya).h
        for dim_cfg in DIMENSIONES_IPM.values():
            for var in dim_cfg["con_nnya"]:
                r_no_cens = calculate_indicator_rate(con_nnya, var, modo="no_censurada")
                r_cens = calculate_indicator_rate(con_nnya, var, modo="censurada")
                r_pobres = calculate_indicator_rate(con_nnya, var, modo="entre_pobres")
                self.assertLessEqual(r_cens, r_no_cens + 1e-9)
                self.assertAlmostEqual(r_cens, h_con * r_pobres, places=6)

        # 4. Construcción de todas las tablas de la interfaz
        self.assertEqual(len(build_sample_table(self.df)), 3)
        self.assertEqual(len(build_domain_poverty_table(self.df)), 3)
        self.assertEqual(len(build_overlap_table(self.df)), 4)
        self.assertEqual(len(build_deprivation_dist_table(self.df)), 4)
        self.assertEqual(len(build_structure_2025_table()), 27)
        self.assertEqual(len(build_dimension_contributions_table(self.df)), 5)
        self.assertEqual(len(build_excluded_indicators_table(self.df)), 7)
        self.assertEqual(len(build_habitat_table(self.df)), 6)
        self.assertEqual(len(build_nnya_summary_table(self.df)), 2)
        self.assertEqual(len(build_indicator_rates_table(self.df, tiene_nnya=1, modo="no_censurada")), 27)
        self.assertEqual(len(build_indicator_rates_table(self.df, tiene_nnya=0, modo="entre_pobres")), 17)


if __name__ == "__main__":
    unittest.main()
