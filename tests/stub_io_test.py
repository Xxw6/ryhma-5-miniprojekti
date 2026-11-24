import unittest
from unittest.mock import patch

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
        self.assertIn("Valitse 1, 2, 3, 4 tai 0.", io.tulosteet)


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