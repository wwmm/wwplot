# -*- coding: utf-8 -*-

from PySide2.QtCore import QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QPushButton, QTabWidget, QVBoxLayout

from table import Table
from plot import Plot


class ApplicationWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.do_histogram = False
        self.show_grid = True
        self.xtitle = "x"
        self.ytitle = "y"
        self.plot_title = "title"

        self.tables = []

        self.window = QUiLoader().load("ui/application_window.ui")

        self.plot_layout = self.window.findChild(QVBoxLayout, "plot_layout")
        self.tab_widget = self.window.findChild(QTabWidget, "tab_widget")
        button_add_tab = self.window.findChild(QPushButton, "button_add_tab")

        self.tab_widget.tabCloseRequested.connect(self.remove_tab)
        button_add_tab.clicked.connect(self.add_tab)

        self.plot = Plot(self.window)

        self.plot.setMinimumSize(640, 480)
        self.plot.set_grid(self.show_grid)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        self.plot.set_title(self.plot_title)
        self.plot.tight_layout()

        self.plot_layout.addWidget(self.plot)
        self.plot_layout.addWidget(self.plot.toolbar)

        self.add_tab()

        self.window.show()

    def add_tab(self):
        table = Table()

        table.model.dataChanged.connect(self.data_changed)

        self.tables.append(table)

        self.tab_widget.addTab(table.main_widget, "table " + str(len(self.tables)))

    def remove_tab(self, index):
        widget = self.tab_widget.widget(index)

        self.tab_widget.removeTab(index)

        for t in self.tables:
            if t.main_widget == widget:
                self.tables.remove(t)

                self.update_plot()

                break

    def data_changed(self, top_left_index, bottom_right_index, roles):
        self.update_plot()

    def update_plot(self):
        self.plot.axes.clear()
        self.plot.set_grid(self.show_grid)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        self.plot.set_title(self.plot_title)
