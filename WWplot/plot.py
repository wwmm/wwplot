# -*- coding: utf-8 -*-

from matplotlib import rcParams
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy

rcParams["font.size"] = 14
rcParams["legend.fontsize"] = "small"
rcParams["figure.titlesize"] = "medium"
rcParams["xtick.labelsize"] = "medium"
rcParams["ytick.labelsize"] = "medium"
rcParams["markers.fillstyle"] = "none"


class Plot(FigureCanvasQTAgg):
    mouse_motion = Signal(float, float)

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

        self.markers = ("o", "s", "v", "P", "*", "D", "x", ">")
        self.colors = ("#2196f3", "#f44336", "#4caf50", "#ff9800", "#607d8b", "#673ab7", "#795548")

        self.rectangle = RectangleSelector(self.axes, self.rectangle_callback, useblit=True,
                                           button=[1],  # only left button
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=False)

        # self.rectangle.artists[0].set_facecolor('#ffc400')
        # self.rectangle.artists[0].set_edgecolor('black')

        # rectprops=dict(facecolor='#ffc400', edgecolor='black',
        #   alpha=0.2, fill=True),

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

    def plot(self, x, y, marker_idx):
        line_obj, = self.axes.plot(x, y, color=self.colors[marker_idx], linestyle="-")

        return line_obj

    def errorbar(self, x, x_err, y, y_err, marker_idx, legenda):
        line_obj, caplines, barlinecols = self.axes.errorbar(x, y, yerr=y_err, xerr=x_err,
                                                             marker=self.markers[marker_idx],
                                                             color=self.colors[marker_idx], linestyle="None",
                                                             label=legenda,
                                                             clip_on=True, capsize=5)

        return line_obj, caplines, barlinecols

    def hist(self, x, marker_idx, legenda):
        """
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram_bin_edges.html#numpy.histogram_bin_edges

        auto : Maximum of the ‘sturges’ and ‘fd’ estimators. Provides good all around performance.
        """

        n, bins, patches = self.axes.hist(x, bins="auto", facecolor=self.colors[marker_idx], label=legenda, alpha=0.5,
                                          density=True, rwidth=0.85)

        # last bin element has to be removed so it has the same size as n

        return n, bins[:-1]

    def set_xlabel(self, value):
        self.axes.set_xlabel(value)

    def set_ylabel(self, value):
        self.axes.set_ylabel(value)

    def set_title(self, value):
        self.axes.set_title(value)

    def set_grid(self, value):
        if value:
            self.axes.grid(visible=value, linestyle="--")
        else:
            self.axes.grid(visible=value)

    def set_margins(self, value):
        self.axes.margins(value)

    def tight_layout(self):
        self.fig.tight_layout()

    def redraw_canvas(self):
        self.axes.relim()
        self.axes.autoscale_view(tight=True)

        self.fig.tight_layout()

        self.axes.legend().set_draggable(True)  # has to be called after tight_layout

        self.draw_idle()

    def rectangle_callback(self, press_event, release_event):
        x1_data, y1_data = press_event.xdata, press_event.ydata
        x2_data, y2_data = release_event.xdata, release_event.ydata

        self.axes.set_xlim(x1_data, x2_data)
        self.axes.set_ylim(y1_data, y2_data)

        self.draw_idle()

    def save_image(self, path):
        self.fig.savefig(path)

    def on_mouse_motion(self, event):
        x_data, y_data = event.xdata, event.ydata

        self.mouse_motion.emit(x_data, y_data)
