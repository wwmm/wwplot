# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class Plot(FigureCanvasQTAgg):

    def __init__(self, parent=None, dpi_value=120):
        self.fig = Figure(dpi=dpi_value)

        FigureCanvasQTAgg.__init__(self, self.fig)

        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)

        self.axes.tick_params(direction='in')

        self.toolbar = NavigationToolbar2QT(self, parent)

        self.markers = ('o', 's', 'v', 'P', '*', 'D', 'x', '>')

    def plot(self, x, y, config_str):
        line_obj, = self.axes.plot(x, y, config_str)

        return line_obj

    def errorbar(self, x, x_err, y, y_err, marker_idx, legenda):
        line_obj, caplines, barlinecols = self.axes.errorbar(x, y, yerr=y_err, xerr=x_err, fmt=self.markers[marker_idx],
                                                             label=legenda, clip_on=True, capsize=5)

        return line_obj, caplines, barlinecols

    def hist(self, x):
        obj = self.axes.hist(x, facecolor='green', alpha=0.8, density=True)

        return obj

    def set_xlabel(self, value):
        self.axes.set_xlabel(value)

    def set_ylabel(self, value):
        self.axes.set_ylabel(value)

    def set_title(self, value):
        self.axes.set_title(value)

    def set_grid(self, value):
        if value:
            self.axes.grid(b=value, linestyle='--')
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
