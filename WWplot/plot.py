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
