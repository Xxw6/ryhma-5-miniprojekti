class Viite:
    def __init__(
        self,
        tekijat,
        otsikko,
        vuosi,
        kustantaja=""
    ):
        self.tekijat = tekijat
        self.otsikko = otsikko
        self.vuosi = vuosi
        self.kustantaja = kustantaja
        self.viiteavain = self.muodosta_viiteavain()

    def muodosta_viiteavain(self):
        if "," in self.tekijat:
            sukunimi = self.tekijat.split(",")[0].strip()
        else:
            sukunimi = self.tekijat.split()[-1]

        return self.tarkista_viiteavain(
            f"{sukunimi}{self.vuosi}"
        )

    def tarkista_viiteavain(self, viiteavain):
        if not viiteavain.isalnum():
            raise ValueError(
                "Viiteavain ei saa sisältää välilyöntejä "
                "tai erikoismerkkejä."
            )

        return viiteavain
