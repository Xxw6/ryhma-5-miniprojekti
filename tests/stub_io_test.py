import unittest
from unittest.mock import Mock, patch

from main import Sovellus, SyoteTulostus
from tests.stub_io import StubIO


class TestStubIO(unittest.TestCase):
    def test_syotteet_luetaan_jarjestyksessa_ja_kysymykset_tallentuvat(self):
        io = StubIO(["1", "Martin2008"])

        self.assertEqual(io.lue("Valinta: "), "1")
        self.assertEqual(io.lue("Viiteavain: "), "Martin2008")
        self.assertEqual(io.kysymykset, ["Valinta: ", "Viiteavain: "])

    def test_tulosteet_tallentuvat_jarjestyksessa(self):
        io = StubIO([])

        io.kirjoita("Ensimmäinen")
        io.kirjoita("Toinen")

        self.assertEqual(io.tulosteet, ["Ensimmäinen", "Toinen"])

    def test_syotteiden_loppumisesta_tulee_selkea_virhe(self):
        io = StubIO([])

        with self.assertRaisesRegex(EOFError, "testisyötteet loppuivat"):
            io.lue("Valinta: ")


class TestValikonIO(unittest.TestCase):
    def test_sovellus_kayttaa_annettua_io_oliota_konsolin_sijaan(self):
        io = StubIO(["0"])
        sovellus = Sovellus(None, io)

        with patch("builtins.input", side_effect=AssertionError("Oikea syöte")):
            with patch("builtins.print", side_effect=AssertionError("Oikea tulostus")):
                sovellus.kaynnista()

        self.assertEqual(io.kysymykset, ["Valinta: "])
        self.assertIn("0 Lopeta", io.tulosteet[0])

    def test_virheellisen_valinnan_jalkeen_voi_lopettaa(self):
        io = StubIO(["virhe", "0"])
        sovellus = Sovellus(None, io)

        sovellus.kaynnista()

        self.assertEqual(io.kysymykset, ["Valinta: ", "Valinta: "])
        self.assertIn("Valitse 1, 2, 3, 4, 5, 6 tai 0.", io.tulosteet)

class TestSyoteTulostus(unittest.TestCase):
    def test_lue_valittaa_kysymyksen_ja_palauttaa_kayttajan_syotteen(self):
        io = SyoteTulostus()

        with patch("builtins.input", return_value="3") as syote:
            vastaus = io.lue("Valinta: ")

        syote.assert_called_once_with("Valinta: ")
        self.assertEqual(vastaus, "3")

    def test_kirjoita_tulostaa_annetun_tekstin(self):
        io = SyoteTulostus()

        with patch("builtins.print") as tulostus:
            io.kirjoita("Teos tallennettu.")

        tulostus.assert_called_once_with("Teos tallennettu.")

class TestHaunKayttoliittyma(unittest.TestCase):
    def test_haku_nayttaa_kirjaviitteen_tuloksen(self):
        io = StubIO(["6", "Tervo", "2022", "Otava", "0"])
        palvelu = Mock()
        palvelu.hae_viitteet.return_value = [{
            "tyyppi": "book",
            "viiteavain": "Tervo2022",
            "tekijat": "Tervo, Jari",
            "otsikko": "Ukko",
            "vuosi": 2022,
            "kustantaja": "Otava",
        }]

        sovellus = Sovellus(palvelu, io)
        sovellus.kaynnista()

        palvelu.hae_viitteet.assert_called_once_with(
            tekija="Tervo",
            vuosi="2022",
            julkaisu="Otava"
        )
        self.assertIn(
            "[Tervo2022] Tervo, Jari: Ukko (2022). Otava",
            io.tulosteet
        )

    def test_haku_nayttaa_artikkeliviitteen_tuloksen(self):
        io = StubIO(["6", "Tervo", "", "", "0"])
        palvelu = Mock()
        palvelu.hae_viitteet.return_value = [{
            "tyyppi": "article",
            "viiteavain": "Tervo2022",
            "tekijat": "Tervo, Jari",
            "otsikko": "Testiartikkeli",
            "vuosi": 2022,
            "journal": "Julkaisu X",
        }]

        sovellus = Sovellus(palvelu, io)
        sovellus.kaynnista()

        self.assertIn(
            "[Tervo2022] Tervo, Jari: "
            "Testiartikkeli (2022). Julkaisu X",
            io.tulosteet
        )

    def test_haku_ilmoittaa_tyhjasta_tuloksesta(self):
        io = StubIO(["6", "Ei löydy", "", "", "0"])
        palvelu = Mock()
        palvelu.hae_viitteet.return_value = []

        sovellus = Sovellus(palvelu, io)
        sovellus.kaynnista()

        self.assertIn("Ei hakutuloksia.", io.tulosteet)

    def test_haku_ilmoittaa_virheellisista_hakuehdoista(self):
        io = StubIO(["6", "", "", "", "0"])
        palvelu = Mock()
        palvelu.hae_viitteet.side_effect = ValueError(
            "Anna vähintään yksi hakuehto."
        )

        sovellus = Sovellus(palvelu, io)
        sovellus.kaynnista()

        self.assertIn(
            "Anna vähintään yksi hakuehto.",
            io.tulosteet
        )