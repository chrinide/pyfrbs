#!/usr/bin/env python

import sys
import psycopg2

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QTreeWidgetItem, QTableWidgetItem
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self, *args, addr):
        super(Window, self).__init__(*args)

        self.conn = psycopg2.connect(host=addr, database='fuzzy', user='user1', password='pass1')

        loadUi('expert.ui', self)

        # Initialize variables tab

        self.fillComboWithLemmas(self.uiVariablesCombo, 'variables')
        self.uiVariablesCombo.currentIndexChanged.connect(self.onVariableSelected)
        self.uiCreateVariableButton.clicked.connect(self.onCreateVariableClicked)
        self.uiRenameVariableButton.clicked.connect(self.onRenameVariableClicked)
        self.uiDeleteVariableButton.clicked.connect(self.onDeleteVariableClicked)

        self.uiVariableVerifiedCheck.stateChanged.connect(self.onVariableVerified)
        self.uiRangeMinEdit.textEdited.connect(self.checkRange)
        self.uiRangeMinEdit.setValidator(QDoubleValidator(-1000000, 1000000, 2, self.uiRangeMinEdit))
        self.uiRangeMaxEdit.textEdited.connect(self.checkRange)
        self.uiRangeMaxEdit.setValidator(QDoubleValidator(-1000000, 1000000, 2, self.uiRangeMaxEdit))

        self.loadTerms()
        self.uiTermsCombo.currentIndexChanged.connect(self.onTermSelected)
        self.uiAddTermButton.clicked.connect(self.onAddTermClicked)
        self.uiTermsList.clicked.connect(self.onVariableTermSelected)
        self.uiRemoveTermButton.clicked.connect(self.onRemoveTermClicked)

        self.loadHedges()
        self.uiHedgesCombo.currentTextChanged.connect(self.onHedgeSelected)
        self.uiAddHedgeButton.clicked.connect(self.onAddHedgeClicked)
        self.uiHedgesList.clicked.connect(self.onVariableHedgeSelected)
        self.uiRemoveHedgeButton.clicked.connect(self.onRemoveHedgeClicked)

        self.uiCommitVariableButton.clicked.connect(self.commitVariable)

        # Initialize terms tab

        self.fillComboWithLemmas(self.uiTerms2Combo, 'terms')
        self.uiTerms2Combo.currentIndexChanged.connect(self.onTerm2Selected)
        self.uiCreateTermButton.clicked.connect(self.onCreateTermClicked)
        self.uiRenameTermButton.clicked.connect(self.onRenameTermClicked)
        self.uiDeleteTermButton.clicked.connect(self.onDeleteTermClicked)

        self.uiTermVerifiedCheck.stateChanged.connect(self.onTermVerified)

        self.fillComboWithNames(self.uiFunctionCombo, 'functions')
        self.uiFunctionCombo.currentIndexChanged.connect(self.onFunctionSelected)

        self.uiPointsEdit.textEdited.connect(self.checkPoints)

        self.uiCommitTermButton.clicked.connect(self.commitTerm)

        # Initialize hedges tab

        self.fillComboWithLemmas(self.uiHedges2Combo, 'hedges')
        self.uiHedges2Combo.currentIndexChanged.connect(self.onHedge2Selected)
        self.uiCreateHedgeButton.clicked.connect(self.onCreateHedgeClicked)
        self.uiRenameHedgeButton.clicked.connect(self.onRenameHedgeClicked)
        self.uiDeleteHedgeButton.clicked.connect(self.onDeleteHedgeClicked)

        self.uiHedgeVerifiedCheck.stateChanged.connect(self.onHedgeVerified)

        self.uiResultEdit.textEdited.connect(self.checkResult)

        self.uiCommitHedgeButton.clicked.connect(self.commitHedge)

        # Initialize rules tab

        self.fillComboWithNames(self.uiRulesCombo, 'rules')
        self.uiRulesCombo.currentIndexChanged.connect(self.onRuleSelected)
        self.uiCreateRuleButton.clicked.connect(self.onCreateRuleClicked)
        self.uiRenameRuleButton.clicked.connect(self.onRenameRuleClicked)
        self.uiDeleteRuleButton.clicked.connect(self.onDeleteRuleClicked)

        self.uiRuleVerifiedCheck.stateChanged.connect(self.onRuleVerified)
        
        self.fillComboWithNames(self.uiAntecedentNodeTypesCombo, 'types')
        self.uiAntecedentNodeTypesCombo.currentIndexChanged.connect(self.onAntecedentNodeTypeSelected)
        self.uiAntecedentNodesCombo.currentIndexChanged.connect(self.onAntecedentNodeValueSelected)
        self.uiAddAntecedentNodeButton.clicked.connect(self.onAddAntecedentNodeClicked)
        self.uiAntecedentTree.currentItemChanged.connect(self.onAntecedentNodeSelected)
        self.uiRemoveAntecedentNodeButton.clicked.connect(self.onRemoveAntecedentNodeClicked)

        self.fillComboWithNames(self.uiConsequentNodeTypesCombo, 'types')
        self.uiConsequentNodeTypesCombo.currentIndexChanged.connect(self.onConsequentNodeTypeSelected)
        self.uiConsequentNodesCombo.currentIndexChanged.connect(self.onConsequentNodeValueSelected)
        self.uiAddConsequentNodeButton.clicked.connect(self.onAddConsequentNodeClicked)
        self.uiConsequentTree.currentItemChanged.connect(self.onConsequentNodeSelected)
        self.uiRemoveConsequentNodeButton.clicked.connect(self.onRemoveConsequentNodeClicked)

        self.uiCommitRuleButton.clicked.connect(self.commitRule)

        # Initialize debug tab

        self.uiModeCombo.addItem('Переменные', 0)
        self.uiModeCombo.addItem('Термы', 1)
        self.uiModeCombo.addItem('Модификаторы', 2)
        self.uiModeCombo.addItem('Переменные и термы', 3)
        self.uiModeCombo.addItem('Переменные и модификаторы', 4)
        self.uiModeCombo.addItem('Синонимы', 5)
        self.uiModeCombo.setCurrentIndex(-1)
        self.uiModeCombo.currentIndexChanged.connect(self.onModeSelected)

        # Initialize main window

        self.uiTabs.setCurrentIndex(0)
        self.uiTabs.currentChanged.connect(self.onTabChanged)

    def getLemmas(self, group):
        cur = self.conn.cursor()
        cur.execute('SELECT lemma FROM synonims WHERE group_id = %s ORDER BY hits DESC;', (group,))
        lemmas = []
        for row in cur.fetchall():
            lemmas.append(row[0])
        cur.close()
        return lemmas

    def fillComboWithLemmas(self, combo, table):
        combo.clear()
        cur = self.conn.cursor()
        cur.execute('SELECT id, name, name_id FROM %s;' % table)
        for row in cur.fetchall():
            if (row[1] != ''):
                combo.addItem(row[1], row[0])
            else:
                combo.addItem(', '.join(self.getLemmas(row[2])), row[0])
        cur.close()
        combo.setCurrentIndex(-1)

    def fillComboWithNames(self, combo, table):
        combo.clear()
        cur = self.conn.cursor()
        cur.execute('SELECT id, name FROM %s;' % table)
        for row in cur.fetchall():
            combo.addItem(row[1], row[0])
        cur.close()
        combo.setCurrentIndex(-1)

    # Actions on variables tab

    def loadTerms(self):
        self.fillComboWithLemmas(self.uiTermsCombo, 'terms')
        self.uiAddTermButton.setEnabled(False)

    def loadHedges(self):
        self.fillComboWithLemmas(self.uiHedgesCombo, 'hedges')
        self.uiAddHedgeButton.setEnabled(False)

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
        self.uiVariableVerifiedCheck.setChecked(False)
        self.uiRangeMinEdit.clear()
        self.uiRangeMaxEdit.clear()
        self.uiTermsList.clear()
        self.uiHedgesList.clear()

        if (self.uiVariablesCombo.currentIndex() == -1):
            self.uiRenameVariableButton.setEnabled(False)
            self.uiDeleteVariableButton.setEnabled(False)
            self.uiVariableVerifiedCheck.setEnabled(False)
            self.uiRangeMinEdit.setEnabled(False)
            self.uiRangeMaxEdit.setEnabled(False)
            self.uiTermsCombo.setEnabled(False)
            self.uiTermsList.setEnabled(False)
            self.uiHedgesCombo.setEnabled(False)
            self.uiHedgesList.setEnabled(False)
            return

        if (self.uiVariablesCombo.currentData() != 0):
            cur = self.conn.cursor()
            cur.execute('SELECT terms.id, terms.name, terms.name_id FROM variables, terms, variables_terms WHERE variables.id = %s AND variables.id = variables_terms.variable_id AND terms.id = variables_terms.term_id;', (self.uiVariablesCombo.currentData(),))
            for row in cur.fetchall():
                if (row[1] != ''):
                    item = QListWidgetItem(row[1])
                else:
                    item = QListWidgetItem(', '.join(self.getLemmas(row[2])))
                item.setData(Qt.UserRole, row[0])
                self.uiTermsList.addItem(item)
            cur.close()
            self.loadTerms()

            cur = self.conn.cursor()
            cur.execute('SELECT hedges.id, hedges.name, hedges.name_id FROM variables, hedges, variables_hedges WHERE variables.id = %s AND variables.id = variables_hedges.variable_id AND hedges.id = variables_hedges.hedge_id;', (self.uiVariablesCombo.currentData(),))
            for row in cur.fetchall():
                if (row[1] != ''):
                    item = QListWidgetItem(row[1])
                else:
                    item = QListWidgetItem(', '.join(self.getLemmas(row[2])))
                item.setData(Qt.UserRole, row[0])
                self.uiHedgesList.addItem(item)
            cur.close()
            self.loadHedges()

            cur = self.conn.cursor()
            cur.execute('SELECT min, max FROM variables WHERE id = %s;', (self.uiVariablesCombo.currentData(),))
            range = cur.fetchone()
            if (range):
                self.uiRangeMinEdit.setText('%s' % range[0])
                self.uiRangeMaxEdit.setText('%s' % range[1])

            cur = self.conn.cursor()
            cur.execute('SELECT validated FROM variables WHERE id = %s;', (self.uiVariablesCombo.currentData(),))
            state = cur.fetchone()
            if (state[0] == True):
                self.uiVariableVerifiedCheck.setChecked(True);

        self.uiRenameVariableButton.setEnabled(True)
        self.uiDeleteVariableButton.setEnabled(True)
        self.uiVariableVerifiedCheck.setEnabled(True)
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
        found = False
        for index in range(self.uiTermsList.count()):
            if (self.uiTermsList.item(index).data(Qt.UserRole) == self.uiTermsCombo.currentData()):
                found = True
                break
        if (not found):
            item = QListWidgetItem(self.uiTermsCombo.currentText())
            item.setData(Qt.UserRole, self.uiTermsCombo.currentData())
            self.uiTermsList.addItem(item)
            self.checkRange()

    def onRemoveTermClicked(self):
        self.uiTermsList.takeItem(self.uiTermsList.currentRow())
        if (self.uiTermsList.count() == 0):
            self.uiRemoveTermButton.setEnabled(False)
        self.checkRange()

    def onHedgeSelected(self):
        self.uiAddHedgeButton.setEnabled(True)

    def onVariableHedgeSelected(self):
        self.uiRemoveHedgeButton.setEnabled(True)

    def onAddHedgeClicked(self):
        found = False
        for index in range(self.uiHedgesList.count()):
            if (self.uiHedgesList.item(index).data(Qt.UserRole) == self.uiHedgesCombo.currentData()):
                found = True
                break
        if (not found):
            item = QListWidgetItem(self.uiHedgesCombo.currentText())
            item.setData(Qt.UserRole, self.uiHedgesCombo.currentData())
            self.uiHedgesList.addItem(item)
            self.checkRange()

    def onRemoveHedgeClicked(self):
        self.uiHedgesList.takeItem(self.uiHedgesList.currentRow())
        if (self.uiHedgesList.count() == 0):
            self.uiRemoveHedgeButton.setEnabled(False)
        self.checkRange()

    def onCreateVariableClicked(self):
        self.currentVariable = -1
        self.uiVariablesCombo.setCurrentIndex(-1)
        self.uiVariablesCombo.setEditable(True)
        self.uiVariablesCombo.lineEdit().returnPressed.connect(self.onVariableEntered)
        self.uiVariablesCombo.setFocus()
        self.uiCreateVariableButton.setEnabled(False)

    def onRenameVariableClicked(self):
        self.currentVariable = self.uiVariablesCombo.currentIndex()
        self.uiVariablesCombo.setEditable(True)
        self.uiVariablesCombo.lineEdit().returnPressed.connect(self.onVariableEntered)
        self.uiVariablesCombo.setFocus()
        self.uiCreateVariableButton.setEnabled(False)
        self.uiRenameVariableButton.setEnabled(False)
        self.uiDeleteVariableButton.setEnabled(False)

    def onVariableEntered(self):
        self.uiVariablesCombo.setEditable(False)
        self.uiCreateVariableButton.setEnabled(True)
        self.uiRenameVariableButton.setEnabled(True)
        self.uiDeleteVariableButton.setEnabled(True)
        if (self.currentVariable >= 0):
            name = self.uiVariablesCombo.currentText()
            self.uiVariablesCombo.removeItem(self.uiVariablesCombo.currentIndex())
            if (self.uiVariablesCombo.itemText(self.currentVariable) != name):
                self.uiVariablesCombo.setItemText(self.currentVariable, name)
                self.variableRenamed = True
                self.uiVariablesCombo.setCurrentIndex(self.currentVariable)
                self.checkRange()
            else:
                self.uiVariablesCombo.setCurrentIndex(self.currentVariable)
        else:
            self.uiVariablesCombo.setItemData(self.uiVariablesCombo.currentIndex(), 0)
            self.onVariableSelected()

    def onDeleteVariableClicked(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM variables WHERE id = %s;', (self.uiVariablesCombo.currentData(),))
        self.conn.commit()
        cur.close()
        self.uiVariablesCombo.removeItem(self.uiVariablesCombo.currentIndex())

    def checkRange(self):
        if (self.uiRangeMinEdit.text() != '' and self.uiRangeMaxEdit.text() != ''):
            self.uiCommitVariableButton.setEnabled(True)
        else:
            self.uiCommitVariableButton.setEnabled(False)

    def onVariableVerified(self):
        self.checkRange()

    def commitVariable(self):
        self.uiCommitVariableButton.setEnabled(False)
        cur = self.conn.cursor()
        variable_id = self.uiVariablesCombo.currentData()
        if (variable_id):
            cur.execute('UPDATE variables SET validated = %s, min = %s, max = %s WHERE id = %s;', (self.uiVariableVerifiedCheck.isChecked(), self.uiRangeMinEdit.text(), self.uiRangeMaxEdit.text(), variable_id))
            if (self.variableRenamed == True):
                cur.execute('UPDATE variables SET name = %s WHERE id = %s;', (self.uiVariablesCombo.currentText(), variable_id))
            cur.execute('DELETE FROM variables_terms WHERE variable_id = %s;', (variable_id,))
            cur.execute('DELETE FROM variables_hedges WHERE variable_id = %s;', (variable_id,))
        else:
            cur.execute('INSERT INTO groups (is_variable, is_term, is_hedge) VALUES (true, false, false) RETURNING id;')
            group_id = cur.fetchone()[0]
            for lemma in self.uiVariablesCombo.currentText().replace(' ', '').split(','):
                cur.execute('INSERT INTO synonims (group_id, lemma, grammemes, hits) VALUES (%s, %s, %s, 0);', (group_id, lemma, ''));
            cur.execute('INSERT INTO variables (name_id, name, validated, min, max) VALUES (%s, '', %s, %s, %s) RETURNING id;', (group_id, self.uiVariableVerifiedCheck.isChecked(), self.uiRangeMinEdit.text(), self.uiRangeMaxEdit.text()))
            variable_id = cur.fetchone()[0]
            self.uiVariablesCombo.setItemData(self.uiVariablesCombo.currentIndex(), variable_id)
        for i in range(0, self.uiTermsList.count()):
            cur.execute('INSERT INTO variables_terms (variable_id, term_id) VALUES (%s, %s);', (variable_id, self.uiTermsList.item(i).data(Qt.UserRole)))
        for j in range(0, self.uiHedgesList.count()):
            cur.execute('INSERT INTO variables_hedges (variable_id, hedge_id) VALUES (%s, %s);', (variable_id, self.uiHedgesList.item(j).data(Qt.UserRole)))
        self.conn.commit()
        cur.close()

    # Actions on terms tab

    def onTerm2Selected(self):
        if (self.uiTerms2Combo.isEditable() == True):
            return

        self.uiCommitTermButton.setEnabled(False)
        self.uiTermVerifiedCheck.setChecked(False)
        self.uiPointsEdit.clear()

        if (self.uiTerms2Combo.currentIndex() == -1):
            self.uiRenameTermButton.setEnabled(False)
            self.uiDeleteTermButton.setEnabled(False)
            self.uiTermVerifiedCheck.setEnabled(False)
            self.uiFunctionCombo.setCurrentIndex(-1)
            self.uiFunctionCombo.setEnabled(False)
            self.uiPointsEdit.setEnabled(False)
            return

        if (self.uiTerms2Combo.currentData() != 0):
            self.uiFunctionCombo.blockSignals(True)
            cur = self.conn.cursor()
            cur.execute('SELECT functions.name FROM terms, functions WHERE functions.id = terms.function_id AND terms.id = %s;', (self.uiTerms2Combo.currentData(),))
            name = cur.fetchone()
            if (name):
                self.uiFunctionCombo.setCurrentText(name[0])
            else:
                self.uiFunctionCombo.setCurrentIndex(-1)
            self.uiFunctionCombo.blockSignals(False)

            cur = self.conn.cursor()
            cur.execute('SELECT points FROM terms WHERE id = %s;', (self.uiTerms2Combo.currentData(),))
            points = cur.fetchone()
            if (points):
                self.uiPointsEdit.setText('%s' % points[0])

            cur = self.conn.cursor()
            cur.execute('SELECT validated FROM terms WHERE id = %s;', (self.uiTerms2Combo.currentData(),))
            state = cur.fetchone()
            if (state[0] == True):
                self.uiTermVerifiedCheck.setChecked(True);

        self.uiRenameTermButton.setEnabled(True)
        self.uiDeleteTermButton.setEnabled(True)
        self.uiTermVerifiedCheck.setEnabled(True)
        self.uiPointsEdit.setEnabled(True)
        self.uiFunctionCombo.setEnabled(True)

    def onCreateTermClicked(self):
        self.currentTerm = -1
        self.uiTerms2Combo.setCurrentIndex(-1)
        self.uiTerms2Combo.setEditable(True)
        self.uiTerms2Combo.lineEdit().returnPressed.connect(self.onTermEntered)
        self.uiTerms2Combo.setFocus()
        self.uiCreateTermButton.setEnabled(False)

    def onRenameTermClicked(self):
        self.currentTerm = self.uiTerms2Combo.currentIndex()
        self.uiTerms2Combo.setEditable(True)
        self.uiTerms2Combo.lineEdit().returnPressed.connect(self.onTermEntered)
        self.uiTerms2Combo.setFocus()
        self.uiCreateTermButton.setEnabled(False)
        self.uiRenameTermButton.setEnabled(False)
        self.uiDeleteTermButton.setEnabled(False)

    def onTermEntered(self):
        self.uiTerms2Combo.setEditable(False)
        self.uiCreateTermButton.setEnabled(True)
        self.uiRenameTermButton.setEnabled(True)
        self.uiDeleteTermButton.setEnabled(True)
        if (self.currentTerm >= 0):
            name = self.uiTerms2Combo.currentText()
            self.uiTerms2Combo.removeItem(self.uiTerms2Combo.currentIndex())
            if (self.uiTerms2Combo.itemText(self.currentTerm) != name):
                self.uiTerms2Combo.setItemText(self.currentTerm, name)
                self.termRenamed = True
                self.uiTerms2Combo.setCurrentIndex(self.currentTerm)
                self.checkPoints()
            else:
                self.uiTerms2Combo.setCurrentIndex(self.currentTerm)
        else:
            self.uiTerms2Combo.setItemData(self.uiTerms2Combo.currentIndex(), 0)
            self.onTerm2Selected()
            self.uiFunctionCombo.setFocus()

    def onDeleteTermClicked(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM terms WHERE id = %s;', (self.uiTerms2Combo.currentData(),))
        self.conn.commit()
        cur.close()
        self.uiTerms2Combo.removeItem(self.uiTerms2Combo.currentIndex())

    def checkPoints(self):
        if (self.uiPointsEdit.text() != ''):
            self.uiCommitTermButton.setEnabled(True)
        else:
            self.uiCommitTermButton.setEnabled(False)

    def onTermVerified(self):
        self.checkPoints()

    def onFunctionSelected(self):
        if (self.uiFunctionCombo.currentIndex() != -1):
            self.checkPoints()

    def commitTerm(self):
        self.uiCommitTermButton.setEnabled(False)
        cur = self.conn.cursor()
        term_id = self.uiTerms2Combo.currentData()
        if (term_id):
            cur.execute('UPDATE terms SET validated = %s, function_id = %s, points = %s WHERE id = %s;', (self.uiTermVerifiedCheck.isChecked(), self.uiFunctionCombo.currentData(), self.uiPointsEdit.text(), term_id))
            if (self.termRenamed == True):
                cur.execute('UPDATE terms SET name = %s WHERE id = %s;', (self.uiTerms2Combo.currentText(), term_id))
        else:
            cur.execute('INSERT INTO groups (is_variable, is_term, is_hedge) VALUES (false, true, false) RETURNING id;')
            group_id = cur.fetchone()[0]
            for lemma in self.uiTerms2Combo.currentText().replace(' ', '').split(','):
                cur.execute('INSERT INTO synonims (group_id, lemma, grammemes, hits) VALUES (%s, %s, %s, 0);', (group_id, lemma, ''));
            cur.execute('INSERT INTO terms (validated, name, name_id, function_id, points) VALUES (%s, '', %s, %s, %s) RETURNING id;', (self.uiTermVerifiedCheck.isChecked(), group_id, self.uiFunctionCombo.currentData(), self.uiPointsEdit.text()))
            term_id = cur.fetchone()[0]
            self.uiTerms2Combo.setItemData(self.uiTerms2Combo.currentIndex(), term_id)
        self.conn.commit()
        cur.close()

    # Actions on hedges tab

    def onHedge2Selected(self):
        if (self.uiHedges2Combo.isEditable() == True):
            return

        self.uiCommitHedgeButton.setEnabled(False)
        self.uiHedgeVerifiedCheck.setChecked(False)
        self.uiResultEdit.clear()

        if (self.uiHedges2Combo.currentIndex() == -1):
            self.uiRenameHedgeButton.setEnabled(False)
            self.uiDeleteHedgeButton.setEnabled(False)
            self.uiHedgeVerifiedCheck.setEnabled(False)
            self.uiResultEdit.setEnabled(False)
            return

        if (self.uiHedges2Combo.currentData() != 0):
            cur = self.conn.cursor()
            cur.execute('SELECT result FROM hedges WHERE id = %s;', (self.uiHedges2Combo.currentData(),))
            result = cur.fetchone()
            if (result):
                self.uiResultEdit.setText('%s' % result[0])

            cur = self.conn.cursor()
            cur.execute('SELECT validated FROM hedges WHERE id = %s;', (self.uiHedges2Combo.currentData(),))
            state = cur.fetchone()
            if (state[0] == True):
                self.uiHedgeVerifiedCheck.setChecked(True);

        self.uiRenameHedgeButton.setEnabled(True)
        self.uiDeleteHedgeButton.setEnabled(True)
        self.uiHedgeVerifiedCheck.setEnabled(True)
        self.uiResultEdit.setEnabled(True)

    def onCreateHedgeClicked(self):
        self.currentHedge = -1
        self.uiHedges2Combo.setCurrentIndex(-1)
        self.uiHedges2Combo.setEditable(True)
        self.uiHedges2Combo.lineEdit().returnPressed.connect(self.onHedgeEntered)
        self.uiHedges2Combo.setFocus()
        self.uiCreateHedgeButton.setEnabled(False)

    def onRenameHedgeClicked(self):
        self.currentHedge = self.uiHedges2Combo.currentIndex()
        self.uiHedges2Combo.setEditable(True)
        self.uiHedges2Combo.lineEdit().returnPressed.connect(self.onHedgeEntered)
        self.uiHedges2Combo.setFocus()
        self.uiCreateHedgeButton.setEnabled(False)
        self.uiRenameHedgeButton.setEnabled(False)
        self.uiDeleteHedgeButton.setEnabled(False)

    def onHedgeEntered(self):
        self.uiHedges2Combo.setEditable(False)
        self.uiCreateHedgeButton.setEnabled(True)
        self.uiRenameHedgeButton.setEnabled(True)
        self.uiDeleteHedgeButton.setEnabled(True)
        if (self.currentHedge >= 0):
            name = self.uiHedges2Combo.currentText()
            self.uiHedges2Combo.removeItem(self.uiHedges2Combo.currentIndex())
            if (self.uiHedges2Combo.itemText(self.currentHedge) != name):
                self.uiHedges2Combo.setItemText(self.currentHedge, name)
                self.hedgeRenamed = True
                self.uiHedges2Combo.setCurrentIndex(self.currentHedge)
                self.checkResult()
            else:
                self.uiHedges2Combo.setCurrentIndex(self.currentHedge)
        else:
            self.uiHedges2Combo.setItemData(self.uiHedges2Combo.currentIndex(), 0)
            self.onHedge2Selected()
            self.uiResultEdit.setFocus()

    def onDeleteHedgeClicked(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM hedges WHERE id = %s;', (self.uiHedges2Combo.currentData(),))
        self.conn.commit()
        cur.close()
        self.uiHedges2Combo.removeItem(self.uiHedges2Combo.currentIndex())

    def checkResult(self):
        if (self.uiResultEdit.text() != ''):
            self.uiCommitHedgeButton.setEnabled(True)
        else:
            self.uiCommitHedgeButton.setEnabled(False)

    def onHedgeVerified(self):
        self.checkResult()

    def commitHedge(self):
        self.uiCommitHedgeButton.setEnabled(False)
        cur = self.conn.cursor()
        hedge_id = self.uiHedges2Combo.currentData()
        if (hedge_id):
            cur.execute('UPDATE hedges SET validated = %s, result = %s WHERE id = %s;', (self.uiHedgeVerifiedCheck.isChecked(), self.uiResultEdit.text(), hedge_id))
            if (self.hedgeRenamed == True):
                cur.execute('UPDATE hedges SET name = %s WHERE id = %s;', (self.uiHedges2Combo.currentText(), hedge_id))
        else:
            cur.execute('INSERT INTO groups (is_variable, is_term, is_hedge) VALUES (false, false, true) RETURNING id;')
            group_id = cur.fetchone()[0]
            for lemma in self.uiHedges2Combo.currentText().replace(' ', '').split(','):
                cur.execute('INSERT INTO synonims (group_id, lemma, grammemes, hits) VALUES (%s, %s, %s, 0);', (group_id, lemma, ''));
            cur.execute('INSERT INTO hedges (validated, name, name_id, result) VALUES (%s, '', %s, %s) RETURNING id;', (self.uiHedgeVerifiedCheck.isChecked(), group_id, self.uiResultEdit.text()))
            hedge_id = cur.fetchone()[0]
            self.uiHedges2Combo.setItemData(self.uiHedges2Combo.currentIndex(), hedge_id)
        self.conn.commit()
        cur.close()

    # Actions on rules tab

    def loadTree(self, tree, name, rule_id):
        cur = self.conn.cursor()
        query = 'SELECT nodes.id, types.name FROM rules, nodes, types WHERE rules.%s_id = nodes.id' % name
        cur.execute(query + ' AND rules.id = %s AND types.id = nodes.type_id;', (rule_id,))
        root = cur.fetchone()
        cur.close()
        if (root):
            item = QTreeWidgetItem()
            item.setText(0, '(%s)' % root[1])
            item.setText(1, '%s' % root[0])
            tree.addTopLevelItem(item)
            cur = self.conn.cursor()
            cur.execute('SELECT nodes.id, nodes.parent_id, types.name, types.id FROM nodes, types, closures WHERE nodes.id = closures.descendant_id AND closures.ancestor_id = %s AND nodes.type_id = types.id AND nodes.parent_id IS NOT NULL ORDER BY nodes.parent_id ASC, types.id ASC;', (root[0],))
            nodes = cur.fetchall()
            cur.close()
            for node in nodes:
                if (node[2] in ('variable', 'term', 'hedge')):
                    cur = self.conn.cursor()
                    query = 'SELECT %ss.name_id, %ss.name FROM %ss, nodes WHERE %ss.id = nodes.%s_id' % (node[2], node[2], node[2], node[2], node[2])
                    cur.execute(query + ' AND nodes.id = %s;', (node[0],))
                    row = cur.fetchone()
                    if (row[1] != ''):
                        name = '(%s) ' % node[2] + row[1]
                    else:
                        name = '(%s) ' % node[2] + ', '.join(self.getLemmas(row[0])) 
                    cur.close()
                else:
                    name = '(%s)' % node[2]
                parents = tree.findItems('%s' % node[1], Qt.MatchExactly | Qt.MatchRecursive, 1)
                item = QTreeWidgetItem()
                item.setText(0, '%s' % name)
                item.setText(1, '%s' % node[0])
                parents[0].addChild(item)

    def nodeToString(self, node):
        cur = self.conn.cursor()
        cur.execute('SELECT types.name FROM nodes, types WHERE nodes.type_id = types.id AND nodes.id = %s;', (node.text(1),))
        name = cur.fetchone()[0]
        cur.close()
        if (name in ('variable', 'term', 'hedge')):
            cur = self.conn.cursor()
            query = 'SELECT %ss.name_id, %ss.name FROM %ss, nodes WHERE %ss.id = nodes.%s_id' % (name, name, name, name, name)
            cur.execute(query + ' AND nodes.id = %s;', (node.text(1),))
            row = cur.fetchone()
            if (row[1] != ''):
                token = '\'' + row[1] + '\''
            else:
                token = '\'' + ', '.join(self.getLemmas(row[0])) + '\''
            cur.close()
        elif (name == 'variable_and'):
            token = '%s AND %s' % (self.nodeToString(node.child(0)), self.nodeToString(node.child(1)))
        elif (name == 'variable_or'):
            token = '%s OR %s' % (self.nodeToString(node.child(0)), self.nodeToString(node.child(1)))
        elif (name == 'variable_value'):
            token = '%s IS %s' % (self.nodeToString(node.child(0)), self.nodeToString(node.child(1)))
        elif (name == 'term_complex'):
            token = '%s %s' % (self.nodeToString(node.child(0)), self.nodeToString(node.child(1)))
        else:
            token = ''
        return token

    def onRuleSelected(self):
        if (self.uiRulesCombo.isEditable() == True):
            return

        self.uiCommitRuleButton.setEnabled(False)
        self.uiRuleVerifiedCheck.setChecked(False)
        self.uiAntecedentTree.clear()
        self.uiAntecedentEdit.clear()
        self.uiAntecedentEdit.setEnabled(False)
        self.uiConsequentTree.clear()
        self.uiConsequentEdit.clear()
        self.uiConsequentEdit.setEnabled(False)

        if (self.uiRulesCombo.currentIndex() == -1):
            self.uiRenameRuleButton.setEnabled(False)
            self.uiDeleteRuleButton.setEnabled(False)
            self.uiRuleVerifiedCheck.setEnabled(False)
            self.uiAntecedentNodeTypesCombo.setEnabled(False)
            self.uiAntecedentNodesCombo.setEnabled(False)
            self.uiAddAntecedentNodeButton.setEnabled(False)
            self.uiAntecedentTree.setEnabled(False)
            self.uiConsequentNodeTypesCombo.setEnabled(False)
            self.uiConsequentNodesCombo.setEnabled(False)
            self.uiAddConsequentNodeButton.setEnabled(False)
            self.uiConsequentTree.setEnabled(False)
            return

        if (self.uiRulesCombo.currentData() != 0):

            cur = self.conn.cursor()
            cur.execute('SELECT validated FROM rules WHERE id = %s;', (self.uiRulesCombo.currentData(),))
            state = cur.fetchone()
            if (state[0] == True):
                self.uiRuleVerifiedCheck.setChecked(True);

            self.loadTree(self.uiAntecedentTree, 'antecedent', self.uiRulesCombo.currentData())
            self.loadTree(self.uiConsequentTree, 'consequent', self.uiRulesCombo.currentData())

            if (self.uiAntecedentTree.topLevelItemCount() == 0):
                self.uiAntecedentNodeTypesCombo.setEnabled(True)

            if (self.uiConsequentTree.topLevelItemCount() == 0):
                self.uiConsequentNodeTypesCombo.setEnabled(True)

            self.uiRenameRuleButton.setEnabled(True)
            self.uiDeleteRuleButton.setEnabled(True)
            self.uiRuleVerifiedCheck.setEnabled(True)
            self.uiAntecedentTree.setEnabled(True)
            self.uiConsequentTree.setEnabled(True)

    def onCreateRuleClicked(self):
        self.uiRulesCombo.setCurrentIndex(-1)
        self.uiRulesCombo.setEditable(True)
        self.uiRulesCombo.lineEdit().returnPressed.connect(self.onRuleEntered)
        self.uiRulesCombo.setFocus()
        self.uiCreateRuleButton.setEnabled(False)

    def onRenameRuleClicked(self):
        self.currentRule = self.uiRulesCombo.currentIndex()
        self.uiRulesCombo.setEditable(True)
        self.uiRulesCombo.lineEdit().returnPressed.connect(self.onRuleEntered)
        self.uiRulesCombo.setFocus()
        self.uiCreateRuleButton.setEnabled(False)
        self.uiRenameRuleButton.setEnabled(False)
        self.uiDeleteRuleButton.setEnabled(False)

    def onRuleEntered(self):
        self.uiRulesCombo.setEditable(False)
        self.uiCreateRuleButton.setEnabled(True)
        self.uiRenameRuleButton.setEnabled(True)
        self.uiDeleteRuleButton.setEnabled(True)
        if (self.currentRule >= 0):
            name = self.uiRulesCombo.currentText()
            self.uiRulesCombo.removeItem(self.uiRulesCombo.currentIndex())
            if (self.uiRulesCombo.itemText(self.currentRule) != name):
                self.uiRulesCombo.setItemText(self.currentRule, name)
                self.uiRulesCombo.setCurrentIndex(self.currentRule)
                self.commitRule()
            else:
                self.uiRulesCombo.setCurrentIndex(self.currentRule)
        else:
            self.uiRulesCombo.setItemData(self.uiRulesCombo.currentIndex(), 0)
            self.onRuleSelected()

    def onDeleteRuleClicked(self):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM rules WHERE id = %s;', (self.uiRulesCombo.currentData(),))
        self.conn.commit()
        cur.close()
        self.uiRulesCombo.removeItem(self.uiRulesCombo.currentIndex())

    def onAntecedentNodeTypeSelected(self):
        self.uiAntecedentNodesCombo.clear()
        self.uiAntecedentNodesCombo.setEnabled(False)
        if (self.uiAntecedentNodeTypesCombo.currentIndex() == -1):
            return
        self.uiAntecedentNodesCombo.blockSignals(True)
        if (self.uiAntecedentNodeTypesCombo.currentText() in ('variable', 'term', 'hedge')):
            self.fillComboWithLemmas(self.uiAntecedentNodesCombo, self.uiAntecedentNodeTypesCombo.currentText() + 's')
            self.uiAntecedentNodesCombo.setEnabled(True)
            self.uiAddAntecedentNodeButton.setEnabled(False)
        else:
            self.uiAddAntecedentNodeButton.setEnabled(True)
        self.uiAntecedentNodesCombo.blockSignals(False)

    def onAntecedentNodeValueSelected(self):
        if (self.uiAntecedentNodesCombo.currentIndex() != -1):
            self.uiAddAntecedentNodeButton.setEnabled(True)

    def onAddAntecedentNodeClicked(self):
        parent_id = None
        variable_id = None
        term_id = None
        hedge_id = None
        if (self.uiAntecedentTree.currentItem()):
            parent_id = self.uiAntecedentTree.currentItem().text(1)
        if (self.uiAntecedentNodeTypesCombo.currentText() == 'variable'):
            variable_id = self.uiAntecedentNodesCombo.currentData()
        elif (self.uiAntecedentNodeTypesCombo.currentText() == 'term'):
            term_id = self.uiAntecedentNodesCombo.currentData()
        elif (self.uiAntecedentNodeTypesCombo.currentText() == 'hedge'):
            hedge_id = self.uiAntecedentNodesCombo.currentData()
        cur = self.conn.cursor()
        cur.execute('INSERT INTO nodes (parent_id, type_id, variable_id, term_id, hedge_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;', (parent_id, self.uiAntecedentNodeTypesCombo.currentData(), variable_id, term_id, hedge_id))
        node_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        item = QTreeWidgetItem()
        if (self.uiAntecedentNodesCombo.isEnabled()):
            item.setText(0, '(%s) %s' % (self.uiAntecedentNodeTypesCombo.currentText(), self.uiAntecedentNodesCombo.currentText()))
        else:
            item.setText(0, '(%s)' % self.uiAntecedentNodeTypesCombo.currentText())
        item.setText(1, '%s' % node_id)
        if (self.uiAntecedentTree.currentItem()):
            self.uiAntecedentTree.currentItem().addChild(item)
        else:
            self.uiAntecedentTree.addTopLevelItem(item)
            self.uiAntecedentNodeTypesCombo.setCurrentIndex(-1)
            self.uiAntecedentNodeTypesCombo.setEnabled(False)
            self.uiAddAntecedentNodeButton.setEnabled(False)
        self.uiCommitRuleButton.setEnabled(True)

    def onAntecedentNodeSelected(self):
        self.uiAntecedentNodeTypesCombo.setEnabled(True)
        self.uiRemoveAntecedentNodeButton.setEnabled(True)
        self.uiAntecedentEdit.setEnabled(True)
        self.uiAntecedentEdit.setText(self.nodeToString(self.uiAntecedentTree.currentItem()))

    def onRemoveAntecedentNodeClicked(self):
        current = self.uiAntecedentTree.currentItem()
        if (current.parent()):
            current.parent().takeChild(current.parent().indexOfChild(current))
        else:
            self.uiAntecedentTree.takeTopLevelItem(self.uiAntecedentTree.indexOfTopLevelItem(current))
        if (self.uiAntecedentTree.topLevelItemCount() == 0):
            self.uiRemoveAntecedentNodeButton.setEnabled(False)
            self.uiAddAntecedentNodeButton.setEnabled(False)
            self.onAntecedentNodeTypeSelected()
        self.uiCommitRuleButton.setEnabled(True)

    def onConsequentNodeTypeSelected(self):
        self.uiConsequentNodesCombo.clear()
        self.uiConsequentNodesCombo.setEnabled(False)
        if (self.uiConsequentNodeTypesCombo.currentIndex() == -1):
            return
        self.uiConsequentNodesCombo.blockSignals(True)
        if (self.uiConsequentNodeTypesCombo.currentText() in ('variable', 'term', 'hedge')):
            self.fillComboWithLemmas(self.uiConsequentNodesCombo, self.uiConsequentNodeTypesCombo.currentText() + 's')
            self.uiConsequentNodesCombo.setEnabled(True)
            self.uiAddConsequentNodeButton.setEnabled(False)
        else:
            self.uiAddConsequentNodeButton.setEnabled(True)
        self.uiConsequentNodesCombo.blockSignals(False)

    def onConsequentNodeValueSelected(self):
        if (self.uiConsequentNodesCombo.currentIndex() != -1):
            self.uiAddConsequentNodeButton.setEnabled(True)

    def onAddConsequentNodeClicked(self):
        parent_id = None
        variable_id = None
        term_id = None
        hedge_id = None
        if (self.uiConsequentTree.currentItem()):
            parent_id = self.uiConsequentTree.currentItem().text(1)
        if (self.uiConsequentNodeTypesCombo.currentText() == 'variable'):
            variable_id = self.uiConsequentNodesCombo.currentData()
        elif (self.uiConsequentNodeTypesCombo.currentText() == 'term'):
            term_id = self.uiConsequentNodesCombo.currentData()
        elif (self.uiConsequentNodeTypesCombo.currentText() == 'hedge'):
            hedge_id = self.uiConsequentNodesCombo.currentData()
        cur = self.conn.cursor()
        cur.execute('INSERT INTO nodes (parent_id, type_id, variable_id, term_id, hedge_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;', (parent_id, self.uiConsequentNodeTypesCombo.currentData(), variable_id, term_id, hedge_id))
        node_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        item = QTreeWidgetItem()
        if (self.uiConsequentNodesCombo.isEnabled()):
            item.setText(0, '(%s) %s' % (self.uiConsequentNodeTypesCombo.currentText(), self.uiConsequentNodesCombo.currentText()))
        else:
            item.setText(0, '(%s)' % self.uiConsequentNodeTypesCombo.currentText())
        item.setText(1, '%s' % node_id)
        if (self.uiConsequentTree.currentItem()):
            self.uiConsequentTree.currentItem().addChild(item)
        else:
            self.uiConsequentTree.addTopLevelItem(item)
            self.uiConsequentNodeTypesCombo.setCurrentIndex(-1)
            self.uiConsequentNodeTypesCombo.setEnabled(False)
            self.uiAddConsequentNodeButton.setEnabled(False)
        self.uiCommitRuleButton.setEnabled(True)

    def onConsequentNodeSelected(self):
        self.uiConsequentNodeTypesCombo.setEnabled(True)
        self.uiRemoveConsequentNodeButton.setEnabled(True)
        self.uiConsequentEdit.setEnabled(True)
        self.uiConsequentEdit.setText(self.nodeToString(self.uiConsequentTree.currentItem()))

    def onRemoveConsequentNodeClicked(self):
        current = self.uiConsequentTree.currentItem()
        if (current.parent()):
            current.parent().takeChild(current.parent().indexOfChild(current))
        else:
            self.uiConsequentTree.takeTopLevelItem(self.uiConsequentTree.indexOfTopLevelItem(current))
        if (self.uiConsequentTree.topLevelItemCount() == 0):
            self.uiRemoveConsequentNodeButton.setEnabled(False)
            self.uiAddConsequentNodeButton.setEnabled(False)
            self.onConsequentNodeTypeSelected()
        self.uiCommitRuleButton.setEnabled(True)

    def onRuleVerified(self):
        self.commitRule()

    def commitRule(self):
        self.uiCommitRuleButton.setEnabled(False)

    # Actions on debug tab

    def fillTable(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        self.uiDataTable.clear()
        self.uiDataTable.setRowCount(cur.rowcount)
        self.uiDataTable.setColumnCount(len(cur.description))
        self.uiDataTable.setHorizontalHeaderLabels([desc[0] for desc in cur.description])
        self.uiDataTable.setSortingEnabled(False)
        i = 0
        for row in rows:
            for j in range(0, len(row)):
                item = QTableWidgetItem('%s' % row[j])
                self.uiDataTable.setItem(i, j, item)
            i += 1
        cur.close()
        self.uiDataTable.setSortingEnabled(True)

    def onModeSelected(self):
        if (self.uiModeCombo.currentData() == 0):
            self.fillTable('SELECT variables.id, variables.name, variables.name_id, variables.min, variables.max, variables.validated FROM variables;')
        elif (self.uiModeCombo.currentData() == 1):
            self.fillTable('SELECT terms.id, terms.name, terms.name_id, functions.name, terms.points, terms.validated FROM terms, functions WHERE terms.function_id = functions.id;')
        elif (self.uiModeCombo.currentData() == 2):
            self.fillTable('SELECT hedges.id, hedges.name, hedges.name_id, hedges.result, hedges.validated FROM hedges;')
        elif (self.uiModeCombo.currentData() == 3):
            self.fillTable('SELECT variables.id, variables.name, variables.name_id, variables.min, variables.max, variables.validated, terms.id, terms.name, terms.name_id, functions.name, terms.points, terms.validated FROM variables, terms, functions, variables_terms WHERE variables.id = variables_terms.variable_id AND terms.id = variables_terms.term_id AND terms.function_id = functions.id;')
        elif (self.uiModeCombo.currentData() == 4):
            self.fillTable('SELECT variables.id, variables.name, variables.name_id, variables.min, variables.max, variables.validated, hedges.id, hedges.name, hedges.name_id, hedges.result, hedges.validated FROM variables, hedges, variables_hedges WHERE variables.id = variables_hedges.variable_id AND hedges.id = variables_hedges.hedge_id;')
        elif (self.uiModeCombo.currentData() == 5):
            self.fillTable('SELECT synonims.id, synonims.group_id, synonims.lemma, synonims.grammemes, synonims.hits, groups.is_variable, groups.is_term, groups.is_hedge FROM synonims, groups WHERE synonims.group_id = groups.id;')

    # Actions on main window

    def onTabChanged(self):
        if (self.uiTabs.currentIndex() == 0):
            self.loadTerms()
            self.loadHedges()
            self.onVariableSelected()

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Window(addr=sys.argv[1])
    widget.show()
    sys.exit(app.exec_())
