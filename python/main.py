#!/usr/bin/env python

import sys
import psycopg2

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self, *args):
        super(Window, self).__init__(*args)

        loadUi('main.ui', self)

        self.loadVariables()
        self.loadTerms()
        self.loadTerms2()
        self.loadFunctions()
        self.loadHedges()
        self.loadHedges2()
        self.loadRules()

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

        self.uiRulesCombo.currentIndexChanged.connect(self.onRuleSelected)
        self.uiCreateRuleButton.clicked.connect(self.onCreateRuleClicked)
        self.uiDeleteRuleButton.clicked.connect(self.onDeleteRuleClicked)

        self.uiCommitRuleButton.clicked.connect(self.commitRule)

        self.uiTabs.currentChanged.connect(self.onTabChanged)

    def loadVariables(self):
        self.uiVariablesCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT name FROM variables;')
        for item in cur.fetchall():
            self.uiVariablesCombo.addItem(item[0])
        cur.close()
        self.uiVariablesCombo.setCurrentIndex(-1)

    def loadTerms(self):
        self.uiTermsCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM terms;')
        for item in cur.fetchall():
            self.uiTermsCombo.addItem(item[0])
        cur.close()
        self.uiTermsCombo.setCurrentIndex(-1)
        self.uiAddTermButton.setEnabled(False)

    def loadTerms2(self):
        self.uiTermCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM terms;')
        for item in cur.fetchall():
            self.uiTermCombo.addItem(item[0])
        cur.close()
        self.uiTermCombo.setCurrentIndex(-1)

    def loadHedges(self):
        self.uiHedgesCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM hedges;')
        for item in cur.fetchall():
            self.uiHedgesCombo.addItem(item[0])
        cur.close()
        self.uiHedgesCombo.setCurrentIndex(-1)
        self.uiAddHedgeButton.setEnabled(False)

    def loadHedges2(self):
        self.uiHedgeCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT value FROM hedges;')
        for item in cur.fetchall():
            self.uiHedgeCombo.addItem(item[0])
        cur.close()
        self.uiHedgeCombo.setCurrentIndex(-1)

    def loadFunctions(self):
        self.uiFunctionCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT type FROM functions;')
        for item in cur.fetchall():
            self.uiFunctionCombo.addItem(item[0])
        cur.close()
        self.uiFunctionCombo.setCurrentIndex(-1)

    def loadRules(self):
        self.uiRulesCombo.clear()
        cur = conn.cursor()
        cur.execute('SELECT name FROM rules;')
        for item in cur.fetchall():
            self.uiRulesCombo.addItem(item[0])
        cur.close()
        self.uiRulesCombo.setCurrentIndex(-1)

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

        self.uiTermsList.clear()
        self.uiHedgesList.clear()

        if (self.uiVariablesCombo.currentIndex() == -1):
            self.uiRenameVariableButton.setEnabled(False)
            self.uiDeleteVariableButton.setEnabled(False)
            self.uiRangeMinEdit.clear()
            self.uiRangeMinEdit.setEnabled(False)
            self.uiRangeMaxEdit.clear()
            self.uiRangeMaxEdit.setEnabled(False)
            self.uiTermsCombo.setEnabled(False)
            self.uiTermsList.setEnabled(False)
            self.uiHedgesCombo.setEnabled(False)
            self.uiHedgesList.setEnabled(False)
            return

        cur = conn.cursor()
        cur.execute('SELECT terms.value FROM variables, terms, variables_terms WHERE variables.name = %s AND variables.id = variables_terms.variable_id AND terms.id = variables_terms.term_id;', (self.uiVariablesCombo.currentText(),))
        for item in cur.fetchall():
            self.uiTermsList.addItem(item[0])
        cur.close()
        self.loadTerms()

        cur = conn.cursor()
        cur.execute('SELECT hedges.value FROM variables, hedges, variables_hedges WHERE variables.name = %s AND variables.id = variables_hedges.variable_id AND hedges.id = variables_hedges.hedge_id;', (self.uiVariablesCombo.currentText(),))
        for item in cur.fetchall():
            self.uiHedgesList.addItem(item[0])
        cur.close()
        self.loadHedges()

        cur = conn.cursor()
        cur.execute('SELECT variables.min, variables.max FROM variables WHERE variables.name = %s;', (self.uiVariablesCombo.currentText(),))
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
        cur.execute('DELETE FROM variables WHERE name = %s;', (self.uiVariablesCombo.currentText(),))
        conn.commit()
        cur.close()
        self.uiVariablesCombo.removeItem(self.uiVariablesCombo.currentIndex())

    def onRangeChanged(self):
        self.uiCommitVariableButton.setEnabled(True)

    def commitVariable(self):
        self.uiCommitVariableButton.setEnabled(False)
        cur = conn.cursor()
        cur.execute('SELECT id FROM variables WHERE name = %s', (self.uiVariablesCombo.currentText(),))
        variable_id = cur.fetchone()
        if (variable_id):
            cur.execute('UPDATE variables SET min = %s, max = %s WHERE id = %s;', (self.uiRangeMinEdit.text(), self.uiRangeMaxEdit.text(), variable_id))
        else:
            cur.execute('INSERT INTO variables (name, min, max) VALUES (%s, %s, %s);', (self.uiVariablesCombo.currentText(), self.uiRangeMinEdit.text(), self.uiRangeMaxEdit.text()))
        cur.execute('DELETE FROM variables_terms WHERE variable_id = %s;', (variable_id,))
        for i in range(0, self.uiTermsList.count()):
            cur.execute('INSERT INTO variables_terms (variable_id, term_id) VALUES (%s, (SELECT id AS term_id FROM terms WHERE value = %s))', (variable_id, self.uiTermsList.item(i).text()))
        cur.execute('DELETE FROM variables_hedges WHERE variable_id = %s;', (variable_id,))
        for j in range(0, self.uiHedgesList.count()):
            cur.execute('INSERT INTO variables_hedges (variable_id, hedge_id) VALUES (%s, (SELECT id FROM hedges WHERE value = %s))', (variable_id, self.uiHedgesList.item(j).text()))
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

        self.uiFunctionCombo.blockSignals(True)
        cur = conn.cursor()
        cur.execute('SELECT functions.type FROM terms, functions WHERE functions.id = terms.function_id AND terms.value = %s;', (self.uiTermCombo.currentText(),))
        type = cur.fetchone()
        if (type):
            self.uiFunctionCombo.setCurrentText(type[0])
        else:
            self.uiFunctionCombo.setCurrentIndex(-1)
        self.uiFunctionCombo.blockSignals(False)

        cur = conn.cursor()
        cur.execute('SELECT points FROM terms WHERE value = %s;', (self.uiTermCombo.currentText(),))
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
        cur.execute('DELETE FROM terms WHERE value = %s;', (self.uiTermCombo.currentText(),))
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
        cur.execute('SELECT id FROM terms WHERE value = %s', (self.uiTermCombo.currentText(),))
        term_id = cur.fetchone()
        if (term_id):
            cur.execute('UPDATE terms SET function_id = (SELECT id FROM functions WHERE type = %s), points = %s WHERE id = %s;', (self.uiFunctionCombo.currentText(), self.uiPointsEdit.text(), term_id))
        else:
            cur.execute('INSERT INTO terms (value, function_id, points) VALUES (%s, (SELECT id FROM functions WHERE type = %s), %s);', (self.uiTermCombo.currentText(), self.uiFunctionCombo.currentText(), self.uiPointsEdit.text()))
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
        cur.execute('SELECT result FROM hedges WHERE value = %s;', (self.uiHedgeCombo.currentText(),))
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
        cur.execute('DELETE FROM hedges WHERE value = %s;', (self.uiHedgeCombo.currentText(),))
        conn.commit()
        cur.close()
        self.uiHedgeCombo.removeItem(self.uiHedgeCombo.currentIndex())

    def onResultChanged(self):
        self.uiCommitHedgeButton.setEnabled(True)

    def commitHedge(self):
        self.uiCommitHedgeButton.setEnabled(False)
        cur = conn.cursor()
        cur.execute('SELECT id FROM hedges WHERE value = %s', (self.uiHedgeCombo.currentText(),))
        hedge_id = cur.fetchone()
        if (hedge_id):
            cur.execute('UPDATE hedges SET result = %s WHERE id = %s;', (self.uiResultEdit.text(), hedge_id))
        else:
            cur.execute('INSERT INTO hedges (value, result) VALUES (%s, %s);', (self.uiHedgeCombo.currentText(), self.uiResultEdit.text()))
        conn.commit()
        cur.close()

    def onRuleSelected(self):
        if (self.uiRulesCombo.isEditable() == True):
            return

        self.uiCommitRuleButton.setEnabled(False)

        self.uiAntecedentTree.clear()
        self.uiConsequentTree.clear()

        if (self.uiRulesCombo.currentIndex() == -1):
            self.uiRenameRuleButton.setEnabled(False)
            self.uiDeleteRuleButton.setEnabled(False)
            self.uiAntecedentNodeTypesCombo.setEnabled(False)
            self.uiAntecedentNodesCombo.setEnabled(False)
            self.uiAntecedentTree.setEnabled(False)
            self.uiConsequentNodeTypesCombo.setEnabled(False)
            self.uiConsequentNodesCombo.setEnabled(False)
            self.uiConsequentTree.setEnabled(False)
            return

        cur = conn.cursor()
        cur.execute('SELECT nodes.id, types.name FROM rules, nodes, types WHERE rules.name = %s AND rules.antecedent_id = nodes.id AND types.id = nodes.type_id;', (self.uiRulesCombo.currentText(),))
        root = cur.fetchone()
        cur.close()
        if (root):
            item = QTreeWidgetItem()
            item.setText(0, '%s' % root[0])
            self.uiAntecedentTree.addTopLevelItem(item)
            cur = conn.cursor()
            cur.execute('SELECT * FROM nodes JOIN closures ON nodes.id = closures.descendant_id WHERE closures.ancestor_id IN (SELECT antecedent_id FROM rules WHERE name = %s) ORDER BY parent_id ASC;', (self.uiRulesCombo.currentText(),))
            nodes = cur.fetchall()
            cur.close()
            for node in nodes:
                if node[0] != node[1]:
                    parents = self.uiAntecedentTree.findItems('%s' % node[1], Qt.MatchExactly | Qt.MatchRecursive)
                    item = QTreeWidgetItem()
                    item.setText(0, '%s' % node[0])
                    parents[0].addChild(item)

        cur = conn.cursor()
        cur.execute('SELECT nodes.id, types.name FROM rules, nodes, types WHERE rules.name = %s AND rules.consequent_id = nodes.id AND types.id = nodes.type_id;', (self.uiRulesCombo.currentText(),))
        root = cur.fetchone()
        cur.close()
        if (root):
            item = QTreeWidgetItem()
            item.setText(0, '%s' % root[0])
            self.uiConsequentTree.addTopLevelItem(item)
            cur = conn.cursor()
            cur.execute('SELECT * FROM nodes JOIN closures ON nodes.id = closures.descendant_id WHERE closures.ancestor_id IN (SELECT consequent_id FROM rules WHERE name = %s) ORDER BY parent_id ASC;', (self.uiRulesCombo.currentText(),))
            nodes = cur.fetchall()
            cur.close()
            for node in nodes:
                if node[0] != node[1]:
                    parents = self.uiConsequentTree.findItems('%s' % node[1], Qt.MatchExactly | Qt.MatchRecursive)
                    item = QTreeWidgetItem()
                    item.setText(0, '%s' % node[0])
                    parents[0].addChild(item)

        self.uiRenameRuleButton.setEnabled(True)
        self.uiDeleteRuleButton.setEnabled(True)
        self.uiAntecedentTree.setEnabled(True)
        self.uiConsequentTree.setEnabled(True)

    def onCreateRuleClicked(self):
        self.uiRulesCombo.setCurrentIndex(-1)
        self.uiRulesCombo.setEditable(True)
        self.uiRulesCombo.lineEdit().returnPressed.connect(self.onRuleEntered)
        self.uiRulesCombo.setFocus()
        self.uiCreateRuleButton.setEnabled(False)

    def onRuleEntered(self):
        self.uiRulesCombo.setEditable(False)
        self.uiCreateRuleButton.setEnabled(True)
        self.onRuleSelected()

    def onDeleteRuleClicked(self):
        cur = conn.cursor()
        cur.execute('DELETE FROM rules WHERE name = %s;', (self.uiRulesCombo.currentText(),))
        conn.commit()
        cur.close()
        self.uiRulesCombo.removeItem(self.uiRulesCombo.currentIndex())

    def commitRule(self):
        self.uiCommitRuleButton.setEnabled(False)

    def onTabChanged(self):
        if (self.uiTabs.currentIndex() == 0):
            self.loadTerms()
            self.loadHedges()
            self.onVariableSelected()

if __name__ == "__main__":
    conn = psycopg2.connect(host='127.0.0.1', database='fuzzy', user='user1', password='pass1')
    app = QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec_())
    conn.close()
