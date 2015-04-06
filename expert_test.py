#!/usr/bin/env python

from expert import Window

import sys
import argparse
import unittest

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest

class tests(unittest.TestCase):
    def test_variables(self):
        self.assertEqual(window.uiTabs.currentIndex(), 0)
        self.assertEqual(window.uiVariablesCombo.currentIndex(), -1)
        self.assertEqual(window.uiCreateVariableButton.isEnabled(), True)
        self.assertEqual(window.uiRenameVariableButton.isEnabled(), False)
        self.assertEqual(window.uiDeleteVariableButton.isEnabled(), False)
    
    def test_ranges(self):
        self.assertEqual(window.uiRangeMinEdit.isEnabled(), False)
        self.assertEqual(window.uiRangeMinEdit.text(), '')
        self.assertEqual(window.uiRangeMaxEdit.isEnabled(), False)
        self.assertEqual(window.uiRangeMaxEdit.text(), '')

    def test_terms(self):
        self.assertEqual(window.uiTermsCombo.currentIndex(), -1)
        self.assertEqual(window.uiTermsCombo.isEnabled(), False)
        self.assertEqual(window.uiTermsList.count(), 0)
        self.assertEqual(window.uiTermsList.isEnabled(), False)
        self.assertEqual(window.uiAddTermButton.isEnabled(), False)
        self.assertEqual(window.uiRemoveTermButton.isEnabled(), False)

    def test_hedges(self):
        self.assertEqual(window.uiHedgesCombo.currentIndex(), -1)
        self.assertEqual(window.uiHedgesCombo.isEnabled(), False)
        self.assertEqual(window.uiHedgesList.count(), 0)
        self.assertEqual(window.uiHedgesList.isEnabled(), False)
        self.assertEqual(window.uiAddHedgeButton.isEnabled(), False)
        self.assertEqual(window.uiRemoveHedgeButton.isEnabled(), False)

    def test_commit(self):
        self.assertEqual(window.uiCommitVariableButton.isEnabled(), False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-a', dest='address', default='127.0.0.1:5432')
    parser.add_argument('-d', dest='database', default='db')
    parser.add_argument('-u', dest='username', default='user')
    parser.add_argument('-p', dest='password', default='pass')
    opts = parser.parse_args()
    app = QApplication(sys.argv)
    window = Window(host=opts.address.split(':')[0], port=opts.address.split(':')[1], 
            database=opts.database, username=opts.username, password=opts.password)
    runner = unittest.TextTestRunner()
    itersuite = unittest.TestLoader().loadTestsFromTestCase(tests)
    runner.run(itersuite)
