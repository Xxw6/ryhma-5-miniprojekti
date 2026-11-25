import sqlite3
import unittest

from main import Sovellus
from palvelu import ViitePalvelu
from tietokanta import ViiteVarasto
from tests.stub_io import StubIO


def kirja(**muutokset):
    tiedot = {
        "tekijat": "Tervo, Jari",
        "otsikko": "Ukko",
        "vuosi": "2022",
        "kustantaja": "Otava",
    }
    tiedot.update(muutokset)
    return tiedot


class TestPoisto(unittest.TestCase):
    def setUp(self):
        self.yhteys = sqlite3.connect(":memory:")
        self.varasto = ViiteVarasto(self.yhteys)
        self.palvelu = ViitePalvelu(self.varasto)
        self.avain = self.palvelu.lisaa_teos(kirja())

    def tearDown(self):
        self.yhteys.close()

    def avaimet(self):
        return [viite["viiteavain"] for viite in self.palvelu.listaa_teokset()]

    def test_varasto_poistaa_viitteen_ja_palauttaa_true(self):
        self.assertTrue(self.varasto.poista_viite(self.avain))
        self.assertEqual(self.avaimet(), [])

    def test_varasto_palauttaa_false_olemattomalle_avaimelle(self):
        self.assertFalse(self.varasto.poista_viite("EiOle2000"))
        self.assertEqual(self.avaimet(), [self.avain])

    def test_palvelu_poistaa_vain_annetun_viitteen(self):
        toinen = self.palvelu.lisaa_teos(kirja(tekijat="Linna, Väinö", vuosi="1954"))

        self.palvelu.poista_viite(self.avain)

        self.assertEqual(self.avaimet(), [toinen])

    def test_palvelu_olematon_avain_aiheuttaa_virheen(self):
        with self.assertRaisesRegex(ValueError, "ei löytynyt"):
            self.palvelu.poista_viite("EiOle2000")

    def test_palvelu_tyhja_avain_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.poista_viite("   ")

    def test_palvelu_poistaa_vaikka_avaimen_ymparilla_on_valilyonteja(self):
        self.palvelu.poista_viite(f"  {self.avain}  ")

        self.assertEqual(self.avaimet(), [])

    def test_kayttoliittyma_poistaa_viitteen(self):
        io = StubIO(["5", self.avain, "0"])

        Sovellus(self.palvelu, io).kaynnista()

        self.assertIn(f"Viite {self.avain} poistettu.", io.tulosteet)
        self.assertEqual(self.avaimet(), [])

    def test_kayttoliittyma_kertoo_olemattomasta_avaimesta(self):
        io = StubIO(["5", "EiOle2000", "0"])

        Sovellus(self.palvelu, io).kaynnista()

        self.assertIn("Viiteavainta EiOle2000 ei löytynyt.", io.tulosteet)
        self.assertEqual(self.avaimet(), [self.avain])