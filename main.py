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
                "\n1 Lisää teos\n2 Listaa teokset\n3 Tallenna BibTeX-tiedostoksi\n0 Lopeta"
            )
            valinta = self.syote_tulostus.lue("Valinta: ").strip()
            if valinta == "0":
                return
            if valinta == "1":
                self.lisaa_teos()
            elif valinta == "2":
                self.listaa_teokset()
            elif valinta == "3":
                self.tallenna_bibtex()
            else:
                self.syote_tulostus.kirjoita("Valitse 1, 2, 3 tai 0.")

    def lisaa_teos(self):
        teos = {
            "viiteavain": self.syote_tulostus.lue("Viiteavain (esim. tekija + vuosi ): "),
            "tekijat": self.syote_tulostus.lue("Tekijat: "),
            "otsikko": self.syote_tulostus.lue("Teoksen nimi: "),
            "vuosi": self.syote_tulostus.lue("Julkaisuvuosi: "),
        }
        try:
            self.palvelu.lisaa_teos(teos)
            self.syote_tulostus.kirjoita("Teos tallennettu.")
        except ValueError as virhe:
            self.syote_tulostus.kirjoita(str(virhe))

    def listaa_teokset(self):
        teokset = self.palvelu.listaa_teokset()
        if not teokset:
            self.syote_tulostus.kirjoita("Ei tallennettuja teoksia.")
        for teos in teokset:
            self.syote_tulostus.kirjoita(
                f"[{teos['viiteavain']}] {teos['tekijat']}: {teos['otsikko']} "
                f"({teos['vuosi']})."
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
