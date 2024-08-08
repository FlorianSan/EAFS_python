from PyQt5 import QtCore, QtGui, QtWidgets
from menu import Ui_MainWindow
from biblio.fpln import Ui_Dialog as fplnDialog
#from biblio.ready import Ui_Dialog as readyDialog
#from biblio.init import Ui_Dialog as ...

import sys


import sys

#FPLN
def afficheFpln():
    fpln.show()


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


MainWindow.show()

#Les signaux
ui.fpln.clicked.connect(afficheFpln)
ui.quit.clicked.connect(app.quit)


#-----------Fenêtre FPLN-----------#
DIR = ""
TO = ""
SEG1 = ""
SEG2 = ""
#Création de la boite de dialogue fpln
fpln = QtWidgets.QDialog()
uifpln = fplnDialog()
uifpln.setupUi(fpln)

uifpln.BackButton.clicked.connect(fpln.close)

#-----Aéroport de départ et d'arrivée----"


def DirInputOk():
    if uifpln.DirText.text() != "":
        print(uifpln.DirText.text())
        DIR = uifpln.DirText.text()
        uifpln.DirText.setReadOnly(True)
        uifpln.icone.setVisible(True)
    else: uifpln.OutputText.setText("Error DIR input")

def DirInputCancel():
    uifpln.DirText.clear()
    DIR = ""
    uifpln.DirText.setReadOnly(False)
    uifpln.icone.setVisible(False)

def ToInputOk():
    if uifpln.ToText.text() != "":
        print(uifpln.ToText.text())
        TO = uifpln.ToText.text()
        uifpln.ToText.setReadOnly(True)
        uifpln.icone_2.setVisible(True)
    else: uifpln.OutputText.setText("Error TO input")

def ToInputCancel():
    uifpln.ToText.clear()
    TO = ""
    uifpln.ToText.setReadOnly(False)
    uifpln.icone_2.setVisible(False)


uifpln.DirBox.accepted.connect(DirInputOk)
uifpln.DirBox.rejected.connect(DirInputCancel)

uifpln.ToBox.accepted.connect(ToInputOk)
uifpln.ToBox.rejected.connect(ToInputCancel)


#-----WPT/AIRWAYS----#

#Segment 1

def Seg1InputOk():
    print(uifpln.Seg1TextA.text())
    print(uifpln.Seg1TextB.text())
    uifpln.Seg1TextA.setReadOnly(True)
    uifpln.Seg1TextB.setReadOnly(True)
    uifpln.icone_3.setVisible(True)

def Seg1InputCancel():
    uifpln.Seg1TextA.clear()
    uifpln.Seg1TextB.clear()
    uifpln.Seg1TextA.setReadOnly(False)
    uifpln.Seg1TextB.setReadOnly(False)
    uifpln.icone_4.setVisible(False)

uifpln.Seg1Box.accepted.connect(Seg1InputOk)
uifpln.Seg1Box.rejected.connect(Seg1InputCancel)




#Segment 2

def Seg2InputOk():
    print(uifpln.Seg2TextA.text())
    print(uifpln.Seg2TextB.text())
    uifpln.Seg2TextA.setReadOnly(True)
    uifpln.Seg2TextB.setReadOnly(True)
    uifpln.icone_4.setVisible(True)

def Seg2InputCancel():
    uifpln.Seg2TextA.clear()
    uifpln.Seg2TextB.clear()
    uifpln.Seg2TextA.setReadOnly(False)
    uifpln.Seg2TextB.setReadOnly(False)
    uifpln.icone_4.setVisible(False)

uifpln.Seg2Box.accepted.connect(Seg2InputOk)
uifpln.Seg2Box.rejected.connect(Seg2InputCancel)

#Segment 3

def Seg3InputOk():
    print(uifpln.Seg3TextA.text())
    print(uifpln.Seg3TextB.text())
    uifpln.Seg3TextA.setReadOnly(True)
    uifpln.Seg3TextB.setReadOnly(True)
    uifpln.icone_5.setVisible(True)

def Seg3InputCancel():
    uifpln.Seg3TextA.clear()
    uifpln.Seg3TextB.clear()
    uifpln.Seg3TextA.setReadOnly(False)
    uifpln.Seg3TextB.setReadOnly(False)
    uifpln.icone_5.setVisible(False)

uifpln.Seg3Box.accepted.connect(Seg3InputOk)
uifpln.Seg3Box.rejected.connect(Seg3InputCancel)

#Segment 4

def Seg4InputOk():
    print(uifpln.Seg4TextA.text())
    print(uifpln.Seg4TextB.text())
    uifpln.Seg4TextA.setReadOnly(True)
    uifpln.Seg4TextB.setReadOnly(True)
    uifpln.icone_6.setVisible(True)

def Seg4InputCancel():
    uifpln.Seg4TextA.clear()
    uifpln.Seg4TextB.clear()
    uifpln.Seg4TextA.setReadOnly(False)
    uifpln.Seg4TextB.setReadOnly(False)
    uifpln.icone_6.setVisible(False)

uifpln.Seg4Box.accepted.connect(Seg4InputOk)
uifpln.Seg4Box.rejected.connect(Seg4InputCancel)

#Segment 5

def Seg5InputOk():
    print(uifpln.Seg5TextA.text())
    print(uifpln.Seg5TextB.text())
    uifpln.Seg5TextA.setReadOnly(True)
    uifpln.Seg5TextB.setReadOnly(True)
    uifpln.icone_7.setVisible(True)

def Seg5InputCancel():
    uifpln.Seg5TextA.clear()
    uifpln.Seg5TextB.clear()
    uifpln.Seg5TextA.setReadOnly(False)
    uifpln.Seg5TextB.setReadOnly(False)
    uifpln.icone_7.setVisible(False)

uifpln.Seg5Box.accepted.connect(Seg5InputOk)
uifpln.Seg5Box.rejected.connect(Seg5InputCancel)

#Segment 6

def Seg6InputOk():
    print(uifpln.Seg6TextA.text())
    print(uifpln.Seg6TextB.text())
    uifpln.Seg6TextA.setReadOnly(True)
    uifpln.Seg6TextB.setReadOnly(True)
    uifpln.icone_8.setVisible(True)

def Seg6InputCancel():
    uifpln.Seg6TextA.clear()
    uifpln.Seg6TextB.clear()
    uifpln.Seg6TextA.setReadOnly(False)
    uifpln.Seg6TextB.setReadOnly(False)
    uifpln.icone_8.setVisible(False)

uifpln.Seg6Box.accepted.connect(Seg6InputOk)
uifpln.Seg6Box.rejected.connect(Seg6InputCancel)




sys.exit(app.exec_())
