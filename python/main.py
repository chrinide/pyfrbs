#!/usr/bin/env python

import sys
import psycopg2

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self, *args):
        super(Window, self).__init__(*args)

        loadUi('main.ui', self)

        self.loadVariables()

        self.uiVariablesCombo.currentIndexChanged.connect(self.onVariableSelected)
        self.uiCreateVariableButton.clicked.connect(self.onCreateVariableClicked)
        self.uiDeleteVariableButton.clicked.connect(self.onDeleteVariableClicked)

        self.uiRangeMinEdit.textEdited.connect(self.onRangeChanged)
        self.uiRangeMaxEdit.textEdited.connect(self.onRangeChanged)
        self.uiRangeMinEdit.setValidator(QDoubleValidator(-100, 100, 2, self.uiRangeMinEdit))
        self.uiRangeMaxEdit.setValidator(QDoubleValidator(-100, 100, 2, self.uiRangeMaxEdit))

        self.uiTermsCombo.currentIndexChanged.connect(self.onTermSelected)
        self.uiAddTermButton.clicked.connect(self.onAddTermClicked)
        self.uiTermsList.clicked.connect(self.onVariableTermSelected)
        self.uiRemoveTermButton.clicked.connect(self.onRemoveTermClicked)

        self.uiHedgesCombo.currentTextChanged.connect(self.onHedgeSelected)
        self.uiAddHedgeButton.clicked.connect(self.onAddHedgeClicked)
        self.uiHedgesList.clicked.connect(self.onVariableHedgeSelected)
        self.uiRemoveHedgeButton.clicked.connect(self.onRemoveHedgeClicked)

        self.uiCommitVariableButton.clicked.connect(self.commitVariable)

    def loadVariables(self):
        self.uiVariablesCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT name FROM variable;')
        for item in cur.fetchall():
            self.uiVariablesCombo.addItem(item[0])
        cur.close()
        self.uiVariablesCombo.setCurrentIndex(-1)

    def loadAllTerms(self):
        self.uiTermsCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM term;')
        for item in cur.fetchall():
            self.uiTermsCombo.addItem(item[0])
        cur.close()
        self.uiTermsCombo.setCurrentIndex(-1)
        self.uiAddTermButton.setEnabled(False)

    def loadAllHedges(self):
        self.uiHedgesCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM hedge;')
        for item in cur.fetchall():
            self.uiHedgesCombo.addItem(item[0])
        cur.close()
        self.uiHedgesCombo.setCurrentIndex(-1)
        self.uiAddHedgeButton.setEnabled(False)

    def onVariableSelected(self):
        if (self.uiVariablesCombo.isEditable() == True):
            return

        if (self.uiVariablesCombo.currentIndex() == -1):
            self.uiRenameVariableButton.setEnabled(False)
            self.uiDeleteVariableButton.setEnabled(False)
            self.uiRangeMinEdit.setEnabled(False)
            self.uiRangeMaxEdit.setEnabled(False)
            self.uiTermsCombo.setEnabled(False)
            self.uiTermsList.setEnabled(False)
            self.uiHedgesCombo.setEnabled(False)
            self.uiHedgesList.setEnabled(False)
            return

        self.uiTermsList.clear()
        cur = conn.cursor()
        cur.execute('SELECT term.value FROM variable, term, variable_term WHERE variable.name = %s AND variable.id = variable_term.variable_id AND term.id = variable_term.term_id;', (self.uiVariablesCombo.currentText(),))
        for item in cur.fetchall():
            self.uiTermsList.addItem(item[0])
        cur.close()
        self.loadAllTerms()

        self.uiHedgesList.clear()
        cur = conn.cursor()
        cur.execute('SELECT hedge.value FROM variable, hedge, variable_hedge WHERE variable.name = %s AND variable.id = variable_hedge.variable_id AND hedge.id = variable_hedge.hedge_id;', (self.uiVariablesCombo.currentText(),))
        for item in cur.fetchall():
            self.uiHedgesList.addItem(item[0])
        cur.close()
        self.loadAllHedges()

        cur = conn.cursor()
        cur.execute('SELECT variable.min, variable.max FROM variable WHERE variable.name = %s;', (self.uiVariablesCombo.currentText(),))
        range = cur.fetchone()
        if (range):
            self.uiRangeMinEdit.setText('%s' % range[0])
            self.uiRangeMaxEdit.setText('%s' % range[1])
        else:
            self.uiRangeMinEdit.clear()
            self.uiRangeMaxEdit.clear()

        self.uiRenameVariableButton.setEnabled(True)
        self.uiDeleteVariableButton.setEnabled(True)
        self.uiRangeMinEdit.setEnabled(True)
        self.uiRangeMaxEdit.setEnabled(True)
        self.uiTermsCombo.setEnabled(True)
        self.uiTermsList.setEnabled(True)
        self.uiRemoveTermButton.setEnabled(False)
        self.uiHedgesCombo.setEnabled(True)
        self.uiHedgesList.setEnabled(True)
        self.uiRemoveHedgeButton.setEnabled(False)
        self.uiCommitVariableButton.setEnabled(False)

    def onTermSelected(self):
        self.uiAddTermButton.setEnabled(True)

    def onVariableTermSelected(self):
        self.uiRemoveTermButton.setEnabled(True)

    def onAddTermClicked(self):
        if (not self.uiTermsList.findItems(self.uiTermsCombo.currentText(), Qt.MatchExactly)):
            self.uiTermsList.addItem(self.uiTermsCombo.currentText())
            self.uiCommitVariableButton.setEnabled(True)

    def onRemoveTermClicked(self):
        self.uiTermsList.takeItem(self.uiTermsList.currentRow())
        if (self.uiTermsList.count() == 0):
            self.uiRemoveTermButton.setEnabled(False)
        self.uiCommitVariableButton.setEnabled(True)

    def onHedgeSelected(self):
        self.uiAddHedgeButton.setEnabled(True)

    def onVariableHedgeSelected(self):
        self.uiRemoveHedgeButton.setEnabled(True)

    def onAddHedgeClicked(self):
        if (not self.uiHedgesList.findItems(self.uiHedgesCombo.currentText(), Qt.MatchExactly)):
            self.uiHedgesList.addItem(self.uiHedgesCombo.currentText())
            self.uiCommitVariableButton.setEnabled(True)

    def onRemoveHedgeClicked(self):
        self.uiHedgesList.takeItem(self.uiHedgesList.currentRow())
        if (self.uiHedgesList.count() == 0):
            self.uiRemoveHedgeButton.setEnabled(False)
        self.uiCommitVariableButton.setEnabled(True)

    def onCreateVariableClicked(self):
        self.uiVariablesCombo.setCurrentIndex(-1)
        self.uiVariablesCombo.setEditable(True)
        self.uiVariablesCombo.lineEdit().returnPressed.connect(self.onVariableEntered)
        self.uiVariablesCombo.setFocus()
        self.uiCreateVariableButton.setEnabled(False)

    def onVariableEntered(self):
        self.uiVariablesCombo.setEditable(False)
        self.uiCreateVariableButton.setEnabled(True)
        self.onVariableSelected()

    def onDeleteVariableClicked(self):
        self.uiRangeMinEdit.clear()
        self.uiRangeMaxEdit.clear()
        self.uiVariablesCombo.removeItem(self.uiVariablesCombo.currentIndex())

    def onRangeChanged(self):
        self.uiCommitVariableButton.setEnabled(True)

    def commitVariable(self):
        self.uiCommitVariableButton.setEnabled(False)

if __name__ == "__main__":
    conn = psycopg2.connect(host='10.0.0.1', database='fuzzy', user='user1', password='pass1')
    app = QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())
    conn.close()
