import sqlite3

from main import Sovellus
from palvelu import ViitePalvelu
from tietokanta import ViiteVarasto
from tests.stub_io import StubIO


class AppLibrary:
    def __init__(self):
        self._syotteet = []
        self._io = None
        self._palvelu = ViitePalvelu(ViiteVarasto(sqlite3.connect(":memory:")))

    def syota(self, arvo):
        self._syotteet.append(arvo)

    def kaynnista_sovellus(self):
        self._io = StubIO(self._syotteet + ["0"])
        self._syotteet = []
        Sovellus(self._palvelu, self._io).kaynnista()

    def tulosteessa_pitaisi_olla(self, teksti):
        if teksti not in self._io.tulosteet:
            raise AssertionError(
                f"Tulosteessa ei ole riviä {teksti!r}. Tulosteet: {self._io.tulosteet}"
            )
    def tulosteessa_ei_pitaisi_olla(self, teksti):
        if teksti in self._io.tulosteet:
            raise AssertionError(
                f"Tulosteessa ei pitäisi olla riviä {teksti!r}. Tulosteet: {self._io.tulosteet}"
            )
