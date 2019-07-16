# -*- coding: utf-8 -*-

from PySide2.QtCore import QFile, QObject, Qt
from PySide2.QtGui import QColor, QFontDatabase
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QGraphicsDropShadowEffect, QPushButton,
                               QTabWidget, QVBoxLayout)

from plot import Plot
from table import Table


class ApplicationWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.do_histogram = False
        self.show_grid = True
        self.xtitle = "x"
        self.ytitle = "y"
        self.plot_title = "title"

        self.tables = []

        self.add_fonts()

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

        self.plot_layout.setAlignment(Qt.AlignTop)
        self.plot_layout.addWidget(self.plot.toolbar)
        self.plot_layout.addWidget(self.plot)

        self.add_tab()

        style_file = QFile("ui/custom.css")
        style_file.open(QFile.ReadOnly)

        self.window.setStyleSheet(style_file.readAll().data().decode("utf-8"))

        style_file.close()

        self.tab_widget.setGraphicsEffect(self.card_shadow())
        button_add_tab.setGraphicsEffect(self.button_shadow())

        self.window.show()

    def add_fonts(self):
        if QFontDatabase.addApplicationFont("ui/MaterialIcons-Regular.ttf") == -1:
            print("failed to add font ui/MaterialIcons-Regular")

    def button_shadow(self):
        effect = QGraphicsDropShadowEffect(self.window)

        effect.setColor(QColor(0, 0, 0, 100))
        effect.setXOffset(0)
        effect.setYOffset(1)
        effect.setBlurRadius(5)

        return effect

    def card_shadow(self):
        effect = QGraphicsDropShadowEffect(self.window)

        effect.setColor(QColor(0, 0, 0, 100))
        effect.setXOffset(1)
        effect.setYOffset(1)
        effect.setBlurRadius(5)

        return effect

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

        if not self.do_histogram:
            self.plot.set_margins(0.1)

            for t, n in zip(self.tables, range(len(self.tables))):
                self.plot.errorbar(t.model.data_x, t.model.data_xerr, t.model.data_y, t.model.data_yerr, n,
                                   'table ' + str(n))

                self.plot.axes.legend()

                # if len(t.fit_x) > 0:
                #     self.plot.plot(t.fit_x, t.fit_y, 'r-')
        else:
            self.plot.set_margins(0.0)

        self.plot.redraw_canvas()
