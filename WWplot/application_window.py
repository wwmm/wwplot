# -*- coding: utf-8 -*-

import os

from PySide2.QtCore import QFile, QObject
from PySide2.QtGui import QColor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QFileDialog, QFrame, QGraphicsDropShadowEffect,
                               QLineEdit, QPushButton, QTabWidget)
from WWplot.plot import Plot
from WWplot.table import Table


class ApplicationWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.module_path = os.path.dirname(__file__)

        self.show_grid = True

        self.tables = []

        # loading widgets from designer file

        loader = QUiLoader()

        # print(loader.availableWidgets())

        loader.registerCustomWidget(Plot)

        self.window = loader.load(self.module_path + "/ui/application_window.ui")

        plot_frame = self.window.findChild(QFrame, "plot_frame")
        plot_settings_frame = self.window.findChild(QFrame, "plot_settings_frame")
        self.plot = self.window.findChild(Plot, "plot")
        self.tab_widget = self.window.findChild(QTabWidget, "tab_widget")
        self.xtitle = self.window.findChild(QLineEdit, "x_axis_title")
        self.ytitle = self.window.findChild(QLineEdit, "y_axis_title")
        button_add_tab = self.window.findChild(QPushButton, "button_add_tab")
        button_reset_zoom = self.window.findChild(QPushButton, "reset_zoom")
        button_save_image = self.window.findChild(QPushButton, "save_image")

        # signal connection

        self.tab_widget.tabCloseRequested.connect(self.remove_tab)
        self.xtitle.returnPressed.connect(lambda: self.update_plot())
        self.ytitle.returnPressed.connect(lambda: self.update_plot())
        button_add_tab.clicked.connect(self.add_tab)
        button_reset_zoom.clicked.connect(lambda: self.update_plot())
        button_save_image.clicked.connect(self.save_image)

        # init plot class

        self.plot.set_grid(self.show_grid)

        # 1 tab by default

        self.add_tab()

        # custom stylesheet

        style_file = QFile(self.module_path + "/ui/custom.css")
        style_file.open(QFile.ReadOnly)

        self.window.setStyleSheet(style_file.readAll().data().decode("utf-8"))

        style_file.close()

        # effects

        self.tab_widget.setGraphicsEffect(self.card_shadow())
        plot_frame.setGraphicsEffect(self.card_shadow())
        plot_settings_frame.setGraphicsEffect(self.card_shadow())
        button_add_tab.setGraphicsEffect(self.button_shadow())
        button_reset_zoom.setGraphicsEffect(self.button_shadow())
        button_save_image.setGraphicsEffect(self.button_shadow())

        self.window.show()

    def button_shadow(self):
        effect = QGraphicsDropShadowEffect(self.window)

        effect.setColor(QColor(0, 0, 0, 100))
        effect.setXOffset(1)
        effect.setYOffset(1)
        effect.setBlurRadius(5)

        return effect

    def card_shadow(self):
        effect = QGraphicsDropShadowEffect(self.window)

        effect.setColor(QColor(0, 0, 0, 100))
        effect.setXOffset(2)
        effect.setYOffset(2)
        effect.setBlurRadius(5)

        return effect

    def add_tab(self):
        table = Table()

        table.model.dataChanged.connect(self.data_changed)
        table.legend.returnPressed.connect(lambda: self.update_plot())
        table.fit.finished.connect(lambda: self.update_plot())
        table.chart_type_changed.connect(lambda: self.update_plot())

        self.tables.append(table)

        self.tab_widget.addTab(table.main_widget, "table " + str(len(self.tables)))

        self.update_plot()

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
        self.plot.set_xlabel(self.xtitle.displayText())
        self.plot.set_ylabel(self.ytitle.displayText())

        self.plot.set_margins(0.1)

        for t, n in zip(self.tables, range(len(self.tables))):
            legend = t.legend.displayText()

            if legend == "":
                legend = "table " + str(n)

            if not t.do_histogram:
                self.plot.errorbar(t.model.data_x, t.model.data_xerr, t.model.data_y, t.model.data_yerr, n, legend)

                self.plot.axes.legend()

                if t.show_fit_curve:
                    fit_y = t.fit.fit_function(t.fit.parameters, t.model.data_x)

                    self.plot.plot(t.model.data_x, fit_y, n)
            else:
                hist_values, bins = self.plot.hist(t.model.data_x, n, legend)

                t.hist_x = bins
                t.hist_count = hist_values

                if t.show_fit_curve:
                    fit_y = t.fit.fit_function(t.fit.parameters, bins)

                    self.plot.plot(bins, fit_y, n)

        self.plot.redraw_canvas()

    def save_image(self):
        home = os.path.expanduser("~")

        file_types = "PNG (*.png);; JPEG (*.jpg);; PDF (*.pdf);; SVG (*.svg)"

        path = QFileDialog.getSaveFileName(self.window, "Save Image",  home +
                                           "/image.png", file_types, "PNG (*.png)")[0]

        if path != "":
            self.plot.save_image(path)
