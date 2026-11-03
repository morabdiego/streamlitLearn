"""Pruebas unitarias para las funciones de formateo."""
import unittest
from src.utils.formatters import format_decimal, format_integer, format_percentage


class TestFormatters(unittest.TestCase):
    def test_format_decimal(self):
        self.assertEqual(format_decimal(1234.56, decimales=1), "1.234,6")
        self.assertEqual(format_decimal(1234.56, decimales=2), "1.234,56")
        self.assertEqual(format_decimal(0.333, decimales=3), "0,333")
        self.assertEqual(format_decimal(None), "—")

    def test_format_integer(self):
        self.assertEqual(format_integer(1000), "1.000")
        self.assertEqual(format_integer(253992), "253.992")
        self.assertEqual(format_integer(None), "—")

    def test_format_percentage(self):
        self.assertEqual(format_percentage(18.39, decimales=1), "18,4%")
        self.assertEqual(format_percentage(None), "—")


if __name__ == "__main__":
    unittest.main()
