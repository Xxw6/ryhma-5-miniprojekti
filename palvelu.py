from viite import Viite


class ViitePalvelu:
    def __init__(self, varasto):
        self.varasto = varasto


    def lisaa_teos(self, teos):
        teos = {avain: arvo.strip() for avain, arvo in teos.items()}
        teos.setdefault("kustantaja", "")

        pakolliset = ("tekijat", "otsikko", "vuosi")
        if not all(teos.get(avain) for avain in pakolliset):
            raise ValueError("Täytä kaikki pakolliset kentät.")

        try:
            vuosi = int(teos["vuosi"])
        except ValueError as virhe:
            raise ValueError(
                "Vuoden pitää olla kokonaisluku 1–9999."
            ) from virhe

        if not 1 <= vuosi <= 9999:
            raise ValueError("Vuoden pitää olla kokonaisluku 1–9999.")

        teos["vuosi"] = vuosi

        viite = Viite(
            teos["tekijat"],
            teos["otsikko"],
            vuosi,
            teos["kustantaja"]
        )

        perusavain = viite.viiteavain
        viiteavain = perusavain
        kirjain = ord("a")

        olemassa_olevat = {
            t["viiteavain"] for t in self.varasto.listaa_teokset()
        }

        while viiteavain in olemassa_olevat:
            viiteavain = f"{perusavain}{chr(kirjain)}"
            kirjain += 1

        teos["viiteavain"] = viiteavain

        self.varasto.lisaa_teos(teos)
        return viiteavain


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

    def hae_viitteet(self, tekija="", vuosi="", julkaisu=""):
        tekija = str(tekija or "").strip().casefold()
        vuosi = str(vuosi or "").strip()
        julkaisu = str(julkaisu or "").strip().casefold()

        if not any((tekija, vuosi, julkaisu)):
            raise ValueError("Anna vähintään yksi hakuehto.")

        if vuosi:
            try:
                vuosi = int(vuosi)
            except ValueError as virhe:
                raise ValueError(
                    "Vuoden pitää olla kokonaisluku 1–9999."
                ) from virhe

            if not 1 <= vuosi <= 9999:
                raise ValueError(
                    "Vuoden pitää olla kokonaisluku 1–9999."
                )

        viitteet = self.varasto.listaa_teokset()
        tulokset = []

        for viite in viitteet:
            if tekija and tekija not in viite["tekijat"].casefold():
                continue

            if vuosi and viite["vuosi"] != vuosi:
                continue

            julkaisutiedot = " ".join((
                viite.get("kustantaja") or "",
                viite.get("journal") or ""
            )).casefold()

            if julkaisu and julkaisu not in julkaisutiedot:
                continue

            tulokset.append(viite)

        return tulokset
