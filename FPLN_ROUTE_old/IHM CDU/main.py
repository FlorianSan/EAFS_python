from PyQt5 import QtCore, QtGui, QtWidgets
from menu import Ui_MainWindow
from biblio.fpln import Ui_Dialog as fplnDialog
import classe_segment
from datetime import datetime
from time import strftime
from PyQt5.QtWidgets import QApplication, QPushButton, QFileDialog
import sys




#FPLN
def afficheFpln():
    fpln.show()

def clearall():
    DirInputCancel()
    ToInputCancel()
    for k in range(0,6):
        Liste_Segment[k].Clear()


def save():
    name_fic = str(datetime.today())+".txt"
    fichier = open("Saves/"+name_fic, "x")


    fichier.write(uifpln.DirText.text()+"\n")
    fichier.write(uifpln.ToText.text()+"\n")

    for S in Liste_Segment:
        fichier.write(S.textA.text()+"\n")
        fichier.write(S.textB.text()+"\n")


def open_file_dialog():
    L = [uifpln.DirText, uifpln.ToText, uifpln.Seg1TextA, uifpln.Seg1TextB,
         uifpln.Seg2TextA, uifpln.Seg2TextB,uifpln.Seg3TextA, uifpln.Seg3TextB,
         uifpln.Seg4TextA, uifpln.Seg4TextB,uifpln.Seg5TextA, uifpln.Seg5TextB,
         uifpln.Seg6TextA, uifpln.Seg6TextB]
    c=0
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_name, _ = QFileDialog.getOpenFileName(None, "Sélectionner un fichier", "", "Text Files (*.txt);;All Files (*)", options=options)
    with open(file_name, 'r') as filin:
        lignes = filin.readlines()
        for ligne in lignes:
            if c<14:
                L[c].setText(ligne)
                c=c+1
            else: file_name.close()
    

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


MainWindow.show()

#Les signaux
ui.fpln.clicked.connect(afficheFpln)
ui.quit.clicked.connect(app.quit)


#-----------Fenêtre FPLN-----------#

#Création de la boite de dialogue fpln
fpln = QtWidgets.QDialog()
uifpln = fplnDialog()
uifpln.setupUi(fpln)

uifpln.BackButton.clicked.connect(fpln.close)
uifpln.Clear_Button.clicked.connect(clearall)
uifpln.Save_Button.clicked.connect(save)
uifpln.Open_Button.clicked.connect(lambda: open_file_dialog())

#-----Aéroport de départ et d'arrivée----"

            
def DirInputOk():
    if uifpln.DirText.text() != "":
        print(uifpln.DirText.text())
        uifpln.DirText.setReadOnly(True)
        uifpln.icone.setVisible(True)
    else: uifpln.OutputText.setText("Error DIR input")

def DirInputCancel():
    uifpln.DirText.clear()
    uifpln.DirText.setReadOnly(False)
    uifpln.icone.setVisible(False)

def ToInputOk():
    if uifpln.ToText.text() != "":
        print(uifpln.ToText.text())
        uifpln.ToText.setReadOnly(True)
        uifpln.icone_2.setVisible(True)
    else: uifpln.OutputText.setText("Error TO input")

def ToInputCancel():
    uifpln.ToText.clear()
    uifpln.ToText.setReadOnly(False)
    uifpln.icone_2.setVisible(False)


uifpln.DirBox.accepted.connect(DirInputOk)
uifpln.DirBox.rejected.connect(DirInputCancel)

uifpln.ToBox.accepted.connect(ToInputOk)
uifpln.ToBox.rejected.connect(ToInputCancel)


#-----WPT/AIRWAYS----#

S1 = classe_segment.Segment(1, uifpln, uifpln.Seg1TextA, uifpln.Seg1TextB, uifpln.icone_3)
S2 = classe_segment.Segment(2, uifpln, uifpln.Seg2TextA, uifpln.Seg2TextB, uifpln.icone_4)
S3 = classe_segment.Segment(3, uifpln, uifpln.Seg3TextA, uifpln.Seg3TextB, uifpln.icone_5)
S4 = classe_segment.Segment(4, uifpln, uifpln.Seg4TextA, uifpln.Seg4TextB, uifpln.icone_6)
S5 = classe_segment.Segment(5, uifpln, uifpln.Seg5TextA, uifpln.Seg5TextB, uifpln.icone_7)
S6 = classe_segment.Segment(6, uifpln, uifpln.Seg6TextA, uifpln.Seg6TextB, uifpln.icone_8)

Liste_Segment= [S1, S2, S3, S4, S5, S6]

uifpln.Seg1Box.accepted.connect(lambda: S1.InputOk())
uifpln.Seg1Box.accepted.connect(lambda: S2.shownext())
uifpln.Seg1Box.rejected.connect(lambda: S1.Clear())

uifpln.Seg2Box.accepted.connect(lambda: S2.InputOk())
uifpln.Seg2Box.rejected.connect(lambda: S2.Clear())

uifpln.Seg3Box.accepted.connect(lambda: S3.InputOk())
uifpln.Seg3Box.rejected.connect(lambda: S3.Clear())

uifpln.Seg4Box.accepted.connect(lambda: S4.InputOk())
uifpln.Seg4Box.rejected.connect(lambda: S4.Clear())

uifpln.Seg5Box.accepted.connect(lambda: S5.InputOk())
uifpln.Seg5Box.rejected.connect(lambda: S5.Clear())

uifpln.Seg6Box.accepted.connect(lambda: S6.InputOk())
uifpln.Seg6Box.rejected.connect(lambda: S6.Clear())

sys.exit(app.exec_())
