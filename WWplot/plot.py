# -*- coding: utf-8 -*-

from matplotlib import rcParams
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg,
                                                NavigationToolbar2QT)
from matplotlib.figure import Figure
from PySide2.QtWidgets import QSizePolicy

rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Roboto"]
rcParams["font.size"] = 14
rcParams["legend.fontsize"] = "small"
rcParams["figure.titlesize"] = "medium"
rcParams["xtick.labelsize"] = "medium"
rcParams["ytick.labelsize"] = "medium"
rcParams["markers.fillstyle"] = "none"


class Plot(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.fig = Figure()

        FigureCanvasQTAgg.__init__(self, self.fig)

        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)

        self.axes.tick_params(direction="in")

        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        self.setSizePolicy(size_policy)

        self.toolbar = NavigationToolbar2QT(self, parent)
        self.toolbar.setSizePolicy(size_policy)

        self.markers = ("o", "s", "v", "P", "*", "D", "x", ">")
        self.colors = ("b", "g", "r", "c", "m", "y", "k")

    def plot(self, x, y, marker_idx):
        line_obj, = self.axes.plot(x, y, self.colors[marker_idx] + "-")

        return line_obj

    def errorbar(self, x, x_err, y, y_err, marker_idx, legenda):
        myfmt = self.colors[marker_idx] + self.markers[marker_idx]

        line_obj, caplines, barlinecols = self.axes.errorbar(x, y, yerr=y_err, xerr=x_err, fmt=myfmt, label=legenda,
                                                             clip_on=True, capsize=5)

        return line_obj, caplines, barlinecols

    def hist(self, x):
        obj = self.axes.hist(x, facecolor="green", alpha=0.8, density=True)

        return obj

    def set_xlabel(self, value):
        self.axes.set_xlabel(value)

    def set_ylabel(self, value):
        self.axes.set_ylabel(value)

    def set_title(self, value):
        self.axes.set_title(value)

    def set_grid(self, value):
        if value:
            self.axes.grid(b=value, linestyle="--")
        else:
            self.axes.grid(b=value)

    def set_margins(self, value):
        self.axes.margins(value)

    def tight_layout(self):
        self.fig.tight_layout()

    def redraw_canvas(self):
        self.axes.relim()
        self.axes.autoscale_view(tight=True)
        self.fig.tight_layout()

        self.draw_idle()
