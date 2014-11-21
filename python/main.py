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
        self.loadTerms()
        self.loadFunctions()
        self.loadHedges()

        self.uiVariablesCombo.currentIndexChanged.connect(self.onVariableSelected)
        self.uiCreateVariableButton.clicked.connect(self.onCreateVariableClicked)
        self.uiDeleteVariableButton.clicked.connect(self.onDeleteVariableClicked)

        self.uiRangeMinEdit.textEdited.connect(self.onRangeChanged)
        self.uiRangeMaxEdit.textEdited.connect(self.onRangeChanged)
        self.uiRangeMinEdit.setValidator(QDoubleValidator(-1000000, 1000000, 2, self.uiRangeMinEdit))
        self.uiRangeMaxEdit.setValidator(QDoubleValidator(-1000000, 1000000, 2, self.uiRangeMaxEdit))

        self.uiTermsCombo.currentIndexChanged.connect(self.onTermSelected)
        self.uiAddTermButton.clicked.connect(self.onAddTermClicked)
        self.uiTermsList.clicked.connect(self.onVariableTermSelected)
        self.uiRemoveTermButton.clicked.connect(self.onRemoveTermClicked)

        self.uiHedgesCombo.currentTextChanged.connect(self.onHedgeSelected)
        self.uiAddHedgeButton.clicked.connect(self.onAddHedgeClicked)
        self.uiHedgesList.clicked.connect(self.onVariableHedgeSelected)
        self.uiRemoveHedgeButton.clicked.connect(self.onRemoveHedgeClicked)

        self.uiCommitVariableButton.clicked.connect(self.commitVariable)

        self.uiTermCombo.currentIndexChanged.connect(self.onTerm2Selected)
        self.uiCreateTermButton.clicked.connect(self.onCreateTermClicked)
        self.uiDeleteTermButton.clicked.connect(self.onDeleteTermClicked)

        self.uiFunctionCombo.currentIndexChanged.connect(self.onFunctionSelected)

        self.uiPointsEdit.textEdited.connect(self.onPointsChanged)

        self.uiCommitTermButton.clicked.connect(self.commitTerm)

        self.uiHedgeCombo.currentIndexChanged.connect(self.onHedge2Selected)
        self.uiCreateHedgeButton.clicked.connect(self.onCreateHedgeClicked)
        self.uiDeleteHedgeButton.clicked.connect(self.onDeleteHedgeClicked)

        self.uiResultEdit.textEdited.connect(self.onResultChanged)

        self.uiCommitHedgeButton.clicked.connect(self.commitHedge)

        self.uiTabs.currentChanged.connect(self.onTabChanged)

    def loadVariables(self):
        self.uiVariablesCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT name FROM variable;')
        for item in cur.fetchall():
            self.uiVariablesCombo.addItem(item[0])
        cur.close()
        self.uiVariablesCombo.setCurrentIndex(-1)

    def loadTerms(self):
        self.uiTermCombo.clear()
        self.uiTermsCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM term;')
        for item in cur.fetchall():
            self.uiTermCombo.addItem(item[0])
            self.uiTermsCombo.addItem(item[0])
        cur.close()
        self.uiTermCombo.setCurrentIndex(-1)
        self.uiTermsCombo.setCurrentIndex(-1)
        self.uiAddTermButton.setEnabled(False)

    def loadHedges(self):
        self.uiHedgeCombo.clear()
        self.uiHedgesCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM hedge;')
        for item in cur.fetchall():
            self.uiHedgeCombo.addItem(item[0])
            self.uiHedgesCombo.addItem(item[0])
        cur.close()
        self.uiHedgeCombo.setCurrentIndex(-1)
        self.uiHedgesCombo.setCurrentIndex(-1)
        self.uiAddHedgeButton.setEnabled(False)

    def loadFunctions(self):
        self.uiFunctionCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT type FROM function;')
        for item in cur.fetchall():
            self.uiFunctionCombo.addItem(item[0])
        cur.close()
        self.uiFunctionCombo.setCurrentIndex(-1)

    def onVariableSelected(self):
        if (self.uiVariablesCombo.isEditable() == True):
            return

        self.uiTermsCombo.setCurrentIndex(-1)
        self.uiAddTermButton.setEnabled(False)
        self.uiRemoveTermButton.setEnabled(False)
        self.uiHedgesCombo.setCurrentIndex(-1)
        self.uiAddHedgeButton.setEnabled(False)
        self.uiRemoveHedgeButton.setEnabled(False)
        self.uiCommitVariableButton.setEnabled(False)

        if (self.uiVariablesCombo.currentIndex() == -1):
            self.uiRenameVariableButton.setEnabled(False)
            self.uiDeleteVariableButton.setEnabled(False)
            self.uiRangeMinEdit.clear()
            self.uiRangeMinEdit.setEnabled(False)
            self.uiRangeMaxEdit.clear()
            self.uiRangeMaxEdit.setEnabled(False)
            self.uiTermsCombo.setEnabled(False)
            self.uiTermsList.clear()
            self.uiTermsList.setEnabled(False)
            self.uiHedgesCombo.setEnabled(False)
            self.uiHedgesList.clear()
            self.uiHedgesList.setEnabled(False)
            return

        self.uiTermsList.clear()
        cur = conn.cursor()
        cur.execute('SELECT term.value FROM variable, term, variable_term WHERE variable.name = %s AND variable.id = variable_term.variable_id AND term.id = variable_term.term_id;', (self.uiVariablesCombo.currentText(),))
        for item in cur.fetchall():
            self.uiTermsList.addItem(item[0])
        cur.close()
        self.loadTerms()

        self.uiHedgesList.clear()
        cur = conn.cursor()
        cur.execute('SELECT hedge.value FROM variable, hedge, variable_hedge WHERE variable.name = %s AND variable.id = variable_hedge.variable_id AND hedge.id = variable_hedge.hedge_id;', (self.uiVariablesCombo.currentText(),))
        for item in cur.fetchall():
            self.uiHedgesList.addItem(item[0])
        cur.close()
        self.loadHedges()

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
        self.uiHedgesCombo.setEnabled(True)
        self.uiHedgesList.setEnabled(True)

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
        cur = conn.cursor()
        cur.execute('DELETE FROM variable WHERE name = %s;', (self.uiVariablesCombo.currentText(),))
        conn.commit()
        cur.close()
        self.uiVariablesCombo.removeItem(self.uiVariablesCombo.currentIndex())

    def onRangeChanged(self):
        self.uiCommitVariableButton.setEnabled(True)

    def commitVariable(self):
        self.uiCommitVariableButton.setEnabled(False)
        cur = conn.cursor()
        cur.execute('SELECT id FROM variable WHERE name = %s', (self.uiVariablesCombo.currentText(),))
        variable_id = cur.fetchone()
        if (variable_id):
            cur.execute('UPDATE variable SET min = %s, max = %s WHERE id = %s;', (self.uiRangeMinEdit.text(), self.uiRangeMaxEdit.text(), variable_id))
        else:
            cur.execute('INSERT INTO variable (name, min, max) VALUES (%s, %s, %s);', (self.uiVariablesCombo.currentText(), self.uiRangeMinEdit.text(), self.uiRangeMaxEdit.text()))
        cur.execute('DELETE FROM variable_term WHERE variable_id = %s;', (variable_id,))
        for i in range(0, self.uiTermsList.count()):
            cur.execute('INSERT INTO variable_term (variable_id, term_id) VALUES (%s, (SELECT id AS term_id FROM term WHERE value = %s))', (variable_id, self.uiTermsList.item(i).text()))
        cur.execute('DELETE FROM variable_hedge WHERE variable_id = %s;', (variable_id,))
        for j in range(0, self.uiHedgesList.count()):
            cur.execute('INSERT INTO variable_hedge (variable_id, hedge_id) VALUES (%s, (SELECT id FROM hedge WHERE value = %s))', (variable_id, self.uiHedgesList.item(j).text()))
        conn.commit()
        cur.close()

    def onTerm2Selected(self):
        if (self.uiTermCombo.isEditable() == True):
            return

        self.uiCommitTermButton.setEnabled(False)

        if (self.uiTermCombo.currentIndex() == -1):
            self.uiRenameTermButton.setEnabled(False)
            self.uiDeleteTermButton.setEnabled(False)
            self.uiFunctionCombo.setCurrentIndex(-1)
            self.uiFunctionCombo.setEnabled(False)
            self.uiPointsEdit.clear()
            self.uiPointsEdit.setEnabled(False)
            return

        cur = conn.cursor()
        cur.execute('SELECT function.type FROM term, function WHERE function.id = term.function_id AND term.value = %s;', (self.uiTermCombo.currentText(),))
        type = cur.fetchone()
        if (type):
            self.uiFunctionCombo.setCurrentText(type[0])
        else:
            self.uiFunctionCombo.setCurrentIndex(-1)

        cur = conn.cursor()
        cur.execute('SELECT points FROM term WHERE value = %s;', (self.uiTermCombo.currentText(),))
        points = cur.fetchone()
        if (points):
            self.uiPointsEdit.setText('%s' % points[0])
        else:
            self.uiPointsEdit.clear()

        self.uiRenameTermButton.setEnabled(True)
        self.uiDeleteTermButton.setEnabled(True)
        self.uiPointsEdit.setEnabled(True)
        self.uiFunctionCombo.setEnabled(True)

    def onCreateTermClicked(self):
        self.uiTermCombo.setCurrentIndex(-1)
        self.uiTermCombo.setEditable(True)
        self.uiTermCombo.lineEdit().returnPressed.connect(self.onTermEntered)
        self.uiTermCombo.setFocus()
        self.uiCreateTermButton.setEnabled(False)

    def onTermEntered(self):
        self.uiTermCombo.setEditable(False)
        self.uiCreateTermButton.setEnabled(True)
        self.onTerm2Selected()
        self.uiFunctionCombo.setFocus()

    def onDeleteTermClicked(self):
        cur = conn.cursor()
        cur.execute('DELETE FROM term WHERE value = %s;', (self.uiTermCombo.currentText(),))
        conn.commit()
        cur.close()
        self.uiTermCombo.removeItem(self.uiTermCombo.currentIndex())

    def onPointsChanged(self):
        self.uiCommitTermButton.setEnabled(True)

    def onFunctionSelected(self):
        if (self.uiFunctionCombo.currentIndex() != -1):
            self.uiCommitTermButton.setEnabled(True)

    def commitTerm(self):
        self.uiCommitTermButton.setEnabled(False)
        cur = conn.cursor()
        cur.execute('SELECT id FROM term WHERE value = %s', (self.uiTermCombo.currentText(),))
        term_id = cur.fetchone()
        if (term_id):
            cur.execute('UPDATE term SET function_id = (SELECT id FROM function WHERE type = %s), points = %s WHERE id = %s;', (self.uiFunctionCombo.currentText(), self.uiPointsEdit.text(), term_id))
        else:
            cur.execute('INSERT INTO term (value, function_id, points) VALUES (%s, (SELECT id FROM function WHERE type = %s), %s);', (self.uiTermCombo.currentText(), self.uiFunctionCombo.currentText(), self.uiPointsEdit.text()))
        conn.commit()
        cur.close()

    def onHedge2Selected(self):
        if (self.uiHedgeCombo.isEditable() == True):
            return

        self.uiCommitHedgeButton.setEnabled(False)

        if (self.uiHedgeCombo.currentIndex() == -1):
            self.uiRenameHedgeButton.setEnabled(False)
            self.uiDeleteHedgeButton.setEnabled(False)
            self.uiResultEdit.clear()
            self.uiResultEdit.setEnabled(False)
            return

        cur = conn.cursor()
        cur.execute('SELECT result FROM hedge WHERE value = %s;', (self.uiHedgeCombo.currentText(),))
        result = cur.fetchone()
        if (result):
            self.uiResultEdit.setText('%s' % result[0])
        else:
            self.uiResultEdit.clear()

        self.uiRenameHedgeButton.setEnabled(True)
        self.uiDeleteHedgeButton.setEnabled(True)
        self.uiResultEdit.setEnabled(True)

    def onCreateHedgeClicked(self):
        self.uiHedgeCombo.setCurrentIndex(-1)
        self.uiHedgeCombo.setEditable(True)
        self.uiHedgeCombo.lineEdit().returnPressed.connect(self.onHedgeEntered)
        self.uiHedgeCombo.setFocus()
        self.uiCreateHedgeButton.setEnabled(False)

    def onHedgeEntered(self):
        self.uiHedgeCombo.setEditable(False)
        self.uiCreateHedgeButton.setEnabled(True)
        self.onHedge2Selected()
        self.uiResultEdit.setFocus()

    def onDeleteHedgeClicked(self):
        cur = conn.cursor()
        cur.execute('DELETE FROM hedge WHERE value = %s;', (self.uiHedgeCombo.currentText(),))
        conn.commit()
        cur.close()
        self.uiHedgeCombo.removeItem(self.uiHedgeCombo.currentIndex())

    def onResultChanged(self):
        self.uiCommitHedgeButton.setEnabled(True)

    def commitHedge(self):
        self.uiCommitHedgeButton.setEnabled(False)
        cur = conn.cursor()
        cur.execute('SELECT id FROM hedge WHERE value = %s', (self.uiHedgeCombo.currentText(),))
        hedge_id = cur.fetchone()
        if (hedge_id):
            cur.execute('UPDATE hedge SET result = %s WHERE id = %s;', (self.uiResultEdit.text(), hedge_id))
        else:
            cur.execute('INSERT INTO hedge (value, result) VALUES (%s, %s);', (self.uiHedgeCombo.currentText(), self.uiResultEdit.text()))
        conn.commit()
        cur.close()

    def onTabChanged(self):
        if (self.uiTabs.currentIndex() == 0):
            self.loadTerms()
            self.loadHedges()
            self.onVariableSelected()

if __name__ == "__main__":
    conn = psycopg2.connect(host='78.107.239.213', database='fuzzy', user='user1', password='pass1')
    app = QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())
    conn.close()
