from PyQt5 import QtCore, QtGui, QtWidgets
from menu import Ui_MainWindow
from biblio.fpln import Ui_Dialog as fplnDialog


class Segment:
   
    def __init__(self, numero, uifpln, textA, textB, icone):

        self.numero = numero
        self.uifpln= uifpln
        self.textA = textA
        self.textB = textB
        self.icone = icone
   
    
    def InputOk(self):
        print("clique")
        if (self.textA.text()!="") and (self.textB.text() !=""):
            print(self.textA.text())
            print(self.textB.text())
            self.textA.setReadOnly(True)
            self.textB.setReadOnly(True)
            self.icone.setVisible(True)
        else: self.uifpln.OutputText.setText("Error on segment n°"+str(self.numero))
    
    def Clear(self):
        self.textA.clear()
        self.textB.clear()
        self.textA.setReadOnly(False)
        self.textB.setReadOnly(False)
        self.icone.setVisible(False)

    def shownext(self):
        print("hi")


        
        
        
