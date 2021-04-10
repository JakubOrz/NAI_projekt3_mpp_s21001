import sys

from PyQt5.QtWidgets import QApplication
from Biblioteki.BibliotekaMenu2 import ButtonMenu
from Biblioteki.Core import Core

app = QApplication(sys.argv)

okno = ButtonMenu(name="Perceptron 2 by s21001")
if len(sys.argv) == 2:
    rdzen = Core(okno, sys.argv[1])
else:
    rdzen = Core(okno)

okno.addbutton("Testuj", rdzen.testowa)
okno.addbutton("Wypisz Dane", rdzen.wypiszdane)
okno.addbutton("Trenuj", rdzen.trenuj)
okno.addbutton("Pokaz", rdzen.pokazneurony)
okno.addbutton("Skutecznosc", rdzen.obliczskutecznosc)
okno.addbutton("Resetuj neurony", rdzen.resetuj)

app.exec_()
