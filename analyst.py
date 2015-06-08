#!/usr/bin/env python

import urllib3
import json
from random import random 

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self, *args, host, port):  
        super(Window, self).__init__(*args)

        loadUi('analyst.ui', self)
        
        self.conn = urllib3.connection_from_url('http://%s:%s/' % (host, port))
        self.pool = urllib3.PoolManager()
        self.addr = 'http://%s:%s' % (host, port)

        #Initialize
        
        self.fillVariableCombo(self.uiInputCombo)
        self.fillVariableCombo(self.uiOutputCombo)
        self.uiInputCombo.currentIndexChanged.connect(self.onInputVariableSelected)
        self.uiOutputCombo.currentIndexChanged.connect(self.onOutputVariableSelected)
        self.uiValueEdit.textEdited.connect(self.onValueChanged)
        self.uiAddValueButton.clicked.connect(self.onAddValueClicked)

        self.uiValuesTable.clear()
        self.uiValuesTable.setRowCount(0)
        self.uiValuesTable.setColumnCount(2)
        self.uiValuesTable.setHorizontalHeaderLabels(('Имя', 'Значение'))

        self.uiCommitTaskButton.clicked.connect(self.onCommitTaskClicked)

        # Initialize results tab

        self.uiTaskCombo.currentIndexChanged.connect(self.onTaskChanged)
    
        self.uiTabs.setCurrentIndex(0)
        self.uiTabs.currentChanged.connect(self.onTabChanged)
        self.task = -1

    def fillVariableCombo(self, combo):
        combo.clear()
        r = self.conn.request('GET', '/api/variables')
        data = json.loads(r.data.decode('utf-8'))
        for variable in data['variables']:
            combo.addItem(variable['name'], variable['id'])
        combo.setCurrentIndex(-1)
     
    def fillTaskCombo(self, combo):
        combo.clear()
        r = self.conn.request('GET', '/api/tasks')
        data = json.loads(r.data.decode('utf-8'))
        for task in data['tasks']:
            combo.addItem('%s [%s] (%s - %s)' % (task['id'], task['status'], task['started'], task['finished']), task['id'])
        index = -1
        if self.task != -1:
            index = combo.findData(self.task)
            self.task = -1
        combo.setCurrentIndex(index)

    def onInputVariableSelected(self):
        self.uiRangeMinEdit.clear()
        self.uiRangeMinEdit.setEnabled(False)
        self.uiRangeMaxEdit.clear()
        self.uiRangeMaxEdit.setEnabled(False)
        self.uiValueEdit.clear()
        self.uiValueEdit.setEnabled(False)

        if self.uiInputCombo.currentIndex() == -1:
            return

        r = self.conn.request('GET', '/api/variables/%s' % self.uiInputCombo.currentData())
        variable = json.loads(r.data.decode('utf-8'))
        self.uiRangeMinEdit.setText('%s' % variable['variable']['min'])
        self.uiRangeMinEdit.setEnabled(True)
        self.uiRangeMaxEdit.setText('%s' % variable['variable']['max'])
        self.uiRangeMaxEdit.setEnabled(True)
        self.uiValueEdit.setEnabled(True)
        self.uiValuesTable.setEnabled(True)

    def onOutputVariableSelected(self):
        self.uiCommitTaskButton.setEnabled(False)
        if self.uiOutputCombo.currentIndex() == -1:
            return
        if self.uiValuesTable.rowCount() > 0:
            self.uiCommitTaskButton.setEnabled(True)

    def onValueChanged(self):
        self.uiAddValueButton.setEnabled(True)

    def onAddValueClicked(self):
        rows = self.uiValuesTable.rowCount()
        self.uiValuesTable.setRowCount(rows + 1)
        item = QTableWidgetItem(self.uiInputCombo.currentText())
        item.setData(Qt.UserRole, self.uiInputCombo.currentData())
        self.uiValuesTable.setItem(rows, 0, item)
        item = QTableWidgetItem(self.uiValueEdit.text())
        self.uiValuesTable.setItem(rows, 1, item)
        self.uiValuesTable.setColumnWidth(0, self.uiValuesTable.width() / 3 * 2 - 1)
        self.uiValuesTable.setColumnWidth(1, self.uiValuesTable.width() / 3 - 1)
        self.uiOutputCombo.removeItem(self.uiInputCombo.currentIndex())
        self.uiOutputCombo.setCurrentIndex(-1)
        self.uiInputCombo.removeItem(self.uiInputCombo.currentIndex())
        self.uiInputCombo.setCurrentIndex(-1)
    
    def onCommitTaskClicked(self):
        self.uiCommitTaskButton.setEnabled(False)
        data = {}
        data['inputs'] = []
        for i in range(self.uiValuesTable.rowCount()):
            variable = self.uiValuesTable.item(i, 0).data(Qt.UserRole)
            value = float(self.uiValuesTable.item(i, 1).text())
            data['inputs'].append({'variable': variable, 'value': value})
        data['output'] = self.uiOutputCombo.currentData()
        r = self.pool.urlopen('POST', '%s/api/tasks' % self.addr, headers={'Content-Type': 'application/json'}, body=json.dumps(data))
        self.task = r.headers['Location'].split('/')[-1]
        self.uiTabs.setCurrentIndex(1)

    def onTaskChanged(self):
        self.uiVariablesTable.clear()
        self.uiVariablesTable.setEnabled(False)
        self.uiRulesTable.clear()
        self.uiRulesTable.setEnabled(False)
        if self.uiFunctionGraph.scene():
            self.uiFunctionGraph.scene().clear()
        self.uiFunctionGraph.setEnabled(False)

        if self.uiTaskCombo.currentIndex() == -1:
            return

        r = self.conn.request('GET', '/api/tasks/%s' % self.uiTaskCombo.currentData())
        task = json.loads(r.data.decode('utf-8'))
        self.uiVariablesTable.clear()
        self.uiVariablesTable.setRowCount(len(task['task']['crisps']))
        self.uiVariablesTable.setColumnCount(3)
        self.uiVariablesTable.setHorizontalHeaderLabels(('Имя', 'Значение', 'Входная'))
        self.uiVariablesTable.setSortingEnabled(False)
        i = 0
        for crisp in task['task']['crisps']:
            r = self.conn.request('GET', '/api/variables/%s' % crisp['variable_id'])
            variable = json.loads(r.data.decode('utf-8'))
            item = QTableWidgetItem('%s' % variable['variable']['name'])
            self.uiVariablesTable.setItem(i, 0, item)
            item = QTableWidgetItem('%s' % crisp['value'])
            self.uiVariablesTable.setItem(i, 1, item)
            item = QTableWidgetItem('%s' % crisp['is_input'])
            self.uiVariablesTable.setItem(i, 2, item)
            i += 1
        self.uiVariablesTable.setSortingEnabled(True)
        self.uiVariablesTable.sortByColumn(2, 1)
        for i in range(self.uiVariablesTable.columnCount()):
            self.uiVariablesTable.setColumnWidth(i, self.uiVariablesTable.width() / self.uiVariablesTable.columnCount() - 1)
        self.uiVariablesTable.setEnabled(True)

        self.uiRulesTable.clear()
        self.uiRulesTable.setRowCount(len(task['task']['cutoffs']))
        self.uiRulesTable.setColumnCount(2)
        self.uiRulesTable.setHorizontalHeaderLabels(('Название', 'Уровень отсечения'))
        self.uiRulesTable.setSortingEnabled(False)
        i = 0
        for cutoff in task['task']['cutoffs']:
            r = self.conn.request('GET', '/api/rules/%s' % cutoff['rule_id'])
            rule = json.loads(r.data.decode('utf-8'))
            item = QTableWidgetItem('%s' % rule['rule']['name'])
            self.uiRulesTable.setItem(i, 0, item)
            item = QTableWidgetItem('%s' % cutoff['value'])
            self.uiRulesTable.setItem(i, 1, item)
            i += 1
        self.uiRulesTable.setSortingEnabled(True)
        for i in range(self.uiRulesTable.columnCount()):
            self.uiRulesTable.setColumnWidth(i, self.uiRulesTable.width() / self.uiRulesTable.columnCount() - 1)
        self.uiRulesTable.setEnabled(True)

        scene = QGraphicsScene()
        xscale = (self.uiFunctionGraph.width() - 30) / task['task']['points'][-1]['arg'] - task['task']['points'][0]['arg'] 
        yscale = (self.uiFunctionGraph.height() - 30) / 1.0 * -1
        func = QPainterPath(QPointF(task['task']['points'][0]['arg'] * xscale, task['task']['points'][0]['grade'] * yscale))
        for point in task['task']['points']:
            func.lineTo(point['arg'] * xscale, point['grade'] * yscale);
        scene.addPath(func)
        #scene.addLine(0, 0, self.uiFunctionGraph.width(), self.uiFunctionGraph.height())
        self.uiFunctionGraph.setScene(scene)
        self.uiFunctionGraph.show()
        self.uiFunctionGraph.setEnabled(True)

    def onTabChanged(self):
        if (self.uiTabs.currentIndex() == 1):
            self.fillTaskCombo(self.uiTaskCombo)
