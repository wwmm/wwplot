# -*- coding: utf-8 -*-
"""
application window
"""

from PySide2.QtCore import QObject
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtCore import QUrl
from table_model import TableModel


class ApplicationWindow(QObject):
    """
    Class that handles the main window
    """

    def __init__(self):
        QObject.__init__(self)

        self.engine = QQmlApplicationEngine()

        qmlRegisterType(TableModel, "wwplot", 1, 0, "TableModel")

        self.engine.load(QUrl("qml/application_window.qml"))
