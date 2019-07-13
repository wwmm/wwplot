#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PySide2.QtWidgets import QApplication

from application_window import ApplicationWindow

APP = QApplication(sys.argv)
AW = ApplicationWindow()

sys.exit(APP.exec_())
