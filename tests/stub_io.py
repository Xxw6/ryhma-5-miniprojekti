class StubIO:
    def __init__(self, syotteet):
        self.syotteet = iter(syotteet)
        self.kysymykset = []
        self.tulosteet = []

    def lue(self, kysymys):
        self.kysymykset.append(kysymys)
        try:
            return next(self.syotteet)
        except StopIteration as virhe:
            raise EOFError("StubIO:n testisyötteet loppuivat.") from virhe

    def kirjoita(self, teksti):
        self.tulosteet.append(teksti)