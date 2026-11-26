from viite import Viite


class ViitePalvelu:
    def __init__(self, varasto):
        self.varasto = varasto

    def _validoi_tiedot(self, tiedot, pakolliset):
        tiedot = {
            avain: arvo.strip()
            for avain, arvo in tiedot.items()
        }

        if not all(tiedot.get(avain) for avain in pakolliset):
            raise ValueError("Täytä kaikki pakolliset kentät.")

        try:
            vuosi = int(tiedot["vuosi"])
        except ValueError as virhe:
            raise ValueError(
                "Vuoden pitää olla kokonaisluku 1–9999."
            ) from virhe

        if not 1 <= vuosi <= 9999:
            raise ValueError("Vuoden pitää olla kokonaisluku 1–9999.")

        tiedot["vuosi"] = vuosi
        return tiedot

    def _muodosta_viiteavain(self, viite):
        olemassa_olevat = {
            teos["viiteavain"]
            for teos in self.varasto.listaa_teokset()
        }

        perusavain = viite.viiteavain
        suffiksi = 0

        while True:
            liite = ""
            numero = suffiksi

            while numero > 0:
                numero, jaannos = divmod(numero - 1, 26)
                liite = chr(ord("a") + jaannos) + liite

            viiteavain = f"{perusavain}{liite}"

            if viiteavain not in olemassa_olevat:
                return viiteavain

            suffiksi += 1

    def _tallenna_viite(self, tiedot, tyyppi):
        viite = Viite(
            tiedot["tekijat"],
            tiedot["otsikko"],
            tiedot["vuosi"],
            tiedot.get("kustantaja", ""),
            tiedot.get("viiteavain")
        )

        if tiedot.get("viiteavain", "").strip():
            viiteavain = viite.viiteavain
            olemassa_olevat = {
                teos["viiteavain"]
                for teos in self.varasto.listaa_teokset()
            }

            if viiteavain in olemassa_olevat:
                raise ValueError("Viiteavain on jo käytössä.")
        else:
            viiteavain = self._muodosta_viiteavain(viite)

        tiedot["viiteavain"] = viiteavain
        if tyyppi == "book":
            self.varasto.lisaa_teos(tiedot)
        else:
            self.varasto.lisaa_artikkeli(tiedot)

        return viiteavain

    def lisaa_teos(self, teos):
        teos.setdefault("kustantaja", "")

        teos = self._validoi_tiedot(
            teos,
            ("tekijat", "otsikko", "vuosi")
        )

        return self._tallenna_viite(teos, "book")

    def lisaa_artikkeli(self, artikkeli):
        artikkeli.setdefault("volume", "")
        artikkeli.setdefault("pages", "")

        artikkeli = self._validoi_tiedot(
            artikkeli,
            ("tekijat", "otsikko", "journal", "vuosi")
        )

        return self._tallenna_viite(artikkeli, "article")

    def poista_viite(self, viiteavain):
        viiteavain = viiteavain.strip()
        if not viiteavain:
            raise ValueError("Anna poistettavan viitteen viiteavain.")
        if not self.varasto.poista_viite(viiteavain):
            raise ValueError(f"Viiteavainta {viiteavain} ei löytynyt.")

    def listaa_teokset(self):
        return self.varasto.listaa_teokset()

    def listaa_artikkelit(self):
        return self.varasto.listaa_artikkelit()
