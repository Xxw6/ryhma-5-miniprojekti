import unittest
from palvelu import ViitePalvelu


class ViiteVarastoStub:
    def __init__(self):
        self.teokset = []

    def lisaa_teos(self, teos):
        self.teokset.append(teos)

    def listaa_teokset(self):
        return self.teokset


class TestViitePalvelu(unittest.TestCase):
    def setUp(self):
        self.varasto = ViiteVarastoStub()
        self.palvelu = ViitePalvelu(self.varasto)

    def teos(self, **muutokset):
        teos = {
            "viiteavain": "Tervo22",
            "tekijat": "Tervo Jari",
            "otsikko": "Ukko",
            "vuosi": "2022",
        }
        teos.update(muutokset)
        return teos

    def test_kelvollinen_teos_tallentuu_varastoon(self):
        self.palvelu.lisaa_teos(self.teos())

        self.assertEqual(len(self.varasto.teokset), 1)
        self.assertEqual(self.varasto.teokset[0]["otsikko"], "Ukko")

    def test_vuosi_muutetaan_kokonaisluvuksi(self):
        self.palvelu.lisaa_teos(self.teos())

        self.assertEqual(self.varasto.teokset[0]["vuosi"], 2022)

    def test_kenttien_ylimaaraiset_valilyonnit_poistetaan(self):
        self.palvelu.lisaa_teos(self.teos(otsikko="  Ukko  "))

        self.assertEqual(self.varasto.teokset[0]["otsikko"], "Ukko")

    def test_tyhja_kentta_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.lisaa_teos(self.teos(tekijat=""))

        self.assertEqual(self.varasto.teokset, [])

    def test_vuosi_joka_ei_ole_luku_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.lisaa_teos(self.teos(vuosi="kaksituhatta"))

    def test_vuosi_alueen_ulkopuolella_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.lisaa_teos(self.teos(vuosi="0"))

    def test_listaus_palauttaa_varaston_teokset(self):
        self.palvelu.lisaa_teos(self.teos())

        self.assertEqual(len(self.palvelu.listaa_teokset()), 1)