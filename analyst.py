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
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QFont
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
        self.uiRemoveValueButton.clicked.connect(self.onRemoveValueClicked)
        self.uiClearValueButton.clicked.connect(self.onClearValueClicked)

        self.uiValuesTable.clear()
        self.uiValuesTable.setRowCount(0)
        self.uiValuesTable.setColumnCount(2)
        self.uiValuesTable.setHorizontalHeaderLabels(('Имя', 'Значение'))

        self.uiCommitTaskButton.clicked.connect(self.onCommitTaskClicked)

        # Initialize results tab

        self.uiTaskCombo.currentIndexChanged.connect(self.onTaskChanged)
        self.uiClearButton.clicked.connect(self.clearTasks)

        self.uiVariablesTable.itemSelectionChanged.connect(self.drawSelected)
        self.uiRulesTable.itemSelectionChanged.connect(self.drawSelected)

        self.uiTabs.setCurrentIndex(0)
        self.uiTabs.currentChanged.connect(self.onTabChanged)
        self.task = -1

    def fillVariableCombo(self, combo):
        combo.blockSignals(True)
        combo.clear()
        r = self.conn.request('GET', '/api/variables')
        data = json.loads(r.data.decode('utf-8'))
        for variable in data['variables']:
            combo.addItem(variable['name'], variable['id'])
        combo.setCurrentIndex(-1)
        combo.blockSignals(False)
     
    def fillTaskCombo(self):

        self.uiClearButton.setEnabled(False)
        self.uiTaskCombo.blockSignals(True)
        self.uiTaskCombo.clear()
        index = -1

        r = self.conn.request('GET', '/api/tasks')
        if r.status == 200:
            data = json.loads(r.data.decode('utf-8'))
            for task in data['tasks']:
                self.uiTaskCombo.addItem('%s [%s] (%s - %s)' % (task['id'], task['status'], task['started'], task['finished']), task['id'])
            if self.task != -1:
                index = self.uiTaskCombo.findData(self.task)
                self.task = -1
            self.uiClearButton.setEnabled(True)

        self.uiTaskCombo.setCurrentIndex(index)
        self.uiTaskCombo.blockSignals(False)
        self.onTaskChanged()

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
        self.uiRemoveValueButton.setEnabled(True)
        self.uiClearValueButton.setEnabled(True)
        
        
    def onRemoveValueClicked(self):
        #self.uiValuesTable.takeItem(self.uiValuesTable.currentRow(),0)
        #self.uiValuesTable.takeItem(self.uiValuesTable.currentRow(),1)
        self.uiValuesTable.removeRow(self.uiValuesTable.currentRow())
        if (self.uiValuesTable.rowCount() == 0):
            self.uiRemoveValueButton.setEnabled(False)
            self.uiClearValueButton.setEnabled(False)
    
    def onClearValueClicked(self):
        while (self.uiValuesTable.rowCount() > 0):
            self.uiValuesTable.removeRow(0)
        if (self.uiValuesTable.rowCount() == 0):
            self.uiClearValueButton.setEnabled(False)
            self.uiClearValueButton.setEnabled(False)    
            
            
        
        
        
        
        
        
        
        
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

    def drawAxis(self, data, points):

        xmin = data['xmin']
        xmax = data['xmax']
        ymin = data['ymin']
        ymax = data['ymax']
        xmarg = data['xmarg']
        ymarg = data['xmarg']
        xscale = data['xscale']
        yscale = data['yscale']

        scene = self.uiFunctionGraph.scene()

        scene.addLine(xmarg - 10, ymarg + 10, (xmax - xmin) * xscale + xmarg + 10, ymarg + 10)
        scene.addLine((xmax - xmin) * xscale + xmarg + 8, ymarg + 8, (xmax - xmin) * xscale + xmarg + 10, ymarg + 10)
        scene.addLine((xmax - xmin) * xscale + xmarg + 8, ymarg + 13, (xmax - xmin) * xscale + xmarg + 10, ymarg + 11)
        scene.addLine(xmarg - 10, ymarg + 10, xmarg - 10, (ymax - ymin) * yscale + ymarg - 10)
        scene.addLine(xmarg - 8, (ymax - ymin) * yscale + ymarg - 9, xmarg - 10, (ymax - ymin) * yscale + ymarg - 11)
        scene.addLine(xmarg - 12, (ymax - ymin) * yscale + ymarg - 8, xmarg - 10, (ymax - ymin) * yscale + ymarg - 10)

        y = ymin
        step = (ymax - ymin) / 4
        for i in range(5):
            scene.addLine(xmarg - 12, (y - ymin) * yscale + ymarg, xmarg - 8, (y - ymin) * yscale + ymarg)
            text = QGraphicsTextItem()
            text.setPos(0, (y - ymin) * yscale + ymarg - 7)
            text.setPlainText('%s' % format(round(y, 3), '.3f'))
            text.setFont(QFont('Sans', 6))
            scene.addItem(text)
            y += step
        
        x = xmin
        step = (xmax - xmin) / 19
        for i in range(20):
            scene.addLine((x - xmin) * xscale + xmarg, ymarg + 8, (x - xmin) * xscale + xmarg, ymarg + 12)
            text = QGraphicsTextItem()
            text.setPos((x - xmin) * xscale + xmarg - 14, ymarg + 10)
            text.setPlainText('%s' % format(round(x, 3), '.3f'))
            text.setFont(QFont('Sans', 6))
            scene.addItem(text)
            x += step

    def drawGraph(self, data, points):

        xmin = data['xmin']
        xmax = data['xmax']
        ymin = data['ymin']
        ymax = data['ymax']
        xmarg = data['xmarg']
        ymarg = data['xmarg']
        xscale = data['xscale']
        yscale = data['yscale']

        scene = self.uiFunctionGraph.scene()

        func = QPainterPath(QPointF(xmarg, (points[0]['grade'] - ymin) * yscale + ymarg))
        for point in points:
            func.lineTo((point['arg'] - xmin) * xscale + xmarg, (point['grade'] - ymin) * yscale + ymarg)
        scene.addPath(func)

    def drawPoint(self, data, x, y):

        xmin = data['xmin']
        xmax = data['xmax']
        ymin = data['ymin']
        ymax = data['ymax']
        xmarg = data['xmarg']
        ymarg = data['xmarg']
        xscale = data['xscale']
        yscale = data['yscale']

        scene = self.uiFunctionGraph.scene()

        scene.addLine(xmarg, (y - ymin) * yscale + ymarg, (xmax - xmin) * xscale + xmarg, (y - ymin) * yscale + ymarg, QPen(Qt.DashLine))
        scene.addLine((x - xmin) * xscale + xmarg, ymarg, (x - xmin) * xscale + xmarg, (ymax - ymin) * yscale + ymarg, QPen(Qt.DashLine))

    def prepareView(self, points, x):
        xmin = points[0]['arg']
        xmax = points[-1]['arg']
        ymin = 1.0
        ymax = 0.0
        for point in points:
            ymin = min(ymin, point['grade'])
            ymax = max(ymax, point['grade'])
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        xmarg = 40
        ymarg = 25
        xscale = (self.uiFunctionGraph.width() - xmarg * 2) / (xmax - xmin)
        yscale = -1 * (self.uiFunctionGraph.height() - ymarg * 2) / (ymax - ymin)
        return {
            'xmin': xmin,
            'xmax': xmax,
            'ymin': ymin,
            'ymax': ymax,
            'xmarg': xmarg,
            'ymarg': ymarg,
            'xscale': xscale,
            'yscale': yscale
        }

    def onTaskChanged(self):

        self.uiVariablesTable.clear()
        self.uiVariablesTable.setRowCount(0)
        self.uiVariablesTable.setColumnCount(0)
        self.uiVariablesTable.setEnabled(False)
        self.uiRulesTable.clear()
        self.uiRulesTable.setRowCount(0)
        self.uiRulesTable.setColumnCount(0)
        self.uiRulesTable.setEnabled(False)
        if not self.uiFunctionGraph.scene():
            self.uiFunctionGraph.setScene(QGraphicsScene())
        self.uiFunctionGraph.scene().clear()
        self.uiFunctionGraph.show()
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
            item.setData(Qt.UserRole, crisp['variable_id'])
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
            item.setData(Qt.UserRole, cutoff['rule_id'])
            self.uiRulesTable.setItem(i, 0, item)
            item = QTableWidgetItem('%s' % cutoff['value'])
            self.uiRulesTable.setItem(i, 1, item)
            i += 1
        self.uiRulesTable.setSortingEnabled(True)
        for i in range(self.uiRulesTable.columnCount()):
            self.uiRulesTable.setColumnWidth(i, self.uiRulesTable.width() / self.uiRulesTable.columnCount() - 1)
        self.uiRulesTable.setEnabled(True)
        
        self.drawSelected()

    def drawSelected(self):

        self.uiFunctionGraph.scene().clear()
        self.uiFunctionGraph.update()
        self.uiFunctionGraph.setEnabled(False)

        task_id = self.uiTaskCombo.currentData()
        r = self.conn.request('GET', '/api/tasks/%s' % task_id)
        task = json.loads(r.data.decode('utf-8'))

        rows = []
        for index in self.uiRulesTable.selectedIndexes():
            if not index.row() in rows:
                rows.append(index.row())

        if self.uiVariablesTable.currentRow() != -1 and len(rows) > 0:
    
            variable_id = self.uiVariablesTable.item(self.uiVariablesTable.currentRow(), 0).data(Qt.UserRole)

            need_axis = True

            for row in rows:

                rule_id = self.uiRulesTable.item(row, 0).data(Qt.UserRole)

                for crisp in task['task']['crisps']:
                    if crisp['variable_id'] == variable_id:
                        x = crisp['value']
                        break

                r = self.conn.request('GET', '/api/rules/%s/variables/%s/%s' % (rule_id, variable_id, x))
                if r.status != 200:
                    return
                res = json.loads(r.data.decode('utf-8'))

                data = self.prepareView(res['points'], x)

                if need_axis:
                    self.drawAxis(data, res['points'])
                    need_axis = False

                self.drawGraph(data, res['points'])
                self.drawPoint(data, x, res['grade'])

        else:

            if task['task']['status'] != 200:
                return

            x = None
            for crisp in task['task']['crisps']:
                if not crisp['is_input']:
                    x = crisp['value']
                    break

            data = self.prepareView(task['task']['points'], x)

            self.drawAxis(data, task['task']['points'])
            self.drawGraph(data, task['task']['points'])

            dividend = divisor = 0.0
            for point in task['task']['points']:
                dividend += (point['arg'] - data['xmin']) * point['grade']
                divisor += (point['arg'] - data['xmin'])
            y = round(dividend / divisor, 3)

            self.drawPoint(data, x, y)

        self.uiFunctionGraph.update()
        self.uiFunctionGraph.setEnabled(True)

    def clearTasks(self):

        r = self.conn.request('DELETE', '/api/tasks')
        self.fillTaskCombo()

    def onTabChanged(self):

        if self.uiTabs.currentIndex() == 0:
            self.task = self.uiTaskCombo.currentData()
        elif self.uiTabs.currentIndex() == 1:
            self.fillTaskCombo()
