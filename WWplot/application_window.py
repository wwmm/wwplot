# -*- coding: utf-8 -*-
"""
application window
"""

from PySide2.QtCore import QObject
from PySide2.QtQml import QQmlApplicationEngine


class ApplicationWindow(QObject):
    """
    Class that handles the main window
    """

    def __init__(self):
        QObject.__init__(self)

        self.engine = QQmlApplicationEngine()

        self.engine.load("qml/application_window.qml")

        self.window = self.engine.rootObjects()[0]
