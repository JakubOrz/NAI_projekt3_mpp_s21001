import sys

from PyQt5.QtWidgets import QApplication
from Biblioteki.BibliotekaMenu2 import ButtonMenu
from Biblioteki.Core import Core

app = QApplication(sys.argv)

okno = ButtonMenu(name="Siec neuronowa v1 by s21001")
if len(sys.argv) == 5:
    rdzen = Core(okno, initdata=sys.argv[1], testset=sys.argv[2], alfa=float(sys.argv[3]), k=int(sys.argv[4]))
else:
    rdzen = Core(okno)

okno.addbutton("Trenuj jeszcze", rdzen.inicjujtrening)
okno.addbutton("Pokaz wagi neuronów", rdzen.pokazneurony)
okno.addbutton("Pokaz skutecznosc", rdzen.pokazskutecznosc)
okno.addbutton("Wyszukaj język w zdaniu", rdzen.ocenjezyk)
okno.addbutton("Resetuj neurony", rdzen.resetuj)
okno.addbutton("Wyczyść tabelke", okno.clear)
okno.addbutton("Zmiana zbioru treningowego", rdzen.zmienzbiortrenignowy)
okno.addbutton("Zmiana zbioru treningowego", rdzen.zmienzbiortestowy)
okno.addbutton("Zmiana parametru alfa", rdzen.zmienalfa)

app.exec_()
