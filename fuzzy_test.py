#!/usr/bin/env python

from fuzzy import Window

import sys
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
    app = QApplication(sys.argv)
    window = Window(addr='78.107.239.213')
    unittest.main()
