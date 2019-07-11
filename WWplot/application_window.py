# -*- coding: utf-8 -*-
"""
application window
"""

from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QObject
from PySide2.QtGui import QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QTabWidget

from table import Table


class ApplicationWindow(QObject):
    """
    Class that handles the main window
    """

    def __init__(self):
        QObject.__init__(self)

        self.tables = []

        loader = QUiLoader()

        loader.registerCustomWidget(QtCharts.QChartView)

        # print(loader.availableWidgets())

        self.window = loader.load("ui/application_window.ui")

        self.chart_view = self.window.findChild(QtCharts.QChartView, "chart_view")
        self.tab_widget = self.window.findChild(QTabWidget, "tab_widget")
        button_add_tab = self.window.findChild(QPushButton, "button_add_tab")

        button_add_tab.clicked.connect(self.add_tab)

        # Creating QChart
        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)

        self.chart_view.setChart(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.window.show()

    def add_tab(self):
        """
            Creates a new tab with a table when the button button_add_tab is clicked
        """

        table = Table()

        self.tables.append(table)

        table.name = "table " + str(len(self.tables))

        self.tab_widget.addTab(table.main_widget, table.name)
