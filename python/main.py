#!/usr/bin/env python

import sys
import psycopg2

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self, *args):
        super(Window, self).__init__(*args)
        loadUi('main.ui', self)
        self.loadVariables()
        self.variables.currentIndexChanged.connect(self.onVariableSelected)
        self.terms.currentIndexChanged.connect(self.onTermSelected)
        self.add_term.clicked.connect(self.onAddTermClicked)
        self.remove_term.clicked.connect(self.onRemoveTermClicked)
        self.variable_terms.clicked.connect(self.onVariableTermSelected)
        self.hedges.currentTextChanged.connect(self.onHedgeSelected)
        self.add_hedge.clicked.connect(self.onAddHedgeClicked)
        self.remove_hedge.clicked.connect(self.onRemoveHedgeClicked)
        self.variable_hedges.clicked.connect(self.onVariableHedgeSelected)

    def loadVariables(self):
        self.variables.clear()
        cur = conn.cursor()
        cur.execute('SELECT name FROM variable;')
        for item in cur.fetchall():
            self.variables.addItem(item[0])
        cur.close()
        self.variables.setCurrentIndex(-1)

    def loadAllTerms(self):
        self.terms.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM term;')
        for item in cur.fetchall():
            self.terms.addItem(item[0])
        cur.close()
        self.terms.setCurrentIndex(-1)
        self.add_term.setEnabled(False)

    def loadAllHedges(self):
        self.hedges.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM hedge;')
        for item in cur.fetchall():
            self.hedges.addItem(item[0])
        cur.close()
        self.hedges.setCurrentIndex(-1)
        self.add_hedge.setEnabled(False)

    def onVariableSelected(self):

        self.variable_terms.setEnabled(True)
        self.variable_terms.clear()
        cur = conn.cursor()
        cur.execute('SELECT term.value FROM variable, term, variable_term WHERE variable.name = %s AND variable.id = variable_term.variable_id AND term.id = variable_term.term_id;', (self.variables.currentText(),))
        for item in cur.fetchall():
            self.variable_terms.addItem(item[0])
        cur.close()
        self.loadAllTerms()
        self.terms.setEnabled(True)
        self.remove_term.setEnabled(False)

        self.variable_hedges.setEnabled(True)
        self.variable_hedges.clear()
        cur = conn.cursor()
        cur.execute('SELECT hedge.value FROM variable, hedge, variable_hedge WHERE variable.name = %s AND variable.id = variable_hedge.variable_id AND hedge.id = variable_hedge.hedge_id;', (self.variables.currentText(),))
        for item in cur.fetchall():
            self.variable_hedges.addItem(item[0])
        cur.close()
        self.loadAllHedges()
        self.hedges.setEnabled(True)
        self.remove_hedge.setEnabled(False)
       
    def onTermSelected(self):
        self.add_term.setEnabled(True)

    def onVariableTermSelected(self):
        self.remove_term.setEnabled(True)

    def onAddTermClicked(self):
        self.variable_terms.addItem(self.terms.currentText())

    def onRemoveTermClicked(self):
        self.variable_terms.takeItem(self.variable_terms.currentRow())
        if (self.variable_terms.count() == 0):
            self.remove_term.setEnabled(False)

    def onHedgeSelected(self):
        self.add_hedge.setEnabled(True)

    def onVariableHedgeSelected(self):
        self.remove_hedge.setEnabled(True)

    def onAddHedgeClicked(self):
        self.variable_hedges.addItem(self.hedges.currentText())

    def onRemoveHedgeClicked(self):
        self.variable_hedges.takeItem(self.variable_hedges.currentRow())
        if (self.variable_hedges.count() == 0):
            self.remove_hedge.setEnabled(False)

if __name__ == "__main__":
    conn = psycopg2.connect(host='10.0.0.1', database='fuzzy', user='user1', password='pass1')
    app = QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())
