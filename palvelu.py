class ViitePalvelu:
    def __init__(self, varasto):
        self.varasto = varasto

    def lisaa_teos(self, teos):
        teos = {avain: arvo.strip() for avain, arvo in teos.items()}
        if not all(teos.values()):
            raise ValueError("Täytä kaikki kentät.")
        try:
            vuosi = int(teos["vuosi"])
        except ValueError as virhe:
            raise ValueError("Vuoden pitää olla kokonaisluku 1–9999.") from virhe
        if not 1 <= vuosi <= 9999:
            raise ValueError("Vuoden pitää olla kokonaisluku 1–9999.")
        teos["vuosi"] = vuosi
        self.varasto.lisaa_teos(teos)

    def lisaa_artikkeli(self, artikkeli):
        artikkeli = {
            avain: arvo.strip()
            for avain, arvo in artikkeli.items()
        }

        pakolliset = (
            "viiteavain",
            "tekijat",
            "otsikko",
            "journal",
            "vuosi",
        )

        if not all(artikkeli.get(avain) for avain in pakolliset):
            raise ValueError("Täytä kaikki pakolliset kentät.")

        try:
            vuosi = int(artikkeli["vuosi"])
        except ValueError as virhe:
            raise ValueError(
                "Vuoden pitää olla kokonaisluku 1–9999."
            ) from virhe

        if not 1 <= vuosi <= 9999:
            raise ValueError(
                "Vuoden pitää olla kokonaisluku 1–9999."
            )

        artikkeli["vuosi"] = vuosi

        artikkeli.setdefault("volume", "")
        artikkeli.setdefault("pages", "")

        self.varasto.lisaa_artikkeli(artikkeli)


    def listaa_teokset(self):
        return self.varasto.listaa_teokset()

    def listaa_artikkelit(self):
        return self.varasto.listaa_artikkelit()
