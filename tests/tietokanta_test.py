import sqlite3
import unittest
from tietokanta import ViiteVarasto


class TestViiteVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = ViiteVarasto(sqlite3.connect(":memory:"))

    def kirja(self, **muutokset):
        kirja = {
            "viiteavain": "Tervo2022",
            "tekijat": "Tervo, Jari",
            "otsikko": "Ukko",
            "vuosi": 2022,
            "kustantaja": "Otava",
        }
        kirja.update(muutokset)
        return kirja

    def test_kirja_tallentuu_kustantajan_kanssa(self):
        self.varasto.lisaa_teos(self.kirja())

        teokset = self.varasto.listaa_teokset()

        self.assertEqual(len(teokset), 1)
        self.assertEqual(teokset[0]["kustantaja"], "Otava")
        self.assertEqual(teokset[0]["tyyppi"], "book")

    def test_sama_viiteavain_kahdesti_aiheuttaa_virheen(self):
        self.varasto.lisaa_teos(self.kirja())

        with self.assertRaises(ValueError):
            self.varasto.lisaa_teos(self.kirja(otsikko="Toinen kirja"))
