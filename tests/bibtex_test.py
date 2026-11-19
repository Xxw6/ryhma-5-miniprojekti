import unittest
from bibtex import muodosta_bibtex, muodosta_viite, suojaa


def teos(**muutokset):
    tiedot = {
        "viiteavain": "Tervo22",
        "tekijat": "Tervo, Jari",
        "otsikko": "Ukko",
        "vuosi": 2022,
        "kustantaja": "Otava",
    }
    tiedot.update(muutokset)
    return tiedot


class TestBibtex(unittest.TestCase):
    def test_kirjaviite_alkaa_tyypilla_ja_avaimella(self):
        self.assertTrue(muodosta_viite(teos()).startswith("@book{Tervo22,"))

    def test_kaikki_kentat_tulevat_mukaan(self):
        viite = muodosta_viite(teos())

        self.assertIn("author = {Tervo, Jari},", viite)
        self.assertIn("title = {Ukko},", viite)
        self.assertIn("year = {2022},", viite)
        self.assertIn("publisher = {Otava},", viite)

    def test_tyhja_kustantaja_jatetaan_pois(self):
        self.assertNotIn("publisher", muodosta_viite(teos(kustantaja="")))

    def test_jokainen_teos_on_oma_merkintansa(self):
        tulos = muodosta_bibtex([teos(), teos(viiteavain="Linna54")])

        self.assertEqual(tulos.count("@book{"), 2)
        self.assertIn("@book{Linna54,", tulos)

    def test_tyhja_lista_tuottaa_tyhjan_tiedoston(self):
        self.assertEqual(muodosta_bibtex([]), "")

    def test_latexin_erikoismerkit_suojataan(self):
        self.assertEqual(suojaa("R&D 100%"), r"R\&D 100\%")