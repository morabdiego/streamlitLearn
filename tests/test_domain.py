"""Pruebas unitarias para la lógica de cálculo de Alkire-Foster y análisis de dominio."""
import unittest
import numpy as np
import pandas as pd

from src.domain.alkire_foster import (
    apply_ipm_cutoffs,
    calculate_deprivation_distribution,
    calculate_dimension_contributions,
    calculate_indicator_rate,
    calculate_ipm_metrics,
    calculate_poverty_overlap,
    calculate_structural_habitat_rates,
    score_dimension,
)


class TestAlkireFoster(unittest.TestCase):
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

    def test_calculate_ipm_metrics(self):
        df = pd.DataFrame({
            "pobre_ipm": [1, 0, 1],
            "c_vector": [0.6, 0.2, 0.4],
            "fexp": [100.0, 100.0, 200.0],
        })
        metrics = calculate_ipm_metrics(df)
        self.assertAlmostEqual(metrics.h, 0.75)
        self.assertAlmostEqual(metrics.a, 140 / 300)
        self.assertAlmostEqual(metrics.m0, 0.75 * (140 / 300))
        self.assertEqual(metrics.hogares_expandidos, 400)
        self.assertEqual(metrics.pobres_expandidos, 300)

    def test_calculate_indicator_rate_uncensored_and_censored(self):
        df = pd.DataFrame({
            "ind1": [1, 0, 1, np.nan],
            "pobre_ipm": [1, 0, 0, 1],
            "fexp": [10.0, 20.0, 10.0, 50.0],
        })
        # No censurada: privados (fila 0 y 2) = 20 sobre válidos (40) = 50%
        rate_uncensored = calculate_indicator_rate(df, "ind1", censurado=False)
        self.assertAlmostEqual(rate_uncensored, 50.0)
        # Censurada: privado Y pobre_ipm==1 (solo fila 0 = 10) sobre válidos (40) = 25%
        rate_censored = calculate_indicator_rate(df, "ind1", censurado=True)
        self.assertAlmostEqual(rate_censored, 25.0)

    def test_calculate_poverty_overlap(self):
        df = pd.DataFrame({
            "pobre_ipm": [1, 1, 0, 0],
            "pobre_ingreso": [1, 0, 1, 0],
            "fexp": [10.0, 10.0, 10.0, 10.0],
        })
        overlap = calculate_poverty_overlap(df)
        self.assertEqual(overlap["Doble pobreza (Crónica)"], 25.0)
        self.assertEqual(overlap["Solo pobreza multidimensional"], 25.0)
        self.assertEqual(overlap["Solo pobreza por ingresos"], 25.0)
        self.assertEqual(overlap["No pobre en ninguna"], 25.0)

    def test_calculate_structural_habitat_rates(self):
        df = pd.DataFrame({
            "h2": [3, 1],
            "hacinam_2": [3, 1],
            "v12": [2, 1],
            "h1": [2, 1],
            "hpm4": [1, 2],
            "fexp": [50.0, 50.0],
        })
        rates = calculate_structural_habitat_rates(df)
        for val in rates.values():
            self.assertAlmostEqual(val, 50.0)


if __name__ == "__main__":
    unittest.main()
