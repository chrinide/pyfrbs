#!/usr/bin/env python

from expert import Window

import sys
import argparse

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument('-a', dest='address', default='127.0.0.1:5432')
    parser.add_argument('-d', dest='database', default='db')
    parser.add_argument('-u', dest='username', default='user')
    parser.add_argument('-p', dest='password', default='pass')
    opts = parser.parse_args()
    app = QApplication(sys.argv)
    window = Window(host=opts.address.split(':')[0], port=opts.address.split(':')[1], 
            database=opts.database, username=opts.username, password=opts.password)
    window.show()
    sys.exit(app.exec_())
