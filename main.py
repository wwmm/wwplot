#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import gi
import numpy as np

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from fit import Fit
from plot import Plot


class WWplot(Gtk.Application):
    """Main class."""

    def __init__(self):
        Gtk.Application.__init__(self, application_id="wwmm.wwplot")

        self.selected_row = None
        self.do_histogram = False

    def do_startup(self):
        Gtk.Application.do_startup(self)

        main_ui_builder = Gtk.Builder()
        menu_builder = Gtk.Builder()

        main_ui_builder.add_from_file("ui.glade")
        menu_builder.add_from_file("menu.glade")

        handlers = {
            "onQuit": self.onQuit,
            "onXEdited": self.onXEdited,
            "onXerrEdited": self.onXerrEdited,
            "onYEdited": self.onYEdited,
            "onYerrEdited": self.onYerrEdited,
            "onAdd": self.onAdd,
            "onRemove": self.onRemove,
            "onSwapColumns": self.onSwapColumns,
            "onSelectionChanged": self.onSelectionChanged,
            "onFitFunctionChanged": self.onFitFunctionChanged,
            "onFit": self.onFit,
            "onModeChanged": self.onModeChanged
        }

        menu_handlers = {
            "onXtitleChanged": self.onXtitleChanged,
            "onYtitleChanged": self.onYtitleChanged,
            "onTitleChanged": self.onTitleChanged
        }

        main_ui_builder.connect_signals(handlers)
        menu_builder.connect_signals(menu_handlers)

        self.window = main_ui_builder.get_object("MainWindow")

        headerbar = main_ui_builder.get_object("headerbar")

        self.window.set_titlebar(headerbar)
        self.window.set_application(self)

        self.xerr_column = main_ui_builder.get_object("xerr_column")
        self.y_column = main_ui_builder.get_object("y_column")
        self.yerr_column = main_ui_builder.get_object("yerr_column")

        self.liststore = main_ui_builder.get_object("liststore")

        self.fitfunc = main_ui_builder.get_object("fitfunc")

        self.button_switch_xy = main_ui_builder.get_object("button_switch_xy")

        self.create_appmenu()

        self.window.show_all()

        self.init_menu(main_ui_builder, menu_builder)
        self.init_plot(main_ui_builder)
        self.init_fit(main_ui_builder)

    def do_activate(self):
        self.window.present()

    def create_appmenu(self):
        menu = Gio.Menu()

        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")

        self.set_app_menu(menu)

        # option "about"
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.onAbout)
        self.add_action(about_action)

        # option "quit"
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.onQuit)
        self.add_action(quit_action)

    def onQuit(self, event, data):
        self.quit()

    def onXEdited(self, renderer, row_id, value):
        self.liststore[row_id][0] = float(value.replace(',', '.'))

        self.updatePlot()

    def onXerrEdited(self, renderer, row_id, value):
        self.liststore[row_id][1] = float(value.replace(',', '.'))

        self.updatePlot()

    def onYEdited(self, renderer, row_id, value):
        self.liststore[row_id][2] = float(value.replace(',', '.'))

        self.updatePlot()

    def onYerrEdited(self, renderer, row_id, value):
        self.liststore[row_id][3] = float(value.replace(',', '.'))

        self.updatePlot()

    def onAdd(self, button):
        self.liststore.append([0, 0, 0, 0])

        self.updatePlot()

    def onRemove(self, button):
        if self.selected_row is not None:
            self.liststore.remove(self.selected_row)

            self.updatePlot()

    def onSwapColumns(self, button):
        row_iter = self.liststore.get_iter_first()

        while row_iter is not None:
            y, yerr, x, xerr = self.liststore.get(row_iter, 0, 1, 2, 3)

            self.liststore.set(row_iter, 0, x, 1, xerr, 2, y, 3, yerr)

            row_iter = self.liststore.iter_next(row_iter)

        self.updatePlot()
        self.clear_fitlog()

    def onSelectionChanged(self, selection):
        model, self.selected_row = selection.get_selected()

    def init_menu(self, main_ui_builder, menu_builder):
        button = main_ui_builder.get_object("popover_button")
        menu = menu_builder.get_object("menu")
        xtitle = menu_builder.get_object("xtitle")
        ytitle = menu_builder.get_object("ytitle")
        plot_title = menu_builder.get_object("plot_title")

        self.xtitle = xtitle.get_text()
        self.ytitle = ytitle.get_text()
        self.plot_title = plot_title.get_text()

        popover = Gtk.Popover.new(button)
        popover.props.transitions_enabled = True
        popover.add(menu)

        def on_click(arg):
            if popover.get_visible():
                popover.hide()
            else:
                popover.show_all()

        button.connect("clicked", on_click)

    def init_plot(self, main_ui_builder):
        plot_box = main_ui_builder.get_object("plot")

        self.x = np.array([])
        self.xerr = np.array([])
        self.y = np.array([])
        self.yerr = np.array([])

        # setting plot
        self.plot = Plot(self.window, plot_box)
        self.plot.set_grid(True)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        self.plot.set_title(self.plot_title)
        self.plot.tight_layout()

    def updatePlot(self):
        self.plot.axes.clear()
        self.plot.set_grid(True)
        self.plot.set_xlabel(self.xtitle)
        self.plot.set_ylabel(self.ytitle)
        self.plot.set_title(self.plot_title)

        row_iter = self.liststore.get_iter_first()

        x, xerr, y, yerr = [], [], [], []

        while row_iter is not None:
            c0, c1, c2, c3 = self.liststore.get(row_iter, 0, 1, 2, 3)

            x.append(c0)
            xerr.append(c1)
            y.append(c2)
            yerr.append(c3)

            row_iter = self.liststore.iter_next(row_iter)

        self.x = np.array(x)
        self.xerr = np.array(xerr)
        self.y = np.array(y)
        self.yerr = np.array(yerr)

        if self.do_histogram:
            self.plot.set_margins(0.0)

            self.hist_count, self.hist_bin, patches = self.plot.hist(self.x)
        else:
            self.plot.set_margins(0.03)

            self.plot.errorbar(self.x, self.xerr, self.y, self.yerr, 'bo')

        self.plot.update()

    def onXtitleChanged(self, button):
        self.xtitle = button.get_text()
        self.plot.set_xlabel(self.xtitle)
        self.plot.update()

    def onYtitleChanged(self, button):
        self.ytitle = button.get_text()
        self.plot.set_ylabel(self.ytitle)
        self.plot.update()

    def onTitleChanged(self, button):
        self.plot_title = button.get_text()
        self.plot.set_title(self.plot_title)
        self.plot.update()

    def init_fit(self, main_ui_builder):
        fitfunc = main_ui_builder.get_object("fitfunc")
        self.fit_listbox = main_ui_builder.get_object("fit_listbox")

        self.fit = Fit(maxit=200)
        self.fit.init_function(fitfunc.get_text())

    def onFitFunctionChanged(self, button):
        self.fit.init_function(button.get_text())

    def clear_fitlog(self):
        children = self.fit_listbox.get_children()

        for child in children:
            self.fit_listbox.remove(child)

    def build_fitlog(self, result, result_err, stopreason):
        self.clear_fitlog()

        row = Gtk.ListBoxRow()
        row.add(Gtk.Label("Fit Output"))

        self.fit_listbox.add(row)

        for n in range(0, len(result)):
            label = "P[" + str(n) + "] = " + '{:.6}'.format(result[n]) + " +- "
            label = label + '{:.6}'.format(result_err[n])

            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(label))

            self.fit_listbox.add(row)

        row = Gtk.ListBoxRow()
        row.add(Gtk.Label())

        self.fit_listbox.add(row)

        for reason in stopreason:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(reason))

            self.fit_listbox.add(row)

        self.fit_listbox.show_all()

    def onFit(self, button):
        if len(self.x) > 1:
            self.updatePlot()

            if self.do_histogram is False:
                self.fit.set_data(self.x, self.y, self.xerr, self.yerr)
            else:
                self.fit.set_data(self.hist_bin[:-1], self.hist_count)

            stopreason = self.fit.run()

            result = self.fit.output
            result_err = self.fit.output_err

            self.build_fitlog(result, result_err, stopreason)

            func = self.fit.fit_function

            if self.do_histogram is False:
                self.plot.plot(self.x, func(result, self.x), "r-")
            else:
                self.plot.plot(
                    self.hist_bin[:-1], func(result, self.hist_bin[:-1]), "r-")

            self.plot.update()

    def onModeChanged(self, button, state):
        if state is True:  # do histogram
            self.do_histogram = True

            self.xerr_column.set_visible(False)
            self.y_column.set_visible(False)
            self.yerr_column.set_visible(False)

            equation = "(1.0 / (P[0] * sqrt(2 * pi))) * "
            equation = equation + "exp(- (x - P[1])**2 / (2 * P[0]**2))"

            self.fitfunc.set_text(equation)

            self.button_switch_xy.hide()
        else:  # do xy plot
            self.do_histogram = False

            self.xerr_column.set_visible(True)
            self.y_column.set_visible(True)
            self.yerr_column.set_visible(True)

            equation = "P[0] * x + P[1]"

            self.fitfunc.set_text(equation)

            self.button_switch_xy.show_all()

        self.updatePlot()
        self.clear_fitlog()

    def onAbout(self, action, parameter):
        builder = Gtk.Builder()

        builder.add_from_file("about.glade")

        dialog = builder.get_object("about_dialog")

        dialog.set_transient_for(self.window)

        dialog.show()

if __name__ == "__main__":
    w = WWplot()

    exit_status = w.run(sys.argv)

    sys.exit(exit_status)
