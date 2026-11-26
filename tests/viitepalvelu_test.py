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

    def test_haku_loytaa_tekijan_perusteella(self):
        self.palvelu.lisaa_teos(
            self.teos(tekijat="Tervo Jari")
        )

        tulokset = self.palvelu.hae_viitteet(tekija="tervo")

        self.assertEqual(len(tulokset), 1)
        self.assertEqual(tulokset[0]["tekijat"], "Tervo Jari")

    def test_haku_loytaa_vuoden_perusteella(self):
        self.palvelu.lisaa_teos(
            self.teos(vuosi="2021")
        )
        self.palvelu.lisaa_teos(
            self.teos(vuosi="2022", tekijat="Niemi Sari")
        )

        tulokset = self.palvelu.hae_viitteet(vuosi="2022")

        self.assertEqual(len(tulokset), 1)
        self.assertEqual(tulokset[0]["vuosi"], 2022)

    def test_haku_loytaa_kustantajan_perusteella(self):
        self.palvelu.lisaa_teos(
            self.teos(kustantaja="Otava")
        )

        tulokset = self.palvelu.hae_viitteet(julkaisu="otava")

        self.assertEqual(len(tulokset), 1)

    def test_haku_loytaa_artikkelin_julkaisun_perusteella(self):
        self.palvelu.lisaa_artikkeli(
            self.artikkeli(journal="Tieteellinen julkaisu")
        )

        tulokset = self.palvelu.hae_viitteet(
            julkaisu="tieteellinen"
        )

        self.assertEqual(len(tulokset), 1)

    def test_haku_yhdistaa_useita_ehtoja(self):
        self.palvelu.lisaa_teos(
            self.teos(
                tekijat="Tervo Jari",
                vuosi="2022",
                kustantaja="Otava"
            )
        )
        self.palvelu.lisaa_teos(
            self.teos(
                tekijat="Tervo Jari",
                vuosi="2021",
                kustantaja="Otava"
            )
        )

        tulokset = self.palvelu.hae_viitteet(
            tekija="Tervo",
            vuosi="2022",
            julkaisu="Otava"
        )

        self.assertEqual(len(tulokset), 1)
        self.assertEqual(tulokset[0]["vuosi"], 2022)

    def test_haku_ilman_tuloksia_palauttaa_tyhjan_listan(self):
        self.palvelu.lisaa_teos(self.teos())

        tulokset = self.palvelu.hae_viitteet(
            tekija="Loytymattoman"
        )

        self.assertEqual(tulokset, [])

    def test_haku_ilman_ehtoja_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.hae_viitteet()

    def test_haku_virheellisella_vuodella_aiheuttaa_virheen(self):
        with self.assertRaises(ValueError):
            self.palvelu.hae_viitteet(vuosi="kaksituhatta")