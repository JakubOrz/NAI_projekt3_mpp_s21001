from Biblioteki import MathLib


class Neuron:
    def __init__(self, wymiary=3, alfa=0.01, func=None):
        self.wagi = [0] * wymiary
        self.prog = 0
        self.alfa = alfa
        self.activationfunc = func

    def __str__(self):
        return str(self.wagi)

    def policzwartosc(self, vektor: list):
        return self.activationfunc(MathLib.iloczynskalarny(self.wagi, vektor))

    # def korektawag(self, vektor: list, y: int = 0, d: int = 0, ):
    #     if len(vektor) != len(self.wagi):
    #         raise ValueError("Niedopasowane długości wektorów")
    #
    #     L = self.alfa
    #     self.wagi = [float(stare) + (d - y) * L * float(nowy) for stare, nowy in
    #                  zip(self.wagi, MathLib.normalizuj(vektor))]
    #     self.wagi = MathLib.normalizuj(self.wagi)

    def korektawag2(self, vektor, wzmocnij: bool = True):
        if len(vektor) != len(self.wagi):
            raise ValueError("Niedopasowane długości wektorów")

        d = 1 if wzmocnij else -1
        L = self.alfa
        self.wagi = [float(stare) + (d * L * float(nowy)) for stare, nowy in
                     zip(self.wagi, MathLib.normalizuj(vektor))]
        self.wagi = MathLib.normalizuj(self.wagi)
