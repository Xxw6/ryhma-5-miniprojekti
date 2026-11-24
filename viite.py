class Viite:
    def __init__(
        self,
        tekijat,
        otsikko,
        vuosi,
        kustantaja="",
        viiteavain=None
    ):
        self.tekijat = tekijat
        self.otsikko = otsikko
        self.vuosi = vuosi
        self.kustantaja = kustantaja

        if viiteavain:
            self.viiteavain = self.tarkista_viiteavain(viiteavain)
        else:
            self.viiteavain = self.muodosta_viiteavain()

    def tarkista_viiteavain(self, viiteavain):
        viiteavain = viiteavain.strip()

        if not viiteavain:
            raise ValueError("Viiteavain ei saa olla tyhjä.")

        if not viiteavain.isalnum():
            raise ValueError(
                "Viiteavain ei saa sisältää välilyöntejä "
                "tai erikoismerkkejä."
            )

        return viiteavain

    def muodosta_viiteavain(self):
        if "," in self.tekijat:
            sukunimi = self.tekijat.split(",")[0].strip()
        else:
            sukunimi = self.tekijat.split()[-1]

        sukunimi = sukunimi.replace("-", "")

        return self.tarkista_viiteavain(
            f"{sukunimi}{self.vuosi}"
        )
