from viite import Viite


class ViitePalvelu:
    def __init__(self, varasto):
        self.varasto = varasto

    def lisaa_teos(self, teos):
        teos = {
            avain: arvo.strip()
            for avain, arvo in teos.items()
        }

        if not all(teos.values()):
            raise ValueError("Täytä kaikki kentät.")

        try:
            vuosi = int(teos["vuosi"])
        except ValueError as virhe:
            raise ValueError(
                "Vuoden pitää olla kokonaisluku 1–9999."
            ) from virhe

        if not 1 <= vuosi <= 9999:
            raise ValueError(
                "Vuoden pitää olla kokonaisluku 1–9999."
            )

        viite = Viite(
            tekijat=teos["tekijat"],
            otsikko=teos["otsikko"],
            vuosi=vuosi
        )

        teos["vuosi"] = vuosi
        teos["viiteavain"] = viite.viiteavain

        self.varasto.lisaa_teos(teos)

    def listaa_teokset(self):
        return self.varasto.listaa_teokset()
