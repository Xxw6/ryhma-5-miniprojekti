from contextlib import closing
from pathlib import Path
import sqlite3

from tietokanta import ViiteVarasto
from palvelu import ViitePalvelu
from bibtex import muodosta_bibtex


class SyoteTulostus:

    def lue(self, kysymys):
        return input(kysymys)

    def kirjoita(self, teksti):
        print(teksti)


class Sovellus:
    def __init__(self, palvelu, syote_tulostus):
        self.palvelu = palvelu
        self.syote_tulostus = syote_tulostus

    def kaynnista(self):
        while True:
            self.syote_tulostus.kirjoita(
                "\n1 Lisää kirjaviite"
                "\n2 Lisää artikkeliviite"
                "\n3 Listaa teokset"
                "\n4 Tallenna BibTeX-tiedostoksi"
                "\n5 Poista viite"
                "\n0 Lopeta"
            )
            valinta = self.syote_tulostus.lue("Valinta: ").strip()

            if valinta == "0":
                return
            if valinta == "1":
                self.lisaa_teos()
            elif valinta == "2":
                self.lisaa_artikkeli()
            elif valinta == "3":
                self.listaa_teokset()
            elif valinta == "4":
                self.tallenna_bibtex()
            elif valinta == "5":
                self.poista_viite()
            else:
                self.syote_tulostus.kirjoita(
                    "Valitse 1, 2, 3, 4, 5 tai 0."
                )


    def lisaa_teos(self):
        teos = {
            "tekijat": self.syote_tulostus.lue("Tekijat: "),
            "otsikko": self.syote_tulostus.lue("Teoksen nimi: "),
            "vuosi": self.syote_tulostus.lue("Julkaisuvuosi: "),
            "kustantaja": self.syote_tulostus.lue("Kustantaja (vapaaehtoinen): "),
        }
        try:
            viiteavain = self.palvelu.lisaa_teos(teos)
            self.syote_tulostus.kirjoita(f"Teos tallennettu viiteavaimella {viiteavain}."
            )
        except ValueError as virhe:
            self.syote_tulostus.kirjoita(str(virhe))

    def lisaa_artikkeli(self):
        artikkeli = {
            "viiteavain": self.syote_tulostus.lue(
                "Viiteavain (esim. tekija + vuosi): "
            ),
            "tekijat": self.syote_tulostus.lue("Tekijat: "),
            "otsikko": self.syote_tulostus.lue("Artikkelin otsikko: "),
            "journal": self.syote_tulostus.lue("Julkaisun nimi (journal): "),
            "vuosi": self.syote_tulostus.lue("Julkaisuvuosi: "),
            "volume": self.syote_tulostus.lue(
                "Vuosikerta (volume, vapaaehtoinen): "
            ),
            "pages": self.syote_tulostus.lue(
                "Sivut (pages, vapaaehtoinen): "
            ),
        }
        try:
            self.palvelu.lisaa_artikkeli(artikkeli)
            self.syote_tulostus.kirjoita(
                "Artikkeliviite tallennettu."
            )
        except ValueError as virhe:
            self.syote_tulostus.kirjoita(str(virhe))

    def listaa_teokset(self):
        teokset = self.palvelu.listaa_teokset()

        if not teokset:
            self.syote_tulostus.kirjoita("Ei tallennettuja teoksia.")
            return

        for teos in teokset:
            if teos["tyyppi"] == "article":
                self.syote_tulostus.kirjoita(
                    f"[{teos['viiteavain']}] {teos['tekijat']}: "
                    f"{teos['otsikko']} ({teos['vuosi']}). "
                    f"{teos['journal']}"
                )
            else:
                self.syote_tulostus.kirjoita(
                    f"[{teos['viiteavain']}] {teos['tekijat']}: "
                    f"{teos['otsikko']} ({teos['vuosi']})."
                )


    def tallenna_bibtex(self):
        teokset = self.palvelu.listaa_teokset()
        if not teokset:
            self.syote_tulostus.kirjoita("Ei tallennettuja teoksia.")
            return
        nimi = self.syote_tulostus.lue("Tiedoston nimi (references.bib): ").strip()
        polku = Path(nimi or "references.bib")
        polku.write_text(muodosta_bibtex(teokset), encoding="utf-8")
        self.syote_tulostus.kirjoita(f"BibTeX tallennettu: {polku.resolve()}")
    
    def poista_viite(self):
        viiteavain = self.syote_tulostus.lue("Poistettavan viitteen viiteavain: ")
        try:
            self.palvelu.poista_viite(viiteavain)
            self.syote_tulostus.kirjoita(f"Viite {viiteavain.strip()} poistettu.")
        except ValueError as virhe:
            self.syote_tulostus.kirjoita(str(virhe))

def paaohjelma():
    tietokantapolku = Path(__file__).resolve().parent / "references.db"
    try:
        with closing(sqlite3.connect(tietokantapolku)) as yhteys:
            varasto = ViiteVarasto(yhteys)
            palvelu = ViitePalvelu(varasto)
            Sovellus(palvelu, SyoteTulostus()).kaynnista()
    except (EOFError, KeyboardInterrupt):
        print("\nLopetetaan.")
    except sqlite3.Error as virhe:
        print(f"Tietokantavirhe: {virhe}")


if __name__ == "__main__":
    paaohjelma()
