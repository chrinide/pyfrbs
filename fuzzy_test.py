#!/usr/bin/env python

from fuzzy import Window

import sys
import unittest

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest

class tests(unittest.TestCase):
    def test_variables_tab_initialization(self):
        self.assertEqual(window.uiTabs.currentIndex(), 0)
        self.assertEqual(window.uiVariablesCombo.currentIndex(), -1)
        self.assertEqual(window.uiCreateVariableButton.isEnabled(), True)
        self.assertEqual(window.uiRenameVariableButton.isEnabled(), False)
        self.assertEqual(window.uiDeleteVariableButton.isEnabled(), False)
        self.assertEqual(window.uiRangeMinEdit.isEnabled(), False)
        self.assertEqual(window.uiRangeMinEdit.text(), '')
        self.assertEqual(window.uiRangeMaxEdit.isEnabled(), False)
        self.assertEqual(window.uiRangeMaxEdit.text(), '')
        self.assertEqual(window.uiTermsCombo.currentIndex(), -1)
        self.assertEqual(window.uiTermsCombo.isEnabled(), False)
        self.assertEqual(window.uiTermsList.count(), 0)
        self.assertEqual(window.uiTermsList.isEnabled(), False)
        self.assertEqual(window.uiAddTermButton.isEnabled(), False)
        self.assertEqual(window.uiRemoveTermButton.isEnabled(), False)
        self.assertEqual(window.uiHedgesCombo.currentIndex(), -1)
        self.assertEqual(window.uiHedgesCombo.isEnabled(), False)
        self.assertEqual(window.uiHedgesList.count(), 0)
        self.assertEqual(window.uiHedgesList.isEnabled(), False)
        self.assertEqual(window.uiAddHedgeButton.isEnabled(), False)
        self.assertEqual(window.uiRemoveHedgeButton.isEnabled(), False)
        self.assertEqual(window.uiCommitVariableButton.isEnabled(), False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    unittest.main()