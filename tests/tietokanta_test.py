import sqlite3
import unittest
from tietokanta import ViiteVarasto


class TestViiteVarasto(unittest.TestCase):

    def setUp(self):
        self.yhteys = sqlite3.connect(":memory:")
        self.yhteys.row_factory = sqlite3.Row
        self.yhteys.execute("""
            CREATE TABLE "references" (
                id INTEGER PRIMARY KEY,
                citekey TEXT NOT NULL UNIQUE,
                entry_type TEXT NOT NULL,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                publisher TEXT,
                journal TEXT,
                volume TEXT,
                pages TEXT
            )
        """)
        self.yhteys.executemany("""
            INSERT INTO "references"
            (id, citekey, entry_type, author, title, year, publisher, journal, volume, pages)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (1, "kirja1", "kirja", "Testi Testinen", "Testauksesta", 2020, "WSOY", None, None, None),
            (2, "artikkeli1", "article", "Teppo Testaaja", "Teposta", 1999, None, "Aku Ankka", "10", "1-10"),
        ])
        self.yhteys.commit()
        self.varasto = ViiteVarasto(self.yhteys)

    def tearDown(self):
        self.yhteys.close()

    def test_listaa_teokset_palauttaa_kaikki_id_jarjestyksessa(self):
        tulos = self.varasto.listaa_teokset()

        self.assertEqual([r["id"] for r in tulos], [1, 2])
        self.assertEqual(tulos[1]["viiteavain"], "artikkeli1")
        self.assertEqual(tulos[1]["tyyppi"], "article")
        self.assertEqual(tulos[0]["kustantaja"], "WSOY")

    def test_listaa_artikkelit_palauttaa_vain_artikkelit(self):
        tulos = self.varasto.listaa_artikkelit()

        self.assertEqual(len(tulos), 1)
        self.assertEqual(tulos[0]["viiteavain"], "artikkeli1")
        self.assertEqual(tulos[0]["tekijat"], "Teppo Testaaja")
        self.assertNotIn("tyyppi", tulos[0])
        self.assertNotIn("kustantaja", tulos[0])
    
    def test_listaa_artikkelit_palauttaa_tyhjan_listan_kun_artikkeleita_ei_ole(self):
        self.yhteys.execute(
            'DELETE FROM "references" WHERE entry_type = "article"'
        )
        self.yhteys.commit()

        tulos = self.varasto.listaa_artikkelit()

        self.assertEqual(tulos, [])


    def test_listaa_artikkelit_palauttaa_kaikki_artikkelit(self):
        self.yhteys.execute("""
            INSERT INTO "references"
            (citekey, entry_type, author, title, year, journal, volume, pages)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "artikkeli2", "article", "Matti Meikäläinen",
            "Toinen artikkeli", 2000,
            "Testilehti", "1", "11-20"
        ))
        self.yhteys.commit()

        tulos = self.varasto.listaa_artikkelit()

        self.assertEqual(len(tulos), 2)

    def test_lisaa_teos_tallentaa_teoksen(self):
        teos = {
            "viiteavain": "kirja2",
            "tekijat": "Matti Meikäläinen",
            "otsikko": "Uusi teos",
            "vuosi": 2018
        }

        self.varasto.lisaa_teos(teos)

        tulos = self.varasto.listaa_teokset()

        self.assertEqual(len(tulos), 3)
        self.assertEqual(tulos[-1]["viiteavain"], "kirja2")

    def test_lisaa_artikkeli_tallentaa_artikkelin(self):
        artikkeli = {
            "viiteavain": "artikkeli2",
            "tekijat": "Matti Meikäläinen",
            "otsikko": "Uusi artikkeli",
            "vuosi": 2024,
            "journal": "Testilehti",
            "volume": "1",
            "pages": "1-10"
        }

        self.varasto.lisaa_artikkeli(artikkeli)

        tulos = self.varasto.listaa_artikkelit()

        self.assertEqual(len(tulos), 2)
        self.assertEqual(tulos[-1]["viiteavain"], "artikkeli2")

    def test_lisaa_teos_virhe_kun_viiteavain_on_olemassa(self):
        teos = {
            "viiteavain": "kirja1",
            "tekijat": "Joku",
            "otsikko": "Testi",
            "vuosi": 2024
        }

        with self.assertRaises(ValueError):
            self.varasto.lisaa_teos(teos)

class TestViiteVarastoKirjat(unittest.TestCase):
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
            
    if __name__ == "__main__":
    unittest.main()