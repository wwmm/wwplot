#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script that starts the application
"""

import sys
from PySide2.QtWidgets import QApplication
from application_window import ApplicationWindow

APP = QApplication(sys.argv + ['--style', 'material'])
AW = ApplicationWindow()

if not AW.engine.rootObjects():
    sys.exit(-1)

sys.exit(APP.exec_())
