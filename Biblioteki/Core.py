from Biblioteki.BibliotekaMenu2 import MenuInterface
import Biblioteki.FunkcjeWyjscia as fw
from Biblioteki.Neurony import Neuron
import Biblioteki.myFileReader as reader


class Core:

    def __init__(self, parent: MenuInterface, initdata=None, testset=None, alfa=0.05, k=40):
        self.parent = parent

        if initdata is not None:
            self.traindata = reader.readfile(initdata, ";", False)
        else:
            self.traindata = list()

        if testset is not None:
            self.testdata = reader.readfile(testset, ";", False)
        else:
            self.testdata = list()

        self.alfa = float(alfa)
        self.k = int(k)

        self.neurony = dict()

        if initdata is not None and testset is not None:
            self._trenuj(self.k)

        self.parent.changeinfo(str(self))

    def __str__(self):
        return f"Ilość danych treningowych: {len(self.traindata)}\n" \
               f"Ilość danych treningowych: {len(self.testdata)}\n" \
               f"Stała alfa: {self.alfa}\n" \
               f"Ilość powtórzeń uczenia: {self.k}\n" \
               f"Ilość neuronów: {len(self.neurony)}\n"

    def resetuj(self):
        self.neurony.clear()
        self.parent.changeinfo(str(self))
        self.parent.showdata("Neurony zresetowane", important=False)

    def zmienzbiortrenignowy(self):

        sciezka, cancel = self.parent.collectdata("Zmiana zbioru treningowe", "Podaj mi ścieżkę do pliku CSV z danymi"
                                                                              "\n Uwaga! Zmiana zbioru treningowego "
                                                                              "sposowoduje reset "
                                                                              "neuronów!")
        if cancel:
            return

        try:
            self.traindata = reader.readfile(sciezka, ";")
            self.resetuj()
            self.parent.changeinfo(str(self))
        except FileNotFoundError:
            self.parent.showdata("Zmiana zbiotru treningowego nieudana!")

    def zmienzbiortestowy(self):

        sciezka, cancel = self.parent.collectdata("Zmiana zbioru testowego", "Podaj mi ścieżkę do pliku CSV z danymi")
        if cancel:
            return

        try:
            self.testdata = reader.readfile(sciezka, ";")
            self.parent.changeinfo(str(self))
        except FileNotFoundError:
            self.parent.showdata("Zmiana zbiotru testowego nieudana!")

    def zmienalfa(self):
        alpfa, cancel = self.parent.collectdata("Zmiana alpfha", "Podaj mi nowy parametr alfa")

        if cancel:
            return

        try:
            self.alfa = float(alpfa)
            self.parent.showdata("Zmieniono parametr alfa")
            self.parent.changeinfo(str(self))
        except ValueError:
            self.parent.showdata("Niepoprawny paramter alfa")

    def inicjujtrening(self):

        ile, cancel = self.parent.collectdata("Trening", " Ile razy?")
        if cancel:
            return

        self._trenuj(k=int(ile))

        self.parent.showdata(f"Trening ukończony", important=False)
        self.parent.changeinfo(str(self))

    def _trenuj(self, k: int):

        for i in range(0, k):

            for element in self.traindata:
                # dodawanie nowego neuronu po napotkaniu nowej klasy
                if self.neurony.get(element[-1]) is None:
                    self.neurony[element[-1]] = Neuron(wymiary=len(element) - 1, func=fw.sgn, mocnormalizacji=2)

                # korekta wag
                otrzymany = self.wybierz(element[:-1])
                if otrzymany != element[-1]:
                    # testowałem funkcje uczenia i ta jest najbardziej optymalna
                    self.neurony.get(otrzymany).korektawag2(element[:-1], wzmocnij=False)
                    self.neurony.get(element[-1]).korektawag2(element[:-1], wzmocnij=True)

    def wybierz(self, vektor):
        wyniki = dict()
        for neuron in self.neurony:
            wyniki[neuron] = self.neurony.get(neuron).policzwartosc(vektor)
        # print(wyniki)
        wybrany = sorted(wyniki.items(), key=lambda x: x[1])[-1][0]
        # print(f"Wybrany {wybrany}")
        return wybrany

    def _obliczskutecznosc(self, szczegolowe=False):
        trafione = 0
        omylki = {name: {subname: 0 for subname in self.neurony} for name in self.neurony}

        for element in self.testdata:
            wybrany = self.wybierz(element[:-1])
            omylki.get(element[-1])[wybrany] += 1
            if szczegolowe:
                print(f"Oczekiwany: {element[-1]} Otrzymany: {wybrany}")
            if wybrany == element[-1]:
                trafione += 1

        self.parent.drawtable(omylki, "Element\Zaklasyfikowany jako", nazwa="Macierz omyłek sieci")
        return trafione / len(self.testdata)

    def pokazskutecznosc(self):
        skutecznosc = round(self._obliczskutecznosc() * 100, 3)
        self.parent.showdata(f"Skuteczność sieci wynosi: {skutecznosc}%", important=False)

    def pokazneurony(self):
        for neuron in [*self.neurony]:
            print(neuron, self.neurony.get(neuron))

    def ocenjezyk(self):
        wyraz, cancel = self.parent.collectdata("Ocena jezyka", "Napisz mi zdanie w dowolnym języku a ja ocenię jaki "
                                                                "to język\n Można używać wielkich i małych liter jak i"
                                                                "znaków specjalnych które zignoruję im dłuższe zdanie "
                                                                "tym lepiej")
        if cancel or len(wyraz) < 1:
            return

        slownik = {chr(one): 0 for one in range(97, 123)}

        for letter in wyraz:
            try:
                slownik[letter.lower()] += 1
            except KeyError:
                pass

        sumka = sum([liczba[1] for liczba in slownik.items()])
        frequency = [float(liczba[1]) / sumka for liczba in slownik.items()]

        self.parent.showdata(f"Według mnie jest to język : {self.wybierz(frequency)}", important=True)
