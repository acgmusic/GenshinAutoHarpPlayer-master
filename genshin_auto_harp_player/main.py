#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "acgmusic"
__version__ = "0.1.0"
 
import sys
from AutoHarpPlayer import AutoHarpPlayer
from PyQt5.QtWidgets import (QApplication)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoHarpPlayer()
    sys.exit(app.exec_())
