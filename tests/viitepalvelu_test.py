import unittest
from palvelu import ViitePalvelu


class ViiteVarastoStub:
    def __init__(self):
        self.teokset = []

    def lisaa_teos(self, teos):
        self.teokset.append(teos)

    def lisaa_artikkeli(self, artikkeli):
        self.teokset.append(artikkeli)

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


    def artikkeli(self, **muutokset):
        tiedot = {
            "viiteavain": "Tervo22",
            "tekijat": "Tervo Jari",
            "otsikko": "Ukko",
            "journal": "Tieteellinen julkaisu",
            "vuosi": "2022",
            "volume": "10",
            "pages": "15-20",
        }
        tiedot.update(muutokset)
        return tiedot

    def test_kelvollinen_artikkeli_tallentuu_varastoon(self):
        self.palvelu.lisaa_artikkeli(self.artikkeli())

        self.assertEqual(len(self.varasto.teokset), 1)
        self.assertEqual(
            self.varasto.teokset[0]["journal"],
            "Tieteellinen julkaisu"
        )

    def test_artikkelin_vuosi_muutetaan_kokonaisluvuksi(self):
        self.palvelu.lisaa_artikkeli(self.artikkeli())

        self.assertEqual(self.varasto.teokset[0]["vuosi"], 2022)

    def test_artikkelin_pakollinen_kentta_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.lisaa_artikkeli(self.artikkeli(journal=""))

    def test_artikkelin_vapaaehtoiset_kentat_voivat_olla_tyhjia(self):
        self.palvelu.lisaa_artikkeli(
            self.artikkeli(volume="", pages="")
        )

        self.assertEqual(self.varasto.teokset[0]["volume"], "")
        self.assertEqual(self.varasto.teokset[0]["pages"], "")

    def test_artikkelin_virheellinen_vuosi_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.lisaa_artikkeli(
                self.artikkeli(vuosi="virhe")
            )

    def test_artikkelin_vuosi_alueen_ulkopuolella_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.lisaa_artikkeli(
                self.artikkeli(vuosi="10000")
            )

    def test_kustantaja_tallentuu(self):
        self.palvelu.lisaa_teos(self.teos(kustantaja="Otava"))

        self.assertEqual(self.varasto.teokset[0]["kustantaja"], "Otava")

    def test_kustantaja_on_vapaaehtoinen(self):
        self.palvelu.lisaa_teos(self.teos())

        self.assertEqual(self.varasto.teokset[0]["kustantaja"], "")

    def test_viiteavain_muodostetaan_automaattisesti(self):
        teos = self.teos(tekijat="Tervo, Jari", vuosi="2022")
        del teos["viiteavain"]

        viiteavain = self.palvelu.lisaa_teos(teos)

        self.assertEqual(viiteavain, "Tervo2022")
        self.assertEqual(self.varasto.teokset[0]["viiteavain"], "Tervo2022")
        
    def test_yhdysmerkki_sukunimessa_hyvaksytaan(self):
      teos = self.teos(tekijat="Smith-Jones, Ann")
      del teos["viiteavain"]

      viiteavain = self.palvelu.lisaa_teos(teos)

      self.assertEqual(viiteavain, "SmithJones2022")

    def test_samat_viiteavaimet_muodostuvat_yksilollisiksi(self):
        eka = self.teos()
        toka = self.teos()
        kolmas = self.teos()

        del eka["viiteavain"]
        del toka["viiteavain"]
        del kolmas["viiteavain"]

        eka_avain = self.palvelu.lisaa_teos(eka)
        toka_avain = self.palvelu.lisaa_teos(toka)
        kolmas_avain = self.palvelu.lisaa_teos(kolmas)

        self.assertEqual(eka_avain, "Jari2022")
        self.assertEqual(toka_avain, "Jari2022a")
        self.assertEqual(kolmas_avain, "Jari2022b")

    def test_manuaalinen_viiteavain_tallennetaan(self):
        viiteavain = self.palvelu.lisaa_teos(
            self.teos(viiteavain="OmaAvain2022")
        )

        self.assertEqual(viiteavain, "OmaAvain2022")
        self.assertEqual(
            self.varasto.teokset[0]["viiteavain"],
            "OmaAvain2022"
        )

    def test_tyhjalla_viiteavaimella_muodostetaan_automaattinen(self):
        viiteavain = self.palvelu.lisaa_teos(
            self.teos(viiteavain="")
        )

        self.assertEqual(viiteavain, "Jari2022")

    def test_manuaalinen_viiteavain_saa_olla_artikkelilla(self):
        viiteavain = self.palvelu.lisaa_artikkeli(
            self.artikkeli(viiteavain="Artikkeli2022")
        )

        self.assertEqual(viiteavain, "Artikkeli2022")

    def test_artikkelin_tyhjalla_viiteavaimella_muodostetaan_automaattinen(self):
        viiteavain = self.palvelu.lisaa_artikkeli(
            self.artikkeli(viiteavain="")
        )

        self.assertEqual(viiteavain, "Jari2022")

    def test_manuaalinen_kaksoiskappale_hylataan(self):
        self.palvelu.lisaa_teos(
            self.teos(viiteavain="OmaAvain")
        )

        with self.assertRaisesRegex(ValueError, "jo käytössä"):
            self.palvelu.lisaa_artikkeli(
                self.artikkeli(viiteavain="OmaAvain")
            )

        self.assertEqual(len(self.varasto.teokset), 1)

    def test_manuaalinen_viiteavain_jossa_erikoismerkki_hylataan(self):
        with self.assertRaisesRegex(ValueError, "erikoismerkkejä"):
            self.palvelu.lisaa_teos(
                self.teos(viiteavain="Oma_Avain")
            )

        self.assertEqual(self.varasto.teokset, [])

    def test_automaattinen_avain_ei_ohita_manuaalisesti_varattua(self):
        self.palvelu.lisaa_teos(
            self.teos(viiteavain="Jari2022")
        )

        viiteavain = self.palvelu.lisaa_teos(
            self.teos(viiteavain="")
        )

        self.assertEqual(viiteavain, "Jari2022a")

    def test_automaattinen_viiteavain_toimii_yli_26_suffiksilla(self):
        perusavain = "Jari2022"

        self.varasto.teokset.extend(
            {"viiteavain": perusavain + liite}
            for liite in (
                [""] +
                [chr(kirjain) for kirjain in range(ord("a"), ord("z") + 1)] +
                ["aa"]
            )
        )

        viiteavain = self.palvelu.lisaa_teos(
            self.teos(viiteavain="")
        )

        self.assertEqual(viiteavain, "Jari2022ab")
