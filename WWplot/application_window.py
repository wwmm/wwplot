# -*- coding: utf-8 -*-

from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QObject, Qt
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

        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setTitleText("x")
        self.axis_x.setRange(-10, 10)
        self.axis_x.setTickCount(5)
        self.axis_x.setLabelFormat("%.2f")

        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setTitleText("y")
        self.axis_y.setRange(-10, 10)
        self.axis_y.setTickCount(5)
        self.axis_y.setLabelFormat("%.2f")

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.chart_view.setChart(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.add_tab()

        self.window.show()

    def add_tab(self):
        table = Table()

        self.chart.addSeries(table.series)

        table.series.attachAxis(self.axis_x)
        table.series.attachAxis(self.axis_y)

        table.series.pointAdded.connect(self.chart_data_changed)
        table.series.pointReplaced.connect(self.chart_data_changed)
        table.series.pointRemoved.connect(self.chart_data_changed)

        self.tables.append(table)

        self.tab_widget.addTab(table.main_widget, "table " + str(len(self.tables)))

    def remove_tab(self, index):
        widget = self.tab_widget.widget(index)

        self.tab_widget.removeTab(index)

        for t in self.tables:
            if t.main_widget == widget:
                self.chart.removeSeries(t.series)

                self.tables.remove(t)

                self.chart_data_changed(0)

                break

    def chart_data_changed(self, index):
        Xmin, Xmax, Ymin, Ymax = 0, 0, 0, 0

        for table in self.tables:
            xmin, xmax, ymin, ymax = table.model.get_min_max_xy()

            if xmin < Xmin:
                Xmin = xmin

            if xmax > Xmax:
                Xmax = xmax

            if ymin < Ymin:
                Ymin = ymin

            if ymax > Ymax:
                Ymax = ymax

        self.axis_x.setRange(Xmin, Xmax)
        self.axis_y.setRange(Ymin, Ymax)
