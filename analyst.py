import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.uic import loadUi
#import psycopg2
import urllib3


class Window(QMainWindow):
    def __init__(self, *args,host,port):  
        super(Window, self).__init__(*args)

       
        loadUi('fuzzy.ui', self)
        
        #Initialize
        
        self.fillComboVar(self.comboBoxInVar, 'variables')
        self.comboBoxInVar.currentIndexChanged.connect(self.onVariableSelected)
        
    def fillComboVar(self,combo,table):
        combo.clear()
        conn = urllib3.connection_from_url('http://127.0.0.1:5000/')
        r = conn.request('GET', '/api/variables')
        data = json.loads(r.data.decode('utf-8'))
        for variable in data ['variables']:
            combo.addItem(variable['name'],variable['id'])
        combo.setCurrentIndex(-1)
     
    def onVariableSelected(self):
        if (self.comboBoxInVar.isEditable() == True):
            return  
         
        self.comboBoxOutVar.setCurrentIndex(-1)
        self.pushButtonAddInVar.setEnabled(True)
        self.pushButtonSend.setEnabled(False)
        self.lineEditMax.clear()
        self.lineEditMin.clear()
        #self.listViewInVar.clear()
        
