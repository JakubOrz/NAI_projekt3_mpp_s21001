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

        self.parent.changeinfo(str(self))

    def __str__(self):
        return f"Ilość danych treningowych: {len(self.traindata)}\n" \
               f"Ilość danych treningowych: {len(self.testdata)}\n" \
               f"Stała alfa: {self.alfa}\n" \
               f"Ilość powtórzeń uczenia: {self.k}\n" \
               f"Ilość neuronów: {len(self.neurony)}\n"

    def testowa(self):
        neuron1 = Neuron(wymiary=4, alfa=self.alfa, func=fw.sgn)
        v1 = [3, 4, 2, 1]
        print(neuron1.policzwartosc(v1))

    def resetuj(self):
        self.neurony.clear()
        self.parent.changeinfo(str(self))
        self.parent.showdata("Neurony zresetowane", important=False)

    def wypiszdane(self):
        for element in self.traindata:
            print(element)

    def trenuj(self):

        ile, cancel = self.parent.collectdata("Trening", " Ile razy?")
        if cancel:
            return

        skutecznosc = dict()
        for i in range(0, int(ile)):

            for element in self.traindata:
                # dodawanie nowego neuronu po napotkaniu nowej klasy
                if self.neurony.get(element[-1]) is None:
                    self.neurony[element[-1]] = Neuron(wymiary=len(element) - 1, func=fw.sgn)

                # korekta wag
                otrzymany = self.wybierz(element[:-1])
                if otrzymany != element[-1]:
                    #testowałem funkcje uczenia i ta jest najbardziej optymalna
                    self.neurony.get(otrzymany).korektawag2(element[:-1], wzmocnij=False)
                    self.neurony.get(element[-1]).korektawag2(element[:-1], wzmocnij=True)

            skutecznosc[i] = self.obliczskutecznosc(False)
        czywykres = self.parent.askquestion("Skutecznosc ", "Czy narysować wykres skuteczności w zależności od tury?")
        if czywykres:
            self.parent.drawplot(skutecznosc, "Skutecznosc", "Tura", "Skutecznosc")
        self.parent.showdata(f"Trening ukończony", important=False)
        self.parent.changeinfo(str(self))

    def wybierz(self, vektor):
        wyniki = dict()
        for neuron in self.neurony:
            wyniki[neuron] = self.neurony.get(neuron).policzwartosc(vektor)
        # print(wyniki)
        wybrany = sorted(wyniki.items(), key=lambda x: x[1])[-1][0]
        # print(f"Wybrany {wybrany}")
        return wybrany

    def obliczskutecznosc(self, glosno=False):
        trafione = 0
        for element in self.traindata:
            wybrany = self.wybierz(element[:-1])
            # print(f"Oczekiwany: {element[-1]} Otrzymany: {wybrany}")
            if wybrany == element[-1]:
                trafione += 1
        if glosno:
            self.parent.showdata(f"Skuteczność wynosi: {trafione / len(self.traindata)}")
        else:
            return trafione / len(self.traindata)

    def pokazneurony(self):
        for neuron in [*self.neurony]:
            print(neuron, self.neurony.get(neuron))
