#!/usr/bin/env python

import urllib3
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class Window(QMainWindow):
    def __init__(self, *args, host, port):  
        super(Window, self).__init__(*args)

        loadUi('analyst.ui', self)
        
        self.conn = urllib3.connection_from_url('http://%s:%s/' % (host, port))

        #Initialize
        
        self.fillCombo(self.uiInputCombo)
        self.fillCombo(self.uiOutputCombo)
#        self.comboBoxInVar.currentIndexChanged.connect(self.onVariableSelected)

    def fillCombo(self, combo):
        combo.clear()
        r = self.conn.request('GET', '/api/variables')
        data = json.loads(r.data.decode('utf-8'))
        for variable in data['variables']:
            combo.addItem(variable['name'], variable['id'])
        combo.setCurrentIndex(-1)
     
#    def onVariableSelected(self):
#        if (self.comboBoxInVar.isEditable() == True):
#            return  
#         
#        self.comboBoxOutVar.setCurrentIndex(-1)
#        self.pushButtonAddInVar.setEnabled(True)
#        self.pushButtonSend.setEnabled(False)
#        self.lineEditMax.clear()
#        self.lineEditMin.clear()
        #self.listViewInVar.clear()
        
