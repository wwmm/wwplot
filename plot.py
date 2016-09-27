#!/usr/bin/python

from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg
from matplotlib.figure import Figure


class Plot():
    """Plot class based on Matplotlib"""

    def __init__(self, window, box, dpi_value=100):
        self.f = Figure(dpi=dpi_value)

        self.axes = self.f.add_subplot(111)

        self.canvas = FigureCanvasGTK3Agg(self.f)  # a Gtk.DrawingArea

        self.f.tight_layout()

        box.pack_start(self.canvas, True, True, 0)

        toolbar = NavigationToolbar2GTK3(self.canvas, window)

        box.pack_start(toolbar, False, False, 0)

        box.show_all()

    def plot(self, x, y, config_str):
        line_obj, = self.axes.plot(x, y, config_str)

        return line_obj

    def errorbar(self, x, x_err, y, y_err, config_str):
        line_obj, caplines, barlinecols = self.axes.errorbar(
            x, y, yerr=y_err, xerr=x_err, fmt=config_str, clip_on=False)

        return line_obj, caplines, barlinecols

    def hist(self, x):
        obj = self.axes.hist(x, facecolor="green", alpha=0.8, normed=True)

        return obj

    def set_xlabel(self, value):
        self.axes.set_xlabel(value)

    def set_ylabel(self, value):
        self.axes.set_ylabel(value)

    def set_title(self, value):
        self.axes.set_title(value)

    def set_grid(self, value):
        self.axes.grid(value)

    def set_margins(self, value):
        self.axes.margins(value)

    def tight_layout(self):
        self.f.tight_layout()

    def update(self):
        self.axes.relim()
        self.axes.autoscale_view(tight=True)
        self.f.tight_layout()
        self.canvas.queue_draw()
