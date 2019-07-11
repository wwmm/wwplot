# -*- coding: utf-8 -*-
"""
application window
"""

from PySide2.QtCore import QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QTabWidget

# from PySide2.QtCharts import QtCharts
from table import Table


class ApplicationWindow(QObject):
    """
    Class that handles the main window
    """

    def __init__(self):
        QObject.__init__(self)

        self.window = QUiLoader().load("ui/application_window.ui")

        self.tab_widget = self.window.findChild(QTabWidget, "tab_widget")
        button_add_tab = self.window.findChild(QPushButton, "button_add_tab")

        button_add_tab.clicked.connect(self.add_tab)

        self.window.show()

    def add_tab(self):
        """
            Add a tab when the button button_add_tab is clicked
        """

        self.tab_widget.addTab(Table(), "table")
