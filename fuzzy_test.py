#!/usr/bin/env python

from fuzzy import Window

import sys
import unittest

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest

class case(unittest.TestCase):
    def test_one(self):
        self.assertEqual(window.uiTabs.currentIndex(), 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    unittest.main()
