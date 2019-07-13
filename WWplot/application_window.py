# -*- coding: utf-8 -*-

from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QObject
from PySide2.QtGui import QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QTabWidget

from table import Table


class ApplicationWindow(QObject):
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

        self.tab_widget.tabCloseRequested.connect(self.remove_tab)
        button_add_tab.clicked.connect(self.add_tab)

        # Creating QChart
        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)

        self.chart_view.setChart(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.add_tab()

        self.window.show()

    def add_tab(self):
        table = Table()

        self.tables.append(table)

        self.tab_widget.addTab(table.main_widget, "table " + str(len(self.tables)))

    def remove_tab(self, index):
        widget = self.tab_widget.widget(index)

        self.tab_widget.removeTab(index)

        for t in self.tables:
            if t.main_widget == widget:
                self.tables.remove(t)

                break
